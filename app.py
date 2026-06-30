from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import json
import os
from datetime import datetime
from io import BytesIO

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # required for flash messages

DATA_FILE = "timetable.json"
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Load timetable from file if it exists
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        timetable = json.load(f)
else:
    timetable = {}

def save_timetable():
    with open(DATA_FILE, "w") as f:
        json.dump(timetable, f, indent=4)

def parse_time(t):
    """Convert '6 am', '3 pm', '9:30 am' into datetime for sorting."""
    try:
        return datetime.strptime(t.strip().lower(), "%I %p")
    except ValueError:
        try:
            return datetime.strptime(t.strip().lower(), "%I:%M %p")
        except ValueError:
            return datetime.max  # fallback for bad formats

@app.route("/")
def home():
    sorted_timetable = dict(sorted(timetable.items(), key=lambda x: parse_time(x[0])))
    return render_template("index.html", timetable=sorted_timetable, days=days, search_keyword=None)

@app.route("/add", methods=["POST"])
def add():
    time = request.form.get("time")
    day = request.form.get("day")
    activity = request.form.get("activity")

    if time in timetable and day in timetable[time]:
        flash(f"⚠️ An activity already exists for {time} on {day}. Please edit it instead.")
        return redirect(url_for("home"))

    if time not in timetable:
        timetable[time] = {}
    timetable[time][day] = activity
    save_timetable()

    flash(f"✅ Added activity for {time} on {day}.")
    return redirect(url_for("home"))

@app.route("/edit/<time>/<day>", methods=["POST"])
def edit(time, day):
    new_activity = request.form.get("activity")
    if time in timetable and day in timetable[time]:
        timetable[time][day] = new_activity
        save_timetable()
        flash(f"✏️ Updated activity for {time} on {day}.")
    return redirect(url_for("home"))

@app.route("/delete/<time>/<day>", methods=["POST"])
def delete(time, day):
    if time in timetable and day in timetable[time]:
        del timetable[time][day]
        if not timetable[time]:
            del timetable[time]
        save_timetable()
        flash(f"🗑️ Deleted activity for {time} on {day}.")
    return redirect(url_for("home"))

@app.route("/search", methods=["POST"])
def search():
    keyword = request.form.get("keyword", "").strip()
    day = request.form.get("day", "")

    sorted_timetable = dict(sorted(timetable.items(), key=lambda x: parse_time(x[0])))

    if not keyword:
        flash("Please enter a keyword to search.")
        return render_template("index.html", timetable=sorted_timetable, days=days, search_keyword=None)

    return render_template("index.html", timetable=sorted_timetable, days=days, search_keyword=keyword.lower())

@app.route("/export")
def export():
    if not timetable:
        flash("No timetable data to export.")
        return redirect(url_for("home"))

    data = json.dumps(timetable, indent=4)
    return send_file(
        BytesIO(data.encode("utf-8")),
        mimetype="application/json",
        as_attachment=True,
        download_name="timetable_backup.json"
    )

@app.route("/import", methods=["POST"])
def import_file():
    file = request.files.get("file")
    if not file:
        flash("No file selected for import.")
        return redirect(url_for("home"))

    try:
        imported = json.load(file)
        global timetable
        timetable = imported
        save_timetable()
        flash("✅ Timetable imported successfully.")
    except Exception as e:
        flash(f"⚠️ Failed to import file: {e}")

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
