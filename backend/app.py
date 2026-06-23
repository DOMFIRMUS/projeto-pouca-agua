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
from models.irrigacao import CalculadorIrrigacao
import datetime
from database import init_db, insert_leitura, get_ultima_leitura, update_leitura_status, get_historico, seed_culturas, get_culturas, get_projeto_metadados, get_bancos, insert_banco, delete_banco, insert_projeto


from database import obter_projeto_por_codigo, obter_resumo_hidraulico, init_db, insert_leitura, get_ultima_leitura, update_leitura_status, get_historico, seed_culturas, get_culturas, get_projeto_metadados, insert_projeto
from database import init_db, obter_projeto_por_codigo, obter_resumo_hidraulico, insert_leitura, get_ultima_leitura, update_leitura_status, get_historico, seed_culturas, get_culturas, get_bancos, insert_banco, delete_banco
from database import init_db, insert_leitura, get_ultima_leitura, update_leitura_status, get_historico, seed_culturas, get_culturas, insert_projeto

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


@app.route('/api/projetos/<string:codigo_projeto>/cultura', methods=['POST'])
def vincular_cultura(codigo_projeto):
    """
    Rotina 2 - Vínculo de Kc
    """
@app.route('/api/hidraulica', methods=['POST'])
def processar_hidraulica():
    pass

