import math
from models.irrigacao import CalculadorIrrigacao

def test_calcular_pressao_saturacao_es():
    calc = CalculadorIrrigacao()

    es = calc.calcular_pressao_saturacao_es(30, 20)
    assert round(es, 3) == 2.677

def test_calcular_pressao_saturacao_es_same_temp():
    calc = CalculadorIrrigacao()
    es = calc.calcular_pressao_saturacao_es(25, 25)
    assert round(es, 3) == 2.597
