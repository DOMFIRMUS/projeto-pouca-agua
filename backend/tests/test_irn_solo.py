# -*- coding: utf-8 -*-
import pytest
from backend.models.irrigacao import CalculadorIrrigacao

def test_transicoes_fereres_figura_8():
    calc = CalculadorIrrigacao()
    assert calc.orquestrar_etc_figura_8('fereres_1981', 5.0, 1.15, 15.0, 15.0) == 2.248
    assert calc.orquestrar_etc_figura_8('fereres_1981', 5.0, 1.15, 40.0, 40.0) == 4.232
    assert calc.orquestrar_etc_figura_8('fereres_1981', 5.0, 1.15, 75.0, 75.0) == 5.750

def test_calculo_cad_e_limites():
    calc = CalculadorIrrigacao()
    assert calc.calcular_cad_solo(0.30, 0.15, 0.40) == 60.00
    assert calc.calcular_cad_solo(0.15, 0.30, 0.40) == 0.0

def test_calculo_irn_e_turno_rega():
    calc = CalculadorIrrigacao()
    res = calc.calcular_irn_e_turno_rega(60.0, 0.5, 4.5)
    assert res["raw"] == 30.0
    assert res["turno_rega"] == 6
    assert res["irn"] == 4.5
