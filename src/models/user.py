import sqlite3
from werkzeug.security import generate_password_hash
from config import DB_NAME, DB_TIMEOUT
from src.core.security import db_lock
from config import DEFAULT_THRESHOLDS

def load_users():
    with db_lock:
        conn = sqlite3.connect(DB_NAME, timeout=DB_TIMEOUT)
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT username, password_hash, level FROM app_users").fetchall()
        conn.close()
        return {u['username']: {'password_hash': u['password_hash'], 'level': u['level']} for u in rows}