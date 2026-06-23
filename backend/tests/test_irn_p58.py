import pytest
from backend.models.irrigacao import CalculadorIrrigacao
from backend.app import app
from backend.database import init_db

def obter_conexao_teste():
    import sqlite3
    conn = sqlite3.connect("irrigacao.db")
    conn.row_factory = sqlite3.Row
    return conn

@pytest.fixture
def calculador():
    return CalculadorIrrigacao()

def test_calcular_cad_sucesso(calculador):
    # theta_cc = 0.3, theta_pmp = 0.15, z = 0.5m
    cad = calculador.calcular_cad(0.30, 0.15, 0.5)
    assert cad == 75.0

def test_calcular_cad_excecao_fisica(calculador):
    # pmp > cc
    cad1 = calculador.calcular_cad(0.15, 0.30, 0.5)
    assert cad1 == 0.0

    # z <= 0
    cad2 = calculador.calcular_cad(0.30, 0.15, 0.0)
    assert cad2 == 0.0

def test_calcular_irn_total(calculador):
    # cad = 75.0, fator_f = 0.5 -> IRN = 37.5
    irn = calculador.calcular_irn_p58(75.0, 0.5, tipo_irrigacao='total')
    assert irn == 37.5

def test_calcular_irn_suplementar(calculador):
    # cad = 75.0, fator_f = 0.5, pe = 10.0 -> IRN = 27.5
    irn = calculador.calcular_irn_p58(75.0, 0.5, pe=10.0, tipo_irrigacao='suplementar')
    assert irn == 27.5

def test_calcular_irn_suplementar_trava(calculador):
    # cad = 75.0, fator_f = 0.5, pe = 50.0 -> IRN = -12.5 -> travado em 0.0
    irn = calculador.calcular_irn_p58(75.0, 0.5, pe=50.0, tipo_irrigacao='suplementar')
    assert irn == 0.0

@pytest.fixture
def client():
    app.config['TESTING'] = True
    init_db()
    with app.test_client() as client:
        yield client

def test_api_irn(client):
    conn = obter_conexao_teste()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO projetos_metadados (codigo_projeto, profundidade_z) VALUES ('TEST_PROJ', 0.5)")
    conn.commit()
    conn.close()

    payload = {
        "theta_cc": 0.30,
        "theta_pmp": 0.15,
        "fator_f": 0.5,
        "pe": 10.0,
        "tipo_irrigacao": "suplementar"
    }

    response = client.post('/api/projetos/TEST_PROJ/irn', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['cad_calculada'] == 75.0
    assert data['irn_calculada'] == 27.5
