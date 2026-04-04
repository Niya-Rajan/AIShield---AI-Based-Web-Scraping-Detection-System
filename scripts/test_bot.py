import requests
import time

BASE_URL = "http://127.0.0.1:5000"

# SAME SESSION (IMPORTANT)
SESSION_ID = "a943eacf-a738-4bb0-af2a-1161f379c45a"

session = requests.Session()
session.cookies.set("session_id", SESSION_ID)

headers = {
    "User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"
}

routes = [
    "/",
    "/mars",
    "/blackholes",
    "/artemis",
    "/category"
]

# simulate fast bot behavior
for i in range(15):
    for route in routes:
        session.get(BASE_URL + route, headers=headers)
        time.sleep(0.1)   # fast → bot-like