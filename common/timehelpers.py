from datetime import datetime, timedelta

def currentTimestamp():
    now = datetime.now() + timedelta(hours=3)
    return int(round(now.timestamp() * 1000))
