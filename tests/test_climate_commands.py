"""Test the actual command method in isolation (does not boot Home Assistant)."""
import ast
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock


source = Path(__file__).parents[1] / "custom_components/airtouch2plus/Airtouch2PlusClimateEntity.py"
tree = ast.parse(source.read_text())
entity = next(node for node in tree.body if isinstance(node, ast.ClassDef))
method = next(node for node in entity.body if isinstance(node, ast.AsyncFunctionDef) and node.name == "async_set_hvac_mode")
namespace = {"HVACMode": SimpleNamespace(OFF="off"), "HA_MODE_TO_AT2PLUS_SETMODE": {"cool": 4}}
exec(compile(ast.Module(body=[method], type_ignores=[]), str(source), "exec"), namespace)


class TestClimateCommands(unittest.IsolatedAsyncioTestCase):
    async def test_off_is_sent_even_if_cached_state_says_off(self):
        ac = SimpleNamespace(is_on=lambda: False, turn_off=AsyncMock())
        refresh = SimpleNamespace(refresh=AsyncMock())
        await namespace["async_set_hvac_mode"](SimpleNamespace(_ac=ac, _refresh=refresh), "off")
        ac.turn_off.assert_awaited_once()
        refresh.refresh.assert_awaited_once()

    async def test_on_is_sent_even_if_cached_state_says_on(self):
        ac = SimpleNamespace(is_on=lambda: True, turn_on=AsyncMock(), set_mode=AsyncMock())
        refresh = SimpleNamespace(refresh=AsyncMock())
        await namespace["async_set_hvac_mode"](SimpleNamespace(_ac=ac, _refresh=refresh), "cool")
        ac.turn_on.assert_awaited_once()
        ac.set_mode.assert_awaited_once_with(4)
        refresh.refresh.assert_awaited_once()
