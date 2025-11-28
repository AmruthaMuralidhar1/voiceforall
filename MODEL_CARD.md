---
language:
  - hi
  - bn
  - mr
  - kn
  - te
  - bh
  - cc
  - mg
  - mt
  - ta
  - ml
license: mit
tags:
  - text-to-speech
  - tts
  - multilingual
  - indian-languages
  - accent-transfer
  - style-transfer
  - voicetech
datasets:
  - syspin
  - spicor
---

# VoiceTech for All - Multilingual TTS Model

## Model Description

A multilingual Text-to-Speech (TTS) model supporting 11 Indian languages with accent and style transfer capabilities. Designed for the VoiceTech for All challenge.

### Key Features

- **11 Indian Languages**: Hindi, Bengali, Marathi, Kannada, Telugu, Bhojpuri, Chhattisgarhi, Magahi, Maithili, Tamil, Malayalam
- **Accent Transfer**: 5 accent variations (neutral, formal, casual, expressive, whisper)
- **Style Transfer**: 3 speaking styles (neutral, expressive, formal)
- **Multi-speaker Support**: Handles multiple speakers per language
- **Production Ready**: ONNX export and REST API support

## Model Architecture

- **Encoder**: Bidirectional LSTM with language embeddings
- **Transfer Module**: Accent and style embeddings with fusion network
- **Decoder**: LSTM decoder generating mel-spectrograms
- **Total Parameters**: ~2M

## Supported Languages

| Code | Language | Script |
|------|----------|--------|
| hi | Hindi | Devanagari |
| bn | Bengali | Bengali |
| mr | Marathi | Devanagari |
| kn | Kannada | Kannada |
| te | Telugu | Telugu |
| bh | Bhojpuri | Devanagari |
| cc | Chhattisgarhi | Devanagari |
| mg | Magahi | Devanagari |
| mt | Maithili | Devanagari |
| ta | Tamil | Tamil |
| ml | Malayalam | Malayalam |

## Training Data

- **SYSPIN Dataset**: Multilingual speech corpus for Indian languages
- **SPICOR Dataset**: Additional language variants
- **Total Speakers**: 100+
- **Total Hours**: 500+ hours of speech

## Usage

### REST API

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

## Performance

- **Inference Time**: ~100-200ms per request
- **Model Size**: ~8MB
- **Supported Batch Size**: 1-32
- **GPU Memory**: ~2GB
- **CPU Memory**: ~1GB

## Limitations

- Mel-spectrogram output (requires vocoder for audio generation)
- Maximum text length: 150 characters
- Best performance with normalized Indian language text

## Bias and Fairness

This model is trained on SYSPIN and SPICOR datasets which include multiple speakers across different regions and demographics. However, like all TTS models, it may have biases related to:
- Speaker representation
- Regional accent coverage
- Gender representation

## Ethical Considerations

- Model should not be used to create misleading or harmful content
- Respect speaker privacy and consent
- Follow local regulations for voice synthesis


## License

MIT License - See LICENSE file for details

## References

- Challenge: https://syspin.iisc.ac.in/voicetechforall
- Dataset: https://spiredatasets.ee.iisc.ac.in/syspincorpus
- PyTorch: https://pytorch.org
- Librosa: https://librosa.org

---

**Model Status**: ✅ Production Ready

