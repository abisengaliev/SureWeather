from typing import Dict, List, Any
from enum import Enum

class EventCategory(str, Enum):
    SUNNY_FRIENDLY = "sunny_friendly"
    RAIN_COMPATIBLE = "rain_compatible"
    WIND_BASED = "wind_based"
    COLD_WEATHER = "cold_weather"
    UNCOMFORTABLE = "uncomfortable"

class EventClassifier:
    """
    Classifies events based on weather suitability and characteristics
    """
    
    def __init__(self):
        self.event_categories = self._initialize_categories()
        self.weather_patterns = self._initialize_weather_patterns()
    
    def _initialize_categories(self) -> Dict[str, Dict[str, Any]]:
        """Initialize event categories with their characteristics"""
        return {
            EventCategory.SUNNY_FRIENDLY: {
                "name": "Sunny-Friendly Events",
                "description": "Events that thrive in clear, sunny weather",
                "icon": "☀️",
                "weather_preferences": {
                    "optimal_conditions": ["sunny", "partly_cloudy"],
                    "temperature_range": (15, 30),
                    "max_wind": 20,
                    "max_precipitation": 2,
                    "min_visibility": 8,
                    "uv_tolerance": "high"
                },
                "examples": [
                    "Outdoor concerts", "Festivals", "Hiking", "Beach activities",
                    "Sports events", "Picnics", "Garden tours", "Outdoor markets"
                ],
                "gear_recommendations": ["sunscreen", "sunglasses", "hat", "water"]
            },
            
            EventCategory.RAIN_COMPATIBLE: {
                "name": "Rain-Compatible Events",
                "description": "Events that work well in wet weather or are indoor",
                "icon": "🌧️",
                "weather_preferences": {
                    "optimal_conditions": ["rainy", "cloudy", "sunny"],
                    "temperature_range": (5, 35),
                    "max_wind": 30,
                    "max_precipitation": 50,
                    "min_visibility": 3,
                    "uv_tolerance": "low"
                },
                "examples": [
                    "Museum tours", "Indoor concerts", "Art galleries",
                    "Shopping centers", "Theater shows", "Indoor sports",
                    "Cooking classes", "Library events"
                ],
                "gear_recommendations": ["umbrella", "raincoat", "waterproof_bag"]
            },
            
            EventCategory.WIND_BASED: {
                "name": "Wind-Based Events",
                "description": "Events that require or benefit from wind",
                "icon": "🌬️",
                "weather_preferences": {
                    "optimal_conditions": ["windy", "partly_cloudy", "sunny"],
                    "temperature_range": (5, 30),
                    "min_wind": 10,
                    "max_wind": 25,
                    "max_precipitation": 5,
                    "min_visibility": 5,
                    "uv_tolerance": "medium"
                },
                "examples": [
                    "Kite festivals", "Sailing", "Paragliding", "Wind surfing",
                    "Hot air ballooning", "Wind energy tours", "Flag ceremonies"
                ],
                "gear_recommendations": ["windbreaker", "secure_hat", "goggles"]
            },
            
            EventCategory.COLD_WEATHER: {
                "name": "Cold-Weather Events",
                "description": "Events designed for cold or winter conditions",
                "icon": "❄️",
                "weather_preferences": {
                    "optimal_conditions": ["snowy", "cold", "clear"],
                    "temperature_range": (-20, 10),
                    "max_wind": 20,
                    "max_precipitation": 20,
                    "min_visibility": 5,
                    "uv_tolerance": "low"
                },
                "examples": [
                    "Skiing", "Ice skating", "Snowboarding", "Winter festivals",
                    "Hot spring visits", "Winter hiking", "Ice fishing",
                    "Christmas markets"
                ],
                "gear_recommendations": ["warm_jacket", "gloves", "boots", "thermal_clothing"]
            },
            
            EventCategory.UNCOMFORTABLE: {
                "name": "Weather-Sensitive Events",
                "description": "Events that may be uncomfortable in certain weather",
                "icon": "😓",
                "weather_preferences": {
                    "optimal_conditions": ["mild", "calm"],
                    "temperature_range": (10, 25),
                    "max_wind": 15,
                    "max_precipitation": 1,
                    "min_visibility": 10,
                    "uv_tolerance": "low"
                },
                "examples": [
                    "Outdoor dining", "Wedding ceremonies", "Outdoor photography",
                    "Children's outdoor activities", "Elderly group activities"
                ],
                "gear_recommendations": ["weather_protection", "comfort_items"]
            }
        }
    
    def _initialize_weather_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize weather patterns and their characteristics"""
        return {
            "sunny": {
                "cloud_cover": (0, 20),
                "precipitation": (0, 1),
                "visibility": (8, 15),
                "uv_index": (3, 11),
                "wind_speed": (0, 15)
            },
            "partly_cloudy": {
                "cloud_cover": (20, 60),
                "precipitation": (0, 2),
                "visibility": (6, 12),
                "uv_index": (2, 8),
                "wind_speed": (2, 20)
            },
            "cloudy": {
                "cloud_cover": (60, 90),
                "precipitation": (0, 5),
                "visibility": (4, 10),
                "uv_index": (1, 5),
                "wind_speed": (5, 25)
            },
            "rainy": {
                "cloud_cover": (80, 100),
                "precipitation": (2, 50),
                "visibility": (2, 8),
                "uv_index": (0, 3),
                "wind_speed": (5, 30)
            },
            "stormy": {
                "cloud_cover": (90, 100),
                "precipitation": (10, 100),
                "visibility": (1, 5),
                "uv_index": (0, 2),
                "wind_speed": (15, 50)
            },
            "snowy": {
                "cloud_cover": (70, 100),
                "precipitation": (5, 30),
                "visibility": (2, 10),
                "uv_index": (0, 4),
                "wind_speed": (5, 25),
                "temperature": (-20, 5)
            },
            "windy": {
                "cloud_cover": (30, 80),
                "precipitation": (0, 10),
                "visibility": (5, 15),
                "uv_index": (2, 8),
                "wind_speed": (15, 40)
            },
            "foggy": {
                "cloud_cover": (90, 100),
                "precipitation": (0, 5),
                "visibility": (0.1, 3),
                "uv_index": (0, 2),
                "wind_speed": (0, 10)
            }
        }
    
    def classify_event(self, event_name: str, event_description: str = "") -> EventCategory:
        """Classify an event into a weather category"""
        text = (event_name + " " + event_description).lower()
        
        # Keyword-based classification
        sunny_keywords = [
            "outdoor", "beach", "park", "garden", "festival", "concert",
            "sports", "hiking", "picnic", "market", "fair", "carnival"
        ]
        
        rain_keywords = [
            "museum", "gallery", "theater", "indoor", "shopping", "library",
            "cooking", "class", "workshop", "exhibition", "show"
        ]
        
        wind_keywords = [
            "kite", "sailing", "paragliding", "wind", "balloon", "surfing",
            "flying", "flag", "energy"
        ]
        
        cold_keywords = [
            "ski", "snow", "ice", "winter", "cold", "hot spring", "thermal",
            "christmas", "holiday"
        ]
        
        # Count keyword matches
        sunny_score = sum(1 for keyword in sunny_keywords if keyword in text)
        rain_score = sum(1 for keyword in rain_keywords if keyword in text)
        wind_score = sum(1 for keyword in wind_keywords if keyword in text)
        cold_score = sum(1 for keyword in cold_keywords if keyword in text)
        
        # Return category with highest score
        scores = {
            EventCategory.SUNNY_FRIENDLY: sunny_score,
            EventCategory.RAIN_COMPATIBLE: rain_score,
            EventCategory.WIND_BASED: wind_score,
            EventCategory.COLD_WEATHER: cold_score
        }
        
        if max(scores.values()) == 0:
            return EventCategory.UNCOMFORTABLE
        
        return max(scores, key=scores.get)
    
    def get_optimal_weather_conditions(self, category: EventCategory) -> Dict[str, Any]:
        """Get optimal weather conditions for an event category"""
        return self.event_categories[category]["weather_preferences"]
    
    def get_category_examples(self, category: EventCategory) -> List[str]:
        """Get example events for a category"""
        return self.event_categories[category]["examples"]
    
    def get_gear_recommendations(self, category: EventCategory) -> List[str]:
        """Get gear recommendations for a category"""
        return self.event_categories[category]["gear_recommendations"]
    
    def calculate_category_suitability(self, category: EventCategory, 
                                     weather_data: Dict[str, Any]) -> float:
        """Calculate how suitable weather is for a specific category"""
        preferences = self.get_optimal_weather_conditions(category)
        score = 100.0
        
        # Temperature scoring
        temp = weather_data.get("temperature", 20)
        if "temperature_range" in preferences:
            min_temp, max_temp = preferences["temperature_range"]
            if temp < min_temp:
                score -= (min_temp - temp) * 2
            elif temp > max_temp:
                score -= (temp - max_temp) * 1.5
        
        # Wind scoring
        wind = weather_data.get("wind_speed", 10)
        if "min_wind" in preferences and wind < preferences["min_wind"]:
            score -= (preferences["min_wind"] - wind) * 3
        if "max_wind" in preferences and wind > preferences["max_wind"]:
            score -= (wind - preferences["max_wind"]) * 2
        
        # Precipitation scoring
        precip = weather_data.get("precipitation", 0)
        if "max_precipitation" in preferences and precip > preferences["max_precipitation"]:
            score -= (precip - preferences["max_precipitation"]) * 4
        
        # Visibility scoring
        visibility = weather_data.get("visibility", 10)
        if "min_visibility" in preferences and visibility < preferences["min_visibility"]:
            score -= (preferences["min_visibility"] - visibility) * 2
        
        # UV scoring
        uv = weather_data.get("uv_index", 5)
        uv_tolerance = preferences.get("uv_tolerance", "medium")
        if uv_tolerance == "low" and uv > 6:
            score -= (uv - 6) * 3
        elif uv_tolerance == "high" and uv < 3:
            score -= (3 - uv) * 2
        
        return max(0, min(100, score))
    
    def get_all_categories(self) -> List[Dict[str, Any]]:
        """Get all event categories with their information"""
        return [
            {
                "category": category.value,
                "name": info["name"],
                "description": info["description"],
                "icon": info["icon"],
                "examples": info["examples"]
            }
            for category, info in self.event_categories.items()
        ]
