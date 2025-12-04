# scheduler/service.py
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from scheduler.parser import parse_demands_from_file
from scheduler.scheduler import compute_hourly_agents
from scheduler.formatter import format_json


def build_schedule_from_csv(path: Path, utilization: float = 1.0) -> Dict[str, Any]:
    """
    Core entrypoint for non-CLI callers (UI, tests, etc.)
    Returns *data*, not preformatted strings.
    """
    with path.open("r", newline="") as f:
        demands = parse_demands_from_file(f)
    hourly_agents = compute_hourly_agents(demands, utilization=utilization)

    # Reuse JSON formatter structure but decode it to Python objects
    import json
    return json.loads(format_json(hourly_agents))
