# State refresh candidate

This branch adds a shared 30-second status request fallback alongside push
updates, reports failed refreshes as unavailable, and exposes the timestamp of
the last successful refresh. Explicit HVAC mode commands no longer depend on
the local cache being correct. Responses after commands are requested through
the same refresh lock, and the periodic task is cancelled on integration unload.

This is a development candidate (0.2.13rc1). It has not
been run in a complete Home Assistant runtime or against physical hardware.
The separate `airtouch2-python` branch fixes command loss after reconnection.
The manifest pins a wheel built from the patched library, using an immutable
GitHub commit URL and a SHA-256 checksum. Its version is `0.8.7.post1`.
It also replaces silent connections on the next poll after a response timeout.

Run offline tests with the library `src` directory on `PYTHONPATH`:

    python -m unittest discover -s tests -v

The tests do not import or boot Home Assistant. See `INSTALL.md` for deployment
and rollback. The vendor app's own display refresh is outside this integration.
