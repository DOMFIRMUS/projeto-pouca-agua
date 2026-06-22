# backend/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from models.irrigacao import CalculadorIrrigacao
import datetime
from database import obter_projeto_por_codigo, obter_resumo_hidraulico, init_db, insert_leitura, get_ultima_leitura, update_leitura_status, get_historico, seed_culturas, get_culturas, insert_projeto, get_projeto_metadados, get_bancos, insert_banco, delete_banco, insert_projeto_metadados

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
    codigo_projeto = request.args.get('codigo_projeto', None)
    calc = _calcular_engenharia(temperatura_max, temperatura_min, umidade_atual, ce_agua_ds_m, metodo_eto, codigo_projeto)

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


    raio_umedecido_info = calculador.calcular_raio_umedecido(alpha, q, ko, se)

    if alerta_salinidade and alerta_salinidade.get("salinidade_critica"):
        calc["analise"]["mensagem"] += " Alerta: Ocorrerá decréscimo na produtividade."
    elif ce_agua_ds_m > dados_sistema["ce_solo_min"]:
        calc["analise"]["mensagem"] += " Alerta: Ocorrerá decréscimo na produtividade."

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
            "delta_kPa": calc["delta_kPa"],
            "pressao_atm_kPa": calc["pressao_atm_kPa"],
        }
    }

    if alerta_salinidade:
        response_json.update(alerta_salinidade)

    if raio_umedecido_info.get("alerta_faixa_descontinua"):
        response_json["alerta_faixa_descontinua"] = True
        response_json["mensagem_faixa"] = "Afastamento excessivo entre gotejadores. A faixa contínua de humidade será rompida, prejudicando as raízes."
    elif raio_umedecido_info.get("alerta"):
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

    codigo_projeto = dados_recebidos.get('codigo_projeto', None)
    calc = _calcular_engenharia(temperatura_max, temperatura_min, umidade, 0.5, codigo_projeto=codigo_projeto)

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

    has_advanced = any(key in dados for key in ['declividade', 'So', 'k_linha', 'L_estimado', 'H', 'Hvar'])
    has_basic = all(key in dados for key in ['diametro_mm', 'vazao_gotejador_lh', 'espacamento_m', 'comprimento_m'])

    if not has_advanced and not has_basic:
        if any(key in dados for key in ['So', 'k_linha', 'L_estimado']):
             return jsonify({"erro": "Os campos 'So', 'k_linha' e 'L_estimado' são obrigatórios."}), 400
        return jsonify({"erro": "Faltam parâmetros básicos (diametro_mm, etc) ou avançados (So, k_linha, etc)."}), 400

    resposta = {}

    if has_advanced:
        if 'So' not in dados or 'k_linha' not in dados or 'L_estimado' not in dados:
             return jsonify({"erro": "Os campos 'So', 'k_linha' e 'L_estimado' são obrigatórios."}), 400
        try:
            So = float(dados['So'])
            k_linha = float(dados['k_linha'])
            L_estimado = float(dados['L_estimado'])

            classificacao = calculador.classificar_perfil_pressao(So, k_linha, L_estimado)
            resposta["classificacao"] = classificacao

            if classificacao == 'Perfil Tipo IId (Declive Muito Forte)' and 'H' in dados and 'Hvar' in dados:
                H = float(dados['H'])
                Hvar = float(dados['Hvar'])
                L_max = calculador.calcular_lmax_perfil_tipo_IId(H, Hvar, So, k_linha, L_estimado)
                resposta["L_max"] = round(L_max, 2)
        except ValueError as e:
            if "Restrição de limite físico não atendida" in str(e):
                 return jsonify({"erro": str(e)}), 400
            return jsonify({"erro": "Os valores do fluxo avançado devem ser numéricos."}), 400

    if has_basic:
        try:
            diametro_mm = float(dados['diametro_mm'])
            vazao_gotejador_lh = float(dados['vazao_gotejador_lh'])
            espacamento_m = float(dados['espacamento_m'])
            comprimento_m = float(dados['comprimento_m'])

            resultado_basico = calculador.calcular_perda_carga(
                diametro_mm, vazao_gotejador_lh, espacamento_m, comprimento_m
            )
            if "erro" in resultado_basico:
                return jsonify(resultado_basico), 400
            resposta.update(resultado_basico)
        except ValueError:
            return jsonify({"erro": "Todos os parâmetros básicos devem ser números válidos."}), 400

    if not has_advanced and not has_basic:
         return jsonify({"erro": "Parâmetros insuficientes para realizar cálculos hidráulicos."}), 400

    return jsonify(resposta), 200

@app.route('/api/projetos', methods=['POST'])
def salvar_projeto_metadados():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    campos_obrigatorios = ['codigo_projeto', 'nome_projeto', 'largura', 'altura', 'profundidade']
    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({"erro": f"O campo '{campo}' é obrigatório."}), 400

    sucesso = insert_projeto_metadados(
        dados['codigo_projeto'],
        dados['nome_projeto'],
        int(dados['largura']),
        int(dados['altura']),
        int(dados['profundidade'])
    )

    if sucesso:
        return jsonify({"status": "sucesso", "mensagem": "Projeto salvo com sucesso"}), 201
    else:
        return jsonify({"erro": "O código do projeto já existe (restrição de unicidade)."}), 409


    nome_codigo_subunidade = dados.get('nome_codigo_subunidade')
    area_total_irrigada = dados.get('area_total_irrigada')

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


