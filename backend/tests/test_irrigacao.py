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

def test_perda_conector_lateral():
    calc = CalculadorIrrigacao()
    # Valores de exemplo: diam=0.016, comp=0.05, vel_con=1.5, vel_lat=1.0
    # hfl_l = 2.268121 * (0.016 ** 0.106) * (0.05 ** 1.057) * (1.5 ** 1.766) * (1.0 ** 0.386)
    # 0.016**0.106 ~= 0.648
    # 0.05**1.057 ~= 0.0426
    # 1.5**1.766 ~= 2.046
    # 1.0**0.386 = 1.0
    # 2.268121 * 0.648 * 0.0426 * 2.046 ~= 0.126
    perda = calc.perda_conector_lateral(0.016, 0.05, 1.5, 1.0)
    assert isinstance(perda, float)
    assert round(perda, 3) == 0.126

def test_calcular_pressao_inicial_bomba():
    calc = CalculadorIrrigacao()
    # pressao_emissor = 10.0
    # perda_tubulacao = 2.0
    # hfl_l calculada acima = 0.126
    # pressao_inicial = 10.0 + 2.0 + 0.126 = 12.126
    pressao = calc.calcular_pressao_inicial_bomba(10.0, 2.0, 0.016, 0.05, 1.5, 1.0)
    assert isinstance(pressao, float)
    assert round(pressao, 3) == 12.126
