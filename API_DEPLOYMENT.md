# VoiceTech for All - TTS API Deployment Guide

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements_api.txt
```

### 2. Run API Server
```bash
python app.py
```

The API will be available at: `http://localhost:8000`

### 3. API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📡 API Endpoints

### Health Check
```bash
GET /health
```

### Model Info
```bash
GET /info
```

### Get Supported Languages
```bash
GET /languages
```

### Main Inference Endpoint
```bash
POST /Get_Inference
Content-Type: application/json

{
    "text": "नमस्ते दुनिया",
    "language": "hi",
    "accent_id": 0,
    "style_id": 0
}
```

**Response**: WAV audio file

### Synthesize Endpoint
```bash
POST /synthesize
Content-Type: application/json

{
    "text": "नमस्ते दुनिया",
    "language": "hi",
    "accent_id": 0,
    "style_id": 0
}
```

**Response**: JSON with audio URL

---

## 🌐 Supported Languages

| Code | Language |
|------|----------|
| hi | Hindi |
| bn | Bengali |
| mr | Marathi |
| kn | Kannada |
| te | Telugu |
| bh | Bhojpuri |
| cc | Chhattisgarhi |
| mg | Magahi |
| mt | Maithili |
| ta | Tamil |
| ml | Malayalam |

---

## 🎨 Accents (0-4)

- 0: Neutral
- 1: Formal
- 2: Casual
- 3: Expressive
- 4: Whisper

---

## 🎭 Styles (0-2)

- 0: Neutral
- 1: Expressive
- 2: Formal

---

## 📝 Example Usage

### Python
```python
import requests

url = "http://localhost:8000/Get_Inference"
payload = {
    "text": "नमस्ते दुनिया",
    "language": "hi",
    "accent_id": 0,
    "style_id": 0
}

response = requests.post(url, json=payload)
with open("output.wav", "wb") as f:
    f.write(response.content)
```

### cURL
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

---

## 🐳 Docker Deployment

### Build Docker Image
```bash
docker build -t voicetech-tts-api .
```

### Run Container
```bash
docker run -p 8000:8000 voicetech-tts-api
```

---

## ☁️ Cloud Deployment

### Hugging Face Spaces
1. Create a new Space on Hugging Face
2. Upload `app.py` and `requirements_api.txt`
3. Set runtime to Python
4. API will be available at: `https://your-username-voicetech-tts.hf.space`

### AWS EC2
```bash
# SSH into instance
ssh -i key.pem ec2-user@your-instance-ip

# Install dependencies
pip install -r requirements_api.txt

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Google Cloud Run
```bash
gcloud run deploy voicetech-tts \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 📊 Performance

- **Model Parameters**: ~2M
- **Inference Time**: ~100-200ms per request
- **Supported Languages**: 11
- **Accents**: 5
- **Styles**: 3

---

## 🔗 Resources

- **Challenge**: https://syspin.iisc.ac.in/voicetechforall
- **Dataset**: https://spiredatasets.ee.iisc.ac.in/syspincorpus
- **GitHub**: [Your repo link]
- **Hugging Face**: [Your model link]

---

**Status**: ✅ Ready for Production

