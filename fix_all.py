import re
import os

with open('backend/database.py', 'r') as f:
    db_content = f.read()

# 1. database.py - add codigo_projeto to historico_leitura safely
db_content = db_content.replace(
    'CREATE TABLE IF NOT EXISTS historico_leitura (\n            id INTEGER PRIMARY KEY AUTOINCREMENT,\n            umidade REAL',
    'CREATE TABLE IF NOT EXISTS historico_leitura (\n            id INTEGER PRIMARY KEY AUTOINCREMENT,\n            codigo_projeto TEXT,\n            umidade REAL'
)

alter_table = """    cursor.execute("PRAGMA table_info(historico_leitura)")
    columns = [info[1] for info in cursor.fetchall()]
    if 'codigo_projeto' not in columns:
        cursor.execute('ALTER TABLE historico_leitura ADD COLUMN codigo_projeto TEXT')
"""

db_content = db_content.replace("    cursor.execute('''\n        CREATE TABLE IF NOT EXISTS culturas", alter_table + "    cursor.execute('''\n        CREATE TABLE IF NOT EXISTS culturas")


# 2. Add obter_projeto_por_codigo and obter_resumo_hidraulico to database.py
new_funcs = """
def obter_projeto_por_codigo(codigo_projeto):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projetos_metadados WHERE codigo_projeto = ?', (codigo_projeto,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def obter_resumo_hidraulico(codigo_projeto):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM historico_leitura
        WHERE codigo_projeto = ?
        ORDER BY id DESC LIMIT 1
    ''', (codigo_projeto,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None
"""

db_content += new_funcs

with open('backend/database.py', 'w') as f:
    f.write(db_content)

# 3. app.py
with open('backend/app.py', 'r') as f:
    app_content = f.read()

# Add imports to app.py
app_content = app_content.replace("from database import init_db", "from database import init_db, obter_projeto_por_codigo, obter_resumo_hidraulico", 1)

new_routes = """
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

# Insert routes BEFORE the final if __name__ == '__main__' block
app_content = app_content.replace("if __name__ == '__main__':", new_routes + "if __name__ == '__main__':")

with open('backend/app.py', 'w') as f:
    f.write(app_content)
