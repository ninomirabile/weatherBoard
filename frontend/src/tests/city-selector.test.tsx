import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import CitySelector from '../components/city-selector/city-selector';

const mockCities = ['milano', 'roma', 'london'];

describe('CitySelector', () => {
  it('renders city selector with options', () => {
    const mockOnCitySelect = vi.fn();
    render(<CitySelector cities={mockCities} onCitySelect={mockOnCitySelect} />);
    
    expect(screen.getByText('Select City:')).toBeInTheDocument();
    expect(screen.getByRole('option', { name: 'Choose a city...' })).toBeInTheDocument();
    // Check if cities are rendered
    mockCities.forEach(city => {
      const cityName = city.charAt(0).toUpperCase() + city.slice(1);
      expect(screen.getByText(cityName)).toBeInTheDocument();
    });
  });

  it('calls onCitySelect when a city is selected', () => {
    const mockOnCitySelect = vi.fn();
    render(<CitySelector cities={mockCities} onCitySelect={mockOnCitySelect} />);
    
    const select = screen.getByRole('combobox');
    fireEvent.change(select, { target: { value: 'milano' } });
    
    expect(mockOnCitySelect).toHaveBeenCalledWith('milano');
  });

  it('does not call onCitySelect when empty option is selected', () => {
    const mockOnCitySelect = vi.fn();
    render(<CitySelector cities={mockCities} onCitySelect={mockOnCitySelect} />);
    
    const select = screen.getByRole('combobox');
    fireEvent.change(select, { target: { value: '' } });
    
    expect(mockOnCitySelect).not.toHaveBeenCalled();
  });
}); 