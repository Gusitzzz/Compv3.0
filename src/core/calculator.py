import random

def calc_status(temp, vib, noise, thr):
    tmax, vmax, nmax = thr.get('temp_max',85), thr.get('vib_max',40), thr.get('noise_max',80)
    if temp > tmax or vib > vmax or noise > nmax: return "Gawat"
    if temp > tmax*0.8 or vib > vmax*0.8 or noise > nmax*0.8: return "Perlu_Cek"
    return "Normal"

def get_random_value(param):
    return random.randint(*{'temp': (35,90), 'vib': (5,50), 'noise': (50,90)}[param])