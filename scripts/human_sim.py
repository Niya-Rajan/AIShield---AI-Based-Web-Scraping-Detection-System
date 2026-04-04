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

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"
]

# Increase human sessions (IMPORTANT)
for i in range(150):   # was 50 → now 150
    session = requests.Session()
    #session.cookies.set("session_id", str(uuid.uuid4()))

    headers = {
        "User-Agent": random.choice(user_agents)
    }

    # Slightly more pages
    num_pages = random.randint(4, 8)

    visited = set()

    for j in range(num_pages):
        url = random.choice(routes)

        if url in visited and random.random() < 0.5:
            continue

        visited.add(url)

        session.get(url, headers=headers)

        # Reduced delay (VERY IMPORTANT)
        time.sleep(random.uniform(1, 3))   # was 2–7

    # shorter break between sessions
    time.sleep(random.uniform(4, 10))