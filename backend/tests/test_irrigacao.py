import sys
import os

# Add the backend directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.irrigacao import CalculadorIrrigacao

def test_avaliar_status_solo_critico():
    calc = CalculadorIrrigacao()
    resultado = calc.avaliar_status_solo(30.0)
    assert resultado["status"] == "Crítico (Seco)"
    assert resultado["irrigar"] is True

def test_avaliar_status_solo_moderado():
    calc = CalculadorIrrigacao()
    resultado = calc.avaliar_status_solo(50.0)
    assert resultado["status"] == "Moderado"
    assert resultado["irrigar"] is True

def test_avaliar_status_solo_ideal():
    calc = CalculadorIrrigacao()
    resultado = calc.avaliar_status_solo(70.0)
    assert resultado["status"] == "Ideal"
    assert resultado["irrigar"] is False

def test_avaliar_status_solo_encharcado():
    calc = CalculadorIrrigacao()
    resultado = calc.avaliar_status_solo(90.0)
    assert resultado["status"] == "Encharcado"
    assert resultado["irrigar"] is False

def test_calcular_eto_blaney_criddle():
    calc = CalculadorIrrigacao()
    # t_media = 25, mes_index = 1
    # P for Jan is 25
    # ETo = (0.457 * 25 + 8.13) * (25 / 100) = (11.425 + 8.13) * 0.25 = 19.555 * 0.25 = 4.88875 -> 4.89
    eto = calc.calcular_eto_blaney_criddle(25, 1)
    assert eto == 4.89

def test_calcular_eto_hargreaves():
    calc = CalculadorIrrigacao()
    # ETo para Janeiro (mes_index = 1), Tmax=30, Tmin=20
    # Tmedia = 25. Ra = 42.2
    # ETo = 0.0023 * 42.2 * 0.408 * (25 + 17.8) * sqrt(10)
    eto = calc.calcular_eto_hargreaves(30, 20, -22, 1)
    assert isinstance(eto, float)
    assert eto > 0

def test_calcular_irn_e_cad():
    calc = CalculadorIrrigacao()
    # to_cc=0.3, to_pmp=0.15, z=0.4, f=0.5, fw_percent=100
    # cad = 1000 * (0.3 - 0.15) * 0.4 = 60
    # irn_max = 60 * 0.5 * 1.0 = 30
    cad, irn_max = calc.calcular_irn_e_cad(0.3, 0.15, 0.4, 0.5, 100)
    assert cad == 60.0
    assert irn_max == 30.0

def test_calcular_fator_obstrucao():
    calc = CalculadorIrrigacao()

    # Test 'online'
    # IO = 5 / 10 = 0.5
    # KL = 1.935 * (0.5 ** 0.595) = 1.2811
    kl_online = calc.calcular_fator_obstrucao('online', 10.0, 5.0)
    assert round(kl_online, 4) == 1.2811

    # Test 'pastilha'
    # IO = 5 / 10 = 0.5
    # KL = 1.383 * (0.5 ** 0.576) = 0.9277
    kl_pastilha = calc.calcular_fator_obstrucao('pastilha', 10.0, 5.0)
    assert round(kl_pastilha, 4) == 0.9277

    # Test 'bobi'
    # IO = 5 / 10 = 0.5
    # KL = 1.230 * (0.5 ** 0.510) = 0.8637
    kl_bobi = calc.calcular_fator_obstrucao('bobi', 10.0, 5.0)
    assert round(kl_bobi, 4) == 0.8637

    # Test unknown
    kl_unknown = calc.calcular_fator_obstrucao('unknown', 10.0, 5.0)
    assert kl_unknown == 0.0

    # Test zero area_tubo
    kl_zero = calc.calcular_fator_obstrucao('online', 0.0, 5.0)
    assert kl_zero == 0.0

def test_calcular_perda_carga_total():
    calc = CalculadorIrrigacao()
    # f_tubo=0.02, L=100, D=0.016, V=1.5
    # tipo_emissor='online', area_tubo=200, area_emissor=20
    # IO = 0.1
    # kl_online = 1.935 * (0.1 ** 0.595) = 0.4917
    # hf = (0.02 + 0.4917) * (100 / 0.016) * (1.5 ** 2) / (2 * 9.81)
    # hf = 0.5117 * 6250 * 2.25 / 19.62 = 366.7576 (rounded differently above)

    hf = calc.calcular_perda_carga_total(0.02, 100, 0.016, 1.5, 'online', 200, 20)
    assert round(hf, 4) == 366.7575

    # Test D = 0
    hf_zero = calc.calcular_perda_carga_total(0.02, 100, 0.0, 1.5, 'online', 200, 20)
    assert hf_zero == 0.0

def test_calcular_turno_rega_max():
    calc = CalculadorIrrigacao()
    # irn_max_mm=13.0, etc_mm_dia=5.0, sp_m=0.5, sr_m=1.0
    # TR_max = floor(13.0 / (5.0 * 0.5 * 1.0)) = floor(13.0 / 2.5) = floor(5.2) = 5
    tr_max = calc.calcular_turno_rega_max(13.0, 5.0, 0.5, 1.0)
    assert tr_max == 5

    # Caso com valores zerados para etc_mm_dia, sp_m ou sr_m
    tr_max_zero = calc.calcular_turno_rega_max(13.0, 0, 0.5, 1.0)
    assert tr_max_zero == 0
