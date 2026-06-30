import os

filepath = 'backend/database.py'
with open(filepath, 'r') as f:
    lines = f.readlines()

for i in range(len(lines)):
    if lines[i].strip() == "cursor.execute('''" and lines[i+1].strip() == "CREATE TABLE IF NOT EXISTS bancos (":
         lines[i] = "    cursor.execute('''\n"
         lines.insert(i+1, "        CREATE TABLE IF NOT EXISTS bancos (\n")
         lines.insert(i+2, "            id INTEGER PRIMARY KEY AUTOINCREMENT,\n")
         lines.insert(i+3, "            nome TEXT NOT NULL,\n")
         lines.insert(i+4, "            taxa_mensal REAL NOT NULL\n")
         lines.insert(i+5, "        )\n")
         lines.insert(i+6, "    ''')\n")
         break

with open(filepath, 'w') as f:
    f.writelines(lines)
