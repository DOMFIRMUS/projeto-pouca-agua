with open("backend/app.py", "r") as f:
    content = f.read()

import re

# Remove repeated "fracao_lixiviacao"
content = re.sub(r'(\s*"fracao_lixiviacao": fl,\n)+', r'\n            "fracao_lixiviacao": fl,\n', content)

# Check line 440ish
content = re.sub(r'(\s*"irrigacao_total_necessaria_mm": itn\n)+', r'\n            "irrigacao_total_necessaria_mm": itn,\n', content)
content = re.sub(r'(\s*"irrigacao_total_necessaria_mm": calc\["itn"\]\n)+', r'\n            "irrigacao_total_necessaria_mm": calc["itn"],\n', content)


# Remove multiple empty }
content = re.sub(r'\}\n\s*\}\n\s*\}\n', r'}\n    }\n', content)


with open("backend/app.py", "w") as f:
    f.write(content)
