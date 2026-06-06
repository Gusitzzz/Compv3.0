def settings_routes(app):
    from flask import render_template, redirect, url_for, session, request, flash
    from src.models.database import load_thresholds, load_correction, get_db
    
    @app.route('/settings/', methods=['GET', 'POST'])
    def settings():
        if 'user' not in session or session.get('level') != 'admin': 
            return redirect(url_for('dashboard'))
        
        sel = request.args.get('unit', session.get('last_unit', 'Unit 1'))
        
        if request.method == 'POST':
            conn = get_db()
            if 'save_threshold' in request.form:
                for k in ['temp_max', 'vib_max', 'noise_max']:
                    conn.execute("INSERT OR REPLACE INTO app_thresholds VALUES (?,?)", (k, float(request.form.get(k, 85))))
            if 'save_corr' in request.form:
                u = request.form.get('unit_corr', sel)
                for p, f in [('temp','temp_corr'),('vib','vib_corr'),('noise','noise_corr')]:
                    conn.execute("INSERT OR REPLACE INTO app_correction VALUES (?,?,?)", (u, p, float(request.form.get(f, 1.0))))
            conn.commit()
            conn.close()
            flash('Saved!', 'success')
        
        session['last_unit'] = sel
        return render_template('admin/settings.html', thresholds=load_thresholds(), correction=load_correction(), selected_unit=sel, title="Settings")