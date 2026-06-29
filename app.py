from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

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
        json.dump(timetable, f)

@app.route("/")
def home():
    return render_template("index.html", timetable=timetable, days=days)

@app.route("/add", methods=["POST"])
def add():
    time = request.form.get("time")
    day = request.form.get("day")
    activity = request.form.get("activity")

    if time not in timetable:
        timetable[time] = {}
    timetable[time][day] = activity
    save_timetable()

    return redirect(url_for("home"))

@app.route("/edit/<time>/<day>", methods=["POST"])
def edit(time, day):
    new_activity = request.form.get("activity")
    if time in timetable and day in timetable[time]:
        timetable[time][day] = new_activity
        save_timetable()
    return redirect(url_for("home"))

@app.route("/delete/<time>/<day>", methods=["POST"])
def delete(time, day):
    if time in timetable and day in timetable[time]:
        del timetable[time][day]
        if not timetable[time]:
            del timetable[time]
        save_timetable()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
