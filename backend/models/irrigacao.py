# backend/models/irrigacao.py

class CalculadorIrrigacao:
    def __init__(self):
        # Parâmetros padrão simulados (Podem ser customizados por cultura no futuro)
        self.umidade_critica = 40.0  # Abaixo disso, o solo está muito seco
        self.umidade_ideal_min = 60.0
        self.umidade_ideal_max = 80.0

    def avaliar_status_solo(self, valor_umidade):
        """
        Avalia o percentual de umidade do solo e retorna o status e a ação recomendada.
        """
        if valor_umidade < self.umidade_critica:
            return {
                "status": "Crítico (Seco)",
                "cor_alerta": "danger",
                "irrigar": True,
                "mensagem": "Solo excessivamente seco. Ligue a irrigação imediatamente."
            }
        elif self.umidade_critica <= valor_umidade < self.umidade_ideal_min:
            return {
                "status": "Moderado (Necessita Atenção)",
                "cor_alerta": "warning",
                "irrigar": True,
                "mensagem": "A umidade está caindo. Recomenda-se irrigar levemente."
            }
        elif self.umidade_ideal_min <= valor_umidade <= self.umidade_ideal_max:
            return {
                "status": "Ideal",
                "cor_alerta": "success",
                "irrigar": False,
                "mensagem": "Solo com umidade perfeita para o desenvolvimento da lavoura."
            }
        else:
            return {
                "status": "Encharcado",
                "cor_alerta": "info",
                "irrigar": False,
                "mensagem": "Solo muito úmido. Evite irrigar para não desperdiçar água e sufocar as raízes."
            }

    def calcular_tempo_irrigacao(self, umidade_atual, vazao_emissor_lh=2.0, espacamento_m=0.3):
        """
        Calcula uma estimativa de tempo de irrigação necessário (em minutos).
        Pode ser expandido usando as fórmulas de lâmina líquida da tese.
        """
        if umidade_atual >= self.umidade_ideal_min:
            return 0

        # Simulação simples: quanto mais seco, mais tempo precisa para atingir a umidade ideal
        deficit = self.umidade_ideal_min - umidade_atual

        # Ajuste arbitrário baseado na vazão para gerar um tempo funcional
        tempo_minutos = (deficit * 1.5) / (vazao_emissor_lh * espacamento_m)
        return round(max(tempo_minutos, 5), 1) # Mínimo de 5 minutos se precisar irrigar
