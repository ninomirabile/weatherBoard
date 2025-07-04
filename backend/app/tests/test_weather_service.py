from app.services.weather_service import WeatherService


class TestWeatherService:
    """Test cases for WeatherService"""

    def setup_method(self):
        """Setup test method"""
        self.service = WeatherService()

    def test_get_available_cities(self):
        """Test getting available cities"""
        cities = self.service.get_available_cities()
        assert isinstance(cities, list)
        assert len(cities) > 0
        assert "milano" in cities
        assert "roma" in cities

    def test_get_weather_data_valid_city(self):
        """Test getting weather data for a valid city"""
        weather_data = self.service.get_weather_data("milano")
        assert weather_data is not None
        assert weather_data.city == "Milano"
        assert isinstance(weather_data.temperature, float)
        assert isinstance(weather_data.humidity, float)
        assert isinstance(weather_data.wind_speed, float)
        assert isinstance(weather_data.description, str)

    def test_get_weather_data_invalid_city(self):
        """Test getting weather data for an invalid city"""
        weather_data = self.service.get_weather_data("invalid_city")
        assert weather_data is None

    def test_get_all_weather_data(self):
        """Test getting weather data for all available cities"""
        all_weather_data = self.service.get_all_weather_data()
        assert isinstance(all_weather_data, list)
        assert len(all_weather_data) > 0

        for weather_data in all_weather_data:
            assert weather_data.city in ["Milano", "Roma", "London", "Paris", "Berlin"]
            assert isinstance(weather_data.temperature, float)
            assert isinstance(weather_data.humidity, float)
            assert isinstance(weather_data.wind_speed, float)
            assert isinstance(weather_data.description, str) 