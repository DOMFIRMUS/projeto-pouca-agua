import os

filepath = 'backend/database.py'
with open(filepath, 'r') as f:
    lines = f.readlines()

to_remove = []
for i in range(len(lines)):
    if lines[i].strip() == 'data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP' and lines[i+1].strip() == ')' and lines[i+2].strip() == '""")':
         to_remove.append(i+3)
         to_remove.append(i+4)
         to_remove.append(i+5)
         to_remove.append(i+6)
         to_remove.append(i+7)
         to_remove.append(i+8)
         to_remove.append(i+9)
         to_remove.append(i+10)
         break

for i in sorted(list(set(to_remove)), reverse=True):
    del lines[i]

with open(filepath, 'w') as f:
    f.writelines(lines)
