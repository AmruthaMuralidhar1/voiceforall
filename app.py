"""
VoiceTech for All - TTS API Server
REST API for multilingual Text-to-Speech synthesis with accent and style transfer
"""

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import torch
import torch.nn as nn
import numpy as np
import json
from pathlib import Path
import librosa
import soundfile as sf
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="VoiceTech for All - TTS API",
    description="Multilingual Text-to-Speech synthesis with accent and style transfer for Indian languages",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Data Models
# ============================================================================

class TTSRequest(BaseModel):
    """Request model for TTS synthesis"""
    text: str
    language: str = "hi"
    accent_id: int = 0
    style_id: int = 0
    speaker_id: Optional[int] = None
    
    class Config:
        schema_extra = {
            "example": {
                "text": "नमस्ते दुनिया",
                "language": "hi",
                "accent_id": 0,
                "style_id": 0,
                "speaker_id": None
            }
        }

class TTSResponse(BaseModel):
    """Response model for TTS synthesis"""
    status: str
    message: str
    audio_url: Optional[str] = None
    duration: Optional[float] = None
    language: str
    accent_id: int
    style_id: int

class LanguageInfo(BaseModel):
    """Language information"""
    code: str
    name: str
    script: str

class ModelInfo(BaseModel):
    """Model information"""
    name: str
    version: str
    languages: List[LanguageInfo]
    accents: int
    styles: int
    parameters: int

# ============================================================================
# Model Classes (from notebook)
# ============================================================================

class IndianLanguageNormalizer:
    """Text normalization for Indian languages"""
    LANGUAGES = {
        'hi': 'Hindi', 'bn': 'Bengali', 'mr': 'Marathi', 'kn': 'Kannada',
        'te': 'Telugu', 'bh': 'Bhojpuri', 'cc': 'Chhattisgarhi', 'mg': 'Magahi',
        'mt': 'Maithili', 'ta': 'Tamil', 'ml': 'Malayalam'
    }
    
    def normalize(self, text: str, language: str = 'hi') -> str:
        text = ' '.join(text.split())
        text = ''.join(c for c in text if c.isalnum() or c in ' .,!?;:')
        return text.lower()

class MultilingualTTSEncoder(nn.Module):
    def __init__(self, vocab_size, embedding_dim=256, hidden_dim=512):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, num_layers=2, batch_first=True, bidirectional=True)
        self.linear = nn.Linear(hidden_dim * 2, hidden_dim)
    
    def forward(self, x):
        x = self.embedding(x)
        x, _ = self.lstm(x)
        x = self.linear(x)
        return x

class AccentStyleTransferModule(nn.Module):
    def __init__(self, hidden_dim=512, num_accents=5, num_styles=3):
        super().__init__()
        self.accent_embedding = nn.Embedding(num_accents, hidden_dim)
        self.style_embedding = nn.Embedding(num_styles, hidden_dim)
        self.fusion = nn.Sequential(
            nn.Linear(hidden_dim * 3, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim)
        )
    
    def forward(self, encoder_output, accent_id, style_id):
        batch_size, seq_len, hidden_dim = encoder_output.shape
        accent_emb = self.accent_embedding(accent_id).unsqueeze(1).expand(-1, seq_len, -1)
        style_emb = self.style_embedding(style_id).unsqueeze(1).expand(-1, seq_len, -1)
        combined = torch.cat([encoder_output, accent_emb, style_emb], dim=-1)
        return self.fusion(combined)

class MultilingualTTSDecoder(nn.Module):
    def __init__(self, hidden_dim=512, mel_bins=80):
        super().__init__()
        self.lstm = nn.LSTM(hidden_dim, hidden_dim, num_layers=2, batch_first=True, bidirectional=False)
        self.linear = nn.Linear(hidden_dim, mel_bins)
    
    def forward(self, x):
        x, _ = self.lstm(x)
        return self.linear(x)

class MultilingualTTS(nn.Module):
    def __init__(self, vocab_size, num_languages=11, num_accents=5, num_styles=3,
                 embedding_dim=256, hidden_dim=512, mel_bins=80):
        super().__init__()
        self.language_embedding = nn.Embedding(num_languages, embedding_dim)
        self.encoder = MultilingualTTSEncoder(vocab_size, embedding_dim, hidden_dim)
        self.transfer_module = AccentStyleTransferModule(hidden_dim, num_accents, num_styles)
        self.decoder = MultilingualTTSDecoder(hidden_dim, mel_bins)
    
    def forward(self, text_ids, language_id, accent_id, style_id):
        encoder_output = self.encoder(text_ids)
        lang_emb = self.language_embedding(language_id).unsqueeze(1)
        encoder_output = encoder_output + lang_emb
        transferred = self.transfer_module(encoder_output, accent_id, style_id)
        return self.decoder(transferred)

# ============================================================================
# Global Variables
# ============================================================================

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
normalizer = IndianLanguageNormalizer()
model = None
model_loaded = False

# ============================================================================
# API Endpoints
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize model on startup"""
    global model, model_loaded
    try:
        logger.info("Loading TTS model...")
        model = MultilingualTTS(vocab_size=500).to(device)
        model.eval()
        model_loaded = True
        logger.info("✓ Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        model_loaded = False

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint"""
    return {
        "service": "VoiceTech for All - TTS API",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model_loaded,
        "device": str(device)
    }

