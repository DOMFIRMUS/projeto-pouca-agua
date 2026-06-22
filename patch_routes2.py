with open('backend/app.py', 'r') as f:
    content = f.read()

# Since git clean -fd doesn't clean modified tracked files, let's just make sure there are no duplicate routes
import re

content = re.sub(r"@app\.route\('/api/projetos/<string:codigo_projeto>', methods=\['GET'\]\)\s*def abrir_projeto\(codigo_projeto\):[\s\S]*?return jsonify\(\{\"erro\": \"Projeto não encontrado\"\}\), 404\n\n", "", content)
content = re.sub(r"@app\.route\('/api/projetos/<string:codigo_projeto>/resumo', methods=\['GET'\]\)\s*def consolidacao_resultados\(codigo_projeto\):[\s\S]*?return jsonify\(\{[\s\S]*?\}\), 200\n", "", content)

routes = """
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

"""

content = content.replace("if __name__ == '__main__':", routes + "if __name__ == '__main__':")

with open('backend/app.py', 'w') as f:
    f.write(content)
