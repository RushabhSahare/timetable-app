from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory timetable: {time_slot: {day: activity}}
timetable = {}
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

@app.route("/")
def home():
    return render_template("index.html", timetable=timetable, days=days)

@app.route("/add", methods=["POST"])
def add():
    time_slot = request.form.get("time")
    day = request.form.get("day")
    activity = request.form.get("activity")

    if time_slot not in timetable:
        timetable[time_slot] = {}

    timetable[time_slot][day] = activity
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
