import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path("services/asset-context/asset_context.py")
spec = importlib.util.spec_from_file_location("asset_context", MODULE_PATH)
asset_context = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["asset_context"] = asset_context
spec.loader.exec_module(asset_context)


class AssetContextTests(unittest.TestCase):
    def test_risk_score_is_explainable_and_capped(self):
        asset = asset_context.normalize_asset(
            {
                "ip_addresses": ["203.0.113.10"],
                "criticality": "critical",
                "open_ports": [22, 443, 3389],
                "vulnerabilities": [
                    {"id": "CVE-1", "severity": "critical", "cvss": 9.8},
                    {"id": "CVE-2", "severity": "high", "cvss": 8.1},
                    {"id": "CVE-3", "severity": "critical", "cvss": 10.0},
                ],
                "exposure": {"internet_facing": True, "internal_only": False},
            }
        )

        self.assertEqual(asset["risk_score"], 100)
        self.assertTrue(asset["risk_breakdown"])
        self.assertTrue(
            any(item["factor"] == "exposure" for item in asset["risk_breakdown"])
        )

    def test_seed_asset_has_stable_identity(self):
        first = asset_context.normalize_asset({"ip_addresses": ["10.0.0.5"]})
        second = asset_context.normalize_asset({"ip_addresses": ["10.0.0.5"]})

        self.assertEqual(first["asset_id"], second["asset_id"])


if __name__ == "__main__":
    unittest.main()
