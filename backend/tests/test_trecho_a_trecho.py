import pytest
import math
from backend.models.irrigacao import CalculadorIrrigacao
from backend.app import app
from backend.database import init_db, insert_projeto

@pytest.fixture
def client():
    app.config['TESTING'] = True
    init_db()
    with app.test_client() as client:
        yield client

def test_calcular_reynolds():
    calc = CalculadorIrrigacao()
    # Para V = 1.0 m/s e D = 0.016 m com nu = 1.01e-6
    # R = (1.0 * 0.016) / 1.01e-6 = 15841.5841584...
    R = calc.calcular_reynolds(1.0, 0.016)
    assert math.isclose(R, 15841.58, rel_tol=1e-2)

    # Edge cases
    assert calc.calcular_reynolds(-1.0, 0.016) == 0.0
    assert calc.calcular_reynolds(1.0, 0.0) == 0.0

def test_calcular_fator_atrito_f():
    calc = CalculadorIrrigacao()

    # Laminar: R = 1500 < 2000 => f = 64 / 1500 = 0.042666...
    f_lam = calc.calcular_fator_atrito_f(1500)
    assert math.isclose(f_lam, 0.04266, rel_tol=1e-3)

    # Turbulento: R = 4000 >= 2000 => f = 0.3164 / 4000^0.25 = 0.3164 / 7.9527 = 0.03978
    f_turb = calc.calcular_fator_atrito_f(4000)
    assert math.isclose(f_turb, 0.03978, rel_tol=1e-3)

    # Edge cases
    assert calc.calcular_fator_atrito_f(0) == 0.0

def test_simular_lateral_trecho_a_trecho():
    calc = CalculadorIrrigacao()

    # Teste Aclive (declividade positiva)
    # L_max para h_var_max = 2.0m, p0 = 10.0m
    L_max_aclive, perfil_aclive = calc.simular_lateral_trecho_a_trecho(
        pressao_p0=10.0,
        vazao_q0=2.0, # L/h
        diametro_d=0.016, # m
        espacamento_se=0.5, # m
        declividade_so=0.02, # 2% aclive
        h_var_max=2.0
    )
    assert L_max_aclive > 0
    assert "1" in perfil_aclive

    # Teste Declive (declividade negativa)
    # Pela compensação da gravidade, a linha em declive deve permitir um comprimento maior (ou atingir limites em extremos)
    L_max_declive, perfil_declive = calc.simular_lateral_trecho_a_trecho(
        pressao_p0=10.0,
        vazao_q0=2.0, # L/h
        diametro_d=0.016, # m
        espacamento_se=0.5, # m
        declividade_so=-0.02, # 2% declive
        h_var_max=2.0
    )
    assert L_max_declive > 0
    # O comportamento de limite exato dependerá da hidrodinâmica, mas deve ser calculado sem quebrar
    assert type(perfil_declive) is dict

    # Edge Cases
    L_edge, _ = calc.simular_lateral_trecho_a_trecho(0, 2.0, 0.016, 0.5, 0.0, 2.0)
    assert L_edge == 0.0

def test_api_linha_lateral_trecho(client):
    codigo = "PROJ-TRECHO-TEST"

    # Seed a project
    client.post('/api/projetos', json={
        "codigo_projeto": codigo,
        "nome_projeto": "Teste Trecho",
        "nome_propriedade": "Fazenda",
        "nome_proprietario": "Joao",
        "nome_projetista": "Maria",
        "codigo_subunidade": "S1",
        "area_total_irrigada": 1.0,
        "area_subunidade": 0.5,
        "data_elaboracao": "2024-01-01"
    })

    payload = {
        "pressao_p0": 10.0,
        "diametro_interno_mm": 16.0,
        "declividade_so": 0.0,
        "h_var_max_m": 2.0
    }

    # Realiza a simulação
    response = client.post(f'/api/projetos/{codigo}/linha-lateral-trecho', json=payload)

    # O Flask pode retornar 200 e um JSON com resultados
    assert response.status_code == 200
    data = response.get_json()
    assert data["codigo_projeto"] == codigo
    assert data["comprimento_maximo_m"] > 0
    assert data["numero_emissores"] > 0
    assert "perfil_pressao" in data

    # Error case 400
    payload_bad = {
        "pressao_p0": -1.0,
        "diametro_interno_mm": 16.0,
        "declividade_so": 0.0,
        "h_var_max_m": 2.0
    }
    response_bad = client.post(f'/api/projetos/{codigo}/linha-lateral-trecho', json=payload_bad)
    assert response_bad.status_code == 400

    # Error case 404
    response_404 = client.post('/api/projetos/NAO_EXISTE/linha-lateral-trecho', json=payload)
    assert response_404.status_code == 404
