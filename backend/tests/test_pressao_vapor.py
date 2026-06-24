import pytest
import math
from models.irrigacao import CalculadorIrrigacao

def test_calcular_e_circulo_ponto():
    calc = CalculadorIrrigacao()
    # Test for 20 degrees Celsius
    t = 20.0
    expected = 0.6108 * math.exp((17.27 * t) / (t + 273.3))
    result = calc.calcular_e_circulo_ponto(t)
    assert math.isclose(result, expected, rel_tol=1e-4)

def test_calcular_pressao_saturacao_es():
    calc = CalculadorIrrigacao()
    assert calc.calcular_pressao_saturacao_es(30.0, 20.0) == 2.6771

def test_calcular_pressao_atual_ea():
    calc = CalculadorIrrigacao()
    assert calc.calcular_pressao_atual_ea(3.5, 60.0) == 2.1000

def test_calcular_deficit_vapor():
    calc = CalculadorIrrigacao()
    assert calc.calcular_deficit_vapor(3.5, 2.1) == 1.4000
