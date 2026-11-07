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
  display this README in HACS. The default branch now includes this candidate.

The malformed bare import seen in the live installation was a local edit and
was not present in either original GitHub branch. Uploading a backup of that
file restores the syntax error; use the current default-branch package instead.

## 0.2.13rc1

Chrix0689's refresh candidate adds the following over the upstream integration:

- Keep push notifications and add shared AC/zone status requests every 30 seconds
  after the previous refresh completes, with a 10-second response timeout.
- Wait for replies from every known AC and zone; mark entities unavailable on
  failed refreshes and reconnect on the next poll. Expose `last_successful_refresh`.
- Request fresh status after commands and manual updates; serialise refreshes.
- Send explicit HVAC ON/OFF requests even if the local cached power state already
  matches the requested state.
- Remove temporary callbacks and cancel the periodic task on unload.
- Bound initial connection/discovery and stop the client when setup fails.
- Pin the patched AirTouch library wheel with reconnect/command-loss fixes by
  immutable commit and SHA-256 checksum.
- Test refresh responses, timeouts, recovery, cancellation and explicit commands.
  The initial tests did not import the complete Home Assistant climate module;
  rc2 adds that coverage. These tests do not establish physical hardware behaviour.
