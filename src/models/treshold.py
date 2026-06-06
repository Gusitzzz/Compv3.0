import sqlite3
from config import DB_NAME, DB_TIMEOUT, DEFAULT_THRESHOLDS
from src.core.security import db_lock

def load_thresholds():
    with db_lock:
        conn = sqlite3.connect(DB_NAME, timeout=DB_TIMEOUT)
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT key, value FROM app_thresholds").fetchall()
        conn.close()
        return {r['key']: float(r['value']) for r in rows} or DEFAULT_THRESHOLDS

def load_correction():
    with db_lock:
        conn = sqlite3.connect(DB_NAME, timeout=DB_TIMEOUT)
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT unit, param, value FROM app_correction").fetchall()
        conn.close()
        r = {'Unit 1': {'temp':1,'vib':1,'noise':1}, 'Unit 2': {'temp':1,'vib':1,'noise':1}, 'Unit 3': {'temp':1,'vib':1,'noise':1}}
        for ro in rows:
            if ro['unit'] in r: r[ro['unit']][ro['param']] = float(ro['value'])
        return r