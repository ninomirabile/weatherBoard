import { useState } from 'react';

interface CitySelectorProps {
  cities: string[];
  onCitySelect: (city: string) => void;
}

const CitySelector = ({ cities, onCitySelect }: CitySelectorProps) => {
  const [selectedCity, setSelectedCity] = useState('');

  const handleCityChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const city = event.target.value;
    setSelectedCity(city);
    if (city) {
      onCitySelect(city);
    }
  };

  return (
    <div className="flex items-center space-x-2">
      <label htmlFor="city-select" className="text-sm font-medium text-gray-700">
        Select City:
      </label>
      <select
        id="city-select"
        value={selectedCity}
        onChange={handleCityChange}
        className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm rounded-md"
      >
        <option value="">Choose a city...</option>
        {cities.map((city) => (
          <option key={city} value={city}>
            {city.charAt(0).toUpperCase() + city.slice(1)}
          </option>
        ))}
      </select>
    </div>
  );
};

export default CitySelector; 