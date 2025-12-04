Agent Call Scheduler — Take-Home Assignment

This project implements a control-plane scheduler that determines the number of agents needed per hour to complete customer call workloads. It supports a CLI, a tiny web UI, full test coverage (unit + golden tests), and a clean modular architecture.

📦 Features
✔ Command-Line Scheduler

Reads a CSV input describing customer call workloads

Validates fields (time, numeric values, priority)

Computes per-hour agent requirements

Supports multiple output formats (text, json, csv)

Supports utilization adjustments (--utilization 0.8)

Deterministic: prints exactly 24 hours (00–23)

✔ Tiny Web UI (Bonus)

Upload CSV file directly in the browser

Shows a 24-column grid (1 cell = 1 hour)

Hover over each hour to see customer breakdown

Powered by Flask + static HTML/CSS/JS

Uses the same scheduling engine as CLI

✔ Tests

Unit tests for:

time parsing

CSV validation

hourly math

Golden test for deterministic end-to-end output

pytest.ini ensures only project tests are discovered

📁 Project Structure
project/
│
├── scheduler/
│   ├── __init__.py
│   ├── cli.py              # CLI entry point
│   ├── parser.py           # CSV parsing + validation
│   ├── scheduler.py        # core scheduling math
│   ├── formatter.py        # text/json/csv output
│   ├── service.py          # shared service for CLI + UI
│   └── time_utils.py       # robust time parsing
│
├── tests/
│   ├── test_time_utils.py
│   ├── test_parser.py
│   ├── test_scheduler.py
│   ├── test_e2e_golden.py
│   └── golden_sample.json
│
├── static/
│   └── index.html          # tiny web UI
│
├── sample.csv              # reference CSV used for golden test
├── web_app.py              # Flask server for UI
├── requirements.txt
├── design.md               # 1-page design document
├── Makefile
└── README.md

⚙️ Installation

Requires Python 3.10+.

Create and activate a virtual environment:

python3 -m venv .venv
source .venv/bin/activate


Install dependencies:

pip install -r requirements.txt

🖥️ CLI Usage

Run the CLI with a CSV input file:

python3 -m scheduler.cli --input sample.csv

JSON output
python3 -m scheduler.cli --input sample.csv --format=json

CSV output
python3 -m scheduler.cli --input sample.csv --format=csv

Utilization example
python3 -m scheduler.cli --input sample.csv --utilization 0.85


Or via Makefile:

make run INPUT=sample.csv

🌐 Tiny Web UI

Start the tiny UI server:

python3 web_app.py


Open:

http://localhost:5000/


UI features:

Upload any .csv file

Adjust utilization

Grid updates live

Hover for per-customer breakdown

🧪 Testing

Run all tests:

pytest -q


or via Makefile:

make test


Tests include:

Time parsing edge cases (12AM, 12PM, 09:00)

CSV validation (priority, numeric bounds)

Hourly math & utilization behavior

Golden test ensuring deterministic CLI output

📄 CSV Format

Input CSV example:

#CustomerName, AverageCallDurationSeconds, StartTimePT, EndTimePT, NumberOfCalls, Priority
Stanford Hospital, 300, 9AM, 7PM, 20000, 1


Rules:

Start inclusive, End exclusive

Calls uniformly distributed across active hours

Priority range 1–5 (not used in MVP scheduling)

Agents per hour =

ceil((calls_per_hour * avg_duration_sec / 3600) / utilization)
