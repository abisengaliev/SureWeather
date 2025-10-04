from typing import List, Dict, Any
from .models import ClothingRecommendation, OutfitRecommendation, ClothingItem

class ClothingRecommendationService:
    def __init__(self):
        self.clothing_icons = {
            ClothingItem.UMBRELLA: "☔",
            ClothingItem.SUNGLASSES: "🕶️",
            ClothingItem.JACKET: "🧥",
            ClothingItem.SUNSCREEN: "🧴",
            ClothingItem.BOOTS: "👢",
            ClothingItem.HAT: "👒",
            ClothingItem.GLOVES: "🧤",
            ClothingItem.SCARF: "🧣"
        }
    
    def get_recommendations(self, weather_data: Dict[str, Any], 
                          forecast_type: str, location: str) -> OutfitRecommendation:
        """Get clothing and gear recommendations based on weather data"""
        recommendations = []
        comfort_tips = []
        
        temp = weather_data.get("temperature", 20)
        humidity = weather_data.get("humidity", 50)
        wind_speed = weather_data.get("wind_speed", 10)
        precipitation = weather_data.get("precipitation", 0)
        condition = weather_data.get("condition", "sunny")
        uv_index = weather_data.get("uv_index", 5)
        
        # Temperature-based recommendations
        if temp < 0:
            recommendations.extend([
                ClothingRecommendation(
                    item=ClothingItem.JACKET,
                    priority=5,
                    reason="Very cold weather - heavy winter jacket essential",
                    icon=self.clothing_icons[ClothingItem.JACKET]
                ),
                ClothingRecommendation(
                    item=ClothingItem.GLOVES,
                    priority=5,
                    reason="Protect hands from freezing temperatures",
                    icon=self.clothing_icons[ClothingItem.GLOVES]
                ),
                ClothingRecommendation(
                    item=ClothingItem.SCARF,
                    priority=4,
                    reason="Protect neck and face from cold",
                    icon=self.clothing_icons[ClothingItem.SCARF]
                ),
                ClothingRecommendation(
                    item=ClothingItem.BOOTS,
                    priority=4,
                    reason="Warm, waterproof footwear essential",
                    icon=self.clothing_icons[ClothingItem.BOOTS]
                )
            ])
            comfort_tips.append("Layer up with thermal clothing")
            comfort_tips.append("Keep extremities warm to prevent frostbite")
            
        elif temp < 10:
            recommendations.extend([
                ClothingRecommendation(
                    item=ClothingItem.JACKET,
                    priority=4,
                    reason="Cold weather - warm jacket recommended",
                    icon=self.clothing_icons[ClothingItem.JACKET]
                ),
                ClothingRecommendation(
                    item=ClothingItem.GLOVES,
                    priority=3,
                    reason="Protect hands from cold",
                    icon=self.clothing_icons[ClothingItem.GLOVES]
                ),
                ClothingRecommendation(
                    item=ClothingItem.BOOTS,
                    priority=3,
                    reason="Warm, comfortable footwear",
                    icon=self.clothing_icons[ClothingItem.BOOTS]
                )
            ])
            comfort_tips.append("Wear layers for easy temperature adjustment")
            
        elif temp < 20:
            recommendations.extend([
                ClothingRecommendation(
                    item=ClothingItem.JACKET,
                    priority=2,
                    reason="Light jacket for cool weather",
                    icon=self.clothing_icons[ClothingItem.JACKET]
                )
            ])
            comfort_tips.append("Dress in layers for comfort")
            
        elif temp > 30:
            recommendations.extend([
                ClothingRecommendation(
                    item=ClothingItem.SUNGLASSES,
                    priority=4,
                    reason="Protect eyes from bright sun",
                    icon=self.clothing_icons[ClothingItem.SUNGLASSES]
                ),
                ClothingRecommendation(
                    item=ClothingItem.SUNSCREEN,
                    priority=5,
                    reason="Essential protection from UV rays",
                    icon=self.clothing_icons[ClothingItem.SUNSCREEN]
                ),
                ClothingRecommendation(
                    item=ClothingItem.HAT,
                    priority=4,
                    reason="Protect head from sun and heat",
                    icon=self.clothing_icons[ClothingItem.HAT]
                )
            ])
            comfort_tips.append("Wear light, breathable fabrics")
            comfort_tips.append("Stay hydrated and take breaks in shade")
            
        elif temp > 25:
            recommendations.extend([
                ClothingRecommendation(
                    item=ClothingItem.SUNGLASSES,
                    priority=3,
                    reason="Protect eyes from sun",
                    icon=self.clothing_icons[ClothingItem.SUNGLASSES]
                ),
                ClothingRecommendation(
                    item=ClothingItem.SUNSCREEN,
                    priority=4,
                    reason="Protect skin from UV rays",
                    icon=self.clothing_icons[ClothingItem.SUNSCREEN]
                )
            ])
            comfort_tips.append("Wear light, comfortable clothing")
        
        # Precipitation-based recommendations
        if precipitation > 5:
            recommendations.extend([
                ClothingRecommendation(
                    item=ClothingItem.UMBRELLA,
                    priority=5,
                    reason="Heavy rain expected - umbrella essential",
                    icon=self.clothing_icons[ClothingItem.UMBRELLA]
                ),
                ClothingRecommendation(
                    item=ClothingItem.BOOTS,
                    priority=4,
                    reason="Waterproof footwear for wet conditions",
                    icon=self.clothing_icons[ClothingItem.BOOTS]
                ),
                ClothingRecommendation(
                    item=ClothingItem.JACKET,
                    priority=4,
                    reason="Waterproof jacket recommended",
                    icon=self.clothing_icons[ClothingItem.JACKET]
                )
            ])
            comfort_tips.append("Avoid cotton clothing - it stays wet longer")
            comfort_tips.append("Consider waterproof bags for electronics")
            
        elif precipitation > 1:
            recommendations.extend([
                ClothingRecommendation(
                    item=ClothingItem.UMBRELLA,
                    priority=3,
                    reason="Light rain expected",
                    icon=self.clothing_icons[ClothingItem.UMBRELLA]
                ),
                ClothingRecommendation(
                    item=ClothingItem.JACKET,
                    priority=2,
                    reason="Light rain protection",
                    icon=self.clothing_icons[ClothingItem.JACKET]
                )
            ])
            comfort_tips.append("Quick-drying fabrics recommended")
        
        # Wind-based recommendations
        if wind_speed > 20:
            recommendations.extend([
                ClothingRecommendation(
                    item=ClothingItem.JACKET,
                    priority=3,
                    reason="Windy conditions - windproof jacket recommended",
                    icon=self.clothing_icons[ClothingItem.JACKET]
                ),
                ClothingRecommendation(
                    item=ClothingItem.HAT,
                    priority=3,
                    reason="Secure hat to protect from wind",
                    icon=self.clothing_icons[ClothingItem.HAT]
                )
            ])
            comfort_tips.append("Secure loose items and hair")
            comfort_tips.append("Consider windproof layers")
            
        elif wind_speed > 15:
            recommendations.extend([
                ClothingRecommendation(
                    item=ClothingItem.JACKET,
                    priority=2,
                    reason="Moderate wind - light windbreaker",
                    icon=self.clothing_icons[ClothingItem.JACKET]
                )
            ])
            comfort_tips.append("Dress in layers for wind protection")
        
        # UV Index recommendations
        if uv_index > 7:
            recommendations.extend([
                ClothingRecommendation(
                    item=ClothingItem.SUNSCREEN,
                    priority=5,
                    reason=f"Very high UV index ({uv_index}) - sunscreen essential",
                    icon=self.clothing_icons[ClothingItem.SUNSCREEN]
                ),
                ClothingRecommendation(
                    item=ClothingItem.SUNGLASSES,
                    priority=4,
                    reason="Protect eyes from intense UV",
                    icon=self.clothing_icons[ClothingItem.SUNGLASSES]
                ),
                ClothingRecommendation(
                    item=ClothingItem.HAT,
                    priority=4,
                    reason="Protect head from intense sun",
                    icon=self.clothing_icons[ClothingItem.HAT]
                )
            ])
            comfort_tips.append("Seek shade during peak sun hours (10 AM - 4 PM)")
            comfort_tips.append("Reapply sunscreen every 2 hours")
            
        elif uv_index > 5:
            recommendations.extend([
                ClothingRecommendation(
                    item=ClothingItem.SUNSCREEN,
                    priority=4,
                    reason=f"High UV index ({uv_index}) - sunscreen recommended",
                    icon=self.clothing_icons[ClothingItem.SUNSCREEN]
                ),
                ClothingRecommendation(
                    item=ClothingItem.SUNGLASSES,
                    priority=3,
                    reason="Protect eyes from UV",
                    icon=self.clothing_icons[ClothingItem.SUNGLASSES]
                )
            ])
            comfort_tips.append("Apply sunscreen before going outside")
        
        # Humidity-based tips
        if humidity > 80:
            comfort_tips.append("High humidity - wear breathable fabrics")
            comfort_tips.append("Stay hydrated and take frequent breaks")
        elif humidity < 30:
            comfort_tips.append("Low humidity - use moisturizer and stay hydrated")
        
        # General comfort tips based on forecast type
        if forecast_type == "long_term":
            comfort_tips.append("Plan ahead for seasonal weather changes")
            comfort_tips.append("Consider versatile clothing options")
        else:
            comfort_tips.append("Check weather updates throughout the day")
        
        # Sort recommendations by priority (highest first)
        recommendations.sort(key=lambda x: x.priority, reverse=True)
        
        return OutfitRecommendation(
            location=location,
            forecast_type=forecast_type,
            recommendations=recommendations,
            comfort_tips=comfort_tips
        )
