# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.2.0] - 2025-11-18

### 🎉 Added

#### Hourly Forecast Support
- ⏰ Full hourly forecast support alongside daily forecasts
- ⚙️ Configurable hourly range: 24 to 240 hours (1 to 10 days)
- 📊 Default: 48 hours (2 days)
- 🎯 Dual forecast modes: Switch between daily and hourly views in Home Assistant
- 🌙 Automatic day/night detection in hourly forecasts
- New UI configuration field: "Hourly Forecast Hours" with 7 options (24, 48, 72, 96, 120, 168, 240 hours)

#### Parallel API Calls
- ⚡ 3 API endpoints now execute simultaneously using `asyncio.gather()`
- 🚀 No performance penalty despite multiple calls
- 📡 Endpoints: current conditions + daily forecast + hourly forecast
- ⏱️ Response time similar to a single sequential call

### 🔄 Changed

#### API Usage Updates
**IMPORTANT**: Now makes **3 API calls per update** (previously 2)

**Updated Intervals:**
- Recommended: **120 minutes** (~720 calls/month) - stays within free tier
- Conservative: 150 minutes (~576 calls/month)
- Very conservative: 180 minutes (~480 calls/month)
- Ultra conservative: 240 minutes (~360 calls/month)
- Removed intervals < 90 min (would exceed free tier limit)

**Improved Monitoring:**
- API usage sensor updated to account for 3 calls per update
- New attribute: `calls_per_update: 3`
- Accurate monthly usage calculation

### 🔧 Technical Changes

**Modified Files:**
- `const.py` - New constants and configuration options
- `config_flow.py` - Added hourly forecast hours field
- `__init__.py` - Implemented parallel API calls with asyncio
- `weather.py` - Full hourly forecast support
- `sensor.py` - Updated API usage calculations
- `strings.json` - Updated Spanish translations
- `translations/en.json` - Updated English translations
- `manifest.json` - Version 1.2.0
- `README.md` - Complete documentation of new features

**weather.py - New Methods:**
```python
async def async_forecast_hourly() -> list[Forecast] | None
def _generate_forecast_hourly() -> list[Forecast] | None

# Updated features
_attr_supported_features = (
    WeatherEntityFeature.FORECAST_DAILY | WeatherEntityFeature.FORECAST_HOURLY
)
```

**__init__.py - Parallel Calls:**
```python
current, forecast_daily, forecast_hourly = await asyncio.gather(
    api.get_current_conditions(),
    api.get_daily_forecast(),
    api.get_hourly_forecast(hours=hourly_forecast_hours)
)
```

### 💰 Cost Impact

| Configuration | Before | After |
|---------------|--------|-------|
| Calls per update | 2 | 3 |
| Recommended interval | 60 min | 120 min |
| Monthly calls (recommended) | ~720 | ~720 |

**Result**: More data, same API consumption ✅

### 🎨 New UI Capabilities

**Weather Cards:**
```yaml
# Daily view
type: weather-forecast
entity: weather.google_maps_weather
forecast_type: daily

# Hourly view (NEW)
type: weather-forecast
entity: weather.google_maps_weather
forecast_type: hourly
```

### ⚠️ Migration Notes

- **New installations**: Everything configured automatically
- **Upgrades**: 
  - "hourly_forecast_hours" field will be added with default value (48h)
  - Update interval will remain as configured
  - Consider adjusting interval if using < 90 minutes

### 🐛 Fixed

- More efficient logs for hourly forecasts (only first 3 hours shown)
- Robust validation of hourly forecast data
- Improved error handling in `_generate_forecast_hourly()`

---

## [1.1.2] - 2024-11

### 🐛 Fixed

#### Critical Day/Night Detection Fix
- Now correctly detects day or night conditions
- Uses `clear-night` when clear at night
- Uses `sunny` when clear during the day
- Reads `isDaytime` field from Google API

#### Definitive Forecast Fix
- Removed `_async_forecast_daily()` method with callback (doesn't work in HA 2024.x)
- Correctly implemented `async_forecast_daily()` only
- Added cache system for forecasts
- Cache automatically invalidates on each update
- Improved debug logging

#### Enhanced Logging
- More detailed logs for forecast processing
- Information for each generated day
- Better error handling with full traceback

### 🔧 Technical Changes

**Modified Files:**
- `weather.py` - Complete fix for forecast and day/night conditions
- `const.py` - Updated comments in CONDITION_MAP
- `manifest.json` - Version 1.1.2

**Day/Night Detection:**
```python
is_daytime = current.get("isDaytime", True)
if condition == "sunny" and not is_daytime:
    condition = "clear-night"
```

**Forecast with Cache:**
```python
async def async_forecast_daily(self) -> list[Forecast] | None:
    if self._forecast_cache is not None:
        return self._forecast_cache
    forecast = self._generate_forecast()
    self._forecast_cache = forecast
    return forecast
```

---

## [1.1.1] - 2024-11

### 🐛 Fixed

#### UV Index Sensor Fix
- Removed incompatible `device_class` from UV Index sensor
- Solved error: "is not a valid unit for device class 'irradiance'"
- Sensor now works correctly without warnings

#### Daily Forecast Fix (Attempt 1)
- Fixed `async_forecast_daily()` method for Home Assistant 2024.x
- Added `_async_forecast_daily()` method with callback
- Improved date parsing from API
- Added debug logs for troubleshooting

### 🔧 Modified Files
- `sensor.py` - UV Index fix
- `weather.py` - Forecast fix + improved logging
- `manifest.json` - Version 1.1.1

---

## [1.1.0] - 2024-11

### 🎯 Goal
Add complete control over API usage to stay within the free tier limit of 1,000 calls per month.

### ✨ Added

#### Configurable Update Interval

**Modified Files**: `config_flow.py`, `const.py`, `__init__.py`

**Available Options:**
- 45 minutes (~960 calls/month)
- 60 minutes (~720 calls/month) - Recommended ⭐
- 90 minutes (~480 calls/month)
- 120 minutes (~360 calls/month)
- 180 minutes (~240 calls/month)

#### API Usage Monitoring Sensor

**Modified File**: `sensor.py`

**New Sensor**: `sensor.google_maps_weather_api_usage_estimate`

**Shows:**
- Estimated monthly API calls
- Percentage of limit used
- Status (within/exceeding limit)
- Configured interval

#### Documentation

**New File**: `CONTROL_LIMITES.md`

Complete guide on API limits with examples and alerts.

---

## [1.0.0] - Initial Release

### ✨ Features

- 🌤️ Current weather conditions with automatic day/night detection
- 📅 10-day daily forecast with high/low temperatures
- 📊 11 detailed sensors: UV index, dew point, wind, precipitation, and more
- 🎛️ Configurable update interval to control API usage
- 📈 API usage monitoring to stay within free tier limits
- 🌍 Metric and Imperial units support
- 🌐 Multi-language: Spanish and English
- ⚡ Efficient API calls with robust error handling

---

**Current Version**: 1.2.0  
**Last Updated**: November 18, 2025
