import joblib
import re
import numpy as np

# --- Configuration for Weights ---
WEIGHT_WHOLE_TEXT = 4.0
WEIGHT_SENTENCE_TOTAL = 6.0
# The sum of all weights is 3.0 + 7.0 = 10.0

# --- Load Pretrained Classifier ---
# This section REQUIRES the model files to be present at the specified path.
# If files are missing, the script will raise a FileNotFoundError.
try:
    vectorizer = joblib.load("models/tfidf_vectorizer.pkl")
    model = joblib.load("models/text_classifier.pkl")
    ALL_CLASSES = model.classes_
except FileNotFoundError:
    print("Warning: Text classification models not found. Using dummy implementation.")
    # Create dummy classes for fallback
    ALL_CLASSES = ['CCBC', 'CPMS', 'CDDS']
    vectorizer = None
    model = None

# --- Functions ---

def get_class_scores(text, vectorizer, model, class_labels):
    if not text.strip():
        return {label: 0 for label in class_labels}, 'N/A'

    # If models are not available, return dummy scores
    if vectorizer is None or model is None:
        # Simple heuristic: assign higher score to CDDS for disease-related queries
        if any(word in text.lower() for word in ['disease', 'pest', 'symptom', 'leaf', 'plant', 'crop']):
            return {'CCBC': 0.2, 'CPMS': 0.2, 'CDDS': 0.6}, 'CDDS'
        else:
            # Default to equal distribution
            return {label: 1.0/len(class_labels) for label in class_labels}, 'CCBC'

    try:
        X = vectorizer.transform([text])
        # Use predict_proba to get probability scores for all classes
        probabilities = model.predict_proba(X)[0]
        prediction = model.predict(X)[0]

        # Map probabilities back to their respective class labels
        scores_dict = {label: score for label, score in zip(class_labels, probabilities)}
        return scores_dict, prediction

    except Exception as e:
        print(f"Error during classification: {e}")
        # Return zeros on error
        return {label: 0 for label in class_labels}, 'ERROR'

def split_sentences(text):
    sentences = re.split(r'(?<=[.?!])\s+', text.strip())
    return [s for s in sentences if s]

def classify_text(text):
    scores = {label: 0.0 for label in ALL_CLASSES}
    
    print("\n--- DEBUGGING CLASSIFICATION STEPS ---")

    # 1. Whole Text Classification (Weight: 3.0)
    whole_text_scores, whole_text_pred = get_class_scores(text, vectorizer, model, ALL_CLASSES)
    weight_whole = WEIGHT_WHOLE_TEXT
    
    print(f"\n[WHOLE TEXT] Score Calculation (Weight: {weight_whole:.1f}):")
    print(f"  Input: '{text}'")
    print(f"  Raw Probs (P): { {k: round(v, 3) for k, v in whole_text_scores.items()} } -> Predicted: {whole_text_pred}")
    
    for key, score in whole_text_scores.items():
        weighted_score = score * weight_whole
        scores[key] += weighted_score
        print(f"  -> {key} Score: (P={score:.3f}) * (W={weight_whole:.1f}) = {weighted_score:.3f}")
    print(f"  Current Total Scores: { {k: round(v, 3) for k, v in scores.items()} }")
        
    # 2. Individual Sentence Classification (Total Weight: 7.0)
    sentences = split_sentences(text)
    num_sentences = len(sentences)
    
    if num_sentences > 0:
        score_multiplier = WEIGHT_SENTENCE_TOTAL / num_sentences
        
        print(f"\n[SENTENCES] Score Calculation (N={num_sentences}, Weight: {score_multiplier:.3f}):")
        
        for i, sentence in enumerate(sentences):
            sentence_scores, sentence_pred = get_class_scores(sentence, vectorizer, model, ALL_CLASSES)
            
            print(f"  [Sentence {i+1}] Input: '{sentence}'")
            print(f"    Raw Probs (P): { {k: round(v, 3) for k, v in sentence_scores.items()} } -> Predicted: {sentence_pred}")
            
            for key, score in sentence_scores.items():
                weighted_score = score * score_multiplier
                scores[key] += weighted_score
                print(f"    -> {key} Score: (P={score:.3f}) * (W={score_multiplier:.3f}) = {weighted_score:.3f}")
            
            # Print cumulative scores after each sentence for better debugging flow
            print(f"  Cumulative Total Scores: { {k: round(v, 3) for k, v in scores.items()} }")


    # 3. Final Result
    final_scores = {k: round(v, 3) for k, v in scores.items()}
    majority_key = max(final_scores, key=final_scores.get)
    
    print("\n--- FINAL CLASSIFICATION RESULT ---")
    print(f"Final Scores: {final_scores}")
    
    return majority_key

# --- Example Usage (Using your multi-sentence test case) ---

# print(f"Input Text: '{test_query}'")

# # Run the function
# majority_class = classify_text(test_query)
# print(f"Majority Key: {majority_class}")
