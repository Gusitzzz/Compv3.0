from werkzeug.security import check_password_hash
from src.models.user import load_users

def verify_login(username, password):
    users = load_users()
    if username in users and check_password_hash(users[username]['password_hash'], password):
        return True
    return False

def get_user_level(username):
    users = load_users()
    return users.get(username, {}).get('level', 'operator')