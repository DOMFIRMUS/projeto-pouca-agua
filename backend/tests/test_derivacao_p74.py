import pytest
from flask import json
from backend.app import app
from backend.models.irrigacao import CalculadorIrrigacao
from backend.database import init_db, insert_projeto_metadados

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Inicializa o banco de dados e insere o projeto base para os testes
        init_db()
        # Ensure project exists
        insert_projeto_metadados("PROJ-ZITT", "Projeto Zitterell", 100, 100, 2)
        yield client

def test_limites_zitterell():
    # Teste de Limites de Zitterell
    calc = CalculadorIrrigacao()
    # Valores ideais
    resultado_positivo = calc.validar_limites_conector_zitterell(5.0, 5.0, 30.0, 8.0, 2.0, 10000.0)
    assert resultado_positivo['valido'] is True
    assert len(resultado_positivo['alertas']) == 0

    # Valores fora da curva (Vt = 12.0)
    resultado_negativo = calc.validar_limites_conector_zitterell(5.0, 5.0, 30.0, 8.0, 12.0, 10000.0)
    assert resultado_negativo['valido'] is False
    assert len(resultado_negativo['alertas']) == 1
    assert "Vt fora da faixa" in resultado_negativo['alertas'][0]

def test_chaveamento_topografia():
    # Teste Chaveamento de Topografia
    calc = CalculadorIrrigacao()

    # S_o < 0 (Declive negativo)
    res_declive = calc.orquestrar_dimensionamento_derivacao(-0.02, 15.0, 100.0, 2.0, 1.0, 2.0, 2.0)
    assert res_declive['estrategia_dimensionamento'] == 'Método da Divisão em Trechos'

    # S_o >= 0 (Declive positivo)
    res_aclive = calc.orquestrar_dimensionamento_derivacao(0.01, 15.0, 100.0, 2.0, 1.0, 2.0, 2.0)
    assert res_aclive['estrategia_dimensionamento'] == 'Critério de Único Diâmetro'

def test_protecao_critica(client):
    # Teste de Proteção Crítica (Payloads inválidos)
    response = client.post('/api/projetos/PROJ-ZITT/linha-derivacao', json={})
    assert response.status_code == 400

    response = client.post('/api/projetos/PROJ-ZITT/linha-derivacao', json={
        'declividade_derivacao': 0.01
        # faltam outros campos
    })
    assert response.status_code == 400

def test_integracao_api(client):
    # Teste de Integração de API
    payload = {
        'declividade_derivacao': -0.01,
        'pressao_entrada_h': 20.0,
        'comprimento_total_l': 150.0,
        'vazao_ql': 1.5,
        'espacamento_sl': 1.0,
        'distancia_sl1': 2.0,
        'variacao_hvar': 2.0,
        # Zitterell params optional
        'die': 5.0,
        'dis': 5.0,
        'lc': 30.0,
        'dt': 8.0,
        'vt': 2.0,
        'reynolds': 10000.0
    }

    response = client.post('/api/projetos/PROJ-ZITT/linha-derivacao', json=payload)
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data['estrategia_dimensionamento'] == 'Método da Divisão em Trechos'
    assert 'alertas' in data
    assert len(data['alertas']) == 0
