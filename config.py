SECRET_KEY = 'ammonia_secret_key_2026'
APP_NAME = "Ammonia Compressor Monitoring"
VERSION = "1.0.0"
DEBUG = True

LANGUAGES = ['en', 'id', 'zh']

SIMULATION_INTERVAL = 5
SIMULATION_RUNNING = True

DB_NAME = "ammonia_monitor.db"
DB_TIMEOUT = 30

API_KEY = "ammonia_secret_key_2026"

SESSION_TIMEOUT = 30
MAX_LOGIN_ATTEMPTS = 3
LOCKOUT_DURATION = 5
PASSWORD_MIN_LENGTH = 6

DEFAULT_THRESHOLDS = {'temp_max': 85.0, 'vib_max': 40.0, 'noise_max': 80.0}