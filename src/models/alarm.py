import sqlite3
from config import DB_NAME, DB_TIMEOUT

def save_alarm(time_str, unit, param, val, msg):
    from src.core.security import db_lock
    with db_lock:
        conn = None
        try:
            conn = sqlite3.connect(DB_NAME, timeout=DB_TIMEOUT)
            conn.execute("INSERT INTO alarm_history (time, unit, param, val, msg) VALUES (?,?,?,?,?)", (time_str, unit, param, val, msg))
            conn.commit()
        except Exception as e:
            print(f"Error saving alarm: {e}")
        finally:
            if conn:
                conn.close()