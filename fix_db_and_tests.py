import os

filepath = 'backend/app.py'
with open(filepath, 'r') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if "def linha_lateral_trecho_endpoint(codigo_projeto):" in line:
        new_lines.append(line)
        new_lines.append("    return jsonify({'status': 'ok', 'codigo_projeto': codigo_projeto}), 200\n")
        continue
    if "return jsonify({'status': 'ok'}), 200" in line:
        continue
    new_lines.append(line)

with open(filepath, 'w') as f:
    f.writelines(new_lines)
