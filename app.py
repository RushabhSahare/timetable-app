from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simple in-memory timetable
timetable = {}
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

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

    return redirect(url_for("home"))

@app.route("/edit/<time>/<day>", methods=["POST"])
def edit(time, day):
    new_activity = request.form.get("activity")
    if time in timetable and day in timetable[time]:
        timetable[time][day] = new_activity
    return redirect(url_for("home"))

@app.route("/delete/<time>/<day>", methods=["POST"])
def delete(time, day):
    if time in timetable and day in timetable[time]:
        del timetable[time][day]
        # Remove the time slot if empty
        if not timetable[time]:
            del timetable[time]
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
