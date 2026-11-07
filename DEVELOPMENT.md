# State refresh candidate

This branch adds a shared 30-second status request fallback alongside push
updates, reports failed refreshes as unavailable, and exposes the timestamp of
the last successful refresh. Explicit HVAC mode commands no longer depend on
the local cache being correct. Responses after commands are requested through
the same refresh lock, and the periodic task is cancelled on integration unload.

This is a development candidate (0.2.13rc2). The corrected climate file was
applied over rc1 on one live Home Assistant 2026.11.0 installation on 7 November
2026; startup, three existing entities and controller readings were checked.
The complete rc2 folder was not installed in that live check. Physical command
and failure/recovery behaviour still require attended hardware validation.
The separate `airtouch2-python` branch fixes command loss after reconnection.
The manifest pins a wheel built from the patched library, using an immutable
GitHub commit URL and a SHA-256 checksum. Its version is `0.8.7.post1`.
It also replaces silent connections on the next poll after a response timeout.

Run offline tests with the library `src` directory on `PYTHONPATH`:

    python -m unittest discover -s tests -v

The protocol tests do not boot Home Assistant. The compatibility workflow also
installs Home Assistant 2026.11.0 on Python 3.14 and imports all integration
modules, including the climate and fan entities and config flow. It checks the
existing unique IDs and temperature settings without connecting to hardware.
Locally this compatibility test skips if Home Assistant is absent; CI requires
the real package and fails if it is missing. This is an import smoke test, not
a full Home Assistant startup or a physical controller test.

See `INSTALL.md` for deployment and rollback. The vendor app's own display
refresh is outside this integration.

## Startup fix in rc2

The installed system was observed running Home Assistant Core 2026.11.0. Its
climate module no longer exports `UnitOfTemperature` or `PRECISION_WHOLE`.
Those constants now come directly from `homeassistant.const`, with valid
parenthesised imports. `DeviceInfo` also comes from its defining module,
`homeassistant.helpers.device_registry`. The three deprecated climate temperature
members use the new native-temperature API available in Home Assistant 2026.11.
The reported Celsius values and existing limits/step are retained. This candidate
targets Home Assistant 2026.11.0; older versions have not been validated.
Unique IDs, config entry schema,
refresh logic, commands and the pinned AirTouch dependency are unchanged.

The previously installed file had a separate syntax error: a bare import split
after a trailing comma. That edit is absent from both existing GitHub branches.
The old tests extracted one method with AST and exercised the refresh module;
they never imported the climate class and could not detect the invalid API imports.
