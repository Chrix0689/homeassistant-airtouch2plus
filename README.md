# AirTouch 2+ integration

## Latest fix: 0.2.13rc2 — 7 November 2026

This candidate fixes the climate-platform startup imports and updates the
temperature properties for **Home Assistant 2026.11.0**. The earlier rc1 refresh
candidate contains outdated imports; use rc2 for this Home Assistant version.

### What this fork changes from the original integration

This version includes Chrix0689's status-refresh candidate and the subsequent
Home Assistant compatibility fixes:

- **Regular status updates:** keeps controller push notifications and adds one
  shared status request for the AC and zones every 30 seconds after the previous
  refresh finishes. It also requests status after commands and manual updates.
- **Stale-state reporting:** waits for every known AC and zone to reply. Failed
  refreshes mark the entities unavailable; the next refresh attempts to replace
  the connection. `last_successful_refresh` shows the last complete response time.
- **Explicit power/mode commands:** sends the requested ON/OFF command even when
  Home Assistant's cached state already says the unit is on or off, then requests
  fresh status. This avoids skipping a command solely because the cache is stale.
- **Patched controller library:** pins the forked AirTouch Python library
  (`0.8.7.post1`) with reconnect/command-loss fixes, using an immutable wheel URL
  and SHA-256 checksum. No manual edits to installed Python packages are needed.
- **Refresh lifecycle:** serialises refresh requests, removes temporary response
  callbacks and cancels the periodic task when the integration is unloaded.
- **Home Assistant 2026.11 compatibility:** fixes startup imports, uses the native
  temperature API and adds complete module-import tests against real Home Assistant.

Existing configuration and AC/zone unique IDs are retained. The existing Celsius
temperature range (10–35°C) and 1°C setpoint step are retained. These changes aim
to improve status freshness and recovery; they do not prove that the vendor app
or wall-controller display will always update at the same time. Read the test
scope and remaining hardware checks below before installing.

**[Download this version](https://github.com/Chrix0689/homeassistant-airtouch2plus/archive/refs/heads/master.zip)**

[Changes](CHANGELOG.md) · [Installation and rollback](INSTALL.md) ·
[Compatibility checks](https://github.com/Chrix0689/homeassistant-airtouch2plus/actions/workflows/compatibility.yml)

The default branch (`master`) contains this version. GitHub's **Code → Download
ZIP** downloads the fixed integration; no separate branch selection is needed.

### Compatibility and validation

- Minimum Home Assistant version: **2026.11.0**, for its native-temperature API.
- Automated checks on Python 3.14 with Home Assistant 2026.11.0 import every
  integration module and test identifiers, temperatures, explicit commands,
  status refresh, timeout recovery and cancellation.
- Live check on 7 November 2026: the corrected climate file was applied over
  rc1 on Home Assistant OS / Core 2026.11.0. After restarting, the existing AC
  and two zone entities were available, climate readings displayed, and the
  filtered AirTouch logs showed no issues.
- The complete rc2 folder has automated import coverage. The live check above
  replaced only the climate file; it was not a clean install of that folder.
- Physical command response, wall-controller/app synchronisation and network
  outage recovery still need attended hardware testing. Later Home Assistant
  versions have not been validated. This remains a release candidate.

### Install this candidate

1. Back up Home Assistant and the current `custom_components/airtouch2plus` folder.
2. Download the ZIP above (or use Code → Download ZIP) and extract it.
3. Copy the extracted `custom_components/airtouch2plus` folder into Home
   Assistant's configuration directory, replacing the same integration folder.
   The destination is normally `/config/custom_components/airtouch2plus` (shown
   as `/homeassistant/custom_components/airtouch2plus` by some File editors).
   Do not nest another `airtouch2plus` folder inside it.
4. Preserve the configured integration, `.storage`, entity IDs and automations.
   Existing users do **not** need to delete or re-add the integration.
5. Restart Home Assistant, then check Devices & services and the AirTouch logs.
   The full rc2 package reports `0.2.13rc2`; replacing only the climate file
   leaves the old version label because `manifest.json` is unchanged.

The default branch now includes the fix. For HACS/Marketplace, select this fork
(`Chrix0689/homeassistant-airtouch2plus`); installation through HACS/Marketplace
has not been tested. An update from the original upstream repository can overwrite
a manual fork installation. See [INSTALL.md](INSTALL.md) for dependency
requirements, functional tests and rollback.

## About this integration

_Component to integrate with Polyaire Airtouch 2+._

Uses a pinned patched wheel from [this AirTouch Python library fork](https://github.com/Chrix0689/airtouch2-python),
based on the [original library](https://github.com/nathanvdh/airtouch2-python).

**This component will set up the following platforms.**

Platform | Description
-- | --
`climate` | Control temperature, mode, fan speed
`fan` | Zone power and damper percentage

## First-time setup

After installing the folder and restarting, add **airtouch2plus** under Home
Assistant's Devices & services. Enter your AirTouch 2+ controller's local IP
address when prompted. Existing users keep their existing configured entry.
