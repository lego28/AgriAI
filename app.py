from flask import Flask, request, jsonify, render_template
from imageclassification import predict_images  # Local PyTorch disease detection
from pymongo import MongoClient
import speech_recognition as sr
from search import searchuse
from rag_system import rag_system
from palmchat import ChatPalm
from palm_ripeness import ripeness_classifier, yield_predictor
from biomass_optimizer import biomass_optimizer
app = Flask(__name__, template_folder='.')
import random
from flask import Flask, request, jsonify
import os, base64
import json

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["cocosense"]

os.makedirs("static/sessionimg", exist_ok=True)

# Initialize PalmSense modules
chat_palm = ChatPalm()

@app.route('/')
def home():
    # Serve landing page
    return render_template('landing.html')

@app.route('/ai')
def chat_interface():
    # AI chat interface (renamed from /chat to avoid conflict)
    return render_template('ai_interface.html')

@app.route('/subsidies')
def subsidies_page():
    # Government subsidies information
    return render_template('subsidies.html')

@app.route('/products')
def products_page():
    # Product catalog
    return render_template('products.html')

@app.route('/esg')
def esg_dashboard():
    # ESG sustainability dashboard
    return render_template('esg.html')

@app.route('/detector')
def disease_detector_page():
    # Dedicated disease detection page
    return render_template('disease_detector.html') 

