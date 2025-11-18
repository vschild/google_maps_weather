# Google Maps Weather Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/yourusername/google-maps-weather.svg)](https://github.com/yourusername/google-maps-weather/releases)
[![License](https://img.shields.io/github/license/yourusername/google-maps-weather.svg)](LICENSE)

A custom Home Assistant integration that provides real-time, hyperlocal weather data using the Google Maps Weather API.

## ✨ Features

- 🌤️ **Current weather conditions** with automatic day/night detection
- 📅 **10-day weather forecast**
- 📊 **11 detailed sensors**: UV index, dew point, wind, precipitation, and more
- 🎛️ **Configurable update interval** to control API usage
- 📈 **API usage monitoring** to stay within free tier limits
- 🌍 **Metric and Imperial units** support
- 🌐 **Multi-language**: Spanish and English

## 📸 Screenshots

### Weather Card
![Weather Card](screenshots/weather-card.png)

### Sensors
![Sensors](screenshots/sensors.png)

## 🚀 Quick Start

### Prerequisites

1. **Google Maps API Key**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a project or select existing one
   - Enable **Weather API**
   - Create an API key in Credentials

2. **Home Assistant 2024.1.0+**

### Installation

#### Option 1: HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots in the top right
4. Select "Custom repositories"
5. Add this repository URL
6. Click "Install"
7. Restart Home Assistant

#### Option 2: Manual Installation

1. Download the [latest release](https://github.com/yourusername/google-maps-weather/releases)
2. Extract the `google_maps_weather` folder
3. Copy to `/config/custom_components/google_maps_weather/`
4. Restart Home Assistant

### Configuration

1. Go to **Configuration** → **Devices & Services**
2. Click **+ ADD INTEGRATION**
3. Search for "Google Maps Weather"
4. Enter your configuration:
   - **API Key**: Your Google Maps API key
   - **Latitude**: Your location (auto-filled)
   - **Longitude**: Your location (auto-filled)
   - **Units**: METRIC or IMPERIAL
   - **Update Interval**: 60 minutes (recommended)

## 📊 Entities Created

### Weather Entity
- `weather.google_maps_weather` - Main weather entity with forecast

### Sensors (11 total)
- `sensor.google_maps_weather_uv_index` - UV index
- `sensor.google_maps_weather_dew_point` - Dew point temperature
- `sensor.google_maps_weather_heat_index` - Heat index
- `sensor.google_maps_weather_wind_chill` - Wind chill temperature
- `sensor.google_maps_weather_wind_gust` - Wind gust speed
- `sensor.google_maps_weather_wind_direction` - Wind direction
- `sensor.google_maps_weather_cloud_cover` - Cloud coverage
- `sensor.google_maps_weather_thunderstorm_probability` - Thunderstorm probability
- `sensor.google_maps_weather_precipitation_probability` - Precipitation probability
- `sensor.google_maps_weather_precipitation_amount` - Precipitation amount
- `sensor.google_maps_weather_api_usage_estimate` - Monthly API usage estimate

## 💰 API Usage & Costs

### Free Tier
- **1,000 calls per month** (during Preview period)
- After free tier: $0.15 per 1,000 calls

### Update Intervals

| Interval | Calls/Month | Status |
|----------|-------------|--------|
| 45 min | ~960 | ✓ Within limit |
| **60 min** | **~720** | **✓ Recommended** |
| 90 min | ~480 | ✓ Conservative |
| 120 min | ~360 | ✓ Very conservative |

**All intervals stay within the free tier!**

### Monitor Your Usage

Use the built-in sensor to track your API usage:

```yaml
type: gauge
entity: sensor.google_maps_weather_api_usage_estimate
name: API Usage
min: 0
max: 1000
```

## 📖 Documentation

- [Installation Guide](INSTALL.md)
- [API Limits Control](CONTROL_LIMITES.md)
- [Configuration Examples](configuration_example.yaml)
- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)

## 🎨 Example Lovelace Cards

### Basic Weather Card
```yaml
type: weather-forecast
entity: weather.google_maps_weather
show_forecast: true
```

### Detailed Sensors Card
```yaml
type: entities
title: Weather Details
entities:
  - sensor.google_maps_weather_uv_index
  - sensor.google_maps_weather_precipitation_probability
  - sensor.google_maps_weather_wind_gust
  - sensor.google_maps_weather_api_usage_estimate
```

### API Usage Monitoring
```yaml
type: entities
title: API Usage Monitor
entities:
  - entity: sensor.google_maps_weather_api_usage_estimate
    name: Monthly Calls
  - type: attribute
    entity: sensor.google_maps_weather_api_usage_estimate
    attribute: usage_percentage
    name: "% of Limit"
  - type: attribute
    entity: sensor.google_maps_weather_api_usage_estimate
    attribute: status
    name: Status
```

## 🤖 Automation Examples

### Rain Alert
```yaml
automation:
  - alias: "Rain Alert"
    trigger:
      - platform: numeric_state
        entity_id: sensor.google_maps_weather_precipitation_probability
        above: 70
    action:
      - service: notify.mobile_app
        data:
          message: "High chance of rain! Bring an umbrella ☔"
```

### High UV Alert
```yaml
automation:
  - alias: "High UV Alert"
    trigger:
      - platform: numeric_state
        entity_id: sensor.google_maps_weather_uv_index
        above: 6
    action:
      - service: notify.mobile_app
        data:
          message: "UV index is high. Use sunscreen! ☀️"
```

More examples in [configuration_example.yaml](configuration_example.yaml)

## 🐛 Troubleshooting

### No Forecast Showing
1. Ensure `show_forecast: true` in your weather card
2. Clear browser cache (Ctrl+Shift+R)
3. Check logs for errors
4. Enable debug logging:
   ```yaml
   logger:
     logs:
       custom_components.google_maps_weather: debug
   ```

### API Connection Error
1. Verify API key is correct
2. Check Weather API is enabled in Google Cloud Console
3. Verify no IP restrictions on API key
4. Check internet connectivity

### Sensors Show "Unknown"
1. Wait for first update (up to 60 minutes)
2. Force update: Developer Tools → Services → `homeassistant.update_entity`
3. Check API hasn't exceeded limits

## 🔗 Links

- [Google Weather API Documentation](https://developers.google.com/maps/documentation/weather)
- [Home Assistant](https://www.home-assistant.io/)
- [Issues](https://github.com/yourusername/google-maps-weather/issues)
- [Releases](https://github.com/yourusername/google-maps-weather/releases)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Maps Platform for the Weather API
- Home Assistant community
- All contributors

## ⭐ Support

If you find this integration useful, please consider:
- Starring the repository ⭐
- Reporting bugs and suggesting features
- Contributing code or documentation
- Sharing with others

## 📞 Support & Community

- [Report an Issue](https://github.com/yourusername/google-maps-weather/issues)
- [Home Assistant Community Forum](https://community.home-assistant.io/)

---

**Note**: This integration is not officially affiliated with or endorsed by Google or Home Assistant.

**Version**: 1.1.4  
**Last Updated**: November 2025
