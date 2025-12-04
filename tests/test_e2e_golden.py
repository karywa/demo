# tests/test_e2e_golden.py
from pathlib import Path
import json
import subprocess
import sys


def test_e2e_golden_sample():
    """
    Run CLI on sample.csv and compare JSON output to golden_sample.json.
    """
    root = Path(__file__).resolve().parents[1]
    sample_csv = root / "tests" / "golden_sample_input.csv"
    golden = root / "tests" / "golden_sample_result.json"

    cmd = [
        sys.executable,
        "-m",
        "scheduler.cli",
        "--input",
        str(sample_csv),
        "--format=json",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    actual = json.loads(result.stdout.strip())
    expected = json.loads(golden.read_text())

    assert actual == expected
