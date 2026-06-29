import pytest
from backend.app import app
import json

@pytest.fixture(autouse=True)
def client():
    app.config['TESTING'] = True

    # Setup test DB cleanly for each run
    import backend.database as db
    import tempfile, os
    fd, path = tempfile.mkstemp()
    db.DB_PATH = path
    db.init_db()
    db.seed_culturas()

    with app.test_client() as client:
        yield client

    os.close(fd)
    os.remove(path)

def test_projetos_metadados_criacao(client):
    payload = {"codigo_projeto": "TEST-1", "nome_projeto": "Proj Test", "area_total_irrigada": 10.5}
    response = client.post('/api/projetos', json=payload)
    assert response.status_code == 201

    response_dup = client.post('/api/projetos', json=payload)
    assert response_dup.status_code == 400

def test_vincular_cultura(client):
    client.post('/api/projetos', json={"codigo_projeto": "TEST-2", "nome_projeto": "Proj Test"})

    payload = {"cultura_id": 1, "estagio_selecionado": "inicial"}
    resp = client.post('/api/projetos/TEST-2/cultura', json=payload)
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data['dados_vinculados']['kc_aplicado'] > 0

    resp_fake = client.post('/api/projetos/TEST-FAKE/cultura', json=payload)
    assert resp_fake.status_code == 404

def test_area_umedecida(client):
    client.post('/api/projetos', json={"codigo_projeto": "TEST-3", "nome_projeto": "Proj Test"})

    payload = {"q_vazao": 2.0, "volume_z": 30.0, "ko_condutividade": 15.0, "espacamento_plantas_sp": 0.5, "espacamento_fileiras_sr": 1.0, "numero_emissores_np": 1}
    resp = client.post('/api/projetos/TEST-3/area-umedecida', json=payload)
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert 'metadados' in data

    resp_fake = client.post('/api/projetos/FAKE/area-umedecida', json=payload)
    assert resp_fake.status_code == 404

def test_area_sombreada(client):
    client.post('/api/projetos', json={"codigo_projeto": "TEST-4", "nome_projeto": "Proj Test"})

    payload = {"tipo_copa": "circular", "espacamento_plantas_sp": 1.0, "espacamento_fileiras_sr": 1.0, "diametro_copa_dco": 0.5}
    resp = client.post('/api/projetos/TEST-4/area-sombreada', json=payload)
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert 'ps' in data

    resp_fake = client.post('/api/projetos/FAKE/area-sombreada', json=payload)
    assert resp_fake.status_code == 404

def test_hidraulica_leitura_climatica(client):
    payload = {"t_max": 32.0, "t_min": 20.0, "latitude": -22.0, "mes_index": 1, "ur_media": 60.0}
    resp = client.post('/api/hidraulica', json=payload)
    assert resp.status_code == 201
    assert 'eto' in json.loads(resp.data)

def test_status_endpoints(client):
    client.post('/api/hidraulica', json={"t_max": 30.0, "t_min": 20.0})
    resp = client.get('/api/status')
    assert resp.status_code == 200

    client.post('/api/projetos', json={"codigo_projeto": "TEST-5"})
    resp_proj = client.get('/api/status/TEST-5')
    assert resp_proj.status_code == 200

def test_culturas_endpoints(client):
    resp = client.get('/api/culturas')
    assert resp.status_code == 200
    assert len(json.loads(resp.data)) > 0

    resp_post = client.post('/api/culturas', json={"nome": "Morango", "kc_inicial": 0.4, "kc_media": 1.05, "kc_final": 0.75, "data_plantio": "2023-01-01", "dias_fase_inicial": 20, "dias_meia_estacao": 30, "dias_fase_final": 20})
    assert resp_post.status_code == 201

    resp_dup = client.post('/api/culturas', json={"nome": "morango"})
    assert resp_dup.status_code == 400
