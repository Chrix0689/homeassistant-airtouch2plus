"""Periodic status requests supplement the controller's push notifications."""

import asyncio
import logging
from datetime import datetime, timezone

from airtouch2.protocol.at2plus.messages.AcStatus import AcStatusMessage
from airtouch2.protocol.at2plus.messages.GroupStatus import GroupStatusMessage

_LOGGER = logging.getLogger(__name__)
REFRESH_INTERVAL = 30
RESPONSE_TIMEOUT = 10


class StatusRefresh:
    """One non-overlapping poll for the whole controller, not one per entity.

    Responses still flow through the library's normal entity callbacks. A write
    to the socket alone is not considered proof of a successful refresh.
    """

    def __init__(self, client, interval=REFRESH_INTERVAL, timeout=RESPONSE_TIMEOUT):
        self.client = client
        self.interval = interval
        self.timeout = timeout
        self.available = False
        self.last_refresh = None
        self._lock = asyncio.Lock()
        self._task = None
        self._listeners = []
        self._needs_reconnect = False

    def add_listener(self, callback):
        self._listeners.append(callback)
        return lambda: self._listeners.remove(callback)

    async def refresh(self):
        """Wait for every known AC and zone to report back, including unchanged data."""
        async with self._lock:
            events = []
            unsubscribers = []
            try:
                for entity in (
                    *self.client.aircons_by_id.values(),
                    *self.client.groups_by_id.values(),
                ):
                    event = asyncio.Event()
                    events.append(event)
                    unsubscribers.append(entity.add_callback(event.set))
                async with asyncio.timeout(self.timeout):
                    if self._needs_reconnect:
                        await self.client.reconnect()
                        self._needs_reconnect = False
                    await self.client.send(AcStatusMessage([]))
                    await self.client.send(GroupStatusMessage([]))
                    await asyncio.gather(*(event.wait() for event in events))
                self.available = bool(events)
                if self.available:
                    self.last_refresh = datetime.now(timezone.utc).isoformat()
            except (TimeoutError, OSError, RuntimeError):
                if self.available:
                    _LOGGER.warning("AirTouch status refresh failed; marking entities unavailable")
                self.available = False
                self._needs_reconnect = True
            finally:
                for unsubscribe in unsubscribers:
                    unsubscribe()
            for callback in tuple(self._listeners):
                try:
                    callback()
                except Exception:
                    _LOGGER.exception("AirTouch refresh listener failed")

    def start(self, task_creator=asyncio.create_task):
        self._task = task_creator(self._run())

    async def _run(self):
        while True:
            await self.refresh()
            await asyncio.sleep(self.interval)

    async def stop(self):
        if self._task is not None:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None
