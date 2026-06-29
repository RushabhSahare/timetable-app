from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

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

@app.route("/")
def home():
    sorted_timetable = dict(sorted(timetable.items(), key=lambda x: x[0]))
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

    sorted_timetable = dict(sorted(timetable.items(), key=lambda x: x[0]))

    if not keyword:
        flash("Please enter a keyword to search.")
        return render_template("index.html", timetable=sorted_timetable, days=days, search_keyword=None)

    return render_template("index.html", timetable=sorted_timetable, days=days, search_keyword=keyword.lower())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
