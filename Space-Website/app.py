from flask import Flask, render_template, request, make_response
import csv
import uuid
from datetime import datetime

app = Flask(__name__)

# ---------------- LOGGING ----------------
def log_request(session_id, page):
    with open("logs.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            session_id,
            page,
            datetime.now(),
            request.remote_addr,
            request.headers.get("User-Agent")
        ])

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


if __name__ == "__main__":
    app.run(debug=True)