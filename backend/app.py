# backend/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from models.irrigacao import CalculadorIrrigacao
import datetime
from database import init_db, insert_leitura, get_ultima_leitura, update_leitura_status, get_historico

app = Flask(__name__)
CORS(app)

calculador = CalculadorIrrigacao()

# Inicializa o banco de dados
init_db()

# Variáveis do sistema para cálculos
dados_sistema = {
    "mes_atual": 10,                # Outubro (mês crítico de calor)
    "solo_cc": 0.27,                # Capacidade de campo m³/m³ (ex: solo argiloso)
    "solo_pmp": 0.14,               # Ponto de murcha permanente m³/m³
    "profundidade_raiz_m": 0.40,    # Raiz do cultivo atual (0.4 metros)
    "fator_deplecao_f": 0.50,       # Fator f da tabela 6 da tese
    "porcentagem_umedecida_pw": 50.0, # Gotejamento cobre 50% da área
    "espacamento_plantas_m": 0.5,   # Espaçamento entre plantas na fileira
    "espacamento_fileiras_m": 1.0   # Espaçamento entre fileiras
}

@app.route('/api/status', methods=['GET'])
def obter_status():
    ultima_leitura = get_ultima_leitura()

    if not ultima_leitura:
        return jsonify({"erro": "Nenhuma leitura encontrada no banco de dados."}), 404

    temperatura_max = ultima_leitura['temperatura_max']
    temperatura_min = ultima_leitura['temperatura_min']
    umidade_atual = ultima_leitura['umidade']
    leitura_id = ultima_leitura['id']

    # 1. Executa cálculos científicos baseados na Tese
    eto = calculador.calcular_eto_hargreaves(
        temperatura_max,
        temperatura_min,
        latitude=-22.0,
        mes_index=dados_sistema["mes_atual"]
    )

    cad, irn_max = calculador.calcular_irn_e_cad(
        dados_sistema["solo_cc"],
        dados_sistema["solo_pmp"],
        dados_sistema["profundidade_raiz_m"],
        dados_sistema["fator_deplecao_f"],
        dados_sistema["porcentagem_umedecida_pw"]
    )

    # Cálculo do Turno de Rega Máximo (TR_max)
    # Assumindo etc_mm_dia aproximadamente igual a eto para simplificação (Kc = 1.0)
    turno_rega_max_dias = calculador.calcular_turno_rega_max(
        irn_max_mm=irn_max,
        etc_mm_dia=eto,
        sp_m=dados_sistema["espacamento_plantas_m"],
        sr_m=dados_sistema["espacamento_fileiras_m"]
    )

    # 2. Avalia situação atual do sensor
    analise = calculador.avaliar_status_solo(umidade_atual)

    # Cálculo dinâmico do tempo de rega baseado na lâmina necessária (IRN) e ETo
    if analise["irrigar"]:
        # Se precisa irrigar, estima lâmina proporcional ao défice atual
        defice_proporcional = (dados_sistema["solo_cc"] - (umidade_atual/100 * dados_sistema["solo_cc"]))
        tempo_estimado_minutos = round((defice_proporcional * irn_max * 60) / max(eto, 1), 1)
    else:
        tempo_estimado_minutos = 0.0

    # Atualiza o status e o tempo calculado no banco de dados
    update_leitura_status(leitura_id, analise["status"], max(tempo_estimado_minutos, 0.0))

    return jsonify({
        "umidade_atual": umidade_atual,
        "status_solo": analise["status"],
        "cor_alerta": analise["cor_alerta"],
        "mensagem_acao": analise["mensagem"],
        "precisa_irrigar": analise["irrigar"],
        "turno_rega_max_dias": turno_rega_max_dias,
        "metricas_tese": {
            "evapotranspiracao_referencia_mm_dia": eto,
            "capacidade_agua_disponivel_solo_mm": cad,
            "irrigacao_real_necessaria_max_mm": irn_max,
            "tempo_irrigacao_calculado_minutos": max(tempo_estimado_minutos, 0.0)
        }
    }), 200

@app.route('/api/sensor', methods=['POST'])
def receber_dados_sensor():
    dados_recebidos = request.get_json()
    if not dados_recebidos or 'umidade' not in dados_recebidos:
        return jsonify({"erro": "O campo 'umidade' é obrigatório."}), 400

    umidade = float(dados_recebidos['umidade'])

    # Obtém as temperaturas da última leitura se não forem enviadas
    ultima_leitura = get_ultima_leitura()

    temperatura_max = 31.0 # Valor padrão caso seja a primeira leitura
    temperatura_min = 19.0 # Valor padrão caso seja a primeira leitura

    if ultima_leitura:
        temperatura_max = ultima_leitura['temperatura_max']
        temperatura_min = ultima_leitura['temperatura_min']

    if 'temperatura_max' in dados_recebidos:
        temperatura_max = float(dados_recebidos['temperatura_max'])
    if 'temperatura_min' in dados_recebidos:
        temperatura_min = float(dados_recebidos['temperatura_min'])

    insert_leitura(umidade, temperatura_max, temperatura_min)

    return jsonify({"status": "sucesso", "mensagem": "Métricas de campo atualizadas e inseridas no banco de dados."}), 200

@app.route('/api/historico', methods=['GET'])
def obter_historico():
    historico = get_historico()
    return jsonify(historico), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)