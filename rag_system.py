"""
RAG System with Hugging Face Gradio API
Uses zeus28/Agri-AI Gradio Space for LLM inference
Handles both Coconut and Oil Palm knowledge bases
"""

from gradio_client import Client, handle_file
from pymongo import MongoClient
import os
import glob
from pathlib import Path

try:
    from sentence_transformers import SentenceTransformer
    HAS_TRANSFORMERS = True
except:
    HAS_TRANSFORMERS = False

class HuggingFaceRAG:
    """
    RAG system using HuggingFace Gradio API (zeus28/Agri-AI)
    """
    
    def __init__(self, space_id="zeus28/Agri-AI", persist_dir="./agri_knowledge", crop_type="both"):
        """Initialize RAG system with HuggingFace Gradio API"""
        self.persist_dir = persist_dir
        self.crop_type = crop_type
        self.docs = []
        self.doc_embeddings = []
        self.space_id = space_id
        
        print(f"🚀 Connecting to HuggingFace Space: {space_id}")
        
        # Initialize Gradio client
        try:
            self.client = Client(space_id)
            print("✅ Connected to HuggingFace Gradio API")
        except Exception as e:
            print(f"⚠️  Error connecting to Gradio API: {e}")
            self.client = None
        
        # Initialize embeddings for document similarity
        if HAS_TRANSFORMERS:
            try:
                self.embeddings_model = SentenceTransformer("all-MiniLM-L6-v2")
                print("✅ Embeddings model loaded")
            except Exception as e:
                print(f"⚠️  Error loading embeddings: {e}")
                self.embeddings_model = None
        else:
            self.embeddings_model = None
        
        # MongoDB connection
        try:
            self.mongo_client = MongoClient("mongodb://localhost:27017/")
            self.db = self.mongo_client["cocosense"]
            print("✅ MongoDB connected")
        except Exception as e:
            print(f"⚠️  MongoDB error: {e}")
            self.mongo_client = None
            self.db = None
        
        os.makedirs(persist_dir, exist_ok=True)
        self._load_documents()
    
    def _load_documents(self):
        """Load documents from knowledge base"""
        self.docs = []
        
        # Load from docs
        docs_dir = "docs"
        if os.path.exists(docs_dir):
            for file in glob.glob(f"{docs_dir}/*.txt"):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if content.strip():
                            self.docs.append({
                                'text': content,
                                'source': Path(file).name,
                                'type': 'palm'
                            })
                except:
                    pass
        
        # Load from MongoDB if available
        if self.db is not None:
            try:
                for col_name in ['cocosense.categories', 'cocosense.products']:
                    col = self.db[col_name]
                    for doc in col.find().limit(100):
                        if 'description' in doc:
                            self.docs.append({
                                'text': str(doc.get('description', '')),
                                'source': col_name,
                                'type': 'coconut'
                            })
            except:
                pass
        
        print(f"📚 Loaded {len(self.docs)} documents for RAG")
        
        # Create embeddings if model available
        if self.embeddings_model and self.docs:
            texts = [d['text'][:500] for d in self.docs]
            try:
                self.doc_embeddings = self.embeddings_model.encode(texts)
            except:
                self.doc_embeddings = []
    
    def _find_similar_docs(self, query, top_k=3):
        """Find documents similar to query"""
        if not self.docs:
            return []
        
        if self.embeddings_model and len(self.doc_embeddings) > 0:
            try:
                query_embedding = self.embeddings_model.encode(query)
                
                # Simple cosine similarity
                import numpy as np
                similarities = []
                for i, doc_emb in enumerate(self.doc_embeddings):
                    sim = np.dot(query_embedding, doc_emb) / (
                        np.linalg.norm(query_embedding) * np.linalg.norm(doc_emb) + 1e-10
                    )
                    similarities.append((i, sim))
                
                similarities.sort(key=lambda x: x[1], reverse=True)
                return [self.docs[i]['text'] for i, _ in similarities[:top_k]]
            except:
                return [d['text'] for d in self.docs[:top_k]]
        else:
            return [d['text'] for d in self.docs[:top_k]]
    
    def query(self, text, crop_type=None):
        """Query using HuggingFace Gradio API with RAG"""
        if self.client is None:
            return "❌ HuggingFace Gradio API not connected. Check your internet connection."
        
        try:
            # Determine crop type
            crop = crop_type if crop_type in ['coconut', 'oil_palm'] else 'coconut'
            
            print(f"🔄 Calling HuggingFace Gradio API with message: {text[:50]}... crop: {crop}")
            
            # Use the /chat_fn API endpoint from zeus28/Agri-AI
            result = self.client.predict(
                message=text,
                history=[],
                crop=crop,
                api_name="/chat_fn"
            )
            
            print(f"✅ HuggingFace API raw result type: {type(result)}")
            print(f"✅ HuggingFace API raw result: {str(result)[:200]}")
            
            # The Gradio API returns a tuple: (chat_history, ...)
            # chat_history is a list like [['user_msg', 'ai_response'], ...]
            
            if isinstance(result, tuple):
                chat_history = result[0]
                print(f"📋 Extracted chat_history from tuple: {type(chat_history)}")
            else:
                chat_history = result
                print(f"📋 Result is not tuple, using directly: {type(chat_history)}")
            
            # If it's a list of messages, get the last one
            if isinstance(chat_history, list) and len(chat_history) > 0:
                last_exchange = chat_history[-1]
                print(f"📨 Last exchange: {type(last_exchange)} - {str(last_exchange)[:100]}")
                
                # last_exchange should be [user_message, ai_response]
                if isinstance(last_exchange, (list, tuple)) and len(last_exchange) >= 2:
                    ai_response = str(last_exchange[1]).strip()
                    print(f"📤 Extracted AI response (length: {len(ai_response)})")
                    return ai_response
            
            # Fallback: return as string
            result_str = str(chat_history).strip()
            print(f"📤 Returning fallback string (length: {len(result_str)})")
            return result_str
        
        except Exception as e:
            print(f"❌ HuggingFace API Error: {str(e)[:200]}")
            import traceback
            traceback.print_exc()
            return f"⚠️  Error generating response: {str(e)[:200]}\n\nMake sure the HuggingFace Space is accessible."


# Create singleton instance
rag_system = HuggingFaceRAG(space_id="zeus28/Agri-AI")
