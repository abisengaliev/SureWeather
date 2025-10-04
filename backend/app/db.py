import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any
import os

DATABASE_URL = "sqlite:///./nasa_weather.db"

def init_db():
    """Initialize the SQLite database with required tables"""
    conn = sqlite3.connect("nasa_weather.db")
    cursor = conn.cursor()
    
    # Create query history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS query_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            query_type TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            response_data TEXT NOT NULL
        )
    """)
    
    # Create events table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            weather_requirements TEXT NOT NULL,
            min_comfort_score REAL NOT NULL
        )
    """)
    
    # Insert sample events
    sample_events = [
        ("concert", "Outdoor Concert", "sunny_friendly", "Music festival in open air", 
         '{"max_wind": 15, "min_temp": 15, "max_precipitation": 2}', 70),
        ("museum", "Museum Tour", "rain_compatible", "Indoor cultural experience", 
         '{"max_wind": 30, "min_temp": 5, "max_precipitation": 50}', 30),
        ("kite_festival", "Kite Festival", "wind_based", "Wind-powered kite flying", 
         '{"min_wind": 10, "max_wind": 25, "min_temp": 10, "max_precipitation": 5}', 60),
        ("skiing", "Skiing Adventure", "cold_weather", "Snow sports and winter activities", 
         '{"max_temp": 5, "min_precipitation": 5, "max_wind": 20}', 50),
        ("hiking", "Mountain Hiking", "sunny_friendly", "Outdoor nature exploration", 
         '{"max_wind": 20, "min_temp": 10, "max_precipitation": 5, "min_visibility": 5}', 80)
    ]
    
    cursor.executemany("""
        INSERT OR REPLACE INTO events (id, name, category, description, weather_requirements, min_comfort_score)
        VALUES (?, ?, ?, ?, ?, ?)
    """, sample_events)
    
    conn.commit()
    conn.close()

def save_query(location: str, latitude: float, longitude: float, 
               query_type: str, response_data: Dict[str, Any]):
    """Save a query to the database"""
    conn = sqlite3.connect("nasa_weather.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO query_history (location, latitude, longitude, query_type, timestamp, response_data)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (location, latitude, longitude, query_type, datetime.now(), json.dumps(response_data)))
    
    conn.commit()
    conn.close()

def get_query_history(limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieve query history from the database"""
    conn = sqlite3.connect("nasa_weather.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, location, latitude, longitude, query_type, timestamp, response_data
        FROM query_history
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            "id": row[0],
            "location": row[1],
            "latitude": row[2],
            "longitude": row[3],
            "query_type": row[4],
            "timestamp": row[5],
            "response_data": json.loads(row[6])
        }
        for row in rows
    ]

def get_events() -> List[Dict[str, Any]]:
    """Retrieve all events from the database"""
    conn = sqlite3.connect("nasa_weather.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            "id": row[0],
            "name": row[1],
            "category": row[2],
            "description": row[3],
            "weather_requirements": json.loads(row[4]),
            "min_comfort_score": row[5]
        }
        for row in rows
    ]
