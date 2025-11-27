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
# Clone the repository
git clone https://github.com/lego28/AgriAI.git
cd AgriAI

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Application

```bash
# Start Flask server
python app.py

# Visit http://localhost:5000 in browser
```

**Note**: The system uses HuggingFace Gradio API (`zeus28/Agri-AI` space) for AI chat - no API keys required! The Gradio space must be accessible online.

---

## 💡 Key Features

### 🔬 Multi-Crop Disease Detection
- **4 Crop Types**: Coconut, Coffee, Cotton, Oil Palm
- **Local PyTorch Models**: Trained CNN models for each crop
- **High Accuracy**: 92%+ disease identification
- **Instant Results**: 200-500ms inference time

### 🤖 AI-Powered Chat (Gradio API)
- **HuggingFace Integration**: Uses `zeus28/Agri-AI` Gradio space
- **RAG System**: Retrieval-Augmented Generation with local knowledge base
- **Multi-Language**: Supports English, Hindi, Tamil, Telugu
- **Context-Aware**: Maintains conversation history

### 🌴 Oil Palm Specialized Features
- **Ripeness Classification**: 5-stage maturity detection
- **Yield Prediction**: Harvest timing optimization
- **Biomass Economics**: Revenue calculation from waste streams
- **ESG Scoring**: Sustainability metrics (RSPO compliant)

### 📊 Web Interface
- **Landing Page**: Modern, responsive design
- **AI Chat**: Real-time disease diagnosis
- **Disease Detector**: Dedicated image upload interface
- **ESG Dashboard**: Sustainability tracking
- **Products**: Agricultural product catalog
- **Subsidies**: Government scheme information

---


## 📚 Learning Resources

### Knowledge Base Files
- `docs/diseases.txt` - Disease management guide
- `docs/biomass_conversion.txt` - Technology & economics
- `docs/sustainability_metrics.txt` - ESG framework
- `docs/yield_prediction.txt` - Ripeness & yield guide

### Documentation
- `README.md` - This file
- Code docstrings - Every module has detailed documentation



## 📄 License

This project is built on open-source components:
- Flask (BSD)
- PyTorch (BSD)
- LangChain (MIT)
- Chroma (Apache 2.0)
- HuggingFace Gradio (Apache 2.0)

