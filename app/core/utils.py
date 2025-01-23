from datetime import datetime, timezone


def get_now_utc():
    return datetime.now(tz=timezone.utc)