@app.route('/api/projetos/<string:codigo_projeto>', methods=['GET'])
def abrir_projeto(codigo_projeto):
    projeto = obter_projeto_por_codigo(codigo_projeto)
    if projeto:
        return jsonify(projeto), 200
    else:
        return jsonify({"erro": "Projeto não encontrado"}), 404

@app.route('/api/projetos/<string:codigo_projeto>/resumo', methods=['GET'])
def consolidacao_resultados(codigo_projeto):
    resumo_hidraulico = obter_resumo_hidraulico(codigo_projeto)

    if resumo_hidraulico:
        comp_lateral = resumo_hidraulico.get('comprimento_lateral_m', 'Dados não simulados')
        perda_carga = resumo_hidraulico.get('perda_carga_total_mca', 'Dados não simulados')

        return jsonify({
            "comprimento_maximo_lateral": comp_lateral,
            "diametros_linha_derivacao": "Dados não simulados",
            "perda_carga_linha_lateral": perda_carga,
            "perda_carga_linha_derivacao": "Dados não simulados",
            "perdas_localizadas_carga": "Dados não simulados",
            "dimensionamento_subunidade": "Dados não simulados"
        }), 200
    else:
        return jsonify({
            "comprimento_maximo_lateral": "Dados não simulados",
            "diametros_linha_derivacao": "Dados não simulados",
            "perda_carga_linha_lateral": "Dados não simulados",
            "perda_carga_linha_derivacao": "Dados não simulados",
            "perdas_localizadas_carga": "Dados não simulados",
            "dimensionamento_subunidade": "Dados não simulados"
        }), 200

def _calcular_engenharia(temperatura_max, temperatura_min, umidade_atual, ce_agua_ds_m, metodo_eto='hargreaves', codigo_projeto=None):
    from database import get_projeto_metadados
    altitude_z = 0.0
    if codigo_projeto:
        metadados = get_projeto_metadados(codigo_projeto)
        if metadados:
             altitude_z = float(metadados.get('altura', 0.0))
    t_media = (temperatura_max + temperatura_min) / 2

    if metodo_eto.lower() == 'blaney-criddle':
        eto = calculador.calcular_eto_blaney_criddle(
            t_media,
            mes_index=dados_sistema["mes_atual"]
        )
    elif metodo_eto.lower() == 'penman-monteith':
        # Penman-Monteith required inputs, using defaults for robustness if not passed
        rn = float(request.args.get('rn', 15.0))
        g = float(request.args.get('g', 0.0))
        u2 = float(request.args.get('u2', 2.0))
        es = float(request.args.get('es', 3.0))
        ea = float(request.args.get('ea', 1.5))
        delta = float(request.args.get('delta', 0.15))
        gama = float(request.args.get('gama', 0.066))

        eto = calculador.calcular_eto_penman_monteith(
            rn, g, t_media, u2, es, ea, delta, gama
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

    fl, itn = calculador.calcular_itn(
        irn_max,
        ce_agua_ds_m,
        dados_sistema["ce_solo_min"],
        dados_sistema["ce_solo_max"],
        dados_sistema["uniformidade_emissao_decimal"]
    )

    ti_horas, np_emissores = calculador.calcular_tempo_irrigacao(
        itn_mm=itn,
        espacamento_plantas_sp=dados_sistema["espacamento_plantas_m"],
        espacamento_fileiras_sr=dados_sistema["espacamento_fileiras_m"],
        pw_area_umedecida=dados_sistema["porcentagem_umedecida_pw"],
        dw_diametro_molhado=dados_sistema["dw_diametro_molhado"],
        vazao_emissor_qa=dados_sistema["vazao_emissor_qa"]
    )

    tempo_irrigacao_calculado_minutos = int(ti_horas * 60)
    agenda_rega = calculador.fracionar_tempo_irrigacao(ti_horas, 2.0)

    # Simplified hydraulic assumption for the dashboard overview
    diametro_mm = 16.0
    vazao_gotejador_lh = dados_sistema["vazao_emissor_qa"]
    espacamento_m = dados_sistema["espacamento_plantas_m"]
    comprimento_m = 50.0

    resultado_perda = calculador.calcular_perda_carga(
        diametro_mm, vazao_gotejador_lh, espacamento_m, comprimento_m
    )

    analise_solo = calculador.avaliar_status_solo(umidade_atual)

    delta_kPa = calculador.calcular_declividade_delta(t_media)
    pressao_atm_kPa = calculador.calcular_pressao_atmosferica_p(altitude_z)

    return {
        "eto": eto,
        "cad": cad,
        "irn_max": irn_max,
        "ti_horas": ti_horas,
        "np_emissores": np_emissores,
        "tempo_irrigacao_calculado_minutos": tempo_irrigacao_calculado_minutos,
        "agenda_rega": agenda_rega,
        "turno_rega_max_dias": turno_rega_max_dias,
        "fl": fl,
        "itn": itn,
        "analise": analise_solo,
        "comprimento_lateral_m": comprimento_m,
        "perda_carga_total_mca": resultado_perda.get("perda_carga_mca", 0.0),
        "delta_kPa": delta_kPa,
        "pressao_atm_kPa": pressao_atm_kPa
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
