import os

filepath = 'backend/models/irrigacao.py'
with open(filepath, 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.strip() == "if float(theta_cc) < float(theta_pmp) or float(z) <= 0:":
        lines.insert(i + 1, "            return 0.0\n")
        break

with open(filepath, 'w') as f:
    f.writelines(lines)

print("Fixed backend/models/irrigacao.py")
