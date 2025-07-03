import { useEffect } from 'react';
import { useWeatherStore } from './store/weather-store';
import WeatherDashboard from './features/weather-dashboard/weather-dashboard';
import ErrorToast from './components/error-toast/error-toast';

function App() {
  const { fetchCities, fetchAllWeatherData, loading, error, clearError } = useWeatherStore();

  useEffect(() => {
    // Load initial data
    fetchCities();
    fetchAllWeatherData();
  }, [fetchCities, fetchAllWeatherData]);

  if (loading && !error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading weather data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <h1 className="text-3xl font-bold text-gray-900">
                🌤️ WeatherBoard
              </h1>
            </div>
            <div className="text-sm text-gray-500">
              Real-time Weather Dashboard
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <WeatherDashboard />
      </main>

      <ErrorToast error={error} onClose={clearError} />
    </div>
  );
}

export default App; 