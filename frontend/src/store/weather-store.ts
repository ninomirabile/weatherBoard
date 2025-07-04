import { create } from 'zustand';
import { WeatherState, WeatherResponse, CitiesResponse, WeatherListResponse } from '../types/weather';

const API_BASE_URL = 'http://localhost:8000/api/v1';

interface WeatherStore extends WeatherState {
  selectedCity: string;
  fetchCities: () => Promise<void>;
  fetchWeatherData: (city: string) => Promise<void>;
  fetchAllWeatherData: () => Promise<void>;
  setSelectedCity: (city: string) => void;
  clearError: () => void;
}

export const useWeatherStore = create<WeatherStore>((set, get) => ({
  weatherData: [],
  cities: [],
  loading: false,
  error: null,
  selectedCity: '',

  setSelectedCity: (city: string) => {
    set({ selectedCity: city });
  },

  fetchCities: async () => {
    set({ loading: true, error: null });
    try {
      const response = await fetch(`${API_BASE_URL}/cities`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data: CitiesResponse = await response.json();
      
      if (data.success) {
        set({ cities: data.cities, loading: false });
      } else {
        set({ error: 'Failed to fetch cities', loading: false });
      }
    } catch (error) {
      set({ error: `Error fetching cities: ${error}`, loading: false });
    }
  },

  fetchWeatherData: async (city: string) => {
    set({ loading: true, error: null });
    try {
      const response = await fetch(`${API_BASE_URL}/weather/${city}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data: WeatherResponse = await response.json();
      
      if (data.success && data.data) {
        const currentData = get().weatherData;
        const existingIndex = currentData.findIndex(item => item.city === data.data!.city);
        
        if (existingIndex >= 0) {
          // Update existing city data
          const updatedData = [...currentData];
          updatedData[existingIndex] = data.data;
          set({ weatherData: updatedData, loading: false });
        } else {
          // Add new city data
          set({ weatherData: [...currentData, data.data], loading: false });
        }
      } else {
        set({ error: data.error || 'Failed to fetch weather data', loading: false });
      }
    } catch (error) {
      set({ error: `Error fetching weather data: ${error}`, loading: false });
    }
  },

  fetchAllWeatherData: async () => {
    set({ loading: true, error: null });
    try {
      const response = await fetch(`${API_BASE_URL}/weather`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data: WeatherListResponse = await response.json();
      
      if (data.success) {
        set({ weatherData: data.data, loading: false });
      } else {
        set({ error: data.error || 'Failed to fetch all weather data', loading: false });
      }
    } catch (error) {
      set({ error: `Error fetching all weather data: ${error}`, loading: false });
    }
  },

  clearError: () => {
    set({ error: null });
  },
})); 