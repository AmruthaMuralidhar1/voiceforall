# VoiceTech for All - Multilingual TTS Model

A Python notebook implementing a **multilingual Text-to-Speech (TTS) model** for Indian languages with **accent transfer** and **style transfer** capabilities.

## 🎯 Challenge Requirements - All Met ✅

- ✅ Multilingual Support (11 Indian languages)
- ✅ Text Normalization (Indian language preprocessing)
- ✅ Accent Transfer (5 accent types)
- ✅ Style Transfer (3 style types)
- ✅ Multi-speaker Model
- ✅ SYSPIN Dataset Integration
- ✅ Evaluation Metrics
- ✅ ONNX Export for Deployment

## 🗣️ Supported Languages (11 Total)

Hindi • Bengali • Marathi • Kannada • Telugu • Bhojpuri • Chhattisgarhi • Magahi • Maithili • Tamil • Malayalam

## 🏗️ Model Components

1. **IndianLanguageNormalizer** - Text preprocessing for Indian languages
2. **MultilingualTTS** - Main model (~2M parameters)
3. **AccentStyleTransferModule** - Accent & style control
4. **SYSPINDataset** - SYSPIN dataset loader
5. **TTSTrainer** - Training pipeline
6. **TTSInference** - Speech synthesis engine
7. **TTSEvaluator** - Quality metrics

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install torch torchaudio librosa numpy scipy matplotlib
```

### 2. Download SYSPIN Dataset
```bash
# Download from: https://spiredatasets.ee.iisc.ac.in/syspincorpus
# Extract to: ./syspin_data/
# Expected structure:
# syspin_data/
#   hi/metadata.json
#   hi/wavs/speaker_001/*.wav
#   bn/metadata.json
#   ... (other languages)
```

### 3. Run Notebook
```bash
jupyter notebook VoiceTech_for_All_TTS_Model.ipynb
```

### 4. Notebook Sections
1. Setup & Dependencies
2. Text Normalization
3. Model Architecture
4. Dataset Loading (SYSPIN)
5. Training Loop
6. Training Execution
7. Inference Engine
8. Evaluation Metrics
9. Multilingual Pipeline
10. Export & Deployment

## 📊 Model Configuration

| Parameter | Value |
|-----------|-------|
| Vocabulary Size | 500 tokens |
| Embedding Dim | 256 |
| Hidden Dim | 512 |
| Mel Bins | 80 |
| Total Parameters | ~2M |
| Accents | 5 types |
| Styles | 3 types |

## 🎓 Capabilities

✅ Train multilingual TTS models
✅ Synthesize speech in 11 languages
✅ Apply accent variations
✅ Apply style variations
✅ Evaluate model quality
✅ Export to ONNX
✅ Deploy to production

## 🔗 Resources

- **Challenge**: https://syspin.iisc.ac.in/voicetechforall
- **Dataset**: https://spiredatasets.ee.iisc.ac.in/syspincorpus
- **PyTorch**: https://pytorch.org
- **Librosa**: https://librosa.org

---

**Status**: ✅ Ready to Use


