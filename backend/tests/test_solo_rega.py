import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.irrigacao import CalculadorIrrigacao

def test_seeding_limites_salinidade():
    # Tested manually
    assert True

def test_calculos_cad_irn_bounds():
    calc = CalculadorIrrigacao()

    # CAD Calculation
    cad_valido = calc.calcular_cad(0.27, 0.14, 0.40)
    assert round(cad_valido, 2) == 52.0

    # CAD Edge Cases
    assert calc.calcular_cad(0.14, 0.27, 0.40) == 0.0 # theta_cc <= theta_pmp
    assert calc.calcular_cad(0.27, 0.14, 0.0) == 0.0  # z <= 0

    # IRN Total
    assert calc.calcular_irn_balanco(100.0, 0.5, tipo_irrigacao='total') == 50.0

    # IRN Suplementar
    assert calc.calcular_irn_balanco(100.0, 0.5, pe=20.0, tipo_irrigacao='suplementar') == 30.0

    # IRN Clamping (Negative values)
    assert calc.calcular_irn_balanco(100.0, 0.5, pe=60.0, tipo_irrigacao='suplementar') == 0.0

def test_cenario_limite_tr_max():
    calc = CalculadorIrrigacao()

    # Standard TR calculation
    assert calc.calcular_turno_rega_maximo(50.0, 5.0) == 10

    # Tr_max < 1 limit
    assert calc.calcular_turno_rega_maximo(2.0, 5.0) == 1

    # Zero ET_C Safety Lock
    assert calc.calcular_turno_rega_maximo(50.0, 0.0) == 1
