import re

with open('backend/models/irrigacao.py', 'r') as f:
    content = f.read()

# Make sure calcular_eto_blaney_criddle_unused is empty block safe
content = content.replace("def calcular_eto_blaney_criddle_unused(self, t_media, mes_index, latitude_sul=20.0):\n    def", "def calcular_eto_blaney_criddle_unused(self, t_media, mes_index, latitude_sul=20.0):\n        pass\n    def")

with open('backend/models/irrigacao.py', 'w') as f:
    f.write(content)

with open('backend/app.py', 'r') as f:
    app_content = f.read()

app_content = app_content.replace(
"""        resposta_json = {
        # Raio Umedecido Check
        se = request.args.get('se', request.args.get('espacamento_m', dados_sistema.get("espacamento_plantas_sp", 0.5)), type=float)""",
"""        # Raio Umedecido Check
        se = request.args.get('se', request.args.get('espacamento_m', dados_sistema.get("espacamento_plantas_sp", 0.5)), type=float)
        resposta_json = {""")

with open('backend/app.py', 'w') as f:
    f.write(app_content)

with open('backend/tests/test_app.py', 'r') as f:
    test_content = f.read()

test_content = test_content.replace(
"""def test_hidraulica_post_success(client):

def test_hidraulica_post_missing_fields""",
"""def test_hidraulica_post_success(client):
    pass

def test_hidraulica_post_missing_fields""")

test_content = test_content.replace(
"""def test_hidraulica_post_success(client):

def test_hidraulica_post_success_advanced""",
"""def test_hidraulica_post_success(client):
    pass

def test_hidraulica_post_success_advanced""")

with open('backend/tests/test_app.py', 'w') as f:
    f.write(test_content)
