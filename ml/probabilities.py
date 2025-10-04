import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import random

class SeasonalProbabilityModel:
    """
    Mock seasonal probability model for long-term climate forecasting.
    In a real implementation, this would use historical NASA POWER data
    or other climate datasets to calculate probabilities.
    """
    
    def __init__(self):
        self.climate_zones = self._initialize_climate_zones()
    
    def _initialize_climate_zones(self) -> Dict[str, Dict]:
        """Initialize climate zone characteristics"""
        return {
            "tropical": {
                "lat_range": (-23.5, 23.5),
                "temp_range": (20, 35),
                "precip_pattern": "high_variable",
                "seasonal_variation": "low"
            },
            "subtropical": {
                "lat_range": (23.5, 35),
                "temp_range": (10, 30),
                "precip_pattern": "moderate_seasonal",
                "seasonal_variation": "moderate"
            },
            "temperate": {
                "lat_range": (35, 50),
                "temp_range": (-5, 25),
                "precip_pattern": "moderate_uniform",
                "seasonal_variation": "high"
            },
            "continental": {
                "lat_range": (50, 70),
                "temp_range": (-20, 20),
                "precip_pattern": "low_summer",
                "seasonal_variation": "very_high"
            },
            "polar": {
                "lat_range": (70, 90),
                "temp_range": (-40, 5),
                "precip_pattern": "very_low",
                "seasonal_variation": "extreme"
            }
        }
    
    def get_climate_zone(self, latitude: float) -> str:
        """Determine climate zone based on latitude"""
        abs_lat = abs(latitude)
        
        for zone, characteristics in self.climate_zones.items():
            min_lat, max_lat = characteristics["lat_range"]
            if min_lat <= abs_lat <= max_lat:
                return zone
        
        return "temperate"  # Default fallback
    
    def calculate_monthly_probabilities(self, latitude: float, longitude: float, 
                                      months_ahead: int = 6) -> List[Dict]:
        """Calculate monthly climate probabilities for the next 6 months"""
        climate_zone = self.get_climate_zone(latitude)
        current_month = datetime.now().month
        
        probabilities = []
        
        for i in range(months_ahead):
            month = (current_month + i - 1) % 12 + 1
            month_prob = self._calculate_month_probabilities(
                month, climate_zone, latitude, longitude
            )
            probabilities.append(month_prob)
        
        return probabilities
    
    def _calculate_month_probabilities(self, month: int, climate_zone: str, 
                                     latitude: float, longitude: float) -> Dict:
        """Calculate probabilities for a specific month"""
        # Base probabilities by climate zone and month
        base_probs = self._get_base_probabilities(climate_zone, month)
        
        # Apply latitude adjustments
        lat_adjustments = self._get_latitude_adjustments(latitude, month)
        
        # Apply longitude adjustments (continental vs maritime)
        lon_adjustments = self._get_longitude_adjustments(longitude, latitude)
        
        # Combine adjustments
        final_probs = {}
        for key in base_probs:
            final_probs[key] = max(0, min(1, 
                base_probs[key] + lat_adjustments.get(key, 0) + lon_adjustments.get(key, 0)
            ))
        
        return {
            "month": month,
            "month_name": self._get_month_name(month),
            "probabilities": {
                "very_hot": round(final_probs["very_hot"], 2),
                "very_cold": round(final_probs["very_cold"], 2),
                "very_wet": round(final_probs["very_wet"], 2),
                "very_windy": round(final_probs["very_windy"], 2),
                "uncomfortable": round(final_probs["uncomfortable"], 2)
            },
            "avg_temperature": round(final_probs["avg_temp"], 1),
            "avg_precipitation": round(final_probs["avg_precip"], 1)
        }
    
    def _get_base_probabilities(self, climate_zone: str, month: int) -> Dict:
        """Get base probabilities for climate zone and month"""
        # Seasonal patterns
        is_winter = month in [12, 1, 2]
        is_spring = month in [3, 4, 5]
        is_summer = month in [6, 7, 8]
        is_fall = month in [9, 10, 11]
        
        # Adjust for southern hemisphere
        if climate_zone in ["tropical", "subtropical"]:
            # Less seasonal variation in tropical/subtropical
            if is_winter:
                return {
                    "very_hot": 0.1, "very_cold": 0.0, "very_wet": 0.3,
                    "very_windy": 0.2, "uncomfortable": 0.2,
                    "avg_temp": 25, "avg_precip": 60
                }
            elif is_summer:
                return {
                    "very_hot": 0.4, "very_cold": 0.0, "very_wet": 0.4,
                    "very_windy": 0.3, "uncomfortable": 0.3,
                    "avg_temp": 28, "avg_precip": 80
                }
            else:
                return {
                    "very_hot": 0.2, "very_cold": 0.0, "very_wet": 0.3,
                    "very_windy": 0.2, "uncomfortable": 0.2,
                    "avg_temp": 26, "avg_precip": 70
                }
        
        elif climate_zone == "temperate":
            if is_winter:
                return {
                    "very_hot": 0.0, "very_cold": 0.3, "very_wet": 0.4,
                    "very_windy": 0.4, "uncomfortable": 0.3,
                    "avg_temp": 5, "avg_precip": 80
                }
            elif is_summer:
                return {
                    "very_hot": 0.2, "very_cold": 0.0, "very_wet": 0.2,
                    "very_windy": 0.3, "uncomfortable": 0.2,
                    "avg_temp": 22, "avg_precip": 50
                }
            elif is_spring:
                return {
                    "very_hot": 0.1, "very_cold": 0.1, "very_wet": 0.3,
                    "very_windy": 0.4, "uncomfortable": 0.2,
                    "avg_temp": 15, "avg_precip": 70
                }
            else:  # fall
                return {
                    "very_hot": 0.1, "very_cold": 0.2, "very_wet": 0.3,
                    "very_windy": 0.3, "uncomfortable": 0.2,
                    "avg_temp": 12, "avg_precip": 60
                }
        
        elif climate_zone == "continental":
            if is_winter:
                return {
                    "very_hot": 0.0, "very_cold": 0.6, "very_wet": 0.2,
                    "very_windy": 0.5, "uncomfortable": 0.5,
                    "avg_temp": -10, "avg_precip": 30
                }
            elif is_summer:
                return {
                    "very_hot": 0.3, "very_cold": 0.0, "very_wet": 0.3,
                    "very_windy": 0.2, "uncomfortable": 0.2,
                    "avg_temp": 20, "avg_precip": 60
                }
            else:
                return {
                    "very_hot": 0.1, "very_cold": 0.3, "very_wet": 0.2,
                    "very_windy": 0.4, "uncomfortable": 0.3,
                    "avg_temp": 5, "avg_precip": 40
                }
        
        else:  # polar
            if is_winter:
                return {
                    "very_hot": 0.0, "very_cold": 0.8, "very_wet": 0.1,
                    "very_windy": 0.6, "uncomfortable": 0.7,
                    "avg_temp": -25, "avg_precip": 20
                }
            elif is_summer:
                return {
                    "very_hot": 0.0, "very_cold": 0.2, "very_wet": 0.2,
                    "very_windy": 0.4, "uncomfortable": 0.3,
                    "avg_temp": 5, "avg_precip": 40
                }
            else:
                return {
                    "very_hot": 0.0, "very_cold": 0.5, "very_wet": 0.1,
                    "very_windy": 0.5, "uncomfortable": 0.5,
                    "avg_temp": -10, "avg_precip": 25
                }
    
    def _get_latitude_adjustments(self, latitude: float, month: int) -> Dict:
        """Get latitude-based adjustments"""
        abs_lat = abs(latitude)
        adjustments = {}
        
        # Higher latitudes have more extreme seasonal variations
        if abs_lat > 60:
            adjustments["very_cold"] = 0.2 if month in [12, 1, 2] else -0.1
            adjustments["very_hot"] = 0.1 if month in [6, 7, 8] else -0.1
        elif abs_lat > 40:
            adjustments["very_cold"] = 0.1 if month in [12, 1, 2] else -0.05
            adjustments["very_hot"] = 0.1 if month in [6, 7, 8] else -0.05
        
        return adjustments
    
    def _get_longitude_adjustments(self, longitude: float, latitude: float) -> Dict:
        """Get longitude-based adjustments (continental vs maritime)"""
        adjustments = {}
        
        # Continental effect (more extreme temperatures)
        if -100 < longitude < 100:  # Roughly continental areas
            adjustments["very_hot"] = 0.1
            adjustments["very_cold"] = 0.1
            adjustments["very_windy"] = 0.1
        else:  # Maritime areas
            adjustments["very_hot"] = -0.1
            adjustments["very_cold"] = -0.1
            adjustments["very_wet"] = 0.1
        
        return adjustments
    
    def _get_month_name(self, month: int) -> str:
        """Get month name from number"""
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        return month_names[month - 1]
    
    def generate_historical_mock_data(self, latitude: float, longitude: float, 
                                    years: int = 5) -> pd.DataFrame:
        """Generate mock historical data for training/validation"""
        data = []
        current_date = datetime.now()
        
        for year in range(years):
            for month in range(1, 13):
                for day in range(1, 29):  # Simplified - 28 days per month
                    date = datetime(current_date.year - years + year, month, day)
                    
                    # Generate realistic weather data based on location and season
                    climate_zone = self.get_climate_zone(latitude)
                    base_probs = self._get_base_probabilities(climate_zone, month)
                    
                    # Add some randomness
                    temp = base_probs["avg_temp"] + random.uniform(-5, 5)
                    precip = max(0, base_probs["avg_precip"] + random.uniform(-20, 20))
                    wind = random.uniform(5, 25)
                    humidity = random.uniform(30, 90)
                    
                    data.append({
                        "date": date,
                        "temperature": round(temp, 1),
                        "precipitation": round(precip, 1),
                        "wind_speed": round(wind, 1),
                        "humidity": round(humidity, 0),
                        "latitude": latitude,
                        "longitude": longitude,
                        "climate_zone": climate_zone
                    })
        
        return pd.DataFrame(data)
