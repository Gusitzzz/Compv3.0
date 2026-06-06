import sqlite3
from config import DB_NAME, DB_TIMEOUT
from src.core.security import db_lock

def save_reading(unit, temp, vib, noise, status, ts):
    from src.core.security import db_lock
    with db_lock:
        conn = None
        try:
            conn = sqlite3.connect(DB_NAME, timeout=DB_TIMEOUT)
            conn.execute("INSERT INTO sensor_readings (unit, temperature, vibration, noise, status, timestamp) VALUES (?,?,?,?,?,?)", (unit, temp, vib, noise, status, ts))
            conn.commit()
        except Exception as e:
            print(f"Error saving reading: {e}")
        finally:
            if conn:
                conn.close()