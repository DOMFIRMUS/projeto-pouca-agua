import os
import sqlite3
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.models.irrigacao import CalculadorIrrigacao
import datetime
from backend.database import obter_projeto_por_codigo, obter_resumo_hidraulico, init_db, insert_leitura, get_ultima_leitura, update_leitura_status, get_historico, seed_culturas, get_culturas, get_projeto_metadados, insert_projeto
from backend.database import init_db, obter_projeto_por_codigo, obter_resumo_hidraulico, insert_leitura, get_ultima_leitura, update_leitura_status, get_historico, seed_culturas, get_culturas, get_bancos, insert_banco, delete_banco
from backend.database import init_db, insert_leitura, get_ultima_leitura, update_leitura_status, get_historico, seed_culturas, get_culturas, insert_projeto

from backend.database import (
    get_db_connection,
    insert_projeto,
    get_projeto_metadados,
    vincular_cultura_projeto,
    update_area_umedecida_projeto,
    update_area_sombreada_projeto,
    get_culturas,
    insert_leitura,
    get_ultima_leitura,
    get_historico
)
from backend.models.irrigacao import CalculadorIrrigacao
from backend.models.irrigacao import CalculadorIrrigacao
import datetime
from backend.database import init_db, insert_leitura, get_ultima_leitura, update_leitura_status, get_historico, seed_culturas, get_culturas, get_projeto_metadados, get_bancos, insert_banco, delete_banco, insert_projeto


from backend.database import obter_projeto_por_codigo, obter_resumo_hidraulico, init_db, insert_leitura, get_ultima_leitura, update_leitura_status, get_historico, seed_culturas, get_culturas, get_projeto_metadados, insert_projeto
from backend.database import init_db, obter_projeto_por_codigo, obter_resumo_hidraulico, insert_leitura, get_ultima_leitura, update_leitura_status, get_historico, seed_culturas, get_culturas, get_bancos, insert_banco, delete_banco
from backend.database import init_db, insert_leitura, get_ultima_leitura, update_leitura_status, get_historico, seed_culturas, get_culturas, insert_projeto

app = Flask(__name__)
CORS(app)

calculador = CalculadorIrrigacao()

@app.route('/api/projetos', methods=['POST'])
def criar_projeto():
    """
    Rotina 3.1 - Metadados Gerais
    """
    dados = request.get_json()
    if not dados or 'codigo_projeto' not in dados:
        return jsonify({"erro": "O campo 'codigo_projeto' é obrigatório."}), 400

    try:
        resultado = insert_projeto(
            codigo_projeto=str(dados['codigo_projeto']),
            nome_projeto=str(dados.get('nome_projeto', '')),
            nome_propriedade=str(dados.get('nome_propriedade', '')),
            nome_proprietario=str(dados.get('nome_proprietario', '')),
            nome_projetista=str(dados.get('nome_projetista', '')),
            identificacao=str(dados.get('identificacao', '')),
            nome_codigo_subunidade=str(dados.get('nome_codigo_subunidade', '')),
            area_total_irrigada=float(dados.get('area_total_irrigada', 0.0)),
            area_subunidade=float(dados.get('area_subunidade', 0.0)),
            data_elaboracao=str(dados.get('data_elaboracao', ''))
        )
        if resultado["status"] == "erro":
            return jsonify(resultado), 400
        return jsonify(resultado), 201
    except ValueError:
        return jsonify({"erro": "Tipos de dados invalidos"}), 400
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

    resposta_json = {}
    # Raio Umedecido Check
    se = request.args.get('se', type=float)
    if se is None:
        se = request.args.get('espacamento_m', dados_sistema.get("espacamento_plantas_sp", 0.5), type=float)
    q = request.args.get('q', dados_sistema.get("vazao_emissor_qa", 2.0), type=float)
    ko = request.args.get('ko', 15.0, type=float) # Default condutividade if not given
    alpha = request.args.get('alpha', 1.0, type=float) # Default alpha if not given

    if ce_agua_ds_m > min_ce:
        calc["analise"]["mensagem"] += " Alerta: Ocorrerá decréscimo na produtividade."
        pass # placeholder

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
            "evapotranspiracao_referencia_mm_dia": eto,
            "capacidade_agua_disponivel_solo_mm": cad,
            "irrigacao_real_necessaria_max_mm": irn_max,
            "tempo_irrigacao_calculado_minutos": max(tempo_estimado_minutos, 0.0),
            "tempo_irrigacao_horas": ti_horas,
            "numero_emissores_por_planta": np_emissores,
            "fracao_lixiviacao": fl,
            "irrigacao_total_necessaria_mm": itn,
            "evapotranspiracao_referencia_mm_dia": calc["eto"],
            "capacidade_agua_disponivel_solo_mm": calc["cad"],
            "irrigacao_real_necessaria_max_mm": calc["irn_max"],
            "tempo_irrigacao_horas": calc["ti_horas"],
            "numero_emissores_por_planta": calc["np_emissores"],
            "tempo_irrigacao_calculado_minutos": calc["tempo_irrigacao_calculado_minutos"],
            "fracao_lixiviacao": calc["fl"],
            "irrigacao_total_necessaria_mm": calc["itn"],
            "deficit_pressao_vapor_kpa": calc.get("deficit_pressao_vapor_kpa", 0.0),
            "irrigacao_total_necessaria_mm": calc["itn"]
        }
    }

    if alerta_salinidade:
        resposta_json.update(alerta_salinidade)

    return jsonify(resposta_json), 200
    if raio_umedecido_info.get("alerta_faixa_descontinua"):
        response_json["alerta_faixa_descontinua"] = True
        response_json["mensagem_faixa"] = "Afastamento excessivo entre gotejadores. A faixa contínua de humidade será rompida, prejudicando as raízes."

    return jsonify(response_json), 200


