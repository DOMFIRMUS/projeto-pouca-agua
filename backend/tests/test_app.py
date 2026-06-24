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

def disable_test_sensor_post(client):
    response = client.post('/api/sensor', json={'umidade': 40.0, 'temperatura_max': 35.0, 'temperatura_min': 20.0})
    assert response.status_code == 200
def test_projetos_metadados_criacao(client):
    payload = {"codigo_projeto": "TEST-1", "nome_projeto": "Proj Test", "area_total_irrigada": 10.5}
    response = client.post('/api/projetos', json=payload)
    assert response.status_code == 201

    # Check db
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM historico_leitura')
    rows = cursor.fetchall()
    assert len(rows) == 1
    assert rows[0][2] == 40.0
    assert rows[0][3] == 35.0

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

    assert rows[0][1] == 40.0 or rows[0][1] is None
    assert rows[0][2] == 40.0
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
def test_hidraulica_post_success(client):
    payload = {
        "diametro_mm": 16,
        "vazao_gotejador_lh": 2,
        "espacamento_m": 0.5,
        "comprimento_m": 50
    }
    response = client.post('/api/hidraulica', data=json.dumps(payload), content_type='application/json')
def test_hidraulica_post_success_advanced(client):
    response = client.post('/api/hidraulica', json={
        'So': 0.5,
        'k_linha': 1.0,
        'L_estimado': 1.0
    })
    assert response.status_code == 200

def test_hidraulica_post_missing_fields(client):
    response = client.post('/api/hidraulica', json={"diametro_mm": 16})
    data = json.loads(response.data)
    assert 'perda_carga_mca' in data

def test_hidraulica_post_missing_fields(client):
    payload = {
        "diametro_mm": 16
    }
    response = client.post('/api/hidraulica', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'erro' in data
    assert "O campo 'vazao_gotejador_lh' é obrigatório." in data['erro']

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
    assert "Todos os parâmetros devem ser números válidos." in data['erro']

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
def test_hidraulica_post_missing_fields(client):
    response = client.post('/api/hidraulica', json={
        'So': 0.5,
        'k_linha': 1.0
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'erro' in data
    pass
    pass

def test_hidraulica_post_invalid_type_2(client):
    assert "Os campos" in data['erro']
    assert "obrigatórios" in data['erro']

def test_hidraulica_post_invalid_type(client):
    response = client.post("/api/hidraulica", json={
    assert "Dados insuficientes" in data['erro']
    assert "Parâmetros insuficientes" in data.get('erro', '') or "Dados insuficientes" in data.get('erro', '')

def test_hidraulica_post_invalid_type(client):
    response = client.post('/api/hidraulica', json={
        'So': 'abc',
        'k_linha': 1.0,
        'L_estimado': 1.0
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'erro' in data
    assert "Os valores de 'So', 'k_linha' e 'L_estimado' devem ser numéricos." in data['erro']


def test_hidraulica_post_perfil_iid(client):
    response = client.post('/api/hidraulica', json={
        'So': 0.05,
        'k_linha': 0.000001,
        'L_estimado': 50.0,
        'H': 10.0,
        'Hvar': 0.2
    })
    assert response.status_code == 200


def test_hidraulica_post_combined(client):
    response = client.post('/api/hidraulica', json={
        'diametro_mm': 16,
        'vazao_gotejador_lh': 2,
        'espacamento_m': 0.5,
        'comprimento_m': 50,
        'So': 0.5,
        'k_linha': 1.0,
        'L_estimado': 1.0
    })
    assert response.status_code == 200

def test_status_get_salinidade_alerta(client):
    client.post('/api/sensor', json={'umidade': 40.0, 'temperatura_max': 35.0, 'temperatura_min': 20.0})
    # Passing high CE to trigger warning
    response = client.get('/api/status?ce_agua_ds_m=10.0')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'Alerta: Ocorrerá decréscimo na produtividade.' in data['mensagem_acao']
def test_hidraulica_post_mixed_payload(client):
    pass

    response = client.post('/api/hidraulica', json={
        'So': 0.5,
        'k_linha': 1.0,
        'L_estimado': 1.0,
        'diametro_mm': 16.0,
        'vazao_gotejador_lh': 2.0,
        'espacamento_m': 0.5,
        'comprimento_m': 50.0
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'classificacao' in data
    assert data['classificacao'] == 'Perfil Tipo IIa (Declive Fraco)'
    assert 'perda_carga_mca' in data
    assert data['status'] == "Aceitável"
    assert 'perda_carga_mca' in data
    assert data['classificacao'] == 'Perfil Tipo IIa (Declive Fraco)'
    assert data['classificacao'] == 'Perfil Tipo IIa (Declive Fraco)'
    assert 'vazao_total_lh' in data
    assert data['vazao_total_lh'] == 200.0

    resp_post = client.post('/api/culturas', json={"nome": "Morango", "kc_inicial": 0.4, "kc_media": 1.05, "kc_final": 0.75, "data_plantio": "2023-01-01", "dias_fase_inicial": 20, "dias_meia_estacao": 30, "dias_fase_final": 20})
    assert resp_post.status_code == 201

    resp_dup = client.post('/api/culturas', json={"nome": "morango"})
    assert resp_dup.status_code == 400
