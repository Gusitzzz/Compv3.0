from flask import Flask, render_template, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash
import os, sys, threading, webbrowser, time
from datetime import datetime, timedelta
from config import SECRET_KEY, SESSION_TIMEOUT, API_KEY, SIMULATION_INTERVAL, SIMULATION_RUNNING

# App Setup
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=SESSION_TIMEOUT)

# Global units
units = {
    "Unit 1": {"temp": 0, "vib": 0, "noise": 0, "status": "Normal", "online": False},
    "Unit 2": {"temp": 0, "vib": 0, "noise": 0, "status": "Normal", "online": False},
    "Unit 3": {"temp": 0, "vib": 0, "noise": 0, "status": "Normal", "online": False},
}

# Import routes from src/routes/
from src.routes.auth import auth_routes
from src.routes.main import main_routes
from src.routes.unit import unit_routes
from src.routes.settings import settings_routes
from src.routes.users import user_routes
from src.routes.database import database_routes
from src.routes.export import export_routes
from src.routes.history import history_routes

# Register routes
auth_routes(app)
main_routes(app, units)
unit_routes(app, units)
settings_routes(app)
user_routes(app)
database_routes(app)
export_routes(app)
history_routes(app)

# API Routes
from src.api.data import receive_data
from src.api.refresh import refresh_data
from src.api.unit import unit_data

@app.route('/api/refresh_data/')
def api_refresh(): return refresh_data(units)

@app.route('/api/unit_data/<name>/')
def api_unit(name): return unit_data(name, units)

@app.route('/api/data/', methods=['POST'])
def api_data(): return receive_data(units)

@app.before_request
def before_request():
    from flask import session
    if 'lang' not in session:
        session['lang'] = 'id'

LANG = {
    'en': {
        'logged_in_as': 'Logged in as',
        'dashboard': 'Dashboard',
        'unit_menu': 'Unit',
        'system': 'System',
        'alarm_history': 'Alarm History',
        'database': 'Database',
        'settings': 'Settings',
        'users': 'User Admin',
        'logout': 'Logout',
        'online': 'Online',
        'offline': 'Offline',
        'real_time_monitoring': 'Real Time Monitoring',
        'back_to_dashboard': 'Back to Dashboard',
        'parameter_trend': 'Parameter Trend',
        'temperature': 'Temperature',
        'vibration': 'Vibration',
        'noise': 'Noise',
        'gawat': 'Bahaya',
        'perlu_cek': 'Perlu Cek',
        'normal': 'Normal',
        'total_units': 'Total Units',
        'active_alarms': 'Active Alarms',
        'view_details': 'View Details'
    },
    'id': {
        'logged_in_as': 'Logged sebagai',
        'dashboard': 'Dashboard',
        'unit_menu': 'Unit',
        'system': 'Sistem',
        'alarm_history': 'Riwayat Alarm',
        'database': 'Database',
        'settings': 'Pengaturan',
        'users': 'Kelola User',
        'logout': 'Keluar',
        'online': 'Online',
        'offline': 'Offline',
        'real_time_monitoring': 'Monitoring Realtime',
        'back_to_dashboard': 'Kembali ke Dashboard',
        'parameter_trend': 'Tren Parameter',
        'temperature': 'Suhu',
        'vibration': 'Getaran',
        'noise': 'Kebisingan',
        'gawat': 'BAHAYA',
        'perlu_cek': 'Perlu Cek',
        'normal': 'Normal',
        'total_units': 'Total Unit',
        'active_alarms': 'Alarm Aktif',
        'view_details': 'Lihat Detail'
    },
    'zh': {
        'logged_in_as': '登录为',
        'dashboard': '仪表板',
        'unit_menu': '单元',
        'system': '系统',
        'alarm_history': '警报历史',
        'database': '数据库',
        'settings': '设置',
        'users': '用户管理',
        'logout': '退出',
        'online': '在线',
        'offline': '离线',
        'real_time_monitoring': '实时监控',
        'back_to_dashboard': '返回仪表板',
        'parameter_trend': '参数趋势',
        'temperature': '温度',
        'vibration': '振动',
        'noise': '噪音',
        'gawat': '危险',
        'perlu_cek': '需要检查',
        'normal': '正常',
        'total_units': '总单元',
        'active_alarms': '活动警报',
        'view_details': '查看详情'
    }
}

@app.context_processor
def inject_t():
    def t(key):
        lang = session.get('lang', 'id')
        return LANG.get(lang, LANG['id']).get(key, key)
    return dict(t=t, units=units)

# Error handlers
@app.errorhandler(404)
def error_404(e): return render_template('error.html', code=404, message="Page not found"), 404

@app.errorhandler(500)
def error_500(e): return render_template('error.html', code=500, message="Server error"), 500

# Main
if __name__ == '__main__':
    base = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
    app.template_folder = os.path.join(base, 'templates')
    
    from src.models.database import init_db
    from src.core.simulator import run_simulation
    
    init_db()
    
    sim_thread = threading.Thread(target=run_simulation, args=(units,), daemon=True)
    sim_thread.start()
    
    print(f"\n{'='*50}")
    print("AMMONIA COMPRESSOR MONITORING SYSTEM")
    print(f"{'='*50}")
    print(f"http://localhost:5000")
    print(f"Login: admin / admin")
    print(f"{'='*50}\n")
    
    threading.Thread(target=lambda: (time.sleep(1.5), webbrowser.open_new("http://localhost:5000/")), daemon=True).start()
    
    app.run(host='0.0.0.0', port=5000, debug=False)