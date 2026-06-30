import os

filepath = 'backend/tests/test_area_umedecida.py'
with open(filepath, 'r') as f:
    lines = f.readlines()

for i in range(len(lines)):
    if lines[i].strip() == "from app import app":
         lines[i] = "from backend.app import app\n"
         break

with open(filepath, 'w') as f:
    f.writelines(lines)