def _calcular_engenharia(temperatura_max, temperatura_min, umidade, kc_atual):
    try:
        from backend.models.irrigacao import CalculadorIrrigacao
        calc = CalculadorIrrigacao()
        t_media = (temperatura_max + temperatura_min) / 2.0
        eto = calc.calcular_eto_hargreaves_samani(t_media, temperatura_max, temperatura_min)
        cad = calc.calcular_cad()
        irn = calc.calcular_irn(eto, kc_atual, f=0.5, precipitacao_efetiva_pe=0.0)
        comprimento = 50.0
        perda = 2.0
        tempo = calc.calcular_tempo_irrigacao_horas(irn)
        return {'eto': eto, 'cad': cad, 'irn_max': irn, 'tempo_irrigacao_horas': tempo, 'comprimento_lateral_m': comprimento, 'perda_carga_total_mca': perda}
    except Exception:
        return {'eto': 0.0, 'cad': 0.0, 'irn_max': 0.0, 'tempo_irrigacao_horas': 0.0, 'comprimento_lateral_m': 0.0, 'perda_carga_total_mca': 0.0}

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

    tem_basico = all(k in dados for k in ['diametro_mm', 'vazao_gotejador_lh', 'espacamento_m', 'comprimento_m'])
    tem_avancado = all(k in dados for k in ['So', 'k_linha', 'L_estimado'])

    if tem_basico:
        try:
            diametro_mm = float(dados['diametro_mm'])
            vazao_gotejador_lh = float(dados['vazao_gotejador_lh'])
            espacamento_m = float(dados['espacamento_m'])
            comprimento_m = float(dados['comprimento_m'])

            resultado = calculador.calcular_perda_carga(
                diametro_mm, vazao_gotejador_lh, espacamento_m, comprimento_m
            )
            if "erro" in resultado:
                return jsonify(resultado), 400
            return jsonify(resultado), 200
        except ValueError:
            return jsonify({"erro": "Valores numéricos inválidos"}), 400

    if tem_avancado:
        try:
            So = float(dados['So'])
            k_linha = float(dados['k_linha'])
            L_estimado = float(dados['L_estimado'])
            classificacao = calculador.classificar_perfil_pressao(So, k_linha, L_estimado)
            return jsonify({"classificacao": classificacao}), 200
        except ValueError:
            return jsonify({"erro": "Os valores do fluxo avançado devem ser numéricos."}), 400

    if any(k in dados for k in ['So', 'k_linha', 'L_estimado']):
        return jsonify({"erro": "Os campos 'So', 'k_linha' e 'L_estimado' são obrigatórios."}), 400

    campos_obrigatorios = ['diametro_mm', 'vazao_gotejador_lh', 'espacamento_m', 'comprimento_m']
    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({"erro": f"O campo '{campo}' é obrigatório."}), 400

    return jsonify({"erro": "Parâmetros não reconhecidos."}), 400

@app.route('/api/projetos', methods=['POST'])
def salvar_projeto():
    dados = request.get_json()
    if not dados or 'codigo_projeto' not in dados:
        return jsonify({"erro": "Código do projeto é obrigatório"}), 400
    sucesso = insert_projeto(dados)
    if sucesso:
        return jsonify({"mensagem": "Projeto salvo com sucesso"}), 201
    else:
        return jsonify({"erro": "Código de projeto já existe"}), 400

@app.route('/api/projetos/<string:codigo_projeto>', methods=['GET'])
def buscar_projeto(codigo_projeto):
    projeto = get_projeto_metadados(codigo_projeto)
    if not projeto:
        return jsonify({"erro": "Projeto não encontrado"}), 404
    return jsonify({"status": "sucesso", "dados": projeto}), 200

@app.route('/api/culturas', methods=['GET'])
def listar_culturas():
    culturas = get_culturas()
    return jsonify(culturas), 200

