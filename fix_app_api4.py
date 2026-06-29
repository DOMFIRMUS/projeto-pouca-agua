with open("backend/app.py", "r") as f:
    content = f.read()

content = content.replace(
"""            "tempo_irrigacao_calculado_minutos": max(tempo_estimado_minutos, 0.0),
            "fracao_lixiviacao": fl,
            "fracao_lixiviacao": fl,
            "irrigacao_total_necessaria_mm": itn,
            "tempo_irrigacao_calculado_minutos": tempo_irrigacao_calculado_minutos,
            "fracao_lixiviacao": fl,
            "irrigacao_total_necessaria_mm": itn,""",
"""            "tempo_irrigacao_calculado_minutos": max(tempo_estimado_minutos, 0.0),
            "fracao_lixiviacao": fl,
            "irrigacao_total_necessaria_mm": itn,"""
)

content = content.replace(
"""            "fracao_lixiviacao": fl,
            "fracao_lixiviacao": fl,
            "fracao_lixiviacao": fl,
            "tempo_irrigacao_calculado_minutos": max(tempo_estimado_minutos, 0.0),
            "fracao_lixiviacao": fl,
            "irrigacao_total_necessaria_mm": itn,
            "delta_kPa": calc["delta_kPa"],""",
"""            "tempo_irrigacao_calculado_minutos": max(tempo_estimado_minutos, 0.0),
            "fracao_lixiviacao": fl,
            "irrigacao_total_necessaria_mm": itn,
            "delta_kPa": calc["delta_kPa"],"""
)

with open("backend/app.py", "w") as f:
    f.write(content)
