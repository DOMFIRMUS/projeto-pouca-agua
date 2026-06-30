import os

filepath = 'backend/database.py'
with open(filepath, 'r') as f:
    lines = f.readlines()

for i in range(len(lines)):
    if lines[i].strip() == "cursor.execute('''" and lines[i+1].strip() == "CREATE TABLE IF NOT EXISTS bancos (":
         lines[i] = "    cursor.execute('''\n"
         lines[i+1] = "        CREATE TABLE IF NOT EXISTS bancos (\n"
         break

with open(filepath, 'w') as f:
    f.writelines(lines)
