"""Weather platform for Google Maps Weather integration."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from homeassistant.components.weather import (
    Forecast,
    WeatherEntity,
    WeatherEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONDITION_MAP, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Google Maps Weather entity."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    
    async_add_entities([GoogleMapsWeatherEntity(coordinator, entry)], True)


class GoogleMapsWeatherEntity(CoordinatorEntity, WeatherEntity):
    """Representation of Google Maps Weather entity."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_native_pressure_unit = UnitOfPressure.MBAR
    _attr_native_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_native_wind_speed_unit = UnitOfSpeed.KILOMETERS_PER_HOUR
    _attr_supported_features = (
        WeatherEntityFeature.FORECAST_DAILY
    )

    def __init__(self, coordinator, entry: ConfigEntry) -> None:
        """Initialize the weather entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_weather"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Google Maps Weather",
            "manufacturer": "Google",
            "model": "Weather API",
        }

    @property
    def condition(self) -> str | None:
        """Return the current condition."""
        if not self.coordinator.data or "current" not in self.coordinator.data:
            return None
        
        current = self.coordinator.data["current"]
        weather_type = current.get("weatherCondition", {}).get("type", "CLEAR")
        is_daytime = current.get("isDaytime", True)
        
        # Mapear condición base
        condition = CONDITION_MAP.get(weather_type, "sunny")
        
        # Si es despejado y es de noche, cambiar a clear-night
        if condition == "sunny" and not is_daytime:
            condition = "clear-night"
        
        _LOGGER.debug(f"Current condition: {weather_type} -> {condition} (daytime: {is_daytime})")
        
        return condition

    @property
    def native_temperature(self) -> float | None:
        """Return the temperature."""
        if not self.coordinator.data or "current" not in self.coordinator.data:
            return None
        
        temp_data = self.coordinator.data["current"].get("temperature", {})
        return temp_data.get("degrees")

    @property
    def native_apparent_temperature(self) -> float | None:
        """Return the apparent temperature (feels like)."""
        if not self.coordinator.data or "current" not in self.coordinator.data:
            return None
        
        feels_like_data = self.coordinator.data["current"].get("feelsLikeTemperature", {})
        return feels_like_data.get("degrees")

    @property
    def humidity(self) -> float | None:
        """Return the humidity."""
        if not self.coordinator.data or "current" not in self.coordinator.data:
            return None
        
        return self.coordinator.data["current"].get("relativeHumidity")

    @property
    def native_pressure(self) -> float | None:
        """Return the pressure."""
        if not self.coordinator.data or "current" not in self.coordinator.data:
            return None
        
        pressure_data = self.coordinator.data["current"].get("airPressure", {})
        return pressure_data.get("meanSeaLevelMillibars")

    @property
    def native_wind_speed(self) -> float | None:
        """Return the wind speed."""
        if not self.coordinator.data or "current" not in self.coordinator.data:
            return None
        
        wind_data = self.coordinator.data["current"].get("wind", {})
        speed_data = wind_data.get("speed", {})
        return speed_data.get("value")

    @property
    def wind_bearing(self) -> float | None:
        """Return the wind bearing."""
        if not self.coordinator.data or "current" not in self.coordinator.data:
            return None
        
        wind_data = self.coordinator.data["current"].get("wind", {})
        direction_data = wind_data.get("direction", {})
        return direction_data.get("degrees")

    @property
    def native_visibility(self) -> float | None:
        """Return the visibility."""
        if not self.coordinator.data or "current" not in self.coordinator.data:
            return None
        
        visibility_data = self.coordinator.data["current"].get("visibility", {})
        return visibility_data.get("value")

    @property
    def uv_index(self) -> float | None:
        """Return the UV index."""
        if not self.coordinator.data or "current" not in self.coordinator.data:
            return None
        
        return self.coordinator.data["current"].get("uvIndex")

    @property
    def cloud_coverage(self) -> float | None:
        """Return the cloud coverage."""
        if not self.coordinator.data or "current" not in self.coordinator.data:
            return None
        
        return self.coordinator.data["current"].get("cloudCover")

    async def async_forecast_daily(self) -> list[Forecast] | None:
        """Return the daily forecast in native units."""
        # NO usar cache aquí - siempre generar fresco para los listeners
        forecast = self._generate_forecast()
        _LOGGER.debug(f"async_forecast_daily called, returning {len(forecast) if forecast else 0} days")
        return forecast

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        super()._handle_coordinator_update()
        # Notificar a los listeners que hay nuevo forecast disponible
        _LOGGER.debug("Coordinator updated, notifying forecast listeners")
        # Esto hace que Home Assistant llame a async_forecast_daily
        # para obtener el forecast actualizado
        self.async_write_ha_state()

    def _generate_forecast(self) -> list[Forecast] | None:
        """Generate forecast data from coordinator data."""
        if not self.coordinator.data or "forecast" not in self.coordinator.data:
            _LOGGER.warning("No forecast data available in coordinator")
            return None

        forecast_list = []
        forecast_data = self.coordinator.data["forecast"].get("forecastDays", [])
        
        if not forecast_data:
            _LOGGER.warning("forecastDays is empty")
            return None
        
        _LOGGER.info(f"Processing {len(forecast_data)} days of forecast")
        
        # Log de la estructura del primer día para debug
        if forecast_data and _LOGGER.isEnabledFor(logging.DEBUG):
            first_day = forecast_data[0]
            _LOGGER.debug(f"First day structure keys: {list(first_day.keys())}")
            if "daytimeForecast" in first_day:
                _LOGGER.debug(f"daytimeForecast keys: {list(first_day['daytimeForecast'].keys())}")
            if "nighttimeForecast" in first_day:
                _LOGGER.debug(f"nighttimeForecast keys: {list(first_day['nighttimeForecast'].keys())}")

        for idx, day in enumerate(forecast_data):
            try:
                daytime = day.get("daytimeForecast", {})
                nighttime = day.get("nighttimeForecast", {})
                
                if not daytime and not nighttime:
                    _LOGGER.warning(f"Day {idx}: No daytime or nighttime forecast")
                    continue
                
                # Obtener temperatura máxima (daytime) y mínima (nighttime)
                # Temperatura máxima - puede estar en daytime o en el día directamente
                temp_max = None
                if daytime:
                    # Primero intentar obtener del objeto temperature
                    temp_data = daytime.get("temperature", {})
                    if isinstance(temp_data, dict):
                        temp_max = temp_data.get("degrees")
                    
                    # Si no está ahí, intentar con maxTemperature
                    if temp_max is None:
                        max_temp_data = daytime.get("maxTemperature", {})
                        if isinstance(max_temp_data, dict):
                            temp_max = max_temp_data.get("degrees")
                
                # Si aún es None, intentar obtener del nivel superior del día
                if temp_max is None:
                    max_temp_data = day.get("maxTemperature", {})
                    if isinstance(max_temp_data, dict):
                        temp_max = max_temp_data.get("degrees")
                
                # Temperatura mínima - similar lógica
                temp_min = None
                if nighttime:
                    temp_data = nighttime.get("temperature", {})
                    if isinstance(temp_data, dict):
                        temp_min = temp_data.get("degrees")
                    
                    if temp_min is None:
                        min_temp_data = nighttime.get("minTemperature", {})
                        if isinstance(min_temp_data, dict):
                            temp_min = min_temp_data.get("degrees")
                
                if temp_min is None:
                    min_temp_data = day.get("minTemperature", {})
                    if isinstance(min_temp_data, dict):
                        temp_min = min_temp_data.get("degrees")
                
                # Log para debug - solo para el primer día
                if idx == 0:
                    _LOGGER.debug(f"Day {idx} temp extraction: temp_max={temp_max}, temp_min={temp_min}")
                    _LOGGER.debug(f"Day {idx} daytime.temperature: {daytime.get('temperature')}")
                    _LOGGER.debug(f"Day {idx} nighttime.temperature: {nighttime.get('temperature')}")
                
                # Si no tenemos temperatura máxima, saltar este día
                if temp_max is None:
                    _LOGGER.warning(f"Day {idx}: No maximum temperature found, skipping. Available keys in day: {list(day.keys())}")
                    if daytime:
                        _LOGGER.warning(f"Day {idx}: Available keys in daytimeForecast: {list(daytime.keys())}")
                    continue
                
                # Obtener condición climática del día
                weather_type = daytime.get("weatherCondition", {}).get("type", "CLEAR")
                condition = CONDITION_MAP.get(weather_type, "sunny")
                
                # Obtener precipitación
                precipitation = daytime.get("precipitation", {}).get("qpf", {}).get("quantity", 0)
                precip_prob = daytime.get("precipitation", {}).get("probability", {}).get("percent", 0)
                
                # Obtener fecha - usar interval startTime
                interval = day.get("interval", {})
                start_time = interval.get("startTime")
                
                if not start_time:
                    _LOGGER.warning(f"Day {idx}: No start time found, skipping")
                    continue
                
                # Extraer solo la fecha en formato ISO (YYYY-MM-DD)
                if "T" in start_time:
                    datetime_str = start_time.split("T")[0]
                else:
                    datetime_str = start_time
                
                # Crear entrada de forecast
                # IMPORTANTE: Usar native_temperature (no temperature) para HA 2024.x
                forecast_entry = Forecast(
                    datetime=datetime_str,
                    condition=condition,
                    native_temperature=temp_max,  # Temperatura máxima del día
                    native_templow=temp_min,  # Temperatura mínima del día
                    native_precipitation=precipitation,
                    precipitation_probability=precip_prob,
                )
                
                forecast_list.append(forecast_entry)
                _LOGGER.info(
                    f"Day {idx}: {datetime_str} - {condition}, "
                    f"High: {temp_max}°C, Low: {temp_min}°C, "
                    f"Precip: {precip_prob}%"
                )
                
            except Exception as err:
                _LOGGER.error(f"Error processing forecast day {idx}: {err}", exc_info=True)
                continue

        if forecast_list:
            _LOGGER.info(f"Successfully generated forecast with {len(forecast_list)} days")
        else:
            _LOGGER.warning("No forecast entries were generated")
            
        return forecast_list if forecast_list else None
