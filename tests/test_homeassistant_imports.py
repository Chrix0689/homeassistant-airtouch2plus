"""Import whole modules against real Home Assistant APIs, without a controller.

The offline protocol tests deliberately do not require Home Assistant. CI sets
REQUIRE_HOMEASSISTANT=1 so a missing runtime fails instead of skipping this test.
"""
import importlib
import importlib.util
import os
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).parents[1]))
HAS_HA = importlib.util.find_spec("homeassistant") is not None
if not HAS_HA and os.environ.get("REQUIRE_HOMEASSISTANT") == "1":
    raise ImportError("The compatibility job requires the real Home Assistant package")


@unittest.skipUnless(HAS_HA, "Run the compatibility job with Home Assistant installed")
class TestHomeAssistantImports(unittest.TestCase):
    def test_all_integration_modules_import(self):
        for module in (
            "", ".config_flow", ".climate", ".fan", ".refresh",
            ".Airtouch2PlusClimateEntity", ".Airtouch2PlusGroupEntity",
        ):
            with self.subTest(module=module):
                importlib.import_module("custom_components.airtouch2plus" + module)

    def test_existing_entity_identifiers_and_temperature_settings(self):
        from types import SimpleNamespace
        from homeassistant.const import UnitOfTemperature
        from custom_components.airtouch2plus.Airtouch2PlusClimateEntity import (
            Airtouch2PlusClimateEntity,
        )
        from custom_components.airtouch2plus.Airtouch2PlusGroupEntity import (
            AirTouch2PlusGroupEntity,
        )

        ac = SimpleNamespace(status=SimpleNamespace(id=0), ability=None)
        refresh = SimpleNamespace(available=True)
        climate = Airtouch2PlusClimateEntity(ac, refresh)
        group = AirTouch2PlusGroupEntity(
            SimpleNamespace(status=SimpleNamespace(id=1), name="Zone"), refresh
        )
        self.assertEqual(climate.unique_id, "at2plus_ac_0")
        self.assertEqual(group.unique_id, "at2plus_group_1")
        self.assertEqual(climate.device_info["identifiers"], {("airtouch2plus", "at2plus_ac_0")})
        self.assertEqual(climate.temperature_unit, UnitOfTemperature.CELSIUS)
        self.assertEqual((climate.min_temp, climate.max_temp), (10.0, 35.0))
        self.assertEqual(climate.target_temperature_step, 1.0)
