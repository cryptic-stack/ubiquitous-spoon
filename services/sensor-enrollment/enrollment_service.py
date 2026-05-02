#!/usr/bin/env python3
"""SentinelMesh sensor enrollment service.

MVP behavior:
- Report whether enrollment token storage is present.
- Provide a container target for future enrollment API work.

Future behavior:
- Issue and validate sensor enrollment tokens.
- Return manager/receiver/log pipeline settings.
- Track enrolled sensors and health heartbeats.
"""

from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def token_count(enrollment_dir: Path) -> int:
    token_file = enrollment_dir / "tokens.jsonl"
    if not token_file.exists():
        return 0
    with token_file.open("r", encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def main() -> None:
    enrollment_dir = Path(os.getenv("SENTINELMESH_ENROLLMENT_DIR", "/enrollment"))
    interval = int(os.getenv("SENTINELMESH_ENROLLMENT_INTERVAL", "300"))
    enrollment_dir.mkdir(parents=True, exist_ok=True)

    while True:
        summary = {
            "service": "sensor-enrollment",
            "status": "running",
            "timestamp": utc_now(),
            "enrollment_dir": str(enrollment_dir),
            "token_count": token_count(enrollment_dir),
        }
        print(json.dumps(summary), flush=True)
        time.sleep(interval)


if __name__ == "__main__":
    main()
