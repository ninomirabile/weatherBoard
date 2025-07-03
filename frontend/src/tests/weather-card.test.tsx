import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import WeatherCard from '../components/weather-card/weather-card';
import { WeatherData } from '../types/weather';

const mockWeatherData: WeatherData = {
  city: 'Milano',
  temperature: 22.5,
  humidity: 65.0,
  wind_speed: 12.3,
  description: 'Sunny',
  timestamp: '2024-01-01T12:00:00Z'
};

describe('WeatherCard', () => {
  it('renders weather information correctly', () => {
    render(<WeatherCard weather={mockWeatherData} />);
    
    expect(screen.getByText('Milano')).toBeInTheDocument();
    expect(screen.getByText('22.5°C')).toBeInTheDocument();
    expect(screen.getByText('65%')).toBeInTheDocument();
    expect(screen.getByText('12.3 km/h')).toBeInTheDocument();
    expect(screen.getByText('Sunny')).toBeInTheDocument();
  });

  it('displays weather icon', () => {
    render(<WeatherCard weather={mockWeatherData} />);
    
    // Check if weather icon is present (emoji)
    expect(screen.getByText('☀️')).toBeInTheDocument();
  });

  it('formats timestamp correctly', () => {
    render(<WeatherCard weather={mockWeatherData} />);
    // Cerca un testo che assomiglia a un orario (es: 12:00, 12.00, ecc.)
    const timeRegex = /\b\d{2}[:\.]\d{2}\b/;
    const timeElement = screen.getByText((content) => timeRegex.test(content));
    expect(timeElement).toBeInTheDocument();
  });
}); 