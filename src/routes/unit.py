def unit_routes(app, units):
    from flask import render_template, redirect, url_for, session
    from src.models.database import get_db
    
    @app.route('/unit/<name>/')
    def detail(name):
        if 'user' not in session: return redirect(url_for('login_page'))
        if name not in ["Unit 1", "Unit 2", "Unit 3"]: return redirect(url_for('dashboard'))
        
        conn = get_db()
        rows = conn.execute("SELECT timestamp, temperature, vibration, noise FROM sensor_readings WHERE unit=? ORDER BY timestamp DESC LIMIT 24", (name,)).fetchall()
        conn.close()
        rows = list(reversed(rows)) if rows else []
        
        return render_template('dashboard/detail.html', 
            unit_name=name, 
            data=units.get(name,{}), 
            labels=[str(r['timestamp'])[11:16] for r in rows],
            temp_data=[r['temperature'] for r in rows],
            vib_data=[r['vibration'] for r in rows],
            noise_data=[r['noise'] for r in rows],
            title=name)