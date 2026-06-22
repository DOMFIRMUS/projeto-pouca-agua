with open('backend/app.py', 'r') as f:
    lines = f.readlines()

import re
# The lines inside metricas_tese are completely messed up and repeated. Let's fix them manually.

# Find the start of the response_json dictionary
start_idx = -1
for i, line in enumerate(lines):
    if line.strip() == '"metricas_tese": {':
        start_idx = i
        break

end_idx = -1
if start_idx != -1:
    for i in range(start_idx, len(lines)):
        if line.strip() == '}':
            end_idx = i
            break

# A better way is to replace the whole broken JSON chunk
import os
os.system('git restore backend/app.py')
