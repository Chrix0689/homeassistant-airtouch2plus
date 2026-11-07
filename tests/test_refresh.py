"""Exercise the refresh loop with real protocol requests and simulated replies."""
import asyncio
import importlib.util
from pathlib import Path
import unittest

from airtouch2.protocol.at2plus.messages.AcStatus import AcStatusMessage
from airtouch2.protocol.at2plus.messages.GroupStatus import GroupStatusMessage

spec = importlib.util.spec_from_file_location(
    "refresh", Path(__file__).parents[1] / "custom_components/airtouch2plus/refresh.py"
)
refresh_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(refresh_module)
StatusRefresh = refresh_module.StatusRefresh


class Entity:
    def __init__(self):
        self.callbacks = []

    def add_callback(self, callback):
        self.callbacks.append(callback)
        return lambda: self.callbacks.remove(callback)

    def report(self):
        for callback in tuple(self.callbacks):
            callback()


class Client:
    def __init__(self):
        self.aircons_by_id = {0: Entity()}
        self.groups_by_id = {0: Entity(), 1: Entity()}
        self.requests = []
        self.reply = True
        self.reconnects = 0

    async def reconnect(self):
        self.reconnects += 1

    async def send(self, message):
        self.requests.append(message)
        if self.reply:
            entities = self.aircons_by_id if isinstance(message, AcStatusMessage) else self.groups_by_id
            for entity in entities.values():
                entity.report()


class TestRefresh(unittest.IsolatedAsyncioTestCase):
    async def test_polls_ac_and_all_zones(self):
        client = Client()
        refresh = StatusRefresh(client)
        await refresh.refresh()
        self.assertTrue(refresh.available)
        self.assertIsNotNone(refresh.last_refresh)
        self.assertEqual([type(m) for m in client.requests], [AcStatusMessage, GroupStatusMessage])
        self.assertTrue(all(not e.callbacks for e in (*client.aircons_by_id.values(), *client.groups_by_id.values())))

    async def test_silent_connection_is_replaced_on_next_poll(self):
        client = Client()
        client.reply = False
        refresh = StatusRefresh(client, timeout=0.2)
        await refresh.refresh()
        client.reply = True
        await refresh.refresh()
        self.assertEqual(client.reconnects, 1)
        self.assertTrue(refresh.available)

    async def test_bad_listener_does_not_stop_updates(self):
        client = Client()
        refresh = StatusRefresh(client)
        def broken():
            raise ValueError("broken listener")
        refresh.add_listener(broken)
        reports = []
        refresh.add_listener(lambda: reports.append(refresh.last_refresh))
        await refresh.refresh()
        await refresh.refresh()
        self.assertEqual(len(reports), 2)

    async def test_stale_data_becomes_unavailable_then_recovers(self):
        client = Client()
        refresh = StatusRefresh(client, timeout=0.2)
        await refresh.refresh()
        last_success = refresh.last_refresh
        client.reply = False
        await refresh.refresh()
        self.assertFalse(refresh.available)
        self.assertEqual(refresh.last_refresh, last_success)
        client.reply = True
        await refresh.refresh()
        self.assertTrue(refresh.available)

    async def test_all_zones_must_reply(self):
        client = Client()
        client.groups_by_id[1].report = lambda: None
        refresh = StatusRefresh(client, timeout=0.2)
        await refresh.refresh()
        self.assertFalse(refresh.available)

    async def test_periodic_refresh_and_clean_stop(self):
        client = Client()
        refresh = StatusRefresh(client, interval=0.01)
        second_poll = asyncio.Event()
        refresh.add_listener(lambda: second_poll.set() if len(client.requests) >= 4 else None)
        refresh.start()
        await asyncio.wait_for(second_poll.wait(), 1)
        await refresh.stop()
        count = len(client.requests)
        await asyncio.sleep(0.02)
        self.assertEqual(len(client.requests), count)

    async def test_cancellation_cleans_response_callbacks(self):
        client = Client()
        client.reply = False
        refresh = StatusRefresh(client)
        refresh.start()
        await asyncio.sleep(0)
        await refresh.stop()
        self.assertTrue(all(not e.callbacks for e in (*client.aircons_by_id.values(), *client.groups_by_id.values())))

    async def test_transport_error_does_not_kill_future_polls(self):
        client = Client()
        original = client.send
        async def fail(message):
            raise ConnectionError("offline")
        client.send = fail
        refresh = StatusRefresh(client)
        await refresh.refresh()
        self.assertFalse(refresh.available)
        client.send = original
        await refresh.refresh()
        self.assertTrue(refresh.available)


if __name__ == "__main__":
    unittest.main()
