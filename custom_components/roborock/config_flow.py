"""Config flow to configure Xiaomi Miio."""
import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_TOKEN, CONF_DEVICE_ID

from .const import DOMAIN, CONF_FLOW_TYPE, CONF_DEVICE, CONF_MODEL

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): str,
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_DEVICE_ID): str,
        vol.Required(CONF_TOKEN): vol.All(str, vol.Length(min=32, max=32)),
        vol.Optional(CONF_MODEL): str,
    }
)


class RoborockFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        return await self.async_step_device()

    async def async_step_device(self, user_input=None):
        errors = {}
        if user_input is not None:
            device_id = user_input[CONF_DEVICE_ID]
            await self.async_set_unique_id(CONF_DEVICE_ID)
            self._abort_if_unique_id_configured()

            model = ""
            if CONF_MODEL in user_input:
              model = user_input[CONF_MODEL]

            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data={
                    CONF_FLOW_TYPE: CONF_DEVICE,
                    CONF_NAME: user_input[CONF_NAME],
                    CONF_HOST: user_input[CONF_HOST],
                    CONF_DEVICE_ID: device_id,
                    CONF_TOKEN: user_input[CONF_TOKEN],
                    CONF_MODEL: model,
                },
            )

        return self.async_show_form(
            step_id="device", data_schema=CONFIG_SCHEMA, errors=errors
        )
