from flask import Flask, render_template, request, make_response
import csv
import uuid
from datetime import datetime
from collections import defaultdict
import os

app = Flask(__name__)

# ---------------- SESSION STORAGE ----------------
user_sessions = defaultdict(list)
detected_bots = set()

# ---------------- CREATE LOG FILES ----------------
if not os.path.exists("logs.csv"):
    with open("logs.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "session_id", "page", "timestamp", "ip", "user_agent"
        ])

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

# ---------------- SESSION ID ----------------
def get_session_id():
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id

# ---------------- RESPONSE HELPER ----------------
def create_response(template, session_id):
    response = make_response(render_template(template))
    response.set_cookie("session_id", session_id)
    return response

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

# ---------------- NORMAL LOGGING + DETECTION ----------------
def log_request(session_id, page):
    timestamp = datetime.now()

    # Save logs
    with open("logs.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            session_id,
            page,
            timestamp,
            request.remote_addr,
            request.headers.get("User-Agent")
        ])

    # Track session
    user_sessions[session_id].append(timestamp)

    times = user_sessions[session_id]
    pages = len(times)

    if pages > 1:
        time_diff = (times[-1] - times[0]).total_seconds()
        time_diff = max(time_diff, 0.1)

        avg_time = time_diff / (pages - 1)
        pages_per_min = pages / (time_diff / 60)

        intervals = [
            (times[i] - times[i - 1]).total_seconds()
            for i in range(1, len(times))
        ]

        mean_interval = sum(intervals) / len(intervals) if intervals else 0

        ua = str(request.headers.get("User-Agent")).lower()

        # ---------------- BOT DETECTION ----------------
        if session_id not in detected_bots and (
            (pages_per_min > 100 and avg_time < 1.0) or
            (len(intervals) > 3 and mean_interval < 0.5) or
            ("bot" in ua)
        ):
            detected_bots.add(session_id)

            log_bot(
                session_id,
                request.remote_addr,
                request.headers.get("User-Agent"),
                pages,
                time_diff,
                avg_time,
                pages_per_min
            )

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    session_id = get_session_id()
    log_request(session_id, "home")
    return create_response("index.html", session_id)


@app.route("/about")
def about():
    session_id = get_session_id()
    log_request(session_id, "about")
    return create_response("about/index.html", session_id)


@app.route("/mars")
def mars():
    session_id = get_session_id()
    log_request(session_id, "mars")
    return create_response("articles/mars.html", session_id)


@app.route("/blackholes")
def blackholes():
    session_id = get_session_id()
    log_request(session_id, "blackholes")
    return create_response("articles/blackholes.html", session_id)


@app.route("/artemis")
def artemis():
    session_id = get_session_id()
    log_request(session_id, "artemis")
    return create_response("articles/artemis.html", session_id)


@app.route("/category")
def category():
    session_id = get_session_id()
    log_request(session_id, "category")
    return create_response("category/index.html", session_id)


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)