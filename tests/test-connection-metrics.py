import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path("services/connection-metrics/connection_metrics.py")
spec = importlib.util.spec_from_file_location("connection_metrics", MODULE_PATH)
connection_metrics = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["connection_metrics"] = connection_metrics
spec.loader.exec_module(connection_metrics)


class ConnectionMetricsTests(unittest.TestCase):
    def test_metrics_include_required_series(self):
        assets = [
            {
                "asset_id": "asset-1",
                "hostnames": ["range-dc-01"],
                "criticality": "critical",
                "risk_score": 65,
                "vulnerabilities": [{"severity": "critical"}],
            }
        ]
        connections = [
            {
                "src_asset": "range-dc-01",
                "dst_asset": "range-files-01",
                "dst_ip": "192.168.56.20",
                "dst_port": "445",
                "protocol": "tcp",
                "count": 3,
                "weight": 3,
            }
        ]

        metrics = connection_metrics.build_metrics(assets, connections)

        self.assertIn("sentinelmesh_connection_observed_total", metrics)
        self.assertIn("sentinelmesh_asset_risk_score", metrics)
        self.assertIn("sentinelmesh_asset_vulnerability_count", metrics)
        self.assertIn("sentinelmesh_relationship_weight", metrics)

    def test_graph_returns_nodes_and_edges(self):
        graph = connection_metrics.build_graph(
            [{"hostnames": ["range-dc-01"], "risk_score": 65, "criticality": "critical"}],
            [{"src_asset": "range-dc-01", "dst_asset": "range-files-01", "dst_port": "445"}],
        )

        self.assertEqual(len(graph["edges"]), 1)
        self.assertTrue(any(node["id"] == "range-dc-01" for node in graph["nodes"]))


if __name__ == "__main__":
    unittest.main()
