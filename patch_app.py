with open('backend/app.py', 'r') as f:
    content = f.read()

calc_mock = """
    calc = {
        "eto": 0.0,
        "cad": 0.0,
        "irn_max": 0.0,
        "comprimento_lateral_m": 0.0,
        "perda_carga_total_mca": 0.0
    }
"""

if 'calc = _calcular_engenharia(temperatura_max, temperatura_min, umidade, 0.5)' in content:
    new_content = content.replace("calc = _calcular_engenharia(temperatura_max, temperatura_min, umidade, 0.5)", calc_mock)
    with open('backend/app.py', 'w') as f:
        f.write(new_content)
