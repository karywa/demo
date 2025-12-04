# tests/test_scheduler.py
from scheduler.parser import CustomerDemand
from scheduler.scheduler import compute_hourly_agents


def test_single_call_full_hour():
    """
    1 call of 3600s in a 1-hour window -> exactly 1 agent.
    """
    d = CustomerDemand(
        name="ClientX",
        avg_call_duration_s=3600,  # 1hr
        start_hour=10,
        end_hour=11,
        num_calls=1,
        priority=1,
    )
    hourly = compute_hourly_agents([d], utilization=1.0)

    # Only hour 10 should have 1 agent
    assert hourly[10]["ClientX"] == 1
    for h in range(24):
        if h != 10:
            assert "ClientX" not in hourly[h]


def test_uniform_distribution_multi_hour():
    """
    6 calls of 600s (10 min) over 3 hours:
    calls_per_hour = 2, raw_agents = (2 * 600) / 3600 = 1/3.
    With utilization 1.0 -> ceil(1/3) = 1 agent per hour.
    """
    d = CustomerDemand(
        name="ClientY",
        avg_call_duration_s=600,
        start_hour=9,
        end_hour=12,  # hours 9,10,11
        num_calls=6,
        priority=1,
    )

    hourly = compute_hourly_agents([d], utilization=1.0)

    for h in [9, 10, 11]:
        assert hourly[h]["ClientY"] == 1
    for h in range(24):
        if h not in [9, 10, 11]:
            assert "ClientY" not in hourly[h]


def test_utilization_makes_staffing_more_conservative():
    """
    raw_agents = 1.0. With u=1.0 -> 1 agent.
    With u=0.8 -> ceil(1.0 / 0.8) = 2 agents.
    """
    d = CustomerDemand(
        name="ClientZ",
        avg_call_duration_s=600,  # 10 min
        start_hour=9,
        end_hour=10,
        num_calls=6,  # 6*600 /3600 = 1.0 raw
        priority=1,
    )

    hourly = compute_hourly_agents([d], utilization=1.0)
    assert hourly[9]["ClientZ"] == 1

    hourly_conservative = compute_hourly_agents([d], utilization=0.8)
    assert hourly_conservative[9]["ClientZ"] == 2
