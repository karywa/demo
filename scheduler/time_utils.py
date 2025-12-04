# scheduler/time_utils.py
from __future__ import annotations

import re


_TIME_RE = re.compile(
    r"""
    ^\s*
    (?P<hour>\d{1,2})
    (:(?P<minute>\d{2}))?
    (?P<ampm>\s*[AaPp][Mm])?
    \s*$
    """,
    re.VERBOSE,
)


def parse_time_label(label: str) -> int:
    """
    Parse a time label like "6AM", "11PM", "09:00", "23" into an hour [0, 24].

    - 12AM -> 0
    - 12PM -> 12
    - 1PM  -> 13
    - If no AM/PM, treat as 24-hour clock.
    - Minutes are allowed but ignored for bucketing.
    """
    m = _TIME_RE.match(label)
    if not m:
        raise ValueError(f"Invalid time label: {label!r}")

    hour = int(m.group("hour"))
    minute = m.group("minute")
    ampm = m.group("ampm")
    minute_val = int(minute) if minute is not None else 0
    if not (0 <= minute_val < 60):
        raise ValueError(f"Invalid minutes in time label: {label!r}")

    if ampm:
        ampm = ampm.strip().lower()
        if not (1 <= hour <= 12):
            raise ValueError(f"Hour out of range for AM/PM time: {label!r}")
        if ampm == "am":
            if hour == 12:
                hour = 0
        elif ampm == "pm":
            if hour != 12:
                hour += 12
        else:
            raise ValueError(f"Invalid AM/PM suffix in time label: {label!r}")
    else:
        # 24-hour format
        if not (0 <= hour <= 24):
            raise ValueError(f"Hour out of range for 24-hour time: {label!r}")

    return hour
