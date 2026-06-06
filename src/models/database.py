import sqlite3
from config import DB_NAME, DB_TIMEOUT, DEFAULT_THRESHOLDS

def get_db():
    conn = sqlite3.connect(DB_NAME, timeout=DB_TIMEOUT)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    from src.core.security import db_lock
    with db_lock:
        conn = get_db()
        conn.execute('''CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY, unit TEXT, temperature REAL, vibration REAL,
            noise REAL, status TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS app_users (
            username TEXT PRIMARY KEY, password_hash TEXT, level TEXT DEFAULT 'operator')''')
        conn.execute('''CREATE TABLE IF NOT EXISTS app_thresholds (
            key TEXT PRIMARY KEY, value REAL)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS app_correction (
            unit TEXT, param TEXT, value REAL DEFAULT 1.0, PRIMARY KEY (unit, param))''')
        conn.execute('''CREATE TABLE IF NOT EXISTS alarm_history (
            id INTEGER PRIMARY KEY, time TEXT, unit TEXT, param TEXT, val REAL, msg TEXT)''')
        conn.commit()
        
        if not conn.execute("SELECT 1 FROM app_users WHERE username='admin'").fetchone():
            from werkzeug.security import generate_password_hash
            conn.execute("INSERT INTO app_users VALUES (?,?,?)", ('admin', generate_password_hash('admin'), 'admin'))
            conn.execute("INSERT INTO app_users VALUES (?,?,?)", ('operator', generate_password_hash('1234'), 'operator'))
        for k, v in DEFAULT_THRESHOLDS.items():
            conn.execute("INSERT OR IGNORE INTO app_thresholds VALUES (?,?)", (k, v))
        for u in ['Unit 1', 'Unit 2', 'Unit 3']:
            for p in ['temp', 'vib', 'noise']:
                conn.execute("INSERT OR IGNORE INTO app_correction VALUES (?,?,1.0)", (u, p))
        conn.commit()
        conn.close()
    print("Database initialized")

def save_reading(unit, temp, vib, noise, status, ts):
    from src.core.security import db_lock
    with db_lock:
        conn = None
        try:
            conn = get_db()
            conn.execute("INSERT INTO sensor_readings (unit, temperature, vibration, noise, status, timestamp) VALUES (?,?,?,?,?,?)", (unit, temp, vib, noise, status, ts))
            conn.commit()
        except Exception as e:
            print(f"Error saving reading: {e}")
        finally:
            if conn:
                conn.close()

def save_alarm(time_str, unit, param, val, msg):
    from src.core.security import db_lock
    with db_lock:
        conn = None
        try:
            conn = get_db()
            conn.execute("INSERT INTO alarm_history (time, unit, param, val, msg) VALUES (?,?,?,?,?)", (time_str, unit, param, val, msg))
            conn.commit()
        except Exception as e:
            print(f"Error saving alarm: {e}")
        finally:
            if conn:
                conn.close()

def get_filtered_history(tanggal, jam_mulai, jam_selesai):
    from src.core.security import db_lock
    with db_lock:
        conn = get_db()
        rows = conn.execute(
            "SELECT id, unit, temperature, vibration, noise, status, timestamp FROM sensor_readings "
            "WHERE date(timestamp)=date(?) AND time(timestamp)>=time(?) AND time(timestamp)<=time(?) "
            "ORDER BY timestamp ASC",
            (tanggal, jam_mulai, jam_selesai)
        ).fetchall()
        conn.close()
        return [dict(row) for row in rows]


def get_history(limit=500):
    from src.core.security import db_lock
    with db_lock:
        conn = get_db()
        rows = conn.execute("SELECT * FROM sensor_readings ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        conn.close()
        return [dict(row) for row in rows]

def get_alarm_history(limit=500):
    from src.core.security import db_lock
    with db_lock:
        conn = get_db()
        rows = conn.execute("SELECT * FROM alarm_history ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        conn.close()
        return [dict(row) for row in rows]

def load_thresholds():
    from src.core.security import db_lock
    with db_lock:
        conn = get_db()
        rows = conn.execute("SELECT key, value FROM app_thresholds").fetchall()
        conn.close()
        return {r['key']: float(r['value']) for r in rows} or DEFAULT_THRESHOLDS

def load_correction():
    from src.core.security import db_lock
    with db_lock:
        conn = get_db()
        rows = conn.execute("SELECT unit, param, value FROM app_correction").fetchall()
        conn.close()
        r = {'Unit 1': {'temp':1,'vib':1,'noise':1}, 'Unit 2': {'temp':1,'vib':1,'noise':1}, 'Unit 3': {'temp':1,'vib':1,'noise':1}}
        for ro in rows:
            if ro['unit'] in r: r[ro['unit']][ro['param']] = float(ro['value'])
        return r

def load_users():
    from src.core.security import db_lock
    with db_lock:
        conn = get_db()
        rows = conn.execute("SELECT username, password_hash, level FROM app_users").fetchall()
        conn.close()
        return {u['username']: {'password_hash': u['password_hash'], 'level': u['level']} for u in rows}