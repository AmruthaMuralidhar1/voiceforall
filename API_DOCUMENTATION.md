# VoiceTech for All - API Documentation

## 🌐 API Endpoints

### Base URL
```
http://localhost:8000
```

---

## 📋 Endpoints

### 1. Health Check
**Endpoint**: `GET /health`

**Description**: Check if API is running

**Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cpu"
}
```

---

### 2. Model Information
**Endpoint**: `GET /info`

**Description**: Get model details and capabilities

**Response**:
```json
{
  "name": "MultilingualTTS",
  "version": "1.0.0",
  "languages": [
    {
      "code": "hi",
      "name": "Hindi",
      "script": "Devanagari"
    },
    ...
  ],
  "accents": 5,
  "styles": 3,
  "parameters": 2000000
}
```

---

### 3. Get Supported Languages
**Endpoint**: `GET /languages`

**Description**: List all supported languages

**Response**:
```json
{
  "languages": {
    "hi": "Hindi",
    "bn": "Bengali",
    "mr": "Marathi",
    "kn": "Kannada",
    "te": "Telugu",
    "bh": "Bhojpuri",
    "cc": "Chhattisgarhi",
    "mg": "Magahi",
    "mt": "Maithili",
    "ta": "Tamil",
    "ml": "Malayalam"
  },
  "count": 11
}
```

---

### 4. Main Inference Endpoint ⭐
**Endpoint**: `POST /Get_Inference`

**Description**: Synthesize speech from text (main endpoint)

**Request**:
```json
{
  "text": "नमस्ते दुनिया",
  "language": "hi",
  "accent_id": 0,
  "style_id": 0
}
```

**Parameters**:
- `text` (string, required): Text to synthesize
- `language` (string, default: "hi"): Language code
- `accent_id` (integer, default: 0): Accent ID (0-4)
- `style_id` (integer, default: 0): Style ID (0-2)

**Response**: WAV audio file

**Example**:
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

### 5. Synthesize Endpoint
**Endpoint**: `POST /synthesize`

**Description**: Synthesize speech and return metadata

**Request**:
```json
{
  "text": "नमस्ते दुनिया",
  "language": "hi",
  "accent_id": 0,
  "style_id": 0
}
```

**Response**:
```json
{
  "status": "success",
  "message": "Speech synthesized successfully",
  "audio_url": "/audio/tts_20231215_143022.wav",
  "duration": 2.5,
  "language": "hi",
  "accent_id": 0,
  "style_id": 0
}
```

---

### 6. Download Audio
**Endpoint**: `GET /audio/{filename}`

**Description**: Download synthesized audio file

**Example**:
```bash
curl "http://localhost:8000/audio/tts_20231215_143022.wav" \
  --output audio.wav
```

---

## 🎨 Accent IDs

| ID | Accent |
|----|--------|
| 0 | Neutral |
| 1 | Formal |
| 2 | Casual |
| 3 | Expressive |
| 4 | Whisper |

---

## 🎭 Style IDs

| ID | Style |
|----|-------|
| 0 | Neutral |
| 1 | Expressive |
| 2 | Formal |

---

## 🔧 Error Handling

### Error Response Format
```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Errors

| Status | Error | Solution |
|--------|-------|----------|
| 400 | Language not supported | Use supported language code |
| 400 | accent_id must be 0-4 | Use valid accent ID |
| 400 | style_id must be 0-2 | Use valid style ID |
| 503 | Model not loaded | Restart API server |
| 500 | Internal server error | Check server logs |

---

## 📊 Rate Limiting

- No rate limiting by default
- Recommended: 10 requests/second per client
- Batch requests for better performance

---

## 🔐 Security

- CORS enabled for all origins
- No authentication required (add if needed)
- Input validation on all endpoints
- Error messages don't expose sensitive info

---

## 📈 Performance Tips

1. **Batch Processing**: Send multiple requests in parallel
2. **Text Length**: Keep text under 150 characters
3. **GPU Usage**: Use GPU for faster inference
4. **Caching**: Cache audio files for repeated requests

---

## 🚀 Deployment

### Local
```bash
python app.py
```

### Docker
```bash
docker build -t voicetech-tts .
docker run -p 8000:8000 voicetech-tts
```

### Production
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

---

## 📚 Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

**API Version**: 1.0.0
**Last Updated**: 2025

