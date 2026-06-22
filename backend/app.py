# backend/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from models.irrigacao import CalculadorIrrigacao
import datetime
from database import init_db, insert_leitura, get_ultima_leitura, update_leitura_status, get_historico, seed_culturas, get_culturas, get_projeto_metadados, get_bancos, insert_banco, delete_banco, insert_projeto



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
    "espacamento_fileiras_m": 1.0,   # Espaçamento entre fileiras
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

    ce_agua_ds_m = request.args.get('ce_agua_ds_m', default=0.5, type=float)
    metodo_eto = request.args.get('metodo_eto', 'hargreaves')
    calc = _calcular_engenharia(temperatura_max, temperatura_min, umidade_atual, ce_agua_ds_m, metodo_eto)

    # Atualiza o status e o tempo calculado no banco de dados
    update_leitura_status(
        leitura_id,
        calc["analise"]["status"],
        calc["tempo_irrigacao_calculado_minutos"],
        calc["eto"],
        calc["cad"],
        calc["irn_max"],
        calc["comprimento_lateral_m"],
        calc["perda_carga_total_mca"]
    )

    alerta_salinidade = None
    if culturas:
        cultura_ativa = culturas[0]
        verificacao = calculador.verificar_limite_salinidade(ce_agua_ds_m, cultura_ativa['nome'])
        if verificacao.get("salinidade_critica"):
            alerta_salinidade = verificacao

    # Raio Umedecido Check
    se = request.args.get('se', request.args.get('espacamento_m', dados_sistema.get("espacamento_plantas_sp", 0.5)), type=float)
    q = request.args.get('q', dados_sistema.get("vazao_emissor_qa", 2.0), type=float)
    ko = request.args.get('ko', 15.0, type=float) # Default condutividade if not given
    alpha = request.args.get('alpha', 1.0, type=float) # Default alpha if not given

    if ce_agua_ds_m > min_ce:
        calc["analise"]["mensagem"] += " Alerta: Ocorrerá decréscimo na produtividade."

    raio_umedecido_info = calculador.calcular_raio_umedecido(alpha, q, ko, se)

    response_json = {
        "umidade_atual": umidade_atual,
        "status_solo": calc["analise"]["status"],
        "cor_alerta": calc["analise"]["cor_alerta"],
        "mensagem_acao": calc["analise"]["mensagem"],
        "precisa_irrigar": calc["analise"]["irrigar"],
        "kc_atual": kc_atual,
        "agenda_rega": calc["agenda_rega"],
        "turno_rega_max_dias": calc["turno_rega_max_dias"],
        "lamina_bruta_irrigacao_mm": calc["itn"],
        "metricas_tese": {
            "evapotranspiracao_referencia_mm_dia": calc["eto"],
            "capacidade_agua_disponivel_solo_mm": calc["cad"],
            "irrigacao_real_necessaria_max_mm": calc["irn_max"],
            "tempo_irrigacao_horas": calc["ti_horas"],
            "numero_emissores_por_planta": calc["np_emissores"],
            "tempo_irrigacao_calculado_minutos": calc["tempo_irrigacao_calculado_minutos"],
            "fracao_lixiviacao": calc["fl"],
            "irrigacao_total_necessaria_mm": calc["itn"],
            "deficit_pressao_vapor_kpa": calc.get("deficit_pressao_vapor_kpa", 0.0)
        }
    }

    if alerta_salinidade:
        resposta_json.update(alerta_salinidade)

    return jsonify(resposta_json), 200
    if raio_umedecido_info.get("alerta_faixa_descontinua"):
        response_json["alerta_faixa_descontinua"] = True
        response_json["mensagem_faixa"] = "Afastamento excessivo entre gotejadores. A faixa contínua de humidade será rompida, prejudicando as raízes."

    return jsonify(response_json), 200

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

    calc = _calcular_engenharia(temperatura_max, temperatura_min, umidade, 0.5)

    insert_leitura(
        umidade,
        temperatura_max,
        temperatura_min,
        calc["eto"],
        calc["cad"],
        calc["irn_max"],
        calc["comprimento_lateral_m"],
        calc["perda_carga_total_mca"]
    )

    return jsonify({"status": "sucesso", "mensagem": "Métricas de campo atualizadas e inseridas no banco de dados."}), 200

