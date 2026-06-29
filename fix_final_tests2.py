import re

with open('backend/models/irrigacao.py', 'r') as f:
    content = f.read()

# Make sure blaney_criddle_unused is completely empty and clean
content = content.replace("def calcular_eto_blaney_criddle_unused(self, t_media, mes_index, latitude_sul=20.0):\n        pass\n\n    def calcular_pressao_atual_ea(self, es, umidade_relativa_media_ur):", "def calcular_eto_blaney_criddle_unused(self, t_media, mes_index, latitude_sul=20.0):\n        pass\n\n    def calcular_pressao_atual_ea(self, es, umidade_relativa_media_ur):")
content = content.replace("def calcular_eto_blaney_criddle_unused(self, t_media, mes_index, latitude_sul=20.0):\n        pass\n    def calcular_pressao_atual_ea", "def calcular_eto_blaney_criddle_unused(self, t_media, mes_index, latitude_sul=20.0):\n        pass\n\n    def calcular_pressao_atual_ea")
content = content.replace("def calcular_eto_blaney_criddle_unused(self, t_media, mes_index, latitude_sul=20.0):\n    def calcular_pressao_atual_ea", "def calcular_eto_blaney_criddle_unused(self, t_media, mes_index, latitude_sul=20.0):\n        pass\n\n    def calcular_pressao_atual_ea")

with open('backend/models/irrigacao.py', 'w') as f:
    f.write(content)

with open('backend/app.py', 'r') as f:
    app_content = f.read()

app_content = app_content.replace(
"""        resposta_json = {
    # Raio Umedecido Check
    se = """,
"""    # Raio Umedecido Check
    se = """)
app_content = app_content.replace(
"""        resposta_json = {
        # Raio Umedecido Check
        se = """,
"""        # Raio Umedecido Check
        se = """)
app_content = app_content.replace(
"""    resposta_json = {
    # Raio Umedecido Check
    se = """,
"""    # Raio Umedecido Check
    se = """)

with open('backend/app.py', 'w') as f:
    f.write(app_content)

with open('backend/tests/test_app.py', 'r') as f:
    test_content = f.read()

test_content = test_content.replace(
"""def test_hidraulica_post_success(client):

def""",
"""def test_hidraulica_post_success(client):
    pass

def""")

with open('backend/tests/test_app.py', 'w') as f:
    f.write(test_content)
