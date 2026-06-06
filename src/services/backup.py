import shutil
import os
from datetime import datetime

def backup_database():
    from config import DB_NAME
    if os.path.exists(DB_NAME):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"ammonia_backup_{timestamp}.db"
        shutil.copy(DB_NAME, f"backups/{backup_name}")
        return backup_name
    return None

def restore_database(backup_file):
    from config import DB_NAME
    if os.path.exists(f"backups/{backup_file}"):
        shutil.copy(f"backups/{backup_file}", DB_NAME)
        return True
    return False