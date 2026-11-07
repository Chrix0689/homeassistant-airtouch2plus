# Airtouch 2+ integration

> **Latest fork candidate: 0.2.13rc2 (7 November 2026), for Home Assistant 2026.11.0.**
> The code on `master` is the legacy integration and does not include the fork's
> refresh/reconnect changes or startup fix. Before downloading, read
> **[what this fork changes and its test scope](https://github.com/Chrix0689/homeassistant-airtouch2plus/tree/fix/ha-startup-compatibility#what-this-fork-changes-from-the-original-integration)**.
> The candidate adds recurring status requests, stale-state availability,
> explicit power commands, a pinned patched controller library and current
> Home Assistant imports/temperature properties. It remains a release candidate.
> **[Download the fixed candidate ZIP](https://github.com/Chrix0689/homeassistant-airtouch2plus/archive/refs/heads/fix/ha-startup-compatibility.zip)**
> Both `fix/ha-startup-compatibility` and `fix/regular-state-refresh` include rc2.
> [Installation and rollback](https://github.com/Chrix0689/homeassistant-airtouch2plus/blob/fix/ha-startup-compatibility/INSTALL.md)

_Component to integrate with Polyaire Airtouch 2+._

Utilizes [airtouch2-python](https://github.com/nathanvdh/airtouch2-python)

**This component will set up the following platforms.**

Platform | Description
-- | --
`climate` | Control temperature, mode, fan speed

## Installation
This is integration is not available in home assistant by default, it must be either manually copied to your home assistant 'integrations' directory, or installed via HACS (recommended).

See the HACS documentation on how to install it: https://www.hacs.xyz/docs/use

You will then need to add this github repo as a custom repository: https://www.hacs.xyz/docs/faq/custom_repositories

Make sure to select the 'Integration' type.

Download the added custom repository.

The airtouch2plus integration should now appear in the list of integrations with all the others.

When you add the integration, you will be prompted for the host address (IP) of your Airtouch 2+ system - enter it and that's it!
