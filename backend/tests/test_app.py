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

def test_hidraulica_post_invalid_type(client):
    payload = {
        "diametro_mm": "abc",
        "vazao_gotejador_lh": 2,
        "espacamento_m": 0.5,
        "comprimento_m": 50
    }
    response = client.post('/api/hidraulica', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'erro' in data
    assert "Todos os parâmetros básicos devem ser números válidos." in data['erro']
def test_hidraulica_post_success_basic(client):
    response = client.post('/api/hidraulica', json={
        'diametro_mm': 16.0,
        'vazao_gotejador_lh': 2.0,
        'espacamento_m': 0.5,
        'comprimento_m': 100.0
    })
    assert response.status_code == 200
    data = json.loads(response.data)
