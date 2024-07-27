"""Config flow for vlaams_verkeerscentrum."""

import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)

from .api import VerkeersCentrumApi
from .const import APP_NAME, CONF_TRAJECTORIES, DOMAIN
from .exceptions import InvalidCredentialsException

_LOGGER = logging.getLogger(__name__)


def get_login_data_schema():
    """Get data schema."""
    return vol.Schema(
        {
            vol.Required(CONF_EMAIL): TextSelector(
                TextSelectorConfig(type=TextSelectorType.EMAIL)
            ),
            vol.Required(CONF_PASSWORD): TextSelector(
                TextSelectorConfig(type=TextSelectorType.PASSWORD)
            ),
        }
    )


def get_trajectories_data_schema(**kwargs):
    """Get data schema."""
    trajectory_options: list[SelectOptionDict] = [
        {"label": f"{traj.description} ({traj.name})", "value": traj.id}
        for traj in kwargs.get("trajectories", [])
    ]

    return vol.Schema(
        {
            vol.Required(CONF_TRAJECTORIES, default=[]): SelectSelector(
                SelectSelectorConfig(
                    options=trajectory_options,
                    mode=SelectSelectorMode.LIST,
                    multiple=True,
                    custom_value=True,
                    translation_key="trajectories",
                )
            ),
        }
    )


class VlaamsVerkeerscentrumConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize."""
        self._client: VerkeersCentrumApi = None
        self._login_data: dict[str, str] = None

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is None:
            return self._show_user_form()
        errors = {}
        if errors:
            return self._show_user_form(errors)
        unique_id = user_input[CONF_EMAIL]
        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured()
        # Login to Verkeerscentrum
        self._client = VerkeersCentrumApi(
            user_input[CONF_EMAIL], user_input[CONF_PASSWORD]
        )
        try:
            await self._client.login()
        except InvalidCredentialsException:
            errors["base"] = "invalid_credentials"
            return self._show_user_form(errors)
        except Exception:  # noqa: BLE001 # pylint: disable=broad-except
            errors["base"] = "unknown"
            return self._show_user_form(errors)
        self._login_data = user_input
        return await self.async_step_trajectories()

    def _show_user_form(self, errors=None):
        """Show the form to the user."""
        data_schema = get_login_data_schema()
        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors or {}
        )

    async def async_step_trajectories(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is None:
            return await self._show_trajectories_form()
        data = {
            CONF_TRAJECTORIES: user_input[CONF_TRAJECTORIES],
            CONF_EMAIL: self._login_data[CONF_EMAIL],
            CONF_PASSWORD: self._login_data[CONF_PASSWORD],
        }
        await self._client.close()
        return self.async_create_entry(title=APP_NAME, data=data)

    async def _show_trajectories_form(self):
        """Show the form to the user."""
        try:
            trajectories = await self._client.get_user_trajectories()
            data_schema = get_trajectories_data_schema(trajectories=trajectories)
        except Exception as e:  # noqa: BLE001 # pylint: disable=broad-except
            _LOGGER.debug("Exception: %s", e)
            return self.async_show_form(
                step_id="trajectories", data_schema={}, errors={"base": "unknown"}
            )
        return self.async_show_form(
            step_id="trajectories", data_schema=data_schema, errors={}
        )
