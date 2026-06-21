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
    assert resultado["status"] == "Moderado (Necessita Atenção)"
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

def test_calcular_tempo_irrigacao_nao_necessario():
    calc = CalculadorIrrigacao()
    tempo = calc.calcular_tempo_irrigacao(70.0)
    assert tempo == 0

def test_calcular_tempo_irrigacao_necessario():
    calc = CalculadorIrrigacao()
    tempo = calc.calcular_tempo_irrigacao(50.0, 2.0, 0.3)
    # deficit = 60 - 50 = 10
    # tempo = (10 * 1.5) / (2.0 * 0.3) = 15 / 0.6 = 25.0
    assert tempo == 25.0

def test_calcular_tempo_irrigacao_minimo():
    calc = CalculadorIrrigacao()
    tempo = calc.calcular_tempo_irrigacao(59.0, 2.0, 0.3)
    # deficit = 60 - 59 = 1
    # tempo = (1 * 1.5) / (2.0 * 0.3) = 1.5 / 0.6 = 2.5
    # should be max(2.5, 5) = 5
    assert tempo == 5.0
