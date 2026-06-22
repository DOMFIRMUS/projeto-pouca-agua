import os
import sqlite3
import json
from flask import Flask, jsonify, request
from flask_cors import CORS

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
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route('/api/projetos/<string:codigo_projeto>/cultura', methods=['POST'])
def vincular_cultura(codigo_projeto):
    """
    Rotina 2 - Vínculo de Kc
    """
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

    except ValueError:
        return jsonify({"erro": "Tipos de dados invalidos"}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route('/api/projetos/<string:codigo_projeto>/area-umedecida', methods=['POST'])
def calcular_area_umedecida_endpoint(codigo_projeto):
    """
    Rotina 4 - Pw (Raio Umedecido Rw, Diametro Molhado Dw, Area Umedecida Pw)
    """
    dados = request.get_json()
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
