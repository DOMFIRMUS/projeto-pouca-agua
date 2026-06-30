import os

filepath = 'backend/tests/test_area_umedecida.py'
with open(filepath, 'r') as f:
    lines = f.readlines()

for i in range(len(lines)):
    if lines[i].strip() == "from database import init_db, get_db_connection":
         lines[i] = "from backend.database import init_db, get_db_connection\n"
         break

with open(filepath, 'w') as f:
    f.writelines(lines)
