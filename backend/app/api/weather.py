from fastapi import APIRouter, HTTPException
from typing import List

from app.models.weather import WeatherResponse, CitiesResponse, WeatherListResponse, WeatherData
from app.services import get_weather_data_service

router = APIRouter()
weather_service = get_weather_data_service()

@router.get("/cities", response_model=CitiesResponse)
async def get_available_cities():
    """Get list of available cities for weather data"""
    try:
        cities = weather_service.get_available_cities()
        return CitiesResponse(
            success=True,
            cities=cities
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/weather/{city}", response_model=WeatherResponse)
async def get_weather_data(city: str):
    """Get weather data for a specific city"""
    try:
        weather_data = weather_service.get_weather_data(city)
        
        if weather_data is None:
            return WeatherResponse(
                success=False,
                error=f"City '{city}' not found. Available cities: {weather_service.get_available_cities()}"
            )
        
        return WeatherResponse(
            success=True,
            data=weather_data
        )
    except Exception as e:
        return WeatherResponse(
            success=False,
            error=str(e)
        )

@router.get("/weather", response_model=WeatherListResponse)
async def get_all_weather_data():
    """Get weather data for all available cities"""
    try:
        weather_data = weather_service.get_all_weather_data()
        return WeatherListResponse(
            success=True,
            data=weather_data
        )
    except Exception as e:
        return WeatherListResponse(
            success=False,
            data=[],
            error=str(e)
        ) 