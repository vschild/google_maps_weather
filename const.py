"""Constants for the Google Maps Weather integration."""

DOMAIN = "google_maps_weather"

# API endpoints
API_BASE_URL = "https://weather.googleapis.com/v1"
CURRENT_CONDITIONS_ENDPOINT = f"{API_BASE_URL}/currentConditions:lookup"
DAILY_FORECAST_ENDPOINT = f"{API_BASE_URL}/forecast/days:lookup"
HOURLY_FORECAST_ENDPOINT = f"{API_BASE_URL}/forecast/hours:lookup"

# Configuration
CONF_API_KEY = "api_key"
CONF_LATITUDE = "latitude"
CONF_LONGITUDE = "longitude"
CONF_UNITS = "units"
CONF_UPDATE_INTERVAL = "update_interval"
CONF_HOURLY_FORECAST_HOURS = "hourly_forecast_hours"

# Defaults
DEFAULT_NAME = "Google Maps Weather"
DEFAULT_UNITS = "METRIC"
DEFAULT_UPDATE_INTERVAL = 60  # 60 minutos = ~2160 llamadas/mes (3 llamadas por actualización)
DEFAULT_HOURLY_FORECAST_HOURS = 24  # 24 horas por defecto

# Update interval options (en minutos)
# Cálculo de llamadas mensuales aproximadas = 3 * (60 * 24 * 30) / intervalo
# (3+ llamadas por actualización: current + daily + ceil(hourly/24))
UPDATE_INTERVALS = {
    15: "0.25 hours (~8640 calls/month) - Under free limit",
    30: "0.5 hours (~4320 calls/month)",
    60: "1 hours (~2160 calls/month)",
    90: "1.5 hours (~1440 calls/month)",
    120: "2 hours (~1080 calls/month)",
    150: "2.5 hours (~864 calls/month)",
    180: "3 hours (~720 calls/month)",
    240: "4 hours (~540 calls/month)",
}

# Hourly forecast hours options
HOURLY_FORECAST_OPTIONS = {
    24: "24 hours (1 day)",
    48: "48 hours (2 days) - +1 API calls per update interval",
    72: "72 hours (3 days) - +2 API calls per update interval",
    96: "96 hours (4 days) - +3 API calls per update interval",
    120: "120 hours (5 days) - +4 API calls per update interval",
    168: "168 hours (7 days) - +6 API calls per update interval",
    240: "240 hours (10 days) - Maximum - +9 API calls per update interval",
}

# Mapeo de códigos de condición climática de Google a Home Assistant
# Home Assistant conditions: clear-night, cloudy, exceptional, fog, hail,
# lightning, lightning-rainy, partlycloudy, pouring, rainy, snowy,
# snowy-rainy, sunny, windy, windy-variant
# Google list: https://developers.google.com/maps/documentation/weather/reference/rest/v1/WeatherCondition
# Home Assistant List: https://www.home-assistant.io/integrations/weather/#condition-mapping
CONDITION_MAP = {
    "CLEAR": "sunny",  # Se convertirá a clear-night si es de noche
    "MOSTLY_CLEAR": "sunny",
    "PARTLY_CLOUDY": "partlycloudy",
    "MOSTLY_CLOUDY": "cloudy",
    "CLOUDY": "cloudy",
    "OVERCAST": "cloudy",
    "FOG": "fog",
    "LIGHT_FOG": "fog",
    "MIST": "fog",
    "DRIZZLE": "rainy",
    "LIGHT_RAIN": "rainy",
    "RAIN": "rainy",
    "MODERATE_RAIN": "rainy",
    "HEAVY_RAIN": "pouring",
    "FREEZING_DRIZZLE": "snowy-rainy",
    "FREEZING_RAIN": "snowy-rainy",
    "LIGHT_SNOW": "snowy",
    "SNOW": "snowy",
    "MODERATE_SNOW": "snowy",
    "HEAVY_SNOW": "snowy",
    "ICE_PELLETS": "hail",
    "THUNDERSTORM": "lightning",
    "LIGHT_THUNDERSTORM": "lightning-rainy",
    "BLIZZARD": "snowy",
    "HAIL": "hail",
    "WINDY": "windy",
    "BLOWING_SNOW":	"snowy",
    "CHANCE_OF_SHOWERS": "rainy",
    "CHANCE_OF_SNOW_SHOWERS": "snowy",
    "HAIL_SHOWERS": "hail",
    "HEAVY_RAIN_SHOWERS": "pouring",
    "HEAVY_SNOW_SHOWERS": "snowy",
    "HEAVY_SNOW_STORM": "snowy",
    "HEAVY_THUNDERSTORM": "lightning",
    "LIGHT_RAIN_SHOWERS": "rainy",
    "LIGHT_SNOW_SHOWERS": "snowy",
    "LIGHT_THUNDERSTORM_RAIN": "lightning-rainy",
    "LIGHT_TO_MODERATE_RAIN": "rainy",
    "LIGHT_TO_MODERATE_SNOW": "snowy",
    "MODERATE_TO_HEAVY_RAIN": "pouring",
    "MODERATE_TO_HEAVY_SNOW": "snowy",
    "RAIN_AND_SNOW": "snowy-rainy",
    "RAIN_PERIODICALLY_HEAVY": "pouring",
    "RAIN_SHOWERS": "rainy",
    "SCATTERED_SHOWERS": "rainy",
    "SCATTERED_SNOW_SHOWERS": "snowy",
    "SCATTERED_THUNDERSTORMS": "lightning",
    "SNOWSTORM": "snowy",
    "SNOW_PERIODICALLY_HEAVY": "snowy",
    "SNOW_SHOWERS": "snowy",
    "THUNDERSHOWER": "lightning-rainy",
    "TYPE_UNSPECIFIED": "exceptional",
    "WIND_AND_RAIN": "windy-variant",
}
