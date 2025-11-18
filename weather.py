"""Weather platform for Google Maps Weather integration."""
from __future__ import annotations

import logging
from datetime import datetime, timezone
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
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

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
        WeatherEntityFeature.FORECAST_DAILY | WeatherEntityFeature.FORECAST_HOURLY
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
        forecast = self._generate_forecast_daily()
        _LOGGER.debug(f"async_forecast_daily called, returning {len(forecast) if forecast else 0} days")
        return forecast

    async def async_forecast_hourly(self) -> list[Forecast] | None:
        """Return the hourly forecast in native units."""
        forecast = self._generate_forecast_hourly()
        _LOGGER.debug(f"async_forecast_hourly called, returning {len(forecast) if forecast else 0} hours")
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

    def _generate_forecast_daily(self) -> list[Forecast] | None:
        """Generate daily forecast data from coordinator data."""
        if not self.coordinator.data or "forecast" not in self.coordinator.data:
            _LOGGER.warning("No forecast data available in coordinator")
            return None

        forecast_list = []
        forecast_data = self.coordinator.data["forecast"].get("forecastDays", [])
        
        if not forecast_data:
            _LOGGER.warning("forecastDays is empty")
            return None
        
        # Obtener la fecha actual en la zona horaria configurada en Home Assistant
        hass_timezone = (
            dt_util.get_time_zone(self.hass.config.time_zone)
            if self.hass.config.time_zone
            else dt_util.DEFAULT_TIME_ZONE
        )
        today = dt_util.now(hass_timezone).date()
        
        _LOGGER.info(f"Processing {len(forecast_data)} days of forecast (today: {today})")
        
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
                
                # Convertir la fecha del pronóstico a la zona horaria local
                try:
                    forecast_dt = dt_util.parse_datetime(start_time)
                    if forecast_dt is None:
                        raise ValueError("parse_datetime returned None")
                    if forecast_dt.tzinfo is None:
                        forecast_dt = forecast_dt.replace(tzinfo=timezone.utc)
                    local_forecast_dt = forecast_dt.astimezone(hass_timezone)
                    forecast_date = local_forecast_dt.date()
                    if forecast_date < today:
                        _LOGGER.debug(
                            f"Day {idx}: Skipping past date {start_time} (local date {forecast_date})"
                        )
                        continue
                    datetime_str = forecast_date.isoformat()
                except (ValueError, AttributeError) as err:
                    _LOGGER.warning(
                        f"Day {idx}: Invalid date format {start_time}: {err}"
                    )
                    continue
                
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

    def _generate_forecast_hourly(self) -> list[Forecast] | None:
        """Generate hourly forecast data from coordinator data."""
        if not self.coordinator.data or "hourly" not in self.coordinator.data:
            _LOGGER.warning("No hourly forecast data available in coordinator")
            return None

        forecast_list = []
        hourly_data = self.coordinator.data["hourly"].get("forecastHours", [])
        
        if not hourly_data:
            _LOGGER.warning("forecastHours is empty")
            return None
        
        # Obtener la hora actual en UTC
        now_utc = datetime.now(timezone.utc)
        
        _LOGGER.info(f"Processing {len(hourly_data)} hours of forecast (now: {now_utc})")
        
        for idx, hour in enumerate(hourly_data):
            try:
                # Obtener temperatura
                temp_data = hour.get("temperature", {})
                temperature = temp_data.get("degrees") if isinstance(temp_data, dict) else None
                
                if temperature is None:
                    _LOGGER.warning(f"Hour {idx}: No temperature found, skipping")
                    continue
                
                # Obtener condición climática
                weather_type = hour.get("weatherCondition", {}).get("type", "CLEAR")
                is_daytime = hour.get("isDaytime", True)
                
                # Mapear condición base
                condition = CONDITION_MAP.get(weather_type, "sunny")
                
                # Si es despejado y es de noche, cambiar a clear-night
                if condition == "sunny" and not is_daytime:
                    condition = "clear-night"
                
                # Obtener precipitación
                precip_data = hour.get("precipitation", {})
                precipitation = precip_data.get("qpf", {}).get("quantity", 0) if isinstance(precip_data, dict) else 0
                precip_prob = precip_data.get("probability", {}).get("percent", 0) if isinstance(precip_data, dict) else 0
                
                # Obtener fecha y hora - usar interval startTime
                interval = hour.get("interval", {})
                start_time = interval.get("startTime")
                
                if not start_time:
                    _LOGGER.warning(f"Hour {idx}: No start time found, skipping")
                    continue
                
                # Filtrar: solo incluir horas futuras
                try:
                    # Parsear la fecha/hora ISO con timezone
                    forecast_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                    # Asegurar que tenga timezone
                    if forecast_time.tzinfo is None:
                        forecast_time = forecast_time.replace(tzinfo=timezone.utc)
                    
                    if forecast_time < now_utc:
                        _LOGGER.debug(f"Hour {idx}: Skipping past hour {start_time}")
                        continue
                except (ValueError, AttributeError) as err:
                    _LOGGER.warning(f"Hour {idx}: Invalid datetime format {start_time}: {err}")
                    continue
                
                # Crear entrada de forecast
                forecast_entry = Forecast(
                    datetime=start_time,  # Formato ISO completo con hora
                    condition=condition,
                    native_temperature=temperature,
                    native_precipitation=precipitation,
                    precipitation_probability=precip_prob,
                )
                
                forecast_list.append(forecast_entry)
                
                # Log solo para las primeras 3 horas
                if idx < 3:
                    _LOGGER.debug(
                        f"Hour {idx}: {start_time} - {condition}, "
                        f"Temp: {temperature}°C, Precip: {precip_prob}%"
                    )
                
            except Exception as err:
                _LOGGER.error(f"Error processing forecast hour {idx}: {err}", exc_info=True)
                continue

        if forecast_list:
            _LOGGER.info(f"Successfully generated hourly forecast with {len(forecast_list)} hours")
        else:
            _LOGGER.warning("No hourly forecast entries were generated")
            
        return forecast_list if forecast_list else None
