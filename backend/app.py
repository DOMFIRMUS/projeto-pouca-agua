from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.models.irrigacao import CalculadorIrrigacao
from backend.database import obter_projeto_por_codigo, salvar_projeto_hidraulica_lateral

app = Flask(__name__)
CORS(app)

@app.route('/api/projetos/<string:codigo_projeto>/linha-lateral-declive', methods=['POST'])
def linha_lateral_declive_endpoint(codigo_projeto):
    projeto = obter_projeto_por_codigo(codigo_projeto)
    if not projeto:
        return jsonify({"erro": "Projeto inexistente."}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Nenhum dado JSON fornecido"}), 400

    required_keys = ['pressao_h', 'h_var_fraction', 'declividade_so', 'k_linha', 'L_estimado']
    for k in required_keys:
        if k not in dados:
             return jsonify({"erro": f"Parâmetro obrigatório ausente: {k}"}), 400

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
