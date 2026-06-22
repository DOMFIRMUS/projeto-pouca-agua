import re

with open("backend/app.py", "r") as f:
    content = f.read()

# Fix the duplicate tempo_irrigacao_calculado_minutos key in metricas_tese
content = re.sub(r'"tempo_irrigacao_calculado_minutos": max\(tempo_estimado_minutos, 0\.0\),\s*"tempo_irrigacao_horas": ti_horas,\s*"numero_emissores_por_planta": np_emissores,\s*"tempo_irrigacao_calculado_minutos": tempo_irrigacao_calculado_minutos,\s*"fracao_lixiviacao": fl,\s*"irrigacao_total_necessaria_mm": itn,\s*"tempo_irrigacao_calculado_minutos": max\(tempo_estimado_minutos, 0\.0\)',
r'"tempo_irrigacao_calculado_minutos": tempo_irrigacao_calculado_minutos,\n            "tempo_irrigacao_horas": ti_horas,\n            "numero_emissores_por_planta": np_emissores,\n            "fracao_lixiviacao": fl,\n            "irrigacao_total_necessaria_mm": itn', content)

with open("backend/app.py", "w") as f:
    f.write(content)
