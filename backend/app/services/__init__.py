# Business logic services for WeatherBoard 
import os
from .weather_service import WeatherService
from .mqtt_service import MQTTWeatherService

def get_weather_data_service():
    data_source = os.getenv("DATA_SOURCE", "mock").lower()
    if data_source == "mqtt":
        return MQTTWeatherService()
    return WeatherService() 