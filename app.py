from flask import Flask, render_template, request, make_response
import csv
import uuid
from datetime import datetime
from collections import defaultdict
import os

app = Flask(__name__)

# ---------------- SESSION STORAGE ----------------
user_sessions = defaultdict(list)

# ---------------- CREATE BOT LOG FILE (ONCE) ----------------
if not os.path.exists("bot_logs.csv"):
    with open("bot_logs.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "session_id",
            "ip",
            "user_agent",
            "pages_visited",
            "session_duration",
            "avg_time_per_page",
            "pages_per_min",
            "timestamp"
        ])

# ---------------- NORMAL LOGGING ----------------
def log_request(session_id, page):
    timestamp = datetime.now()

    # Save normal logs
    with open("logs.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            session_id,
            page,
            timestamp,
            request.remote_addr,
            request.headers.get("User-Agent")
        ])

    # Track session behavior
    user_sessions[session_id].append(timestamp)

    times = user_sessions[session_id]
    pages = len(times)

    # Only calculate if multiple pages visited
    if pages > 1:
        time_diff = (times[-1] - times[0]).total_seconds()

        avg_time = time_diff / pages if pages > 0 else 0
        pages_per_min = pages / (time_diff / 60) if time_diff > 0 else pages

        # ---------------- BOT DETECTION ----------------
        if pages_per_min > 20 or avg_time < 2:
            log_bot(
                session_id,
                request.remote_addr,
                request.headers.get("User-Agent"),
                pages,
                time_diff,
                avg_time,
                pages_per_min
            )

# ---------------- BOT LOGGING ----------------
def log_bot(session_id, ip, user_agent, pages, session_duration, avg_time, ppm):
    with open("bot_logs.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            session_id,
            ip,
            user_agent,
            pages,
            session_duration,
            avg_time,
            ppm,
            datetime.now()
        ])

    print(f"🚨 BOT DETECTED: {session_id}")

# ---------------- SESSION ID ----------------
def get_session_id():
    return str(uuid.uuid4())

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = get_session_id()

    log_request(session_id, "home")

    response = make_response(render_template("index.html"))
    response.set_cookie("session_id", session_id)
    return response


@app.route("/about")
def about():
    session_id = request.cookies.get("session_id")
    log_request(session_id, "about")
    return render_template("about/index.html")


@app.route("/mars")
def mars():
    session_id = request.cookies.get("session_id")
    log_request(session_id, "mars")
    return render_template("articles/mars.html")


@app.route("/blackholes")
def blackholes():
    session_id = request.cookies.get("session_id")
    log_request(session_id, "blackholes")
    return render_template("articles/blackholes.html")


@app.route("/artemis")
def artemis():
    session_id = request.cookies.get("session_id")
    log_request(session_id, "artemis")
    return render_template("articles/artemis.html")


@app.route("/category")
def category():
    session_id = request.cookies.get("session_id")
    log_request(session_id, "category")
    return render_template("category/index.html")


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)