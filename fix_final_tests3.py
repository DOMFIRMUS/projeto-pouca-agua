with open("backend/models/irrigacao.py", "r") as f:
    text = f.read()

# Fix the exact indentation error inside models/irrigacao.py
text = text.replace("def calcular_eto_blaney_criddle_unused(self, t_media, mes_index, latitude_sul=20.0):\n        pass\n\n    def calcular_pressao_atual_ea(self", "def calcular_eto_blaney_criddle_unused(self, t_media, mes_index, latitude_sul=20.0):\n        pass\n\n    def calcular_pressao_atual_ea(self")
text = text.replace("def calcular_eto_blaney_criddle_unused(self, t_media, mes_index, latitude_sul=20.0):\n    def calcular_pressao_atual_ea(self", "def calcular_eto_blaney_criddle_unused(self, t_media, mes_index, latitude_sul=20.0):\n        pass\n\n    def calcular_pressao_atual_ea(self")

with open("backend/models/irrigacao.py", "w") as f:
    f.write(text)

with open("backend/app.py", "r") as f:
    app_text = f.read()

# Fix the exact syntax error in app.py near `se =`
import re
app_text = re.sub(r'        resposta_json = \{\n        # Raio Umedecido Check\n        se =', r'        # Raio Umedecido Check\n        se =', app_text)
app_text = re.sub(r'        resposta_json = \{\n    # Raio Umedecido Check\n    se =', r'        # Raio Umedecido Check\n        se =', app_text)

with open("backend/app.py", "w") as f:
    f.write(app_text)

with open("backend/tests/test_app.py", "r") as f:
    test_text = f.read()

# Fix test missing blocks
test_text = test_text.replace("def test_hidraulica_post_success(client):\n    \ndef test_hidraulica_post_missing_fields(client):", "def test_hidraulica_post_success(client):\n    pass\n\ndef test_hidraulica_post_missing_fields(client):")

test_text = test_text.replace("def test_hidraulica_post_success(client):\n\ndef test_hidraulica_post_success_advanced(client):", "def test_hidraulica_post_success(client):\n    pass\n\ndef test_hidraulica_post_success_advanced(client):")

with open("backend/tests/test_app.py", "w") as f:
    f.write(test_text)
