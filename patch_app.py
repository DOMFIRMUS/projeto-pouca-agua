import sys

def patch_file():
    with open('backend/app.py', 'r') as f:
        content = f.read()

    new_content = content.replace(
'''<<<<<<< HEAD
@app.route('/api/hidraulica', methods=['POST'])
def obter_hidraulica():
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
=======
@app.route('/api/culturas', methods=['GET'])
def obter_culturas():
    culturas = get_culturas()
    return jsonify(culturas), 200
>>>>>>> origin/main''',
'''@app.route('/api/culturas', methods=['GET'])
def obter_culturas():
    culturas = get_culturas()
    return jsonify(culturas), 200

@app.route('/api/hidraulica', methods=['POST'])
def obter_hidraulica():
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

    return jsonify({"classificacao": classificacao}), 200''')

    with open('backend/app.py', 'w') as f:
        f.write(new_content)

patch_file()
