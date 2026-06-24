import re

with open('backend/models/irrigacao.py', 'r') as f:
    content = f.read()

# Make sure it's not already there
if 'calcular_diametro_dw_schwartzman' not in content:
    # Let's insert the missing methods at the end of CalculadorIrrigacao class
    new_methods = """
    def calcular_diametro_dw_schwartzman(self, z_profundidade, q_vazao, ko_condutividade):
        \"\"\"
        Equação 25 (Diâmetro Máximo Molhado - Dw)
        Dw = 1.32 * z^0.35 * (q / ko)^0.33
        \"\"\"
        if ko_condutividade <= 0:
            return 0.0

        if z_profundidade < 0 or q_vazao < 0:
            return 0.0

        dw = 1.32 * (z_profundidade ** 0.35) * ((q_vazao / ko_condutividade) ** 0.33)
        return round(dw, 4)

    def calcular_raio_rw(self, alpha, q_vazao, ko_condutividade):
        \"\"\"
        Equação 26 (Raio Molhado Saturado - Rw)
        Rw = sqrt(4 / (alpha^2 * pi^2) + q / (pi * ko)) - 2 / (alpha * pi)
        \"\"\"
        import math
        if alpha <= 0 or ko_condutividade <= 0:
            return 0.0
        if q_vazao < 0:
            return 0.0

        termo1 = 4.0 / ((alpha ** 2) * (math.pi ** 2))
        termo2 = q_vazao / (math.pi * ko_condutividade)
        termo3 = 2.0 / (alpha * math.pi)

        valor_interno = termo1 + termo2
        if valor_interno < 0:
            return 0.0

        rw = math.sqrt(valor_interno) - termo3

        if rw < 0:
            return 0.0

        return round(rw, 4)

    def calcular_area_umedecida_fluxograma(self, tipo_disposicao, configuracao_linha, params):
        \"\"\"
        Método orquestrador baseado na Figura 6 da tese.
        \"\"\"
        import math
        z = params.get('profundidade_z', 0.0)
        q = params.get('q_vazao', 0.0)
        ko = params.get('condutividade_ko', 0.0)
        alpha = params.get('parametro_alpha', 0.0)
        sp = params.get('espacamento_plantas_sp', 0.0)
        sr = params.get('espacamento_fileiras_sr', 0.0)
        np_emissores = params.get('np_emissores', 1)

        dw = self.calcular_diametro_dw_schwartzman(z, q, ko)
        rw = self.calcular_raio_rw(alpha, q, ko)

        if sp <= 0 or sr <= 0:
            return {
                "dw": dw, "rw": rw, "aw": 0.0, "ap": 0.0, "pw": 0.0,
                "erro": "Espaçamentos devem ser maiores que zero."
            }

        ap = sp * sr
        aw = 0.0

        if tipo_disposicao == 'faixa_continua':
            largura_faixa = dw
            if configuracao_linha == 'LLD':
                largura_faixa *= 2
            aw = largura_faixa * sp

        elif tipo_disposicao == 'por_arvore':
            area_bulbo_individual = math.pi * (rw ** 2)
            aw = np_emissores * area_bulbo_individual
            if configuracao_linha == 'LLD':
                aw *= 2

        pw = (aw / ap) * 100

        return {
            "dw": round(dw, 2),
            "rw": round(rw, 2),
            "aw": round(aw, 2),
            "ap": round(ap, 2),
            "pw": round(pw, 2)
        }
"""
    with open('backend/models/irrigacao.py', 'a') as f:
        f.write(new_methods)
