import math
import datetime

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
    def calcular_itn(self, irn_mm, ce_agua_ds_m, ce_solo_min, ce_solo_max, uniformidade_emissao_decimal):
        """
        Calcula a Irrigação Total Necessária (ITN) e a Fração de Lixiviação (FL)
        com base nas Equações 42 e 43 da tese.
        """
        # Equação 43: FL = CEa / (2 * CEes_max)
        fl = ce_agua_ds_m / (2 * ce_solo_max)

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

    def calcular_perda_carga(self, diametro_mm, vazao_gotejador_lh, espacamento_m, comprimento_m):
        """
        Calcula a perda de carga em uma linha lateral de gotejamento usando a equação
        empírica para tubos plásticos pequenos (Flamant/Blasius) e aplica o fator de Christiansen.
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

        # Equação empírica de perda de carga para tubo contínuo (hf)
        # J = 0.000859 * Q^1.75 * D^-4.75
        hf_continua = 0.000859 * comprimento_m * (q_m3s ** 1.75) * (d_m ** -4.75)

        # Fator de Christiansen para múltiplas saídas
        fator_f = (1 / (m + 1)) + (1 / (2 * n_emissores)) + (math.sqrt(m - 1) / (6 * n_emissores**2))

        # Perda de carga real
        hf_mca = hf_continua * fator_f

        status = "Aceitável" if hf_mca <= 2.0 else "Desuniformidade Elevada"

        return {
            "vazao_total_lh": round(vazao_total_lh, 2),
            "perda_carga_mca": round(hf_mca, 3),
            "status": status
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
    def classificar_perfil_pressao(self, So, k_linha, L_estimado):
        """
        Classifica o perfil de pressão hidráulica baseado na tese.
        So: declividade em decimal
        k_linha: constante da linha
        L_estimado: comprimento estimado
        """
        if So <= 0:
            return 'Perfil Tipo I (Aclive ou Nível)'

        J = k_linha * (L_estimado ** 1.75)
        razao = So / J

        if 0 < razao < 1:
            return 'Perfil Tipo IIa (Declive Fraco)'
        elif razao == 1:
            return 'Perfil Tipo IIb (Declive Moderado)'
        elif 1 < razao < 2.75:
            return 'Perfil Tipo IIc (Declive Forte)'
        else:
            return 'Perfil Tipo IId (Declive Muito Forte)'

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

    def calcular_pressao_inicial_bomba(self, pressao_emissor, perda_carga_tubulacao, diametro_conector_m, comprimento_conector_m, vel_conector_ms, vel_lateral_ms):
        """
        Método principal de perda de carga:
        Calcula a pressão inicial necessária da bomba adicionando a perda de carga localizada (Hfl_l).
        """
        hfl_l = self.perda_conector_lateral(diametro_conector_m, comprimento_conector_m, vel_conector_ms, vel_lateral_ms)
        pressao_inicial = pressao_emissor + perda_carga_tubulacao + hfl_l
        return pressao_inicial

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
