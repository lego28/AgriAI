import torch
import torch.nn.functional as F
from torchvision import models, transforms, datasets
from PIL import Image
import json
import os

# Multi-crop disease detection models
CROP_MODELS = {
    'coconut': 'models/coconut_best.pth',
    'coffee': 'models/coffee_best.pth',
    'cotton': 'models/cotton_best.pth',
    'palm': 'models/palm_best.pth',
    'oil_palm': 'models/palm_best.pth'  # Alias for palm
}

# Legacy model path (fallback)
MODEL_PATH = "models/alexnet_coconut.pth"       
DATA_DIR = "models/coconut_diseases"             
IMAGE_PATH = ["static/sessionimg/2123_2123_1.png"]
TOP_K = 4                                 

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# ===============================
# 3. Load Model & Classes (Lazy Loading)
# ===============================
# Cache models per crop type
loaded_models = {}

def _load_model(crop_type='coconut'):
    """Lazy load the model for specific crop type"""
    global loaded_models
    
    # Normalize crop type
    crop_type = crop_type.lower().strip()
    
    # Return cached model if already loaded
    if crop_type in loaded_models:
        return loaded_models[crop_type]
    
    print(f"🔄 Loading {crop_type} disease detection model...")
    
    # Determine model path
    model_path = CROP_MODELS.get(crop_type, MODEL_PATH)
    
    if not os.path.exists(model_path):
        print(f"⚠️  Model file '{model_path}' not found for crop: {crop_type}")
        # Try fallback to coconut model
        if crop_type != 'coconut' and os.path.exists(CROP_MODELS['coconut']):
            print(f"   Falling back to coconut model...")
            model_path = CROP_MODELS['coconut']
        else:
            loaded_models[crop_type] = {'model': None, 'class_names': [f"{crop_type.title()} Disease"], 'num_classes': 1}
            return loaded_models[crop_type]
    
    # Load class names from checkpoint metadata
    try:
        checkpoint = torch.load(model_path, map_location=device, weights_only=False)
        
        # Extract model state and metadata
        if isinstance(checkpoint, dict):
            if 'class_names' in checkpoint:
                class_names = checkpoint['class_names']
            elif 'classes' in checkpoint:
                class_names = checkpoint['classes']
            else:
                # Try to infer from model structure
                class_names = [f"{crop_type.title()} Disease Class {i}" for i in range(37)]  # Default 37 classes
            
            model_state = checkpoint.get('model_state_dict', checkpoint.get('state_dict', checkpoint))
        else:
            model_state = checkpoint
            class_names = [f"{crop_type.title()} Disease Class {i}" for i in range(37)]
        
        num_classes = len(class_names)
        print(f"✅ Found {num_classes} disease classes for {crop_type}")
        
        # Load pretrained AlexNet and modify classifier
        model = models.alexnet(weights=models.AlexNet_Weights.IMAGENET1K_V1)
        model.classifier[6] = torch.nn.Linear(4096, num_classes)
        
        # Load trained weights
        model.load_state_dict(model_state)
        model = model.to(device)
        model.eval()
        
        print(f"✅ {crop_type.title()} model loaded successfully!")
        
        loaded_models[crop_type] = {
            'model': model,
            'class_names': class_names,
            'num_classes': num_classes
        }
        
    except Exception as e:
        print(f"❌ Error loading {crop_type} model: {str(e)[:150]}")
        loaded_models[crop_type] = {'model': None, 'class_names': [f"{crop_type.title()} Disease"], 'num_classes': 1}
    
    return loaded_models[crop_type]

results = []
def predict_images(imgs, crop_type='coconut'):
    """Predict disease for images using AlexNet - supports multiple crop types"""
    global results
    model_data = _load_model(crop_type)  # Load model for specific crop
    results[:] = []
    
    for i in imgs:
        print(f"Processing image: {i} (crop: {crop_type})")
        try:
            predict_image(i, crop_type=crop_type, top_k=10)
        except Exception as e:
            print(f"Error processing image {i}: {str(e)[:100]}")
            results.append({
                "class_name": "Image analysis skipped",
                "confidence": 0
            })
    
    if not results:
        return "Image processing unavailable"
    
    result = sorted(results, key=lambda x: x["confidence"], reverse=True)
    
    # Format output
    output = result[0]["class_name"]
    if result[0]["confidence"] > 0:
        output += f", Confidence: {result[0]['confidence']}%"
    
    if len(result) > 1 and result[1]["confidence"] > 0:
        output += f" | Also detected: {result[1]['class_name']}"
    
    return output

def predict_image(image_path, crop_type='coconut', top_k=10):
    """Predict the top-k class labels and confidences for an input image."""
    model_data = _load_model(crop_type)  # Ensure model is loaded for this crop
    model = model_data['model']
    class_names = model_data['class_names']
    
    # Skip base64 encoded data
    if image_path.startswith('data:image'):
        print(f"⚠️  Base64 image data received. Skipping image classification.")
        results.append({
            "class_name": "Base64 data",
            "confidence": 0
        })
        return
    
    # Clean path
    if image_path.startswith('/static/'):
        image_path = image_path.lstrip('/')
    elif not image_path.startswith('static/'):
        image_path = os.path.join('static', image_path)

    full_path = os.path.join(os.getcwd(), image_path)

    if not os.path.exists(full_path):
        print(f"❌ Image file not found: {full_path}")
        print(f"   Received path: {image_path}")
        results.append({
            "class_name": "Image not found",
            "confidence": 0
        })
        return

    # If model is not available, return placeholder
    if model is None:
        print("⚠️  Model not available. Using placeholder prediction.")
        results.append({
            "class_name": "Model unavailable",
            "confidence": 0
        })
        return

    try:
        image = Image.open(full_path).convert("RGB")
        img_tensor = transform(image).unsqueeze(0).to(device)

        with torch.no_grad():
            outputs = model(img_tensor)
            probs = F.softmax(outputs, dim=1)

        # Top-k predictions
        top_probs, top_indices = torch.topk(probs, min(top_k, len(class_names)))

        for i in range(min(top_k, len(class_names))):
            class_name = class_names[top_indices[0][i].item()]
            confidence = top_probs[0][i].item() * 100
            
            # Check if already in results
            found = False
            for p in results:
                if p["class_name"] == class_name:
                    p["confidence"] = max(p["confidence"], round(confidence, 2))
                    found = True
                    break
            if not found:
                results.append({
                    "class_name": class_name,
                    "confidence": round(confidence, 2)
                })
    except Exception as e:
        print(f"❌ Error during prediction: {str(e)[:100]}")
        results.append({
            "class_name": "Prediction error",
            "confidence": 0
        })

if __name__ == "__main__":
    # Test with coconut model
    print("Testing coconut disease detection:")
    predictions = predict_images(IMAGE_PATH, crop_type='coconut')
    print(predictions)
    
    # Test other crops if images available
    # predictions = predict_images(IMAGE_PATH, crop_type='coffee')
    # predictions = predict_images(IMAGE_PATH, crop_type='palm')
