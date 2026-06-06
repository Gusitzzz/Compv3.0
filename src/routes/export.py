def export_routes(app):
    from flask import render_template, redirect, url_for, session, request, send_file, flash
    from src.models.database import get_history, get_filtered_history
    from src.services.export import export_filtered, export_all
    from datetime import datetime
    
    @app.route('/export/', methods=['POST'])
    def export_page():
        if 'user' not in session: return redirect(url_for('login_page'))
        try:
            import openpyxl
        except:
            import os
            os.system('pip install openpyxl')
            import openpyxl
        
        tgl = request.form.get('tanggal') or datetime.now().strftime('%Y-%m-%d')
        jm, js = request.form.get('jam_mulai','00:00'), request.form.get('jam_selesai','23:59')
        
        data = get_filtered_history(tgl, jm, js)
        if not data:
            data = get_history(100)
        if not data:
            flash('Tidak ada data untuk filter tersebut', 'warning')
            return redirect('/database/')
        
        fname = export_filtered(data, tgl, jm, js)
        return send_file(fname, as_attachment=True, download_name=fname)
    
    @app.route('/db_export/')
    def db_export():
        if 'user' not in session: return redirect(url_for('login_page'))
        data = get_history(10000)
        fname = export_all(data)
        return send_file(fname, as_attachment=True, download_name=fname)