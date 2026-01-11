import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import aiohttp_client
import aiohttp
import xml.etree.ElementTree as ET

from .const import (
    DOMAIN, CONF_HOST, CONF_NAME, CONF_LOCALE, CONF_EMPTY_SLOT_TEXT, CONF_INPUT_SOURCES,
    DEFAULT_NAME, DEFAULT_LOCALE, DEFAULT_EMPTY_SLOT_TEXT, DEFAULT_INPUT_SOURCES,
    LOCALIZED_STRINGS
)

DEFAULT_USERNAME = 'su3g4go6sk7'
DEFAULT_PASSWORD = 'ji39454xu/^'

class AirMusicConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            name = user_input.get(CONF_NAME, DEFAULT_NAME)
            locale = user_input.get(CONF_LOCALE, DEFAULT_LOCALE)
            empty_slot_text = user_input.get(CONF_EMPTY_SLOT_TEXT, LOCALIZED_STRINGS.get(locale, {}).get("empty_slot", DEFAULT_EMPTY_SLOT_TEXT))
            
            # Handle input_sources: convert from comma-separated string to list if needed
            input_sources_raw = user_input.get(CONF_INPUT_SOURCES, ", ".join(LOCALIZED_STRINGS.get(locale, {}).get("input_sources", DEFAULT_INPUT_SOURCES)))
            if isinstance(input_sources_raw, str):
                input_sources = [s.strip() for s in input_sources_raw.split(",")]
            else:
                input_sources = input_sources_raw

            # Validate the connection to the host with authentication
            session = aiohttp_client.async_get_clientsession(self.hass)
            url = f"http://{host}/playinfo"
            try:
                async with session.get(url, auth=aiohttp.BasicAuth(DEFAULT_USERNAME, DEFAULT_PASSWORD)) as response:
                    if response.status == 200:
                        content = await response.text()
                        root = ET.fromstring(content)
                        rt_element = root.find('rt')
                        if rt_element is not None and rt_element.text == 'INVALID_CMD':
                            # Initialize the device
                            init_url = f"http://{host}/init?language=en"
                            async with session.get(init_url, auth=aiohttp.BasicAuth(DEFAULT_USERNAME, DEFAULT_PASSWORD)) as init_response:
                                if init_response.status != 200:
                                    errors["base"] = "init_failed"
                                    return self.async_show_form(
                                        step_id="user", data_schema=self.data_schema, errors=errors
                                    )
                        # Proceed with the configuration
                        return self.async_create_entry(title=name, data={
                            CONF_HOST: host,
                            CONF_NAME: name,
                            CONF_LOCALE: locale,
                            CONF_EMPTY_SLOT_TEXT: empty_slot_text,
                            CONF_INPUT_SOURCES: input_sources
                        })
                    else:
                        errors["base"] = "cannot_connect"
            except aiohttp.ClientError:
                errors["base"] = "cannot_connect"
            except ET.ParseError:
                errors["base"] = "invalid_response"
            except Exception:
                errors["base"] = "unknown"

        self.data_schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
            vol.Optional(CONF_LOCALE, default=DEFAULT_LOCALE): vol.In(list(LOCALIZED_STRINGS.keys())),
            vol.Optional(CONF_EMPTY_SLOT_TEXT): str,
            vol.Optional(CONF_INPUT_SOURCES): str,
        })

        return self.async_show_form(
            step_id="user", data_schema=self.data_schema, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return AirMusicOptionsFlow(config_entry)


class AirMusicOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            name = user_input.get(CONF_NAME, DEFAULT_NAME)
            locale = user_input.get(CONF_LOCALE, self.config_entry.data.get(CONF_LOCALE, DEFAULT_LOCALE))
            empty_slot_text = user_input.get(CONF_EMPTY_SLOT_TEXT, self.config_entry.data.get(CONF_EMPTY_SLOT_TEXT, LOCALIZED_STRINGS.get(locale, {}).get("empty_slot", DEFAULT_EMPTY_SLOT_TEXT)))
            
            # Handle input_sources: convert from comma-separated string to list if needed
            input_sources_raw = user_input.get(CONF_INPUT_SOURCES, ", ".join(self.config_entry.data.get(CONF_INPUT_SOURCES, LOCALIZED_STRINGS.get(locale, {}).get("input_sources", DEFAULT_INPUT_SOURCES))))
            if isinstance(input_sources_raw, str):
                input_sources = [s.strip() for s in input_sources_raw.split(",")]
            else:
                input_sources = input_sources_raw

            # Validate the connection to the host with authentication
            session = aiohttp_client.async_get_clientsession(self.hass)
            url = f"http://{host}/playinfo"
            try:
                async with session.get(url, auth=aiohttp.BasicAuth(DEFAULT_USERNAME, DEFAULT_PASSWORD)) as response:
                    if response.status == 200:
                        content = await response.text()
                        root = ET.fromstring(content)
                        rt_element = root.find('rt')
                        if rt_element is not None and rt_element.text == 'INVALID_CMD':
                            # Initialize the device
                            init_url = f"http://{host}/init?language=en"
                            async with session.get(init_url, auth=aiohttp.BasicAuth(DEFAULT_USERNAME, DEFAULT_PASSWORD)) as init_response:
                                if init_response.status != 200:
                                    errors["base"] = "init_failed"
                                    return self.async_show_form(
                                        step_id="user", data_schema=self.data_schema, errors=errors
                                    )
                        # Proceed with updating the configuration
                        self.hass.config_entries.async_update_entry(
                            self.config_entry, data={
                                CONF_HOST: host,
                                CONF_NAME: name,
                                CONF_LOCALE: locale,
                                CONF_EMPTY_SLOT_TEXT: empty_slot_text,
                                CONF_INPUT_SOURCES: input_sources
                            }
                        )
                        return self.async_create_entry(title="", data={})
                    else:
                        errors["base"] = "cannot_connect"
            except aiohttp.ClientError:
                errors["base"] = "cannot_connect"
            except ET.ParseError:
                errors["base"] = "invalid_response"
            except Exception:
                errors["base"] = "unknown"

        # Convert input_sources list to comma-separated string for display
        input_sources_str = ", ".join(self.config_entry.data.get(CONF_INPUT_SOURCES, DEFAULT_INPUT_SOURCES))

        self.data_schema = vol.Schema({
            vol.Required(CONF_HOST, default=self.config_entry.data.get(CONF_HOST)): str,
            vol.Optional(CONF_NAME, default=self.config_entry.data.get(CONF_NAME, DEFAULT_NAME)): str,
            vol.Optional(CONF_LOCALE, default=self.config_entry.data.get(CONF_LOCALE, DEFAULT_LOCALE)): vol.In(list(LOCALIZED_STRINGS.keys())),
            vol.Optional(CONF_EMPTY_SLOT_TEXT, default=self.config_entry.data.get(CONF_EMPTY_SLOT_TEXT, DEFAULT_EMPTY_SLOT_TEXT)): str,
            vol.Optional(CONF_INPUT_SOURCES, default=input_sources_str): str,
        })

        return self.async_show_form(
            step_id="user", data_schema=self.data_schema, errors=errors
        )

