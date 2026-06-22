with open('backend/database.py', 'r') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if line.strip().startswith('INSERT INTO projetos_metadados (codigo_projeto, nome_projeto, nome_propriedade') and 'identificacao' in line and i == 125: # It's lines[125]
        skip = True

    if skip and 'conn.close()' in line and 'finally:' in lines[i-1]:
        skip = False
        continue

    if not skip:
        new_lines.append(line)

with open('backend/database.py', 'w') as f:
    f.writelines(new_lines)
