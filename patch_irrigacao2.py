with open("backend/models/irrigacao.py", "r") as f:
    content = f.read()

content = content.replace(
    "    def calcular_cad(self, theta_cc, theta_pmp, z):\n        if float(theta_cc) < float(theta_pmp) or float(z) <= 0:\n\n    def calcular_fator_atrito_p66(self, reynolds_r):",
    "    def calcular_cad(self, theta_cc, theta_pmp, z):\n        if float(theta_cc) < float(theta_pmp) or float(z) <= 0:\n            return 0.0\n        return (float(theta_cc) - float(theta_pmp)) * float(z) * 1000.0\n\n    def calcular_fator_atrito_p66(self, reynolds_r):"
)

with open("backend/models/irrigacao.py", "w") as f:
    f.write(content)
