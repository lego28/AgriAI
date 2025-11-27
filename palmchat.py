"""
PalmChat - Oil Palm Disease Knowledge Retrieval
Mirrors chatcpms.py but for oil palm specific queries
"""

import numpy as np
import re
from rapidfuzz import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings

warnings.filterwarnings("ignore")

# Oil Palm Disease Knowledge Base
PALM_DISEASES = {
    'ganoderma_basal_stem_rot': {
        'symptoms': 'Rotting of base, yellowing fronds, reduced growth, tree death',
        'cause': 'Ganoderma fungus',
        'treatment': 'Remove affected trees, sanitize soil, improve drainage',
        'prevention': 'Avoid soil compaction, use resistant varieties'
    },
    'leaf_spot_disease': {
        'symptoms': 'Brown spots on leaves, premature leaf drop',
        'cause': 'Fungal infection',
        'treatment': 'Spray fungicides, remove infected fronds',
        'prevention': 'Maintain good spacing, reduce humidity'
    },
    'bunch_rot': {
        'symptoms': 'Blackening of fruit bunches, fungal growth',
        'cause': 'Phytophthora species',
        'treatment': 'Remove affected bunches, spray copper fungicide',
        'prevention': 'Improve air circulation, avoid waterlogging'
    },
    'pest_infestation': {
        'symptoms': 'Chewed fronds, holes in stems, visible insects',
        'cause': 'Rhinoceros beetle, leaf roller insects',
        'treatment': 'Manual removal, insecticide spray',
        'prevention': 'Pheromone traps, regular monitoring'
    }
}

INTENT_KEYWORDS = {
    "DIAGNOSIS": ["disease", "symptom", "problem", "what is wrong", "diagnose"],
    "TREATMENT": ["treat", "cure", "fix", "solution", "how to fix"],
    "PREVENTION": ["prevent", "avoid", "protect", "how to prevent"],
    "YIELD": ["yield", "production", "harvest", "bunch", "ripeness"],
    "BIOMASS": ["waste", "biomass", "fuel", "conversion", "bunches"],
    "GENERAL": ["tell me", "about", "info", "explain"]
}

class ChatPalm:
    """Oil Palm Disease Chat Module"""
    
    def __init__(self):
        self.diseases = PALM_DISEASES
        self._prepare_knowledge_base()
    
    def _prepare_knowledge_base(self):
        """Prepare TF-IDF vectors for disease matching"""
        disease_descriptions = []
        self.disease_names = []
        
        for disease_name, info in self.diseases.items():
            combined_text = f"{disease_name} {info['symptoms']} {info['cause']}"
            disease_descriptions.append(combined_text)
            self.disease_names.append(disease_name)
        
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.disease_matrix = self.vectorizer.fit_transform(disease_descriptions)
    
    def _extract_intent(self, query):
        """Determine user's intent"""
        best_intent = "GENERAL"
        max_score = 0
        
        for intent, keywords in INTENT_KEYWORDS.items():
            score = sum(query.lower().count(kw) for kw in keywords)
            if score > max_score:
                max_score = score
                best_intent = intent
        
        return best_intent
    
    def _find_disease(self, query):
        """Find most relevant disease from query"""
        try:
            query_vec = self.vectorizer.transform([query])
            scores = cosine_similarity(query_vec, self.disease_matrix)[0]
            best_idx = np.argmax(scores)
            confidence = scores[best_idx]
            
            if confidence > 0.2:
                return self.disease_names[best_idx], confidence
            return None, 0.0
        except:
            return None, 0.0
    
    def get_response(self, query):
        """Generate response for palm farming query"""
        intent = self._extract_intent(query)
        disease, confidence = self._find_disease(query)
        
        # If high confidence disease match
        if disease and confidence > 0.5:
            disease_info = self.diseases[disease]
            
            if intent == "DIAGNOSIS":
                response = f"""
**Oil Palm Disease: {disease.replace('_', ' ').title()}**

🔍 **Symptoms:** {disease_info['symptoms']}
🦠 **Cause:** {disease_info['cause']}
💊 **Treatment:** {disease_info['treatment']}
🛡️ **Prevention:** {disease_info['prevention']}
                """
            
            elif intent == "TREATMENT":
                response = f"""
**Treatment for {disease.replace('_', ' ').title()}:**

💊 {disease_info['treatment']}

Prevention Steps:
- {disease_info['prevention']}
- Monitor regularly for early detection
- Consult local agricultural officer
                """
            
            elif intent == "PREVENTION":
                response = f"""
**Prevention of {disease.replace('_', ' ').title()}:**

🛡️ {disease_info['prevention']}

Additional Measures:
- Maintain 8-9m spacing between palms
- Ensure proper drainage
- Remove diseased palms immediately
- Use certified healthy seedlings
                """
            
            else:
                response = f"""
**About {disease.replace('_', ' ').title()}:**

Symptoms: {disease_info['symptoms']}
Treatment: {disease_info['treatment']}
Prevention: {disease_info['prevention']}
                """
            
            return response, disease, confidence
        
        # Generic responses
        if intent == "YIELD":
            response = """
**Oil Palm Yield Information:**

Expected yield: 20-25 tons fresh fruit bunches per hectare per year
Optimal conditions:
- Temperature: 25-32°C
- Rainfall: 1500-2500mm annually
- Well-drained soil
- 8-9m spacing
- Proper fertilization schedule
            """
        
        elif intent == "BIOMASS":
            response = """
**Oil Palm Biomass Potential:**

Empty Fruit Bunches (EFB): 4.5 tons/palm/year
- Use: Biofuel, compost, animal bedding
Palm Kernel Shells: 1.2 tons/palm/year
- Use: Biochar, energy generation
Palm Fronds: 2 tons/palm/year
- Use: Mulch, livestock feed

Economics: Can generate 20-30% additional revenue!
            """
        
        else:
            response = """
**Oil Palm Farming Assistance:**

I can help with:
✓ Disease diagnosis and treatment
✓ Pest management
✓ Yield optimization
✓ Biomass utilization
✓ Sustainability practices

Describe your situation or ask a specific question!
            """
        
        return response, None, 0.0

# Initialize global instance
chat_palm = ChatPalm()
