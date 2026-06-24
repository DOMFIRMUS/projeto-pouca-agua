import sys
import os
import math
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.irrigacao import CalculadorIrrigacao

def test_tabela_stefan_boltzmann_interpolacao():
    calc = CalculadorIrrigacao()
    # T = 18.0 -> 35.24
    # T = 18.5 -> 35.48
    # Test for T = 18.2. Interpolation formula:
    # y = y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    # y = 35.24 + (35.48 - 35.24) * (18.2 - 18.0) / (18.5 - 18.0)
    # y = 35.24 + (0.24) * (0.2) / 0.5
    # y = 35.24 + 0.096 = 35.336

    # We used 18.2 directly and the algorithm rounded it? Wait, let's just check the method directly.
    val = calc.obter_stefan_boltzmann(18.2)
    # Because my script used standard floats, 35.336 should be exact.
    assert math.isclose(val, 35.336, rel_tol=1e-5), f"Expected 35.336 but got {val}"

def test_precisao_equacoes_radiacao():
    calc = CalculadorIrrigacao()

    # Eq 17 (Rso)
    # Rso = [0.75 + 2 * (Altitude / 100000)] * Ra
    # Altitude = 500, Ra = 20
    # Rso = [0.75 + 2 * (500 / 100000)] * 20 = [0.75 + 0.01] * 20 = 0.76 * 20 = 15.2
    rso = calc.calcular_rso(altitude=500.0, ra=20.0)
    assert math.isclose(rso, 15.2, rel_tol=1e-5), f"Expected 15.2 but got {rso}"

    # Eq 18 (Rns)
    # Rns = 0.77 * Rs
    # Rs = 15
    # Rns = 0.77 * 15 = 11.55
    rns = calc.calcular_rns(rs=15.0)
    assert math.isclose(rns, 11.55, rel_tol=1e-5), f"Expected 11.55 but got {rns}"

    # Eq 19 (Rnl)
    # t_max=30.0, t_min=20.0, ea=2.5, rs=10, rso=15
    # stefan_max for 30.0 -> we need to look up. Wait, 30.0 is not in the original table list?
    # Original table has up to 36.5. 30.0 isn't defined explicitly in my dictionary except wait, it says "33.0...". Let me check what 30.0 returns.
    # Ah, the dictionary I provided actually goes:
    # 2.0 to 4.5, then 17.0 to 20.5, then 33.0 to 36.5.
    # So 30.0 will interpolate between 20.5 and 33.0! Wait, let's just use temperatures exactly in the table to be rigorous:
    # t_max = 33.0 -> 43.08
    # t_min = 20.0 -> 36.21
    # ea = 2.5
    # rs = 10, rso = 15 -> razao = 10/15 = 0.6666...
    # Rnl = [(43.08 + 36.21) / 2.0] * (0.34 - 0.14 * sqrt(2.5)) * (1.35 * (10/15) - 0.35)
    # Termo temp = 79.29 / 2 = 39.645
    # Termo umidade = 0.34 - 0.14 * 1.5811388 = 0.34 - 0.221359 = 0.11864
    # Termo neb = 1.35 * 0.6666... - 0.35 = 0.9 - 0.35 = 0.55
    # Rnl = 39.645 * 0.11864 * 0.55 = 2.5869
    rnl = calc.calcular_rnl(t_max=33.0, t_min=20.0, ea=2.5, rs=10.0, rso=15.0)
    assert math.isclose(rnl, 2.5869, rel_tol=1e-3), f"Expected ~2.5869 but got {rnl}"

    # Eq 20 (Rn)
    # Rn = Rns - Rnl
    rn = calc.calcular_rn(rns=11.55, rnl=2.5869)
    assert math.isclose(rn, 8.9631, rel_tol=1e-3), f"Expected 8.9631 but got {rn}"

def test_caso_limite_rso_zero():
    calc = CalculadorIrrigacao()
    # If rso <= 0, razao_rs_rso = 1.0
    # t_max = 33.0, t_min = 20.0, ea = 2.5
    # Termo temp = 39.645
    # Termo umidade = 0.11864
    # Termo neb = 1.35 * (1.0) - 0.35 = 1.0
    # Rnl = 39.645 * 0.11864 * 1.0 = 4.7034

    rnl = calc.calcular_rnl(t_max=33.0, t_min=20.0, ea=2.5, rs=10.0, rso=0.0)
    assert math.isclose(rnl, 4.7034, rel_tol=1e-3), f"Expected ~4.7034 but got {rnl}"

    rnl2 = calc.calcular_rnl(t_max=33.0, t_min=20.0, ea=2.5, rs=10.0, rso=-5.0)
    assert math.isclose(rnl2, 4.7034, rel_tol=1e-3), f"Expected ~4.7034 but got {rnl2}"
