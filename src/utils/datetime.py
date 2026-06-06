from datetime import datetime, timedelta

def get_now_str():
    return (datetime.utcnow() + timedelta(hours=7)).strftime('%Y-%m-%d %H:%M:%S')