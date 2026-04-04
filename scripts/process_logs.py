import pandas as pd

# Load logs
df = pd.read_csv("logs.csv", header=None)
df.columns = ["session_id", "page", "timestamp", "ip", "user_agent"]

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Sort
df = df.sort_values(by=["session_id", "timestamp"])

sessions = []

for session_id, group in df.groupby("session_id"):
    pages = len(group)

    time_diff = (group["timestamp"].max() - group["timestamp"].min()).total_seconds()

    if pages < 2:
        continue

    session_duration = time_diff
    avg_time = time_diff / pages if pages > 0 else 0
    pages_per_min = pages / (time_diff / 60) if time_diff > 0 else pages

    # 🚨 LABEL LOGIC
    if pages_per_min > 20 or avg_time < 2:
        label = 1   # BOT
    else:
        label = 0   # HUMAN

    sessions.append([
        session_id,
        pages,
        session_duration,
        avg_time,
        pages_per_min,
        label
    ])

# Create dataset
final_df = pd.DataFrame(sessions, columns=[
    "session_id",
    "pages_visited",
    "session_duration",
    "avg_time_per_page",
    "pages_per_min",
    "label"
])

# Save
final_df.to_csv("dataset.csv", index=False)

print("✅ dataset.csv with labels created!")