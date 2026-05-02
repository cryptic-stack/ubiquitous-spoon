import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path("services/soc-portal/soc_portal.py")
spec = importlib.util.spec_from_file_location("soc_portal", MODULE_PATH)
soc_portal = importlib.util.module_from_spec(spec)
sys.modules["soc_portal"] = soc_portal
spec.loader.exec_module(soc_portal)


class SocPortalTests(unittest.TestCase):
    def test_query_from_text_supports_field_term(self):
        self.assertEqual(
            soc_portal.query_from_text("source.ip:10.10.10.25"),
            {"term": {"source.ip": "10.10.10.25"}},
        )

    def test_format_event_builds_operator_pivots(self):
        event = soc_portal.format_event(
            {
                "_id": "event-1",
                "_index": "sentinelmesh-events-test",
                "_source": {
                    "@timestamp": "2026-05-02T18:00:00Z",
                    "event": {"module": "suricata", "dataset": "suricata.eve"},
                    "event_type": "alert",
                    "src_ip": "10.10.10.25",
                    "dest_ip": "203.0.113.25",
                    "dest_port": 443,
                    "alert": {"signature": "test alert", "severity": 2},
                },
            }
        )
        self.assertEqual(event["risk"], "high")
        self.assertEqual(event["source_ip"], "10.10.10.25")
        self.assertIn("hunt_source", event["pivots"])
        self.assertIn("pcap", event["pivots"])

    def test_format_asset_prefers_hostname(self):
        asset = soc_portal.format_asset(
            {
                "asset_id": "asset-1",
                "hostnames": ["range-dc-01"],
                "ip_addresses": ["10.10.10.25"],
                "criticality": "critical",
                "risk_score": 95,
                "vulnerabilities": [{"severity": "critical"}],
                "exposure": {"internet_facing": True},
            }
        )
        self.assertEqual(asset["name"], "range-dc-01")
        self.assertEqual(asset["risk_score"], 95)
        self.assertEqual(asset["vulnerability_count"], 1)
        self.assertTrue(asset["internet_facing"])

    def test_format_asset_calculates_display_risk_when_missing(self):
        asset = soc_portal.format_asset(
            {
                "asset_id": "asset-1",
                "hostnames": ["range-dc-01"],
                "criticality": "critical",
                "vulnerabilities": [{"severity": "critical"}],
                "exposure": {"internet_facing": True},
                "open_ports": [53, 88, 445],
            }
        )
        self.assertEqual(asset["risk_score"], 100)


if __name__ == "__main__":
    unittest.main()
