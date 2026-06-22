import math
from models.irrigacao import CalculadorIrrigacao

def test_calcular_pressao_atual_ea():
    calc = CalculadorIrrigacao()
    # If es = 2.677 and UR_m = 60%, then ea = 2.677 * (60 / 100) = 1.6062
    ea = calc.calcular_pressao_atual_ea(2.677, 60)
    assert round(ea, 3) == 1.606

def test_calcular_deficit_pressao_vapor():
    calc = CalculadorIrrigacao()
    deficit = calc.calcular_deficit_pressao_vapor(2.677, 1.606)
    assert round(deficit, 3) == 1.071
