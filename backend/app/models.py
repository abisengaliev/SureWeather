from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class WeatherCondition(str, Enum):
    SUNNY = "sunny"
    CLOUDY = "cloudy"
    RAINY = "rainy"
    SNOWY = "snowy"
    WINDY = "windy"
    FOGGY = "foggy"
    STORMY = "stormy"

class EventCategory(str, Enum):
    SUNNY_FRIENDLY = "sunny_friendly"
    RAIN_COMPATIBLE = "rain_compatible"
    WIND_BASED = "wind_based"
    COLD_WEATHER = "cold_weather"
    UNCOMFORTABLE = "uncomfortable"

class ClothingItem(str, Enum):
    UMBRELLA = "umbrella"
    SUNGLASSES = "sunglasses"
    JACKET = "jacket"
    SUNSCREEN = "sunscreen"
    BOOTS = "boots"
    HAT = "hat"
    GLOVES = "gloves"
    SCARF = "scarf"

# Weather Data Models
class WeatherData(BaseModel):
    temperature: float
    humidity: int
    wind_speed: float
    wind_direction: int
    precipitation: float
    cloud_cover: int
    visibility: float
    uv_index: float
    condition: WeatherCondition
    timestamp: datetime

class HourlyForecast(BaseModel):
    time: datetime
    weather: WeatherData
    comfort_index: float  # 0-100 scale

class DailyForecast(BaseModel):
    date: datetime
    high_temp: float
    low_temp: float
    avg_humidity: int
    avg_wind_speed: float
    total_precipitation: float
    condition: WeatherCondition
    hourly_forecasts: List[HourlyForecast]
    comfort_index: float

class ShortTermForecast(BaseModel):
    location: str
    latitude: float
    longitude: float
    current: WeatherData
    daily_forecasts: List[DailyForecast]
    generated_at: datetime

# Long-term Climate Models
class ClimateProbability(BaseModel):
    very_hot: float  # >35°C
    very_cold: float  # <0°C
    very_wet: float  # >10mm precipitation
    very_windy: float  # >20 km/h
    uncomfortable: float  # combined index

class MonthlyOutlook(BaseModel):
    month: int
    month_name: str
    probabilities: ClimateProbability
    avg_temperature: float
    avg_precipitation: float

class LongTermForecast(BaseModel):
    location: str
    latitude: float
    longitude: float
    monthly_outlooks: List[MonthlyOutlook]
    generated_at: datetime

# Event Models
class Event(BaseModel):
    id: str
    name: str
    category: EventCategory
    description: str
    weather_requirements: Dict[str, Any]
    min_comfort_score: float

class EventSuitabilityScore(BaseModel):
    event_id: str
    event_name: str
    score: float  # 0-100
    reasons: List[str]
    recommendations: List[str]

# Clothing Recommendation Models
class ClothingRecommendation(BaseModel):
    item: ClothingItem
    priority: int  # 1-5, 5 being most important
    reason: str
    icon: str

class OutfitRecommendation(BaseModel):
    location: str
    forecast_type: str  # "short_term" or "long_term"
    recommendations: List[ClothingRecommendation]
    comfort_tips: List[str]

# Request/Response Models
class LocationRequest(BaseModel):
    latitude: float
    longitude: float
    city_name: Optional[str] = None

class ForecastRequest(BaseModel):
    location: LocationRequest
    days: int = 16

class EventRecommendationRequest(BaseModel):
    location: LocationRequest
    forecast_type: str = "short_term"
    event_categories: Optional[List[EventCategory]] = None

class ClothingRequest(BaseModel):
    location: LocationRequest
    forecast_type: str = "short_term"

# Database Models
class QueryHistory(BaseModel):
    id: int
    location: str
    latitude: float
    longitude: float
    query_type: str
    timestamp: datetime
    response_data: Dict[str, Any]
