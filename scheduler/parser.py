# scheduler/parser.py
from __future__ import annotations

import csv
from dataclasses import dataclass
from typing import List, TextIO

from scheduler.time_utils import parse_time_label


class ValidationError(Exception):
    """Raised when the input CSV has invalid contents."""


@dataclass
class CustomerDemand:
    name: str
    avg_call_duration_s: float
    start_hour: int  # inclusive, 0-23
    end_hour: int    # exclusive, 1-24
    num_calls: int
    priority: int


def _parse_int(field: str, field_name: str) -> int:
    try:
        return int(field)
    except ValueError:
        raise ValidationError(f"Invalid integer for {field_name}: {field!r}")


def _parse_float(field: str, field_name: str) -> float:
    try:
        return float(field)
    except ValueError:
        raise ValidationError(f"Invalid float for {field_name}: {field!r}")


def _parse_priority(field: str) -> int:
    value = _parse_int(field, "Priority")
    if not (1 <= value <= 5):
        raise ValidationError(f"Priority out of range [1,5]: {value}")
    return value


def parse_demands_from_file(f: TextIO) -> List[CustomerDemand]:
    """
    Parse and validate customer demands from a CSV file-like object.
    """
    reader = csv.reader(f)
    demands: List[CustomerDemand] = []

    for line_no, row in enumerate(reader, start=1):
        # Skip empty lines
        if not row or all(not cell.strip() for cell in row):
            continue

        # Allow optional comment line starting with '#'
        if row[0].strip().startswith("#"):
            continue

        if len(row) < 6:
            raise ValidationError(f"Line {line_no}: expected 6 fields, got {len(row)}")

        (
            name,
            avg_call_duration_s,
            start_time_str,
            end_time_str,
            num_calls_str,
            priority_str,
        ) = [cell.strip() for cell in row[:6]]

        if not name:
            raise ValidationError(f"Line {line_no}: CustomerName is empty")

        avg_duration = _parse_float(avg_call_duration_s, "AverageCallDurationSeconds")
        if avg_duration <= 0:
            raise ValidationError(
                f"Line {line_no}: AverageCallDurationSeconds must be > 0"
            )

        num_calls = _parse_int(num_calls_str, "NumberOfCalls")
        if num_calls < 0:
            raise ValidationError(f"Line {line_no}: NumberOfCalls must be >= 0")

        priority = _parse_priority(priority_str)

        try:
            start_hour = parse_time_label(start_time_str)
            end_hour = parse_time_label(end_time_str)
        except ValueError as e:
            raise ValidationError(f"Line {line_no}: {e}") from e

        if not (0 <= start_hour < 24):
            raise ValidationError(f"Line {line_no}: start hour out of range: {start_hour}")
        if not (1 <= end_hour <= 24):
            raise ValidationError(f"Line {line_no}: end hour out of range: {end_hour}")
        if end_hour <= start_hour:
            raise ValidationError(
                f"Line {line_no}: EndTime must be after StartTime "
                f"(start={start_hour}, end={end_hour})"
            )

        demands.append(
            CustomerDemand(
                name=name,
                avg_call_duration_s=avg_duration,
                start_hour=start_hour,
                end_hour=end_hour,
                num_calls=num_calls,
                priority=priority,
            )
        )

    if not demands:
        raise ValidationError("No valid customer rows found in CSV")

    return demands
