with open("backend/app.py", "r") as f:
    content = f.read()

content = content.replace(
"""            "pressao_atm_kPa": calc["pressao_atm_kPa"],
            "deficit_pressao_vapor_kpa": calc.get("deficit_pressao_vapor_kpa", 0.0)
        }

    if alerta_salinidade:""",
"""            "pressao_atm_kPa": calc["pressao_atm_kPa"],
            "deficit_pressao_vapor_kpa": calc.get("deficit_pressao_vapor_kpa", 0.0)
        }
    }
    if alerta_salinidade:"""
)

with open("backend/app.py", "w") as f:
    f.write(content)
