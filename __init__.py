"""The Google Maps Weather integration."""
from __future__ import annotations

import asyncio
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_UPDATE_INTERVAL,
    CONF_HOURLY_FORECAST_HOURS,
    DEFAULT_UPDATE_INTERVAL,
    DEFAULT_HOURLY_FORECAST_HOURS,
    DOMAIN,
)
from .api import GoogleMapsWeatherAPI

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.WEATHER, Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Google Maps Weather from a config entry."""
    api_key = entry.data["api_key"]
    latitude = entry.data["latitude"]
    longitude = entry.data["longitude"]
    update_interval = entry.data.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
    hourly_forecast_hours = entry.data.get(CONF_HOURLY_FORECAST_HOURS, DEFAULT_HOURLY_FORECAST_HOURS)
    
    api = GoogleMapsWeatherAPI(api_key, latitude, longitude)
    
    # Crear coordinador para gestionar las actualizaciones
    async def async_update_data():
        """Fetch data from API."""
        try:
            # Ejecutar las 3 llamadas en paralelo para optimizar tiempo de respuesta
            current, forecast_daily, forecast_hourly = await asyncio.gather(
                api.get_current_conditions(),
                api.get_daily_forecast(),
                api.get_hourly_forecast(hours=hourly_forecast_hours)
            )
            
            _LOGGER.debug(
                "Datos obtenidos: condiciones actuales, pronóstico diario y horario (%s horas)",
                hourly_forecast_hours
            )
            
            return {
                "current": current,
                "forecast": forecast_daily,
                "hourly": forecast_hourly
            }
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
    
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(minutes=update_interval),
    )
    
    # Obtener los datos iniciales
    await coordinator.async_config_entry_first_refresh()
    
    # Guardar el coordinador en hass.data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "api": api,
    }
    
    # Configurar las plataformas
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Log del intervalo configurado (ahora con 3 llamadas por actualización)
    monthly_calls = int(3 * (60 * 24 * 30) / update_interval)
    _LOGGER.info(
        "Google Maps Weather configurado: %s minutos de actualización, "
        "%s horas de pronóstico horario (~%s llamadas/mes con 3 endpoints)",
        update_interval,
        hourly_forecast_hours,
        monthly_calls
    )
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok
