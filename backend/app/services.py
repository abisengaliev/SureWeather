import httpx
import os
import random
import math
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from .models import (
    WeatherData, HourlyForecast, DailyForecast, ShortTermForecast,
    WeatherCondition, ClimateProbability, MonthlyOutlook, LongTermForecast
)

# OpenWeather API configuration
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "demo_key")
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/3.0/onecall"

class WeatherService:
    def __init__(self):
        self.api_key = OPENWEATHER_API_KEY
        self.base_url = OPENWEATHER_BASE_URL
    
    async def get_short_term_forecast(self, lat: float, lon: float, city_name: str = None) -> ShortTermForecast:
        """Get short-term forecast (up to 16 days) from OpenWeather API or fallback generator"""
        try:
            return await self._fetch_from_api(lat, lon, city_name)
        except Exception as e:
            print(f"API Error: {e}. Using fallback generator.")
            return self._generate_fallback_forecast(lat, lon, city_name)
    
    async def _fetch_from_api(self, lat: float, lon: float, city_name: str) -> ShortTermForecast:
        """Fetch forecast from OpenWeather One Call API 3.0"""
        async with httpx.AsyncClient() as client:
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric",
                "exclude": "minutely,alerts"
            }
            
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return self._parse_api_response(data, lat, lon, city_name)
    
    def _parse_api_response(self, data: Dict, lat: float, lon: float, city_name: str) -> ShortTermForecast:
        """Parse OpenWeather API response into our models"""
        current = self._parse_current_weather(data["current"])
        daily_forecasts = []
        
        for day_data in data["daily"][:16]:  # Limit to 16 days
            daily_forecast = self._parse_daily_weather(day_data)
            daily_forecasts.append(daily_forecast)
        
        return ShortTermForecast(
            location=city_name or f"{lat},{lon}",
            latitude=lat,
            longitude=lon,
            current=current,
            daily_forecasts=daily_forecasts,
            generated_at=datetime.now()
        )
    
    def _parse_current_weather(self, current_data: Dict) -> WeatherData:
        """Parse current weather from API response"""
        return WeatherData(
            temperature=current_data["temp"],
            humidity=current_data["humidity"],
            wind_speed=current_data["wind_speed"],
            wind_direction=current_data["wind_deg"],
            precipitation=current_data.get("rain", {}).get("1h", 0) + current_data.get("snow", {}).get("1h", 0),
            cloud_cover=current_data["clouds"],
            visibility=current_data["visibility"] / 1000,  # Convert to km
            uv_index=current_data["uvi"],
            condition=self._map_weather_condition(current_data["weather"][0]["main"]),
            timestamp=datetime.fromtimestamp(current_data["dt"])
        )
    
    def _parse_daily_weather(self, day_data: Dict) -> DailyForecast:
        """Parse daily weather from API response"""
        hourly_forecasts = []
        
        # Generate hourly forecasts for the day (simplified)
        for hour in range(0, 24, 3):  # Every 3 hours
            temp_variation = random.uniform(-2, 2)
            hourly_weather = WeatherData(
                temperature=day_data["temp"]["day"] + temp_variation,
                humidity=day_data["humidity"],
                wind_speed=day_data["wind_speed"],
                wind_direction=day_data["wind_deg"],
                precipitation=day_data.get("rain", 0),
                cloud_cover=day_data["clouds"],
                visibility=10,
                uv_index=day_data["uvi"],
                condition=self._map_weather_condition(day_data["weather"][0]["main"]),
                timestamp=datetime.fromtimestamp(day_data["dt"]) + timedelta(hours=hour)
            )
            
            comfort_index = self._calculate_comfort_index(hourly_weather)
            hourly_forecasts.append(HourlyForecast(
                time=hourly_weather.timestamp,
                weather=hourly_weather,
                comfort_index=comfort_index
            ))
        
        comfort_index = self._calculate_comfort_index(
            WeatherData(
                temperature=(day_data["temp"]["max"] + day_data["temp"]["min"]) / 2,
                humidity=day_data["humidity"],
                wind_speed=day_data["wind_speed"],
                wind_direction=day_data["wind_deg"],
                precipitation=day_data.get("rain", 0),
                cloud_cover=day_data["clouds"],
                visibility=10,
                uv_index=day_data["uvi"],
                condition=self._map_weather_condition(day_data["weather"][0]["main"]),
                timestamp=datetime.fromtimestamp(day_data["dt"])
            )
        )
        
        return DailyForecast(
            date=datetime.fromtimestamp(day_data["dt"]),
            high_temp=day_data["temp"]["max"],
            low_temp=day_data["temp"]["min"],
            avg_humidity=day_data["humidity"],
            avg_wind_speed=day_data["wind_speed"],
            total_precipitation=day_data.get("rain", 0),
            condition=self._map_weather_condition(day_data["weather"][0]["main"]),
            hourly_forecasts=hourly_forecasts,
            comfort_index=comfort_index
        )
    
    def _map_weather_condition(self, condition: str) -> WeatherCondition:
        """Map OpenWeather condition to our enum"""
        condition_map = {
            "Clear": WeatherCondition.SUNNY,
            "Clouds": WeatherCondition.CLOUDY,
            "Rain": WeatherCondition.RAINY,
            "Drizzle": WeatherCondition.RAINY,
            "Snow": WeatherCondition.SNOWY,
            "Thunderstorm": WeatherCondition.STORMY,
            "Mist": WeatherCondition.FOGGY,
            "Fog": WeatherCondition.FOGGY,
            "Haze": WeatherCondition.FOGGY
        }
        return condition_map.get(condition, WeatherCondition.CLOUDY)
    
    def _generate_fallback_forecast(self, lat: float, lon: float, city_name: str) -> ShortTermForecast:
        """Generate synthetic forecast when API is unavailable"""
        current = self._generate_synthetic_weather()
        daily_forecasts = []
        
        for day in range(16):
            daily_forecast = self._generate_synthetic_daily_forecast(day)
            daily_forecasts.append(daily_forecast)
        
        return ShortTermForecast(
            location=city_name or f"{lat},{lon}",
            latitude=lat,
            longitude=lon,
            current=current,
            daily_forecasts=daily_forecasts,
            generated_at=datetime.now()
        )
    
    def _generate_synthetic_weather(self) -> WeatherData:
        """Generate synthetic current weather data"""
        base_temp = random.uniform(15, 25)
        return WeatherData(
            temperature=base_temp,
            humidity=random.randint(30, 80),
            wind_speed=random.uniform(2, 15),
            wind_direction=random.randint(0, 360),
            precipitation=random.uniform(0, 5),
            cloud_cover=random.randint(10, 90),
            visibility=random.uniform(5, 15),
            uv_index=random.uniform(0, 10),
            condition=random.choice(list(WeatherCondition)),
            timestamp=datetime.now()
        )
    
    def _generate_synthetic_daily_forecast(self, day_offset: int) -> DailyForecast:
        """Generate synthetic daily forecast"""
        base_temp = random.uniform(10, 30)
        high_temp = base_temp + random.uniform(2, 8)
        low_temp = base_temp - random.uniform(2, 8)
        
        hourly_forecasts = []
        for hour in range(0, 24, 3):
            temp = low_temp + (high_temp - low_temp) * (hour / 24) + random.uniform(-2, 2)
            weather = WeatherData(
                temperature=temp,
                humidity=random.randint(40, 90),
                wind_speed=random.uniform(1, 20),
                wind_direction=random.randint(0, 360),
                precipitation=random.uniform(0, 10),
                cloud_cover=random.randint(20, 100),
                visibility=random.uniform(3, 15),
                uv_index=random.uniform(0, 11),
                condition=random.choice(list(WeatherCondition)),
                timestamp=datetime.now() + timedelta(days=day_offset, hours=hour)
            )
            comfort_index = self._calculate_comfort_index(weather)
            hourly_forecasts.append(HourlyForecast(
                time=weather.timestamp,
                weather=weather,
                comfort_index=comfort_index
            ))
        
        avg_weather = WeatherData(
            temperature=(high_temp + low_temp) / 2,
            humidity=random.randint(40, 80),
            wind_speed=random.uniform(3, 15),
            wind_direction=random.randint(0, 360),
            precipitation=random.uniform(0, 8),
            cloud_cover=random.randint(30, 80),
            visibility=random.uniform(5, 15),
            uv_index=random.uniform(1, 8),
            condition=random.choice(list(WeatherCondition)),
            timestamp=datetime.now() + timedelta(days=day_offset)
        )
        
        return DailyForecast(
            date=datetime.now() + timedelta(days=day_offset),
            high_temp=high_temp,
            low_temp=low_temp,
            avg_humidity=avg_weather.humidity,
            avg_wind_speed=avg_weather.wind_speed,
            total_precipitation=avg_weather.precipitation,
            condition=avg_weather.condition,
            hourly_forecasts=hourly_forecasts,
            comfort_index=self._calculate_comfort_index(avg_weather)
        )
    
    def _calculate_comfort_index(self, weather: WeatherData) -> float:
        """Calculate comfort index (0-100) based on weather conditions"""
        # Temperature comfort (optimal around 20-25°C)
        temp_score = max(0, 100 - abs(weather.temperature - 22.5) * 4)
        
        # Humidity comfort (optimal around 40-60%)
        humidity_score = max(0, 100 - abs(weather.humidity - 50) * 1.5)
        
        # Wind comfort (moderate wind is good)
        wind_score = max(0, 100 - abs(weather.wind_speed - 8) * 5)
        
        # Precipitation penalty
        precip_penalty = min(50, weather.precipitation * 10)
        
        # UV index penalty for high UV
        uv_penalty = min(30, max(0, weather.uv_index - 6) * 5)
        
        # Visibility penalty
        visibility_penalty = min(20, max(0, 10 - weather.visibility) * 2)
        
        comfort = (temp_score + humidity_score + wind_score) / 3 - precip_penalty - uv_penalty - visibility_penalty
        return max(0, min(100, comfort))
    
    def get_long_term_forecast(self, lat: float, lon: float, city_name: str = None) -> LongTermForecast:
        """Generate long-term seasonal outlook (5-6 months)"""
        monthly_outlooks = []
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        
        current_month = datetime.now().month
        for i in range(6):  # Next 6 months
            month = (current_month + i - 1) % 12 + 1
            outlook = self._generate_monthly_outlook(month, lat, lon)
            monthly_outlooks.append(MonthlyOutlook(
                month=month,
                month_name=month_names[month - 1],
                probabilities=outlook["probabilities"],
                avg_temperature=outlook["avg_temperature"],
                avg_precipitation=outlook["avg_precipitation"]
            ))
        
        return LongTermForecast(
            location=city_name or f"{lat},{lon}",
            latitude=lat,
            longitude=lon,
            monthly_outlooks=monthly_outlooks,
            generated_at=datetime.now()
        )
    
    def _generate_monthly_outlook(self, month: int, lat: float, lon: float) -> Dict[str, Any]:
        """Generate monthly climate probabilities based on season and location"""
        # Seasonal patterns based on month
        is_winter = month in [12, 1, 2]
        is_spring = month in [3, 4, 5]
        is_summer = month in [6, 7, 8]
        is_fall = month in [9, 10, 11]
        
        # Latitude-based adjustments
        is_northern_hemisphere = lat > 0
        if not is_northern_hemisphere:
            is_winter, is_spring, is_summer, is_fall = is_summer, is_fall, is_winter, is_spring
        
        # Base probabilities
        if is_summer:
            very_hot = random.uniform(0.4, 0.8)
            very_cold = random.uniform(0.0, 0.1)
            very_wet = random.uniform(0.1, 0.4)
            very_windy = random.uniform(0.2, 0.5)
        elif is_winter:
            very_hot = random.uniform(0.0, 0.1)
            very_cold = random.uniform(0.3, 0.7)
            very_wet = random.uniform(0.2, 0.6)
            very_windy = random.uniform(0.3, 0.6)
        elif is_spring:
            very_hot = random.uniform(0.1, 0.3)
            very_cold = random.uniform(0.1, 0.3)
            very_wet = random.uniform(0.2, 0.5)
            very_windy = random.uniform(0.3, 0.6)
        else:  # fall
            very_hot = random.uniform(0.1, 0.4)
            very_cold = random.uniform(0.1, 0.4)
            very_wet = random.uniform(0.2, 0.5)
            very_windy = random.uniform(0.2, 0.5)
        
        # Calculate uncomfortable days (combination of extreme conditions)
        uncomfortable = min(1.0, (very_hot + very_cold + very_windy) / 3 + very_wet * 0.5)
        
        probabilities = ClimateProbability(
            very_hot=round(very_hot, 2),
            very_cold=round(very_cold, 2),
            very_wet=round(very_wet, 2),
            very_windy=round(very_windy, 2),
            uncomfortable=round(uncomfortable, 2)
        )
        
        # Generate average temperature and precipitation
        if is_summer:
            avg_temp = random.uniform(20, 30)
            avg_precip = random.uniform(20, 80)
        elif is_winter:
            avg_temp = random.uniform(-5, 10)
            avg_precip = random.uniform(30, 100)
        elif is_spring:
            avg_temp = random.uniform(10, 20)
            avg_precip = random.uniform(40, 90)
        else:  # fall
            avg_temp = random.uniform(5, 20)
            avg_precip = random.uniform(30, 80)
        
        return {
            "probabilities": probabilities,
            "avg_temperature": round(avg_temp, 1),
            "avg_precipitation": round(avg_precip, 1)
        }
