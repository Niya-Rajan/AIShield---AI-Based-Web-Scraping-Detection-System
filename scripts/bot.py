import requests
import uuid
import random
import time

routes = [
    "http://127.0.0.1:5000/",
    "http://127.0.0.1:5000/mars",
    "http://127.0.0.1:5000/blackholes",
    "http://127.0.0.1:5000/artemis",
    "http://127.0.0.1:5000/category"
]

for i in range(80):
    session = requests.Session()
    session.cookies.set("session_id", str(uuid.uuid4()))

    headers = {
        "User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"
    }

    pattern = routes.copy()
    random.shuffle(pattern)

    num_pages = random.randint(6, 12)

    delay = random.uniform(0.1, 0.8)

    # occasional aggressive bot
    if random.random() < 0.2:
        delay = random.uniform(0.01, 0.05)

    for j in range(num_pages):
        url = pattern[j % len(pattern)]
        session.get(url, headers=headers)
        time.sleep(delay)

    time.sleep(random.uniform(0.5, 2))