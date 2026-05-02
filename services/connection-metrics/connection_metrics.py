#!/usr/bin/env python3
"""SentinelMesh connection metrics service.

MVP behavior:
- Expose Prometheus metrics for seeded asset relationships.
- Expose a JSON node/edge graph for Grafana relationship panels.

Future behavior:
- Consume Zeek/OpenSearch connection events.
- Emit relationship metrics from live network observations.
"""

from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


DEFAULT_CONNECTIONS = [
    {
        "src_asset": "range-dc-01",
        "dst_asset": "internet-vpn-peer",
        "dst_ip": "203.0.113.25",
        "dst_port": "443",
        "protocol": "tcp",
        "count": 12,
        "weight": 12,
    },
    {
        "src_asset": "range-dc-01",
        "dst_asset": "range-files-01",
        "dst_ip": "192.168.56.20",
        "dst_port": "445",
        "protocol": "tcp",
        "count": 7,
        "weight": 7,
    },
]


def load_json_array(path: Path | None, default: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if path is None or not path.exists():
        return default

    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, list):
        raise ValueError(f"Expected JSON array: {path}")

    return data


def load_assets(path: Path | None) -> list[dict[str, Any]]:
    return load_json_array(path, [])


def load_connections(path: Path | None) -> list[dict[str, Any]]:
    return load_json_array(path, DEFAULT_CONNECTIONS)


def label_value(value: Any) -> str:
    return str(value).replace("\\", "\\\\").replace('"', '\\"')


def metric_line(name: str, labels: dict[str, Any], value: Any) -> str:
    label_text = ",".join(f'{key}="{label_value(val)}"' for key, val in labels.items())
    return f"{name}{{{label_text}}} {value}"


def asset_hostname(asset: dict[str, Any]) -> str:
    hostnames = asset.get("hostnames") or []
    if hostnames:
        return str(hostnames[0])
    if asset.get("fqdn"):
        return str(asset["fqdn"])
    if asset.get("ip_addresses"):
        return str(asset["ip_addresses"][0])
    return str(asset.get("asset_id", "unknown"))


def vulnerability_counts(asset: dict[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for vulnerability in asset.get("vulnerabilities", []):
        severity = str(vulnerability.get("severity", "unknown")).lower()
        counts[severity] = counts.get(severity, 0) + 1
    return counts


def build_metrics(assets: list[dict[str, Any]], connections: list[dict[str, Any]]) -> str:
    lines = [
        "# HELP sentinelmesh_connection_observed_total Observed SentinelMesh asset connections.",
        "# TYPE sentinelmesh_connection_observed_total counter",
    ]

    for connection in connections:
        labels = {
            "src_asset": connection.get("src_asset", "unknown"),
            "dst_asset": connection.get("dst_asset", "unknown"),
            "dst_ip": connection.get("dst_ip", "0.0.0.0"),
            "dst_port": connection.get("dst_port", "0"),
            "protocol": connection.get("protocol", "unknown"),
        }
        lines.append(
            metric_line(
                "sentinelmesh_connection_observed_total",
                labels,
                connection.get("count", 1),
            )
        )

    lines.extend(
        [
            "# HELP sentinelmesh_relationship_weight Weighted SentinelMesh asset relationship strength.",
            "# TYPE sentinelmesh_relationship_weight gauge",
        ]
    )
    for connection in connections:
        labels = {
            "src_asset": connection.get("src_asset", "unknown"),
            "dst_asset": connection.get("dst_asset", "unknown"),
            "protocol": connection.get("protocol", "unknown"),
        }
        lines.append(
            metric_line(
                "sentinelmesh_relationship_weight",
                labels,
                connection.get("weight", connection.get("count", 1)),
            )
        )

    lines.extend(
        [
            "# HELP sentinelmesh_asset_risk_score SentinelMesh asset risk score.",
            "# TYPE sentinelmesh_asset_risk_score gauge",
        ]
    )
    for asset in assets:
        labels = {
            "asset_id": asset.get("asset_id", asset_hostname(asset)),
            "hostname": asset_hostname(asset),
            "criticality": asset.get("criticality", "unknown"),
        }
        lines.append(metric_line("sentinelmesh_asset_risk_score", labels, asset.get("risk_score", 0)))

    lines.extend(
        [
            "# HELP sentinelmesh_asset_vulnerability_count SentinelMesh asset vulnerabilities by severity.",
            "# TYPE sentinelmesh_asset_vulnerability_count gauge",
        ]
    )
    for asset in assets:
        for severity, count in vulnerability_counts(asset).items():
            labels = {
                "asset_id": asset.get("asset_id", asset_hostname(asset)),
                "hostname": asset_hostname(asset),
                "severity": severity,
            }
            lines.append(metric_line("sentinelmesh_asset_vulnerability_count", labels, count))

    return "\n".join(lines) + "\n"


def build_graph(assets: list[dict[str, Any]], connections: list[dict[str, Any]]) -> dict[str, Any]:
    nodes: dict[str, dict[str, Any]] = {}

    for asset in assets:
        name = asset_hostname(asset)
        nodes[name] = {
            "id": name,
            "title": name,
            "risk_score": asset.get("risk_score", 0),
            "criticality": asset.get("criticality", "unknown"),
        }

    for connection in connections:
        src = str(connection.get("src_asset", "unknown"))
        dst = str(connection.get("dst_asset", connection.get("dst_ip", "unknown")))
        nodes.setdefault(src, {"id": src, "title": src, "risk_score": 0, "criticality": "unknown"})
        nodes.setdefault(dst, {"id": dst, "title": dst, "risk_score": 0, "criticality": "unknown"})

    edges = [
        {
            "id": f"{connection.get('src_asset', 'unknown')}->{connection.get('dst_asset', connection.get('dst_ip', 'unknown'))}:{connection.get('dst_port', '0')}",
            "source": connection.get("src_asset", "unknown"),
            "target": connection.get("dst_asset", connection.get("dst_ip", "unknown")),
            "protocol": connection.get("protocol", "unknown"),
            "dst_ip": connection.get("dst_ip", ""),
            "dst_port": connection.get("dst_port", ""),
            "weight": connection.get("weight", connection.get("count", 1)),
        }
        for connection in connections
    ]

    return {"nodes": list(nodes.values()), "edges": edges}


class MetricsHandler(BaseHTTPRequestHandler):
    assets: list[dict[str, Any]] = []
    connections: list[dict[str, Any]] = []

    def do_GET(self) -> None:
        if self.path == "/metrics":
            body = build_metrics(self.assets, self.connections).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; version=0.0.4")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if self.path == "/graph/assets":
            body = json.dumps(build_graph(self.assets, self.connections)).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if self.path == "/health":
            body = b'{"status":"ok"}\n'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, format: str, *args: Any) -> None:
        return


def main() -> None:
    host = os.getenv("SENTINELMESH_CONNECTION_METRICS_HOST", "0.0.0.0")
    port = int(os.getenv("SENTINELMESH_CONNECTION_METRICS_PORT", "9105"))
    asset_path = os.getenv("SENTINELMESH_ASSET_SEED_PATH")
    connection_path = os.getenv("SENTINELMESH_CONNECTION_SEED_PATH")

    MetricsHandler.assets = load_assets(Path(asset_path) if asset_path else None)
    MetricsHandler.connections = load_connections(Path(connection_path) if connection_path else None)

    server = ThreadingHTTPServer((host, port), MetricsHandler)
    print(f"connection-metrics listening on {host}:{port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()