def speech_to_text(file_path):
    """Convert speech (any language) to text in English letters."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    text = recognizer.recognize_google(audio)  # replace with Gemini API if needed
    return text

@app.route('/generate_session', methods=['POST'])
def generate_session():
    while True:
        session_id = "{:04x}".format(random.randint(0, 0xFFFF))
        if db["sessions"].find_one({"session_id": session_id}) is None:
            return jsonify({"session_id": session_id})

@app.route("/chat", methods=["POST"])
def chatbot():
    data = request.json
    crop_type = data.get('crop_type', 'coconut')  # 'coconut' or 'palm'
    language = data.get('language', 'en')  # Get language preference
    
    query_texts = ""  
    
    # Handle text input
    if "text" in data and data["text"]:
        query_texts += data["text"]
    
    # Handle voice input
    if "voice" in data and data["voice"]:
        voice_text = speech_to_text(data["voice"])
        query_texts +=" " + voice_text
    
    # Handle image input
    if "image_urls" in data and data["image_urls"]:
        image_urls = data["image_urls"]
        
        # If it's base64 data, save it first
        if image_urls and isinstance(image_urls[0], str) and image_urls[0].startswith('data:image'):
            print("📸 Base64 image data received. Saving...")
            try:
                # Extract base64 and save
                img_data = image_urls[0].split(',')[1] if ',' in image_urls[0] else image_urls[0]
                img_bytes = base64.b64decode(img_data)
                session_id = data.get('session_id', 'temp')
                filename = f"{session_id}_chat_img.png"
                filepath = os.path.join('static/sessionimg', filename)
                with open(filepath, 'wb') as f:
                    f.write(img_bytes)
                image_urls = [f"/static/sessionimg/{filename}"]
                print(f"✅ Image saved: {filepath}")
            except Exception as e:
                print(f"⚠️  Error saving base64 image: {str(e)[:100]}")
                image_urls = []
        
        if image_urls:
            # Use LOCAL PyTorch Disease Detector
            try:
                print(f"🔬 Using local PyTorch disease detector for {crop_type}")
                
                # Special handling for palm ripeness if needed
                if crop_type == 'palm' and 'ripeness' in query_texts.lower():
                    try:
                        ripeness_result = ripeness_classifier.predict_ripeness(image_urls[0], return_probabilities=True)
                        if ripeness_result.get('ripeness_stage') is not None:
                            query_texts += f"\n\nRipeness Analysis: {json.dumps(ripeness_result)}"
                    except Exception as e:
                        print(f"⚠️  Palm ripeness error: {str(e)[:100]}")
                
                # Disease detection using local PyTorch model with crop-specific models
                disease_result = predict_images(image_urls, crop_type=crop_type)
                
                if disease_result and not disease_result.startswith("Image"):
                    disease_info = f"\n\nImage Analysis Result:\n- Disease Detected: {disease_result}"
                    query_texts += disease_info
                    print(f"✅ Disease detected: {disease_result}")
                else:
                    print(f"⚠️  Disease detection returned: {disease_result}")
                    query_texts += "\n\n[Image analysis: Processing completed]"
                    
            except Exception as e:
                print(f"⚠️  Image classification error: {str(e)[:100]}")
                query_texts += "\n\n[Image analysis unavailable]"

    oamsg = query_texts.strip()
    print(f"Session: {data['session_id']}, Crop: {crop_type}, Language: {language}")
    
    # Map language codes to names for instruction
    language_map = {
        'en': 'English',
        'hi': 'Hindi (हिंदी)',
        'ta': 'Tamil (தமிழ்)',
        'te': 'Telugu (తెలుగు)'
    }
    
    language_name = language_map.get(language, 'English')
    
    # Add language instruction to prompt if not English
    if language != 'en':
        enhanced_message = f"[Please respond in {language_name}] {oamsg}"
    else:
        enhanced_message = oamsg
    
    # Use RAG system with HuggingFace Agri-AI for ALL crops
    response = rag_system.query(enhanced_message, crop_type=crop_type)
    
    # Ensure response is a string, not a list
    if isinstance(response, list):
        print(f"⚠️  Response is a list, converting: {type(response)}")
        response = str(response)
    
    # Save chat message to MongoDB
    try:
        from datetime import datetime
        chat_message = {
            "session_id": data["session_id"],
            "timestamp": datetime.utcnow(),
            "user_message": oamsg,
            "ai_response": response,
            "crop_type": crop_type,
            "language": language
        }
        db["chat_history"].insert_one(chat_message)
        print(f"✅ Chat saved to history: {data['session_id']}")
    except Exception as e:
        print(f"⚠️  Failed to save chat history: {str(e)}")
    
    return jsonify({
        "response": response,
        "crop_type": crop_type,
        "language": language,
        "session_id": data["session_id"]
    })

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query', '')
    print("Received query:", query)

    search_results_array = searchuse(query) 
    response_data = {
        "data": search_results_array
    }

    return jsonify(response_data)

@app.route('/get_chat_sessions', methods=['GET'])
def get_chat_sessions():
    """Get list of all chat sessions for sidebar"""
    try:
        # Get unique sessions with their latest message
        pipeline = [
            {"$sort": {"timestamp": -1}},
            {"$group": {
                "_id": "$session_id",
                "last_message": {"$first": "$user_message"},
                "last_timestamp": {"$first": "$timestamp"},
                "message_count": {"$sum": 1}
            }},
            {"$sort": {"last_timestamp": -1}},
            {"$limit": 20}  # Show last 20 sessions
        ]
        
        sessions = list(db["chat_history"].aggregate(pipeline))
        
        # Format for frontend
        formatted_sessions = []
        for session in sessions:
            formatted_sessions.append({
                "session_id": session["_id"],
                "preview": session["last_message"][:50] + "..." if len(session["last_message"]) > 50 else session["last_message"],
                "timestamp": session["last_timestamp"].isoformat(),
                "message_count": session["message_count"]
            })
        
        return jsonify({"sessions": formatted_sessions})
    except Exception as e:
        print(f"⚠️  Error fetching chat sessions: {str(e)}")
        return jsonify({"sessions": []})

@app.route('/get_chat_history/<session_id>', methods=['GET'])
def get_chat_history(session_id):
    """Get full chat history for a specific session"""
    try:
        messages = list(db["chat_history"].find(
            {"session_id": session_id},
            {"_id": 0, "user_message": 1, "ai_response": 1, "timestamp": 1, "crop_type": 1}
        ).sort("timestamp", 1))
        
        return jsonify({"messages": messages})
    except Exception as e:
        print(f"⚠️  Error fetching chat history: {str(e)}")
        return jsonify({"messages": []})

@app.route('/delete_chat_session/<session_id>', methods=['DELETE'])
def delete_chat_session(session_id):
    """Delete a chat session"""
    try:
        result = db["chat_history"].delete_many({"session_id": session_id})
        return jsonify({"success": True, "deleted_count": result.deleted_count})
    except Exception as e:
        print(f"⚠️  Error deleting chat session: {str(e)}")
        return jsonify({"success": False, "error": str(e)})
@app.route('/upload_image', methods=['POST'])
def upload_image():
    data = request.get_json()
    session_id = data['session_id']
    img_id = data['img_id']
    image_data = data['image']

    img_bytes = base64.b64decode(image_data.split(',')[1])
    filename = f"{session_id}_{img_id}.png"
    filepath = os.path.join('static/sessionimg', filename)

    with open(filepath, 'wb') as f:
        f.write(img_bytes)

    return jsonify({'url': f"/static/sessionimg/{filename}"})

# ==================== PalmSense API Endpoints ====================

@app.route('/palm/ripeness', methods=['POST'])
def palm_ripeness_check():
    """Predict ripeness of oil palm bunch from image"""
    data = request.json
    image_path = data.get('image_path', '')
    
    if not image_path:
        return jsonify({'error': 'No image path provided'}), 400
    
    try:
        result = ripeness_classifier.predict_ripeness(image_path, return_probabilities=True)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/palm/batch_ripeness', methods=['POST'])
def palm_batch_ripeness():
    """Predict ripeness for multiple images (plantation monitoring)"""
    data = request.json
    image_paths = data.get('image_paths', [])
    plantation_hectares = data.get('plantation_hectares', 1)
    
    if not image_paths:
        return jsonify({'error': 'No image paths provided'}), 400
    
    try:
        batch_results = ripeness_classifier.predict_batch(image_paths)
        
        # Calculate yield prediction
        yield_prediction = yield_predictor.predict_yield_from_ripeness(
            batch_results['predictions'],
            plantation_hectares
        )
        
        batch_results['yield_prediction'] = yield_prediction
        return jsonify(batch_results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/palm/biomass_optimization', methods=['POST'])
def palm_biomass_calc():
    """Calculate biomass conversion and revenue potential"""
    data = request.json
    num_palms = data.get('num_palms', 1000)
    annual_cycles = data.get('annual_cycles', 2)
    location = data.get('location', 'tropics')
    
    try:
        optimizer = biomass_optimizer.__class__(num_palms, annual_cycles, location)
        report = optimizer.generate_optimization_report()
        return jsonify(report)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/palm/esg_score', methods=['POST'])
def palm_esg_score():
    """Generate ESG sustainability score for plantation"""
    data = request.json
    
    try:
        # Use biomass optimizer's ESG calculation
        esg_data = biomass_optimizer.calculate_esg_score()
        return jsonify(esg_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/palm/disease_info', methods=['GET'])
def palm_disease_info():
    """Get oil palm disease knowledge base"""
    disease_name = request.args.get('disease', '')
    
    try:
        if disease_name in chat_palm.PALM_DISEASES:
            disease_info = chat_palm.PALM_DISEASES[disease_name]
            return jsonify({
                'disease': disease_name,
                'information': disease_info
            })
        else:
            return jsonify({'error': f'Disease {disease_name} not found in knowledge base'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/rag/query', methods=['POST'])
def rag_query():
    """Query RAG system for dual-crop knowledge (coconut + palm)"""
    data = request.json
    question = data.get('question', '')
    crop_type = data.get('crop_type', 'both')  # 'coconut', 'palm', or 'both'
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        response = rag_system.query(question, crop_type)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e), 'suggestion': 'Make sure HuggingFace Space (zeus28/Agri-AI) is accessible'}), 500

@app.route('/disease/detect', methods=['POST'])
def detect_disease():
    """
    Dedicated endpoint for disease detection using local PyTorch models
    Supports: Coconut, Coffee, Cotton, Oil Palm (multiple crop-specific models)
    """
    try:
        # Handle file upload
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
            
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Get crop type from form data (default: coconut)
        crop_type = request.form.get('crop_type', 'coconut').lower()
        
        # Validate crop type
        valid_crops = ['coconut', 'coffee', 'cotton', 'palm', 'oil_palm']
        if crop_type not in valid_crops:
            crop_type = 'coconut'
        
        # Save uploaded file
        filename = f"disease_detect_{os.urandom(8).hex()}.png"
        filepath = os.path.join('static/sessionimg', filename)
        file.save(filepath)
        
        print(f"🔬 Detecting {crop_type} diseases...")
        
        # Detect disease using local PyTorch model with crop-specific model
        result = predict_images([filepath], crop_type=crop_type)
        
        if result and not result.startswith("Image"):
            # Parse result format: "disease_name, Confidence: X%"
            parts = result.split(", Confidence: ")
            disease_name = parts[0] if len(parts) > 0 else "Unknown"
            confidence = parts[1].replace("%", "") if len(parts) > 1 else "0"
            
            return jsonify({
                'success': True,
                'disease': disease_name,
                'confidence': float(confidence),
                'crop_type': crop_type,
                'image_url': f"/static/sessionimg/{filename}"
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Unable to detect disease clearly'
            }), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/palm/model_info', methods=['GET'])
def palm_model_info():
    """Get information about PalmSense ML models"""
    try:
        info = {
            'ripeness_classifier': ripeness_classifier.get_model_info(),
            'biomass_optimizer': {
                'type': 'Economic model',
                'biomass_yields': biomass_optimizer.BIOMASS_YIELDS,
                'conversion_efficiencies': biomass_optimizer.CONVERSION_EFFICIENCY
            },
            'rag_system': {
                'type': 'Retrieval Augmented Generation',
                'llm': 'HuggingFace zeus28/Agri-AI (Gradio API)',
                'embeddings': 'HuggingFace all-MiniLM-L6-v2',
                'vector_store': 'Semantic search'
            }
        }
        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
