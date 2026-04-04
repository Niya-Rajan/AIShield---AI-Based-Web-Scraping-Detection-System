def extract_features(session_data):
    times = [t[0] for t in session_data]
    pages = len(times)

    if pages < 2:
        return None

    time_diff = (times[-1] - times[0]).total_seconds()
    time_diff = max(time_diff, 0.1)

    avg_time = time_diff / (pages - 1)
    pages_per_min = pages / (time_diff / 60)

    return [[pages, time_diff, avg_time, pages_per_min]]