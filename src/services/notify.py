from src.core.simulator import pending_notif, pending_notif_lock

def get_notifications():
    with pending_notif_lock:
        notifs = list(pending_notif)
        pending_notif.clear()
    return notifs

def push_notification(unit, status, temp, vib, noise, time_str):
    with pending_notif_lock:
        pending_notif.append({
            "unit": unit,
            "status": status,
            "temp": temp,
            "vib": vib,
            "noise": noise,
            "time": time_str
        })
        if len(pending_notif) > 20:
            pending_notif[:] = pending_notif[-20:]