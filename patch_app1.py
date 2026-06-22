with open('backend/app.py', 'r') as f:
    content = f.read()

# Make sure we import the new functions
if 'obter_projeto_por_codigo' not in content:
    content = content.replace("from database import init_db", "from database import obter_projeto_por_codigo, obter_resumo_hidraulico, init_db", 1)

new_route = """@app.route('/api/projetos/<string:codigo_projeto>', methods=['GET'])
def abrir_projeto(codigo_projeto):
    projeto = obter_projeto_por_codigo(codigo_projeto)
    if projeto:
        return jsonify(projeto), 200
    else:
        return jsonify({"erro": "Projeto não encontrado"}), 404

"""

# Append the new route before the relatorio_dimensionamento route
content = content.replace("@app.route('/api/relatorio-dimensionamento', methods=['GET'])", new_route + "@app.route('/api/relatorio-dimensionamento', methods=['GET'])")

with open('backend/app.py', 'w') as f:
    f.write(content)
