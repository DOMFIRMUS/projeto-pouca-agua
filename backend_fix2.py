with open("backend/database.py", "r") as f:
    text = f.read()

text = text.replace("    '''\n    , (codigo_projeto,))", "    ''', (codigo_projeto,))")

# Check if there's duplicate `obter_resumo_hidraulico`
import re
text = re.sub(r"def obter_projeto_por_codigo\(codigo_projeto\):\n    conn = get_db_connection\(\)\n    cursor = conn.cursor\(\)\n    cursor.execute\('SELECT \* FROM projetos_metadados WHERE codigo_projeto = \?', \(codigo_projeto,\)\)\n    row = cursor.fetchone\(\)\n    conn.close\(\)\n    if row:\n        return dict\(row\)\n    return None\n\ndef obter_resumo_hidraulico\(codigo_projeto\):\n    conn = get_db_connection\(\)\n    cursor = conn.cursor\(\)\n    cursor.execute\('''\n        SELECT \* FROM historico_leitura\n        WHERE codigo_projeto = \?\n        ORDER BY id DESC LIMIT 1\n    ''', \(codigo_projeto,\)\)\n    row = cursor.fetchone\(\)\n    conn.close\(\)\n    if row:\n        return dict\(row\)\n    return None", "", text)

with open("backend/database.py", "w") as f:
    f.write(text)

with open("backend/tests/test_app.py", "r") as f:
    text = f.read()

text = text.replace("    response = client.post('/api/hidraulica/perfil', json={\n    response = client.post('/api/hidraulica_perfil', json={\n    response = client.post('/api/classificar_hidraulica', json={\ndef test_hidraulica_post_success_advanced(client):\n    response = client.post('/api/hidraulica', json={\ndef test_hidraulica_post_success(client):\n    response = client.post('/api/classificar_perfil', json={", "def test_hidraulica_post_success_advanced(client):\n    response = client.post('/api/hidraulica', json={")

with open("backend/tests/test_app.py", "w") as f:
    f.write(text)
