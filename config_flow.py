"""Config flow for Google Maps Weather integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .api import GoogleMapsWeatherAPI
from .const import (
    CONF_API_KEY,
    CONF_UNITS,
    CONF_UPDATE_INTERVAL,
    CONF_HOURLY_FORECAST_HOURS,
    DEFAULT_NAME,
    DEFAULT_UNITS,
    DEFAULT_UPDATE_INTERVAL,
    DEFAULT_HOURLY_FORECAST_HOURS,
    DOMAIN,
    UPDATE_INTERVALS,
    HOURLY_FORECAST_OPTIONS,
)

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    api = GoogleMapsWeatherAPI(
        data[CONF_API_KEY],
        data[CONF_LATITUDE],
        data[CONF_LONGITUDE],
        data.get(CONF_UNITS, DEFAULT_UNITS)
    )

    try:
        # Intentar obtener las condiciones actuales para verificar la API
        await api.get_current_conditions()
    except Exception as err:
        _LOGGER.error("Error validating API: %s", err)
        raise
    finally:
        await api.close()

    # Retornar información para crear la entrada
    return {"title": DEFAULT_NAME}


class GoogleMapsWeatherConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Google Maps Weather."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "cannot_connect"
            else:
                # Verificar si ya existe una entrada con la misma ubicación
                await self.async_set_unique_id(
                    f"{user_input[CONF_LATITUDE]}_{user_input[CONF_LONGITUDE]}"
                )
                self._abort_if_unique_id_configured()

                return self.async_create_entry(title=info["title"], data=user_input)

        # Valores por defecto usando la ubicación de Home Assistant
        default_latitude = self.hass.config.latitude
        default_longitude = self.hass.config.longitude

        data_schema = vol.Schema(
            {
                vol.Required(CONF_API_KEY): str,
                vol.Required(CONF_LATITUDE, default=default_latitude): cv.latitude,
                vol.Required(CONF_LONGITUDE, default=default_longitude): cv.longitude,
                vol.Optional(CONF_UNITS, default=DEFAULT_UNITS): vol.In(
                    ["METRIC", "IMPERIAL"]
                ),
                vol.Optional(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): vol.In(
                    list(UPDATE_INTERVALS.keys())
                ),
                vol.Optional(CONF_HOURLY_FORECAST_HOURS, default=DEFAULT_HOURLY_FORECAST_HOURS): vol.In(
                    list(HOURLY_FORECAST_OPTIONS.keys())
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "update_intervals": "\n".join(
                    [f"• {interval} min: {desc}" for interval, desc in UPDATE_INTERVALS.items()]
                ),
                "hourly_forecast_options": "\n".join(
                    [f"• {hours}h: {desc}" for hours, desc in HOURLY_FORECAST_OPTIONS.items()]
                )
            },
        )
