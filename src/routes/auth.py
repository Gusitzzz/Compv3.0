from flask import render_template, redirect, url_for, session, flash, request

def auth_routes(app):
    from flask import render_template, redirect, url_for, session, flash, request
    from src.services.auth import verify_login, get_user_level
    
    @app.route('/', methods=['GET', 'POST'])
    def login_page():
        if request.method == 'POST':
            u, p = request.form.get('username','').strip(), request.form.get('password','')
            if verify_login(u, p):
                session['user'] = u
                session['level'] = get_user_level(u)
                return redirect(url_for('dashboard'))
            flash('Invalid credentials', 'danger')
        
        return render_template('auth/login.html', title="Login")
    
    @app.route('/logout/')
    def logout():
        session.clear()
        return redirect(url_for('login_page'))