@app.route('/api/perda_carga', methods=['POST'])
def perda_carga():
    dados = request.get_json()
    if not dados or 'cultura_id' not in dados or 'estagio_selecionado' not in dados:
        return jsonify({"erro": "Os campos 'cultura_id' e 'estagio_selecionado' são obrigatórios."}), 400

    projeto = get_projeto_metadados(codigo_projeto)
    if not projeto:
        return jsonify({"erro": "Projeto inexistente. Configure os metadados primeiro."}), 404

    try:
        cultura_id = int(dados['cultura_id'])
        estagio_selecionado = str(dados['estagio_selecionado'])

        culturas = get_culturas()
        cultura_selecionada = next((c for c in culturas if c['id'] == cultura_id), None)
    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    tem_perfil = any(k in dados for k in ['So', 'k_linha', 'L_estimado'])
    # Branch logic based on the incoming JSON payload parameters
    if any(k in dados for k in ['So', 'k_linha', 'L_estimado']):
        if not ('So' in dados and 'k_linha' in dados and 'L_estimado' in dados):
            return jsonify({"erro": "Os campos 'So', 'k_linha' e 'L_estimado' são obrigatórios."}), 400

        try:
            So = float(dados['So'])
            k_linha = float(dados['k_linha'])
            L_estimado = float(dados['L_estimado'])
        except ValueError:
            return jsonify({"erro": "Os valores de 'So', 'k_linha' e 'L_estimado' devem ser numéricos."}), 400

        classificacao = calculador.classificar_perfil_pressao(So, k_linha, L_estimado)
        return jsonify({"classificacao": classificacao}), 200

    else:
        campos_obrigatorios = ['diametro_mm', 'vazao_gotejador_lh', 'espacamento_m', 'comprimento_m']

    # Determina o fluxo de cálculo com base nos campos recebidos
    if 'So' in dados or 'k_linha' in dados or 'L_estimado' in dados:
        if not ('So' in dados and 'k_linha' in dados and 'L_estimado' in dados):
            return jsonify({"erro": "Os campos 'So', 'k_linha' e 'L_estimado' são obrigatórios."}), 400

        try:
            So = float(dados['So'])
            k_linha = float(dados['k_linha'])
            L_estimado = float(dados['L_estimado'])
        except ValueError:
            return jsonify({"erro": "Os valores de 'So', 'k_linha' e 'L_estimado' devem ser numéricos."}), 400

        classificacao = calculador.classificar_perfil_pressao(So, k_linha, L_estimado)
        return jsonify({"classificacao": classificacao}), 200

    if 'So' in dados_recebidos and 'k_linha' in dados_recebidos and 'L_estimado' in dados_recebidos:
        try:
            So = float(dados_recebidos['So'])
            k_linha = float(dados_recebidos['k_linha'])
            L_estimado = float(dados_recebidos['L_estimado'])
        except ValueError:
            return jsonify({"erro": "Os valores de 'So', 'k_linha' e 'L_estimado' devem ser numéricos."}), 400

    resultado_final = {}

    tem_dados_basicos = all(campo in dados for campo in ['diametro_mm', 'vazao_gotejador_lh', 'espacamento_m', 'comprimento_m'])
    tem_dados_topograficos = all(campo in dados for campo in ['So', 'k_linha', 'L_estimado'])

    if not tem_dados_basicos and not tem_dados_topograficos:
        return jsonify({"erro": "Dados insuficientes. Envie os parâmetros básicos (diametro_mm, vazao_gotejador_lh, espacamento_m, comprimento_m) e/ou topográficos (So, k_linha, L_estimado)."}), 400

    tem_perfil = any(k in dados for k in ['So', 'k_linha', 'L_estimado', 'declividade', 'H', 'Hvar'])
    tem_perda = any(k in dados for k in ['diametro_mm', 'vazao_gotejador_lh', 'espacamento_m', 'comprimento_m'])

    if not tem_perfil and not tem_perda:
        return jsonify({"erro": "Nenhum parâmetro válido enviado."}), 400

    resultado_final = {}

    if tem_perfil:
        if 'So' not in dados or 'k_linha' not in dados or 'L_estimado' not in dados:
            return jsonify({"erro": "Os campos 'So', 'k_linha' e 'L_estimado' são obrigatórios."}), 400
    # Lógica de Perda de Carga
    if tem_perda:
        campos_perda = ['diametro_mm', 'vazao_gotejador_lh', 'espacamento_m', 'comprimento_m']
        for campo in campos_perda:
            if campo not in dados:
                return jsonify({"erro": f"O campo '{campo}' é obrigatório."}), 400
    if 'So' in dados or 'k_linha' in dados or 'L_estimado' in dados:
        if 'So' not in dados or 'k_linha' not in dados or 'L_estimado' not in dados:
            return jsonify({"erro": "Os campos 'So', 'k_linha' e 'L_estimado' são obrigatórios."}), 400
        try:
            So = float(dados['So'])
            k_linha = float(dados['k_linha'])
            L_estimado = float(dados['L_estimado'])
        except ValueError:
            return jsonify({"erro": "Os valores de 'So', 'k_linha' e 'L_estimado' devem ser numéricos."}), 400
        classificacao = calculador.classificar_perfil_pressao(So, k_linha, L_estimado)
        return jsonify({"classificacao": classificacao}), 200

    # Ramo 2: Cálculo de Perda de Carga Distribuída
    campos_obrigatorios = ['diametro_mm', 'vazao_gotejador_lh', 'espacamento_m', 'comprimento_m']

    # Verifica se pelo menos o primeiro campo do ramo 2 está presente antes de assumir este caminho
    if 'diametro_mm' in dados:
        for campo in campos_obrigatorios:
            if campo not in dados:
                return jsonify({"erro": f"O campo '{campo}' é obrigatório."}), 400

        pass # end if diametro_mm

    return jsonify({"erro": "Parâmetros não reconhecidos."}), 400

        if not cultura_selecionada:
            return jsonify({"erro": "Cultura inexistente."}), 404

        vincular_cultura_projeto(codigo_projeto, cultura_id, estagio_selecionado)

        kc_aplicado = calculador.definir_kc_por_estagio(
            cultura_selecionada['kc_inicial'],
            cultura_selecionada['kc_media'],
            cultura_selecionada['kc_final'],
            estagio_selecionado
        )

        return jsonify({
            "status": "sucesso",
            "mensagem": "Cultura vinculada com sucesso ao projeto",
            "dados_vinculados": {
                "codigo_projeto": codigo_projeto,
                "cultura_id": cultura_id,
                "estagio_selecionado": estagio_selecionado,
                "kc_aplicado": kc_aplicado
            }
        }), 200
        resultado = calculador.calcular_perda_carga(
            diametro_mm,
            vazao_gotejador_lh,
            espacamento_m,
            comprimento_m
        )

        if "erro" in resultado:
            return jsonify(resultado), 400

        return jsonify(resultado), 200

    # If neither branch condition is fully met, check if we are missing fields for profile classification
    if any(campo in dados for campo in ['So', 'k_linha', 'L_estimado']):
         return jsonify({"erro": "Os campos 'So', 'k_linha' e 'L_estimado' são obrigatórios."}), 400

    # Fallback to missing fields for head loss
    for campo in campos_obrigatorios_perda_carga:
        if campo not in dados:
            return jsonify({"erro": f"O campo '{campo}' é obrigatório."}), 400

    missing_fields = [campo for campo in campos_obrigatorios if campo not in dados]
    if missing_fields:
        if any(k in dados for k in ['So', 'k_linha', 'L_estimado']):
            return jsonify({"erro": "Os campos 'So', 'k_linha' e 'L_estimado' são obrigatórios."}), 400
        else:
            return jsonify({"erro": f"O campo '{missing_fields[0]}' é obrigatório."}), 400
        if "erro" in resultado_perda:
            return jsonify(resultado_perda), 400

        resultado_final.update(resultado_perda)

    # Lógica de Perfil de Pressão
    if tem_perfil:
        if 'So' not in dados or 'k_linha' not in dados or 'L_estimado' not in dados:
            return jsonify({"erro": "Os campos 'So', 'k_linha' e 'L_estimado' são obrigatórios."}), 400

        try:
            resultado = calculador.calcular_perda_carga(
                diametro_mm,
                vazao_gotejador_lh,
                espacamento_m,
                comprimento_m
            )
            if "erro" in resultado:
                return jsonify(resultado), 400
            return jsonify(resultado), 200
        except ValueError:
            return jsonify({"erro": "Todos os parâmetros devem ser números válidos."}), 400

    # If it falls through, it's missing fields for both
    # The tests check specifically for diametro_mm being the first required field if nothing else matches
    for campo in campos_obrigatorios:
        if campo not in dados_recebidos:
            # Revert exactly to what tests expect or unify elegantly
            if 'So' in dados_recebidos or 'k_linha' in dados_recebidos:
                 return jsonify({"erro": "Os campos 'So', 'k_linha' e 'L_estimado' são obrigatórios."}), 400
            return jsonify({"erro": f"O campo '{campo}' é obrigatório."}), 400

    except ValueError:
        return jsonify({"erro": "Tipos de dados invalidos"}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

        return jsonify({"erro": "Todos os parâmetros devem ser números válidos."}), 400

    resultado = calculador.calcular_perda_carga(
        diametro_mm,
        vazao_gotejador_lh,
        espacamento_m,
        comprimento_m,
        comprimento_equivalente_le
    )

    if "erro" in resultado:
        return jsonify(resultado), 400
    return jsonify({"erro": "Parâmetros inválidos"}), 400

    validacao = calculador.validar_criterio_pressao_subunidade(
        resultado['perda_carga_mca'],
        pressao_entrada_mca
    )

    resultado.update(validacao)

    return jsonify(resultado), 200

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

@app.route('/api/culturas', methods=['GET'])
def obter_culturas():
    culturas = get_culturas()
    return jsonify(culturas), 200

@app.route('/api/culturas', methods=['GET'])
def obter_culturas():
    culturas = get_culturas()
    return jsonify(culturas), 200

@app.route('/api/classificar_perfil', methods=['POST'])
@app.route('/api/hidraulica_classificacao', methods=['POST'])
@app.route('/api/hidraulica/perfil', methods=['POST'])
@app.route('/api/hidraulica_perfil', methods=['POST'])
@app.route('/api/classificar_hidraulica', methods=['POST'])
def obter_classificacao_perfil():
    pass

@app.route('/api/projetos/<string:codigo_projeto>/area-umedecida', methods=['POST'])
def calcular_area_umedecida_endpoint(codigo_projeto):
    """
    Rotina 4 - Pw (Raio Umedecido Rw, Diametro Molhado Dw, Area Umedecida Pw)
    """
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    # Determina qual lógica usar com base nos campos presentes
    if 'So' in dados or 'k_linha' in dados or 'L_estimado' in dados:
        if 'So' not in dados or 'k_linha' not in dados or 'L_estimado' not in dados:
            return jsonify({"erro": "Os campos 'So', 'k_linha' e 'L_estimado' são obrigatórios."}), 400
        try:
            So = float(dados['So'])
            k_linha = float(dados['k_linha'])
            L_estimado = float(dados['L_estimado'])
        except ValueError:
            return jsonify({"erro": "Os valores de 'So', 'k_linha' e 'L_estimado' devem ser numéricos."}), 400

        # Mapeamento alterado devido ao mock que foi inserido anteriormente
        if hasattr(calculador, 'classificar_perfil_topografico'):
             classificacao = calculador.classificar_perfil_topografico(So, k_linha, L_estimado)
        else:
             classificacao = calculador.classificar_perfil_pressao(So, k_linha, L_estimado)
             classificacao = {"classificacao": classificacao}

        return jsonify(classificacao), 200
    else:
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
    if not dados:
        return jsonify({"erro": "Payload invalido"}), 400

    projeto = get_projeto_metadados(codigo_projeto)
    if not projeto:
        return jsonify({"erro": "Projeto inexistente. Configure os metadados primeiro."}), 404

    try:
        q_vazao = float(dados.get('q_vazao', 2.0))
        volume_z = float(dados.get('volume_z', 30.0))
        ko_condutividade = float(dados.get('ko_condutividade', 15.0))
        espacamento_plantas_sp = float(dados.get('espacamento_plantas_sp', 0.5))
        espacamento_fileiras_sr = float(dados.get('espacamento_fileiras_sr', 1.0))
        numero_emissores_np = int(dados.get('numero_emissores_np', 1))

        # This calls the method from the model
        resultado = calculador.calcular_area_umedecida(
            q_vazao, volume_z, ko_condutividade, espacamento_plantas_sp, espacamento_fileiras_sr, numero_emissores_np
        )

        update_area_umedecida_projeto(
            codigo_projeto,
            0.0, # rw was removed
            resultado[0], # dw
            resultado[1], # pw
            str(dados.get('tipo_disposicao', '')),
            str(dados.get('configuracao_linha', '')),
            float(dados.get('parametro_alpha', 1.0)),
            ko_condutividade,
            volume_z
        )

        return jsonify({
            "status": "sucesso",
            "metadados": resultado
        }), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
    if not has_advanced and not has_basic:
        if any(key in dados for key in ['So', 'k_linha', 'L_estimado']):
             return jsonify({"erro": "Os campos 'So', 'k_linha' e 'L_estimado' são obrigatórios."}), 400
        return jsonify({"erro": "Faltam parâmetros básicos (diametro_mm, etc) ou avançados (So, k_linha, etc)."}), 400


@app.route('/api/projetos/<string:codigo_projeto>/area-sombreada', methods=['POST'])
def calcular_area_sombreada_endpoint(codigo_projeto):
    """
    Rotina 5 - Ps (Area Sombreada)
    """
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Payload invalido"}), 400

    projeto = get_projeto_metadados(codigo_projeto)
    if not projeto:
        return jsonify({"erro": "Projeto inexistente. Configure os metadados primeiro."}), 404

    try:
        tipo_copa = str(dados.get('tipo_copa', 'circular'))
        espacamento_plantas_sp = float(dados.get('espacamento_plantas_sp', 1.0))
        espacamento_fileiras_sr = float(dados.get('espacamento_fileiras_sr', 1.0))
        largura_faixa_ss = dados.get('largura_faixa_ss', None)
        diametro_copa_dco = dados.get('diametro_copa_dco', None)

        if largura_faixa_ss is not None: largura_faixa_ss = float(largura_faixa_ss)
        if diametro_copa_dco is not None: diametro_copa_dco = float(diametro_copa_dco)

        ps = calculador.calcular_area_sombreada(
            tipo_copa, espacamento_plantas_sp, espacamento_fileiras_sr, largura_faixa_ss, diametro_copa_dco
        )

        update_area_sombreada_projeto(
            codigo_projeto,
            ps,
            tipo_copa,
            largura_faixa_ss if largura_faixa_ss else 0.0,
            diametro_copa_dco if diametro_copa_dco else 0.0
        )
        return jsonify({
            "status": "sucesso",
            "ps": ps
        }), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@app.route('/api/hidraulica', methods=['POST'])
def leitura_climatica():
    """
    Cálculo em Cadeia de ETo e Balanço de Radiação
    """
        if "erro" in resultado:
            return jsonify(resultado), 400

        return jsonify(resultado), 200

    return jsonify({"erro": "Payload inválido. Envie os parâmetros para classificação de perfil ou perda de carga."}), 400

    # Advanced Flow: Pressure Profiles
    tem_fluxo_avancado = any(campo in dados for campo in ['So', 'k_linha', 'L_estimado', 'declividade', 'H', 'Hvar'])

    if tem_fluxo_avancado:
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

    if not tem_fluxo_basico and not tem_fluxo_avancado:
         return jsonify({"erro": "Parâmetros insuficientes para realizar cálculos hidráulicos."}), 400

    return jsonify(resultado_final), 200

    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    resposta_combinada = {}
    erro_ocorrido = False
    mensagem_erro = ""

    # Verifica parâmetros de topografia / perfil (obter_hidraulica original)
    if 'So' in dados and 'k_linha' in dados and 'L_estimado' in dados:
        try:
            So = float(dados['So'])
            k_linha = float(dados['k_linha'])
            L_estimado = float(dados['L_estimado'])
            classificacao = calculador.classificar_perfil_pressao(So, k_linha, L_estimado)
            return jsonify({"classificacao": classificacao}), 200
        except ValueError:
            return jsonify({"erro": "Os valores de 'So', 'k_linha' e 'L_estimado' devem ser numéricos."}), 400

    # Verifica parâmetros básicos (hidraulica original)
    campos_basicos = ['diametro_mm', 'vazao_gotejador_lh', 'espacamento_m', 'comprimento_m']
    tem_todos_basicos = all(campo in dados for campo in campos_basicos)

    if tem_todos_basicos:
        try:
            diametro_mm = float(dados['diametro_mm'])
            vazao_gotejador_lh = float(dados['vazao_gotejador_lh'])
            espacamento_m = float(dados['espacamento_m'])
            comprimento_m = float(dados['comprimento_m'])

            resultado = calculador.calcular_perda_carga(
                diametro_mm,
                vazao_gotejador_lh,
                espacamento_m,
                comprimento_m
            )
            if "erro" in resultado:
                return jsonify(resultado), 400
            return jsonify(resultado), 200
        except ValueError:
            return jsonify({"erro": "Todos os parâmetros devem ser números válidos."}), 400

    return jsonify({"erro": "Parâmetros não reconhecidos."}), 400

    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    campos_basicos = ['diametro_mm', 'vazao_gotejador_lh', 'espacamento_m', 'comprimento_m']
    campos_avancados = ['So', 'k_linha', 'L_estimado']

    tem_basico = all(campo in dados for campo in campos_basicos)
    tem_avancado = all(campo in dados for campo in campos_avancados)

    if not tem_basico and not tem_avancado:
        return jsonify({"erro": "Parâmetros insuficientes. Envie os campos básicos ('diametro_mm', 'vazao_gotejador_lh', 'espacamento_m', 'comprimento_m') ou avançados ('So', 'k_linha', 'L_estimado')."}), 400

    resposta = {}

    if tem_basico:
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

@app.route('/api/hidraulica_legacy', methods=['POST'])
def obter_hidraulica_legacy():
    pass

def classificar_perfil():
    dados_recebidos = request.get_json()
    if not dados_recebidos or 'So' not in dados_recebidos or 'k_linha' not in dados_recebidos or 'L_estimado' not in dados_recebidos:
        return jsonify({"erro": "Os campos 'So', 'k_linha' e 'L_estimado' são obrigatórios."}), 400
    else:
        return jsonify({"erro": "O campo 'diametro_mm' é obrigatório."}), 400

@app.route('/api/projetos', methods=['POST'])
def salvar_projeto_metadados():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Payload invalido"}), 400

    try:
        t_max = float(dados.get('t_max', 30.0))
        t_min = float(dados.get('t_min', 20.0))
        latitude = float(dados.get('latitude', -22.0))
        mes_index = int(dados.get('mes_index', 1))

        eto = calculador.calcular_eto_hargreaves(t_max, t_min, latitude, mes_index)

        # Insert reading into historico_leitura
        leitura_id = insert_leitura(
            umidade=float(dados.get('ur_media', 60.0)),
            temperatura_max=t_max,
            temperatura_min=t_min,
            eto_calculada=eto,
            cad_calculada=0.0,
            irn_calculada=0.0,
            comprimento_lateral_m=0.0,
            perda_carga_total_mca=0.0
    if is_classificacao:
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
    return jsonify(resultado_final), 200

    if has_basic:
        resultado_final["classificacao"] = calculador.classificar_perfil_pressao(So, k_linha, L_estimado)

    if is_perda_carga:
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
        resultado = calculador.calcular_perda_carga(
            diametro_mm,
            vazao_gotejador_lh,
            espacamento_m,
            comprimento_m
        )

        return jsonify({
            "status": "sucesso",
            "id": leitura_id,
            "eto": eto
        }), 201

    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@app.route('/api/status', methods=['GET'])
def obter_status_geral():
    try:
        historico = get_historico()
        return jsonify({
            "status": "sucesso",
            "historico": historico
        }), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
        if "erro" in resultado:
            return jsonify(resultado), 400

        return jsonify(resultado), 200

    if not is_classificacao and not is_perda_carga:
        return jsonify({"erro": "Nenhum parâmetro válido enviado."}), 400
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
    area_subunidade = dados.get('area_subunidade')
    data_elaboracao = dados.get('data_elaboracao')

    resultado = insert_projeto(
        codigo_projeto,
        nome_projeto,
        nome_propriedade,
        nome_proprietario,
        nome_projetista,
        identificacao,
        nome_codigo_subunidade,
        area_total_irrigada,
        area_subunidade,
        data_elaboracao
    )

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


@app.route('/api/status/<string:codigo_projeto>', methods=['GET'])
def obter_status_projeto(codigo_projeto):
    try:
        projeto = get_projeto_metadados(codigo_projeto)
        if not projeto:
            return jsonify({"erro": "Projeto inexistente."}), 404

        historico = get_historico(codigo_projeto)
        return jsonify({
            "status": "sucesso",
            "projeto": projeto,
            "historico": historico
        }), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route('/api/culturas', methods=['GET', 'POST'])
def rotina_culturas():
    if request.method == 'GET':
        culturas = get_culturas()
        return jsonify(culturas), 200
    else:
        dados = request.get_json()
        if not dados or 'nome' not in dados:
            return jsonify({"erro": "O campo 'nome' é obrigatório"}), 400

        try:
            nome = str(dados['nome'])
            culturas_existentes = get_culturas()
            if any(c['nome'].lower() == nome.lower() for c in culturas_existentes):
                return jsonify({"erro": "Cultura já cadastrada"}), 400

            # In a real app we would insert into DB here.
            from backend.database import insert_cultura
            insert_cultura(nome, dados.get('kc_inicial', 1.0), dados.get('kc_media', 1.0), dados.get('kc_final', 1.0), dados.get('data_plantio', ''), dados.get('dias_fase_inicial', 0), dados.get('dias_meia_estacao', 0), dados.get('dias_fase_final', 0))
            return jsonify({"status": "sucesso", "mensagem": "Cultura adicionada"}), 201
        except Exception as e:
            return jsonify({"erro": str(e)}), 400


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

@app.route('/api/projetos/<string:codigo_projeto>/area-sombreada', methods=['POST'])
def calcular_e_salvar_area_sombreada(codigo_projeto):
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({'erro': 'Nenhum dado JSON fornecido'}), 400

        tipo_calculo = dados.get('tipo_calculo')
        if not tipo_calculo:
            return jsonify({'erro': 'Parâmetro tipo_calculo é obrigatório'}), 400

        params = dados.get('params', {})

        # Initialize calculador
        calc = CalculadorIrrigacao()

        try:
            ps_calculado = calc.calcular_porcentagem_area_sombreada_ps(tipo_calculo, params)
        except ValueError as e:
            return jsonify({'erro': str(e)}), 400

        # Parse audit values for persistence
        ss_largura = params.get('ss_largura')
        dco_diametro = params.get('dco_diametro')

        # Save to database
        # from backend.database import salvar_dados_area_sombreada should be accessible if we import backend.database as database
        import backend.database as db
        salvo = db.salvar_dados_area_sombreada(
            codigo_projeto=codigo_projeto,
            tipo_calculo=tipo_calculo,
            ss_largura=ss_largura,
            dco_diametro=dco_diametro,
            ps_calculado=ps_calculado
        )

        if not salvo:
            return jsonify({'erro': 'Projeto não encontrado no banco de dados'}), 404

        return jsonify({
            'codigo_projeto': codigo_projeto,
            'tipo_calculo': tipo_calculo,
            'ps_calculado': ps_calculado,
            'mensagem': 'Área sombreada calculada e salva com sucesso'
        }), 200

    except Exception as e:
        return jsonify({'erro': 'Erro interno do servidor', 'detalhes': str(e)}), 500


@app.route('/api/projetos/<string:codigo_projeto>/perdas-conexoes', methods=['POST'])
def calcular_e_salvar_perdas_conexoes(codigo_projeto):
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({'erro': 'Nenhum dado JSON fornecido'}), 400

        required_keys = ['v_d', 'd_d', 'a_p', 'd_c', 'l_c', 'v_c', 'v_l']
        for k in required_keys:
            if k not in dados or dados[k] is None:
                return jsonify({'erro': f'Parâmetro {k} é obrigatório e não pode ser nulo.'}), 400

        try:
            v_d = float(dados['v_d'])
            d_d = float(dados['d_d'])
            a_p = float(dados['a_p'])
            d_c = float(dados['d_c'])
            l_c = float(dados['l_c'])
            v_c = float(dados['v_c'])
            v_l = float(dados['v_l'])
        except ValueError:
            return jsonify({'erro': 'Parâmetros devem ser numéricos.'}), 400

        if d_d <= 0:
            return jsonify({'erro': 'Parâmetro d_d deve ser maior que zero.'}), 400

        from backend.models.irrigacao import CalculadorIrrigacao
        calc = CalculadorIrrigacao()

        validacao = calc.validar_limites_vilaca(v_d, d_d, a_p, d_c, l_c, v_c, v_l)
        limites_status = 0 if validacao['limites_estourados'] else 1

        hfl_d = calc.calcular_perda_direta_hfl_d(v_d, d_d, a_p)
        hfl_l = calc.calcular_perda_lateral_hfl_l(d_c, l_c, v_c, v_l)

        import backend.database as db
        salvo = db.salvar_perdas_conexoes(
            codigo_projeto=codigo_projeto,
            v_d=v_d, d_d=d_d, a_p=a_p, hfl_d=hfl_d,
            d_c=d_c, l_c=l_c, v_c=v_c, v_l=v_l, hfl_l=hfl_l,
            limites_status=limites_status
        )

        if not salvo:
            return jsonify({'erro': 'Projeto não encontrado no banco de dados'}), 404

        return jsonify({
            'status': 'sucesso',
            'codigo_projeto': codigo_projeto,
            'resultados': {
                'perda_direta_hfl_d': hfl_d,
                'perda_lateral_hfl_l': hfl_l
            },
            'auditoria_limites': validacao
        }), 200

    except Exception as e:
        return jsonify({'erro': 'Erro interno do servidor', 'detalhes': str(e)}), 500
