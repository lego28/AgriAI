from flask import Flask, request, jsonify
from pymongo import MongoClient
# Import the main handler and the new context helper
from session_manager import get_session_response, check_and_rewrite_for_classification
from classification import classify_text 
import expertsys 
import datetime
import os
import random
import string
import sys

sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)

# --- MongoDB Setup ---
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "cocosense"
KB_COLLECTION_NAME = "cpms"
CCBC_COLLECTION_NAME = "ccbc"
SESSION_COLLECTION_NAME = "sessions"

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client[DB_NAME]
    kb_collection = db[KB_COLLECTION_NAME]
    ccbc_collection = db[CCBC_COLLECTION_NAME]
    session_collection = db[SESSION_COLLECTION_NAME]
    client.admin.command('ping')
    print("🤖 MongoDB connection successful. Chatbot server is starting with Context-First Routing.")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    sys.exit(1)

# --- Utility Function ---
def create_session_id():
    return ''.join(random.choices(string.hexdigits.lower(), k=16))

# --- Chat Endpoint ---
@app.route('/chat', methods=['POST'])
def chat_endpoint():
    data = request.get_json()
    session_id = data.get('session_id')
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "Missing message"}), 400

    # 1. Session Retrieval
    session_doc = session_collection.find_one({"session_id": session_id})
    chat_history = session_doc.get("chat_json", []) if session_doc else []
    is_new_session = not session_doc

    if is_new_session and not session_id:
        session_id = create_session_id()
        print(f"--- New Session Created: {session_id} ---")

    # 2. Context Check and Query Rewriting for Classification
    query_for_classification, is_contextual, previous_system = check_and_rewrite_for_classification(user_message, chat_history)

    # 3. Classification and Routing Determination
    classification_route = 'CPMS' # Default fallback
    
    try:
        if is_contextual and previous_system and previous_system in ['CPMS', 'CCBC']:
            # Context-First: Use the previous system to maintain thread coherence
            initial_classification = previous_system
            print(f"[DEBUG-SERVER] Context detected. Forcing classification route to previous system: {initial_classification}")
        else:
            # Classify the potentially rewritten query
            initial_classification = classify_text(query_for_classification)
            print(f"[DEBUG-SERVER] Classified Rewritten Query as: {initial_classification}")
        
        classification_route = initial_classification
        
    except Exception as e:
        print(f"CRITICAL ERROR: Classification failed on '{query_for_classification}': {e}")
        classification_route = 'CPMS' # Use safe default on classifier failure

    # 4. Get Response using Fallback Logic (CCBC -> CPMS)
    response_text = ""
    matched_query = None
    system_used = None
    
    current_route = classification_route
    
    try:
        # Loop for potential fallback 
        while True:
            if current_route == 'EXPERT_SYS':
                # Expert System: Terminal (No Fallback)
                expert_input_json = {"disease_query": user_message}
                response_text = expertsys.run_expert_system(expert_input_json)
                matched_query = "Expert System Diagnosis"
                system_used = 'EXPERT_SYS'
                break
                
            elif current_route in ['CCBC', 'CPMS']:
                print(f"[DEBUG-SERVER] Attempting {current_route} match...")
                
                # The session manager handles its own Tier 1/Tier 2 rewrite logic internally
                response_text, matched_query, system_used = get_session_response(
                    user_message, chat_history, kb_collection, ccbc_collection, current_route
                )
                
                if matched_query is not None or current_route == 'CPMS':
                    # Success OR we've already tried CPMS (the final fallback)
                    if matched_query is None and current_route == 'CPMS':
                        response_text = "I couldn't find a relevant answer in any knowledge base. Can you rephrase?"
                        system_used = 'NOT_FOUND'
                    break
                else:
                    # CCBC failed, FALLBACK to CPMS
                    print(f"[DEBUG-SERVER] {current_route} failed. Falling back to CPMS.")
                    current_route = 'CPMS'
            
            else:
                response_text = "Classification failed and the system is offline."
                system_used = 'UNKNOWN'
                break

    except Exception as e:
        print(f"CRITICAL ERROR during response generation/fallback: {e}")
        response_text = "Sorry, a critical server error occurred."
        system_used = 'FATAL_ERROR'


    # 5. Log and Update Session 
    
    chat_history.append({
        "role": "sent",
        "message": user_message,
        "timestamp": datetime.datetime.now().isoformat()
    })

    chat_history.append({
        "role": "received",
        "message": response_text,
        "matched_query": matched_query, 
        "system_used": system_used,
        "timestamp": datetime.datetime.now().isoformat()
    })
    
    session_collection.update_one(
        {"session_id": session_id},
        {"$set": {"chat_json": chat_history, "last_updated": datetime.datetime.now().isoformat()}},
        upsert=True
    )
    print(f"--- Session {session_id} updated. System Used: {system_used} ---\n")

    return jsonify({
        "session_id": session_id,
        "response": response_text,
        "is_new_session": is_new_session
    })

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)