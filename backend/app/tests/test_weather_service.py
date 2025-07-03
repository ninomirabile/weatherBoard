import pytest
import os
from app.services import get_weather_data_service

class TestWeatherService:
    """Test cases for WeatherService (mock mode)"""

    @pytest.fixture(autouse=True)
    def set_mock_mode(self):
        os.environ["DATA_SOURCE"] = "mock"
        yield
        os.environ.pop("DATA_SOURCE", None)
        
    def setup_method(self):
        """Setup method for each test"""
        self.weather_service = get_weather_data_service()
    
    def test_get_available_cities(self):
        """Test getting available cities"""
        cities = self.weather_service.get_available_cities()
        
        assert isinstance(cities, list)
        assert len(cities) > 0
        assert "milano" in cities
        assert "roma" in cities
        assert "london" in cities
    
    def test_get_weather_data_valid_city(self):
        """Test getting weather data for a valid city"""
        weather_data = self.weather_service.get_weather_data("milano")
        
        assert weather_data is not None
        assert weather_data.city == "Milano"
        assert isinstance(weather_data.temperature, float)
        assert isinstance(weather_data.humidity, float)
        assert isinstance(weather_data.wind_speed, float)
        assert isinstance(weather_data.description, str)
        assert -10 <= weather_data.temperature <= 35
        assert 30 <= weather_data.humidity <= 90
        assert 0 <= weather_data.wind_speed <= 50
    
    def test_get_weather_data_invalid_city(self):
        """Test getting weather data for an invalid city"""
        weather_data = self.weather_service.get_weather_data("invalid_city")
        
        assert weather_data is None
    
    def test_get_all_weather_data(self):
        """Test getting weather data for all cities"""
        all_weather_data = self.weather_service.get_all_weather_data()
        
        assert isinstance(all_weather_data, list)
        assert len(all_weather_data) == len(self.weather_service.get_available_cities())
        
        for weather_data in all_weather_data:
            assert weather_data.city in [city.title() for city in self.weather_service.get_available_cities()] 