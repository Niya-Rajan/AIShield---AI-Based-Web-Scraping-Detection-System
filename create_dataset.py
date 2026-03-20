import pandas as pd
import numpy as np
import random

# Add noise (10–15%)
if random.random() < 0.15:
    label = 1 - label

# ---------------- LOAD LOGS ----------------
df = pd.read_csv("logs.csv")

# Clean column names
df.columns = df.columns.str.strip()

# ---------------- FIX TIMESTAMP ----------------
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# Drop invalid rows
df = df.dropna(subset=["timestamp"])

# Convert to seconds
df["timestamp"] = df["timestamp"].astype("int64") // 10**9

# ---------------- SORT ----------------
df = df.sort_values(by=["session_id", "timestamp"])

dataset = []

# ---------------- SESSION PROCESSING ----------------
for session_id, group in df.groupby("session_id"):

    group = group.sort_values(by="timestamp")
    pages = len(group)

    # Skip very small sessions
    if pages < 2:
        continue

    timestamps = group["timestamp"].values

    duration = timestamps[-1] - timestamps[0]
    duration = max(duration, 5)   #FIXED (important)

    # ---------------- FEATURES ----------------
    avg_time = duration / (pages - 1)
    pages_per_min = (pages / duration) * 60
    unique_pages = group["page"].nunique()

    intervals = np.diff(timestamps)

    if len(intervals) == 0:
        continue

    request_interval_mean = np.mean(intervals)
    request_interval_std = np.std(intervals)

    repeat_ratio = 1 - (unique_pages / pages)

    # ---------------- USER AGENT ----------------
    ua = str(group["user_agent"].iloc[0]).lower()

    if "bot" in ua or "crawl" in ua:
        ua_flag = 1
    else:
        ua_flag = 0

    # ---------------- FINAL LABEL LOGIC ----------------
    if (
        ua_flag == 1 or                     # known bots
        pages_per_min > 60 or              # extremely fast
        (pages > 8 and request_interval_std < 0.3)  # very consistent pattern
    ):
        label = 1   # BOT
    else:
        label = 0   # HUMAN

    dataset.append([
        session_id,
        pages,
        duration,
        avg_time,
        pages_per_min,
        unique_pages,
        repeat_ratio,
        request_interval_mean,
        request_interval_std,
        ua_flag,
        label
    ])

# ---------------- CREATE DATASET ----------------
final_df = pd.DataFrame(dataset, columns=[
    "session_id",
    "pages_visited",
    "session_duration",
    "avg_time_per_page",
    "pages_per_min",
    "unique_pages",
    "repeat_ratio",
    "request_interval_mean",
    "request_interval_std",
    "ua_flag",
    "label"
])

# ---------------- SAVE ----------------
final_df.to_csv("dataset.csv", index=False)

print("✅ dataset.csv created successfully!")

print("\n📊 Label distribution:")
print(final_df["label"].value_counts())

print("\n🔍 Sample data:")
print(final_df.head())