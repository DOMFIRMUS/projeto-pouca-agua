# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
import sqlite3
from backend.database import init_db, salvar_dados_solo_p58
from backend.models.irrigacao import CalculadorIrrigacao

app = Flask(__name__)
init_db()

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
