import os

filepath = 'backend/models/irrigacao.py'
with open(filepath, 'r') as f:
    lines = f.readlines()

for i in range(len(lines)):
    if lines[i].strip() == '"vazao_total_lh": round(vazao_total, 2)':
         lines.insert(i+1, "        }\n")
         break

with open(filepath, 'w') as f:
    f.writelines(lines)
