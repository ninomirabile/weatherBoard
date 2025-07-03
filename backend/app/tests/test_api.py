import pytest
import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestWeatherAPI:
    """Test cases for Weather API endpoints"""
    
    @pytest.fixture(autouse=True)
    def set_mock_mode(self):
        os.environ["DATA_SOURCE"] = "mock"
        yield
        os.environ.pop("DATA_SOURCE", None)

    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "WeatherBoard API is running"}
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "data_source" in data
        assert "timestamp" in data
        assert data["data_source"] == "mock"
    
    def test_get_cities(self):
        """Test getting available cities"""
        response = client.get("/api/v1/cities")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "cities" in data
        assert isinstance(data["cities"], list)
        assert len(data["cities"]) > 0
        assert "milano" in data["cities"]
    
    def test_get_weather_data_valid_city(self):
        """Test getting weather data for a valid city"""
        response = client.get("/api/v1/weather/milano")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        
        weather_data = data["data"]
        assert weather_data["city"] == "Milano"
        assert "temperature" in weather_data
        assert "humidity" in weather_data
        assert "wind_speed" in weather_data
        assert "description" in weather_data
        assert "timestamp" in weather_data
    
    def test_get_weather_data_invalid_city(self):
        """Test getting weather data for an invalid city"""
        response = client.get("/api/v1/weather/invalid_city")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is False
        assert "error" in data
        assert "not found" in data["error"].lower()
    
    def test_get_all_weather_data(self):
        """Test getting weather data for all cities"""
        response = client.get("/api/v1/weather")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) > 0
        
        for weather_data in data["data"]:
            assert "city" in weather_data
            assert "temperature" in weather_data
            assert "humidity" in weather_data
            assert "wind_speed" in weather_data
            assert "description" in weather_data
            assert "timestamp" in weather_data 