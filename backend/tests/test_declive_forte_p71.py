import pytest
import math
from backend.models.irrigacao import CalculadorIrrigacao

def test_classificacao_perfil_ii_c():
    calc = CalculadorIrrigacao()
    So = 0.05
    k_linha = 1.5e-5
    razao_alvo = 2.0
    L_estimado = (So / (razao_alvo * k_linha)) ** (1/1.75)

    perfil = calc.classificar_perfil_pressao(So, k_linha, L_estimado)
    assert 'Perfil Tipo IIc' in perfil

def test_classificacao_perfil_ii_d():
    calc = CalculadorIrrigacao()
    So = 0.1
    k_linha = 1.5e-5
    razao_alvo = 3.5
    L_estimado = (So / (razao_alvo * k_linha)) ** (1/1.75)

    perfil = calc.classificar_perfil_pressao(So, k_linha, L_estimado)
    assert 'Perfil Tipo IId' in perfil

def test_solver_iterativo_perfil_ii_c_convergencia():
    calc = CalculadorIrrigacao()
    H = 10.0
    H_var_fraction = 0.2
    So = -0.05 # Força envio de topografia em declive como negativo (valida abs)
    k_linha = 1.5e-5

    L_max = calc.resolver_lmax_perfil_ii_c(H, H_var_fraction, k_linha, So)

    assert isinstance(L_max, float)
    assert L_max > 0.0
    # Valida convergencia e sanidade dimensional
    assert L_max < 200.0

def test_solver_iterativo_perfil_ii_c_divisao_por_zero_protegida():
    calc = CalculadorIrrigacao()
    H = 10.0
    H_var_fraction = 0.2
    So = 0.0 # Gatilho para divisão por zero se abs_so/den_condicao não for protegido
    k_linha = 1.5e-5

    L_max = calc.resolver_lmax_perfil_ii_c(H, H_var_fraction, k_linha, So)
    # A salvaguarda deve devolver 0.0 instantaneamente
    assert L_max == 0.0
