# scheduler/scheduler.py
from __future__ import annotations

from math import ceil
from typing import Dict, List

from scheduler.parser import CustomerDemand


HourlyAgents = Dict[int, Dict[str, int]]  # hour -> customer_name -> agents


def compute_hourly_agents(
    demands: List[CustomerDemand],
    utilization: float = 1.0,
) -> HourlyAgents:
    """
    Compute agents needed per hour per customer.

    utilization: fraction of each agent's capacity that is usable (0 < u <= 1).
    More conservative sizing with u < 1 → more agents:
        agents = ceil(raw_agents / utilization)
    """
    if utilization <= 0 or utilization > 1.0:
        raise ValueError("utilization must be in (0, 1]")

    per_hour: HourlyAgents = {h: {} for h in range(24)}

    for d in demands:
        active_hours = list(range(d.start_hour, d.end_hour))
        if not active_hours:
            # Should not happen due to validation, but guard anyway
            continue

        calls_per_hour = d.num_calls / float(len(active_hours))

        for h in active_hours:
            raw_agents = (calls_per_hour * d.avg_call_duration_s) / 3600.0
            # Avoid negative/NaN; validation should prevent it
            effective = raw_agents / utilization
            agents = int(ceil(effective))
            if agents <= 0:
                continue

            per_customer = per_hour[h]
            per_customer[d.name] = per_customer.get(d.name, 0) + agents

    return per_hour
