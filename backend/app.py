# backend/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from models.irrigacao import CalculadorIrrigacao
import datetime

app = Flask(__name__)
CORS(app)

calculador = CalculadorIrrigacao()

# Estado inicial simulando sensores de campo e dados do agricultor
dados_sistema = {
    "ultima_umidade": 45.0,         # Solo atualmente em nível de atenção
    "temperatura_max": 31.0,        # Clima local para cálculo de ETo
    "temperatura_min": 19.0,
    "mes_atual": 10,                # Outubro (mês crítico de calor)
    "solo_cc": 0.27,                # Capacidade de campo m³/m³ (ex: solo argiloso)
    "solo_pmp": 0.14,               # Ponto de murcha permanente m³/m³
    "profundidade_raiz_m": 0.40,    # Raiz do cultivo atual (0.4 metros)
    "fator_deplecao_f": 0.50,       # Fator f da tabela 6 da tese
    "porcentagem_umedecida_pw": 50.0 # Gotejamento cobre 50% da área
}

@app.route('/api/status', methods=['GET'])
def obter_status():
    # 1. Executa cálculos científicos baseados na Tese
    eto = calculador.calcular_eto_hargreaves(
        dados_sistema["temperatura_max"],
        dados_sistema["temperatura_min"],
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

    # 2. Avalia situação atual do sensor
    umidade_atual = dados_sistema["ultima_umidade"]
    analise = calculador.avaliar_status_solo(umidade_atual)

    # Cálculo dinâmico do tempo de rega baseado na lâmina necessária (IRN) e ETo
    if analise["irrigar"]:
        # Se precisa irrigar, estima lâmina proporcional ao défice atual
        defice_proporcional = (dados_sistema["solo_cc"] - (umidade_atual/100 * dados_sistema["solo_cc"]))
        tempo_estimado_minutos = round((defice_proporcional * irn_max * 60) / max(eto, 1), 1)
    else:
        tempo_estimado_minutos = 0.0

    return jsonify({
        "umidade_atual": umidade_atual,
        "status_solo": analise["status"],
        "cor_alerta": analise["cor_alerta"],
        "mensagem_acao": analise["mensagem"],
        "precisa_irrigar": analise["irrigar"],
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

    dados_sistema["ultima_umidade"] = float(dados_recebidos['umidade'])
    if 'temperatura_max' in dados_recebidos:
        dados_sistema["temperatura_max"] = float(dados_recebidos['temperatura_max'])
    if 'temperatura_min' in dados_recebidos:
        dados_sistema["temperatura_min"] = float(dados_recebidos['temperatura_min'])

    return jsonify({"status": "sucesso", "mensagem": "Métricas de campo atualizadas."}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)