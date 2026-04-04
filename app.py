from flask import Flask, render_template, request, make_response
import csv
import uuid
from datetime import datetime
from collections import defaultdict
import os
import json

# 🔥 IMPORT MODULES
from engine.fake_engine import smart_fake
from engine.feature_extractor import extract_features
from engine.detector import predict_bot

app = Flask(__name__)

# ---------------- PATHS ----------------
LOGS_PATH = "data/logs.csv"
BOT_LOGS_PATH = "data/bot_logs.csv"

# ---------------- SESSION STORAGE ----------------
user_sessions = defaultdict(list)
detected_bots = {}

# ---------------- CREATE LOG FILES ----------------
os.makedirs("data", exist_ok=True)

if not os.path.exists(LOGS_PATH):
    with open(LOGS_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "session_id", "page", "timestamp", "ip", "user_agent"
        ])

if not os.path.exists(BOT_LOGS_PATH):
    with open(BOT_LOGS_PATH, "w", newline="") as f:
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
    with open(BOT_LOGS_PATH, "a", newline="") as f:
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

# ---------------- ML DETECTION ----------------
def log_request(session_id, page):
    timestamp = datetime.now()

    # Save logs
    with open(LOGS_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            session_id,
            page,
            timestamp,
            request.remote_addr,
            request.headers.get("User-Agent")
        ])

    # Track session
    user_sessions[session_id].append((timestamp, page))

    # Extract features
    features = extract_features(user_sessions[session_id])

    if not features:
        return

    prediction = predict_bot(features)

    print("FEATURES:", features)
    print("PREDICTION:", prediction)

    last_flag_time = detected_bots.get(session_id)

    # Stable detection
    if prediction == 1 and (
        session_id not in detected_bots or
        (last_flag_time and (datetime.now() - last_flag_time).seconds > 30)
    ):
        detected_bots[session_id] = datetime.now()

        session_data = user_sessions[session_id]
        times = [t[0] for t in session_data]
        pages = len(times)

        time_diff = max((times[-1] - times[0]).total_seconds(), 0.1)
        avg_time = time_diff / (pages - 1)
        ppm = pages / (time_diff / 60)

        log_bot(
            session_id,
            request.remote_addr,
            request.headers.get("User-Agent"),
            pages,
            time_diff,
            avg_time,
            ppm
        )

# ---------------- MIDDLEWARE ----------------
@app.after_request
def modify_response(response):
    try:
        session_id = request.cookies.get("session_id")

        if not session_id:
            return response

        if response.content_type.startswith("text/html"):

            if session_id in detected_bots:

                bot_time = detected_bots[session_id]
                time_diff = (datetime.now() - bot_time).total_seconds()

                if time_diff < 30:
                    print("FAKE CONTENT APPLIED")
                    content = response.get_data(as_text=True)

                    # 🔥 Apply fake transformation
                    content = smart_fake(content)

                    response.set_data(content)
                else:
                    detected_bots.pop(session_id, None)

    except Exception as e:
        print("Middleware Error:", e)

    return response

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

@app.route("/admin", methods=["GET", "POST"])
def admin():
    rules_path = "config/rules.json"

    # Load existing rules
    with open(rules_path, "r") as f:
        rules = json.load(f)

    if request.method == "POST":
        word = request.form.get("word").lower()
        replacement = request.form.get("replacement")

        # Add / Update rule
        rules[word] = replacement

        with open(rules_path, "w") as f:
            json.dump(rules, f, indent=4)

    return render_template("admin.html", rules=rules)

# ---------------- HONEYPOT ----------------
@app.route("/admin-secret")
def trap():
    print("🚨 BOT TRAPPED:", request.remote_addr)
    return "Access Logged"

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)