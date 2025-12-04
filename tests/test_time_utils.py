# tests/test_time_utils.py
import pytest

from scheduler.time_utils import parse_time_label


@pytest.mark.parametrize(
    "label, expected",
    [
        ("12AM", 0),
        ("12am", 0),
        ("12PM", 12),
        ("12pm", 12),
        ("1AM", 1),
        ("1PM", 13),
        ("11PM", 23),
        ("6AM", 6),
        ("09:00", 9),
        ("23:30", 23),
        ("0", 0),
        ("24", 24),
    ],
)
def test_parse_time_label_valid(label, expected):
    assert parse_time_label(label) == expected


@pytest.mark.parametrize(
    "label",
    [
        "25:00",   # hour out of range
        "13PM",    # invalid 12h + AM/PM
        "0PM",     # invalid 12h + AM/PM
        "12MM",    # bad suffix
        "abc",     # garbage
        "",        # empty
        "10:99",   # invalid minutes
    ],
)
def test_parse_time_label_invalid(label):
    with pytest.raises(ValueError):
        parse_time_label(label)
