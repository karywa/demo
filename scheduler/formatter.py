# scheduler/formatter.py
from __future__ import annotations

import json
from typing import Dict

from scheduler.scheduler import HourlyAgents


def _format_hour_label(hour: int) -> str:
    return f"{hour:02d}:00"


def format_text(hourly_agents: HourlyAgents) -> str:
    """
    Produce the 24-line human-readable format:

    06:00 : total=193 ; VNS=193
    """
    lines = []
    for h in range(24):
        hour_label = _format_hour_label(h)
        per_customer = hourly_agents.get(h, {}) or {}
        total = sum(per_customer.values())
        if total == 0:
            lines.append(f"{hour_label} : total=0 ; none")
            continue

        # Deterministic ordering: alphabetical by customer name
        parts = [f"{name}={per_customer[name]}" for name in sorted(per_customer.keys())]
        detail = ", ".join(parts)
        lines.append(f"{hour_label} : total={total} ; {detail}")
    return "\n".join(lines)


def format_json(hourly_agents: HourlyAgents) -> str:
    """
    Emit a stable JSON structure:

    [
      {
        "hour": "06:00",
        "total": 193,
        "customers": {"VNS": 193}
      },
      ...
    ]
    """
    result = []
    for h in range(24):
        per_customer = hourly_agents.get(h, {}) or {}
        total = sum(per_customer.values())
        result.append(
            {
                "hour": _format_hour_label(h),
                "total": total,
                "customers": {
                    name: per_customer[name]
                    for name in sorted(per_customer.keys())
                },
            }
        )
    return json.dumps(result, indent=2, sort_keys=False)


def format_csv(hourly_agents: HourlyAgents) -> str:
    """
    Simple long-form CSV:

    hour,total,customer,agents
    06:00,193,VNS,193
    07:00,877,VNS,193
    07:00,877,ANMC,684
    ...
    """
    lines = ["hour,total,customer,agents"]
    for h in range(24):
        hour_label = _format_hour_label(h)
        per_customer: Dict[str, int] = hourly_agents.get(h, {}) or {}
        total = sum(per_customer.values())
        if not per_customer:
            lines.append(f"{hour_label},{total},,0")
        else:
            # One row per customer
            for name in sorted(per_customer.keys()):
                agents = per_customer[name]
                lines.append(f"{hour_label},{total},{name},{agents}")
    return "\n".join(lines)