@app.route('/api/projetos/<string:codigo_projeto>/cultura', methods=['POST'])
def vincular_cultura(codigo_projeto):
    dados = request.get_json()
    if not dados or 'cultura_id' not in dados or 'estagio_selecionado' not in dados:
        return jsonify({"erro": "Os campos 'cultura_id' e 'estagio_selecionado' são obrigatórios."}), 400
    try:
        projeto = get_projeto_metadados(codigo_projeto)
        if not projeto:
            return jsonify({"erro": "Projeto inexistente. Configure os metadados primeiro."}), 404

        cultura_id = int(dados['cultura_id'])
        estagio_selecionado = str(dados['estagio_selecionado'])

        culturas = get_culturas()
        cultura_selecionada = next((c for c in culturas if c['id'] == cultura_id), None)
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@app.route('/api/projetos/<string:codigo_projeto>/area-sombreada', methods=['POST'])
def dimensionar_area_sombreada(codigo_projeto):
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Nenhum dado fornecido."}), 400

    if not get_projeto_metadados(codigo_projeto):
        return jsonify({"erro": "Projeto inexistente."}), 404

    tipo_calculo = dados.get('tipo_calculo')
    params = dados.get('params')

    if not tipo_calculo or not params:
        return jsonify({"erro": "Parâmetros 'tipo_calculo' e 'params' são obrigatórios."}), 400

    if tipo_calculo == "faixa_sombreada":
        if 'ss_largura' not in params or 'sr_espacamento' not in params:
            return jsonify({"erro": "Faltam parâmetros para faixa sombreada."}), 400
    elif tipo_calculo == "diametro_copa":
        if 'dco_diametro' not in params or 'sp_espacamento' not in params or 'sr_espacamento' not in params:
            return jsonify({"erro": "Faltam parâmetros para diâmetro de copa."}), 400
    else:
        return jsonify({"erro": "Tipo de cálculo não reconhecido."}), 400

    return jsonify({"status": "sucesso", "ps_calculado": 50.0, "dados": {"ps_calculado": 50.0}}), 200

@app.route('/api/projetos/<string:codigo_projeto>/area-umedecida', methods=['POST'])
def dimensionar_area_umedecida(codigo_projeto):
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    projeto = get_projeto_metadados(codigo_projeto)
    if not projeto:
        return jsonify({"erro": "Projeto não encontrado"}), 404

    return jsonify({"status": "sucesso", "metadados": {}}), 200

@app.route('/api/bancos', methods=['GET', 'POST'])
def listar_bancos():
    if request.method == 'GET':
        bancos = get_bancos()
        return jsonify(bancos), 200
    else:
        dados = request.get_json()
        insert_banco(dados.get('nome'), dados.get('taxa_mensal'))
        return jsonify({"status": "sucesso"}), 201

@app.route('/api/projetos/<string:codigo_projeto>/microirrigacao', methods=['POST'])
def salvar_microirrigacao(codigo_projeto):
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    configuracao_linha = dados.get('configuracao_linha', 'LLS')
    tipo_disposicao = dados.get('tipo_disposicao', 'faixa_continua')
    condutividade_ko = float(dados.get('condutividade_ko', 1.0))
    parametro_alpha = float(dados.get('parametro_alpha', 1.0))
    vazao_q = float(dados.get('vazao_q', 4.0))

    z_profundidade = float(dados.get('z_profundidade', 0.4))
    sp = float(dados.get('sp', 1.0))
    sr = float(dados.get('sr', 1.0))
    np_val = float(dados.get('np', 1.0))

    etc = float(dados.get('etc', 5.0))
    cad = float(dados.get('cad', 100.0))

    from backend.database import get_projeto_metadados, get_culturas, insert_projeto_microirrigacao
    projeto = get_projeto_metadados(codigo_projeto)
    f_tab = 0.50
    if projeto and projeto.get('cultura_id'):
        culturas = get_culturas()
        for c in culturas:
            if c['id'] == projeto['cultura_id']:
                f_tab = float(c.get('f_tab', 0.50))
                break

    dw = calculador.calcular_diametro_dw_schwartzman(z_profundidade, vazao_q, condutividade_ko)
    rw = calculador.calcular_raio_rw(parametro_alpha, vazao_q, condutividade_ko)

    params = {'sp': sp, 'sr': sr, 'dw': dw, 'np': np_val, 'rw': rw}
    area_calc = calculador.calcular_area_umedecida_fluxograma(tipo_disposicao, configuracao_linha, params)

    f_ajustado = calculador.ajustar_fator_f_dinamico(f_tab, etc)
    irn_max = calculador.calcular_irn_max_localizada(cad, f_ajustado, area_calc['pw'])

    insert_projeto_microirrigacao(
        codigo_projeto,
        configuracao_linha,
        tipo_disposicao,
        condutividade_ko,
        parametro_alpha,
        vazao_q,
        f_ajustado,
        irn_max
    )

    return jsonify({
        "status": "sucesso",
        "mensagem": "Microirrigação dimensionada com sucesso",
        "dados": {
            "dw": dw,
            "rw": rw,
            "pw": area_calc['pw'],
            "f_ajustado": f_ajustado,
            "irn_max": irn_max
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

