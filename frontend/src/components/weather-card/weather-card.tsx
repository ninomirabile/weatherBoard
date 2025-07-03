import { WeatherData } from '../../types/weather';

interface WeatherCardProps {
  weather: WeatherData;
}

const WeatherCard = ({ weather }: WeatherCardProps) => {
  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString('it-IT', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getWeatherIcon = (description: string) => {
    const descriptionLower = description.toLowerCase();
    
    if (descriptionLower.includes('sunny') || descriptionLower.includes('clear')) {
      return '☀️';
    } else if (descriptionLower.includes('cloudy') || descriptionLower.includes('overcast')) {
      return '☁️';
    } else if (descriptionLower.includes('rainy') || descriptionLower.includes('rain')) {
      return '🌧️';
    } else if (descriptionLower.includes('partly')) {
      return '⛅';
    } else {
      return '🌤️';
    }
  };

  return (
    <div className="weather-card">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-xl font-semibold text-gray-900">{weather.city}</h3>
          <p className="text-sm text-gray-500">{formatTimestamp(weather.timestamp)}</p>
        </div>
        <div className="text-3xl">
          {getWeatherIcon(weather.description)}
        </div>
      </div>

      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-gray-600">Temperature</span>
          <span className="text-2xl font-bold text-gray-900">
            {weather.temperature}°C
          </span>
        </div>

        <div className="flex items-center justify-between">
          <span className="text-gray-600">Humidity</span>
          <span className="font-semibold text-gray-900">
            {weather.humidity}%
          </span>
        </div>

        <div className="flex items-center justify-between">
          <span className="text-gray-600">Wind Speed</span>
          <span className="font-semibold text-gray-900">
            {weather.wind_speed} km/h
          </span>
        </div>

        <div className="pt-3 border-t border-gray-200">
          <span className="text-sm font-medium text-gray-700 capitalize">
            {weather.description}
          </span>
        </div>
      </div>
    </div>
  );
};

export default WeatherCard; 