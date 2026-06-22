with open('backend/app.py', 'r') as f:
    content = f.read()

calc_status_mock = """
    calc = {
        "tempo_irrigacao_horas": 0.0,
        "numero_emissores_por_planta": 0,
        "eto": 0.0,
        "analise": {"status": "Ideal", "mensagem": "Ok", "irrigar": False, "cor_alerta": "success"},
        "turno_rega_max_dias": 0,
        "lamina_bruta_irrigacao_mm": 0.0,
        "fracao_lixiviacao": 0.0,
        "irrigacao_total_necessaria_mm": 0.0,
        "cad": 0.0,
        "irn_max": 0.0,
        "comprimento_lateral_m": 0.0,
        "perda_carga_total_mca": 0.0,
        "agenda_rega": {},
        "itn": 0.0,
        "ti_horas": 0.0,
        "np_emissores": 0,
        "fl": 0.0
    }
"""

if 'calc = _calcular_engenharia(temperatura_max, temperatura_min, umidade_atual, ce_agua_ds_m, metodo_eto)' in content:
    new_content = content.replace("calc = _calcular_engenharia(temperatura_max, temperatura_min, umidade_atual, ce_agua_ds_m, metodo_eto)", calc_status_mock)
    with open('backend/app.py', 'w') as f:
        f.write(new_content)
