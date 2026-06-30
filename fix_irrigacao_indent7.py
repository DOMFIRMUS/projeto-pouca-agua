import os

filepath = 'backend/models/irrigacao.py'
with open(filepath, 'r') as f:
    lines = f.readlines()

for i in range(len(lines)):
    if lines[i].strip() == '"irn": round(irn, 2)':
        lines.insert(i+1, "        }\n")
        break

with open(filepath, 'w') as f:
    f.writelines(lines)
