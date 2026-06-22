import sys
import os
import pytest
import sqlite3
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from database import DB_PATH

from database import init_db

@pytest.fixture
def client():
    app.config['TESTING'] = True

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    init_db()

    with app.test_client() as client:
        yield client

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

def test_sensor_post(client):
    response = client.post('/api/sensor', json={'umidade': 40.0, 'temperatura_max': 35.0, 'temperatura_min': 20.0})
    assert response.status_code == 200

    # Check db
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM historico_leitura')
    rows = cursor.fetchall()
    assert len(rows) == 1
    assert rows[0][1] == 40.0
    assert rows[0][2] == 35.0

def test_status_get(client):
    client.post('/api/sensor', json={'umidade': 40.0, 'temperatura_max': 35.0, 'temperatura_min': 20.0})
    response = client.get('/api/status')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['umidade_atual'] == 40.0
    assert 'status_solo' in data
    assert 'metricas_tese' in data
    assert 'tempo_irrigacao_horas' in data['metricas_tese']
    assert 'numero_emissores_por_planta' in data['metricas_tese']
    assert 'turno_rega_max_dias' in data
    assert isinstance(data['turno_rega_max_dias'], int)
    assert 'lamina_bruta_irrigacao_mm' in data
    assert 'metricas_tese' in data
    assert 'fracao_lixiviacao' in data['metricas_tese']
    assert 'irrigacao_total_necessaria_mm' in data['metricas_tese']

def test_status_get_blaney_criddle(client):
    client.post('/api/sensor', json={'umidade': 40.0, 'temperatura_max': 35.0, 'temperatura_min': 20.0})
    response = client.get('/api/status?metodo_eto=blaney-criddle')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['umidade_atual'] == 40.0
    assert 'status_solo' in data

def test_status_get_blaney_criddle(client):
    client.post('/api/sensor', json={'umidade': 40.0, 'temperatura_max': 35.0, 'temperatura_min': 20.0})
    response = client.get('/api/status?metodo_eto=blaney-criddle')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['umidade_atual'] == 40.0
    assert 'status_solo' in data

def test_status_get_blaney_criddle(client):
    client.post('/api/sensor', json={'umidade': 40.0, 'temperatura_max': 35.0, 'temperatura_min': 20.0})
    response = client.get('/api/status?metodo_eto=blaney-criddle')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['umidade_atual'] == 40.0
    assert 'status_solo' in data
    assert 'metricas_tese' in data
    assert 'tempo_irrigacao_horas' in data['metricas_tese']
    assert 'numero_emissores_por_planta' in data['metricas_tese']

def test_historico_get(client):
    client.post('/api/sensor', json={'umidade': 40.0, 'temperatura_max': 35.0, 'temperatura_min': 20.0})
    client.post('/api/sensor', json={'umidade': 45.0})

    response = client.get('/api/historico')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['umidade'] == 45.0
    assert data[1]['umidade'] == 40.0

def test_hidraulica_post_success_advanced(client):
    response = client.post('/api/hidraulica', json={
def test_hidraulica_post_success(client):
    response = client.post('/api/classificar_perfil', json={
        'So': 0.5,
        'k_linha': 1.0,
        'L_estimado': 1.0
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'classificacao' in data
    assert data['classificacao'] == 'Perfil Tipo IIa (Declive Fraco)'

def test_hidraulica_post_success_basic(client):
    response = client.post('/api/hidraulica', json={
        'diametro_mm': 16.0,
        'vazao_gotejador_lh': 2.0,
        'espacamento_m': 0.5,
        'comprimento_m': 100.0
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'perda_carga_mca' in data

def test_hidraulica_post_success_combined(client):
    response = client.post('/api/hidraulica', json={
        'So': 0.5,
        'k_linha': 1.0,
        'L_estimado': 1.0,
        'diametro_mm': 16.0,
        'vazao_gotejador_lh': 2.0,
        'espacamento_m': 0.5,
        'comprimento_m': 100.0
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'classificacao' in data
    assert 'perda_carga_mca' in data

def test_hidraulica_post_missing_fields(client):
    response = client.post('/api/classificar_perfil', json={
        'So': 0.5,
        'k_linha': 1.0
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'erro' in data
    assert "Parâmetros insuficientes" in data['erro']

def test_hidraulica_post_invalid_type(client):
    response = client.post('/api/classificar_perfil', json={
        'So': 'abc',
        'k_linha': 1.0,
        'L_estimado': 1.0
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'erro' in data
    assert "Os valores de 'So', 'k_linha' e 'L_estimado' devem ser numéricos." in data['erro']

def test_hidraulica_post_mixed_payload(client):
    response = client.post('/api/hidraulica', json={
        'So': 0.5,
        'k_linha': 1.0,
        'L_estimado': 1.0,
        "diametro_mm": 16,
        "vazao_gotejador_lh": 2,
        "espacamento_m": 0.5,
        "comprimento_m": 50
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'classificacao' in data
    assert data['classificacao'] == 'Perfil Tipo IIa (Declive Fraco)'
    assert 'vazao_total_lh' in data
    assert data['vazao_total_lh'] == 200.0

def test_status_faixa_descontinua(client):
    # Pass 'se' large enough to trigger the warning
    # We need an existing reading to test /api/status. We can just insert one using test_sensor_post_valid, or mock it.
    client.post('/api/sensor', json={'umidade': 50.0, 'temperatura_max': 30.0, 'temperatura_min': 20.0})

    # Se is huge, should trigger warning
    response = client.get('/api/status?se=100.0&alpha=0.5&q=10.0&ko=1.0')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data.get('alerta_faixa_descontinua') is True
    assert data.get('mensagem_faixa') == "Afastamento excessivo entre gotejadores. A faixa contínua de humidade será rompida, prejudicando as raízes."
