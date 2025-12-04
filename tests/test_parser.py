# tests/test_parser.py
from io import StringIO

import pytest

from scheduler.parser import (
    ValidationError,
    parse_demands_from_file,
)


def test_parse_single_valid_row():
    csv_data = """#CustomerName, AverageCallDurationSeconds, StartTimePT, EndTimePT, NumberOfCalls, Priority
TestClient, 300, 9AM, 5PM, 100, 2
"""
    f = StringIO(csv_data)
    demands = parse_demands_from_file(f)

    assert len(demands) == 1
    d = demands[0]
    assert d.name == "TestClient"
    assert d.avg_call_duration_s == 300
    # 9AM -> 9, 5PM -> 17 (end exclusive)
    assert d.start_hour == 9
    assert d.end_hour == 17
    assert d.num_calls == 100
    assert d.priority == 2


def test_parse_skips_comments_and_blank_lines():
    csv_data = """
# Header line
#CustomerName, AverageCallDurationSeconds, StartTimePT, EndTimePT, NumberOfCalls, Priority

ClientA, 120, 6AM, 10AM, 50, 1

"""
    f = StringIO(csv_data)
    demands = parse_demands_from_file(f)
    assert len(demands) == 1
    assert demands[0].name == "ClientA"


def test_parse_invalid_priority_raises():
    csv_data = "BadClient, 300, 9AM, 5PM, 100, 7\n"
    f = StringIO(csv_data)
    with pytest.raises(ValidationError):
        parse_demands_from_file(f)


def test_parse_negative_calls_raises():
    csv_data = "BadClient, 300, 9AM, 5PM, -10, 1\n"
    f = StringIO(csv_data)
    with pytest.raises(ValidationError):
        parse_demands_from_file(f)


def test_parse_end_before_start_raises():
    csv_data = "BadWindow, 300, 5PM, 9AM, 10, 1\n"
    f = StringIO(csv_data)
    with pytest.raises(ValidationError):
        parse_demands_from_file(f)
