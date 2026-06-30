import os

filepath = 'backend/models/irrigacao.py'
with open(filepath, 'r') as f:
    lines = f.readlines()

to_remove = []
for i in range(len(lines)):
    if lines[i].strip() == "def calcular_eto_blaney_criddle(self, t_media, mes_index, latitude_sul=-22.0):":
        to_remove.append(i)
        to_remove.append(i+1)
        to_remove.append(i+2)
        to_remove.append(i+3)
        break

for i in sorted(list(set(to_remove)), reverse=True):
    del lines[i]

with open(filepath, 'w') as f:
    f.writelines(lines)
