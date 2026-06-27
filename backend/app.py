# -*- coding: utf-8 -*-
import math
# backend/app.py
import os
import sqlite3
import json
from flask import Flask, jsonify, request
import sqlite3
from backend.database import init_db, salvar_dados_solo_p58
from backend.models.irrigacao import CalculadorIrrigacao
from backend.models.irrigacao import CalculadorIrrigacao
from backend.database import obter_projeto_por_codigo, salvar_projeto_hidraulica_lateral

app = Flask(__name__)
CORS(app)

@app.route('/api/projetos/<string:codigo_projeto>/linha-lateral-declive', methods=['POST'])
def linha_lateral_declive_endpoint(codigo_projeto):
    projeto = obter_projeto_por_codigo(codigo_projeto)
    if not projeto:
        return jsonify({"erro": "Projeto inexistente."}), 404

import datetime
from backend.database import init_db, insert_leitura, get_ultima_leitura, update_leitura_status, get_historico, seed_culturas, get_culturas, get_projeto_metadados, get_bancos, insert_banco, delete_banco, insert_projeto


from backend.database import obter_projeto_por_codigo, obter_resumo_hidraulico, init_db, insert_leitura, get_ultima_leitura, update_leitura_status, get_historico, seed_culturas, get_culturas, get_projeto_metadados, insert_projeto
from backend.database import salvar_hidraulica_lateral
from backend.database import init_db, obter_projeto_por_codigo, obter_resumo_hidraulico, insert_leitura, get_ultima_leitura, update_leitura_status, get_historico, seed_culturas, get_culturas, get_bancos, insert_banco, delete_banco
from backend.database import init_db, insert_leitura, get_ultima_leitura, update_leitura_status, get_historico, seed_culturas, get_culturas, insert_projeto
from database import obter_projeto_por_codigo, obter_resumo_hidraulico, init_db, insert_leitura, get_ultima_leitura, update_leitura_status, get_historico, seed_culturas, get_culturas, insert_projeto_metadados, get_projeto_metadados
from database import init_db, insert_leitura, get_ultima_leitura, update_leitura_status, get_historico, seed_culturas, get_culturas, get_bancos, insert_banco, delete_banco
from database import obter_projeto_por_codigo, obter_resumo_hidraulico, init_db, insert_leitura, get_ultima_leitura, update_leitura_status, get_historico, seed_culturas, get_culturas, insert_projeto, get_projeto_metadados, get_bancos, insert_banco, delete_banco, insert_projeto_metadados
from database import init_db, insert_leitura, get_ultima_leitura, update_leitura_status, get_historico, seed_culturas, get_culturas, get_projeto_metadados, get_bancos, insert_banco, delete_banco, insert_projeto
from database import obter_projeto_por_codigo, obter_resumo_hidraulico, init_db, insert_leitura, get_ultima_leitura, update_leitura_status, get_historico, seed_culturas, get_culturas, get_projeto_metadados, insert_projeto
from database import init_db, obter_projeto_por_codigo, obter_resumo_hidraulico, insert_leitura, get_ultima_leitura, update_leitura_status, get_historico, seed_culturas, get_culturas, get_bancos, insert_banco, delete_banco
from database import init_db, insert_leitura, get_ultima_leitura, update_leitura_status, get_historico, seed_culturas, get_culturas, insert_projeto

app = Flask(__name__)
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

