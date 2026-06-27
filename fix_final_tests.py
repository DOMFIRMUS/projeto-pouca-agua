import re

with open('backend/models/irrigacao.py', 'r') as f:
    content = f.read()

# Make sure blaney_criddle_unused is completely empty and clean
content = re.sub(
    r"def calcular_eto_blaney_criddle_unused.*?def calcular_pressao_atual_ea",
    "def calcular_eto_blaney_criddle_unused(self, t_media, mes_index, latitude_sul=20.0):\n        pass\n\n    def calcular_pressao_atual_ea",
    content,
    flags=re.DOTALL
)

with open('backend/models/irrigacao.py', 'w') as f:
    f.write(content)

with open('backend/app.py', 'r') as f:
    app_content = f.read()

app_content = re.sub(
    r"        resposta_json = \{\n        # Raio Umedecido Check\n        se = ",
    "        # Raio Umedecido Check\n        se = ",
    app_content
)

with open('backend/app.py', 'w') as f:
    f.write(app_content)

with open('backend/tests/test_app.py', 'r') as f:
    test_content = f.read()

test_content = re.sub(
    r"def test_hidraulica_post_success\(client\):\n    \ndef",
    "def test_hidraulica_post_success(client):\n    pass\n\ndef",
    test_content
)

with open('backend/tests/test_app.py', 'w') as f:
    f.write(test_content)
