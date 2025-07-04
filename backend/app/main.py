from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.api import weather
from app.services import get_weather_data_service

app = FastAPI(
    title="WeatherBoard API",
    description="Real-time weather data API for WeatherBoard application",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(weather.router, prefix="/api/v1", tags=["weather"])


@app.get("/")
async def root():
    return {"message": "WeatherBoard API is running"}


@app.get("/health")
async def health_check():
    """Health check endpoint with service status"""
    data_source = os.getenv("DATA_SOURCE", "mock").lower()

    health_status = {
        "status": "healthy",
        "data_source": data_source,
        "timestamp": "2024-01-01T00:00:00Z"
    }

    # Add MQTT-specific health info if using MQTT
    if data_source == "mqtt":
        weather_service = get_weather_data_service()
        if hasattr(weather_service, '_client'):
            mqtt_status = (
                "connected" if weather_service._client.is_connected()
                else "disconnected"
            )
            health_status["mqtt_status"] = mqtt_status
            health_status["mqtt_broker"] = (
                f"{weather_service.broker_host}:{weather_service.broker_port}"
            )

    return health_status 