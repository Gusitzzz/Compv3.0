import time
import random
import threading
from datetime import datetime, timedelta
from config import SIMULATION_INTERVAL, SIMULATION_RUNNING
from src.core.calculator import calc_status

units_global = {}
alarm_log = []
pending_notif = []
pending_notif_lock = threading.Lock()

def get_now_str():
    return (datetime.utcnow() + timedelta(hours=7)).strftime('%Y-%m-%d %H:%M:%S')

def run_simulation(app_units):
    global units_global, alarm_log, pending_notif
    print(f"Simulation started - {SIMULATION_INTERVAL}s interval")
    
    while SIMULATION_RUNNING:
        try:
            now_str = get_now_str()
            from src.models.database import load_thresholds, load_correction, save_reading, save_alarm
            thr = load_thresholds()
            corr = load_correction()
            
            for unit_name in ["Unit 1", "Unit 2", "Unit 3"]:
                ctemp = round(random.randint(35,90) * corr[unit_name]['temp'], 1)
                cvib = round(random.randint(5,50) * corr[unit_name]['vib'], 1)
                cnoise = round(random.randint(50,90) * corr[unit_name]['noise'], 1)
                status = calc_status(ctemp, cvib, cnoise, thr)
                
                app_units[unit_name] = {'temp':ctemp, 'vib':cvib, 'noise':cnoise, 'status':status, 'online':True}
                save_reading(unit_name, ctemp, cvib, cnoise, status, now_str)
                
                if status == "Gawat":
                    val = max(ctemp, cvib, cnoise)
                    msg = f"Overthreshold: T={ctemp}, V={cvib}, N={cnoise}"
                    save_alarm(now_str, unit_name, "Multiple", val, msg)
                    alarm_log.insert(0, {"time":now_str, "unit":unit_name, "param":"Multiple", "val":val})
                    if len(alarm_log) > 200: alarm_log = alarm_log[:200]
                
                if status in ("Gawat", "Perlu_Cek"):
                    with pending_notif_lock:
                        pending_notif.append({
                            "unit": unit_name,
                            "status": status,
                            "temp": ctemp,
                            "vib": cvib,
                            "noise": cnoise,
                            "time": now_str
                        })
            
            print(f"[{now_str}] " + "  ".join([f"{u}={app_units[u]['temp']}°/{app_units[u]['status']}" for u in app_units]))
        except Exception as e:
            print(f"Sim error: {e}")
        time.sleep(SIMULATION_INTERVAL)