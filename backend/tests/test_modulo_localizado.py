# -*- coding: utf-8 -*-
import pytest
from backend.models.irrigacao import CalculadorIrrigacao

def test_schwartzman_e_rw_limites():
    calc = CalculadorIrrigacao()
    assert calc.calcular_diametro_dw_schwartzman(0.40, 1.6, 0.0) == 0.0
    assert calc.calcular_diametro_dw_schwartzman(0.40, 1.6, 2.0) == 0.89
    assert calc.calcular_raio_rw(0.0, 1.6, 2.0) == 0.0

def test_ajuste_fator_f():
    calc = CalculadorIrrigacao()
    assert calc.ajustar_fator_f_dinamico(0.40, 2.0) == 0.520
    assert calc.ajustar_fator_f_dinamico(0.40, 7.0) == 0.320

def test_calcular_constante_psicrometrica_gamma():
    calc = CalculadorIrrigacao()
    assert calc.calcular_constante_psicrometrica_gamma(101.3) == 0.06736

def test_calcular_area_umedecida_fluxograma():
    calc = CalculadorIrrigacao()
    params = {"sp": 1.0, "sr": 1.0, "dw": 1.0, "rw": 1.0, "np": 1.0}
    res = calc.calcular_area_umedecida_fluxograma("faixa_continua", "LLS", params)
    assert res["dw"] == 1.0
    assert res["rw"] == 1.0
    assert res["aw"] == 1.0
    assert res["ap"] == 1.0
    assert res["pw"] == 100.0

def test_calcular_irn_max_localizada():
    calc = CalculadorIrrigacao()
    assert calc.calcular_irn_max_localizada(10.0, 0.5, 50.0) == 2.5
