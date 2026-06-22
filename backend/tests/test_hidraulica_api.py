import sys
import os
import pytest
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hidraulica_endpoint(client):
    payload = {
        "diametro_mm": 16,
        "vazao_gotejador_lh": 2,
        "espacamento_m": 0.5,
        "comprimento_m": 50
    }
    response = client.post('/api/hidraulica', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['vazao_total_lh'] == 200.0
    assert 'perda_carga_mca' in data
    assert data['status'] == "Aceitável"

def test_hidraulica_endpoint_missing_fields(client):
    payload = {
        "diametro_mm": 16
    }
    response = client.post('/api/hidraulica', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "erro" in data
