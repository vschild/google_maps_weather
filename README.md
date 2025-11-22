# Google Maps Weather Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![Version](https://img.shields.io/badge/version-1.2.3-blue.svg)](https://github.com/vschild/google_maps_weather/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024.1.0%2B-blue.svg)](https://www.home-assistant.io/)

A custom Home Assistant integration that provides real-time, hyperlocal weather data using the Google Maps Weather API.

## ✨ Features

- 🌤️ **Current weather conditions** with automatic day/night detection
- 📅 **10-day daily forecast** with high/low temperatures
- ⏰ **Hourly forecast** (24 to 240 hours, configurable)
- 📊 **11 detailed sensors**: UV index, dew point, wind, precipitation, and more
- 🎛️ **Configurable update interval** to control API usage
- ⚙️ **Configurable hourly forecast range** (1 to 10 days)
- 📈 **API usage monitoring** to stay within free tier limits
- 🌍 **Metric and Imperial units** support
- 🌐 **Multi-language**: Spanish and English
- ⚡ **Parallel API calls** for optimal performance

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

1. Download the [latest release](https://github.com/vschild/google_maps_weather/releases)
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
   - **Hourly Forecast Hours**: 24 hours (recommended)

## 📊 Entities Created

### Weather Entity
- `weather.google_maps_weather` - Main weather entity with daily and hourly forecasts

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
- **10,000 calls per month**
- After free tier: $0.15 per 1,000 calls

### API Calls Per Update
This integration makes **3+ API calls per update**:
1. Current conditions
2. Daily forecast (10 days)
3. Hourly forecast (configurable: 24-240 hours; 1 call for every 24 hours)

### Recommended Update Intervals

| Interval | Calls/Month | Status |
|----------|-------------|--------|
| 15 min | ~8640 | ✓ Within limit |
| 30 min | ~4320 | ✓ Within limit |
| **60 min** | **~2160** | **✓ Recommended** |
| 90 min | ~1440 | ✓ Within limit |
| 120 min | ~1080 | ✓ Conservative |
| 150 min | ~864 | ✓ Conservative |
| 180 min | ~720 | ✓ Very conservative |
| 240 min | ~540 | ✓ Ultra conservative |

**Note**: Calls/Month are estimated with a 24 hour forecast and for 30 days. ⚠️ Think twice before selecting 10 days (240h) or 7 days (168h) of hourly updates and a 15 or 30 min update interval. 

### Hourly Forecast Options

| Hours | Description | Status |
|-------|-------------|--------|
| **24h** | **1 day** | **✓ Recommended** |
| 48h | 2 days | ✓ Extended - +1 API Calls/update |
| 72h | 3 days | ✓ Extended - +2 API Calls/update|
| 96h | 4 days | ✓ Extended - +3 API Calls/update|
| 120h | 5 days | ✓ Extended - +4 API Calls/update|
| 168h | 7 days | ✓ Full week - +6 API Calls/update|
| 240h | 10 days | ✓ Maximum - +9 API Calls/update|

**Note**: Each additional 24 hour period results in an additional API call. ⚠️ Think twice before selecting 10 days (240h) or 7 days (168h) of hourly updates and a 15 or 30 min update interval.

### Maximumn (31 days, Single location) API usage
|   | 15 min | 30 min | 60 min | 90 min | 120 min | 150 min | 180 min | 240 min |
|---|--------|--------|--------|--------|---------|---------|---------|---------|
| **24h** | 🟢 8928 | 🟢 4464 | 🟢 2232 | 🟢 1488 | 🟢 1116 | 🟢 893 | 🟢 744 | 🟢 558 |
| **48h** | 🔴 11904 | 🟢 5952 | 🟢 2976 | 🟢 1984 | 🟢 1488 | 🟢 1191 | 🟢 992 | 🟢 744 |
| **96h** | 🔴 14880 | 🟢 7440 | 🟢 3720 | 🟢 2480 | 🟢 1860 | 🟢 1488 | 🟢 1240 | 🟢 930 |
| **120h** | 🔴 17856 | 🟢 8928 | 🟢 4464 | 🟢 2976 | 🟢 2232 | 🟢 1786 | 🟢 1488 | 🟢 1116 |
| **168h** | 🔴 23808 | 🔴 11904 | 🟢 5952 | 🟢 3968 | 🟢 2976 | 🟢 2381 | 🟢 1984 | 🟢 1488 |
| **240h** | 🔴 32736 | 🔴 16368 | 🟢 8184 | 🟢 5456 | 🟢 4092 | 🟢 3274 | 🟢 2728 | 🟢 2046 |

### Monitor Your Usage

Use the built-in sensor to track your API usage:

```yaml
type: gauge
entity: sensor.google_maps_weather_api_usage_estimate
name: API Usage
min: 0
max: 10000
```

## 📖 Documentation

- [Installation Guide](INSTALL.md)
- [API Limits Control](CONTROL_LIMITES.md)
- [Configuration Examples](configuration_example.yaml)
- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)

