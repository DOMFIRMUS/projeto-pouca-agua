import os

filepath = 'backend/tests/test_area_umedecida.py'
with open(filepath, 'r') as f:
    lines = f.readlines()

for i in range(len(lines)):
    if lines[i].strip() == "from models.irrigacao import CalculadorIrrigacao":
         lines[i] = "from backend.models.irrigacao import CalculadorIrrigacao\n"
         break

with open(filepath, 'w') as f:
    f.writelines(lines)

filepath = 'backend/tests/test_derivacao_p74.py'
with open(filepath, 'r') as f:
    lines = f.readlines()

for i in range(len(lines)):
    if "insert_projeto_metadados" in lines[i]:
         lines[i] = lines[i].replace("insert_projeto_metadados", "insert_projeto")
         break

with open(filepath, 'w') as f:
    f.writelines(lines)

filepath = 'backend/tests/test_app.py'
with open(filepath, 'r') as f:
    lines = f.readlines()

to_remove = []
for i in range(len(lines)):
    if lines[i].strip() == 'response = client.post("/api/hidraulica", json={':
        lines.insert(i+1, "    })\n")
        break

with open(filepath, 'w') as f:
    f.writelines(lines)
