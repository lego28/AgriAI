"""
Palm Ripeness Classifier
Bunch maturity detection and yield readiness prediction
Uses pretrained ResNet50 for transfer learning
"""

import torch
import torch.nn as nn
from torchvision import models, transforms
import numpy as np
from PIL import Image
import json
from datetime import datetime, timedelta

class PalmRipenessClassifier:
    """
    Oil palm bunch ripeness classification
    States: GREEN, YELLOW, RED, DARK_RED, FALLEN
    """
    
    RIPENESS_STAGES = {
        0: {'name': 'GREEN', 'days_to_harvest': 30, 'yield_readiness': 0.0, 'color': '#00AA00'},
        1: {'name': 'YELLOW', 'days_to_harvest': 20, 'yield_readiness': 0.3, 'color': '#FFAA00'},
        2: {'name': 'RED', 'days_to_harvest': 10, 'yield_readiness': 0.7, 'color': '#FF3333'},
        3: {'name': 'DARK_RED', 'days_to_harvest': 0, 'yield_readiness': 1.0, 'color': '#990000'},
        4: {'name': 'FALLEN', 'days_to_harvest': -1, 'yield_readiness': 0.95, 'color': '#333333'}
    }
    
    # Ripeness to oil content mapping (%)
    OIL_CONTENT_BY_STAGE = {
        0: 8,    # GREEN - immature
        1: 20,   # YELLOW - developing
        2: 35,   # RED - mature
        3: 42,   # DARK_RED - peak ripeness
        4: 40    # FALLEN - slightly degraded
    }
    
    # Average fresh fruit bunch (FFB) weight by ripeness (kg)
    FFB_WEIGHT_BY_STAGE = {
        0: 5,
        1: 15,
        2: 22,
        3: 25,
        4: 24  # Slight loss due to ground time
    }
    
    def __init__(self, model_name='resnet50', pretrained=True, device='cpu'):
        """
        Initialize ripeness classifier
        model_name: 'resnet50', 'resnet101', 'efficientnet_b0'
        pretrained: Use ImageNet weights
        device: 'cpu' or 'cuda'
        """
        self.device = torch.device(device)
        self.model_name = model_name
        
        if model_name == 'resnet50':
            self.model = models.resnet50(pretrained=pretrained)
        elif model_name == 'resnet101':
            self.model = models.resnet101(pretrained=pretrained)
        else:
            self.model = models.resnet50(pretrained=pretrained)
        
        # Modify final layer for 5 ripeness classes
        num_features = self.model.fc.in_features
        self.model.fc = nn.Linear(num_features, 5)  # 5 ripeness stages
        self.model = self.model.to(self.device)
        self.model.eval()
        
        # Image preprocessing
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
    
    def predict_ripeness(self, image_path, return_probabilities=False):
        """
        Predict ripeness stage from image
        
        Args:
            image_path: Path to bunch image
            return_probabilities: Return confidence for each stage
        
        Returns:
            dict with ripeness stage, confidence, harvest timing, yield metrics
        """
        try:
            image = Image.open(image_path).convert('RGB')
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(image_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                predicted_class = torch.argmax(probabilities, dim=1).item()
                confidence = probabilities[0, predicted_class].item()
            
            stage_info = self.RIPENESS_STAGES[predicted_class]
            
            result = {
                'ripeness_stage': predicted_class,
                'stage_name': stage_info['name'],
                'confidence': round(confidence, 3),
                'days_to_optimal_harvest': stage_info['days_to_harvest'],
                'yield_readiness_percent': stage_info['yield_readiness'] * 100,
                'estimated_oil_content_percent': self.OIL_CONTENT_BY_STAGE[predicted_class],
                'estimated_ffb_weight_kg': self.FFB_WEIGHT_BY_STAGE[predicted_class],
                'harvest_recommendation': self._get_harvest_recommendation(predicted_class),
                'expected_yield_ml_oil': self._calculate_expected_oil(predicted_class)
            }
            
            if return_probabilities:
                result['stage_probabilities'] = {
                    self.RIPENESS_STAGES[i]['name']: round(probabilities[0, i].item(), 3)
                    for i in range(5)
                }
            
            return result
        
        except Exception as e:
            return {
                'error': str(e),
                'stage_name': 'UNKNOWN',
                'confidence': 0.0
            }
    
    def _get_harvest_recommendation(self, ripeness_stage):
        """Get harvest recommendation based on stage"""
        recommendations = {
            0: '❌ NOT READY - Too green. Wait 25-30 days',
            1: '⚠️  EARLY - Can harvest in 2-3 weeks for premium quality',
            2: '✅ GOOD - Ready for harvest. Optimal in 10 days',
            3: '✅✅ OPTIMAL - Perfect ripeness. Harvest NOW for maximum yield',
            4: '⚠️  OVERRIPE - Already fallen. Collect immediately to prevent decay'
        }
        return recommendations.get(ripeness_stage, 'Unknown')
    
    def _calculate_expected_oil(self, ripeness_stage):
        """Calculate expected oil yield in ml"""
        ffb_weight = self.FFB_WEIGHT_BY_STAGE[ripeness_stage]
        oil_percent = self.OIL_CONTENT_BY_STAGE[ripeness_stage]
        
        # Average oil density ~0.92 g/ml
        oil_kg = (ffb_weight * oil_percent) / 100
        oil_ml = (oil_kg * 1000) / 0.92
        
        return round(oil_ml)
    
    def predict_batch(self, image_paths, plot_uncertainty=False):
        """
        Predict ripeness for multiple images
        Useful for plantation-wide monitoring
        """
        predictions = []
        
        for image_path in image_paths:
            pred = self.predict_ripeness(image_path, return_probabilities=True)
            pred['image_path'] = image_path
            predictions.append(pred)
        
        # Calculate plantation statistics
        ready_count = sum(1 for p in predictions if p.get('ripeness_stage', -1) in [2, 3])
        total_oil_potential = sum(p.get('expected_yield_ml_oil', 0) for p in predictions)
        avg_confidence = np.mean([p['confidence'] for p in predictions])
        
        summary = {
            'total_bunches': len(predictions),
            'bunches_ready_to_harvest': ready_count,
            'harvest_readiness_percent': (ready_count / len(predictions) * 100) if predictions else 0,
            'total_oil_potential_liters': round(total_oil_potential / 1000, 2),
            'average_model_confidence': round(avg_confidence, 3),
            'predicted_harvest_date': self._predict_harvest_date(predictions),
            'stage_distribution': self._get_stage_distribution(predictions)
        }
        
        return {
            'predictions': predictions,
            'summary': summary
        }
    
    def _predict_harvest_date(self, predictions):
        """Predict optimal harvest date for plantation"""
        if not predictions:
            return None
        
        days_to_harvest = [
            self.RIPENESS_STAGES[p.get('ripeness_stage', 0)]['days_to_harvest']
            for p in predictions
        ]
        
        avg_days = np.mean([d for d in days_to_harvest if d >= 0]) if any(d >= 0 for d in days_to_harvest) else 15
        harvest_date = datetime.now() + timedelta(days=int(avg_days))
        
        return harvest_date.strftime('%Y-%m-%d')
    
    def _get_stage_distribution(self, predictions):
        """Get distribution of ripeness stages"""
        distribution = {stage: 0 for stage in self.RIPENESS_STAGES}
        
        for pred in predictions:
            stage = pred.get('ripeness_stage', 0)
            distribution[stage] += 1
        
        return {
            self.RIPENESS_STAGES[stage]['name']: count
            for stage, count in distribution.items()
        }
    
    def train_mode(self, training=True):
        """Switch model to train/eval mode"""
        if training:
            self.model.train()
        else:
            self.model.eval()
    
    def save_model(self, filepath='palm_ripeness_model.pth'):
        """Save model weights"""
        torch.save(self.model.state_dict(), filepath)
        return filepath
    
    def load_model(self, filepath='palm_ripeness_model.pth'):
        """Load model weights"""
        self.model.load_state_dict(torch.load(filepath, map_location=self.device))
        self.model.eval()
    
    def get_model_info(self):
        """Get model architecture info"""
        return {
            'model_type': self.model_name,
            'total_parameters': sum(p.numel() for p in self.model.parameters()),
            'trainable_parameters': sum(p.numel() for p in self.model.parameters() if p.requires_grad),
            'ripeness_classes': 5,
            'input_size': (224, 224),
            'device': str(self.device)
        }

class YieldPredictionModel:
    """
    Predict palm oil yield based on ripeness data
    Integrates ripeness classification with biomass calculations
    """
    
    def __init__(self, palms_per_hectare=120, harvest_cycles_per_year=2):
        self.palms_per_hectare = palms_per_hectare
        self.cycles_per_year = harvest_cycles_per_year
    
    def predict_yield_from_ripeness(self, ripeness_predictions, plantation_hectares=1):
        """
        Predict oil yield from batch ripeness predictions
        
        Args:
            ripeness_predictions: List of prediction dicts from predict_batch
            plantation_hectares: Size of plantation
        
        Returns:
            Yield prediction with confidence intervals
        """
        if not ripeness_predictions:
            return {'error': 'No predictions provided'}
        
        total_palms = len(ripeness_predictions)
        total_oil_ml = sum(p.get('expected_yield_ml_oil', 0) for p in ripeness_predictions)
        
        # Calculate per-palm average
        avg_oil_per_palm_ml = total_oil_ml / total_palms if total_palms > 0 else 0
        avg_oil_per_palm_liters = avg_oil_per_palm_ml / 1000
        
        # Extrapolate to hectare
        estimated_palms_per_hectare = self.palms_per_hectare
        yield_per_hectare_liters = avg_oil_per_palm_liters * estimated_palms_per_hectare
        
        # Yield categories (MT/hectare/year, 1 MT = 915 liters crude palm oil)
        yield_mt_per_hectare = yield_per_hectare_liters / 915
        
        # Annual projection
        annual_yield_per_hectare_mt = yield_mt_per_hectare * self.cycles_per_year
        annual_yield_total_mt = annual_yield_per_hectare_mt * plantation_hectares
        annual_yield_total_liters = annual_yield_total_mt * 915
        
        # Quality assessment
        quality_score = self._assess_quality(ripeness_predictions)
        
        return {
            'current_cycle_yield': {
                'per_palm_liters': round(avg_oil_per_palm_liters, 2),
                'per_hectare_liters': round(yield_per_hectare_liters, 2),
                'per_hectare_metric_tons': round(yield_mt_per_hectare, 2)
            },
            'annual_projection': {
                'per_hectare_metric_tons': round(annual_yield_per_hectare_mt, 2),
                'total_metric_tons': round(annual_yield_total_mt, 2),
                'total_liters': round(annual_yield_total_liters, 2),
                'plantation_size_hectares': plantation_hectares
            },
            'quality_metrics': {
                'quality_score': round(quality_score, 2),
                'average_ripeness_confidence': round(
                    np.mean([p.get('confidence', 0) for p in ripeness_predictions]), 3
                ),
                'optimal_bunches_percent': round(
                    sum(1 for p in ripeness_predictions if p.get('ripeness_stage') in [2, 3]) / len(ripeness_predictions) * 100
                    if ripeness_predictions else 0, 1
                )
            },
            'yield_category': self._categorize_yield(annual_yield_per_hectare_mt)
        }
    
    def _assess_quality(self, predictions):
        """Quality score 0-100 based on ripeness distribution"""
        if not predictions:
            return 0
        
        stages = [p.get('ripeness_stage', 0) for p in predictions]
        
        # Optimal ripeness is stage 2-3
        optimal_count = sum(1 for s in stages if s in [2, 3])
        optimal_percent = (optimal_count / len(stages)) * 100 if stages else 0
        
        # Overripe (stage 4) has penalty
        overripe_count = sum(1 for s in stages if s == 4)
        overripe_penalty = overripe_count * 2
        
        quality = min(100, optimal_percent - overripe_penalty)
        return quality
    
    def _categorize_yield(self, mt_per_hectare):
        """Categorize yield performance"""
        if mt_per_hectare >= 20:
            return 'EXCELLENT - Above 20 MT/ha/year'
        elif mt_per_hectare >= 15:
            return 'GOOD - 15-20 MT/ha/year'
        elif mt_per_hectare >= 10:
            return 'AVERAGE - 10-15 MT/ha/year'
        else:
            return 'LOW - Below 10 MT/ha/year'

# Initialize global instances
ripeness_classifier = PalmRipenessClassifier(device='cpu')
yield_predictor = YieldPredictionModel()
