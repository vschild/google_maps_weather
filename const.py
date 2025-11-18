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

# Defaults
DEFAULT_NAME = "Google Maps Weather"
DEFAULT_UNITS = "METRIC"
DEFAULT_UPDATE_INTERVAL = 60  # 60 minutos = ~720 llamadas/mes (dentro del límite gratuito)

# Update interval options (en minutos)
# Cálculo de llamadas mensuales aproximadas = (60 * 24 * 30) / intervalo
UPDATE_INTERVALS = {
    30: "30 minutos (~1440 llamadas/mes) - Sobrepasa límite gratuito",
    45: "45 minutos (~960 llamadas/mes) - Dentro del límite",
    60: "1 hora (~720 llamadas/mes) - Recomendado",
    90: "1.5 horas (~480 llamadas/mes) - Conservador",
    120: "2 horas (~360 llamadas/mes) - Muy conservador",
    180: "3 horas (~240 llamadas/mes) - Ultra conservador",
}

# Mapeo de códigos de condición climática de Google a Home Assistant
# Home Assistant conditions: clear-night, cloudy, exceptional, fog, hail,
# lightning, lightning-rainy, partlycloudy, pouring, rainy, snowy,
# snowy-rainy, sunny, windy, windy-variant
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
}
