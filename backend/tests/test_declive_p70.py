import pytest
import math
from backend.models.irrigacao import CalculadorIrrigacao
from backend.app import app
import backend.database as db

@pytest.fixture
def calc():
    return CalculadorIrrigacao()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    db.init_db()
    with app.test_client() as client:
        yield client

def test_ponto_pressao_minima_ratio(calc):
    So = 0.05
    k_linha = 1.34e-4
    L = 50.0
    ratio = calc.calcular_ponto_pressao_minima_ratio(So, k_linha, L)
    So_abs = abs(So)
    atrito = k_linha * math.pow(L, 1.75)
    razao = So_abs / atrito
    expected = 1 - 0.56098 * math.pow(razao, 0.57143)
    expected = max(0.0, min(1.0, expected))
    assert math.isclose(ratio, expected, rel_tol=1e-5)

def test_ponto_pressao_minima_ratio_trava_zero(calc):
    ratio = calc.calcular_ponto_pressao_minima_ratio(0.05, 0.0, 50.0)
    assert ratio == 1.0

def test_classificar_dimensionar_perfil_ii_b(calc):
    pressao_h = 10.0
    h_var_fraction = 0.20
    So = 0.02
    k_linha = 1.34e-4
    L_estimado = math.pow(So / k_linha, 1 / 1.75)
    l_max = calc.classificar_dimensionar_perfil_ii_b(pressao_h, h_var_fraction, k_linha, So, L_estimado)
    assert l_max is not None
    expected = (pressao_h * h_var_fraction) / (0.357 * So)
    assert math.isclose(l_max, round(expected, 3), rel_tol=1e-5)

def test_classificar_dimensionar_perfil_ii_b_nao_atendido(calc):
    l_max = calc.classificar_dimensionar_perfil_ii_b(10.0, 0.20, 1.34e-4, 0.02, 10.0)
    assert l_max is None

def test_classificar_dimensionar_perfil_ii_b_so_zero(calc):
    l_max = calc.classificar_dimensionar_perfil_ii_b(10.0, 0.20, 1.34e-4, 0.0, 50.0)
    assert l_max == 0.0

def test_refinar_lmax_perfil_ii_a(calc):
    pressao_h = 10.0
    h_var_fraction = 0.20
    k_linha = 1.34e-4
    So = 0.05
    lmax = calc.refinar_lmax_perfil_ii_a(pressao_h, h_var_fraction, k_linha, So)
    assert isinstance(lmax, float)
    assert lmax >= 0.0

def test_api_linha_lateral_declive_404(client):
    res = client.post('/api/projetos/INEXISTENTE/linha-lateral-declive', json={
        "pressao_h": 10.0,
        "h_var_fraction": 0.2,
        "declividade_so": -0.02,
        "k_linha": 1.34e-4,
        "L_estimado": 50.0
    })
    assert res.status_code == 404

def test_api_linha_lateral_declive_sucesso(client):
    try:
        conn = db.get_db_connection()
        conn.execute("INSERT OR IGNORE INTO projetos_metadados (codigo_projeto, nome_projeto) VALUES ('PROJ-123', 'Projeto Teste')")
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()

    res = client.post('/api/projetos/PROJ-123/linha-lateral-declive', json={
        "pressao_h": 10.0,
        "h_var_fraction": 0.2,
        "declividade_so": -0.02,
        "k_linha": 1.34e-4,
        "L_estimado": 50.0
    })

    assert res.status_code == 200
    data = res.get_json()
    assert "comprimento_maximo_m" in data
    assert "posicao_pressao_minima_ratio" in data
    assert "perfil_pressao_tipo" in data
