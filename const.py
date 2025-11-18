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
DEFAULT_UPDATE_INTERVAL = 120  # 120 minutos = ~720 llamadas/mes (3 llamadas por actualización)
DEFAULT_HOURLY_FORECAST_HOURS = 48  # 48 horas por defecto

# Update interval options (en minutos)
# Cálculo de llamadas mensuales aproximadas = 3 * (60 * 24 * 30) / intervalo
# (3 llamadas por actualización: current + daily + hourly)
UPDATE_INTERVALS = {
    90: "1.5 horas (~960 llamadas/mes) - Dentro del límite",
    120: "2 horas (~720 llamadas/mes) - Recomendado",
    150: "2.5 horas (~576 llamadas/mes) - Conservador",
    180: "3 horas (~480 llamadas/mes) - Muy conservador",
    240: "4 horas (~360 llamadas/mes) - Ultra conservador",
}

# Hourly forecast hours options
HOURLY_FORECAST_OPTIONS = {
    24: "24 horas (1 día)",
    48: "48 horas (2 días) - Recomendado",
    72: "72 horas (3 días)",
    96: "96 horas (4 días)",
    120: "120 horas (5 días)",
    168: "168 horas (7 días)",
    240: "240 horas (10 días) - Máximo",
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
