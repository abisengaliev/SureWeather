from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from .models import (
    LocationRequest, ForecastRequest, EventRecommendationRequest, ClothingRequest,
    ShortTermForecast, LongTermForecast, EventSuitabilityScore, OutfitRecommendation
)
from .services import WeatherService
from .scoring import EventScoringService
from .clothing import ClothingRecommendationService
from .db import save_query, get_query_history, get_events

router = APIRouter()
weather_service = WeatherService()
event_scoring = EventScoringService()
clothing_service = ClothingRecommendationService()

@router.get("/forecast/short-term")
async def get_short_term_forecast(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    city_name: Optional[str] = Query(None, description="City name")
) -> ShortTermForecast:
    """Get short-term weather forecast (up to 16 days)"""
    try:
        forecast = await weather_service.get_short_term_forecast(lat, lon, city_name)
        
        # Save query to history
        save_query(
            location=forecast.location,
            latitude=lat,
            longitude=lon,
            query_type="short_term_forecast",
            response_data=forecast.dict()
        )
        
        return forecast
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching forecast: {str(e)}")

@router.get("/forecast/long-term")
async def get_long_term_forecast(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    city_name: Optional[str] = Query(None, description="City name")
) -> LongTermForecast:
    """Get long-term seasonal outlook (5-6 months)"""
    try:
        forecast = weather_service.get_long_term_forecast(lat, lon, city_name)
        
        # Save query to history
        save_query(
            location=forecast.location,
            latitude=lat,
            longitude=lon,
            query_type="long_term_forecast",
            response_data=forecast.dict()
        )
        
        return forecast
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating long-term forecast: {str(e)}")

@router.get("/events")
async def get_events() -> List[dict]:
    """Get all available events"""
    return get_events()

@router.get("/events/recommendations")
async def get_event_recommendations(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    forecast_type: str = Query("short_term", description="Type of forecast: short_term or long_term"),
    event_categories: Optional[str] = Query(None, description="Comma-separated event categories")
) -> List[EventSuitabilityScore]:
    """Get event recommendations based on weather forecast"""
    try:
        # Parse event categories if provided
        categories = None
        if event_categories:
            categories = [cat.strip() for cat in event_categories.split(",")]
        
        # Get appropriate forecast
        if forecast_type == "short_term":
            forecast = await weather_service.get_short_term_forecast(lat, lon)
            weather_data = forecast.current
        else:
            forecast = weather_service.get_long_term_forecast(lat, lon)
            # Use first month's data for long-term
            weather_data = {
                "temperature": forecast.monthly_outlooks[0].avg_temperature,
                "humidity": 60,  # Default
                "wind_speed": 10,  # Default
                "precipitation": forecast.monthly_outlooks[0].avg_precipitation,
                "condition": "sunny"  # Default
            }
        
        # Get event recommendations
        recommendations = event_scoring.get_event_recommendations(
            weather_data, forecast_type, categories
        )
        
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting event recommendations: {str(e)}")

@router.get("/clothing/recommendations")
async def get_clothing_recommendations(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    forecast_type: str = Query("short_term", description="Type of forecast: short_term or long_term")
) -> OutfitRecommendation:
    """Get clothing and gear recommendations"""
    try:
        # Get appropriate forecast
        if forecast_type == "short_term":
            forecast = await weather_service.get_short_term_forecast(lat, lon)
            weather_data = forecast.current
        else:
            forecast = weather_service.get_long_term_forecast(lat, lon)
            # Use first month's data for long-term
            weather_data = {
                "temperature": forecast.monthly_outlooks[0].avg_temperature,
                "humidity": 60,
                "wind_speed": 10,
                "precipitation": forecast.monthly_outlooks[0].avg_precipitation,
                "condition": "sunny"
            }
        
        recommendations = clothing_service.get_recommendations(
            weather_data, forecast_type, forecast.location
        )
        
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting clothing recommendations: {str(e)}")

@router.get("/score/event")
async def calculate_event_score(
    event_id: str = Query(..., description="Event ID"),
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    forecast_type: str = Query("short_term", description="Type of forecast")
) -> EventSuitabilityScore:
    """Calculate suitability score for a specific event"""
    try:
        # Get appropriate forecast
        if forecast_type == "short_term":
            forecast = await weather_service.get_short_term_forecast(lat, lon)
            weather_data = forecast.current
        else:
            forecast = weather_service.get_long_term_forecast(lat, lon)
            weather_data = {
                "temperature": forecast.monthly_outlooks[0].avg_temperature,
                "humidity": 60,
                "wind_speed": 10,
                "precipitation": forecast.monthly_outlooks[0].avg_precipitation,
                "condition": "sunny"
            }
        
        score = event_scoring.calculate_event_score(event_id, weather_data)
        return score
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating event score: {str(e)}")

@router.get("/history")
async def get_history(limit: int = Query(50, description="Number of recent queries to return")) -> List[dict]:
    """Get query history"""
    return get_query_history(limit)

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "nasa-weather-api"}
