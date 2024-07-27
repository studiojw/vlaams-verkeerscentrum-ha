"""Sensor platform for Vlaams Verkeerscentrum."""

import logging

from homeassistant.components.persistent_notification import (
    create as create_notification,
)
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import VerkeersCentrumApi
from .const import APP_NAME, CONF_APP_NAME, CONF_TRAJECTORIES
from .exceptions import InvalidCredentialsException

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up entry."""
    app_config = {
        CONF_APP_NAME: APP_NAME,
    }

    config = {**app_config, **config_entry.data}

    api = VerkeersCentrumApi(config[CONF_EMAIL], config[CONF_PASSWORD])
    coordinator = VerkeersCentrumDataUpdateCoordinator(
        hass, api, config[CONF_TRAJECTORIES]
    )
    await coordinator.async_config_entry_first_refresh()

    sensors = [
        VerkeerscentrumSensor(coordinator, trajectory)
        for trajectory in coordinator.data.values()
    ]

    async_add_entities(sensors)


class VerkeersCentrumDataUpdateCoordinator(DataUpdateCoordinator):
    """Gather data."""

    def __init__(self, hass: HomeAssistant, api, trajectories) -> None:
        """Initialize."""
        self.api: VerkeersCentrumApi = api
        self.trajectories = trajectories
        super().__init__(hass, _LOGGER, name=APP_NAME, always_update=False)

    async def _async_update_data(self):
        try:
            data = {}
            for trajectory_id in self.trajectories:
                trajectory = await self.api.get_user_trajectory(trajectory_id)
                if trajectory:
                    data[trajectory_id] = trajectory
        except InvalidCredentialsException:
            _LOGGER.error("Invalid credentials")
            create_notification(
                hass=self.hass,
                title=f"{APP_NAME} - Invalid credentials",
                message="Please check your credentials and try again.",
                notification_id="vlaams_verkeerscentrum_invalid_credentials",
            )
        except Exception as err:  # noqa: BLE001
            raise UpdateFailed(f"Error fetching data: {err}")  # noqa: B904
        else:
            return data


class VerkeerscentrumSensor(SensorEntity):
    """Sensor for Vlaams Verkeerscentrum."""

    def __init__(self, coordinator, trajectory: dict) -> None:
        """Initialize."""
        self.coordinator = coordinator
        self.trajectory = trajectory

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{APP_NAME} {self.trajectory['description']}"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return f"{APP_NAME}_{self.trajectory['id']}"

    @property
    def device_class(self):
        """Return the device class."""
        return SensorDeviceClass.DURATION

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement."""
        return "min"

    @property
    def state(self):
        """Return the state of the sensor."""
        trajectory_id = self.trajectory["id"]
        trajectory_data = self.coordinator.data.get(trajectory_id)
        if trajectory_data is None:
            return None
        actual_travel_time = trajectory_data.get("actual_travel_time")
        if actual_travel_time is None:
            return None
        return actual_travel_time

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "trajectory_id": self.trajectory.get("id"),
            "description": self.trajectory.get("description"),
            "name": self.trajectory.get("name"),
            "delay": self.trajectory.get("delay"),
        }

    @property
    def available(self):
        """Return the availability of the sensor."""
        return self.coordinator.last_update_success

    async def async_update(self):
        """Update the sensor."""
        await self.coordinator.async_request_refresh()
