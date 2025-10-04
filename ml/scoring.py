import numpy as np
from typing import Dict, List, Tuple
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import os

class EventSuitabilityMLModel:
    """
    Machine Learning model for event suitability scoring.
    This would typically be trained on historical weather and event data.
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = [
            'temperature', 'humidity', 'wind_speed', 'precipitation',
            'cloud_cover', 'visibility', 'uv_index'
        ]
        self.load_or_train_model()
    
    def load_or_train_model(self):
        """Load pre-trained model or train a new one"""
        model_path = "event_suitability_model.pkl"
        scaler_path = "event_scaler.pkl"
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
        else:
            self.train_model()
    
    def train_model(self):
        """Train the event suitability model with synthetic data"""
        # Generate synthetic training data
        X, y = self._generate_training_data()
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train Random Forest model
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.model.fit(X_scaled, y)
        
        # Save model and scaler
        joblib.dump(self.model, "event_suitability_model.pkl")
        joblib.dump(self.scaler, "event_scaler.pkl")
    
    def _generate_training_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Generate synthetic training data for event suitability"""
        np.random.seed(42)
        n_samples = 10000
        
        # Generate weather features
        X = np.random.rand(n_samples, len(self.feature_columns))
        
        # Scale features to realistic ranges
        X[:, 0] = X[:, 0] * 40 - 10  # temperature: -10 to 30°C
        X[:, 1] = X[:, 1] * 100  # humidity: 0-100%
        X[:, 2] = X[:, 2] * 30  # wind_speed: 0-30 km/h
        X[:, 3] = X[:, 3] * 20  # precipitation: 0-20 mm
        X[:, 4] = X[:, 4] * 100  # cloud_cover: 0-100%
        X[:, 5] = X[:, 5] * 15 + 1  # visibility: 1-16 km
        X[:, 6] = X[:, 6] * 11  # uv_index: 0-11
        
        # Generate target scores based on weather conditions
        y = self._calculate_synthetic_scores(X)
        
        return X, y
    
    def _calculate_synthetic_scores(self, X: np.ndarray) -> np.ndarray:
        """Calculate synthetic suitability scores based on weather features"""
        scores = np.zeros(X.shape[0])
        
        for i in range(X.shape[0]):
            temp, humidity, wind, precip, clouds, visibility, uv = X[i]
            
            # Base score
            score = 50.0
            
            # Temperature scoring (optimal around 20-25°C)
            temp_score = max(0, 100 - abs(temp - 22.5) * 2)
            score = (score + temp_score) / 2
            
            # Humidity scoring (optimal around 40-60%)
            humidity_score = max(0, 100 - abs(humidity - 50) * 1.5)
            score = (score + humidity_score) / 2
            
            # Wind scoring (moderate wind is good)
            wind_score = max(0, 100 - abs(wind - 10) * 3)
            score = (score + wind_score) / 2
            
            # Precipitation penalty
            precip_penalty = min(40, precip * 2)
            score -= precip_penalty
            
            # Visibility penalty
            visibility_penalty = min(20, max(0, 10 - visibility) * 2)
            score -= visibility_penalty
            
            # UV penalty for high UV
            uv_penalty = min(30, max(0, uv - 6) * 5)
            score -= uv_penalty
            
            # Cloud cover bonus (some clouds are good)
            cloud_bonus = max(0, 20 - abs(clouds - 30))
            score += cloud_bonus
            
            scores[i] = max(0, min(100, score))
        
        return scores
    
    def predict_suitability(self, weather_data: Dict[str, float], 
                          event_requirements: Dict[str, float]) -> float:
        """Predict event suitability score using ML model"""
        if self.model is None:
            return 50.0  # Default score if model not available
        
        # Prepare features
        features = np.array([[
            weather_data.get('temperature', 20),
            weather_data.get('humidity', 50),
            weather_data.get('wind_speed', 10),
            weather_data.get('precipitation', 0),
            weather_data.get('cloud_cover', 50),
            weather_data.get('visibility', 10),
            weather_data.get('uv_index', 5)
        ]])
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Predict base score
        base_score = self.model.predict(features_scaled)[0]
        
        # Apply event-specific adjustments
        adjusted_score = self._apply_event_adjustments(
            base_score, weather_data, event_requirements
        )
        
        return max(0, min(100, adjusted_score))
    
    def _apply_event_adjustments(self, base_score: float, 
                               weather_data: Dict[str, float],
                               event_requirements: Dict[str, float]) -> float:
        """Apply event-specific adjustments to the base score"""
        score = base_score
        
        # Temperature requirements
        if 'min_temp' in event_requirements:
            temp = weather_data.get('temperature', 20)
            if temp < event_requirements['min_temp']:
                penalty = (event_requirements['min_temp'] - temp) * 3
                score -= penalty
        
        if 'max_temp' in event_requirements:
            temp = weather_data.get('temperature', 20)
            if temp > event_requirements['max_temp']:
                penalty = (temp - event_requirements['max_temp']) * 2
                score -= penalty
        
        # Wind requirements
        if 'min_wind' in event_requirements:
            wind = weather_data.get('wind_speed', 10)
            if wind < event_requirements['min_wind']:
                penalty = (event_requirements['min_wind'] - wind) * 2
                score -= penalty
        
        if 'max_wind' in event_requirements:
            wind = weather_data.get('wind_speed', 10)
            if wind > event_requirements['max_wind']:
                penalty = (wind - event_requirements['max_wind']) * 3
                score -= penalty
        
        # Precipitation requirements
        if 'max_precipitation' in event_requirements:
            precip = weather_data.get('precipitation', 0)
            if precip > event_requirements['max_precipitation']:
                penalty = (precip - event_requirements['max_precipitation']) * 5
                score -= penalty
        
        return score

