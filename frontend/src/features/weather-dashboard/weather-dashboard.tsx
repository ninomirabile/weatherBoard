import { useWeatherStore } from '../../store/weather-store';
import WeatherCard from '../../components/weather-card/weather-card';
import CitySelector from '../../components/city-selector/city-selector';

const WeatherDashboard = () => {
  const { weatherData, cities, fetchWeatherData, loading } = useWeatherStore();

  const handleCitySelect = (city: string) => {
    fetchWeatherData(city);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Weather Dashboard</h2>
          <p className="mt-1 text-sm text-gray-500">
            Real-time weather information for selected cities
          </p>
        </div>
        <div className="mt-4 sm:mt-0">
          <CitySelector cities={cities} onCitySelect={handleCitySelect} />
        </div>
      </div>

      {loading && (
        <div className="flex justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>
      )}

      {weatherData.length === 0 && !loading && (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No weather data</h3>
          <p className="text-gray-500">Select a city to view weather information</p>
        </div>
      )}

      {weatherData.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {weatherData.map((weather) => (
            <WeatherCard key={weather.city} weather={weather} />
          ))}
        </div>
      )}
    </div>
  );
};

export default WeatherDashboard; 