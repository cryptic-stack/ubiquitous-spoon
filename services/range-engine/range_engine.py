#!/usr/bin/env python3
"""SentinelMesh cyber range engine.

MVP behavior:
- Discover available scenario JSON files.
- Emit periodic status with scenario names.

Future behavior:
- Inject synthetic logs.
- Coordinate PCAP replay.
- Send scoring events to CTFd or other range systems.
"""

from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_scenarios(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    scenarios: list[dict[str, Any]] = []
    for scenario_path in sorted(path.glob("*.json")):
        with scenario_path.open("r", encoding="utf-8") as handle:
            scenario = json.load(handle)
        scenario["_path"] = str(scenario_path)
        scenarios.append(scenario)

    return scenarios


def main() -> None:
    scenario_dir = Path(os.getenv("SENTINELMESH_RANGE_SCENARIO_DIR", "/scenarios/range"))
    interval = int(os.getenv("SENTINELMESH_RANGE_INTERVAL", "300"))

    while True:
        scenarios = load_scenarios(scenario_dir)
        summary = {
            "service": "range-engine",
            "status": "running",
            "timestamp": utc_now(),
            "scenario_dir": str(scenario_dir),
            "scenario_count": len(scenarios),
            "scenarios": [scenario.get("id", "unknown") for scenario in scenarios],
        }
        print(json.dumps(summary), flush=True)
        time.sleep(interval)


if __name__ == "__main__":
    main()
