import os

filepath = 'backend/tests/test_derivacao_p74.py'
with open(filepath, 'r') as f:
    lines = f.readlines()

for i in range(len(lines)):
    if "from backend.database import" in lines[i] and "insert_projeto_metadados" in lines[i]:
        lines[i] = lines[i].replace("insert_projeto_metadados", "insert_projeto")
        break

with open(filepath, 'w') as f:
    f.writelines(lines)
