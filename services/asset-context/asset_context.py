#!/usr/bin/env python3
"""SentinelMesh asset context service.

MVP behavior:
- Load optional seed assets from JSON.
- Normalize asset records.
- Calculate explainable risk scores.
- Emit periodic health/state summaries.

Future behavior:
- Pull passive observations from indexed Zeek, Suricata, and Arkime data.
- Import vulnerability scanner results.
- Write enriched asset state back to OpenSearch.
"""

from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CRITICALITY_BASE_SCORE = {
    "low": 5,
    "medium": 15,
    "high": 25,
    "critical": 35,
}

VULNERABILITY_WEIGHTS = {
    "info": 0,
    "low": 2,
    "medium": 5,
    "high": 10,
    "critical": 20,
}


@dataclass(frozen=True)
class AssetContextConfig:
    asset_index: str
    event_index_pattern: str
    opensearch_url: str
    risk_model: str
    seed_assets_path: Path | None
    interval_seconds: int


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_asset_id(asset: dict[str, Any]) -> str:
    """Create a deterministic ID when an asset does not provide one."""

    identity_parts: list[str] = []
    identity_parts.extend(asset.get("mac_addresses") or [])
    identity_parts.extend(asset.get("ip_addresses") or [])
    identity_parts.extend(asset.get("hostnames") or [])
    identity_parts.append(asset.get("fqdn") or "")
    identity = "|".join(sorted(part for part in identity_parts if part))

    if not identity:
        return str(uuid.uuid4())

    return str(uuid.uuid5(uuid.NAMESPACE_DNS, identity))


def normalize_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def normalize_asset(asset: dict[str, Any]) -> dict[str, Any]:
    now = utc_now()
    normalized = dict(asset)

    normalized["asset_id"] = normalized.get("asset_id") or stable_asset_id(normalized)
    normalized["ip_addresses"] = normalize_list(normalized.get("ip_addresses"))
    normalized["mac_addresses"] = normalize_list(normalized.get("mac_addresses"))
    normalized["hostnames"] = normalize_list(normalized.get("hostnames"))
    normalized["fqdn"] = normalized.get("fqdn") or ""
    normalized["first_seen"] = normalized.get("first_seen") or now
    normalized["last_seen"] = normalized.get("last_seen") or now
    normalized["os_guess"] = normalized.get("os_guess") or ""
    normalized["services"] = normalize_list(normalized.get("services"))
    normalized["open_ports"] = normalize_list(normalized.get("open_ports"))
    normalized["protocols"] = normalize_list(normalized.get("protocols"))
    normalized["users_observed"] = normalize_list(normalized.get("users_observed"))
    normalized["criticality"] = normalized.get("criticality") or "low"
    normalized["tags"] = normalize_list(normalized.get("tags"))
    normalized["vulnerabilities"] = normalize_list(normalized.get("vulnerabilities"))
    normalized["exposure"] = normalized.get("exposure") or {
        "internet_facing": False,
        "internal_only": True,
    }

    risk = calculate_risk(normalized)
    normalized["risk_score"] = risk["score"]
    normalized["risk_breakdown"] = risk["breakdown"]

    return normalized


def calculate_risk(asset: dict[str, Any]) -> dict[str, Any]:
    breakdown: list[dict[str, Any]] = []
    score = 0

    criticality = str(asset.get("criticality", "low")).lower()
    criticality_score = CRITICALITY_BASE_SCORE.get(criticality, 5)
    score += criticality_score
    breakdown.append(
        {
            "factor": "asset_criticality",
            "value": criticality,
            "score": criticality_score,
        }
    )

    for vulnerability in asset.get("vulnerabilities", []):
        severity = str(vulnerability.get("severity", "low")).lower()
        weight = VULNERABILITY_WEIGHTS.get(severity, 2)
        cvss = vulnerability.get("cvss")
        if isinstance(cvss, (int, float)) and cvss >= 9:
            weight = max(weight, 20)
        score += weight
        breakdown.append(
            {
                "factor": "vulnerability",
                "id": vulnerability.get("id", "unknown"),
                "severity": severity,
                "score": weight,
            }
        )

    exposure = asset.get("exposure", {})
    if exposure.get("internet_facing"):
        score += 20
        breakdown.append(
            {
                "factor": "exposure",
                "value": "internet_facing",
                "score": 20,
            }
        )

    sensitive_ports = {22, 3389, 445, 5985, 5986}
    open_ports = {int(port) for port in asset.get("open_ports", []) if str(port).isdigit()}
    exposed_sensitive_ports = sorted(open_ports.intersection(sensitive_ports))
    if exposed_sensitive_ports:
        score += 10
        breakdown.append(
            {
                "factor": "sensitive_service_exposure",
                "ports": exposed_sensitive_ports,
                "score": 10,
            }
        )

    return {
        "score": min(score, 100),
        "breakdown": breakdown,
    }


def load_seed_assets(path: Path | None) -> list[dict[str, Any]]:
    if path is None or not path.exists():
        return []

    with path.open("r", encoding="utf-8") as handle:
        raw_assets = json.load(handle)

    if not isinstance(raw_assets, list):
        raise ValueError(f"Seed asset file must contain a JSON array: {path}")

    return [normalize_asset(asset) for asset in raw_assets]


def load_config() -> AssetContextConfig:
    seed_path = os.getenv("SENTINELMESH_ASSET_SEED_PATH")
    interval = int(os.getenv("SENTINELMESH_ASSET_CONTEXT_INTERVAL", "300"))

    return AssetContextConfig(
        asset_index=os.getenv("SENTINELMESH_ASSET_INDEX", "sentinelmesh-assets"),
        event_index_pattern=os.getenv(
            "SENTINELMESH_EVENT_INDEX_PATTERN", "sentinelmesh-events-*"
        ),
        opensearch_url=os.getenv(
            "SENTINELMESH_OPENSEARCH_URL", "http://opensearch:9200"
        ),
        risk_model=os.getenv("SENTINELMESH_RISK_MODEL", "mvp-v1"),
        seed_assets_path=Path(seed_path) if seed_path else None,
        interval_seconds=interval,
    )


def service_summary(config: AssetContextConfig, assets: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "service": "asset-context",
        "status": "running",
        "timestamp": utc_now(),
        "asset_index": config.asset_index,
        "event_index_pattern": config.event_index_pattern,
        "opensearch_url": config.opensearch_url,
        "risk_model": config.risk_model,
        "seed_assets_loaded": len(assets),
        "highest_seed_risk": max((asset["risk_score"] for asset in assets), default=0),
    }


def main() -> None:
    config = load_config()
    assets = load_seed_assets(config.seed_assets_path)

    while True:
        print(json.dumps(service_summary(config, assets)), flush=True)
        time.sleep(config.interval_seconds)


if __name__ == "__main__":
    main()