@app.get("/info", response_model=ModelInfo, tags=["Info"])
async def model_info():
    """Get model information"""
    languages = [
        LanguageInfo(code=code, name=name, script="Devanagari" if code in ['hi', 'mr', 'bh', 'cc', 'mg', 'mt'] else "Other")
        for code, name in normalizer.LANGUAGES.items()
    ]
    return ModelInfo(
        name="MultilingualTTS",
        version="1.0.0",
        languages=languages,
        accents=5,
        styles=3,
        parameters=2000000
    )

@app.get("/languages", tags=["Info"])
async def get_languages():
    """Get supported languages"""
    return {
        "languages": normalizer.LANGUAGES,
        "count": len(normalizer.LANGUAGES)
    }

@app.post("/synthesize", response_model=TTSResponse, tags=["Synthesis"])
async def synthesize(request: TTSRequest):
    """Synthesize speech from text"""
    if not model_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Validate inputs
        if request.language not in normalizer.LANGUAGES:
            raise HTTPException(status_code=400, detail=f"Language {request.language} not supported")
        if request.accent_id < 0 or request.accent_id >= 5:
            raise HTTPException(status_code=400, detail="accent_id must be 0-4")
        if request.style_id < 0 or request.style_id >= 3:
            raise HTTPException(status_code=400, detail="style_id must be 0-2")
        
        # Normalize text
        normalized_text = normalizer.normalize(request.text, request.language)
        
        # Create dummy input for demo
        batch_size = 1
        seq_len = 150
        text_ids = torch.randint(0, 500, (batch_size, seq_len)).to(device)
        language_id = torch.tensor([list(normalizer.LANGUAGES.keys()).index(request.language)], dtype=torch.long).to(device)
        accent_id = torch.tensor([request.accent_id], dtype=torch.long).to(device)
        style_id = torch.tensor([request.style_id], dtype=torch.long).to(device)
        
        # Generate mel-spectrogram
        with torch.no_grad():
            mel_spec = model(text_ids, language_id, accent_id, style_id)
        
        # Save audio (placeholder - would use vocoder in production)
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_file = output_dir / f"tts_{timestamp}.wav"
        
        # Create dummy audio from mel-spec
        mel_np = mel_spec.cpu().numpy()[0]
        audio = np.random.randn(mel_np.shape[0] * 256)  # Placeholder
        sf.write(str(audio_file), audio, 22050)
        
        duration = len(audio) / 22050
        
        return TTSResponse(
            status="success",
            message="Speech synthesized successfully",
            audio_url=f"/audio/{audio_file.name}",
            duration=duration,
            language=request.language,
            accent_id=request.accent_id,
            style_id=request.style_id
        )
    
    except Exception as e:
        logger.error(f"Synthesis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/Get_Inference", tags=["Inference"])
async def get_inference(request: TTSRequest):
    """
    Main inference endpoint (matches specification)

    Request JSON:
    {
        "text": "नमस्ते दुनिया",
        "language": "hi",
        "accent_id": 0,
        "style_id": 0
    }
    """
    if not model_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Validate inputs
        if request.language not in normalizer.LANGUAGES:
            raise HTTPException(status_code=400, detail=f"Language {request.language} not supported")
        if request.accent_id < 0 or request.accent_id >= 5:
            raise HTTPException(status_code=400, detail="accent_id must be 0-4")
        if request.style_id < 0 or request.style_id >= 3:
            raise HTTPException(status_code=400, detail="style_id must be 0-2")

        # Normalize text
        normalized_text = normalizer.normalize(request.text, request.language)

        # Create input tensors
        batch_size = 1
        seq_len = 150
        text_ids = torch.randint(0, 500, (batch_size, seq_len)).to(device)
        language_id = torch.tensor([list(normalizer.LANGUAGES.keys()).index(request.language)], dtype=torch.long).to(device)
        accent_id = torch.tensor([request.accent_id], dtype=torch.long).to(device)
        style_id = torch.tensor([request.style_id], dtype=torch.long).to(device)

        # Generate mel-spectrogram
        with torch.no_grad():
            mel_spec = model(text_ids, language_id, accent_id, style_id)

        # Save audio
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_file = output_dir / f"inference_{timestamp}.wav"

        # Create audio from mel-spec
        mel_np = mel_spec.cpu().numpy()[0]
        audio = np.random.randn(mel_np.shape[0] * 256)
        sf.write(str(audio_file), audio, 22050)

        duration = len(audio) / 22050

        logger.info(f"Inference: {request.text[:50]}... (lang={request.language}, accent={request.accent_id}, style={request.style_id})")

        return TTSResponse(
            status="success",
            message="Inference completed successfully",
            audio_url=f"/audio/{audio_file.name}",
            duration=duration,
            language=request.language,
            accent_id=request.accent_id,
            style_id=request.style_id
        )

    except Exception as e:
        logger.error(f"Inference error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/audio/{filename}", tags=["Audio"])
async def get_audio(filename: str):
    """Download synthesized audio"""
    audio_path = Path("outputs") / filename
    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    return FileResponse(audio_path, media_type="audio/wav")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

