from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class WeatherData(BaseModel):
    """Weather data model for API responses"""
    city: str = Field(..., description="City name")
    temperature: float = Field(..., description="Temperature in Celsius")
    humidity: float = Field(..., description="Humidity percentage")
    wind_speed: float = Field(..., description="Wind speed in km/h")
    description: str = Field(..., description="Weather description")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Data timestamp")

class WeatherResponse(BaseModel):
    """API response model for weather data"""
    success: bool = Field(..., description="Request success status")
    data: Optional[WeatherData] = Field(None, description="Weather data")
    error: Optional[str] = Field(None, description="Error message if any")

class WeatherListResponse(BaseModel):
    """API response model for weather data list"""
    success: bool = Field(..., description="Request success status")
    data: List[WeatherData] = Field(..., description="List of weather data")
    error: Optional[str] = Field(None, description="Error message if any")

class CitiesResponse(BaseModel):
    """API response model for available cities"""
    success: bool = Field(..., description="Request success status")
    cities: list[str] = Field(..., description="List of available cities") 