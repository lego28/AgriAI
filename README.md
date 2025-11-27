# AgriAI: Agricultural Intelligence System

## Overview

An integrated AI system for **multi-crop** farming (coconut, coffee, cotton, oil palm) with:
- **Disease detection** (image + text-based) with ML models
- **Yield prediction** using ripeness classification and biomass analysis
- **Biomass optimization** with ESG sustainability scoring
- **Generative AI** (HuggingFace Gradio API) for knowledge retrieval
- **Web interfaces** for farmer access and ESG tracking

**Tech Stack**: Python 3.13 | Flask | PyTorch | LangChain | HuggingFace Gradio | Chroma

---

## 📁 Project Structure

```
AgriAI/
│
├── 🔧 CORE MODULES
│   ├── app.py                           # Flask app (legacy)
│   ├── server.py                        # Main server application
│   ├── classification.py                # Text classification
│   ├── imageclassification.py           # Multi-crop disease detection (CNN)
│   ├── search.py                        # Search engine
│   └── test_palmsense.py                # Testing suite
│
├── 🌴 AI MODULES
│   ├── rag_system.py                    # RAG system for knowledge retrieval
│   ├── palmchat.py                      # Oil palm disease chat
│   ├── palm_ripeness.py                 # Ripeness classifier + yield predictor
│   └── biomass_optimizer.py             # ESG + economics calculator
│
├── 🌐 WEB INTERFACE
│   ├── landing.html                     # Landing page
│   ├── ai_interface.html                # AI chat interface
│   ├── disease_detector.html            # Disease detection UI
│   ├── products.html                    # Products catalog
│   ├── subsidies.html                   # Government subsidies info
│   ├── esg.html                         # ESG dashboard
│   └── static/
│       ├── ai_app.js                    # AI interface logic
│       ├── ai_style.css                 # AI interface styling
│       ├── landing.js                   # Landing page logic
│       ├── landing.css                  # Landing page styling
│       ├── products.js                  # Products page logic
│       ├── products.css                 # Products page styling
│       ├── subsidies.js                 # Subsidies page logic
│       ├── subsidies.css                # Subsidies page styling
│       ├── esg.js                       # ESG dashboard logic
│       ├── esg.css                      # ESG dashboard styling
│       ├── theme-toggle.js              # Dark/light theme toggle
│       └── sessionimg/                  # User session images
│
├── 📚 KNOWLEDGE BASE
│   └── docs/
│       ├── diseases.txt                 # Disease management guide
│       ├── biomass_conversion.txt       # Conversion technologies & economics
│       ├── sustainability_metrics.txt   # ESG framework
│       └── yield_prediction.txt         # Ripeness guides & yield formulas
│
├── 🧠 MACHINE LEARNING MODELS
│   └── models/
│       ├── coconut_best.pth             # Coconut disease detection
│       ├── coffee_best.pth              # Coffee disease detection
│       ├── cotton_best.pth              # Cotton disease detection
│       ├── palm_best.pth                # Oil palm disease detection
│       └── crop_classifier.pth          # Multi-crop classifier
│
├── 📚 DOCUMENTATION
│   ├── README.md                        # This file
│   └── IMPLEMENTATION_SUMMARY.md        # Implementation notes
│
├── 🔌 UTILITIES
│   ├── utils/                           # Helper functions (empty)
│   ├── agri_knowledge/                  # Knowledge repository (empty)
│   ├── requirements.txt                 # Python dependencies
│   └── venv/                            # Virtual environment
│
└── 📦 BUILD
    ├── .dist/                           # Distribution files
    └── __pycache__/                     # Python cache
```

---

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Navigate to project
cd c:\Users\arcot\Downloads\AgriAI\AgriAI

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup Gemini API

```bash
# Get your Gemini API key from https://makersuite.google.com/app/apikey

# Set environment variable (PowerShell)
$env:GEMINI_API_KEY="your-api-key-here"

# Or add to .env file
# GEMINI_API_KEY=your-api-key-here
```

### 3. Run Application

```bash
# Start server
python server.py

# Or use legacy app
python app.py

# Visit http://localhost:5000 in browser
```


## 📚 Learning Resources

### Knowledge Base Files
- `docs/diseases.txt` - Disease management guide
- `docs/biomass_conversion.txt` - Technology & economics
- `docs/sustainability_metrics.txt` - ESG framework
- `docs/yield_prediction.txt` - Ripeness & yield guide

### Documentation
- `README.md` - This file
- `IMPLEMENTATION_SUMMARY.md` - Implementation notes
- Code docstrings - Every module has detailed documentation

### Research References
- RSPO (Roundtable on Sustainable Palm Oil) standards
- ISCC (International Sustainability & Carbon Certification)
- FAO (Food and Agriculture Organization) oil palm guides
- ResNet50 architecture for image classification

---

## 📄 License

This project is built on open-source components:
- Flask (BSD)
- PyTorch (BSD)
- LangChain (MIT)
- Chroma (Apache 2.0)

---

**Last Updated**: November 28, 2025
**Version**: 1.0.0
**Status**: Production Ready ✅

