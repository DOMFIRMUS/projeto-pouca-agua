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

def test_calcular_kl():
    calc = CalculadorIrrigacao()
    # Test Keller
    assert calc.calcular_kl('Keller', 0.5) == round(0.5 + 0.15 * (1 - 0.5), 2)
    # Test Bernardo
    assert calc.calcular_kl('Bernardo', 0.5) == 0.5
    # Test Fereres
    assert calc.calcular_kl('Fereres', 0.70) == 1.0
    assert calc.calcular_kl('Fereres', 0.50) == round((1.09 * 0.50) + 0.30, 2)
    assert calc.calcular_kl('Fereres', 0.15) == round((1.94 * 0.15) + 0.10, 2)
    # Test Keller_Bliesner
    assert calc.calcular_kl('Keller_Bliesner', 0.25) == round(0.10 * 5.0, 2)  # sqrt(25) = 5
    # Test Fallback
    assert calc.calcular_kl('Desconhecido', 0.5) == 1.0

def test_calcular_etc():
    calc = CalculadorIrrigacao()
    # etc = eto * kc * kl
    # 5.0 * 1.2 * 0.8 = 4.8
    assert calc.calcular_etc(5.0, 1.2, 0.8) == 4.8
    # Com KL padrão de 1.0
    # 4.0 * 1.1 * 1.0 = 4.4
    assert calc.calcular_etc(4.0, 1.1) == 4.4
