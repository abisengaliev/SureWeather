from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from .routes import router
from .db import init_db

app = FastAPI(
    title="SureWeather API",
    description="Weather forecasting and event suitability API for NASA Space Apps",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api/v1")

# Initialize database
@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
async def root():
    return {"message": "SureWeather API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "nasa-weather-api"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
