import os

filepath = 'backend/database.py'
with open(filepath, 'r') as f:
    lines = f.readlines()

for i in range(len(lines)):
    if lines[i].strip() == '""", (ps, tipo_calculo, ss_largura_faixa, dco_diametro_copa, codigo_projeto))':
         del lines[i]
         break

with open(filepath, 'w') as f:
    f.writelines(lines)
