def user_routes(app):
    from flask import render_template, redirect, url_for, session, request, flash
    from werkzeug.security import generate_password_hash
    from src.models.user import load_users
    
    @app.route('/users/', methods=['GET', 'POST'])
    def manage_users():
        if 'user' not in session or session.get('level') != 'admin': 
            return redirect(url_for('dashboard'))
        
        if request.method == 'POST':
            from src.models.database import get_db
            conn = get_db()
            
            if 'register' in request.form:
                nu, np = request.form.get('new_username','').strip(), request.form.get('new_password','')
                if nu and np and nu != 'admin' and not conn.execute("SELECT 1 FROM app_users WHERE username=?", (nu,)).fetchone():
                    conn.execute("INSERT INTO app_users VALUES (?,?,?)", (nu, generate_password_hash(np), 'operator'))
                    flash(f'User {nu} added', 'success')
            
            if 'delete' in request.form:
                du = request.form.get('delete_username','')
                if du and du != 'admin' and du != session.get('user'):
                    conn.execute("DELETE FROM app_users WHERE username=?", (du,))
            
            conn.commit()
            conn.close()
        
        return render_template('admin/users.html', users=load_users(), title="Users")