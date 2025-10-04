#!/usr/bin/env python3
"""
Simple server startup script for SureWeather backend
"""
import uvicorn
from app.main import app

if __name__ == "__main__":
    print("🌍 SureWeather Backend Starting...")
    print("📍 Server: http://127.0.0.1:8000")
    print("📚 API Docs: http://127.0.0.1:8000/docs")
    print("=" * 50)
    
    try:
        uvicorn.run(
            app, 
            host="127.0.0.1", 
            port=8000, 
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")