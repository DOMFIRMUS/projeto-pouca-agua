# backend/models/irrigacao.py
import math

class CalculadorIrrigacao:
    def __init__(self):
        # Parâmetros agronómicos padrão (Ex: Tomate / Cana-de-açúcar)
        self.umidade_critica = 40.0
        self.umidade_ideal_min = 60.0
        self.umidade_ideal_max = 80.0

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
