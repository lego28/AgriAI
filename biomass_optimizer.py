"""
PalmSense Biomass-to-Biofuel Optimizer
ESG Scoring + Economics + Sustainability
"""

import json
from datetime import datetime

class BiomassBiofuelOptimizer:
    """Calculate biomass conversion economics and ESG metrics"""
    
    # Biomass yields per palm per year (kg)
    BIOMASS_YIELDS = {
        'empty_fruit_bunches': 4500,      # EFB - main waste stream
        'palm_kernel_shells': 1200,       # PKS - excellent energy content
        'palm_fronds': 2000,              # Fronds - continuous throughout year
        'trunk': 200                      # End-of-life palm trunk
    }
    
    # Energy content (MJ/kg)
    ENERGY_CONTENT = {
        'efb': 18.5,
        'pks': 19.2,
        'fronds': 17.8,
        'bioethanol': 26.8,
        'biodiesel': 37.5,
        'biochar': 28.0
    }
    
    # Conversion efficiencies (realistic values)
    CONVERSION_EFFICIENCY = {
        'efb_to_bioethanol': 0.42,        # 42% ethanol yield
        'efb_to_biochar': 0.35,           # 35% charcoal yield
        'pks_direct_combustion': 0.88,    # 88% energy transfer
        'fronds_pellets': 0.91,           # 91% to pellets
        'combined_biogas': 0.65           # 65% biogas conversion
    }
    
    # Market prices (USD/kg or USD/MJ equivalent)
    MARKET_PRICES = {
        'bioethanol': 0.68,               # USD/liter (convert: 0.8kg/liter)
        'biodiesel': 1.25,                # USD/liter
        'biochar': 0.40,                  # USD/kg (premium product)
        'wood_pellets': 0.15,             # USD/kg
        'biogas': 0.018,                  # USD/m³
        'fertilizer_from_ash': 0.25       # USD/kg potash equivalent
    }
    
    # ESG Impact Factors
    ESG_FACTORS = {
        'carbon_offset': 3.67,            # kg CO2 offset per kg biomass used
        'soil_health': 0.45,              # score contribution
        'waste_reduction': 0.80,          # fraction of waste utilized
        'biodiversity': 0.35              # relative score for ecosystem
    }
    
    def __init__(self, num_palms=1000, annual_harvest_cycles=2, location="tropics"):
        """
        Initialize optimizer
        num_palms: Number of oil palms in plantation
        annual_harvest_cycles: Usually 1-2 for oil palm
        location: "tropics", "subtropics" (affects yields)
        """
        self.num_palms = num_palms
        self.annual_cycles = annual_harvest_cycles
        self.location = location
        
        # Location adjustments
        if location == "subtropics":
            for key in self.BIOMASS_YIELDS:
                self.BIOMASS_YIELDS[key] *= 0.85  # 15% reduction
    
    def calculate_total_biomass(self):
        """Calculate total annual biomass available"""
        total_kg = 0
        breakdown = {}
        
        for biomass_type, yield_per_palm_kg in self.BIOMASS_YIELDS.items():
            annual_yield = yield_per_palm_kg * self.num_palms * self.annual_cycles
            breakdown[biomass_type] = {
                'kg': annual_yield,
                'tons': annual_yield / 1000,
                'per_palm_kg': yield_per_palm_kg * self.annual_cycles
            }
            total_kg += annual_yield
        
        return {
            'total_biomass_kg': total_kg,
            'total_biomass_tons': total_kg / 1000,
            'breakdown': breakdown,
            'plantation_size': self.num_palms,
            'cycles_per_year': self.annual_cycles
        }
    
    def calculate_energy_potential(self):
        """Calculate energy generation potential"""
        biomass = self.calculate_total_biomass()
        energy_mj = 0
        energy_breakdown = {}
        
        for biomass_type, data in biomass['breakdown'].items():
            if biomass_type == 'empty_fruit_bunches':
                energy_type = 'efb'
            elif biomass_type == 'palm_kernel_shells':
                energy_type = 'pks'
            else:
                energy_type = 'fronds'
            
            mj_content = data['kg'] * self.ENERGY_CONTENT[energy_type]
            energy_breakdown[biomass_type] = {
                'mj': mj_content,
                'kwh': mj_content / 3.6,  # 1 kWh = 3.6 MJ
                'energy_content_per_kg_mj': self.ENERGY_CONTENT[energy_type]
            }
            energy_mj += mj_content
        
        return {
            'total_energy_mj': energy_mj,
            'total_energy_kwh': energy_mj / 3.6,
            'breakdown': energy_breakdown,
            'equivalent_households_per_year': (energy_mj / 3.6) / 3650  # avg 10kWh/day
        }
    
    def calculate_biofuel_production(self):
        """Calculate biofuel production scenarios"""
        biomass = self.calculate_total_biomass()
        
        # Scenario 1: Maximum Bioethanol from EFB
        efb_kg = biomass['breakdown']['empty_fruit_bunches']['kg']
        bioethanol_liters = (efb_kg * self.CONVERSION_EFFICIENCY['efb_to_bioethanol']) / 0.8  # 0.8kg/liter
        bioethanol_value = bioethanol_liters * self.MARKET_PRICES['bioethanol']
        
        # Scenario 2: Direct Energy from PKS (highest efficiency)
        pks_kg = biomass['breakdown']['palm_kernel_shells']['kg']
        pks_energy_kwh = (pks_kg * self.ENERGY_CONTENT['pks'] * self.CONVERSION_EFFICIENCY['pks_direct_combustion']) / 3.6
        
        # Scenario 3: Biochar Premium Product
        biochar_kg = efb_kg * self.CONVERSION_EFFICIENCY['efb_to_biochar']
        biochar_value = biochar_kg * self.MARKET_PRICES['biochar']
        
        return {
            'bioethanol': {
                'liters': bioethanol_liters,
                'usd_value': bioethanol_value,
                'efficiency': self.CONVERSION_EFFICIENCY['efb_to_bioethanol']
            },
            'direct_energy_from_pks': {
                'kwh': pks_energy_kwh,
                'potential_usd_value': pks_energy_kwh * 0.12,  # avg $0.12/kWh
                'efficiency': self.CONVERSION_EFFICIENCY['pks_direct_combustion']
            },
            'biochar_production': {
                'kg': biochar_kg,
                'usd_value': biochar_value,
                'premium_product': True
            }
        }
    
    def calculate_revenue_potential(self):
        """Calculate total revenue from biomass utilization"""
        biofuel = self.calculate_biofuel_production()
        biomass = self.calculate_total_biomass()
        
        revenue = {
            'bioethanol': biofuel['bioethanol']['usd_value'],
            'pks_energy': biofuel['direct_energy_from_pks']['potential_usd_value'],
            'biochar': biofuel['biochar_production']['usd_value']
        }
        
        # Additional revenue from byproducts
        fronds_kg = biomass['breakdown']['palm_fronds']['kg']
        pellets_kg = fronds_kg * self.CONVERSION_EFFICIENCY['fronds_pellets']
        revenue['wood_pellets'] = pellets_kg * self.MARKET_PRICES['wood_pellets']
        
        total_revenue = sum(revenue.values())
        revenue['total_annual_usd'] = total_revenue
        revenue['revenue_per_hectare'] = total_revenue / (self.num_palms / 120)  # ~120 palms/hectare
        
        return revenue
    
    def calculate_esg_score(self):
        """
        Calculate ESG (Environmental, Social, Governance) Score
        Range: 0-100 (higher is better)
        """
        biomass = self.calculate_total_biomass()
        total_biomass_kg = biomass['total_biomass_kg']
        
        # Environmental Score (40% weight)
        carbon_offset_kg = total_biomass_kg * self.ESG_FACTORS['carbon_offset']
        co2_credits = carbon_offset_kg / 1000  # metric tons
        env_score = min(40, (co2_credits / 50) * 40)  # 50 tons CO2 = full score
        
        # Waste Reduction Score (35% weight)
        waste_utilization = self.ESG_FACTORS['waste_reduction']
        waste_score = waste_utilization * 35
        
        # Social/Biodiversity Score (25% weight)
        soil_health = self.ESG_FACTORS['soil_health']
        biodiversity = self.ESG_FACTORS['biodiversity']
        social_score = (soil_health + biodiversity) / 2 * 25
        
        total_esg = env_score + waste_score + social_score
        
        return {
            'total_score': round(total_esg, 1),
            'environmental_score': round(env_score, 1),
            'waste_reduction_score': round(waste_score, 1),
            'social_biodiversity_score': round(social_score, 1),
            'carbon_offset_metric_tons': round(co2_credits, 2),
            'esg_rating': self._get_esg_rating(total_esg),
            'sustainability_level': 'Excellent' if total_esg >= 75 else 'Good' if total_esg >= 60 else 'Moderate'
        }
    
    def _get_esg_rating(self, score):
        """Convert ESG score to rating"""
        if score >= 85:
            return "AAA ⭐⭐⭐"
        elif score >= 75:
            return "AA ⭐⭐"
        elif score >= 60:
            return "A ⭐"
        else:
            return "B 📊"
    
    def generate_optimization_report(self):
        """Generate comprehensive optimization report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'plantation_details': {
                'num_palms': self.num_palms,
                'annual_cycles': self.annual_cycles,
                'location': self.location
            },
            'biomass_potential': self.calculate_total_biomass(),
            'energy_potential': self.calculate_energy_potential(),
            'biofuel_production': self.calculate_biofuel_production(),
            'revenue_potential': self.calculate_revenue_potential(),
            'esg_analysis': self.calculate_esg_score(),
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self):
        """Generate optimization recommendations"""
        revenue = self.calculate_revenue_potential()
        esg = self.calculate_esg_score()
        
        recommendations = []
        
        # Revenue recommendations
        if revenue['total_annual_usd'] < 10000:
            recommendations.append({
                'category': 'Revenue',
                'priority': 'HIGH',
                'suggestion': 'Expand biochar production - highest value product',
                'potential_increase': '35-45%'
            })
        
        # ESG recommendations
        if esg['total_score'] < 75:
            recommendations.append({
                'category': 'Sustainability',
                'priority': 'HIGH',
                'suggestion': 'Implement complete waste-to-energy system',
                'esg_improvement': '15-20 points'
            })
        
        recommendations.append({
            'category': 'Best Practice',
            'priority': 'MEDIUM',
            'suggestion': 'Document biomass tracking for ESG certification',
            'benefit': 'Access premium buyers, 5-10% price premium'
        })
        
        return recommendations
    
    def export_report(self, filename=None):
        """Export report as JSON"""
        report = self.generate_optimization_report()
        
        if filename is None:
            filename = f"palm_optimization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        return filename

# Initialize global instance
biomass_optimizer = BiomassBiofuelOptimizer(num_palms=1000, annual_harvest_cycles=2)
