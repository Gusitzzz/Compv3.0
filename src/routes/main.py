def main_routes(app, units):
    from flask import render_template, redirect, url_for, session, request
    
    @app.route('/set_language/<lang>/')
    def set_language(lang):
        if lang in ['en', 'id', 'zh']:
            session['lang'] = lang
        return redirect(request.referrer or url_for('login_page'))
    
    @app.route('/dashboard/')
    def dashboard():
        if 'user' not in session: return redirect(url_for('login_page'))
        
        c_total = len(units)
        c_online = sum(1 for u in units.values() if u.get('online'))
        c_alarms = sum(1 for u in units.values() if u.get('status') == 'Gawat')
        
        return render_template(
            'dashboard/index.html',
            units=units,
            title="Dashboard",
            total_units_count=c_total,
            active_alarms_count=c_alarms,
            online_count=c_online
        )