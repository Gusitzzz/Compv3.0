def refresh_data(app_units):
    from flask import jsonify
    from src.models.database import get_alarm_history
    from src.core.simulator import pending_notif, pending_notif_lock
    
    data = {u: {'temp':v['temp'], 'vib':v['vib'], 'noise':v['noise'], 'status':v['status']} for u, v in app_units.items()}
    c = {'total': len(app_units), 'alarms': sum(1 for u in app_units.values() if u['status']=='Gawat'), 'online': sum(1 for u in app_units.values() if u.get('online'))}
    
    with pending_notif_lock:
        notifs = list(pending_notif)
        pending_notif.clear()
    
    return jsonify({'units': data, 'total': c['total'], 'active_alarms': c['alarms'], 'online_count': c['online'], 'notifications': notifs})