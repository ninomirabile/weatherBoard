import os
import json
import time
from typing import List, Optional, Dict
from threading import Thread, Lock
import paho.mqtt.client as mqtt
from app.models.weather import WeatherData


class MQTTWeatherService:
    """Service for managing weather data from MQTT broker"""
    AVAILABLE_CITIES = ["milano", "roma", "london", "paris", "berlin"]
    CACHE_TTL = 300  # 5 minutes cache TTL

    def __init__(self):
        self.broker_host = os.getenv("MQTT_BROKER_HOST", "localhost")
        self.broker_port = int(os.getenv("MQTT_BROKER_PORT", 1883))
        self._weather_cache: Dict[str, tuple[WeatherData, float]] = {}
        self._cache_lock = Lock()
        self._client = mqtt.Client()
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.on_disconnect = self._on_disconnect
        self._running = True

        # Start MQTT client in a background thread
        self._thread = Thread(target=self._start_mqtt_loop, daemon=True)
        self._thread.start()

    def _start_mqtt_loop(self):
        try:
            self._client.connect(self.broker_host, self.broker_port, keepalive=60)
            self._client.loop_forever()
        except Exception as e:
            print(f"[MQTT] Connection error: {e}")

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"[MQTT] Connected to broker at {self.broker_host}:{self.broker_port}")
            for city in self.AVAILABLE_CITIES:
                topic = f"/weather/{city}"
                client.subscribe(topic)
                print(f"[MQTT] Subscribed to {topic}")
        else:
            print(f"[MQTT] Connection failed with code {rc}")

    def _on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print(f"[MQTT] Unexpected disconnection with code {rc}")

    def _on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode("utf-8")
            data = json.loads(payload)
            # Validate and parse with Pydantic
            weather = WeatherData(**data)
            city = weather.city.lower()

            with self._cache_lock:
                self._weather_cache[city] = (weather, time.time())
            print(f"[MQTT] Updated cache for {city}: {weather}")
        except Exception as e:
            print(f"[MQTT] Error processing message on {msg.topic}: {e}")

    def _clean_expired_cache(self):
        """Remove expired entries from cache"""
        current_time = time.time()
        with self._cache_lock:
            expired_cities = [
                city for city, (_, timestamp) in self._weather_cache.items()
                if current_time - timestamp > self.CACHE_TTL
            ]
            for city in expired_cities:
                del self._weather_cache[city]
                print(f"[MQTT] Removed expired cache for {city}")

    def get_available_cities(self) -> List[str]:
        return self.AVAILABLE_CITIES.copy()

    def get_weather_data(self, city: str) -> Optional[WeatherData]:
        self._clean_expired_cache()
        with self._cache_lock:
            cache_entry = self._weather_cache.get(city.lower())
            if cache_entry:
                weather_data, _ = cache_entry
                return weather_data
        return None

    def get_all_weather_data(self) -> List[WeatherData]:
        self._clean_expired_cache()
        with self._cache_lock:
            return [data for data, _ in self._weather_cache.values() if data is not None]

    def shutdown(self):
        """Graceful shutdown of MQTT service"""
        self._running = False
        if self._client.is_connected():
            self._client.disconnect()
        print("[MQTT] Service shutdown complete") 