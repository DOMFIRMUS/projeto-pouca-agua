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
            r = (v * diametro_m) / 1.01e-6

            if r < 2000:
                f = 64 / r if r > 0 else 0
            elif 2000 <= r < 3000:
                f = 0.04
            else:
                f = 0.316 / (r ** 0.25)

            hf = 8.263e-2 * f * (vazao_acumulada_m3s ** 2 / diametro_m ** 5) * espacamento_m

            # Pressão no emissor atual = pressão do emissor anterior + perda de carga + desnível
            pressao_atual = pressao_anterior + hf + (declividade * espacamento_m)

            if abs(pressao_atual - pressao_ultimo_emissor) > hvar_max:
                break

            comprimento_total += espacamento_m
            pressao_anterior = pressao_atual
            i += 1

        return comprimento_total

    def avaliar_status_solo(self, valor_umidade):
        if valor_umidade < self.umidade_critica:
            return {"status": "Crítico (Seco)", "cor_alerta": "danger", "irrigar": True, "mensagem": "Solo excessivamente seco. Ligue a irrigação."}
        elif self.umidade_critica <= valor_umidade < self.umidade_ideal_min:
            return {"status": "Moderado", "cor_alerta": "warning", "irrigar": True, "mensagem": "A umidade está caindo. Recomenda-se irrigar levemente."}
        elif self.umidade_ideal_min <= valor_umidade <= self.umidade_ideal_max:
            return {"status": "Ideal", "cor_alerta": "success", "irrigar": False, "mensagem": "Solo com umidade perfeita."}
        else:
            return {"status": "Encharcado", "cor_alerta": "info", "irrigar": False, "mensagem": "Solo muito úmido. Evite desperdiçar água."}

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