## 🎨 Example Lovelace Cards

### Weather Card with Daily Forecast
```yaml
type: weather-forecast
entity: weather.google_maps_weather
show_forecast: true
forecast_type: daily
```

### Weather Card with Hourly Forecast
```yaml
type: weather-forecast
entity: weather.google_maps_weather
show_forecast: true
forecast_type: hourly
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
2. Set `forecast_type: daily` or `forecast_type: hourly` explicitly
3. Clear browser cache (Ctrl+Shift+R)
4. Check logs for errors
5. Enable debug logging:
   ```yaml
   logger:
     logs:
       custom_components.google_maps_weather: debug
   ```

### Hourly Forecast Not Available
1. Ensure you're running Home Assistant 2024.1.0 or later
2. Check that your weather card supports hourly forecasts
3. Verify the integration is configured with hourly forecast hours
4. Check logs for any API errors related to hourly data

### API Connection Error
1. Verify API key is correct
2. Check Weather API is enabled in Google Cloud Console
3. Verify no IP restrictions on API key
4. Check internet connectivity

### Sensors Show "Unknown"
1. Wait for first update (up to 120 minutes with default settings)
2. Force update: Developer Tools → Services → `homeassistant.update_entity`
3. Check API hasn't exceeded limits
4. Verify all 3 API endpoints are responding correctly

## 🔗 Links

- [Google Weather API Documentation](https://developers.google.com/maps/documentation/weather)
- [Home Assistant](https://www.home-assistant.io/)
- [Issues](https://github.com/vschild/google_maps_weather/issues)
- [Releases](https://github.com/vschild/google_maps_weather/releases)

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

- [Report an Issue](https://github.com/vschild/google_maps_weather/issues)
- [Home Assistant Community Forum](https://community.home-assistant.io/)

---

## 🆕 What's New in v1.2.x

### Hourly Forecast Support
- ⏰ **Hourly forecasts** now available alongside daily forecasts
- ⚙️ **Configurable range**: Choose from 24 to 240 hours
- 🎯 **Dual forecast modes**: Switch between daily and hourly views in Home Assistant

### Enhanced Performance
- ⚡ **Parallel API calls**: All 3 endpoints fetch simultaneously
- 🚀 **No performance penalty**: Fast response times despite multiple calls
- 📊 **Better data coverage**: Current + 10-day daily + configurable hourly

### Improved Configuration
- 🎛️ **New setting**: Hourly forecast hours selector
- 📈 **Updated intervals**: Optimized for 3 API calls per update
- 💡 **Smart defaults**: 30-minute intervals, 24-hour forecasts
- 📱 **Better UI**: Enhanced configuration descriptions

### API Usage Optimization
- 💰 **Still free tier friendly**: Default settings = ~4320 calls/month
- 📊 **Transparent monitoring**: API usage sensor shows calls per update
- ✅ **Stay within limits**: All recommended intervals keep you under 10000/month

---

**Note**: This integration is not officially affiliated with or endorsed by Google or Home Assistant.

**Version**: 1.2.4  
**Last Updated**: November 2025
