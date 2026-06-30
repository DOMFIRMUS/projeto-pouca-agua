import os

filepath = 'backend/database.py'
with open(filepath, 'r') as f:
    lines = f.readlines()

to_remove = []
for i in range(len(lines)):
    if lines[i].strip() == "cursor.execute('''" and lines[i+1].strip() == "CREATE TABLE IF NOT EXISTS projetos_metadados (":
         lines[i] = "    cursor.execute('''\n"
         break

with open(filepath, 'w') as f:
    f.writelines(lines)
