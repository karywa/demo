# scheduler/cli.py
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scheduler.formatter import format_csv, format_json, format_text
from scheduler.parser import ValidationError, parse_demands_from_file
from scheduler.scheduler import compute_hourly_agents


def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute hourly agent staffing from call requirements CSV."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to input CSV file.",
    )
    parser.add_argument(
        "--utilization",
        type=float,
        default=1.0,
        help="Agent utilization in (0,1], e.g. 0.8 for 80%%. "
             "Lower utilization → more agents.",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json", "csv"],
        default="text",
        help="Output format (default: text).",
    )
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)

    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"ERROR: input file does not exist: {input_path}", file=sys.stderr)
        return 1

    try:
        utilization = float(args.utilization)
    except (TypeError, ValueError):
        print("ERROR: --utilization must be a float", file=sys.stderr)
        return 1

    if not (0 < utilization <= 1.0):
        print("ERROR: --utilization must be in (0,1]", file=sys.stderr)
        return 1

    try:
        with input_path.open("r", newline="") as f:
            demands = parse_demands_from_file(f)
    except ValidationError as e:
        print(f"ERROR: invalid input CSV: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"ERROR: failed to read input file: {e}", file=sys.stderr)
        return 1

    hourly_agents = compute_hourly_agents(demands, utilization=utilization)

    if args.format == "json":
        out = format_json(hourly_agents)
    elif args.format == "csv":
        out = format_csv(hourly_agents)
    else:
        out = format_text(hourly_agents)

    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
