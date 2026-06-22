with open('backend/app.py', 'r') as f:
    lines = f.readlines()

new_lines = []
skip = False

for i, line in enumerate(lines):
    if line.strip() == '"metricas_tese": {':
        skip = True
        new_lines.append(line)
        new_lines.append('            "evapotranspiracao_referencia_mm_dia": calc["eto"],\n')
        new_lines.append('            "capacidade_agua_disponivel_solo_mm": calc["cad"],\n')
        new_lines.append('            "irrigacao_real_necessaria_max_mm": calc["irn_max"],\n')
        new_lines.append('            "tempo_irrigacao_horas": calc["ti_horas"],\n')
        new_lines.append('            "numero_emissores_por_planta": calc["np_emissores"],\n')
        new_lines.append('            "tempo_irrigacao_calculado_minutos": calc["tempo_irrigacao_calculado_minutos"],\n')
        new_lines.append('            "fracao_lixiviacao": calc["fl"],\n')
        new_lines.append('            "irrigacao_total_necessaria_mm": calc["itn"]\n')
        new_lines.append('        }\n')
        continue

    if skip:
        if line.strip() == '}':
            skip = False
        continue

    if not skip:
        new_lines.append(line)

with open('backend/app_fixed.py', 'w') as f:
    f.writelines(new_lines)
