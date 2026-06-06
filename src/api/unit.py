def unit_data(name, app_units):
    from flask import jsonify
    from src.models.database import get_db
    
    conn = get_db()
    rows = conn.execute("SELECT timestamp, temperature, vibration, noise FROM sensor_readings WHERE unit=? ORDER BY timestamp DESC LIMIT 24", (name,)).fetchall()
    conn.close()
    rows = list(reversed(rows))
    return jsonify({
        'labels': [str(r['timestamp'])[11:16] for r in rows],
        'temp_data': [r['temperature'] for r in rows],
        'vib_data': [r['vibration'] for r in rows],
        'noise_data': [r['noise'] for r in rows],
        'current': app_units.get(name, {"temp":0,"vib":0,"noise":0,"status":"Normal","online":False})
    })