# backend/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from models.irrigacao import CalculadorIrrigacao

app = Flask(__name__)
CORS(app) # Permite o acesso do Frontend

# Instancia a nossa classe de inteligência agronômica
calculador = CalculadorIrrigacao()

# Banco de dados temporário na memória RAM (Simulado para o início do projeto)
dados_sistema = {
    "ultima_umidade": 65.0,        # Valor padrão inicial (%)
    "temperatura_ambiente": 28.5,  # Graus Celsius simulados
    "ultima_atualizacao": "Nenhum dado recebido ainda"
}

@app.route('/api/status', methods=['GET'])
def obter_status():
    """
    Endpoint que o telefone do agricultor vai chamar para atualizar a tela.
    """
    umidade_atual = dados_sistema["ultima_umidade"]
    analise = calculador.avaliar_status_solo(umidade_atual)
    tempo_estimado = calculador.calcular_tempo_irrigacao(umidade_atual)

    resposta = {
        "umidade_atual": umidade_atual,
        "temperatura_ambiente": dados_sistema["temperatura_ambiente"],
        "status_solo": analise["status"],
        "cor_alerta": analise["cor_alerta"],
        "mensagem_acao": analise["mensagem"],
        "precisa_irrigar": analise["irrigar"],
        "tempo_irrigacao_minutos": tempo_estimado
    }
    return jsonify(resposta), 200

@app.route('/api/sensor', methods=['POST'])
def receber_dados_sensor():
    """
    Endpoint que o dispositivo IoT (ESP32/Arduino) vai chamar no campo para enviar dados.
    """
    dados_recebidos = request.get_json()

    if not dados_recebidos or 'umidade' not in dados_recebidos:
        return jsonify({"erro": "Dados inválidos. O campo 'umidade' é obrigatório."}), 400

    # Atualiza o nosso "banco de dados" na memória
    dados_sistema["ultima_umidade"] = float(dados_recebidos['umidade'])

    if 'temperatura' in dados_recebidos:
        dados_sistema["temperatura_ambiente"] = float(dados_recebidos['temperatura'])

    import datetime
    dados_sistema["ultima_atualizacao"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return jsonify({"status": "sucesso", "mensagem": "Dados atualizados com sucesso!"}), 200

if __name__ == '__main__':
    # Roda o servidor na porta 5000, visível na rede local
    app.run(host='0.0.0.0', port=5000, debug=True)
