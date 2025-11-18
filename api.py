"""API client for Google Maps Weather."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp

from .const import (
    CURRENT_CONDITIONS_ENDPOINT,
    DAILY_FORECAST_ENDPOINT,
    HOURLY_FORECAST_ENDPOINT,
    DEFAULT_UNITS,
)

_LOGGER = logging.getLogger(__name__)


class GoogleMapsWeatherAPI:
    """Class to interact with Google Maps Weather API."""

    def __init__(
        self, 
        api_key: str, 
        latitude: float, 
        longitude: float,
        units: str = DEFAULT_UNITS
    ) -> None:
        """Initialize the API client."""
        self.api_key = api_key
        self.latitude = latitude
        self.longitude = longitude
        self.units = units
        self._session = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def _make_request(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make a request to the API."""
        if params is None:
            params = {}
        
        # Agregar parámetros comunes
        params.update({
            "key": self.api_key,
            "location.latitude": self.latitude,
            "location.longitude": self.longitude,
        })
        
        # Agregar sistema de unidades si no es el endpoint de condiciones actuales
        if "currentConditions" not in endpoint:
            params["unitsSystem"] = self.units

        session = await self._get_session()
        
        try:
            async with session.get(endpoint, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                return data
        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching data from Google Maps Weather API: %s", err)
            raise
        except Exception as err:
            _LOGGER.error("Unexpected error: %s", err)
            raise

    async def get_current_conditions(self) -> dict[str, Any]:
        """Get current weather conditions."""
        params = {
            "unitsSystem": self.units
        }
        return await self._make_request(CURRENT_CONDITIONS_ENDPOINT, params)

    async def get_daily_forecast(self, days: int = 10) -> dict[str, Any]:
        """Get daily weather forecast.
        
        Args:
            days: Number of days to forecast (1-10, default: 10)
        """
        params = {
            "days": min(max(days, 1), 10)  # Limitar entre 1 y 10
        }
        return await self._make_request(DAILY_FORECAST_ENDPOINT, params)

    async def get_hourly_forecast(self, hours: int = 240) -> dict[str, Any]:
        """Get hourly weather forecast.
        
        Args:
            hours: Number of hours to forecast (1-240, default: 240)
        """
        params = {
            "hours": min(max(hours, 1), 240)  # Limitar entre 1 y 240
        }
        return await self._make_request(HOURLY_FORECAST_ENDPOINT, params)

    async def close(self) -> None:
        """Close the aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()
