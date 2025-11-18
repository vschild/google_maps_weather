"""Sensor platform for Google Maps Weather integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfLength,
    UnitOfPrecipitationDepth,
    UnitOfSpeed,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Google Maps Weather sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    
    sensors = [
        GoogleMapsWeatherSensor(
            coordinator,
            entry,
            "UV Index",
            "uv_index",
            "uvIndex",
            None,
            None,  # UV Index no usa device_class porque no tiene unidad estándar
        ),
        GoogleMapsWeatherSensor(
            coordinator,
            entry,
            "Dew Point",
            "dew_point",
            "dewPoint.degrees",
            "°C",
            SensorDeviceClass.TEMPERATURE,
        ),
        GoogleMapsWeatherSensor(
            coordinator,
            entry,
            "Heat Index",
            "heat_index",
            "heatIndex.degrees",
            "°C",
            SensorDeviceClass.TEMPERATURE,
        ),
        GoogleMapsWeatherSensor(
            coordinator,
            entry,
            "Wind Chill",
            "wind_chill",
            "windChill.degrees",
            "°C",
            SensorDeviceClass.TEMPERATURE,
        ),
        GoogleMapsWeatherSensor(
            coordinator,
            entry,
            "Wind Gust",
            "wind_gust",
            "wind.gust.value",
            "km/h",
            None,
            SensorStateClass.MEASUREMENT,
        ),
        GoogleMapsWeatherSensor(
            coordinator,
            entry,
            "Wind Direction",
            "wind_direction",
            "wind.direction.cardinal",
            None,
            None,
        ),
        GoogleMapsWeatherSensor(
            coordinator,
            entry,
            "Cloud Cover",
            "cloud_cover",
            "cloudCover",
            PERCENTAGE,
            None,
            SensorStateClass.MEASUREMENT,
        ),
        GoogleMapsWeatherSensor(
            coordinator,
            entry,
            "Thunderstorm Probability",
            "thunderstorm_probability",
            "thunderstormProbability",
            PERCENTAGE,
            None,
            SensorStateClass.MEASUREMENT,
        ),
        GoogleMapsWeatherSensor(
            coordinator,
            entry,
            "Precipitation Probability",
            "precipitation_probability",
            "precipitation.probability.percent",
            PERCENTAGE,
            None,
            SensorStateClass.MEASUREMENT,
        ),
        GoogleMapsWeatherSensor(
            coordinator,
            entry,
            "Precipitation Amount",
            "precipitation_amount",
            "precipitation.qpf.quantity",
            "mm",
            None,
            SensorStateClass.MEASUREMENT,
        ),
        APIUsageSensor(
            coordinator,
            entry,
        ),
    ]
    
    async_add_entities(sensors, True)


class GoogleMapsWeatherSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Google Maps Weather sensor."""

    def __init__(
        self,
        coordinator,
        entry: ConfigEntry,
        name: str,
        sensor_id: str,
        data_path: str,
        unit: str | None,
        device_class: SensorDeviceClass | None = None,
        state_class: SensorStateClass | None = None,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = name
        self._attr_unique_id = f"{entry.entry_id}_{sensor_id}"
        self._data_path = data_path
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        self._attr_has_entity_name = True
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Google Maps Weather",
            "manufacturer": "Google",
            "model": "Weather API",
        }

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        if not self.coordinator.data or "current" not in self.coordinator.data:
            return None
        
        # Navegar por el path de datos (ej: "wind.gust.value")
        data = self.coordinator.data["current"]
        keys = self._data_path.split(".")
        
        for key in keys:
            if isinstance(data, dict) and key in data:
                data = data[key]
            else:
                return None
        
        return data


class APIUsageSensor(CoordinatorEntity, SensorEntity):
    """Sensor to monitor API usage."""

    def __init__(
        self,
        coordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the API usage sensor."""
        super().__init__(coordinator)
        self._attr_name = "API Usage Estimate"
        self._attr_unique_id = f"{entry.entry_id}_api_usage"
        self._attr_native_unit_of_measurement = "calls/month"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:api"
        self._attr_has_entity_name = True
        self._entry = entry
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Google Maps Weather",
            "manufacturer": "Google",
            "model": "Weather API",
        }

    @property
    def native_value(self) -> int:
        """Return estimated API calls per month."""
        update_interval = self._entry.data.get(
            CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
        )
        # Calcular llamadas estimadas por mes
        # (60 minutos * 24 horas * 30 días) / intervalo
        return int((60 * 24 * 30) / update_interval)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        update_interval = self._entry.data.get(
            CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
        )
        estimated_calls = int((60 * 24 * 30) / update_interval)
        
        # Determinar estado según el límite
        if estimated_calls <= 1000:
            status = "✓ Dentro del límite gratuito"
            percentage = (estimated_calls / 1000) * 100
        else:
            status = "⚠️ Sobrepasa límite gratuito"
            percentage = 100
            
        return {
            "update_interval_minutes": update_interval,
            "update_interval_display": f"{update_interval} minutos",
            "estimated_monthly_calls": estimated_calls,
            "free_tier_limit": 1000,
            "usage_percentage": round(percentage, 1),
            "status": status,
            "calls_per_day": round(estimated_calls / 30, 1),
            "within_free_tier": estimated_calls <= 1000,
        }
