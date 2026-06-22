# backend/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from models.irrigacao import CalculadorIrrigacao
import datetime
from database import init_db, insert_leitura, get_ultima_leitura, update_leitura_status, get_historico, seed_culturas, get_culturas, insert_projeto

app = Flask(__name__)
CORS(app)

calculador = CalculadorIrrigacao()

# Inicializa o banco de dados
init_db()
seed_culturas()

# Variáveis do sistema para cálculos
dados_sistema = {
    "mes_atual": 10,                # Outubro (mês crítico de calor)
    "solo_cc": 0.27,                # Capacidade de campo m³/m³ (ex: solo argiloso)
    "solo_pmp": 0.14,               # Ponto de murcha permanente m³/m³
    "profundidade_raiz_m": 0.40,    # Raiz do cultivo atual (0.4 metros)
    "fator_deplecao_f": 0.50,       # Fator f da tabela 6 da tese
    "porcentagem_umedecida_pw": 50.0, # Gotejamento cobre 50% da área
    "espacamento_plantas_sp": 0.5,
    "espacamento_fileiras_sr": 1.0,
    "dw_diametro_molhado": 0.3,
    "vazao_emissor_qa": 2.0,
    "espacamento_plantas_m": 0.5,   # Espaçamento entre plantas na fileira
    "espacamento_fileiras_m": 1.0,  # Espaçamento entre fileiras
    "ce_solo_min": 1.0,             # Condutividade elétrica mínima do solo suportada (dS/m) - padrão
    "ce_solo_max": 3.0,             # Condutividade elétrica máxima tolerada pela cultura (dS/m)
    "uniformidade_emissao_decimal": 0.90 # Uniformidade de emissão do gotejador (90%)
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

    culturas = get_culturas()
    kc_atual = 1.0 # Default fallback
    if culturas:
        cultura_ativa = culturas[0]
        kc_atual = calculador.obter_kc_atual(
            data_plantio=cultura_ativa['data_plantio'],
            dias_fases={
                'inicial': cultura_ativa['dias_fase_inicial'],
                'meia_estacao': cultura_ativa['dias_meia_estacao'],
                'final': cultura_ativa['dias_fase_final']
            },
            kc_valores={
                'inicial': cultura_ativa['kc_inicial'],
                'media': cultura_ativa['kc_media'],
                'final': cultura_ativa['kc_final']
            }
        )

    # 1. Executa cálculos científicos baseados na Tese
    metodo_eto = request.args.get('metodo_eto', 'hargreaves')
    t_media = (temperatura_max + temperatura_min) / 2

    if metodo_eto.lower() == 'blaney-criddle':
        eto = calculador.calcular_eto_blaney_criddle(
            t_media,
            mes_index=dados_sistema["mes_atual"]
        )
    else:
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
        dados_sistema["porcentagem_umedecida_pw"],
        etc_calculada=eto
    )

    # Cálculo do Turno de Rega Máximo (TR_max)
    # Assumindo etc_mm_dia aproximadamente igual a eto para simplificação (Kc = 1.0)
    turno_rega_max_dias = calculador.calcular_turno_rega_max(
        irn_max_mm=irn_max,
        etc_mm_dia=eto,
        sp_m=dados_sistema["espacamento_plantas_m"],
        sr_m=dados_sistema["espacamento_fileiras_m"]
    )
    # Verifica se foi enviada a condutividade elétrica da água via query params
    ce_agua_ds_m = request.args.get('ce_agua_ds_m', default=0.5, type=float)

    fl, itn = calculador.calcular_itn(
        irn_max,
        ce_agua_ds_m,
        dados_sistema["ce_solo_min"],
        dados_sistema["ce_solo_max"],
        dados_sistema["uniformidade_emissao_decimal"]
    )

    # 2. Avalia situação atual do sensor
    analise = calculador.avaliar_status_solo(umidade_atual)

    # Cálculo dinâmico do tempo de rega baseado na lâmina necessária (IRN) e ETo
    if analise["irrigar"]:
        # Se precisa irrigar, estima lâmina proporcional ao défice atual usando o ITN ao invés do irn_max
        defice_proporcional = (dados_sistema["solo_cc"] - (umidade_atual/100 * dados_sistema["solo_cc"]))
        tempo_estimado_minutos = round((defice_proporcional * irn_max * 60) / max(eto, 1), 1)
        itn_mm = defice_proporcional * irn_max
        tempo_estimado_minutos = round((defice_proporcional * itn * 60) / max(eto, 1), 1)
    else:
        tempo_estimado_minutos = 0.0
        itn_mm = 0.0

    ti_horas, np_emissores = calculador.calcular_tempo_irrigacao(
        itn_mm,
        dados_sistema["espacamento_plantas_sp"],
        dados_sistema["espacamento_fileiras_sr"],
        dados_sistema["porcentagem_umedecida_pw"],
        dados_sistema["dw_diametro_molhado"],
        dados_sistema["vazao_emissor_qa"]
    )

    tempo_irrigacao_calculado_minutos = max(tempo_estimado_minutos, 0.0)

    # Fracionamento do tempo de irrigação
    tempo_irrigacao_horas = tempo_irrigacao_calculado_minutos / 60.0
    agenda_rega = calculador.fracionar_tempo_irrigacao(tempo_irrigacao_horas)

    # Atualiza o status e o tempo calculado no banco de dados
    update_leitura_status(leitura_id, analise["status"], tempo_irrigacao_calculado_minutos)

    return jsonify({
        "umidade_atual": umidade_atual,
        "status_solo": analise["status"],
        "cor_alerta": analise["cor_alerta"],
        "mensagem_acao": analise["mensagem"],
        "precisa_irrigar": analise["irrigar"],
        "kc_atual": kc_atual,
        "agenda_rega": agenda_rega,
        "turno_rega_max_dias": turno_rega_max_dias,
        "lamina_bruta_irrigacao_mm": itn,
        "metricas_tese": {
            "evapotranspiracao_referencia_mm_dia": eto,
            "capacidade_agua_disponivel_solo_mm": cad,
            "irrigacao_real_necessaria_max_mm": irn_max,
            "tempo_irrigacao_calculado_minutos": max(tempo_estimado_minutos, 0.0),
            "tempo_irrigacao_horas": ti_horas,
            "numero_emissores_por_planta": np_emissores,
            "fracao_lixiviacao": fl,
            "irrigacao_total_necessaria_mm": itn
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

@app.route('/api/hidraulica', methods=['POST'])
def hidraulica():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    campos_obrigatorios = ['diametro_mm', 'vazao_gotejador_lh', 'espacamento_m', 'comprimento_m']

    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({"erro": f"O campo '{campo}' é obrigatório."}), 400

    try:
        diametro_mm = float(dados['diametro_mm'])
        vazao_gotejador_lh = float(dados['vazao_gotejador_lh'])
        espacamento_m = float(dados['espacamento_m'])
        comprimento_m = float(dados['comprimento_m'])
    except ValueError:
        return jsonify({"erro": "Todos os parâmetros devem ser números válidos."}), 400

    resultado = calculador.calcular_perda_carga(
        diametro_mm,
        vazao_gotejador_lh,
        espacamento_m,
        comprimento_m
    )

    if "erro" in resultado:
        return jsonify(resultado), 400

    return jsonify(resultado), 200
@app.route('/api/culturas', methods=['GET'])
def obter_culturas():
    culturas = get_culturas()
    return jsonify(culturas), 200

@app.route('/api/classificar_perfil', methods=['POST'])
def classificar_perfil():
    dados_recebidos = request.get_json()
    if not dados_recebidos or 'So' not in dados_recebidos or 'k_linha' not in dados_recebidos or 'L_estimado' not in dados_recebidos:
        return jsonify({"erro": "Os campos 'So', 'k_linha' e 'L_estimado' são obrigatórios."}), 400

    try:
        So = float(dados_recebidos['So'])
        k_linha = float(dados_recebidos['k_linha'])
        L_estimado = float(dados_recebidos['L_estimado'])
    except ValueError:
        return jsonify({"erro": "Os valores de 'So', 'k_linha' e 'L_estimado' devem ser numéricos."}), 400

    classificacao = calculador.classificar_perfil_pressao(So, k_linha, L_estimado)

    return jsonify({"classificacao": classificacao}), 200

@app.route('/api/projetos', methods=['POST'])
def criar_projeto():
    dados = request.get_json()
    if not dados or 'codigo_projeto' not in dados:
        return jsonify({"erro": "O campo 'codigo_projeto' é obrigatório."}), 400

    sucesso = insert_projeto(dados)

    if not sucesso:
        return jsonify({"erro": "Este Código já existe"}), 400

    return jsonify({"status": "sucesso", "mensagem": "Projeto criado com sucesso"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)