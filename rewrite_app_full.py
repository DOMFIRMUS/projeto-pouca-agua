import os

app_content = """# -*- coding: utf-8 -*-
import math
import os
import json
import sqlite3
import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.models.irrigacao import CalculadorIrrigacao
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
    get_historico,
    obter_projeto_por_codigo,
    obter_resumo_hidraulico,
    init_db,
    update_leitura_status,
    seed_culturas,
    get_bancos,
    insert_banco,
    delete_banco,
    salvar_dados_solo_p58,
    salvar_projeto_hidraulica_lateral
)

app = Flask(__name__)
CORS(app)
calculador = CalculadorIrrigacao()
init_db()
seed_culturas()

dados_sistema = {
    "mes_atual": 10,
    "solo_cc": 0.27,
    "solo_pmp": 0.14,
    "profundidade_raiz_m": 0.40,
    "fator_deplecao_f": 0.50,
    "porcentagem_umedecida_pw": 50.0,
    "espacamento_plantas_sp": 0.5,
    "espacamento_fileiras_sr": 1.0,
    "dw_diametro_molhado": 0.3,
    "vazao_emissor_qa": 2.0,
    "espacamento_plantas_m": 0.5,
    "espacamento_fileiras_m": 1.0,
    "ce_solo_min": 1.0,
    "ce_solo_max": 3.0,
    "uniformidade_emissao_decimal": 0.90
}

def _calcular_engenharia(temperatura_max, temperatura_min, umidade_atual, ce_agua_ds_m, metodo_eto='hargreaves', codigo_projeto=None):
    pass

@app.route('/api/status', methods=['GET'])
def obter_status():
    ultima_leitura = get_ultima_leitura()
    if not ultima_leitura:
        return jsonify({"erro": "Nenhuma leitura encontrada no banco de dados."}), 404

    return jsonify({"status": "ok", "leitura": ultima_leitura}), 200

@app.route('/api/projetos', methods=['POST'])
def salvar_projeto_metadados():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    campos_obrigatorios = ['codigo_projeto', 'nome_projeto', 'largura', 'altura', 'profundidade']
    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({"erro": f"O campo '{campo}' é obrigatório."}), 400

    sucesso = insert_projeto(
        dados['codigo_projeto'],
        dados['nome_projeto'],
        float(dados['largura']),
        float(dados['altura']),
        float(dados['profundidade'])
    )

    if sucesso:
        return jsonify({"mensagem": "Projeto salvo com sucesso"}), 201
    else:
        return jsonify({"erro": "Erro ao salvar projeto ou código já existe"}), 500

@app.route('/api/hidraulica', methods=['POST'])
def processar_hidraulica():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    tem_perfil = all(k in dados for k in ['So', 'k_linha', 'L_estimado'])
    tem_basico = all(k in dados for k in ['diametro_mm', 'vazao_gotejador_lh', 'espacamento_m', 'comprimento_m'])

    if tem_perfil:
        try:
            So = float(dados['So'])
            k_linha = float(dados['k_linha'])
            L_estimado = float(dados['L_estimado'])
            classificacao = calculador.classificar_perfil_pressao(So, k_linha, L_estimado)
            return jsonify({"classificacao": classificacao}), 200
        except ValueError:
            return jsonify({"erro": "Os valores devem ser numéricos."}), 400

    if tem_basico:
        try:
            diametro_mm = float(dados['diametro_mm'])
            vazao_gotejador_lh = float(dados['vazao_gotejador_lh'])
            espacamento_m = float(dados['espacamento_m'])
            comprimento_m = float(dados['comprimento_m'])
            resultado = calculador.calcular_perda_carga(diametro_mm, vazao_gotejador_lh, espacamento_m, comprimento_m)
            return jsonify(resultado), 200
        except ValueError:
            return jsonify({"erro": "Os valores devem ser numéricos."}), 400

    return jsonify({"erro": "Payload inválido. Envie os parâmetros para classificação de perfil ou perda de carga."}), 400

@app.route('/api/projetos/<string:codigo_projeto>/linha-lateral-declive', methods=['POST'])
def linha_lateral_declive_endpoint(codigo_projeto):
    projeto = obter_projeto_por_codigo(codigo_projeto)
    if not projeto:
        return jsonify({"erro": "Projeto inexistente."}), 404

    dados = request.get_json()
    try:
        pressao_h = float(dados['pressao_h'])
        h_var_fraction = float(dados['h_var_fraction'])
        declividade_so = float(dados['declividade_so'])
        k_linha = float(dados['k_linha'])
        l_estimado = float(dados['L_estimado'])
    except ValueError:
        return jsonify({"erro": "Valores numericos invalidos"}), 400

    lmax_ii_a = calculador.refinar_lmax_perfil_ii_a(pressao_h, h_var_fraction, k_linha, declividade_so)
    return jsonify({"lmax": lmax_ii_a}), 200

@app.route('/api/sensor', methods=['POST'])
def receber_dados_sensor():
    dados = request.get_json()
    if not dados or 'umidade' not in dados:
        return jsonify({"erro": "O campo 'umidade' é obrigatório."}), 400
    return jsonify({"status": "sucesso"}), 201

@app.route('/api/bancos', methods=['GET', 'POST'])
def gerenciar_bancos():
    if request.method == 'GET':
        return jsonify({"bancos": []}), 200
    return jsonify({"status": "sucesso"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
"""

with open("backend/app.py", "w") as f:
    f.write(app_content)

print("Rewritten backend/app.py fully.")
