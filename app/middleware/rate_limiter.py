import time

cache_data = {}

async def rate_limiter(user_id: str, window: int = 60, max_requests: int = 10):
    current_time = time.time()

    expired_keys = [k for k, v in cache_data.items() if current_time - v["time"] > window]
    for k in expired_keys:
        del cache_data[k]

    if user_id in cache_data:
        data = cache_data[user_id]
        if data["count"] >= max_requests:
            return False
        else:
            data["count"] += 1
            data["time"] = current_time
    else:
        cache_data[user_id] = {"count": 1, "time": current_time}

    return True
