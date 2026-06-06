from flask import request, jsonify
from config import API_KEY

def receive_data(app_units):
    from flask import request, jsonify
    from src.utils.datetime import get_now_str
    from src.core.calculator import calc_status
    from src.models.database import save_reading, load_thresholds, load_correction, save_alarm
    
    api_key = request.headers.get('X-API-Key')
    if api_key != API_KEY:
        return jsonify({'error': 'Unauthorized'}), 401
    
    d = request.get_json() or {}
    unit = d.get('unit', 'Unknown')
    raw_temp = float(d.get('temperature', 0))
    raw_vib = float(d.get('vibration', 0))
    raw_noise = float(d.get('noise', 0))
    
    corr = load_correction()
    thr = load_thresholds()
    c_u = corr.get(unit, {'temp':1, 'vib':1, 'noise':1})
    
    ctemp = round(raw_temp * c_u['temp'], 1)
    cvib = round(raw_vib * c_u['vib'], 1)
    cnoise = round(raw_noise * c_u['noise'], 1)
    status = calc_status(ctemp, cvib, cnoise, thr)
    now_str = get_now_str()
    
    save_reading(unit, ctemp, cvib, cnoise, status, now_str)
    
    if unit in app_units:
        app_units[unit] = {'temp':ctemp, 'vib':cvib, 'noise':cnoise, 'status':status, 'online':True}
    
    if status == "Gawat":
        save_alarm(now_str, unit, "Multiple", max(ctemp,cvib,cnoise), f"T={ctemp},V={cvib},N={cnoise}")
    
    return jsonify({'success': True, 'status': status})