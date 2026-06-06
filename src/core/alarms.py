def save_alarm(time_str, unit, param, val, msg):
    from src.models.database import save_alarm as db_save_alarm
    db_save_alarm(time_str, unit, param, val, msg)