class ClimateTrendAnalyzer:
    """
    Analyzes climate trends and patterns for long-term forecasting
    """
    
    def __init__(self):
        self.trend_models = {}
    
    def analyze_trends(self, historical_data: np.ndarray, 
                      months_ahead: int = 6) -> Dict[str, List[float]]:
        """Analyze climate trends from historical data"""
        trends = {
            'temperature_trend': [],
            'precipitation_trend': [],
            'wind_trend': [],
            'humidity_trend': []
        }
        
        # Simple linear trend analysis
        for i in range(months_ahead):
            # This is a simplified trend analysis
            # In practice, you'd use more sophisticated time series methods
            temp_trend = self._calculate_linear_trend(historical_data[:, 0])
            precip_trend = self._calculate_linear_trend(historical_data[:, 1])
            wind_trend = self._calculate_linear_trend(historical_data[:, 2])
            humidity_trend = self._calculate_linear_trend(historical_data[:, 3])
            
            trends['temperature_trend'].append(temp_trend)
            trends['precipitation_trend'].append(precip_trend)
            trends['wind_trend'].append(wind_trend)
            trends['humidity_trend'].append(humidity_trend)
        
        return trends
    
    def _calculate_linear_trend(self, data: np.ndarray) -> float:
        """Calculate linear trend coefficient"""
        if len(data) < 2:
            return 0.0
        
        x = np.arange(len(data))
        slope = np.polyfit(x, data, 1)[0]
        return slope
    
    def detect_anomalies(self, current_data: Dict[str, float], 
                        historical_data: np.ndarray) -> List[str]:
        """Detect weather anomalies compared to historical data"""
        anomalies = []
        
        # Temperature anomaly
        if 'temperature' in current_data:
            temp_mean = np.mean(historical_data[:, 0])
            temp_std = np.std(historical_data[:, 0])
            if abs(current_data['temperature'] - temp_mean) > 2 * temp_std:
                anomalies.append("Temperature anomaly detected")
        
        # Precipitation anomaly
        if 'precipitation' in current_data:
            precip_mean = np.mean(historical_data[:, 1])
            precip_std = np.std(historical_data[:, 1])
            if current_data['precipitation'] > precip_mean + 2 * precip_std:
                anomalies.append("High precipitation anomaly")
        
        return anomalies
