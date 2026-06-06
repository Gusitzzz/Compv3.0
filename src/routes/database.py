def database_routes(app):
    from flask import render_template, redirect, url_for, session
    from src.models.database import get_history
    from datetime import datetime
    
    @app.route('/database/')
    def database_page():
        if 'user' not in session: return redirect(url_for('login_page'))
        return render_template('data/database.html', 
                               data=get_history(), 
                               title="Database", 
                               today=datetime.now().strftime('%Y-%m-%d'))