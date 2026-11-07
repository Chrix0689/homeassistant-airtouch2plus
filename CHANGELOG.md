# Changelog

## 0.2.13rc2 — 2026-11-07

- Fix climate-platform startup by importing temperature constants directly from
  `homeassistant.const`, using a valid parenthesised import block.
- Import `DeviceInfo` from `homeassistant.helpers.device_registry`.
- Use Home Assistant 2026.11's native temperature unit/current/target properties.
  Keep Celsius readings, the 10–35°C limits and 1°C target step.
- Preserve config entries, AC/zone unique IDs, commands, refresh behaviour and
  the pinned `airtouch2` 0.8.7.post1 wheel.
- Add real Home Assistant 2026.11.0 / Python 3.14 module-import and entity tests
  alongside the protocol tests. Checks passed for commit `c309985`.
- Confirm the climate-file upgrade over rc1 starts on one live Home Assistant
  2026.11.0 installation, preserves three entities and displays controller readings.
  The complete rc2 folder was not installed in that live check. Physical command
  and failure/recovery testing remain outstanding.
- Declare Home Assistant 2026.11.0 as the minimum version in `hacs.json` and
  display this README in HACS. Use the explicit candidate branch download.

The malformed bare import seen in the live installation was a local edit and
was not present in either original GitHub branch. Uploading a backup of that
file restores the syntax error; use the fixed branch package instead.

## 0.2.13rc1

- Add shared status requests, stale-state availability and reconnect recovery.
- Refresh after explicit commands and retain push callbacks.
- Pin the patched AirTouch library. The initial tests exercised protocol/refresh
  behaviour but did not import the complete Home Assistant climate module.
