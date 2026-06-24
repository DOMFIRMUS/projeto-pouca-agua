import pytest
from backend.models.irrigacao import CalculadorIrrigacao

@pytest.fixture
def calc():
    return CalculadorIrrigacao()

def test_validacao_limites_vilaca_ideais(calc):
    res = calc.validar_limites_vilaca(v_d=1.5, d_d=0.05, a_p=200e-6, d_c=0.012, l_c=0.055, v_c=5.0, v_l=1.0)
    assert res['limites_estourados'] is False
    assert len(res['alertas']) == 0

def test_validacao_limites_vilaca_fora_faixa(calc):
    res = calc.validar_limites_vilaca(v_d=4.0, d_d=0.05, a_p=200e-6, d_c=0.012, l_c=0.055, v_c=5.0, v_l=1.0)
    assert res['limites_estourados'] is True

def test_calculo_perdas_matematica(calc):
    calc_d = calc.calcular_perda_direta_hfl_d(1.0, 0.05, 200e-6)
    assert isinstance(calc_d, float)
    calc_l = calc.calcular_perda_lateral_hfl_l(d_c=0.012, l_c=0.055, v_c=5.0, v_l=1.0)
    assert isinstance(calc_l, float)

def test_caso_limite_divisao_por_zero(calc):
    res_d = calc.calcular_perda_direta_hfl_d(v_d=1.0, d_d=0.0, a_p=200e-6)
    assert res_d == 0.0
    res_l = calc.calcular_perda_lateral_hfl_l(d_c=-0.01, l_c=0.055, v_c=5.0, v_l=1.0)
    assert res_l == 0.0
