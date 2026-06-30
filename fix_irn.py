import os

filepath = 'backend/models/irrigacao.py'
with open(filepath, 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.strip() == "def calcular_cad_solo(self, theta_cc, theta_pmp, z):":
        lines[i+1] = "        if float(theta_cc) <= float(theta_pmp) or float(z) <= 0: return 0.0\n"
        lines[i+2] = "        return round(1000.0 * (float(theta_cc) - float(theta_pmp)) * float(z), 2)\n"
        break

with open(filepath, 'w') as f:
    f.writelines(lines)
