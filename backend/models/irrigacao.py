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
