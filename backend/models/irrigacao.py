# backend/models/irrigacao.py
import math

class CalculadorIrrigacao:
    def __init__(self):
        # Parâmetros agronómicos padrão (Ex: Tomate / Cana-de-açúcar)
        self.umidade_critica = 40.0
        self.umidade_ideal_min = 60.0
        self.umidade_ideal_max = 80.0

    def calcular_eto_blaney_criddle(self, t_media, mes_index):
        """
        Calcula a Evapotranspiração de Referência (ETo em mm/dia) usando o método de Blaney-Criddle-FAO.
        """
        # Percentagem diária de horas anuais de luz solar para a Latitude 20 Sul
        p_dict = {1: 25, 2: 26, 3: 27, 4: 28, 5: 29, 6: 30, 7: 30, 8: 29, 9: 28, 10: 26, 11: 25, 12: 25}

        p = p_dict.get(mes_index, 25)
        eto = (0.457 * t_media + 8.13) * (p / 100)
        return round(eto, 2)

    def calcular_eto_hargreaves(self, t_max, t_min, latitude, mes_index):
        """
        Calcula a Evapotranspiração de Referência (ETo em mm/dia) usando a equação
        de Hargreaves-Samani (1985) presente na tese (Equação 10).
        """
        t_media = (t_max + t_min) / 2

        # Tabela 2 da tese: Radiação Solar no topo da atmosfera (Ra) simplificada para Latitudes comuns no Brasil (ex: ~22°S)
        # Valores aproximados de Ra (MJ m^-2 dia^-1) de Janeiro (0) a Dezembro (11) para Lat 22°S
        tabela_ra_22s = [42.2, 40.1, 36.2, 30.6, 25.6, 23.0, 24.0, 28.1, 33.7, 38.4, 41.4, 42.6]

        # Garante que o mês está no intervalo correto
        if mes_index < 1 or mes_index > 12:
            mes_index = 1
        ra = tabela_ra_22s[mes_index - 1]

        # Equação 10 da Tese: ETo = 0.0023 * Ra * 0.408 * (Tmedia + 17.8) * sqrt(Tmax - Tmin)
        term_temp = t_media + 17.8
        term_diff = math.sqrt(max(t_max - t_min, 0.1))

        eto = 0.0023 * ra * 0.408 * term_temp * term_diff
        return round(eto, 2)

    def calcular_irn_e_cad(self, tomcc, to_pmp, profundidade_z, fator_f, pw_percent):
        """
        Calcula a Capacidade de Água Disponível (CAD) e a Irrigação Real Necessária Máxima (IRN_max)
        baseado no solo e na fração de área umedecida (Equações 36 e 40 da tese).
        """
        # Equação 36: CAD = 1000 * (to_cc - to_pmp) * z
        cad = 1000 * (tomcc - to_pmp) * profundidade_z

        # Fração de área umedecida (decimal)
        fw = pw_percent / 100.0

        # Equação 40: IRN_max = CAD * f * Fw
        irn_max = cad * fator_f * fw
        return round(cad, 2), round(irn_max, 2)

    def calcular_fator_obstrucao(self, tipo_emissor, area_tubo, area_emissor):
        """
        Calcula o Índice de Obstrução (IO) e retorna o fator de perda de carga localizada (KL).
        """
        if area_tubo <= 0:
            return 0.0

        io = area_emissor / area_tubo
        tipo_emissor = tipo_emissor.lower()

        if tipo_emissor == 'online':
            kl = 1.935 * (io ** 0.595)
        elif tipo_emissor == 'pastilha':
            kl = 1.383 * (io ** 0.576)
        elif tipo_emissor == 'bobi':
            kl = 1.230 * (io ** 0.510)
        else:
            kl = 0.0

        return round(kl, 4)

    def calcular_perda_carga_total(self, f_tubo, comprimento, diametro, velocidade, tipo_emissor, area_tubo, area_emissor):
        """
        Calcula a perda de carga total da linha lateral (hf) adicionando o fator de obstrução (KL)
        ao fator de atrito 'f' do tubo.
        """
        if diametro <= 0:
            return 0.0

        kl = self.calcular_fator_obstrucao(tipo_emissor, area_tubo, area_emissor)

        # hf = (f + KL) * (L / D) * (V^2 / 2g)
        hf = (f_tubo + kl) * (comprimento / diametro) * (velocidade ** 2) / (2 * 9.81)

        return round(hf, 4)

    def avaliar_status_solo(self, valor_umidade):
        if valor_umidade < self.umidade_critica:
            return {"status": "Crítico (Seco)", "cor_alerta": "danger", "irrigar": True, "mensagem": "Solo excessivamente seco. Ligue a irrigação."}
        elif self.umidade_critica <= valor_umidade < self.umidade_ideal_min:
            return {"status": "Moderado", "cor_alerta": "warning", "irrigar": True, "mensagem": "A umidade está caindo. Recomenda-se irrigar levemente."}
        elif self.umidade_ideal_min <= valor_umidade <= self.umidade_ideal_max:
            return {"status": "Ideal", "cor_alerta": "success", "irrigar": False, "mensagem": "Solo com umidade perfeita."}
        else:
            return {"status": "Encharcado", "cor_alerta": "info", "irrigar": False, "mensagem": "Solo muito úmido. Evite desperdiçar água."}

    def calcular_area_umedecida(self, q_vazao, volume_z, ko_condutividade, espacamento_plantas_sp, espacamento_fileiras_sr, numero_emissores_np):
        """
        Calcula o Diâmetro Molhado (Dw) e a Porcentagem de Área Umedecida (Pw).
        """
        if ko_condutividade <= 0 or espacamento_plantas_sp <= 0 or espacamento_fileiras_sr <= 0:
            return 0.0, 0.0

        dw = 1.32 * ((volume_z * q_vazao) / ko_condutividade) ** (1/3)
        pw = numero_emissores_np * ((math.pi * (dw ** 2)) / (4 * espacamento_plantas_sp * espacamento_fileiras_sr)) * 100

        return round(dw, 2), round(pw, 2)
