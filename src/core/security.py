import threading

db_lock = threading.Lock()

def is_admin():
    from flask import session
    from src.models.user import load_users
    return load_users().get(session.get('user', ''), {}).get('level') == 'admin'