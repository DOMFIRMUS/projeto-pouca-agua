import pytest
import math
from backend.models.irrigacao import CalculadorIrrigacao

@pytest.fixture
def calc():
    return CalculadorIrrigacao()

def test_solver_perfil_iii_convergencia(calc):
    pressao_h = 10.0
    h_var_fraction = 0.2
    k_linha = 1.876100819513971e-05
    declividade_so = -0.09870751728366786

    l_max = calc.resolver_lmax_perfil_iii(pressao_h, h_var_fraction, k_linha, declividade_so)

    assert l_max > 0.0
    assert isinstance(l_max, float)

def test_solver_perfil_iii_divisao_zero(calc):
    pressao_h = 10.0
    h_var_fraction = 0.2
    k_linha = 10.0
    declividade_so = -0.01

    l_max = calc.resolver_lmax_perfil_iii(pressao_h, h_var_fraction, k_linha, declividade_so)
    assert l_max == 0.0

def test_orquestrador_fallback_perfil_iii(calc, monkeypatch):
    def mock_fail(*args, **kwargs):
        raise ValueError("Forced failure")

    monkeypatch.setattr(calc, "calcular_lmax_perfil_tipo_IIa", mock_fail)
    monkeypatch.setattr(calc, "calcular_lmax_perfil_tipo_IIb", mock_fail)
    monkeypatch.setattr(calc, "calcular_lmax_perfil_tipo_IIc", mock_fail)
    monkeypatch.setattr(calc, "calcular_lmax_perfil_tipo_IId", mock_fail)

    pressao_h = 10.0
    h_var_fraction = 0.2
    k_linha = 1.876100819513971e-05
    declividade_so = -0.09870751728366786

    l_max, perfil = calc.orquestrar_comprimento_declive(pressao_h, h_var_fraction, k_linha, declividade_so)

    assert l_max > 0.0
    assert perfil == 'Perfil Tipo III'

def test_orquestrador_fluxo_padrao_iia(calc):
    pressao_h = 10.0
    h_var_fraction = 0.2
    k_linha = 0.0005
    declividade_so = -0.001

    l_max, perfil = calc.orquestrar_comprimento_declive(pressao_h, h_var_fraction, k_linha, declividade_so)

    assert l_max is not None
    assert isinstance(perfil, str)
    assert "Perfil" in perfil
