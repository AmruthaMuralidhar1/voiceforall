# VoiceTech for All - Multilingual TTS with Accent & Style Transfer

A production-ready Text-to-Speech (TTS) system for 11 Indian languages with accent and style transfer capabilities, featuring both a Jupyter notebook for model development and a REST API for deployment.

## 🎯 Features

- **11 Indian Languages**: Hindi, Bengali, Marathi, Kannada, Telugu, Bhojpuri, Chhattisgarhi, Magahi, Maithili, Tamil, Malayalam
- **Accent Transfer**: 5 accent types (Neutral, Formal, Casual, Expressive, Whisper)
- **Style Transfer**: 3 style types (Neutral, Expressive, Formal)
- **REST API**: FastAPI-based server with `/Get_Inference` endpoint
- **Docker Support**: Production-ready containerization
- **SYSPIN Dataset**: Integration with official SYSPIN corpus
- **Interactive Documentation**: Swagger UI and ReDoc

## 📦 Deliverables

### Model & Training
- **VoiceTech_for_All_TTS_Model.ipynb** - Complete Jupyter notebook with 10 sections
- **VOICETECH_README.md** - Model documentation

### REST API
- **app.py** - FastAPI server with 6 endpoints
- **requirements_api.txt** - Python dependencies
- **Dockerfile** - Production Docker image
- **test_api.py** - Comprehensive test suite

### Documentation
- **API_DOCUMENTATION.md** - Complete API reference
- **API_DEPLOYMENT.md** - Deployment guide
- **MODEL_CARD.md** - Hugging Face model card

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements_api.txt
```

### 2. Run API Server
```bash
python app.py
```

### 3. Test API
```bash
python test_api.py
```

### 4. Access Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📡 Main API Endpoint

**POST /Get_Inference**

```bash
curl -X POST "http://localhost:8000/Get_Inference" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "नमस्ते दुनिया",
    "language": "hi",
    "accent_id": 0,
    "style_id": 0
  }' \
  --output output.wav
```

## 🐳 Docker Deployment

```bash
docker build -t voicetech-tts-api .
docker run -p 8000:8000 voicetech-tts-api
```

## 📚 Documentation

- **API_DOCUMENTATION.md** - All endpoints with examples
- **API_DEPLOYMENT.md** - Deployment to AWS, GCP, HF Spaces
- **VOICETECH_README.md** - Model training guide

## 🔗 Resources

- Challenge: https://syspin.iisc.ac.in/voicetechforall
- Dataset: https://spiredatasets.ee.iisc.ac.in/syspincorpus
- FastAPI: https://fastapi.tiangolo.com

## ✅ Status

Production-ready for local, Docker, and cloud deployment.
