import random
from typing import List, Optional
from datetime import datetime

from app.models.weather import WeatherData


class WeatherService:
    """Service for managing weather data"""

    # Available cities for Phase 1
    AVAILABLE_CITIES = ["milano", "roma", "london", "paris", "berlin"]

    # Weather descriptions for simulation
    WEATHER_DESCRIPTIONS = [
        "Sunny", "Cloudy", "Rainy", "Partly Cloudy",
        "Overcast", "Light Rain", "Heavy Rain", "Clear"
    ]

    def __init__(self):
        """Initialize weather service"""
        pass

    def get_available_cities(self) -> List[str]:
        """Get list of available cities"""
        return self.AVAILABLE_CITIES.copy()

    def get_weather_data(self, city: str) -> Optional[WeatherData]:
        """
        Get weather data for a specific city
        Phase 1: Returns simulated data
        Phase 2: Will return real-time MQTT data
        """
        if city.lower() not in [c.lower() for c in self.AVAILABLE_CITIES]:
            return None

        # Simulate weather data (Phase 1)
        weather_data = WeatherData(
            city=city.title(),
            temperature=round(random.uniform(-10, 35), 1),  # -10°C to 35°C
            humidity=round(random.uniform(30, 90), 1),      # 30% to 90%
            wind_speed=round(random.uniform(0, 50), 1),     # 0 to 50 km/h
            description=random.choice(self.WEATHER_DESCRIPTIONS),
            timestamp=datetime.utcnow()
        )

        return weather_data

    def get_all_weather_data(self) -> List[WeatherData]:
        """Get weather data for all available cities"""
        weather_data_list = []

        for city in self.AVAILABLE_CITIES:
            weather_data = self.get_weather_data(city)
            if weather_data:
                weather_data_list.append(weather_data)

        return weather_data_list 