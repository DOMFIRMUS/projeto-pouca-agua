with open('backend/app.py', 'r') as f:
    content = f.read()

# Let's fix the metricas_tese first in pristine
import re

# find the metricas_tese dictionary block and clean it up by regex or string replacement
# since the pristine file also has duplicate lines, we need to extract and replace the broken block

def fix_metricas(content):
    start = content.find('"metricas_tese": {')
    if start == -1: return content

    end = content.find('}', start)
    if end == -1: return content

    # Actually just string replace the broken line because there's a missing comma
    # "irrigacao_total_necessaria_mm": calc["itn"]\n            "evapotranspiracao_referencia_mm_dia": eto,

    fixed_content = content.replace('"irrigacao_total_necessaria_mm": calc["itn"]\n            "evapotranspiracao_referencia_mm_dia": eto,', '"irrigacao_total_necessaria_mm": calc["itn"],\n            "evapotranspiracao_referencia_mm_dia": eto,')

    # Clean the multiple duplicates if there are syntax errors
    return fixed_content

new_content = fix_metricas(content)

# Now, add the routes
if 'obter_projeto_por_codigo' not in new_content:
    new_content = new_content.replace("from database import init_db", "from database import obter_projeto_por_codigo, obter_resumo_hidraulico, init_db", 1)

new_route = """@app.route('/api/projetos/<string:codigo_projeto>', methods=['GET'])
def abrir_projeto(codigo_projeto):
    projeto = obter_projeto_por_codigo(codigo_projeto)
    if projeto:
        return jsonify(projeto), 200
    else:
        return jsonify({"erro": "Projeto não encontrado"}), 404

"""

new_content = new_content.replace("@app.route('/api/relatorio-dimensionamento', methods=['GET'])", new_route + "@app.route('/api/relatorio-dimensionamento', methods=['GET'])")

with open('backend/app_cleaned.py', 'w') as f:
    f.write(new_content)
