with open("backend/models/irrigacao.py", "r") as f:
    content = f.read()

content = content.replace(
"""    def calcular_eto_blaney_criddle_unused(self, t_media, mes_index, latitude_sul=20.0):
    def calcular_eto_blaney_criddle(self, t_media, mes_index):""",
"""    def calcular_eto_blaney_criddle_unused(self, t_media, mes_index, latitude_sul=20.0):
        pass

    def calcular_eto_blaney_criddle(self, t_media, mes_index):""")

with open("backend/models/irrigacao.py", "w") as f:
    f.write(content)