def _calcular_engenharia(temperatura_max, temperatura_min, umidade_atual, ce_agua_ds_m, metodo_eto='hargreaves'):


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
            mes_index=dados_sistema["mes_atual"],
            latitude_sul=-22.0
        )
    elif metodo_eto.lower() == 'penman-monteith':
        # Penman-Monteith required inputs, using defaults for robustness if not passed
        rn = float(request.args.get('rn', 15.0))
        g = float(request.args.get('g', 0.0))
        u2 = float(request.args.get('u2', 2.0))
        delta = float(request.args.get('delta', 0.15))
        gama = float(request.args.get('gama', 0.066))

        # Integração da Sub-rotina Hidráulica de Pressões e Déficit de Pressão de Vapor
        es_calculado = calculador.calcular_pressao_saturacao_es(temperatura_max, temperatura_min)
        ea_calculado = calculador.calcular_pressao_atual_ea(es_calculado, umidade_atual)
        deficit_vapor = calculador.calcular_deficit_vapor(es_calculado, ea_calculado)

        eto = calculador.calcular_eto_penman_monteith(
            rn, g, t_media, u2, es_calculado, ea_calculado, delta, gama
        n_insolacao = request.args.get('n', default=8.0, type=float)
        ra = calculador.obter_radiacao_solar_ra(-22.0, dados_sistema["mes_atual"])
        N_max = calculador.obter_duracao_maxima_n(-22.0, dados_sistema["mes_atual"])
        rs = calculador.calcular_radiacao_solar_rs(ra, n_insolacao, N_max)
        rso, rns = calculador.calcular_rns(rs, ra, altitude_m=500.0)

        # We need `ea` here. It is fetched below. Let's just calculate it.
        ea = float(request.args.get('ea', 1.5))
        r_nl, rn_calc = calculador.calcular_rn(temperatura_max, temperatura_min, ea, rs, rso, rns)

        # Pass the calculated rn or allow override via args
        rn = request.args.get('rn', default=rn_calc, type=float)
        g = float(request.args.get('g', 0.0))
        u2 = float(request.args.get('u2', 2.0))
        es = float(request.args.get('es', 3.0))
        ea = float(request.args.get('ea', 1.5))
        delta = float(request.args.get('delta', 0.15))
        gama = float(request.args.get('gama', 0.066))

        eto = calculador.calcular_eto_penman_monteith(
            rn, g, t_media, u2, es, ea, delta, gama
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
        1.0,
        3.0,
        dados_sistema["ce_solo_min"],
        dados_sistema["ce_solo_max"],
        dados_sistema["uniformidade_emissao_decimal"]
    )

    analise = calculador.avaliar_status_solo(umidade_atual)

    if analise["irrigar"]:
        defice_proporcional = (dados_sistema["solo_cc"] - (umidade_atual/100 * dados_sistema["solo_cc"]))
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
    tempo_irrigacao_horas = tempo_irrigacao_calculado_minutos / 60.0
    agenda_rega = calculador.fracionar_tempo_irrigacao(tempo_irrigacao_horas)

    es_placeholder = 2.4
    ur_placeholder = 60.0
    ea_placeholder = calculador.calcular_pressao_atual_ea(es_placeholder, ur_placeholder)
    deficit_pressao_vapor_kpa = calculador.calcular_deficit_pressao_vapor(es_placeholder, ea_placeholder)

    try:
        comprimento_lateral_m = calculador.comprimento_trecho_a_trecho(
            diametro_m=dados_sistema.get("diametro_lateral_m", 0.016),
            vazao_emissor_m3s=dados_sistema["vazao_emissor_qa"] / 3600000.0,
            espacamento_m=dados_sistema["espacamento_plantas_m"],
            pressao_entrada_mca=dados_sistema.get("pressao_entrada_mca", 10.0),
            declividade=dados_sistema.get("declividade", 0.0),
            hvar_max=dados_sistema.get("hvar_max", 2.0)
        )
    except Exception:
        comprimento_lateral_m = 0.0

    resultado_perda = calculador.calcular_perda_carga(
        diametro_mm=dados_sistema.get("diametro_lateral_m", 0.016) * 1000.0,
        vazao_gotejador_lh=dados_sistema["vazao_emissor_qa"],
        espacamento_m=dados_sistema["espacamento_plantas_m"],
        comprimento_m=comprimento_lateral_m
    )

    if "erro" in resultado_perda:
        perda_carga_total_mca = 0.0
    else:
        perda_carga_total_mca = resultado_perda.get('perda_carga_mca', 0.0)

    return {
        "eto": eto,
        "cad": cad,
        "irn_max": irn_max,
        "turno_rega_max_dias": turno_rega_max_dias,
        "fl": fl,
        "itn": itn,
        "analise": analise,
        "ti_horas": ti_horas,
        "np_emissores": np_emissores,
        "tempo_irrigacao_calculado_minutos": tempo_irrigacao_calculado_minutos,
        "agenda_rega": agenda_rega,
        "comprimento_lateral_m": comprimento_lateral_m,
        "perda_carga_total_mca": perda_carga_total_mca,
        "deficit_pressao_vapor_kpa": deficit_pressao_vapor_kpa
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
    min_ce = 1.0
    min_ce = dados_sistema["ce_solo_min"]
    max_ce = dados_sistema["ce_solo_max"]

    if culturas:
        cultura_ativa = culturas[0]
        min_ce = cultura_ativa.get('min_ce', dados_sistema["ce_solo_min"])
        max_ce = cultura_ativa.get('max_ce', dados_sistema["ce_solo_max"])
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

    calc = {
        "tempo_irrigacao_horas": 0.0,
        "numero_emissores_por_planta": 0,
        "eto": 0.0,
        "analise": {"status": "Ideal", "mensagem": "Ok", "irrigar": False, "cor_alerta": "success"},
        "turno_rega_max_dias": 0,
        "lamina_bruta_irrigacao_mm": 0.0,
        "fracao_lixiviacao": 0.0,
        "irrigacao_total_necessaria_mm": 0.0,
        "cad": 0.0,
        "irn_max": 0.0,
        "comprimento_lateral_m": 0.0,
        "perda_carga_total_mca": 0.0,
        "agenda_rega": {},
        "itn": 0.0,
        "ti_horas": 0.0,
        "np_emissores": 0,
        "fl": 0.0
    }

    codigo_projeto = request.args.get('codigo_projeto', None)
    calc = _calcular_engenharia(temperatura_max, temperatura_min, umidade_atual, ce_agua_ds_m, metodo_eto, codigo_projeto)

    # Atualiza o status e o tempo calculado no banco de dados
    update_leitura_status(
        leitura_id,
        calc["analise"]["status"],
        0.0,
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

    if ce_agua_ds_m > 1.0:
        calc["analise"]["mensagem"] += " Alerta: Ocorrerá decréscimo na produtividade."
    if ce_agua_ds_m > dados_sistema['ce_solo_min']:
        calc["analise"]["mensagem"] += " Alerta: Ocorrerá decréscimo na produtividade."
    if ce_agua_ds_m > min_ce:
        calc["analise"]["mensagem"] += " Alerta: Ocorrerá decréscimo na produtividade."
        pass # placeholder

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
        "metricas_tese": {
            "radiacao_liquida_rn_mj_m2_dia": calc.get("rn", 0.0),
            "evapotranspiracao_referencia_mm_dia": calc.get("eto", 0.0),
            "capacidade_agua_disponivel_solo_mm": calc.get("cad", 0.0),
            "irrigacao_real_necessaria_max_mm": calc.get("irn_max", 0.0),
            "tempo_irrigacao_horas": calc.get("ti_horas", 0.0),
            "numero_emissores_por_planta": calc.get("np_emissores", 0),
            "tempo_irrigacao_calculado_minutos": calc.get("tempo_irrigacao_calculado_minutos", 0.0),
            "fracao_lixiviacao": calc.get("fl", 0.0),
            "irrigacao_total_necessaria_mm": calc.get("itn", 0.0),
            "deficit_pressao_vapor_kpa": calc.get("deficit_pressao_vapor_kpa", 0.0)
            "evapotranspiracao_referencia_mm_dia": eto,
            "capacidade_agua_disponivel_solo_mm": cad,
            "irrigacao_real_necessaria_max_mm": irn_max,
            "tempo_irrigacao_calculado_minutos": max(tempo_estimado_minutos, 0.0),
            "tempo_irrigacao_horas": ti_horas,
            "numero_emissores_por_planta": np_emissores,
            "fracao_lixiviacao": fl,
            "irrigacao_total_necessaria_mm": itn,
            "irrigacao_total_necessaria_mm": itn
            "evapotranspiracao_referencia_mm_dia": calc["eto"],
            "capacidade_agua_disponivel_solo_mm": calc["cad"],
            "irrigacao_real_necessaria_max_mm": calc["irn_max"],
            "tempo_irrigacao_horas": calc["ti_horas"],
            "numero_emissores_por_planta": calc["np_emissores"],
            "tempo_irrigacao_calculado_minutos": 0.0,
            "fracao_lixiviacao": calc["fl"],
            "irrigacao_total_necessaria_mm": calc["itn"],
            "deficit_pressao_vapor_kpa": calc.get("deficit_pressao_vapor_kpa", 0.0),
            "irrigacao_total_necessaria_mm": calc["itn"]
            "irrigacao_total_necessaria_mm": calc["itn"],
            "evapotranspiracao_referencia_mm_dia": eto,
            "capacidade_agua_disponivel_solo_mm": cad,
            "irrigacao_real_necessaria_max_mm": irn_max,
            "tempo_irrigacao_calculado_minutos": tempo_irrigacao_calculado_minutos,
            "tempo_irrigacao_horas": ti_horas,
            "numero_emissores_por_planta": np_emissores,
            "tempo_irrigacao_calculado_minutos": tempo_irrigacao_calculado_minutos,
            "fracao_lixiviacao": fl,
            "fracao_lixiviacao": fl,
            "tempo_irrigacao_horas": ti_horas,
            "numero_emissores_por_planta": np_emissores,
            "tempo_irrigacao_calculado_minutos": tempo_irrigacao_calculado_minutos,
            "fracao_lixiviacao": fl,
            "fracao_lixiviacao": fl,
            "irrigacao_total_necessaria_mm": itn,
            "tempo_irrigacao_calculado_minutos": tempo_irrigacao_calculado_minutos,
            "tempo_irrigacao_calculado_minutos": tempo_irrigacao_calculado_minutos,
            "tempo_irrigacao_horas": ti_horas,
            "numero_emissores_por_planta": np_emissores,
            "fracao_lixiviacao": fl,
            "tempo_irrigacao_horas": ti_horas,
            "numero_emissores_por_planta": np_emissores,
            "fracao_lixiviacao": fl,
            "fracao_lixiviacao": fl,
            "fracao_lixiviacao": fl,
            "fracao_lixiviacao": fl,
            "tempo_irrigacao_calculado_minutos": tempo_irrigacao_calculado_minutos,
            "fracao_lixiviacao": fl,
            "fracao_lixiviacao": fl,
            "fracao_lixiviacao": fl,
            "fracao_lixiviacao": fl,
            "tempo_irrigacao_calculado_minutos": tempo_irrigacao_calculado_minutos,
            "fracao_lixiviacao": fl,
            "fracao_lixiviacao": fl,
            "irrigacao_total_necessaria_mm": itn,
            "deficit_pressao_vapor_kpa": deficit_pressao_vapor_kpa,
            "tempo_irrigacao_calculado_minutos": tempo_irrigacao_calculado_minutos,
            "fracao_lixiviacao": fl,
            "fracao_lixiviacao": fl,
            "fracao_lixiviacao": fl,
            "fracao_lixiviacao": fl,
            "fracao_lixiviacao": fl,
            "tempo_irrigacao_calculado_minutos": max(tempo_estimado_minutos, 0.0),
            "fracao_lixiviacao": fl,
            "fracao_lixiviacao": fl,
            "irrigacao_total_necessaria_mm": itn,
            "tempo_irrigacao_calculado_minutos": tempo_irrigacao_calculado_minutos,
            "fracao_lixiviacao": fl,
            "irrigacao_total_necessaria_mm": itn
            "delta_kPa": calc["delta_kPa"],
            "pressao_atm_kPa": calc["pressao_atm_kPa"],
            "deficit_pressao_vapor_kpa": calc.get("deficit_pressao_vapor_kpa", 0.0)
        }
    }

    if alerta_salinidade:
        response_json.update(alerta_salinidade)
        resposta_json.update(alerta_salinidade)
#
#    return jsonify(resposta_json), 200
#    if raio_umedecido_info.get("alerta_faixa_descontinua"):
#        response_json["alerta_faixa_descontinua"] = True
#        response_json["mensagem_faixa"] = "Afastamento excessivo entre gotejadores. A faixa contínua de humidade será rompida, prejudicando as raízes."
        response_json.update(alerta_salinidade)

    return jsonify(response_json), 200

def _calcular_engenharia(temperatura_max, temperatura_min, umidade_atual, ce_agua_ds_m, metodo_eto='hargreaves'):
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

    # Verifica se foi enviada a condutividade elétrica da água via query params
    ce_agua_ds_m = request.args.get('ce_agua_ds_m', default=0.5, type=float)

    fl, itn = calculador.calcular_itn(
        irn_max,
        ce_agua_ds_m,
        dados_sistema["ce_solo_min"],
        dados_sistema["ce_solo_max"],
        dados_sistema["uniformidade_emissao_decimal"]
    )

    analise = calculador.avaliar_status_solo(umidade_atual)
    if ce_agua_ds_m > dados_sistema["ce_solo_min"]:
        analise["mensagem"] += " Alerta: Ocorrerá decréscimo na produtividade."

    if analise["irrigar"]:
        defice_proporcional = (dados_sistema["solo_cc"] - (umidade_atual/100 * dados_sistema["solo_cc"]))
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
    tempo_irrigacao_horas = tempo_irrigacao_calculado_minutos / 60.0
    agenda_rega = calculador.fracionar_tempo_irrigacao(tempo_irrigacao_horas)

    # Cálculo da Pressão Atual de Vapor e Déficit de Pressão de Vapor
    # Usando valores de placeholder para Pressão de Saturação (es) e Umidade Relativa (ur)
    es_placeholder = 2.4
    ur_placeholder = 60.0
    ea = calculador.calcular_pressao_atual_ea(es_placeholder, ur_placeholder)
    deficit_pressao_vapor_kpa = calculador.calcular_deficit_pressao_vapor(es_placeholder, ea)
    try:
        comprimento_lateral_m = calculador.comprimento_trecho_a_trecho(
            diametro_m=dados_sistema.get("diametro_lateral_m", 0.016),
            vazao_emissor_m3s=dados_sistema["vazao_emissor_qa"] / 3600000.0,
            espacamento_m=dados_sistema["espacamento_plantas_m"],
            pressao_entrada_mca=dados_sistema.get("pressao_entrada_mca", 10.0),
            declividade=dados_sistema.get("declividade", 0.0),
            hvar_max=dados_sistema.get("hvar_max", 2.0)
        )
    except Exception:
        comprimento_lateral_m = 0.0

    resultado_perda = calculador.calcular_perda_carga(
        diametro_mm=dados_sistema.get("diametro_lateral_m", 0.016) * 1000.0,
        vazao_gotejador_lh=dados_sistema["vazao_emissor_qa"],
        espacamento_m=dados_sistema["espacamento_plantas_m"],
        comprimento_m=comprimento_lateral_m
    )

    if "erro" in resultado_perda:
        perda_carga_total_mca = 0.0
    else:
        perda_carga_total_mca = resultado_perda.get('perda_carga_mca', 0.0)


    # --- Balanço de Radiação Líquida (Rn) ---
    altitude_m = dados_sistema.get("altitude_m", 500.0)
    ra = calculador.obter_radiacao_solar_ra(-22.0, dados_sistema["mes_atual"])
    rso = calculador.calcular_rso(altitude_m, ra)
    rs = 0.16 * math.sqrt(max(0.1, temperatura_max - temperatura_min)) * ra
    rns = calculador.calcular_rns(rs)
    ea_val = ea if 'ea' in locals() else 1.5
    rnl = calculador.calcular_rnl(temperatura_max, temperatura_min, ea_val, rs, rso)
    rn_calculado = calculador.calcular_rn(rns, rnl)
    # ----------------------------------------

    return {
        "rn": round(rn_calculado, 2),
        "eto": eto,
        "cad": cad,
        "irn_max": irn_max,
        "turno_rega_max_dias": turno_rega_max_dias,
        "fl": fl,
        "itn": itn,
        "analise": analise,
        "ti_horas": ti_horas,
        "np_emissores": np_emissores,
        "tempo_irrigacao_calculado_minutos": tempo_irrigacao_calculado_minutos,
        "agenda_rega": agenda_rega,
        "comprimento_lateral_m": comprimento_lateral_m,
        "perda_carga_total_mca": perda_carga_total_mca
    }


    return jsonify(response_json), 200

    return jsonify(response_json), 200
    if raio_umedecido_info.get("alerta_faixa_descontinua"):
        response_json["alerta_faixa_descontinua"] = True
        response_json["mensagem_faixa"] = "Afastamento excessivo entre gotejadores. A faixa contínua de humidade será rompida, prejudicando as raízes."
    elif raio_umedecido_info.get("alerta"):
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


    calc = {
        "eto": 0.0,
        "cad": 0.0,
        "irn_max": 0.0,
        "comprimento_lateral_m": 0.0,
        "perda_carga_total_mca": 0.0
    }

    codigo_projeto = dados_recebidos.get('codigo_projeto', None)
    calc = _calcular_engenharia(temperatura_max, temperatura_min, umidade, 0.5, codigo_projeto=codigo_projeto)

    import datetime
    insert_leitura(
        "PROJ-DEFAULT",
        temperatura_max,
        temperatura_min,
        umidade,
        8.0,
        "hargreaves",
        calc["eto"],
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    return jsonify({"status": "sucesso", "mensagem": "Métricas de campo atualizadas e inseridas no banco de dados."}), 200

@app.route('/api/historico', methods=['GET'])
def obter_historico():
    historico = get_historico()
    return jsonify(historico), 200


@app.route('/api/bancos', methods=['GET', 'POST'])
def gerenciar_bancos():
    if request.method == 'GET':


@app.route('/api/projetos/<string:codigo_projeto>/cultura', methods=['POST'])
def vincular_cultura(codigo_projeto):
    """
    Rotina 2 - Vínculo de Kc
    """
@app.route('/api/hidraulica', methods=['POST'])
def obter_hidraulica():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    if 'So' in dados and 'k_linha' in dados and 'L_estimado' in dados:
def processar_hidraulica():
    dados = request.get_json()
    if not dados: return jsonify({"erro": "Nenhum dado enviado"}), 400
    pass

@app.route('/api/perda_carga', methods=['POST'])
def perda_carga():
    dados = request.get_json()
    if not dados or 'cultura_id' not in dados or 'estagio_selecionado' not in dados:
        return jsonify({"erro": "Os campos 'cultura_id' e 'estagio_selecionado' são obrigatórios."}), 400

    projeto = get_projeto_metadados(codigo_projeto)
    if not projeto:
        return jsonify({"erro": "Projeto inexistente. Configure os metadados primeiro."}), 404

    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400
    try:
        cultura_id = int(dados['cultura_id'])
        estagio_selecionado = str(dados['estagio_selecionado'])

        culturas = get_culturas()
        cultura_selecionada = next((c for c in culturas if c['id'] == cultura_id), None)
    except (ValueError, KeyError, TypeError):
        return jsonify({"erro": "Erro parsing json"}), 400
    except Exception as e:
        return jsonify({'erro': str(e)}), 400
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
        campos_basicos = ['diametro_mm', 'vazao_gotejador_lh', 'espacamento_m', 'comprimento_m']
        for c in campos_basicos:
            if c not in dados:
                if any(k in dados for k in ['So', 'k_linha', 'L_estimado']): return jsonify({"erro": "Os campos 'So', 'k_linha' e 'L_estimado' são obrigatórios."}), 400
                return jsonify({"erro": f"O campo '{c}' é obrigatório."}), 400
    resultado_final = {}
    if tem_perda:
        campos = ['diametro_mm', 'vazao_gotejador_lh', 'espacamento_m', 'comprimento_m']
        for c in campos:
            if c not in dados: return jsonify({"erro": f"O campo '{c}' é obrigatório."}), 400
        try:
            resultado_perda = calculador.calcular_perda_carga(float(dados['diametro_mm']), float(dados['vazao_gotejador_lh']), float(dados['espacamento_m']), float(dados['comprimento_m']))
            if "erro" in resultado_perda: return jsonify(resultado_perda), 400
            resultado_final.update(resultado_perda)
        except ValueError: return jsonify({"erro": "Todos os parâmetros devem ser números válidos."}), 400
    if tem_perfil:
        if 'So' not in dados or 'k_linha' not in dados or 'L_estimado' not in dados: return jsonify({"erro": "Os campos 'So', 'k_linha' e 'L_estimado' são obrigatórios."}), 400
        try:
            resultado_final["classificacao"] = calculador.classificar_perfil_pressao(float(dados['So']), float(dados['k_linha']), float(dados['L_estimado']))
        except ValueError: return jsonify({"erro": "Os valores de 'So', 'k_linha' e 'L_estimado' devem ser numéricos."}), 400
    return jsonify(resultado_final), 200
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

    elif all(campo in dados for campo in ['diametro_mm', 'vazao_gotejador_lh', 'espacamento_m', 'comprimento_m']):
        try:
            diametro_mm = float(dados['diametro_mm'])
            vazao_lh = float(dados['vazao_gotejador_lh'])
            espacamento = float(dados['espacamento_m'])
            comprimento = float(dados['comprimento_m'])
        except ValueError:
            return jsonify({"erro": "Parâmetros inválidos. Devem ser números."}), 400

        resultado = calculador.calcular_perda_carga(diametro_mm, vazao_lh, espacamento, comprimento)
        return jsonify(resultado), 200

    return jsonify({"erro": "Parâmetros insuficientes. Envie dados para perda de carga ou perfil topográfico."}), 400

@app.route('/api/projetos', methods=['POST'])
def salvar_projeto_metadados():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    campos_obrigatorios = ['codigo_projeto', 'nome_projeto', 'largura', 'altura', 'profundidade']
    for campo in campos_obrigatorios:
        if campo not in dados:
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

#        if not cultura_selecionada:
#            return jsonify({"erro": "Cultura inexistente."}), 404
#
#        vincular_cultura_projeto(codigo_projeto, cultura_id, estagio_selecionado)
#
#        kc_aplicado = calculador.definir_kc_por_estagio(
#            cultura_selecionada['kc_inicial'],
#            cultura_selecionada['kc_media'],
#            cultura_selecionada['kc_final'],
#            estagio_selecionado
#        )
#
#        return jsonify({
#            "status": "sucesso",
#            "mensagem": "Cultura vinculada com sucesso ao projeto",
#            "dados_vinculados": {
#                "codigo_projeto": codigo_projeto,
#                "cultura_id": cultura_id,
#                "estagio_selecionado": estagio_selecionado,
#                "kc_aplicado": kc_aplicado
#            }
#        }), 200
#        resultado = calculador.calcular_perda_carga(
#            diametro_mm,
#            vazao_gotejador_lh,
#            espacamento_m,
#            comprimento_m
#        )
#
#        if "erro" in resultado:
#            return jsonify(resultado), 400
#
#        return jsonify(resultado), 200
#
#    # If neither branch condition is fully met, check if we are missing fields for profile classification
#    if any(campo in dados for campo in ['So', 'k_linha', 'L_estimado']):
#         return jsonify({"erro": "Os campos 'So', 'k_linha' e 'L_estimado' são obrigatórios."}), 400
#
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

#    except ValueError:
#        return jsonify({"erro": "Tipos de dados invalidos"}), 400
#    except Exception as e:
#        return jsonify({"erro": str(e)}), 500
#
#        return jsonify({"erro": "Todos os parâmetros devem ser números válidos."}), 400
#
#    resultado = calculador.calcular_perda_carga(
#        diametro_mm,
#        vazao_gotejador_lh,
#        espacamento_m,
#        comprimento_m,
#        comprimento_equivalente_le
#    )
#
#    if "erro" in resultado:
#        return jsonify(resultado), 400
#    return jsonify({"erro": "Parâmetros inválidos"}), 400
#
#    validacao = calculador.validar_criterio_pressao_subunidade(
#        resultado['perda_carga_mca'],
#        pressao_entrada_mca
#    )
#
#    resultado.update(validacao)
#
#    return jsonify(resultado), 200
#
#@app.route('/api/projetos', methods=['POST'])
#def salvar_projeto_metadados():
#    dados = request.get_json()
#    if not dados:
#        return jsonify({"erro": "Nenhum dado enviado"}), 400
#
#    campos_obrigatorios = ['codigo_projeto', 'nome_projeto', 'largura', 'altura', 'profundidade']
#    for campo in campos_obrigatorios:
#        if campo not in dados:
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

def hidraulica():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

def processar_hidraulica():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    has_advanced = any(key in dados for key in ['declividade', 'So', 'k_linha', 'L_estimado', 'H', 'Hvar'])
    has_basic = all(key in dados for key in ['diametro_mm', 'vazao_gotejador_lh', 'espacamento_m', 'comprimento_m'])

    if not has_advanced and not has_basic:
        # Tenta identificar erro especifico do teste se enviou dados avancados incompletos
        if any(key in dados for key in ['So', 'k_linha', 'L_estimado']):
             return jsonify({"erro": "Os campos 'So', 'k_linha' e 'L_estimado' são obrigatórios."}), 400
        return jsonify({"erro": "Faltam parâmetros básicos (diametro_mm, etc) ou avançados (So, k_linha, etc)."}), 400

    resposta = {}

    if has_advanced:
        if 'So' not in dados or 'k_linha' not in dados or 'L_estimado' not in dados:
             return jsonify({"erro": "Os campos 'So', 'k_linha' e 'L_estimado' são obrigatórios."}), 400
@app.route('/api/classificar_perfil', methods=['POST'])
@app.route('/api/hidraulica', methods=['POST'])
def processar_hidraulica():


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
        return jsonify({"erro": "Nenhum dado JSON fornecido"}), 400

    required_keys = ['pressao_h', 'h_var_fraction', 'declividade_so', 'k_linha', 'L_estimado']
    for k in required_keys:
        if k not in dados:
             return jsonify({"erro": f"Parâmetro obrigatório ausente: {k}"}), 400
        return jsonify({"erro": "Nenhum dado enviado"}), 400

def obter_conexao():
    conn = sqlite3.connect("irrigacao.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return jsonify({"status": "Plataforma de Irrigacao Familar Ativa"}), 200

@app.route("/api/projetos/<string:codigo_projeto>/irn", methods=["POST"])
def calcular_irn_projeto_p58(codigo_projeto):
    try:
        pressao_h = float(dados['pressao_h'])
        h_var_fraction = float(dados['h_var_fraction'])
        declividade_so = float(dados['declividade_so'])
        k_linha = float(dados['k_linha'])
        l_estimado = float(dados['L_estimado'])
    except ValueError:
        return jsonify({"erro": "Os valores informados devem ser numéricos."}), 400

    calc = CalculadorIrrigacao()
    razo_ponto_minimo = calc.calcular_ponto_pressao_minima_ratio(declividade_so, k_linha, l_estimado)
    lmax_ii_b = calc.classificar_dimensionar_perfil_ii_b(pressao_h, h_var_fraction, k_linha, declividade_so, l_estimado)
    lmax_ii_a = calc.refinar_lmax_perfil_ii_a(pressao_h, h_var_fraction, k_linha, declividade_so)

    tipo_perfil = "Perfil Tipo II-b" if lmax_ii_b is not None else "Perfil Tipo II-a"
    lmax_final = lmax_ii_b if lmax_ii_b is not None else lmax_ii_a

    salvou = salvar_projeto_hidraulica_lateral(
        codigo_projeto, pressao_h, h_var_fraction, declividade_so, k_linha, l_estimado,
        razo_ponto_minimo, lmax_ii_a, lmax_ii_b, tipo_perfil
    )
        payload = request.get_json() or {}
        cc = payload.get("theta_cc")
        pmp = payload.get("theta_pmp")
        fator_f = payload.get("fator_f")
        pe = payload.get("pe", 0.0)
        tipo = payload.get("tipo_irrigacao", "total")

        if cc is None or pmp is None or fator_f is None or float(cc) < 0 or float(pmp) < 0 or float(fator_f) < 0:
            return jsonify({"erro": "Dados de entrada invalidos ou negativos"}), 400

        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT profundidade_z FROM projetos_metadados WHERE codigo_projeto = ?", (codigo_projeto,))
        row = cursor.fetchone()
        conn.close()

        if row is None:
            return jsonify({"erro": "Projeto nao encontrado"}), 404

        z = row[0] if row[0] is not None else 0.40 # Fallback seguro de engenharia

        calculador = CalculadorIrrigacao()
        cad = calculador.calcular_cad(cc, pmp, z)
        irn = calculador.calcular_irn_p58(cad, fator_f, pe, tipo)

        salvar_dados_solo_p58(codigo_projeto, fator_f, pe, tipo, cad, irn)

        return jsonify({
            "codigo_projeto": codigo_projeto,
            "cad_calculada": cad,
            "irn_calculada": irn
        }), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)

@app.route('/api/hidraulica', methods=['POST'])
def leitura_climatica():
    """
    Cálculo em Cadeia de ETo e Balanço de Radiação
    """
#        if "erro" in resultado:
#            return jsonify(resultado), 400
#
#        return jsonify(resultado), 200
#
#    return jsonify({"erro": "Payload inválido. Envie os parâmetros para classificação de perfil ou perda de carga."}), 400
#
#    # Advanced Flow: Pressure Profiles
#    tem_fluxo_avancado = any(campo in dados for campo in ['So', 'k_linha', 'L_estimado', 'declividade', 'H', 'Hvar'])
#
#    if tem_fluxo_avancado:
#        if 'So' not in dados or 'k_linha' not in dados or 'L_estimado' not in dados:
#             return jsonify({"erro": "Os campos 'So', 'k_linha' e 'L_estimado' são obrigatórios."}), 400
#        try:
#            So = float(dados['So'])
#            k_linha = float(dados['k_linha'])
#            L_estimado = float(dados['L_estimado'])
#
#            classificacao = calculador.classificar_perfil_pressao(So, k_linha, L_estimado)
#            resposta["classificacao"] = classificacao
#
#            if classificacao == 'Perfil Tipo IId (Declive Muito Forte)' and 'H' in dados and 'Hvar' in dados:
#                H = float(dados['H'])
#                Hvar = float(dados['Hvar'])
#                L_max = calculador.calcular_lmax_perfil_tipo_IId(H, Hvar, So, k_linha, L_estimado)
#                resposta["L_max"] = round(L_max, 2)
#        except ValueError as e:
#            if "Restrição de limite físico não atendida" in str(e):
#                 return jsonify({"erro": str(e)}), 400
#            return jsonify({"erro": "Os valores do fluxo avançado devem ser numéricos."}), 400
#
#    if not tem_fluxo_basico and not tem_fluxo_avancado:
#         return jsonify({"erro": "Parâmetros insuficientes para realizar cálculos hidráulicos."}), 400
#
#    return jsonify(resultado_final), 200
#
#    if not dados:
#        return jsonify({"erro": "Nenhum dado enviado"}), 400
#
#    resposta_combinada = {}
#    erro_ocorrido = False
#    mensagem_erro = ""
#
#    # Verifica parâmetros de topografia / perfil (obter_hidraulica original)
#    if 'So' in dados and 'k_linha' in dados and 'L_estimado' in dados:
#        try:
#            So = float(dados['So'])
#            k_linha = float(dados['k_linha'])
#            L_estimado = float(dados['L_estimado'])
#            classificacao = calculador.classificar_perfil_pressao(So, k_linha, L_estimado)
#            return jsonify({"classificacao": classificacao}), 200
#        except ValueError:
#            return jsonify({"erro": "Os valores de 'So', 'k_linha' e 'L_estimado' devem ser numéricos."}), 400
#
#    # Verifica parâmetros básicos (hidraulica original)
#    campos_basicos = ['diametro_mm', 'vazao_gotejador_lh', 'espacamento_m', 'comprimento_m']
#    tem_todos_basicos = all(campo in dados for campo in campos_basicos)
#
#    if tem_todos_basicos:
#        try:
#            diametro_mm = float(dados['diametro_mm'])
#            vazao_gotejador_lh = float(dados['vazao_gotejador_lh'])
#            espacamento_m = float(dados['espacamento_m'])
#            comprimento_m = float(dados['comprimento_m'])
#
#            resultado = calculador.calcular_perda_carga(
#                diametro_mm,
#                vazao_gotejador_lh,
#                espacamento_m,
#                comprimento_m
#            )
#            if "erro" in resultado:
#                return jsonify(resultado), 400
#            return jsonify(resultado), 200
#        except ValueError:
#            return jsonify({"erro": "Todos os parâmetros devem ser números válidos."}), 400
#
#    return jsonify({"erro": "Parâmetros não reconhecidos."}), 400
#
#    if not dados:
#        return jsonify({"erro": "Nenhum dado enviado"}), 400
#
#    campos_basicos = ['diametro_mm', 'vazao_gotejador_lh', 'espacamento_m', 'comprimento_m']
#    campos_avancados = ['So', 'k_linha', 'L_estimado']
#
#    tem_basico = all(campo in dados for campo in campos_basicos)
#    tem_avancado = all(campo in dados for campo in campos_avancados)
#
#    if not tem_basico and not tem_avancado:
#        return jsonify({"erro": "Parâmetros insuficientes. Envie os campos básicos ('diametro_mm', 'vazao_gotejador_lh', 'espacamento_m', 'comprimento_m') ou avançados ('So', 'k_linha', 'L_estimado')."}), 400
#
#    resposta = {}
#
#    if tem_basico:
#    if has_basic:
#        try:
#            diametro_mm = float(dados['diametro_mm'])
#            vazao_gotejador_lh = float(dados['vazao_gotejador_lh'])
#            espacamento_m = float(dados['espacamento_m'])
#            comprimento_m = float(dados['comprimento_m'])
#
#            resultado_basico = calculador.calcular_perda_carga(
#                diametro_mm, vazao_gotejador_lh, espacamento_m, comprimento_m
#            )
#            if "erro" in resultado_basico:
#                return jsonify(resultado_basico), 400
#            resposta.update(resultado_basico)
#        except ValueError:
#            return jsonify({"erro": "Todos os parâmetros básicos devem ser números válidos."}), 400
#
#    if not has_advanced and not has_basic:
#         return jsonify({"erro": "Parâmetros insuficientes para realizar cálculos hidráulicos."}), 400
#
#    return jsonify(resposta), 200
#
#@app.route('/api/hidraulica_legacy', methods=['POST'])
#def obter_hidraulica_legacy():
#    pass
#
#def classificar_perfil():
#    dados_recebidos = request.get_json()
#    if not dados_recebidos or 'So' not in dados_recebidos or 'k_linha' not in dados_recebidos or 'L_estimado' not in dados_recebidos:
#        return jsonify({"erro": "Os campos 'So', 'k_linha' e 'L_estimado' são obrigatórios."}), 400
#    else:
#        return jsonify({"erro": "O campo 'diametro_mm' é obrigatório."}), 400
#
#@app.route('/api/projetos', methods=['POST'])
#def salvar_projeto_metadados():
#    dados = request.get_json()
#    if not dados:
#        return jsonify({"erro": "Payload invalido"}), 400
#
#    try:
#        t_max = float(dados.get('t_max', 30.0))
#        t_min = float(dados.get('t_min', 20.0))
#        latitude = float(dados.get('latitude', -22.0))
#        mes_index = int(dados.get('mes_index', 1))
#
#        eto = calculador.calcular_eto_hargreaves(t_max, t_min, latitude, mes_index)
#
#        # Insert reading into historico_leitura
#        leitura_id = insert_leitura(
#            umidade=float(dados.get('ur_media', 60.0)),
#            temperatura_max=t_max,
#            temperatura_min=t_min,
#            eto_calculada=eto,
#            cad_calculada=0.0,
#            irn_calculada=0.0,
#            comprimento_lateral_m=0.0,
#            perda_carga_total_mca=0.0
#    if is_classificacao:
#        if 'So' not in dados or 'k_linha' not in dados or 'L_estimado' not in dados:
#            return jsonify({"erro": "Os campos 'So', 'k_linha' e 'L_estimado' são obrigatórios."}), 400
#        try:
#            So = float(dados['So'])
#            k_linha = float(dados['k_linha'])
#            L_estimado = float(dados['L_estimado'])
#            classificacao = calculador.classificar_perfil_pressao(So, k_linha, L_estimado)
#            resultado_final["classificacao"] = classificacao
#        except ValueError:
#            return jsonify({"erro": "Os valores de 'So', 'k_linha' e 'L_estimado' devem ser numéricos."}), 400
#
#    if tem_perda:
#    return jsonify(resultado_final), 200
#
#    if has_basic:
#        resultado_final["classificacao"] = calculador.classificar_perfil_pressao(So, k_linha, L_estimado)
#
#    if is_perda_carga:
#        campos_obrigatorios = ['diametro_mm', 'vazao_gotejador_lh', 'espacamento_m', 'comprimento_m']
#        for campo in campos_obrigatorios:
#            if campo not in dados:
#                return jsonify({"erro": f"O campo '{campo}' é obrigatório."}), 400
#        try:
#            diametro_mm = float(dados['diametro_mm'])
#            vazao_gotejador_lh = float(dados['vazao_gotejador_lh'])
#            espacamento_m = float(dados['espacamento_m'])
#            comprimento_m = float(dados['comprimento_m'])
#            resultado = calculador.calcular_perda_carga(diametro_mm, vazao_gotejador_lh, espacamento_m, comprimento_m)
#            if "erro" in resultado:
#                return jsonify(resultado), 400
#            resultado_final.update(resultado)
#        except ValueError:
#            return jsonify({"erro": "Todos os parâmetros devem ser números válidos."}), 400
#
#    return jsonify(resultado_final), 200
#
#@app.route('/api/projetos', methods=['POST'])
#def criar_projeto():
#    dados = request.get_json()
#    if not dados or 'codigo_projeto' not in dados:
#        return jsonify({"erro": "O campo 'codigo_projeto' é obrigatório."}), 400
#
#    from backend.database import get_projeto_metadados, insert_projeto
#    projeto_existente = get_projeto_metadados(dados['codigo_projeto'])
#        resultado = calculador.calcular_perda_carga(
#            diametro_mm,
#            vazao_gotejador_lh,
#            espacamento_m,
#            comprimento_m
#        )
#
#        return jsonify({
#            "status": "sucesso",
#            "id": leitura_id,
#            "eto": eto
#        }), 201
#
#    except Exception as e:
#        return jsonify({"erro": str(e)}), 400
#
        if "erro" in resultado:
            return jsonify(resultado), 400

        return jsonify(resultado), 200

    return jsonify({"erro": "Payload inválido. Envie os parâmetros para classificação de perfil ou perda de carga."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

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

@app.route('/api/perda_carga', methods=['POST'])
def perda_carga():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    try:
        diametro_mm = float(dados['diametro_mm'])
        vazao_lh = float(dados['vazao_gotejador_lh'])
        espacamento = float(dados['espacamento_m'])
        comprimento = float(dados['comprimento_m'])
    except ValueError:
        return jsonify({"erro": "Parâmetros inválidos. Devem ser números."}), 400
    except KeyError as e:
        return jsonify({"erro": f"O campo '{e.args[0]}' é obrigatório."}), 400

    resultado = calculador.calcular_perda_carga(diametro_mm, vazao_lh, espacamento, comprimento)
    return jsonify(resultado), 200





@app.route('/api/projetos', methods=['POST'])
def salvar_projeto():
    try:
        So = float(dados_recebidos['So'])
        k_linha = float(dados_recebidos['k_linha'])
        L_estimado = float(dados_recebidos['L_estimado'])
    except ValueError:
        return jsonify({"erro": "Os valores de 'So', 'k_linha' e 'L_estimado' devem ser numéricos."}), 400
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


@app.route('/api/projetos/<string:codigo_projeto>/area-umedecida', methods=['POST'])
def calcular_area_umedecida_endpoint(codigo_projeto):
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    projeto = obter_projeto_por_codigo(codigo_projeto)
    if not projeto:
        return jsonify({"erro": "Projeto não encontrado."}), 400

    campos_necessarios = [
        'tipo_disposicao', 'configuracao_linha', 'parametro_alpha',
        'condutividade_ko', 'profundidade_z', 'q_vazao',
        'espacamento_plantas_sp', 'espacamento_fileiras_sr'
    ]

    for campo in campos_necessarios:
        if campo not in dados:
            return jsonify({"erro": f"O campo '{campo}' é obrigatório."}), 400

    tipo_disposicao = dados['tipo_disposicao']
    configuracao_linha = dados['configuracao_linha']

    if tipo_disposicao not in ['faixa_continua', 'por_arvore']:
        return jsonify({"erro": "tipo_disposicao deve ser 'faixa_continua' ou 'por_arvore'."}), 400

    if configuracao_linha not in ['LLS', 'LLD']:
        return jsonify({"erro": "configuracao_linha deve ser 'LLS' ou 'LLD'."}), 400

    try:
        params = {
            'parametro_alpha': float(dados['parametro_alpha']),
            'condutividade_ko': float(dados['condutividade_ko']),
            'profundidade_z': float(dados['profundidade_z']),
            'q_vazao': float(dados['q_vazao']),
            'espacamento_plantas_sp': float(dados['espacamento_plantas_sp']),
            'espacamento_fileiras_sr': float(dados['espacamento_fileiras_sr']),
            'np_emissores': int(dados.get('np_emissores', 1))
        }

        for key, value in params.items():
            if value < 0:
                return jsonify({"erro": f"O valor de '{key}' não pode ser negativo."}), 400

    except ValueError:
        return jsonify({"erro": "Os parâmetros físicos devem ser numéricos."}), 400

    resultado = calculador.calcular_area_umedecida_fluxograma(
        tipo_disposicao,
        configuracao_linha,
        params
    )

    if "erro" in resultado:
        return jsonify(resultado), 400

    dados_para_salvar = {
        'tipo_disposicao': tipo_disposicao,
        'configuracao_linha': configuracao_linha,
        'parametro_alpha': params['parametro_alpha'],
        'condutividade_ko': params['condutividade_ko'],
        'profundidade_z': params['profundidade_z'],
        'rw_calculado': resultado['rw'],
        'dw_calculado': resultado['dw'],
        'pw_final': resultado['pw']
    }

    from database import salvar_dados_area_umedecida
    sucesso = salvar_dados_area_umedecida(codigo_projeto, dados_para_salvar)
    if not sucesso:
        return jsonify({"erro": "Falha ao salvar os dados no banco."}), 500

    return jsonify({
        "status": "sucesso",
        "dados_calculados": resultado
    }), 200
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

@app.route('/api/culturas', methods=['GET'])
def obter_culturas():
    culturas = get_culturas()
    return jsonify(culturas), 200



    return jsonify({"status": "sucesso", "mensagem": "Projeto criado com sucesso"}), 201

    if not salvou:
        return jsonify({"erro": "Falha ao persistir no banco de dados."}), 500

    return jsonify({
        "codigo_projeto": codigo_projeto,
        "perfil_pressao_tipo": tipo_perfil,
        "posicao_pressao_minima_ratio": round(razo_ponto_minimo, 4),
        "comprimento_maximo_m": lmax_final,
        "detalhes": {
            "lmax_calculado_perfil_iia": lmax_ii_a,
            "lmax_calculado_perfil_iib": lmax_ii_b
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    sucesso = insert_projeto(dados)
    if not sucesso:
        return jsonify({"erro": "Este Código já existe"}), 400


@app.route('/api/projetos/<string:codigo_projeto>', methods=['GET'])
def abrir_projeto(codigo_projeto):
    projeto = obter_projeto_por_codigo(codigo_projeto)
    if projeto:
        return jsonify(projeto), 200
    else:
        return jsonify({"erro": "Projeto não encontrado"}), 404

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
@app.route('/api/projetos/<string:codigo_projeto>/area-sombreada', methods=['POST'])
def calcular_e_salvar_area_sombreada(codigo_projeto):
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({'erro': 'Nenhum dado JSON fornecido'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
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

@app.route('/api/projetos/<string:codigo_projeto>/linha-lateral-declive', methods=['POST'])
def calcular_linha_lateral_declive_endpoint(codigo_projeto):

@app.route('/api/projetos/<string:codigo_projeto>/linha-derivacao', methods=['POST'])
def configurar_linha_derivacao(codigo_projeto):
    '''
    Rotina 10 - Dimensionamento da Linha de Derivação (Pág 74)
    '''
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Payload invalido"}), 400

    from backend.database import obter_projeto_por_codigo, salvar_hidraulica_derivacao
    projeto = obter_projeto_por_codigo(codigo_projeto)
    if not projeto:
        return jsonify({"erro": "Projeto não encontrado"}), 404

    campos_obrigatorios = [
        'declividade_derivacao', 'pressao_entrada_h', 'comprimento_total_l',
        'vazao_ql', 'espacamento_sl', 'distancia_sl1', 'variacao_hvar'
    ]

    for campo in campos_obrigatorios:
        if campo not in dados or dados[campo] is None:
            return jsonify({"erro": f"O campo '{campo}' é obrigatório."}), 400

    try:
        declividade = float(dados['declividade_derivacao'])
        h_pressao = float(dados['pressao_entrada_h'])
        l_comprimento = float(dados['comprimento_total_l'])
        ql_vazao = float(dados['vazao_ql'])
        sl_espacamento = float(dados['espacamento_sl'])
        sl1_distancia = float(dados['distancia_sl1'])
        hvar_limite = float(dados['variacao_hvar'])
    except ValueError:
        return jsonify({"erro": "Os parâmetros obrigatórios devem ser numéricos."}), 400

    zitterell_status = 1
    alertas_zitterell = []
    z_fields = ['die', 'dis', 'lc', 'dt', 'vt', 'reynolds']
    if all(k in dados and dados[k] is not None for k in z_fields):
        try:
            validador = calculador.validar_limites_conector_zitterell(
                float(dados['die']), float(dados['dis']), float(dados['lc']),
                float(dados['dt']), float(dados['vt']), float(dados['reynolds'])
            )
            if not validador['valido']:
                zitterell_status = 0
                alertas_zitterell = validador['alertas']
        except ValueError:
            pass

    resultado = calculador.orquestrar_dimensionamento_derivacao(
        declividade, h_pressao, l_comprimento, ql_vazao, sl_espacamento, sl1_distancia, hvar_limite
    )

    salvar_hidraulica_derivacao(
        codigo_projeto, declividade, h_pressao, l_comprimento, ql_vazao,
        sl_espacamento, sl1_distancia, hvar_limite, resultado['estrategia_dimensionamento'],
        zitterell_status
    )

    resposta = {
        **resultado,
        'alertas': alertas_zitterell
    }

    return jsonify(resposta), 200
@app.route('/api/projetos/<string:codigo_projeto>/agricultura-familiar-otimizada', methods=['POST'])
def otimizar_agricultura_familiar(codigo_projeto):
    from backend.database import get_projeto_metadados, obter_indicadores_basicos_projeto, salvar_dados_agricultura_familiar
    from backend.models.irrigacao import CalculadorIrrigacao

    projeto = get_projeto_metadados(codigo_projeto)
    if not projeto:
        return jsonify({"erro": "Projeto não encontrado"}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    campos_obrig = ['capacidade_cisterna_l', 'volume_atual_l', 'area_captacao_m2', 'area_horta_m2', 'precipitacao_mm', 'lista_culturas', 'q_bomba_lh']
    for c in campos_obrig:
        if c not in dados:
            return jsonify({"erro": f"O campo {c} é obrigatório"}), 400

    try:
        capacidade_cisterna_l = float(dados['capacidade_cisterna_l'])
        volume_atual_l = float(dados['volume_atual_l'])
        area_captacao_m2 = float(dados['area_captacao_m2'])
        area_horta_m2 = float(dados['area_horta_m2'])
        precipitacao_mm = float(dados['precipitacao_mm'])
        q_bomba_lh = float(dados['q_bomba_lh'])
        lista_culturas = dados['lista_culturas']
        lista_setores_vazao_lh = dados.get('lista_setores_vazao_lh', [])

        if area_captacao_m2 <= 0 or area_horta_m2 <= 0:
            return jsonify({"erro": "Áreas não podem ser nulas ou negativas"}), 400

        if not isinstance(lista_culturas, list):
            return jsonify({"erro": "lista_culturas deve ser um array de objetos"}), 400

    except (ValueError, TypeError):
        return jsonify({"erro": "Formato de dados inválido"}), 400

    indicadores = obter_indicadores_basicos_projeto(codigo_projeto)
    eto = indicadores.get('eto', 4.5)
    kl = indicadores.get('kl', 1.0)
    itn = indicadores.get('itn', 5.0)

    calculador = CalculadorIrrigacao()

    etc_consorcio = calculador.calcular_et_consorcio(eto, kl, lista_culturas)
    kc_consorcio = sum(c.get('kc', 0) * c.get('fracao_area', 0) for c in lista_culturas)
    kc_consorcio = min(kc_consorcio, 1.30)

    cisterna = calculador.simular_autonomia_cisterna(
        volume_atual=volume_atual_l,
        capacidade_max=capacidade_cisterna_l,
        area_irrigada_m2=area_horta_m2,
        lamina_itn_mm=itn,
        precipitacao_mm=precipitacao_mm,
        area_captacao_m2=area_captacao_m2
    )

    bomba = calculador.escalonar_setores_familiar(q_bomba_lh, lista_setores_vazao_lh)

    salvo = salvar_dados_agricultura_familiar(
        codigo_projeto,
        capacidade_cisterna_l,
        area_captacao_m2,
        area_horta_m2,
        kc_consorcio,
        etc_consorcio,
        cisterna['autonomia_dias'],
        bomba['turnos_bomba']
    )

    if not salvo:
        return jsonify({"erro": "Erro ao salvar no banco de dados"}), 500

    return jsonify({
        "status": "sucesso",
        "otimizacao": {
            "etc_consorcio": etc_consorcio,
            "kc_consorcio": round(kc_consorcio, 2),
            "cisterna": cisterna,
            "bomba": bomba
        }
@app.route('/api/projetos/<string:codigo_projeto>/linha-lateral-definitiva', methods=['POST'])
def linha_lateral_definitiva(codigo_projeto):
    """
    Roteamento interno superior para cálculo do L_max da linha lateral (Rotina de Declive e Plano/Aclive).
    """
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Nenhum dado enviado."}), 400

    required_fields = ['pressao_h', 'h_var_fraction', 'k_linha', 'declividade_so']
    for field in required_fields:
        if field not in dados:
            return jsonify({"erro": f"Campo obrigatório ausente: {field}"}), 400

    projeto = get_projeto_metadados(codigo_projeto)
    if not projeto:
        return jsonify({"erro": "Projeto inexistente."}), 404

    try:
        pressao_h = float(dados['pressao_h'])
        h_var_fraction = float(dados['h_var_fraction'])
        k_linha = float(dados['k_linha'])
        declividade_so = float(dados['declividade_so'])

        calc = CalculadorIrrigacao()

        if declividade_so >= 0:
            # Perfil Tipo I
            l_max = calc.calcular_lmax_perfil_tipo_I(pressao_h, h_var_fraction, declividade_so, k_linha)
            perfil = "Perfil Tipo I (Plano/Aclive)"
            status = "safe"
        else:
            # Perfil Tipo II/III (Declive)
            l_max, perfil = calc.orquestrar_comprimento_declive(pressao_h, h_var_fraction, k_linha, declividade_so)
            status = "seguro" if l_max > 0.0 else "divisao_por_zero_evitada"

        if salvar_hidraulica_lateral(codigo_projeto, perfil, float(l_max), status):
            return jsonify({
                "status": "sucesso",
                "perfil_selecionado": perfil,
                "comprimento_limite_m": round(l_max, 3),
                "denominador_seguro_status": status
            }), 200
        else:
            return jsonify({"erro": "Erro ao salvar no banco de dados."}), 500

    except Exception as e:
        return jsonify({"erro": f"Erro matemático/interno: {str(e)}"}), 400

@app.route('/api/projetos/<string:codigo_projeto>/perdas-conexoes', methods=['POST'])
def calcular_e_salvar_perdas_conexoes(codigo_projeto):
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({'erro': 'Nenhum dado JSON fornecido'}), 400

        from backend.database import get_projeto_metadados, insert_projeto_hidraulica_lateral
        projeto = get_projeto_metadados(codigo_projeto)
        if not projeto:
            return jsonify({'erro': 'Projeto inexistente. Configure os metadados primeiro.'}), 404

        H = float(dados.get('H', 10.0))
        H_var = float(dados.get('H_var', 0.2))
        So = float(dados.get('So', 0.05))
        k_linha = float(dados.get('k_linha', 1.5e-5))
        q_media = float(dados.get('q_media', 2.0))
        se_vazao = float(dados.get('se_vazao', 0.5))
        L_estimado = float(dados.get('L_estimado', 50.0))
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

        perfil = calc.classificar_perfil_pressao(So, k_linha, L_estimado)
        l_max = 0.0

        if 'Perfil Tipo IIc' in perfil:
            l_max = calc.resolver_lmax_perfil_ii_c(H, H_var, k_linha, So)
            status_op = "Calculado com Sucesso"
        elif 'Perfil Tipo IId' in perfil:
            status_op = "Registrado Perfil Extremo"
        else:
            status_op = "Fora da faixa de declive forte"

        insert_projeto_hidraulica_lateral(codigo_projeto, k_linha, se_vazao, q_media, l_max, perfil)

        return jsonify({
            'perfil': perfil,
            'l_max': l_max,
            'status': status_op
        }), 200

    except ValueError as e:
        return jsonify({'erro': 'Os valores devem ser numericos.'}), 400
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
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

@app.route("/api/projetos/<string:codigo_projeto>/irn", methods=["POST"])
def calcular_irn_projeto(codigo_projeto):
    payload = request.get_json() or {}
    cc = payload.get("theta_cc")
    pmp = payload.get("theta_pmp")
    fator_f = payload.get("fator_f")

    if cc is None or pmp is None or fator_f is None or float(cc) < 0 or float(pmp) < 0 or float(fator_f) < 0:
        return jsonify({"erro": "Dados malformados ou negativos"}), 400

    import backend.database
    conn = backend.database.get_db_connection()
    cursor = conn.cursor()
    # Handle the fact that 'etc_calculada' might not exist immediately if old schema
    try:
        cursor.execute("SELECT etc_calculada, profundidade_z FROM projetos_metadados WHERE codigo_projeto = ?", (codigo_projeto,))
        row = cursor.fetchone()
    except:
        row = None
    conn.close()

    if not row:
        return jsonify({"erro": "Projeto nao encontrado"}), 404

    etc = row['etc_calculada'] if 'etc_calculada' in row.keys() else 4.5
    z = row['profundidade_z'] if 'profundidade_z' in row.keys() else 0.4
    if etc is None or z is None:
        etc = 4.5
        z = 0.4

    calculador = CalculadorIrrigacao()
    cad = calculador.calcular_cad_solo(cc, pmp, z)
    resultado = calculador.calcular_irn_e_turno_rega(cad, fator_f, etc)

    backend.database.salvar_dados_solo_irn(codigo_projeto, cc, pmp, fator_f, cad, resultado["irn"], resultado["turno_rega"])

    return jsonify({
        "codigo_projeto": codigo_projeto,
        "cad_calculado": cad,
        "raw_calculado": resultado["raw"],
        "turno_rega_final": resultado["turno_rega"],
        "irn_final": resultado["irn"]
    }), 200
