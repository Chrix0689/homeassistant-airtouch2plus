"""The airtouch2 integration."""
from __future__ import annotations
import asyncio

from airtouch2.at2plus import At2PlusClient

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN
from .refresh import StatusRefresh

PLATFORMS: list[Platform] = [Platform.CLIMATE, Platform.FAN]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up airtouch2 from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    client = At2PlusClient(entry.data[CONF_HOST])
    try:
        async with asyncio.timeout(15):
            if not await client.connect():
                raise ConfigEntryNotReady("AirTouch controller is unreachable")
            client.run()
            await client.wait_for_ac()
        if not client.aircons_by_id:
            raise ConfigEntryNotReady("No AC units were found")
    except (OSError, TimeoutError) as err:
        await client.stop()
        raise ConfigEntryNotReady("AirTouch controller did not respond") from err
    except BaseException:
        await client.stop()
        raise
    hass.data[DOMAIN][entry.entry_id] = client
    refresh = StatusRefresh(client)
    hass.data[DOMAIN][entry.entry_id + "_refresh"] = refresh
    try:
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    except BaseException:
        hass.data[DOMAIN].pop(entry.entry_id + "_refresh", None)
        hass.data[DOMAIN].pop(entry.entry_id, None)
        await client.stop()
        raise
    refresh.start(lambda coro: hass.async_create_background_task(coro, "AirTouch status refresh"))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        client: At2PlusClient = hass.data[DOMAIN][entry.entry_id]
        await hass.data[DOMAIN].pop(entry.entry_id + "_refresh").stop()
        await client.stop()
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
