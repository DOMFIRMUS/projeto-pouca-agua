import pytest
import math
from models.irrigacao import CalculadorIrrigacao
from app import app
from database import init_db, get_db_connection

@pytest.fixture
def client(tmp_path):
    app.config['TESTING'] = True

    # Temporarily override database path via environment variables or mock the database if possible
    # Given the database.py module uses a hardcoded DB_PATH variable: DB_PATH = os.path.join(os.path.dirname(__file__), 'pouca_agua.db')
    # we cannot directly change it easily via app.config.
    # The best solution is to just use the default db since it works for other tests, but just properly setup/teardown.

    with app.app_context():
        init_db()
        conn = get_db_connection()
        conn.execute('DELETE FROM projetos_metadados WHERE codigo_projeto = ?', ('PROJ-TEST-AREA',))
        conn.commit()

        conn.execute('INSERT INTO projetos_metadados (codigo_projeto, nome_projeto) VALUES (?, ?)', ('PROJ-TEST-AREA', 'Projeto Teste Area'))
        conn.commit()
        conn.close()

    with app.test_client() as client:
        yield client

    with app.app_context():
        conn = get_db_connection()
        conn.execute('DELETE FROM projetos_metadados WHERE codigo_projeto = ?', ('PROJ-TEST-AREA',))
        conn.commit()
        conn.close()

@pytest.fixture
def calculador():
    return CalculadorIrrigacao()

def test_calcular_diametro_dw_schwartzman(calculador):
    z = 1.0
    q = 4.0
    ko = 2.0

    dw = calculador.calcular_diametro_dw_schwartzman(z, q, ko)
    assert round(dw, 2) == 1.66

    assert calculador.calcular_diametro_dw_schwartzman(z, q, 0) == 0.0
    assert calculador.calcular_diametro_dw_schwartzman(z, q, -1) == 0.0

def test_calcular_raio_rw(calculador):
    alpha = 1.0
    q = 4.0
    ko = 2.0

    rw = calculador.calcular_raio_rw(alpha, q, ko)
    assert round(rw, 2) == 0.38

    assert calculador.calcular_raio_rw(0, q, ko) == 0.0
    assert calculador.calcular_raio_rw(-1, q, ko) == 0.0
    assert calculador.calcular_raio_rw(alpha, q, 0) == 0.0

def test_area_umedecida_faixa_continua_lls(calculador):
    params = {
        'profundidade_z': 1.0, 'q_vazao': 4.0, 'condutividade_ko': 2.0,
        'parametro_alpha': 1.0, 'espacamento_plantas_sp': 2.0,
        'espacamento_fileiras_sr': 4.0, 'np_emissores': 1
    }
    res = calculador.calcular_area_umedecida_fluxograma('faixa_continua', 'LLS', params)
    assert res['dw'] == 1.66
    assert res['rw'] == 0.38
    assert res['aw'] == 3.32
    assert res['ap'] == 8.0
    assert res['pw'] == 41.48

def test_area_umedecida_faixa_continua_lld(calculador):
    params = {
        'profundidade_z': 1.0, 'q_vazao': 4.0, 'condutividade_ko': 2.0,
        'parametro_alpha': 1.0, 'espacamento_plantas_sp': 2.0,
        'espacamento_fileiras_sr': 4.0, 'np_emissores': 1
    }
    res = calculador.calcular_area_umedecida_fluxograma('faixa_continua', 'LLD', params)
    assert res['aw'] == 6.64
    assert res['pw'] == 82.97

def test_area_umedecida_por_arvore_lls(calculador):
    params = {
        'profundidade_z': 1.0, 'q_vazao': 4.0, 'condutividade_ko': 2.0,
        'parametro_alpha': 1.0, 'espacamento_plantas_sp': 2.0,
        'espacamento_fileiras_sr': 4.0, 'np_emissores': 2
    }
    res = calculador.calcular_area_umedecida_fluxograma('por_arvore', 'LLS', params)
    assert res['aw'] == pytest.approx(0.93, abs=0.01)
    assert res['pw'] == pytest.approx(11.58, abs=0.01)

def test_area_umedecida_por_arvore_lld(calculador):
    params = {
        'profundidade_z': 1.0, 'q_vazao': 4.0, 'condutividade_ko': 2.0,
        'parametro_alpha': 1.0, 'espacamento_plantas_sp': 2.0,
        'espacamento_fileiras_sr': 4.0, 'np_emissores': 2
    }
    res = calculador.calcular_area_umedecida_fluxograma('por_arvore', 'LLD', params)
    assert res['aw'] == pytest.approx(1.85, abs=0.01)
    assert res['pw'] == pytest.approx(23.17, abs=0.01)

def test_api_area_umedecida_sucesso(client):
    payload = {
        'tipo_disposicao': 'faixa_continua',
        'configuracao_linha': 'LLS',
        'parametro_alpha': 1.0,
        'condutividade_ko': 2.0,
        'profundidade_z': 1.0,
        'q_vazao': 4.0,
        'espacamento_plantas_sp': 2.0,
        'espacamento_fileiras_sr': 4.0,
        'np_emissores': 1
    }
    response = client.post('/api/projetos/PROJ-TEST-AREA/area-umedecida', json=payload)
    assert response.status_code == 200

    with app.app_context():
        conn = get_db_connection()
        row = conn.execute('SELECT tipo_disposicao, rw_calculado, pw_final FROM projetos_metadados WHERE codigo_projeto = ?', ('PROJ-TEST-AREA',)).fetchone()
        conn.close()

    assert row is not None, "O registro sumiu do banco temporário!"
    assert row['tipo_disposicao'] == 'faixa_continua'
    assert row['rw_calculado'] == 0.38
    assert row['pw_final'] == 41.48

def test_api_area_umedecida_falha_parametros_invalidos(client):
    payload = {
        'tipo_disposicao': 'invalido',
        'configuracao_linha': 'LLS',
        'parametro_alpha': -1.0,
        'condutividade_ko': 2.0,
        'profundidade_z': 1.0,
        'q_vazao': 4.0,
        'espacamento_plantas_sp': 2.0,
        'espacamento_fileiras_sr': 4.0
    }
    response = client.post('/api/projetos/PROJ-TEST-AREA/area-umedecida', json=payload)
    assert response.status_code == 400

def test_api_area_umedecida_falha_projeto_inexistente(client):
    payload = {
        'tipo_disposicao': 'faixa_continua',
        'configuracao_linha': 'LLS',
        'parametro_alpha': 1.0,
        'condutividade_ko': 2.0,
        'profundidade_z': 1.0,
        'q_vazao': 4.0,
        'espacamento_plantas_sp': 2.0,
        'espacamento_fileiras_sr': 4.0
    }
    response = client.post('/api/projetos/PROJ-NAO-EXISTE/area-umedecida', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "Projeto não encontrado" in data["erro"]
