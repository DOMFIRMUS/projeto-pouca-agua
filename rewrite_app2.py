with open('backend/app_cleaned.py', 'r') as f:
    content = f.read()

# Delete everything from the duplicate @app.route('/api/culturas', methods=['GET']) onwards
# up until @app.route('/api/projetos', methods=['POST']) def criar_projeto(). Wait, is it there? Let's check where the next valid route is.
# Actually, the file is full of duplicated git conflict leftovers.
# Let's find def obter_classificacao_perfil(): and delete down to def criar_projeto():

start = content.find("@app.route('/api/classificar_perfil', methods=['POST'])")
end = content.find("@app.route('/api/projetos', methods=['POST'])\ndef criar_projeto():")

if start != -1 and end != -1:
    content = content[:start] + content[end:]

# And delete the second @app.route('/api/culturas', methods=['GET'])
# Wait, let's just do a string replace of the block that has syntax errors.

# Let's just fix it by writing a cleaner regex or direct string manipulation
