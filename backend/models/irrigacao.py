# backend/models/irrigacao.py
import math

class CalculadorIrrigacao:
    def __init__(self):
        # Parâmetros agronómicos padrão (Ex: Tomate / Cana-de-açúcar)
        self.umidade_critica = 40.0
        self.umidade_ideal_min = 60.0
        self.umidade_ideal_max = 80.0

        # Tabela 2 da tese: Radiação Solar no topo da atmosfera (Ra) em MJ/m2/dia para Latitudes Sul
        self.tabela_ra = {
            0: [36.2, 37.4, 37.9, 36.8, 34.8, 33.4, 33.9, 35.6, 37.2, 37.4, 36.3, 35.6],
            2: [36.9, 37.9, 38.0, 36.4, 34.1, 32.6, 33.1, 35.2, 37.1, 37.7, 37.0, 36.4],
            4: [37.6, 38.3, 38.0, 36.0, 33.4, 31.8, 32.3, 34.6, 37.0, 38.0, 37.6, 37.2],
            6: [38.3, 38.7, 38.0, 35.6, 32.7, 30.9, 31.5, 34.0, 36.8, 38.2, 38.2, 38.0],
            8: [38.9, 39.0, 37.9, 35.1, 31.9, 30.0, 30.7, 33.4, 36.6, 38.4, 38.8, 38.7],
            10: [39.5, 39.3, 37.8, 34.6, 31.1, 29.1, 29.8, 32.8, 36.3, 38.5, 39.3, 39.4],
            12: [40.1, 39.6, 37.7, 34.0, 30.2, 28.1, 28.9, 32.1, 36.0, 38.6, 39.8, 40.0],
            14: [40.6, 39.8, 37.5, 33.4, 29.4, 27.1, 28.0, 31.4, 35.6, 38.6, 40.2, 40.6],
            16: [41.0, 39.9, 37.2, 32.7, 28.4, 26.1, 27.0, 30.6, 35.2, 38.6, 40.6, 41.1],
            18: [41.5, 40.1, 36.9, 32.0, 27.5, 25.1, 26.0, 29.8, 34.7, 38.6, 40.9, 41.7],
            20: [41.9, 40.1, 36.6, 31.3, 26.6, 24.1, 25.0, 29.0, 34.2, 38.5, 41.2, 42.1],
            22: [42.2, 40.1, 36.2, 30.6, 25.6, 23.0, 24.0, 28.1, 33.7, 38.4, 41.4, 42.6],
            24: [42.5, 40.1, 35.8, 29.8, 24.6, 21.9, 22.9, 27.2, 33.1, 38.1, 41.7, 42.9],
            26: [42.7, 40.0, 35.3, 28.9, 23.5, 20.8, 21.8, 26.3, 32.5, 37.9, 41.8, 43.3],
            28: [43.0, 39.9, 34.8, 28.1, 22.5, 19.7, 20.7, 25.3, 31.9, 37.6, 41.9, 43.6],
            30: [43.1, 39.8, 34.3, 27.2, 21.4, 18.5, 19.6, 24.4, 31.2, 37.3, 42.0, 43.9],
            32: [43.3, 39.6, 33.7, 26.2, 20.3, 17.4, 18.5, 23.4, 30.4, 37.0, 42.1, 44.1],
            34: [43.3, 39.3, 33.0, 25.3, 19.2, 16.2, 17.4, 22.3, 29.7, 36.6, 42.0, 44.3],
            36: [43.4, 39.0, 32.3, 24.3, 18.0, 15.1, 16.2, 21.3, 28.9, 36.1, 42.0, 44.4],
            38: [43.4, 38.7, 31.6, 23.3, 16.9, 13.9, 15.1, 20.2, 28.0, 35.6, 41.9, 44.5],
            40: [43.3, 38.3, 30.9, 22.2, 15.8, 12.8, 13.9, 19.1, 27.1, 35.1, 41.8, 44.6],
        }

    def obter_radiacao_solar_ra(self, latitude_sul, mes_index):
        """
        Obtém a radiação solar (Ra) com base na latitude sul e no mês do ano.
        """
        # Garante que o mês está no intervalo correto
        if mes_index < 1 or mes_index > 12:
            mes_index = 1

        # O valor da latitude vem do GPS, convertemos para absoluto (caso negativo)
        lat_abs = abs(latitude_sul)

        # Arredonda para o valor par mais próximo
        lat_par = round(lat_abs / 2) * 2

        # Garante que a latitude está dentro dos limites da tabela
        if lat_par < 0:
            lat_par = 0
        elif lat_par > 40:
            lat_par = 40

        return self.tabela_ra[lat_par][mes_index - 1]

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

        # Usa a matriz baseada na Tabela 2 para obter a Radiação Solar (Ra)
        ra = self.obter_radiacao_solar_ra(latitude, mes_index)

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
