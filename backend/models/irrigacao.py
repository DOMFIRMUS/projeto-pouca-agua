import math
import datetime

class CalculadorIrrigacao:

    def definir_kc_por_estagio(self, kc_inicial, kc_media, kc_final, estagio):
        if estagio == 'inicial':
            return kc_inicial
        elif estagio == 'meia_estacao':
            return kc_media
        elif estagio == 'final':
            return kc_final
        else:
            return kc_media

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

        self.tabela_n = {
            0: [12.1, 12.1, 12.1, 12.1, 12.1, 12.1, 12.1, 12.1, 12.1, 12.1, 12.1, 12.1],
            2: [12.2, 12.2, 12.1, 12.0, 12.0, 12.0, 12.0, 12.0, 12.1, 12.1, 12.2, 12.2],
            4: [12.3, 12.2, 12.1, 12.0, 11.9, 11.8, 11.9, 12.0, 12.1, 12.2, 12.3, 12.4],
            6: [12.4, 12.3, 12.1, 11.9, 11.8, 11.7, 11.8, 11.9, 12.1, 12.3, 12.4, 12.5],
            8: [12.5, 12.3, 12.1, 11.9, 11.7, 11.6, 11.6, 11.8, 12.0, 12.3, 12.5, 12.6],
            10: [12.6, 12.4, 12.1, 11.8, 11.6, 11.4, 11.5, 11.7, 12.0, 12.3, 12.6, 12.7],
            12: [12.7, 12.5, 12.2, 11.8, 11.5, 11.3, 11.4, 11.6, 12.0, 12.4, 12.7, 12.8],
            14: [12.8, 12.5, 12.2, 11.7, 11.4, 11.2, 11.3, 11.6, 12.0, 12.4, 12.8, 13.0],
            16: [12.9, 12.6, 12.2, 11.7, 11.3, 11.0, 11.2, 11.5, 12.0, 12.5, 12.9, 13.1],
            18: [13.0, 12.6, 12.2, 11.6, 11.2, 10.9, 11.0, 11.4, 11.9, 12.5, 13.0, 13.2],
            20: [13.2, 12.7, 12.2, 11.5, 11.0, 10.8, 10.9, 11.3, 11.9, 12.6, 13.1, 13.4],
            22: [13.3, 12.8, 12.2, 11.4, 10.9, 10.6, 10.8, 11.2, 11.9, 12.6, 13.2, 13.5],
            24: [13.4, 12.8, 12.2, 11.4, 10.8, 10.5, 10.6, 11.1, 11.8, 12.7, 13.4, 13.6],
            26: [13.6, 12.9, 12.3, 11.3, 10.6, 10.3, 10.5, 11.0, 11.8, 12.8, 13.5, 13.8],
            28: [13.7, 13.0, 12.3, 11.2, 10.5, 10.1, 10.3, 10.9, 11.8, 12.8, 13.6, 14.0],
            30: [13.9, 13.1, 12.3, 11.1, 10.3, 9.9, 10.1, 10.8, 11.8, 12.9, 13.8, 14.2],
            32: [14.1, 13.2, 12.3, 11.0, 10.1, 9.7, 10.0, 10.6, 11.7, 13.0, 13.9, 14.3],
            34: [14.3, 13.3, 12.3, 10.9, 10.0, 9.5, 9.7, 10.5, 11.7, 13.1, 14.1, 14.5],
            36: [14.5, 13.4, 12.4, 10.8, 9.8, 9.2, 9.5, 10.4, 11.7, 13.2, 14.3, 14.8],
            38: [14.7, 13.5, 12.4, 10.6, 9.5, 9.0, 9.3, 10.2, 11.6, 13.3, 14.5, 15.0],
            40: [15.0, 13.6, 12.4, 10.5, 9.3, 8.7, 9.0, 10.0, 11.6, 13.4, 14.8, 15.3],
        }

    def obter_insolacao_maxima_n(self, latitude_sul, mes_index):
        """
        Obtém a insolação máxima (N) com base na latitude sul e no mês do ano.
        """
        # Garante que o mês está no intervalo correto
        if mes_index < 1 or mes_index > 12:
            mes_index = 1

        # Usa o valor absoluto da latitude e limita entre 0 e 40
        lat_abs = abs(latitude_sul)
        lat_limitada = max(0, min(40, lat_abs))

        # Arredonda para o número par mais próximo
        lat_arredondada = round(lat_limitada / 2.0) * 2

        return self.tabela_n[int(lat_arredondada)][int(mes_index) - 1]
        # Tabela 4 da tese: Insolação máxima (N) em horas para Latitudes Sul
        self.tabela_n = {
            20: [13.1, 12.7, 12.1, 11.5, 11.1, 10.8, 10.9, 11.3, 11.9, 12.5, 13.0, 13.2],
        }

    def calcular_rs(self, n_horas_sol, N_max, ra_topo):
        """
        Calcula a Radiação Solar na superfície (Rs) em MJ/m2/dia.
        Equação 16 da tese: Rs = (0.25 + 0.50 * (n / N)) * Ra
        """
        if N_max <= 0:
            return 0.0

        rs = (0.25 + 0.50 * (n_horas_sol / N_max)) * ra_topo
        return round(rs, 2)
    def calcular_pressao_saturacao_es(self, t_max, t_min):
        """
        Calcula a Pressão de Saturação de Vapor (es) média usando o método de Penman-Monteith (FAO56).
        Equação 14: e_o(T) = 0.6108 * exp[(17.27 * T) / (T + 273.3)]
        Equação 13: es = (e_o(T_max) + e_o(T_min)) / 2
        Retorna em kPa.
        """
        def eo(t):
            return 0.6108 * math.exp((17.27 * t) / (t + 273.3))

        eo_tmax = eo(t_max)
        eo_tmin = eo(t_min)
        es = (eo_tmax + eo_tmin) / 2.0
        return es

    def calcular_pressao_atual_ea(self, es, umidade_relativa_media_ur):
        """
        Calcula a Pressão Atual de Vapor (ea) usando a umidade relativa.
        Equação 15: ea = es * (UR_m / 100)
        Retorna em kPa.
        """
        return es * (umidade_relativa_media_ur / 100.0)

    def calcular_deficit_pressao_vapor(self, es, ea):
        """
        Calcula o Déficit de Pressão de Vapor (es - ea).
        Retorna em kPa.
        """
        return es - ea

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

    def calcular_eto_blaney_criddle(self, t_media, mes_index, latitude_sul=20.0):
        pass # stub

    def calcular_pressao_atual_ea(self, es, umidade_relativa_media_ur):
        """
        Calcula a Pressão Atual de Vapor (ea) em kPa.
        Equação 15 da Tese: ea = es * (UR_m / 100)
        """
        ea = es * (umidade_relativa_media_ur / 100.0)
        return round(ea, 4)

    def calcular_deficit_pressao_vapor(self, es, ea):
        """
        Calcula o Déficit de Pressão de Vapor (es - ea) em kPa.
        """
        return round(es - ea, 4)

    def calcular_eto_blaney_criddle(self, t_media, mes_index, latitude_sul=20.0):
        """
        Baseado na Tabela 3 - Percentagem diária de horas anuais de luz solar (P) para Latitude Sul.
        """
        # Tabela 3 - Percentagem diária de horas anuais de luz solar (Latitudes Sul)
        # Mapeia latitude (0 a 60) para os meses (1 a 12)
        # Note que a Tabela 3 tem a ordem para "South" começando com Julho.
        # Os valores da Tabela 3 lidos pela OCR (e corrigidos onde óbvio):
        # Lat South: Jul Aug Sep Oct Nov Dec Jan Feb Mar Apr May Jun
        # Reorganizando para a ordem dos meses Jan (1) a Dez (12):
        tabela_p_sul = {
            60: [41, 38, 32, 26, 20, 15, 13, 17, 22, 28, 34, 40],
            55: [39, 36, 32, 26, 21, 17, 16, 18, 23, 28, 33, 39],
            50: [36, 34, 31, 27, 23, 19, 18, 20, 24, 28, 32, 35],
            45: [35, 34, 30, 27, 23, 20, 20, 21, 24, 28, 32, 34],
            40: [34, 32, 30, 27, 24, 22, 21, 22, 25, 28, 31, 33],
            35: [32, 31, 29, 27, 25, 23, 22, 23, 25, 28, 30, 32],
            30: [32, 31, 29, 27, 25, 24, 23, 24, 26, 28, 30, 31],
            25: [31, 30, 29, 27, 26, 24, 24, 25, 26, 28, 29, 31],
            20: [30, 29, 28, 27, 26, 25, 25, 26, 27, 28, 29, 30],
            15: [29, 29, 28, 27, 26, 26, 25, 26, 27, 28, 28, 29],
            10: [29, 28, 28, 27, 27, 26, 26, 26, 27, 28, 28, 29],
            5:  [28, 28, 28, 27, 27, 27, 27, 27, 27, 28, 28, 28],
            0:  [27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27]
        }

        # Garante que o mês está no intervalo correto
        if mes_index < 1 or mes_index > 12:
            mes_index = 1

        lat_abs = abs(latitude_sul)

        # Arredonda para o múltiplo de 5 mais próximo
        lat_arredondada = round(lat_abs / 5) * 5

        # Garante que a latitude está dentro dos limites da tabela
        if lat_arredondada < 0:
            lat_arredondada = 0
        elif lat_arredondada > 60:
            lat_arredondada = 60

        # Pega a lista de porcentagens para a latitude arredondada
        p_valores = tabela_p_sul.get(lat_arredondada, tabela_p_sul[20])
        p = p_valores[mes_index - 1]

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

    def calcular_eto_penman_monteith(self, rn, g, t_media, u2, es, ea, delta, gama):
        """
        Calcula a Evapotranspiração de Referência (ETo em mm/dia) usando a equação
        de Penman-Monteith - FAO56 (Equação 12 da imagem).
        """
        # Equação 12 da imagem: ETo = (0.408 * delta * (Rn - G) + gama * (900 / (T + 273)) * u2 * (es - ea)) / (delta + gama * (1 + 0.34 * u2))
        numerador_1 = 0.408 * delta * (rn - g)
        numerador_2 = gama * (900 / (t_media + 273)) * u2 * (es - ea)
        denominador = delta + gama * (1 + 0.34 * u2)

        if denominador == 0:
            return 0.0

        eto = (numerador_1 + numerador_2) / denominador
        return round(eto, 2)

    def corrigir_fator_deplecao(self, f_tabela, etc_calculada):
        """
        Corrige dinamicamente o fator de depleção (f) baseado na Evapotranspiração da Cultura (ETc),
        conforme Equação 39 da tese.
        O valor retornado é limitado entre 0.1 e 0.8 para proteger a planta.
        """
        f_corrigido = f_tabela + 0.04 * (5 - etc_calculada)
        return max(0.1, min(0.8, round(f_corrigido, 4)))

    def calcular_irn_e_cad(self, tomcc, to_pmp, profundidade_z, fator_f, pw_percent, etc_calculada=None):
        """
        Calcula a Capacidade de Água Disponível (CAD) e a Irrigação Real Necessária Máxima (IRN_max)
        baseado no solo e na fração de área umedecida (Equações 36 e 40 da tese).
        """
        # Equação 36: CAD = 1000 * (to_cc - to_pmp) * z
        cad = 1000 * (tomcc - to_pmp) * profundidade_z

        # Fração de área umedecida (decimal)
        fw = pw_percent / 100.0

        # Corrige o fator de depleção caso a ETc tenha sido fornecida
        if etc_calculada is not None:
            fator_f = self.corrigir_fator_deplecao(fator_f, etc_calculada)

        # Equação 40: IRN_max = CAD * f * Fw
        irn_max = cad * fator_f * fw
        return round(cad, 2), round(irn_max, 2)

    def calcular_kl(self, metodo, p_decimal):
        """
        Calcula o Coeficiente de Localização (KL) para irrigação localizada.
        'p_decimal' é a fração da área umedecida ou sombreada (o que for maior).
        """
        if metodo == 'Keller':
            kl = p_decimal + 0.15 * (1 - p_decimal)
        elif metodo == 'Bernardo':
            kl = p_decimal
        elif metodo == 'Fereres':
            if p_decimal >= 0.65:
                kl = 1.0
            elif 0.20 < p_decimal < 0.65:
                kl = (1.09 * p_decimal) + 0.30
            else:
                kl = (1.94 * p_decimal) + 0.10
        elif metodo == 'Keller_Bliesner':
            kl = 0.10 * math.sqrt(p_decimal * 100)
        else:
            kl = 1.0
        return round(kl, 2)

    def calcular_etc(self, eto, kc, kl=1.0):
        """
        Calcula a Evapotranspiração da Cultura (ETc) usando ETo, Kc e KL.
        ETc = ETo * Kc * KL
        """
        etc = eto * kc * kl
        return round(etc, 2)
    def calcular_itn(self, irn_mm, ce_agua_ds_m, min_ce, max_ce, uniformidade_emissao_decimal):
        """
        Calcula a Irrigação Total Necessária (ITN) e a Fração de Lixiviação (FL)
        com base nas Equações 42 e 43 da tese, utilizando min_ce e max_ce específicos da cultura.
        """
        # Equação 43: FL = CEa / (2 * CEes_max)
        fl = ce_agua_ds_m / (2 * max_ce)

        # Limitar o FL a valores viáveis para evitar divisão por zero ou negativa na eq. 42
        if fl >= 1.0:
            fl = 0.99
        elif fl < 0.0:
            fl = 0.0

        # Equação 42: ITN = IRN / ((1 - FL) * EAP * Ea)
        # Assumindo EAP = 1.0 (Eficiência de Aplicação) e Ea = uniformidade_emissao_decimal
        eap = 1.0
        itn = irn_mm / ((1 - fl) * eap * uniformidade_emissao_decimal)

        return round(fl, 4), round(itn, 2)

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

    def calcular_tempo_irrigacao(self, itn_mm, espacamento_plantas_sp, espacamento_fileiras_sr, pw_area_umedecida, dw_diametro_molhado, vazao_emissor_qa):
        """
        Calcula o número de emissores por planta (Np) e o Tempo de Irrigação (TI) em horas.
        """
        if dw_diametro_molhado <= 0 or vazao_emissor_qa <= 0:
            return 0.0, 1

        # Np_teorico = (4 * Sp * Sr * Pw) / (pi * Dw^2 * 100)
        np_teorico = (4 * espacamento_plantas_sp * espacamento_fileiras_sr * pw_area_umedecida) / (math.pi * (dw_diametro_molhado ** 2) * 100)
        np = math.ceil(np_teorico)

        if np <= 0:
            np = 1

        # TI = (ITN * Sp * Sr) / (Np * Qa)
        ti = (itn_mm * espacamento_plantas_sp * espacamento_fileiras_sr) / (np * vazao_emissor_qa)

        return ti, np
    def perda_direta_derivacao(self, vel_derivacao_vd, diametro_derivacao_dd, area_protrusao_ap):
        """
        Calcula a Perda Localizada de Carga por Passagem Direta em conectores (Modelo de Vilaça, Eq 76).
        Retorna o valor em m.c.a.
        """
        if diametro_derivacao_dd <= 0:
            return 0.0

        hfl_d = 0.043695 * (vel_derivacao_vd ** 1.897) * (diametro_derivacao_dd ** -2.428) * (area_protrusao_ap ** 1.109)
        return round(hfl_d, 4)

    def calcular_hfl_direta_vilaca(self, v_D, D_D, A_P):
        """
        Calcula a Perda Localizada de Carga por Passagem Direta em conectores (Modelo de Vilaça, Eq 76).
        """
        if not (0.133 <= v_D <= 3.0):
            return {"validacao_modelo_direto": "fora_dos_limites"}
        if not (0.0357 <= D_D <= 0.0721):
            return {"validacao_modelo_direto": "fora_dos_limites"}
        if not (103e-6 <= A_P <= 355e-6):
            return {"validacao_modelo_direto": "fora_dos_limites"}

        hfl_d = 0.043695 * (v_D ** 1.897) * (D_D ** -2.428) * (A_P ** 1.109)
        return round(hfl_d, 4)
    def calcular_turno_rega_max(self, irn_max_mm, etc_mm_dia, sp_m, sr_m):
        """
        Calcula o Turno de Rega Máximo (TR_max) baseado na Equação 44 da tese.
        """
        if etc_mm_dia <= 0 or sp_m <= 0 or sr_m <= 0:
            return 0

        tr_max = math.floor(irn_max_mm / (etc_mm_dia * sp_m * sr_m))
        return tr_max
    def resolver_fator_atrito_f(self, velocidade, diametro_m):
        """
        Calcula o fator de atrito (f) baseado na velocidade e no diâmetro.
        Utiliza o número de Reynolds (R) e equações para diferentes regimes de escoamento.
        """
        r = (velocidade * diametro_m) / 1.01e-6

        if r < 2000:
            f = 64 / r if r > 0 else 0
        elif 2000 <= r < 3000:
            f = 0.04
        else:
            f = 0.316 / (r ** 0.25)

        return f

    def comprimento_trecho_a_trecho(self, diametro_m, vazao_emissor_m3s, espacamento_m, pressao_entrada_mca, declividade, hvar_max):
        """
        Calcula o comprimento máximo da linha lateral trecho a trecho (do último emissor para o primeiro).
        """
        pressao_ultimo_emissor = pressao_entrada_mca
        pressao_anterior = pressao_ultimo_emissor
        comprimento_total = 0.0
        i = 1

        area = math.pi * (diametro_m ** 2) / 4.0

        while True:
            vazao_acumulada_m3s = i * vazao_emissor_m3s
            v = vazao_acumulada_m3s / area
            f = self.resolver_fator_atrito_f(v, diametro_m)

            hf = 8.263e-2 * f * (vazao_acumulada_m3s ** 2 / diametro_m ** 5) * espacamento_m

            # Pressão no emissor atual = pressão do emissor anterior + perda de carga + desnível
            pressao_atual = pressao_anterior + hf + (declividade * espacamento_m)

            if abs(pressao_atual - pressao_ultimo_emissor) > hvar_max:
                break

            comprimento_total += espacamento_m
            pressao_anterior = pressao_atual
            i += 1

        return comprimento_total

    def verificar_limite_salinidade(self, ce_agua_i, cultura_nome):
        """
        Filtro de proteção contra salinização do solo baseado na diretriz de manejo (pág 26 da tese).
        Busca os limites min_ce e max_ce da cultura e verifica: CE_i <= (max_ce + min_ce) / 2
        """
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from database import get_db_connection

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT min_ce, max_ce FROM culturas WHERE nome = ?", (cultura_nome,))
        row = cursor.fetchone()
        conn.close()

        if row:
            min_ce = row['min_ce']
            max_ce = row['max_ce']
            limite = (max_ce + min_ce) / 2.0
            if ce_agua_i > limite:
                return {
                    "salinidade_critica": True,
                    "alerta_manejo": "A salinidade da água ultrapassa a média de resiliência da cultura. Risco iminente de perda de produção."
                }
        return {"salinidade_critica": False}

    def avaliar_status_solo(self, valor_umidade):
        if valor_umidade < self.umidade_critica:
            return {"status": "Crítico (Seco)", "cor_alerta": "danger", "irrigar": True, "mensagem": "Solo excessivamente seco. Ligue a irrigação."}
        elif self.umidade_critica <= valor_umidade < self.umidade_ideal_min:
            return {"status": "Moderado", "cor_alerta": "warning", "irrigar": True, "mensagem": "A umidade está caindo. Recomenda-se irrigar levemente."}
        elif self.umidade_ideal_min <= valor_umidade <= self.umidade_ideal_max:
            return {"status": "Ideal", "cor_alerta": "success", "irrigar": False, "mensagem": "Solo com umidade perfeita."}
        else:
            return {"status": "Encharcado", "cor_alerta": "info", "irrigar": False, "mensagem": "Solo muito úmido. Evite desperdiçar água."}

    def calcular_lambda(self, comprimento_equivalente_le, espacamento_emissores_se):
        """
        Calcula o fator de comprimento equivalente (lambda) para perdas localizadas.
        Equação 51: lambda = (Le + Se) / Se
        """
        if espacamento_emissores_se <= 0:
            return 1.0 # fallback caso espaçamento seja zero ou negativo
        return (comprimento_equivalente_le + espacamento_emissores_se) / espacamento_emissores_se

    def calcular_perda_carga(self, diametro_mm, vazao_gotejador_lh, espacamento_m, comprimento_m, comprimento_equivalente_le=0.0):
        """
        Calcula a perda de carga em uma linha lateral de gotejamento usando a equação
        empírica para tubos plásticos pequenos (Flamant/Blasius) com fator de comprimento equivalente (lambda)
        e aplica o fator de Christiansen.
        """
        if espacamento_m <= 0:
            return {"erro": "Espaçamento deve ser maior que zero"}

        n_emissores = int(comprimento_m / espacamento_m)
        if n_emissores == 0:
            return {"erro": "O comprimento deve ser maior ou igual ao espaçamento"}

        vazao_total_lh = n_emissores * vazao_gotejador_lh

        # Vazão em m³/s e Diâmetro em m para a fórmula de perda de carga
        q_m3s = (vazao_total_lh / 1000.0) / 3600.0
        d_m = diametro_mm / 1000.0

        if d_m <= 0:
             return {"erro": "Diâmetro deve ser maior que zero"}

        # Equação de Flamant/Blasius para plásticos pequenos: m = 1.75
        m = 1.75

        fator_lambda = self.calcular_lambda(comprimento_equivalente_le, espacamento_m)

        # Equação empírica de perda de carga para tubo contínuo (hf) com fator lambda
        # hf_continua = 2.8287e-4 * Q^1.75 * D^-4.75 * L * lambda
        hf_continua = 2.8287e-4 * (q_m3s ** 1.75) * (d_m ** -4.75) * comprimento_m * fator_lambda

        # Fator de Christiansen para múltiplas saídas
        fator_f = (1 / (m + 1)) + (1 / (2 * n_emissores)) + (math.sqrt(m - 1) / (6 * n_emissores**2))

        # Perda de carga real
        hf_mca = hf_continua * fator_f

        status = "Aceitável" if hf_mca <= 2.0 else "Desuniformidade Elevada"

        return {
            "vazao_total_lh": round(vazao_total_lh, 2),
            "perda_carga_mca": round(hf_mca, 3),
            "status": status,
            "fator_lambda": round(fator_lambda, 4)
        }
    def obter_kc_atual(self, data_plantio, dias_fases, kc_valores):
        """
        Calcula o Coeficiente de Cultura (Kc) atual baseado na idade da planta.
        """
        if isinstance(data_plantio, str):
            data_plantio = datetime.datetime.strptime(data_plantio, "%Y-%m-%d").date()

        hoje = datetime.date.today()
        idade_dias = (hoje - data_plantio).days

        if idade_dias < dias_fases['inicial']:
            return kc_valores['inicial']
        elif idade_dias <= dias_fases['inicial'] + dias_fases['meia_estacao']:
            return kc_valores['media']
        else:
            return kc_valores['final']
    def dimensionar_diametro_trecho(self, fator_atrito_f, vazao_trecho_q, desnivel_trecho_dz, comprimento_trecho_L, h0=0.0):
        """
        Dimensiona a linha de derivação trecho a trecho.
        Calcula o diâmetro teórico interno usando a Equação 74 da tese,
        e o ganho de pressão pela Equação 75.
        """
        # Assumir a perda de carga do trecho (hf) como sendo igual ao desnível (dz)
        hf = desnivel_trecho_dz

        if hf <= 0:
            return 0.0

        # Equação 74: D = ((8.263e-2 * f * (Q^2) * L) / hf) ^ (1/5)
        d_teorico = ((8.263e-2 * fator_atrito_f * (vazao_trecho_q ** 2) * comprimento_trecho_L) / hf) ** 0.2

        # Equação 75: H1 = H0 - hf + dz
        # (Essa variável é calculada apenas para cumprir o requisito, mas não é retornada)
        h1 = h0 - hf + desnivel_trecho_dz

        return d_teorico
    def fracionar_tempo_irrigacao(self, ti_total_horas, tempo_maximo_bomba_horas=2.0):
        """
        Fraciona o tempo total de irrigação para proteger a bomba de água de operar
        continuamente por mais tempo que o seu limite seguro.
        """
        if ti_total_horas <= 0:
            return {
                "tempo_total_horas": 0.0,
                "numero_ciclos": 0,
                "horas_por_ciclo": 0.0,
                "tempo_descanso_recomendado_horas": 1.0
            }

        numero_ciclos = math.ceil(ti_total_horas / tempo_maximo_bomba_horas)
        horas_por_ciclo = round(ti_total_horas / numero_ciclos, 2)

        return {
            "tempo_total_horas": round(ti_total_horas, 2),
            "numero_ciclos": numero_ciclos,
            "horas_por_ciclo": horas_por_ciclo,
            "tempo_descanso_recomendado_horas": 1.0
        }
    def calcular_area_umedecida(self, q_vazao, volume_z, ko_condutividade, espacamento_plantas_sp, espacamento_fileiras_sr, numero_emissores_np):
        """
        Calcula o Diâmetro Molhado (Dw) e a Porcentagem de Área Umedecida (Pw).
        """
        if ko_condutividade <= 0 or espacamento_plantas_sp <= 0 or espacamento_fileiras_sr <= 0:
            return 0.0, 0.0

        dw = 1.32 * ((volume_z * q_vazao) / ko_condutividade) ** (1/3)
        pw = numero_emissores_np * ((math.pi * (dw ** 2)) / (4 * espacamento_plantas_sp * espacamento_fileiras_sr)) * 100

        return round(dw, 2), round(pw, 2)
    def calcular_area_sombreada(self, tipo_copa, espacamento_plantas_sp, espacamento_fileiras_sr, largura_faixa_ss=None, diametro_copa_dco=None):
        """
        Calcula a Porcentagem de Área Sombreada (Ps).
        """
        if espacamento_fileiras_sr <= 0:
            return 0.0

        tipo_copa = tipo_copa.lower()

        if tipo_copa == 'faixa_continua':
            if largura_faixa_ss is None:
                return 0.0
            # Equação 28: Ps = (largura_faixa_ss / espacamento_fileiras_sr) * 100
            ps = (largura_faixa_ss / espacamento_fileiras_sr) * 100
            return round(ps, 2)

        elif tipo_copa == 'arvore_isolada':
            if diametro_copa_dco is None or espacamento_plantas_sp <= 0:
                return 0.0
            # Equação 29: Ps = ((math.pi * (diametro_copa_dco ** 2) / 4) / (espacamento_fileiras_sr * espacamento_plantas_sp)) * 100
            area_copa = (math.pi * (diametro_copa_dco ** 2)) / 4
            area_plantio = espacamento_fileiras_sr * espacamento_plantas_sp
            ps = (area_copa / area_plantio) * 100
            return round(ps, 2)

        return 0.0
    def calcular_lmax_perfil_tipo_IId(self, H, Hvar, So, k_linha, L_inicial=50.0):
        """
        Calcula o comprimento máximo (L) para o Perfil Tipo II-d (Declive Muito Forte).
        Valida a restrição de limite físico da Equação 66 e implementa a Equação 67 da tese iterativamente.
        """
        L_atual = L_inicial
    def calcular_lmax_perfil_tipo_IIc(self, H, Hvar, So, k_linha, L_inicial=50.0):
        """
        Calcula o comprimento máximo L para o Perfil Tipo II-c (Declive Forte).
        Resolução iterativa da Equação 65 e validação da Equação 64 da tese.
        """
        L = L_inicial

        for _ in range(1000):
            L_novo = (Hvar + (k_linha * (L ** 2.75)) / 2.75) / So
            if abs(L_novo - L) < 1e-4:
                L_round = round(L_novo, 3)
                # Validar a condição de existência baseada na Equação 64 da tese
                razao = So / (k_linha * (L_round ** 1.75))
                if 1 < razao < 2.75:
                    return L_round
                else:
                    raise ValueError(f"Condição de existência falhou: razão {razao:.4f} fora do intervalo (1, 2.75)")
            L = L_novo

        raise ValueError("O loop iterativo não estabilizou em três casas decimais.")
    def calcular_lmax_perfil_tipo_IIa(self, H, Hvar, So, k_linha, L_inicial=50.0):
        """
        Determina o Comprimento Máximo da Linha Lateral sob o Perfil Tipo II-a (Declive Fraco).
        Utiliza o algoritmo de aproximações sucessivas baseado nas equações 59, 60 e 61 da tese.
        """
        L = L_inicial
        iteracoes = 0
        max_iteracoes = 1000

        while iteracoes < max_iteracoes:
            razao = So / (k_linha * (L_atual ** 1.75))
            if razao < 2.75:
                raise ValueError(f"Restrição de limite físico não atendida (Equação 66): S0 / (k' * L^1.75) = {razao:.4f} < 2.75. O ganho por desnível não supera totalmente a perda por atrito em todas as seções.")

            L_novo = (H * Hvar) / ((So - k_linha * (L_atual ** 1.75)) * (1 - Hvar))

            if abs(L_novo - L_atual) < 0.001:
                return L_novo

            L_atual = L_novo
            iteracoes += 1

        raise ValueError("A iteração para calcular L não convergiu após 1000 passos.")

    def calcular_porcentagem_area_sombreada_ps(self, tipo_calculo, params):
        if tipo_calculo not in ['faixa_sombreada', 'diametro_copa']:
            raise ValueError('Método de cálculo de área sombreada inválido ou dados insuficientes.')

        ps = 0.0

        if tipo_calculo == 'faixa_sombreada':
            ss_largura = params.get('ss_largura')
            sr_espacamento = params.get('sr_espacamento')

            if ss_largura is None or sr_espacamento is None:
                raise ValueError('Método de cálculo de área sombreada inválido ou dados insuficientes.')

            if sr_espacamento <= 0:
                return 0.0

            # Equação 28
            ps = (ss_largura / sr_espacamento) * 100.0

        elif tipo_calculo == 'diametro_copa':
            dco_diametro = params.get('dco_diametro')
            sr_espacamento = params.get('sr_espacamento')
            sp_espacamento = params.get('sp_espacamento')

            if dco_diametro is None or sr_espacamento is None or sp_espacamento is None:
                raise ValueError('Método de cálculo de área sombreada inválido ou dados insuficientes.')

            if sr_espacamento <= 0 or sp_espacamento <= 0:
                return 0.0

            # Equação 29
            area_copa = math.pi * ((dco_diametro ** 2) / 4.0)
            area_plantio = sr_espacamento * sp_espacamento
            ps = (area_copa / area_plantio) * 100.0

        # Normalização limitando o teto matemático a 100.0 e arredondando para 2 casas
        ps = min(ps, 100.0)
        return round(ps, 2)
    def calcular_lmax_perfil_tipo_IIa(self, H, Hvar, So, k_linha, chute_inicial=50.0):
        L = chute_inicial
        iteracoes = 0
        while iteracoes < 1000:
            iteracoes += 1

    def _calcular_condicao_59(self, So, k_linha, L):
        # Condição da Equação 59
        condicao = So / (k_linha * (L ** 1.75))
        if not (0 < condicao < 1):
            raise ValueError(f"Condição da Equação 59 não satisfeita (deve estar entre 0 e 1): {condicao}")

            # Equação 61
            razao_lL = 1 - 0.56098 * (condicao ** 0.57143)

            # Equação 60
            numerador = H * Hvar
            denominador = ((1 - ((1 - razao_lL) ** 2.35)) * k_linha * (L ** 1.33)) - (razao_lL * So)

            if denominador == 0:
                 raise ZeroDivisionError("Divisão por zero ao calcular o novo comprimento L.")

            L_novo = numerador / denominador

            # Critério de paragem
            if abs(L_novo - L) < 0.001:
                return round(L_novo, 3)

            L = L_novo

        raise Exception("O cálculo não convergiu após o número máximo de iterações.")

    def resolver_lmax_perfil_ii_c(self, pressao_h, h_var_fraction, k_linha, declividade_so, max_iter=300, tol=1e-4):
        """
        Solver iterativo para o Perfil Tipo II-c (Equação 65 - Pág. 71).
        Utiliza o algoritmo de iteração de ponto fixo.
        """
        abs_so = abs(declividade_so)
        if abs_so == 0.0:
            return 0.0

        L_n = 50.0  # Chute inicial

        for _ in range(max_iter):
            abs_l_n = abs(L_n)
            k_L_175 = k_linha * (abs_l_n ** 1.75)

            if k_L_175 == 0.0:
                return 0.0

            # Condição = |So| / (k' * L^1.75)
            condicao = abs_so / k_L_175

            # Equação 61
            r_min = 1.0 - 0.56098 * (condicao ** 0.57143)

            numerador = pressao_h * h_var_fraction

            base_r_min = 1.0 - r_min
            if base_r_min < 0:
                base_r_min = 0.0

            # Denominador da Eq 65:
            denominador = (
                abs_so
                - k_L_175
                - (r_min * abs_so)
                + ((1.0 - (base_r_min ** 2.75)) * k_L_175)
                - (pressao_h * h_var_fraction * (abs_so - k_L_175))
            )

            # Trava de Segurança matemática
            if denominador == 0.0:
                return 0.0

            L_novo = abs(numerador / denominador)

            if abs(L_novo - L_n) < tol:
                return round(L_novo, 3)

            L_n = 0.1 * L_novo + 0.9 * L_n

        return round(L_n, 3)

    def classificar_perfil_pressao(self, So, k_linha, L_estimado):
        """
        Classifica o perfil de pressão hidráulica baseado na tese (Pág. 71).
        So: declividade em decimal
        k_linha: constante da linha
        L_estimado: comprimento estimado
        """
        if So <= 0:
            return 'Perfil Tipo I (Aclive ou Nível)'

        J = k_linha * (L_estimado ** 1.75)
        razao = abs(So) / J

        if 0 < razao < 1:
            return 'Perfil Tipo IIa (Declive Fraco)'
        elif razao == 1:
            return 'Perfil Tipo IIb (Declive Moderado)'
        elif 1 < razao < 2.75:
            return 'Perfil Tipo IIc (Declive Forte)'
        else:
            return 'Perfil Tipo IId (Declive Muito Forte)'

    def calcular_lmax_perfil_tipo_IIb(self, H, Hvar, So, k_linha, L_estimado):
        """
        Calcula o Comprimento Máximo da Linha Lateral para Perfil Tipo II-b.
        Verifica a condição de ocorrência do Perfil Tipo II-b pela Equação 62 da tese: (k' * L^1.75) / So = 1
        E aplica a Equação 63 se a condição for atendida.
        """
        if So <= 0:
            return None

        razao = (k_linha * (L_estimado ** 1.75)) / So

        if math.isclose(razao, 1.0, rel_tol=1e-4, abs_tol=1e-4):
            # Equação 63: L = (H * Hvar) / (0.357 * So)
            L = (H * Hvar) / (0.357 * So)
            return L

        return None
    def orquestrar_dimensionamento_declive(self, H, Hvar, So, k_linha):
        """
        Orquestrador de busca de perfis hidráulicos segundo a página 37 da tese.
        """
        def eval_ratio(So, k_linha, L):
            if isinstance(L, complex):
                L = L.real
            denom = k_linha * (abs(L) ** 1.75)
            if denom == 0: denom = 1e-6
            return So / denom

        if So > 0:
            # Passo 1: Perfil Tipo II-a (Declive Fraco)
            L = 50.0
            for _ in range(500):
                if isinstance(L, complex): L = L.real
                L = abs(L)
                ratio = eval_ratio(So, k_linha, L)
                base_ratio = max(0, ratio)
                razao_lL = 1 - 0.56098 * (base_ratio ** 0.57143)

                base_term = max(0, 1 - razao_lL)

                denom = (((1 - (base_term ** 2.35)) * k_linha * (L ** 1.33)) - (razao_lL * So))
                if denom == 0: denom = 1e-6

                L_novo = (H * Hvar) / denom

                if abs(L_novo - L) < 0.001:
                    L = L_novo
                    break
                L = L_novo

            ratio = eval_ratio(So, k_linha, L)
            if 0 < ratio < 1:
                return {"comprimento_l_m": round(L.real, 2), "perfil_classificado": "Perfil Tipo II-a (Declive Fraco)"}

            # Passo 2: Perfil Tipo II-c (Declive Forte)
            L = 50.0
            for _ in range(500):
                if isinstance(L, complex): L = L.real
                L = abs(L)
                ratio = eval_ratio(So, k_linha, L)
                base_ratio = max(0, ratio)
                razao_lL = 1 - 0.56098 * (base_ratio ** 0.57143)
                base_term = max(0, 1 - razao_lL)

                k_L175 = k_linha * (L ** 1.75)
                denom = So - k_L175 + (1 - (base_term**2.75)) * k_L175 - Hvar * (So - k_L175)
                if denom == 0: denom = 1e-6
                L_novo = (H * Hvar) / denom

                if abs(L_novo - L) < 0.001:
                    L = L_novo
                    break
                L = L_novo

            ratio = eval_ratio(So, k_linha, L)
            if 1 < ratio < 2.75:
                return {"comprimento_l_m": round(L.real, 2), "perfil_classificado": "Perfil Tipo II-c (Declive Forte)"}

            # Passo 3: Perfil Tipo II-d (Declive Muito Forte)
            L = 50.0
            for _ in range(500):
                if isinstance(L, complex): L = L.real
                L = abs(L)
                k_L175 = k_linha * (L ** 1.75)
                denom = (So - k_L175) * (1 - Hvar)
                if denom == 0: denom = 1e-6
                L_novo = (H * Hvar) / denom

                if abs(L_novo - L) < 0.001:
                    L = L_novo
                    break
                L = L_novo

            ratio = eval_ratio(So, k_linha, L)
            if ratio >= 2.75:
                return {"comprimento_l_m": round(L.real, 2), "perfil_classificado": "Perfil Tipo II-d (Declive Muito Forte)"}

        # Passo 4: Fallback (Perfil Tipo I/III - Nível ou Aclive)
        L = 50.0
        for _ in range(500):
            if isinstance(L, complex): L = L.real
            L = abs(L)
            k_L175 = k_linha * (L ** 1.75)
            denom = k_L175 + So
            if denom == 0: denom = 1e-6
            L_novo = (H * Hvar) / denom

            if abs(L_novo - L) < 0.001:
                L = L_novo
                break
            L = L_novo

        if isinstance(L, complex): L = L.real
        return {"comprimento_l_m": round(L, 2), "perfil_classificado": "Perfil Tipo I/III (Nível ou Aclive)"}
    def calcular_lmax_perfil_tipo_I(self, H, Hvar, So, k_linha):
        """
        Calcula o comprimento máximo da linha lateral em Perfil Tipo I (Aclive)
        de forma iterativa utilizando a Equação 58 da tese.
        L = (H * Hvar) / (k_linha * L^1.75 + So)
        """
        L_anterior = 10.0
        while True:
            # Equação 58
            L_novo = (H * Hvar) / (k_linha * (L_anterior ** 1.75) + So)

            # Condição de parada (diferença menor que 0.01 metros)
            if abs(L_novo - L_anterior) < 0.01:
                return round(L_novo, 2)

            L_anterior = L_novo

    def perda_conector_lateral(self, diametro_conector_m, comprimento_conector_m, vel_conector_ms, vel_lateral_ms):
        """
        Calcula a Perda Localizada de Carga por conexão de entrada em MCA.
        Equação 77 da Tese (modelo de Vilaça).
        """
        hfl_l = 2.268121 * (diametro_conector_m ** 0.106) * (comprimento_conector_m ** 1.057) * (vel_conector_ms ** 1.766) * (vel_lateral_ms ** 0.386)
        return hfl_l

    def calcular_hfl_lateral_vilaca(self, D_C, L_C, v_C, v_L):
        """
        Calcula a perda localizada de carga decorrente da mudança de direção do fluxo na inserção da linha lateral.
        Implementa a Equação 77 da tese.
        """
        if not (0.0078 <= D_C <= 0.0167):
            raise ValueError(f"D_C ({D_C}) fora da faixa permitida (0.0078 - 0.0167 m).")
        if not (0.0495 <= L_C <= 0.0664):
            raise ValueError(f"L_C ({L_C}) fora da faixa permitida (0.0495 - 0.0664 m).")
        if not (0.267 <= v_C <= 14.378):
            raise ValueError(f"v_C ({v_C}) fora da faixa permitida (0.267 - 14.378 m/s).")
        if not (0.132 <= v_L <= 3.0):
            raise ValueError(f"v_L ({v_L}) fora da faixa permitida (0.132 - 3.0 m/s).")

        hfl_l = 2.268121 * (D_C ** 0.106) * (L_C ** 1.057) * (v_C ** 1.766) * (v_L ** 0.386)
        return hfl_l
    def perda_conector_zitterell(self, die, dis, lc, dt, vt):
        """
        Calcula a perda localizada de carga em conectores de linhas laterais usando o modelo de Zitterell (2011).

        Parâmetros:
        die (float): Diâmetro interno de entrada do conector (mm)
        dis (float): Diâmetro interno de saída do conector (mm)
        lc (float): Comprimento do conector (mm)
        dt (float): Diâmetro interno do tubo (mm)
        vt (float): Velocidade média de escoamento no tubo (m/s)

        Retorna:
        tuple: (hfc, aviso) onde hfc é a perda de carga (mca) e aviso é uma string ou None.
        """
        aviso = None

        # Limites do modelo
        if not (2.318 <= die <= 7.900) or \
           not (2.318 <= dis <= 12.006) or \
           not (21.483 <= lc <= 65.046) or \
           not (4.050 <= dt <= 12.854) or \
           not (0.363 <= vt <= 7.580):
            aviso = "Aviso de precisão reduzida"

        # Equação 72: Hf_c = 0.000141 * D_{ie}^{-5.739} * D_{is}^{2.156} * L_c^{0.925} * D_t^{1.756} * V_t^{1.971}
        hfc = 0.000141 * (die ** -5.739) * (dis ** 2.156) * (lc ** 0.925) * (dt ** 1.756) * (vt ** 1.971)

        return hfc, aviso

    def calcular_pressao_inicial_bomba(self, pressao_emissor, perda_carga_tubulacao, diametro_conector_m, comprimento_conector_m, vel_conector_ms, vel_lateral_ms):
        """
        Método principal de perda de carga:
        Calcula a pressão inicial necessária da bomba adicionando a perda de carga localizada (Hfl_l).
        """
        hfl_l = self.perda_conector_lateral(diametro_conector_m, comprimento_conector_m, vel_conector_ms, vel_lateral_ms)
        pressao_inicial = pressao_emissor + perda_carga_tubulacao + hfl_l
        return pressao_inicial

    def selecionar_tubo_comercial_otimo(self, diametro_teorico, f, Q, L, dz):
        """
        Escolha de tubos comerciais por aproximação de menor módulo descrita na página 40 da tese.
        """
        diametros_comerciais = [0.025, 0.032, 0.040, 0.050, 0.063, 0.075]

        inferiores = [d for d in diametros_comerciais if d <= diametro_teorico]
        superiores = [d for d in diametros_comerciais if d >= diametro_teorico]

        d_inferior = inferiores[-1] if inferiores else diametros_comerciais[0]
        d_superior = superiores[0] if superiores else diametros_comerciais[-1]

        tubos_selecionados = list(set([d_inferior, d_superior]))

        melhor_d = None
        menor_erro = float('inf')

        for d in tubos_selecionados:
            hf = 8.263e-2 * f * (Q ** 2) / (d ** 5) * L
            erro = abs(hf - dz)
            if erro < menor_erro:
                menor_erro = erro
                melhor_d = d

        return melhor_d
    def calcular_rn(self, t_max_c, t_min_c, ea, rs, rso, rns):
        """
        Calcula a Radiação de Onda Longa (Rnl) e o Saldo de Radiação (Rn)
        utilizando o balanço de energia do modelo Penman-Monteith.
        """
        if rso <= 0:
            return 0.0, 0.0

        if ea < 0:
            ea = 0.0

        t_max_k = t_max_c + 273.16
        t_min_k = t_min_c + 273.16
        sigma = 4.903e-9

        # Equação 19
        termo_temperatura = (sigma * (t_max_k ** 4) + sigma * (t_min_k ** 4)) / 2.0
        termo_umidade = 0.34 - 0.14 * math.sqrt(ea)
        termo_nebulosidade = 1.35 * (rs / rso) - 0.35

        r_nl = termo_temperatura * termo_umidade * termo_nebulosidade

        # Equação 20
        r_n = rns - r_nl

        return r_nl, r_n
    def calcular_rns(self, rs, ra, altitude_m):
        """
        Calcula a Radiação Solar de Céu Claro (Rso) e a Radiação Líquida de Onda Curta (Rns).
        Equação 17: Rso = [0.75 + 2 * (Altitude / 100000)] * Ra
        Equação 18: Rns = 0.77 * Rs
        Mantém a unidade: MJ * m^-2 * d^-1
        """
        rso = (0.75 + 2 * (altitude_m / 100000)) * ra
        rns = 0.77 * rs
        return round(rso, 2), round(rns, 2)
    def calcular_constante_psicrometrica(self, altitude_z):
        """
        Calcula a Pressão Atmosférica (P) e a Constante Psicrométrica (γ)
        com base na altitude z (metros) usando as Equações 22 e 23 da tese.
        """
        if altitude_z < 0:
            altitude_z = 0

        # Equação 22: P = 101.3 * (((293 - 0.0065 * z) / 293) ^ 5.26)
        p_kpa = 101.3 * (((293 - 0.0065 * altitude_z) / 293) ** 5.26)

        # Equação 23: gamma = 0.665 * 10^-3 * P
        gamma = (0.665 * (10 ** -3)) * p_kpa

        return round(p_kpa, 2), round(gamma, 6)
    def validar_criterio_pressao_subunidade(self, perda_carga_total_hf, pressao_entrada_h):
        """
        Validador de uniformidade de descarga hidráulica na subunidade baseando-se
        nas restrições de projeto da página 28 da tese.
        """
        if pressao_entrada_h <= 0:
            return {"status_hidraulico": "ERRO", "classe": "Pressão de entrada deve ser maior que zero."}

        hvar_real = (perda_carga_total_hf / pressao_entrada_h) * 100.0

        if hvar_real <= 20.0:
            return {
                "status_hidraulico": "ACEITAVEL",
                "classe": "Uniformidade de gotejamento excelente de acordo com os critérios do modelo computacional"
            }
        else:
            return {
                "status_hidraulico": "REJEITADO",
                "classe": "Desuniformidade Elevada. A variação de pressão viola o limite máximo de 20% estabelecido na tese. Reduza o comprimento ou aumente o diâmetro do tubo."
            }
    def otimizar_escalonamento_rega(self, irn_max, etc, sp, sr, itn, vazao_gotejador, emissores_planta):
        """
        Otimiza o tempo e turno de rega.
        """
        if etc <= 0 or sp <= 0 or sr <= 0 or emissores_planta <= 0 or vazao_gotejador <= 0:
            return 0, 0.0, 0

        # Turno de Rega Máximo (Equação 44)
        tr_max = math.floor(irn_max / (etc * sp * sr))

        # Tempo de Irrigação (TI) em horas (Equação 45)
        ti_horas = (itn * sp * sr) / (emissores_planta * vazao_gotejador)

        # Número ideal de subunidades de campo
        num_subunidades_sugeridas = 0
        if ti_horas > 0:
            num_subunidades_sugeridas = math.floor(24.0 / ti_horas)

        return tr_max, ti_horas, num_subunidades_sugeridas
    def calcular_raio_umedecido(self, alpha, q, ko, se):
        """
        Calcula o raio umedecido (Rw) pela Equação 26 e verifica se a faixa contínua é rompida.
        """
        import math

        if alpha <= 0 or ko <= 0:
            return {"erro": "Alpha e Ko devem ser maiores que zero."}

        term1 = 4 / ((alpha**2) * (math.pi**2))
        term2 = q / (math.pi * ko)
        term3 = 2 / (alpha * math.pi)

        inside_sqrt = term1 + term2 - term3

        if inside_sqrt < 0:
            return {"erro": "Valores resultam em raiz quadrada negativa."}

        rw = math.sqrt(inside_sqrt)

        alerta = False
        mensagem = ""

        if se > (2 * rw):
            alerta = True
            mensagem = "Afastamento excessivo entre gotejadores. A faixa contínua de humidade será rompida, prejudicando as raízes."

        return {
            "rw": round(rw, 4),
            "alerta_faixa_descontinua": alerta,
            "mensagem": mensagem
        }
    def calcular_raio_umedecido(self, alpha, q, ko, se=None):
        """
        Calcula o Raio Umedecido (Rw) para faixa contínua baseado na Equação 26.
        """
        if alpha <= 0 or ko <= 0:
            return {"rw": 0.0}

        termo1 = 4 / ((alpha ** 2) * (math.pi ** 2))
        termo2 = q / (math.pi * ko)
        termo3 = 2 / (alpha * math.pi)

        valor_interno = termo1 + termo2 - termo3

        if valor_interno < 0:
            return {"rw": 0.0}

        rw = math.sqrt(valor_interno)
        rw_arredondado = round(rw, 2)

        resultado = {"rw": rw_arredondado}

        if se is not None:
            if se > 2 * rw_arredondado:
                resultado["alerta"] = "a faixa contínua será rompida"

        return resultado
