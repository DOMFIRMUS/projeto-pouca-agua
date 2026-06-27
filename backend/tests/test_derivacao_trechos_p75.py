import pytest
from backend.models.irrigacao import CalculadorIrrigacao

def test_calcular_hf_derivacao():
    calc = CalculadorIrrigacao()
    # Test calculation with known values
    hf = calc.calcular_hf_derivacao_p75(q_vazao=3600, d_interno=50, l_comprimento=100)
    # 3600 L/h = 1 m3/s, d=50 mm = 0.05 m
    # hf = 8.263e-2 * 1 * 0.02 * (1^2) / (0.05^5) * 100
    assert hf >= 0

def test_diametro_teorico():
    calc = CalculadorIrrigacao()
    d_teorico = calc.calcular_diametro_teorico_derivacao(q_vazao=3600, hf_target=2.0, l_comprimento=100)
    assert d_teorico > 0

def test_divisao_por_zero_protecao():
    calc = CalculadorIrrigacao()
    # d_interno = 0 should return 0.0
    hf = calc.calcular_hf_derivacao_p75(q_vazao=3600, d_interno=0, l_comprimento=100)
    assert hf == 0.0

    # hf_target = 0 should be forced to 0.001
    d_teorico = calc.calcular_diametro_teorico_derivacao(q_vazao=3600, hf_target=0, l_comprimento=100)
    assert d_teorico > 0

def test_selecionar_melhor_diametro_comercial():
    calc = CalculadorIrrigacao()
    d_teorico = 0.045
    lista_comerciais = [0.025, 0.035, 0.050, 0.075]
    # hf is calculated internally.
    d_escolhido, hf_real = calc.selecionar_melhor_diametro_comercial(
        d_teorico, lista_comerciais, q_vazao=3600, l_comprimento=100, delta_z=5.0
    )
    assert d_escolhido in lista_comerciais

def test_calcular_pressao_trecho_seguinte():
    calc = CalculadorIrrigacao()
    h1 = calc.calcular_pressao_trecho_seguinte(h_anterior=20.0, hf_trecho=2.5, delta_z=1.2)
    # 20 - 2.5 + 1.2 = 18.7
    assert h1 == 18.7
