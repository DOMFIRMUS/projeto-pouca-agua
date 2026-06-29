with open("backend/app.py", "r") as f:
    content = f.read()

content = content.replace(
    "def _calcular_engenharia(temperatura_max, temperatura_min, umidade_atual, ce_agua_ds_m, metodo_eto='hargreaves'):\n\n\n@app.route('/api/status', methods=['GET'])",
    "def _calcular_engenharia(temperatura_max, temperatura_min, umidade_atual, ce_agua_ds_m, metodo_eto='hargreaves'):\n    pass\n\n@app.route('/api/status', methods=['GET'])"
)

with open("backend/app.py", "w") as f:
    f.write(content)
