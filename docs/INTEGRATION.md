# WeatherBoard Backend – Integration & Data Source Switch (Mock/MQTT)

This guide explains how to integrate the WeatherBoard backend with simulated (mock) or real data via MQTT, how to configure the data source switch, and how to test integration with external simulators.

---

## 1. Operating Modes

WeatherBoard backend can be started in two modes:
- **Mock**: generates random data on each request (default, ideal for development and testing)
- **MQTT**: subscribes to an MQTT broker and serves real-time data received (from simulators or sensors)

The mode is selected via the `DATA_SOURCE` environment variable:

```bash
# Mock mode (default)
DATA_SOURCE=mock

# MQTT mode
DATA_SOURCE=mqtt
MQTT_BROKER_HOST=localhost
MQTT_BROKER_PORT=1883
```

---

## 2. Starting the Backend

### Mock (default)
```bash
uvicorn app.main:app --reload
```

### MQTT
```bash
DATA_SOURCE=mqtt MQTT_BROKER_HOST=localhost MQTT_BROKER_PORT=1883 uvicorn app.main:app --reload
```

---

## 3. MQTT Payload Format

The backend expects JSON messages with this structure (model `WeatherData`):

```json
{
  "city": "Milano",
  "temperature": 18.3,
  "humidity": 65.5,
  "wind_speed": 10.4,
  "description": "Heavy Rain",
  "timestamp": "2024-07-03T11:34:00Z"
}
```

**Required fields:**
- `city`: string (must match one of the available cities)
- `temperature`: float (°C)
- `humidity`: float (%)
- `wind_speed`: float (km/h)
- `description`: string (e.g. "Sunny", "Heavy Rain", ...)
- `timestamp`: ISO 8601 string (e.g. "2024-07-03T11:34:00Z")

---

## 4. Data Publishing Examples

### With mosquitto_pub
```bash
mosquitto_pub -h localhost -p 1883 -t /weather/milano -m '{
  "city": "Milano",
  "temperature": 18.3,
  "humidity": 65.5,
  "wind_speed": 10.4,
  "description": "Heavy Rain",
  "timestamp": "2024-07-03T11:34:00Z"
}'
```

### With Python (paho-mqtt)
```python
import paho.mqtt.publish as publish
import json

data = {
    "city": "Milano",
    "temperature": 18.3,
    "humidity": 65.5,
    "wind_speed": 10.4,
    "description": "Heavy Rain",
    "timestamp": "2024-07-03T11:34:00Z"
}
publish.single(
    topic="/weather/milano",
    payload=json.dumps(data),
    hostname="localhost",
    port=1883
)
```

---

## 5. Debug & Troubleshooting
- If the backend does not receive data, check that the simulator is publishing to the correct topic and that the payload is valid.
- Backend logs will show any parsing or validation errors.
- If the dashboard shows empty data in MQTT mode, make sure at least one valid message has been published for each city.

---

## 6. FAQ / Best Practices
- You can add new cities by editing the `AVAILABLE_CITIES` list in both the backend and the simulator.
- The backend is extensible: you can add new data sources by implementing a new service and adding the switch in the factory.
- For end-to-end testing, start Mosquitto, the MQTT simulator, and the backend in MQTT mode.

---

## 7. Useful Links
- [WeatherBoard README](../README.md)
- [Example MQTT Simulator](https://github.com/your-user/mqtt-simulator)
- [paho-mqtt documentation](https://www.eclipse.org/paho/index.php?page=clients/python/index.php) 