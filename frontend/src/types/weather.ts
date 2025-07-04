export interface WeatherData {
  city: string;
  temperature: number;
  humidity: number;
  wind_speed: number;
  description: string;
  timestamp: string;
}

export interface WeatherResponse {
  success: boolean;
  data?: WeatherData;
  error?: string;
}

export interface WeatherListResponse {
  success: boolean;
  data: WeatherData[];
  error?: string;
}

export interface CitiesResponse {
  success: boolean;
  cities: string[];
}

export interface WeatherState {
  weatherData: WeatherData[];
  cities: string[];
  loading: boolean;
  error: string | null;
  selectedCity: string;
} 