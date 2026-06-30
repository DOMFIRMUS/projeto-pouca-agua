import os

filepath = 'backend/database.py'
with open(filepath, 'r') as f:
    lines = f.readlines()

for i in range(len(lines)):
    if lines[i].strip() == "CREATE TABLE IF NOT EXISTS historico_leitura (":
         lines[i] = "        CREATE TABLE IF NOT EXISTS historico_leitura (\n"
         lines.insert(i+1, "            id INTEGER PRIMARY KEY AUTOINCREMENT\n")
         lines.insert(i+2, "        )\n")
         lines.insert(i+3, "    \"\"\")\n")
         break

with open(filepath, 'w') as f:
    f.writelines(lines)
