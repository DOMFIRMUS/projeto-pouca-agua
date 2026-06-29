with open("backend/app.py", "r") as f:
    content = f.read()

# Define API key validation logic
api_key_logic = """
    # Validar API Key
    if 'api_key' not in dados_recebidos or dados_recebidos['api_key'] != 'CHAVE_SECRETA_123':
        return jsonify({"erro": "Não autorizado. Chave de API inválida ou ausente."}), 401
"""

# Insert right after: umidade = float(dados_recebidos['umidade'])
# First we find the place to insert
target_string = "umidade = float(dados_recebidos['umidade'])\n"

content = content.replace(target_string, target_string + api_key_logic)

with open("backend/app.py", "w") as f:
    f.write(content)
