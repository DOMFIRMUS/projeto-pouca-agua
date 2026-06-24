import pytest
from backend.models.irrigacao import CalculadorIrrigacao

def test_et_consorcio():
    calc = CalculadorIrrigacao()
    # Test normalization of fractions
    lista_culturas_nao_normalizada = [
        {'kc': 1.0, 'fracao_area': 0.8},
        {'kc': 0.8, 'fracao_area': 0.4} # Sum = 1.2
    ]
    # Expected fractions after normalization: 0.8/1.2 = 0.666, 0.4/1.2 = 0.333
    # Expected Kc: 1.0 * 0.666 + 0.8 * 0.333 = 0.666 + 0.266 = 0.933
    etc = calc.calcular_et_consorcio(eto=5.0, kl=1.0, lista_culturas=lista_culturas_nao_normalizada)
    assert etc > 0

    # Test capping at 1.30
    lista_alta = [{'kc': 1.5, 'fracao_area': 1.0}]
    etc_alta = calc.calcular_et_consorcio(eto=5.0, kl=1.0, lista_culturas=lista_alta)
    assert etc_alta == 6.5 # 5.0 * 1.3 * 1.0

def test_simular_autonomia_cisterna():
    calc = CalculadorIrrigacao()
    # Test extreme drought (zero input)
    res_seca = calc.simular_autonomia_cisterna(
        volume_atual=1000,
        capacidade_max=5000,
        area_irrigada_m2=10,
        lamina_itn_mm=5, # volume_saida = 50
        precipitacao_mm=0,
        area_captacao_m2=20
    )
    assert res_seca['volume_final_l'] == 950
    assert res_seca['autonomia_dias'] == 19.0 # 950 / 50

    # Test spillover
    res_cheia = calc.simular_autonomia_cisterna(
        volume_atual=4000,
        capacidade_max=5000,
        area_irrigada_m2=10,
        lamina_itn_mm=5, # saida = 50
        precipitacao_mm=100,
        area_captacao_m2=50, # entrada = 100 * 50 * 0.9 = 4500
        coeficiente_escoamento=0.9
    )
    # 4000 + 4500 - 50 = 8450 -> capped at 5000
    assert res_cheia['volume_final_l'] == 5000.0

def test_escalonamento_bomba():
    calc = CalculadorIrrigacao()
    res = calc.escalonar_setores_familiar(q_bomba_lh=1000, lista_setores_vazao_lh=[400, 500, 600]) # total = 1500
    assert res['turnos_bomba'] == 2
    assert res['vazao_total_lh'] == 1500
