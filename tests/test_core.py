
def test_status_normal():
    from src.core.calculator import calc_status
    assert calc_status(50, 20, 60, {'temp_max':85,'vib_max':40,'noise_max':80}) == 'Normal'

def test_status_warning():
    from src.core.calculator import calc_status
    assert calc_status(80, 35, 75, {'temp_max':85,'vib_max':40,'noise_max':80}) == 'Perlu_Cek'

def test_status_danger():
    from src.core.calculator import calc_status
    assert calc_status(90, 50, 90, {'temp_max':85,'vib_max':40,'noise_max':80}) == 'Gawat'