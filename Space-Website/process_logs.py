import pandas as pd

# Load logs
df = pd.read_csv("logs.csv", header=None)

# Add column names
df.columns = ["session_id", "page", "timestamp", "ip", "user_agent"]

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Sort by session + time
df = df.sort_values(by=["session_id", "timestamp"])

# Group by session
sessions = []

for session_id, group in df.groupby("session_id"):
    pages = len(group)

    time_diff = (group["timestamp"].max() - group["timestamp"].min()).total_seconds()
    
    avg_time = time_diff / pages if pages > 0 else 0
    pages_per_min = pages / (time_diff / 60) if time_diff > 0 else pages

    sessions.append([session_id, pages, avg_time, pages_per_min])

# Create new dataframe
final_df = pd.DataFrame(sessions, columns=[
    "session_id", "pages_visited", "avg_time", "pages_per_min"
])

# Save structured dataset
final_df.to_csv("dataset.csv", index=False)

print("✅ Dataset created: dataset.csv")