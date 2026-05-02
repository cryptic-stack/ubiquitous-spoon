"""SentinelMesh SOC portal service.

This is an MVP operator API for the static SOC interface. It mirrors the
Security Onion analyst flow at a small scale: overview, alerts, hunt, assets,
case placeholders, detections, PCAP pivots, and external dashboard links.

Future versions should add authentication, persistent analyst state, and a
proper application framework. The current service intentionally uses only the
Python standard library so it can run in a slim container during early builds.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


STATIC_DIR = Path(os.getenv("SENTINELMESH_SOC_STATIC_DIR", "/portal"))
OPENSEARCH_URL = os.getenv("SENTINELMESH_OPENSEARCH_URL", "http://opensearch:9200").rstrip("/")
EVENT_INDEX = os.getenv("SENTINELMESH_EVENT_INDEX_PATTERN", "sentinelmesh-events-*")
ASSET_SEED_PATH = Path(os.getenv("SENTINELMESH_ASSET_SEED_PATH", "/seeds/sample-assets.json"))
REQUEST_TIMEOUT = float(os.getenv("SENTINELMESH_SOC_REQUEST_TIMEOUT", "3"))


def load_seed_assets(path: Path = ASSET_SEED_PATH) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        return []
    return [asset for asset in data if isinstance(asset, dict)]


def asset_name(asset: dict[str, Any]) -> str:
    hostnames = asset.get("hostnames") or []
    if hostnames:
        return str(hostnames[0])
    if asset.get("fqdn"):
        return str(asset["fqdn"])
    ips = asset.get("ip_addresses") or []
    if ips:
        return str(ips[0])
    return str(asset.get("asset_id", "unknown"))


def opensearch_request(method: str, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
    url = f"{OPENSEARCH_URL}{path}"
    data = None
    headers = {"Content-Type": "application/json"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
        return json.loads(response.read().decode("utf-8"))


def count_events(query: dict[str, Any] | None = None) -> int:
    body = {"query": query or {"match_all": {}}}
    response = opensearch_request("POST", f"/{EVENT_INDEX}/_count", body)
    return int(response.get("count", 0))


def search_events(query: dict[str, Any], size: int = 25) -> list[dict[str, Any]]:
    body = {
        "size": size,
        "query": query,
        "sort": [{"@timestamp": {"order": "desc", "unmapped_type": "date"}}],
    }
    response = opensearch_request("POST", f"/{EVENT_INDEX}/_search", body)
    hits = response.get("hits", {}).get("hits", [])
    return [format_event(hit) for hit in hits]


def terms_aggregation(field: str, size: int = 10) -> list[dict[str, Any]]:
    body = {
        "size": 0,
        "aggs": {
            "values": {
                "terms": {
                    "field": field,
                    "size": size,
                    "missing": "unknown",
                }
            }
        },
    }
    response = opensearch_request("POST", f"/{EVENT_INDEX}/_search", body)
    buckets = response.get("aggregations", {}).get("values", {}).get("buckets", [])
    return [{"key": bucket.get("key"), "count": bucket.get("doc_count", 0)} for bucket in buckets]


def format_event(hit: dict[str, Any]) -> dict[str, Any]:
    source = hit.get("_source", {})
    event = source.get("event", {}) if isinstance(source.get("event"), dict) else {}
    alert = source.get("alert", {}) if isinstance(source.get("alert"), dict) else {}
    return {
        "id": hit.get("_id"),
        "index": hit.get("_index"),
        "time": source.get("@timestamp") or source.get("timestamp") or source.get("ts") or "",
        "module": event.get("module") or source.get("event_type") or "unknown",
        "dataset": event.get("dataset") or "unknown",
        "event_type": source.get("event_type") or alert.get("category") or "event",
        "source_ip": nested_get(source, ["source", "ip"]) or source.get("src_ip") or source.get("id.orig_h") or "",
        "destination_ip": nested_get(source, ["destination", "ip"]) or source.get("dest_ip") or source.get("id.resp_h") or "",
        "destination_port": source.get("dest_port") or source.get("id.resp_p") or "",
        "protocol": source.get("proto") or "",
        "signature": alert.get("signature") or source.get("query") or source.get("service") or source.get("app_proto") or "",
        "severity": alert.get("severity") or "",
        "risk": event_risk(source),
        "pivots": build_pivots(source),
    }


def nested_get(data: dict[str, Any], path: list[str]) -> Any:
    current: Any = data
    for item in path:
        if not isinstance(current, dict):
            return None
        current = current.get(item)
    return current


def event_risk(source: dict[str, Any]) -> str:
    alert = source.get("alert", {}) if isinstance(source.get("alert"), dict) else {}
    severity = alert.get("severity")
    if severity in (1, "1"):
        return "critical"
    if severity in (2, "2"):
        return "high"
    if source.get("event_type") == "alert":
        return "medium"
    return "low"


def build_pivots(source: dict[str, Any]) -> dict[str, str]:
    src = nested_get(source, ["source", "ip"]) or source.get("src_ip") or source.get("id.orig_h") or ""
    dst = nested_get(source, ["destination", "ip"]) or source.get("dest_ip") or source.get("id.resp_h") or ""
    pivots: dict[str, str] = {}
    if src:
        pivots["hunt_source"] = f"/?view=hunt&q=source.ip:{urllib.parse.quote(str(src))}"
    if dst:
        pivots["hunt_destination"] = f"/?view=hunt&q=destination.ip:{urllib.parse.quote(str(dst))}"
        pivots["pcap"] = f"/?view=pcap&ip={urllib.parse.quote(str(dst))}"
    return pivots


def query_from_text(text: str) -> dict[str, Any]:
    text = text.strip()
    if not text:
        return {"match_all": {}}
    if ":" in text and " " not in text:
        field, value = text.split(":", 1)
        return {"term": {field: value}}
    return {
        "query_string": {
            "query": text,
            "default_operator": "AND",
            "lenient": True,
        }
    }


def overview_payload() -> dict[str, Any]:
    assets = load_seed_assets()
    status = "online"

    try:
        total_events = count_events()
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        total_events = 0
        status = "degraded"

    try:
        alerts = count_events({"match": {"event_type": "alert"}})
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        alerts = 0

    try:
        recent = search_events({"match_all": {}}, size=8)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        recent = []

    try:
        modules = terms_aggregation("event.module", size=6)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        modules = []

    try:
        services = terms_aggregation("event_type.keyword", size=8)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        services = []

    critical_assets = [asset for asset in assets if str(asset.get("criticality", "")).lower() == "critical"]
    high_risk_assets = sorted(assets, key=lambda asset: int(asset.get("risk_score", 0)), reverse=True)[:8]

    return {
        "status": status,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "metrics": {
            "open_alerts": alerts,
            "indexed_events": total_events,
            "known_assets": len(assets),
            "critical_assets": len(critical_assets),
        },
        "recent_events": recent,
        "high_risk_assets": [format_asset(asset) for asset in high_risk_assets],
        "modules": modules,
        "services": services,
        "links": {
            "grafana": "http://localhost:3000/d/sentinelmesh-relationships/sentinelmesh-relationships",
            "opensearch_dashboards": "http://localhost:5601",
            "opensearch": "http://localhost:9200",
        },
    }


def format_asset(asset: dict[str, Any]) -> dict[str, Any]:
    vulnerabilities = asset.get("vulnerabilities") or []
    risk_score = int(asset.get("risk_score") or calculate_asset_display_risk(asset))
    return {
        "asset_id": asset.get("asset_id", ""),
        "name": asset_name(asset),
        "ip_addresses": asset.get("ip_addresses") or [],
        "criticality": asset.get("criticality", "unknown"),
        "risk_score": risk_score,
        "vulnerability_count": len(vulnerabilities),
        "internet_facing": bool((asset.get("exposure") or {}).get("internet_facing", False)),
        "tags": asset.get("tags") or [],
    }


def calculate_asset_display_risk(asset: dict[str, Any]) -> int:
    criticality_scores = {
        "low": 10,
        "medium": 30,
        "high": 55,
        "critical": 75,
    }
    score = criticality_scores.get(str(asset.get("criticality", "low")).lower(), 10)
    vulnerabilities = asset.get("vulnerabilities") or []
    severity_weights = {"low": 3, "medium": 7, "high": 12, "critical": 18}
    for vulnerability in vulnerabilities:
        if isinstance(vulnerability, dict):
            score += severity_weights.get(str(vulnerability.get("severity", "medium")).lower(), 7)
    exposure = asset.get("exposure") or {}
    if exposure.get("internet_facing"):
        score += 15
    open_ports = asset.get("open_ports") or []
    if len(open_ports) >= 3:
        score += 5
    return min(score, 100)


def response_json(handler: BaseHTTPRequestHandler, payload: dict[str, Any], status: int = 200) -> None:
    body = json.dumps(payload, indent=2).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Cache-Control", "no-store")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def response_file(handler: BaseHTTPRequestHandler, path: Path) -> None:
    if not path.exists() or not path.is_file():
        handler.send_error(404)
        return
    content_type = "text/html; charset=utf-8" if path.suffix == ".html" else "application/octet-stream"
    body = path.read_bytes()
    handler.send_response(200)
    handler.send_header("Content-Type", content_type)
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class SocHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:
        print(f"soc-portal {self.address_string()} {format % args}", flush=True)

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if parsed.path == "/api/health":
            response_json(self, {"status": "ok", "service": "soc-portal"})
            return

        if parsed.path == "/api/overview":
            response_json(self, overview_payload())
            return

        if parsed.path == "/api/events":
            query = query_from_text(params.get("q", [""])[0])
            size = int(params.get("size", ["25"])[0])
            try:
                response_json(self, {"events": search_events(query, size=min(size, 100))})
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                response_json(self, {"events": [], "error": str(exc)}, status=503)
            return

        if parsed.path == "/api/assets":
            assets = [format_asset(asset) for asset in load_seed_assets()]
            response_json(self, {"assets": assets})
            return

        if parsed.path == "/":
            response_file(self, STATIC_DIR / "index.html")
            return

        response_file(self, STATIC_DIR / parsed.path.lstrip("/"))


def main() -> None:
    host = os.getenv("SENTINELMESH_SOC_HOST", "0.0.0.0")
    port = int(os.getenv("SENTINELMESH_SOC_PORT", "8080"))
    server = ThreadingHTTPServer((host, port), SocHandler)
    print(f"soc-portal listening on {host}:{port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
