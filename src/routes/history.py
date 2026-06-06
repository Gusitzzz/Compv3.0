def history_routes(app):
    from flask import render_template, redirect, url_for, session
    from src.models.database import get_alarm_history
    
    @app.route('/history/')
    def history():
        if 'user' not in session: return redirect(url_for('login_page'))
        return render_template('data/history.html', logs=get_alarm_history(), title="History")