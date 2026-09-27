# AirTouch 2+ synchronisation candidate

Version 0.2.13rc1 adds shared status requests every 30 seconds after the previous
request completes, keeps push updates, and refreshes after explicit commands.
Failed replies mark entities unavailable; a later poll replaces the connection.
`last_successful_refresh` reports when all known ACs and zones last replied.
It is a receipt timestamp, not proof that every display has the same snapshot.

The Python dependency is pinned to a published 0.8.7.post1 wheel by immutable
commit and SHA-256. No manual edits to installed Python packages are needed.
Offline regression and protocol tests pass; full HA and hardware validation
remain required. Treat this as a release candidate.

## Install during an attended maintenance window

1. Create a Home Assistant backup and download it off the HA machine. Keep a
   separate copy of the existing `custom_components/airtouch2plus` directory.
2. Extract the candidate's `custom_components/airtouch2plus` folder and replace
   only that same folder inside HA's configuration directory. Do not delete the
   configured integration or alter `.storage`, entity IDs, or automations.
3. Restart Home Assistant. It needs access to raw.githubusercontent.com to
   install the pinned dependency. Check the logs for successful setup.
4. With someone present, change a zone at the wall controller and in the app.
   Check HA converges within roughly 30 seconds plus response time. Try a single
   explicit ON/OFF and temperature command from HA after an idle period.
5. Test temporary controller network loss only when the household agrees:
   verify HA becomes unavailable and automatically recovers once connectivity
   returns. Compare the last-successful-refresh timestamp.

Do not install the fork's unchanged master branch. Use the published candidate
archive or `fix/regular-state-refresh`. HACS management of a fork with the same
domain needs care: an upstream HACS update can overwrite a manual installation.
Do not enable automatic updates for this custom component during validation.

## Rollback

Restore the original component directory (including its original manifest
requiring airtouch2==0.8.7) and restart HA. The original manifest requests the
original library again. If that does not recover the installation, restore
the saved HA backup. Keep configuration entries and entity IDs throughout.