@app.route('/api/historico', methods=['GET'])
def obter_historico():
    historico = get_historico()
    return jsonify(historico), 200


@app.route('/api/culturas', methods=['GET'])
def obter_culturas():
    culturas = get_culturas()
    return jsonify(culturas), 200

@app.route('/api/bancos', methods=['GET', 'POST'])
def gerenciar_bancos():
    if request.method == 'GET':
        try:
            bancos = get_bancos()
            return jsonify(bancos), 200
        except Exception as e:
            return jsonify({"erro": str(e)}), 500

    if request.method == 'POST':
        try:
            dados = request.get_json()
            if not dados or 'nome' not in dados or 'taxa_mensal' not in dados:
                return jsonify({"erro": "Nome e taxa_mensal são obrigatórios"}), 400

            banco_id = insert_banco(dados['nome'], float(dados['taxa_mensal']))
            return jsonify({"mensagem": "Banco cadastrado com sucesso", "id": banco_id}), 201
        except Exception as e:
            return jsonify({"erro": str(e)}), 500

@app.route('/api/bancos/<int:banco_id>', methods=['DELETE'])
def remover_banco(banco_id):
    try:
        delete_banco(banco_id)
        return jsonify({"mensagem": "Banco removido com sucesso"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route('/api/hidraulica', methods=['POST'])
def processar_hidraulica():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    tem_perfil = any(k in dados for k in ['So', 'k_linha', 'L_estimado'])
    tem_perda = any(k in dados for k in ['diametro_mm', 'vazao_gotejador_lh', 'espacamento_m', 'comprimento_m'])

    if not tem_perfil and not tem_perda:
        return jsonify({"erro": "Nenhum parâmetro válido enviado."}), 400

    resultado_final = {}

    if tem_perfil:
        if 'So' not in dados or 'k_linha' not in dados or 'L_estimado' not in dados:
            return jsonify({"erro": "Os campos 'So', 'k_linha' e 'L_estimado' são obrigatórios."}), 400
        try:
            So = float(dados['So'])
            k_linha = float(dados['k_linha'])
            L_estimado = float(dados['L_estimado'])
            classificacao = calculador.classificar_perfil_pressao(So, k_linha, L_estimado)
            resultado_final["classificacao"] = classificacao
        except ValueError:
            return jsonify({"erro": "Os valores de 'So', 'k_linha' e 'L_estimado' devem ser numéricos."}), 400

    if tem_perda:
        campos_obrigatorios = ['diametro_mm', 'vazao_gotejador_lh', 'espacamento_m', 'comprimento_m']
        for campo in campos_obrigatorios:
            if campo not in dados:
                return jsonify({"erro": f"O campo '{campo}' é obrigatório."}), 400
        try:
            diametro_mm = float(dados['diametro_mm'])
            vazao_gotejador_lh = float(dados['vazao_gotejador_lh'])
            espacamento_m = float(dados['espacamento_m'])
            comprimento_m = float(dados['comprimento_m'])
            resultado = calculador.calcular_perda_carga(diametro_mm, vazao_gotejador_lh, espacamento_m, comprimento_m)
            if "erro" in resultado:
                return jsonify(resultado), 400
            resultado_final.update(resultado)
        except ValueError:
            return jsonify({"erro": "Todos os parâmetros devem ser números válidos."}), 400

    return jsonify(resultado_final), 200

@app.route('/api/projetos', methods=['POST'])
def criar_projeto():
    dados = request.get_json()
    if not dados or 'codigo_projeto' not in dados:
        return jsonify({"erro": "O campo 'codigo_projeto' é obrigatório."}), 400

    from backend.database import get_projeto_metadados, insert_projeto
    projeto_existente = get_projeto_metadados(dados['codigo_projeto'])

    if projeto_existente:
        return jsonify({"erro": "Este Código já existe"}), 400

    sucesso = insert_projeto(dados)
    if not sucesso:
        return jsonify({"erro": "Este Código já existe"}), 400

    return jsonify({"status": "sucesso", "mensagem": "Projeto criado com sucesso"}), 201

@app.route('/api/relatorio-dimensionamento', methods=['GET'])
def relatorio_dimensionamento():
    ultima_leitura = get_ultima_leitura()
    if not ultima_leitura:
        return jsonify({"erro": "Nenhuma leitura encontrada no banco de dados."}), 404

    temperatura_max = ultima_leitura['temperatura_max']
    temperatura_min = ultima_leitura['temperatura_min']
    umidade_atual = ultima_leitura['umidade']

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

    turno_rega_max_dias = calculador.calcular_turno_rega_max(
        irn_max_mm=irn_max,
        etc_mm_dia=eto,
        sp_m=dados_sistema["espacamento_plantas_m"],
        sr_m=dados_sistema["espacamento_fileiras_m"]
    )

    ce_agua_ds_m = request.args.get('ce_agua_ds_m', default=0.5, type=float)

    fl, itn = calculador.calcular_itn(
        irn_max,
        ce_agua_ds_m,
        dados_sistema["ce_solo_min"],
        dados_sistema["ce_solo_max"],
        dados_sistema["uniformidade_emissao_decimal"]
    )

    # Hydraulic variables
    diametro_m = 0.016
    diametro_mm = 16.0
    vazao_emissor_lh = dados_sistema["vazao_emissor_qa"]
    vazao_emissor_m3s = vazao_emissor_lh / 3600000.0
    espacamento_m = dados_sistema["espacamento_plantas_m"]
    pressao_entrada_mca = 10.0
    declividade = 0.0
    hvar_max = pressao_entrada_mca * 0.20

    comprimento_maximo = calculador.comprimento_trecho_a_trecho(
        diametro_m=diametro_m,
        vazao_emissor_m3s=vazao_emissor_m3s,
        espacamento_m=espacamento_m,
        pressao_entrada_mca=pressao_entrada_mca,
        declividade=declividade,
        hvar_max=hvar_max
    )

    resultado_perda = calculador.calcular_perda_carga(
        diametro_mm=diametro_mm,
        vazao_gotejador_lh=vazao_emissor_lh,
        espacamento_m=espacamento_m,
        comprimento_m=comprimento_maximo
    )
    perda_carga_total = resultado_perda.get('perda_carga_mca', 0.0)

    # Derivation line variables
    fator_atrito_f = 0.04
    vazao_trecho_q = vazao_emissor_m3s * (comprimento_maximo / espacamento_m)
    desnivel_trecho_dz = 1.0
    comprimento_trecho_L = 50.0
    h0 = 10.0

    diametro_derivacao = calculador.dimensionar_diametro_trecho(
        fator_atrito_f=fator_atrito_f,
        vazao_trecho_q=vazao_trecho_q,
        desnivel_trecho_dz=desnivel_trecho_dz,
        comprimento_trecho_L=comprimento_trecho_L,
        h0=h0
    )

    diametro_derivacao_mm = diametro_derivacao * 1000

    alertas = []
    if perda_carga_total > (pressao_entrada_mca * 0.20):
        alertas.append("Variação de pressão ultrapassa 20% do recomendado.")
    if fl > 0:
        alertas.append(f"A salinidade da água exige lavagem do solo. Fração de Lixiviação: {fl * 100:.2f}%")

    relatorio_compra = {
        "eto": f"{eto:.2f} mm/dia",
        "kc_atual": f"{kc_atual:.2f}",
        "irrigacao_total_necessaria": f"{itn:.2f} mm",
        "turno_rega_maximo": f"{turno_rega_max_dias} dias",
        "comprimento_maximo_lateral": f"{comprimento_maximo:.2f} m",
        "perda_carga_total": f"{perda_carga_total:.2f} mca",
        "diametro_sugerido_derivacao": f"{diametro_derivacao_mm:.2f} mm",
        "alertas": alertas
    }

    return jsonify({"relatorio_compra": relatorio_compra}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
