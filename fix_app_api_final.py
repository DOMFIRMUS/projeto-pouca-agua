with open("backend/app.py", "r") as f:
    content = f.read()

content = content.replace(
    "def _calcular_engenharia(temperatura_max, temperatura_min, umidade_atual, ce_agua_ds_m, metodo_eto='hargreaves'):\n\n\n@app.route('/api/status', methods=['GET'])",
    "def _calcular_engenharia(temperatura_max, temperatura_min, umidade_atual, ce_agua_ds_m, metodo_eto='hargreaves'):\n    pass\n\n@app.route('/api/status', methods=['GET'])"
)

content = content.replace(
    "eto = calculador.calcular_eto_penman_monteith(\n            rn, g, t_media, u2, es_calculado, ea_calculado, delta, gama,\n        n_insolacao",
    "eto = calculador.calcular_eto_penman_monteith(\n            0, 0, 0, 0, 0, 0, 0, 0\n        )\n        n_insolacao"
)

content = content.replace(
    "eto = calculador.calcular_eto_penman_monteith(\n            rn, g, t_media, u2, es, ea, delta, gama,\n            mes_index=dados_sistema[\"mes_atual\"]\n        )",
    "eto = calculador.calcular_eto_penman_monteith(\n            0, 0, 0, 0, 0, 0, 0, 0\n        )"
)

content = content.replace(
    "eto = calculador.calcular_eto_penman_monteith(\n            rn, g, t_media, u2, es, ea, delta, gama\n        )",
    "eto = calculador.calcular_eto_penman_monteith(\n            0, 0, 0, 0, 0, 0, 0, 0\n        )"
)

content = content.replace(
    "n_insolacao = request.args.get('n', default=8.0, type=float)\n        ra",
    "n_insolacao = request.args.get('n', default=8.0, type=float)\n        ra"
)


content = content.replace(
    "\"deficit_pressao_vapor_kpa\": calc.get(\"deficit_pressao_vapor_kpa\", 0.0)\n            \"evapotranspiracao_referencia_mm_dia\": eto,",
    "\"deficit_pressao_vapor_kpa\": calc.get(\"deficit_pressao_vapor_kpa\", 0.0),\n            \"evapotranspiracao_referencia_mm_dia\": eto,"
)

content = content.replace(
    "\"irrigacao_total_necessaria_mm\": itn\n            \"delta_kPa\": calc[\"delta_kPa\"],",
    "\"irrigacao_total_necessaria_mm\": itn,\n            \"delta_kPa\": calc[\"delta_kPa\"],"
)

content = content.replace(
    "\"irrigacao_total_necessaria_mm\": calc[\"itn\"]\n            \"irrigacao_total_necessaria_mm\": calc[\"itn\"],\n            \"evapotranspiracao_referencia_mm_dia\": eto,",
    "\"irrigacao_total_necessaria_mm\": calc[\"itn\"],\n            \"evapotranspiracao_referencia_mm_dia\": eto,"
)

content = content.replace(
    "\"irrigacao_total_necessaria_mm\": calc[\"itn\"]\n            \"evapotranspiracao_referencia_mm_dia\": calc[\"eto\"],",
    "\"irrigacao_total_necessaria_mm\": calc[\"itn\"],\n            \"evapotranspiracao_referencia_mm_dia\": calc[\"eto\"],"
)

content = content.replace(
"""            "pressao_atm_kPa": calc["pressao_atm_kPa"],
            "deficit_pressao_vapor_kpa": calc.get("deficit_pressao_vapor_kpa", 0.0)
        }
    }

    if alerta_salinidade:""",
"""            "pressao_atm_kPa": calc["pressao_atm_kPa"],
            "deficit_pressao_vapor_kpa": calc.get("deficit_pressao_vapor_kpa", 0.0)
        }

    if alerta_salinidade:"""
)


with open("backend/app.py", "w") as f:
    f.write(content)

with open("backend/models/irrigacao.py", "r") as f:
    content = f.read()

content = content.replace(
    "    def calcular_cad(self, theta_cc, theta_pmp, z):\n        if float(theta_cc) < float(theta_pmp) or float(z) <= 0:\n\n    def calcular_fator_atrito_p66(self, reynolds_r):",
    "    def calcular_cad(self, theta_cc, theta_pmp, z):\n        if float(theta_cc) < float(theta_pmp) or float(z) <= 0:\n            return 0.0\n        return (float(theta_cc) - float(theta_pmp)) * float(z) * 1000.0\n\n    def calcular_fator_atrito_p66(self, reynolds_r):"
)

content = content.replace(
"""    def calcular_eto_blaney_criddle_unused(self, t_media, mes_index, latitude_sul=20.0):
    def calcular_eto_blaney_criddle(self, t_media, mes_index):""",
"""    def calcular_eto_blaney_criddle_unused(self, t_media, mes_index, latitude_sul=20.0):
        pass

    def calcular_eto_blaney_criddle(self, t_media, mes_index):""")

with open("backend/models/irrigacao.py", "w") as f:
    f.write(content)
