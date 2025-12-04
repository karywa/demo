# web_app.py
from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
import tempfile
import json

from scheduler.service import build_schedule_from_csv  # your existing function

app = Flask(__name__, static_folder="static", static_url_path="/static")


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/schedule", methods=["POST"])
def api_schedule():
    """
    POST /api/schedule with multipart/form-data:
      - file: CSV file
      - utilization: optional float
    """
    # Debug logging (optional but VERY useful right now)
    print("request.files keys:", list(request.files.keys()))
    print("request.form:", dict(request.form))

    if "file" not in request.files:
        return jsonify({"error": "missing file upload"}), 400

    file_storage = request.files["file"]
    if file_storage.filename == "":
        return jsonify({"error": "empty filename"}), 400

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = Path(tmp.name)
        file_storage.save(tmp_path)

    utilization_str = request.form.get("utilization", "1.0")
    try:
        utilization = float(utilization_str)
    except ValueError:
        return jsonify({"error": "invalid utilization"}), 400

    try:
        schedule = build_schedule_from_csv(tmp_path, utilization=utilization)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(schedule)


if __name__ == "__main__":
    app.run(debug=True)
