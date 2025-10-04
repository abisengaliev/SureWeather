from typing import List, Dict, Any, Optional
from .models import EventSuitabilityScore, EventCategory
from .db import get_events

class EventScoringService:
    def __init__(self):
        self.events = get_events()
    
    def calculate_event_score(self, event_id: str, weather_data: Dict[str, Any]) -> EventSuitabilityScore:
        """Calculate suitability score for a specific event"""
        event = next((e for e in self.events if e["id"] == event_id), None)
        if not event:
            raise ValueError(f"Event {event_id} not found")
        
        score, reasons, recommendations = self._calculate_score(event, weather_data)
        
        return EventSuitabilityScore(
            event_id=event_id,
            event_name=event["name"],
            score=score,
            reasons=reasons,
            recommendations=recommendations
        )
    
    def get_event_recommendations(self, weather_data: Dict[str, Any], 
                                 forecast_type: str, 
                                 categories: Optional[List[str]] = None) -> List[EventSuitabilityScore]:
        """Get event recommendations based on weather conditions"""
        recommendations = []
        
        # Filter events by categories if specified
        filtered_events = self.events
        if categories:
            filtered_events = [e for e in self.events if e["category"] in categories]
        
        for event in filtered_events:
            try:
                score, reasons, recs = self._calculate_score(event, weather_data)
                if score >= event["min_comfort_score"]:  # Only include suitable events
                    recommendations.append(EventSuitabilityScore(
                        event_id=event["id"],
                        event_name=event["name"],
                        score=score,
                        reasons=reasons,
                        recommendations=recs
                    ))
            except Exception as e:
                print(f"Error calculating score for {event['id']}: {e}")
                continue
        
        # Sort by score (highest first)
        recommendations.sort(key=lambda x: x.score, reverse=True)
        return recommendations[:10]  # Return top 10
    
    def _calculate_score(self, event: Dict[str, Any], weather_data: Dict[str, Any]) -> tuple:
        """Calculate score, reasons, and recommendations for an event"""
        score = 100.0
        reasons = []
        recommendations = []
        
        requirements = event["weather_requirements"]
        temp = weather_data.get("temperature", 20)
        humidity = weather_data.get("humidity", 50)
        wind_speed = weather_data.get("wind_speed", 10)
        precipitation = weather_data.get("precipitation", 0)
        condition = weather_data.get("condition", "sunny")
        
        # Temperature scoring
        if "min_temp" in requirements:
            if temp < requirements["min_temp"]:
                penalty = (requirements["min_temp"] - temp) * 5
                score -= penalty
                reasons.append(f"Temperature too low ({temp}°C < {requirements['min_temp']}°C)")
                recommendations.append("Consider indoor alternatives or wait for warmer weather")
        
        if "max_temp" in requirements:
            if temp > requirements["max_temp"]:
                penalty = (temp - requirements["max_temp"]) * 3
                score -= penalty
                reasons.append(f"Temperature too high ({temp}°C > {requirements['max_temp']}°C)")
                recommendations.append("Consider early morning or evening timing")
        
        # Wind scoring
        if "min_wind" in requirements:
            if wind_speed < requirements["min_wind"]:
                penalty = (requirements["min_wind"] - wind_speed) * 2
                score -= penalty
                reasons.append(f"Wind too light ({wind_speed} km/h < {requirements['min_wind']} km/h)")
                recommendations.append("Wait for windier conditions or consider alternative activities")
        
        if "max_wind" in requirements:
            if wind_speed > requirements["max_wind"]:
                penalty = (wind_speed - requirements["max_wind"]) * 4
                score -= penalty
                reasons.append(f"Wind too strong ({wind_speed} km/h > {requirements['max_wind']} km/h)")
                recommendations.append("Consider indoor alternatives or wait for calmer conditions")
        
        # Precipitation scoring
        if "max_precipitation" in requirements:
            if precipitation > requirements["max_precipitation"]:
                penalty = (precipitation - requirements["max_precipitation"]) * 8
                score -= penalty
                reasons.append(f"Too much precipitation ({precipitation}mm > {requirements['max_precipitation']}mm)")
                recommendations.append("Consider indoor alternatives or wait for drier conditions")
        
        # Visibility scoring
        if "min_visibility" in requirements:
            visibility = weather_data.get("visibility", 10)
            if visibility < requirements["min_visibility"]:
                penalty = (requirements["min_visibility"] - visibility) * 3
                score -= penalty
                reasons.append(f"Poor visibility ({visibility}km < {requirements['min_visibility']}km)")
                recommendations.append("Wait for clearer conditions")
        
        # Category-based adjustments
        category = event["category"]
        if category == "sunny_friendly" and condition in ["rainy", "snowy", "stormy"]:
            score -= 30
            reasons.append("Weather not suitable for outdoor sunny activities")
            recommendations.append("Consider indoor alternatives or wait for better weather")
        
        elif category == "rain_compatible" and condition in ["sunny", "cloudy"]:
            score += 10  # Bonus for rain-compatible events in good weather
            reasons.append("Perfect weather for this indoor activity")
        
        elif category == "wind_based" and wind_speed < 5:
            score -= 20
            reasons.append("Insufficient wind for wind-based activities")
            recommendations.append("Wait for windier conditions")
        
        elif category == "cold_weather" and temp > 10:
            score -= 25
            reasons.append("Too warm for cold-weather activities")
            recommendations.append("Consider winter alternatives or wait for colder weather")
        
        # Comfort adjustments
        if humidity > 80:
            score -= 10
            reasons.append("High humidity may cause discomfort")
            recommendations.append("Stay hydrated and take breaks")
        
        if wind_speed > 20:
            score -= 15
            reasons.append("Strong winds may cause discomfort")
            recommendations.append("Dress appropriately and secure loose items")
        
        # Ensure score is within bounds
        score = max(0, min(100, score))
        
        # Add positive reasons if score is high
        if score >= 80:
            reasons.append("Excellent weather conditions for this event")
        elif score >= 60:
            reasons.append("Good weather conditions for this event")
        elif score >= 40:
            reasons.append("Moderate weather conditions - proceed with caution")
        else:
            reasons.append("Poor weather conditions for this event")
        
        return score, reasons, recommendations
