# AirTouch 2+ integration

## Latest fix: 0.2.13rc2 — 7 November 2026

This candidate fixes the climate-platform startup imports and updates the
temperature properties for **Home Assistant 2026.11.0**. The earlier rc1 refresh
candidate contains outdated imports; use rc2 for this Home Assistant version.

**[Download the fixed branch ZIP](https://github.com/Chrix0689/homeassistant-airtouch2plus/archive/refs/heads/fix/ha-startup-compatibility.zip)**

[Changes](CHANGELOG.md) · [Installation and rollback](INSTALL.md) ·
[Compatibility checks](https://github.com/Chrix0689/homeassistant-airtouch2plus/actions/workflows/compatibility.yml)

`fix/ha-startup-compatibility` is the primary fix branch.
`fix/regular-state-refresh` also includes this fix. The fork's `master` branch
contains the legacy integration; its code does not include these changes.

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
2. Download the fixed branch ZIP above and extract it.
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

Use this explicit branch download for the candidate. A normal HACS/Marketplace
download may select the legacy default branch instead. An upstream update can
overwrite a manual installation. See [INSTALL.md](INSTALL.md) for dependency
requirements, functional tests and rollback.

## About this integration

_Component to integrate with Polyaire Airtouch 2+._

Utilizes [airtouch2-python](https://github.com/nathanvdh/airtouch2-python)

**This component will set up the following platforms.**

Platform | Description
-- | --
`climate` | Control temperature, mode, fan speed
`fan` | Zone power and damper percentage

## Original installation guidance

The following describes the original integration. For rc2, follow the candidate
installation instructions above so you get the corrected branch.

This integration can be manually copied into `custom_components`, or managed
through HACS/Marketplace when the intended version is available there.

See the HACS documentation on how to install it: https://www.hacs.xyz/docs/use

You will then need to add this github repo as a custom repository: https://www.hacs.xyz/docs/faq/custom_repositories

Make sure to select the 'Integration' type.

Download the added custom repository.

The airtouch2plus integration should now appear in the list of integrations with all the others.

When you add the integration, you will be prompted for the host address (IP) of your Airtouch 2+ system - enter it and that's it!
