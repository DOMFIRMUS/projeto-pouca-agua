# Prompt para Implementação: Rotina de Cálculo da Evapotranspiração de Referência (ETo)

Você é um engenheiro de software e agrônomo especialista em modelagem de irrigação. Sua tarefa é implementar a "Rotina de cálculo da Evapotranspiração de referência (ETo)" conforme especificado na documentação técnica (Figura 5).

## Objetivo
Criar uma rotina dinâmica (orquestrador/roteador) de cálculo de ETo que avalie as variáveis de entrada disponíveis e direcione o cálculo para o método mais apropriado, seguindo uma ordem de prioridade estrita.

A ETo deve ser recalculada sempre que um novo projeto for iniciado, e seu resultado ficará disponível durante o desenvolvimento do mesmo. Após a obtenção da "Saída: ETO", o fluxo deve seguir para a "Rotina de cálculo da evapotranspiração da cultura - ETc (6)".

## Ordem de Prioridade e Roteamento (Fluxograma)

A seleção do método de cálculo deve seguir a exata sequência de decisões lógicas abaixo:

### 1. Método Penman-Monteith - FAO (Prioridade 1)
*   **Condição:** Avalie se TODAS as variáveis necessárias abaixo estão disponíveis.
*   **Variáveis Necessárias:**
    *   `Tmáx` (Temperatura máxima, °C)
    *   `Tmin` (Temperatura mínima, °C)
    *   `Tmed` (Temperatura média, °C)
    *   `U2` (Velocidade do vento a 2m de altura)
    *   `UR` (Umidade Relativa)
    *   `n` (Insolação/brilho solar)
    *   `Lat` (Latitude)
    *   `Alt` (Altitude, m)
    *   `Data`
*   **Ação (Sim):** Execute o "Cálculo Penman - Monteith - FAO" e retorne a ETo (Saída: ETO).
*   **Ação (Não):** Siga para o método Hargraves - Samani.

### 2. Método Hargraves - Samani (Prioridade 2)
*   **Condição:** Se os dados para Penman-Monteith não estiverem completos, avalie se as variáveis para este método estão disponíveis.
*   **Variáveis Necessárias:**
    *   `Tmáx` (Temperatura máxima, °C)
    *   `Tmin` (Temperatura mínima, °C)
    *   `Tmed` (Temperatura média, °C)
    *   `Lat` (Latitude)
*   **Fórmula (Equação 10):**
    Este método incorpora as temperaturas do ar e a radiação solar recebida no topo da atmosfera (Ra), em que o fator de radiação é função da latitude e do período do ano.
    `ETo = Ra * 0,408 * sqrt(0,0023 * (Tmed + 17,8) * (Tmáx - Tmin))`
    *   **Onde:**
        *   `Tmed`, `Tmáx` e `Tmin` representam, respectivamente, as temperaturas média, máxima e mínima do ar, em °C.
        *   `Ra` – radiação solar no topo da atmosfera (MJ m⁻² d⁻¹), que deve ser obtida via "Tabela 2".
*   **Ação (Sim):** Execute o "Cálculo Hargraves - Samani" usando a equação descrita e retorne a ETo (Saída: ETO).
*   **Ação (Não):** Siga para o método Blanney Criddle - FAO.

### 3. Método Blanney Criddle - FAO (Prioridade 3)
*   **Condição:** Se os dados para os métodos anteriores não estiverem completos, avalie se as variáveis para este método estão disponíveis.
*   **Variáveis Necessárias:**
    *   `Tmáx` (Temperatura máxima, °C)
    *   `Tmin` (Temperatura mínima, °C)
    *   `Tmed` (Temperatura média, °C)
    *   `Ra` (Radiação solar no topo da atmosfera)
    *   `Lat` (Latitude)
*   **Ação (Sim):** Execute o "Cálculo Blanney Criddle - FAO" e retorne a ETo (Saída: ETO).
*   **Ação (Não):** "Sair". Aborte a operação, pois não há dados suficientes para estimar a ETo.

## Saída e Integração
*   A saída de qualquer um dos métodos que for executado com sucesso será o valor da Evapotranspiração de Referência (`Saída: ETO`).
*   Esse valor deverá ser o input direto para a **"Rotina de cálculo da evapotranspiração da cultura – ETc (6)"**.

## Instruções de Implementação
1.  **Função de Roteamento:** Crie uma função central de orquestração (ex: `rotina_selecao_metodo_eto`) que recebe um dicionário ou objeto contendo dados climáticos e avalia as condições dos três métodos estritamente na ordem do fluxograma (Figura 5).
2.  **Validação Dinâmica:** Utilize um sistema robusto para verificar se as variáveis exigidas por cada método não são nulas.
3.  **Implementação de Hargraves-Samani:** Garanta que a raiz quadrada e as constantes (0,408, 0,0023, 17,8) da Equação 10 sejam aplicadas exatamente como na imagem.
4.  **Tratamento de Erros:** A ramificação final "Sair" (quando o método Blanney Criddle também não for aplicável) deve lançar um erro informando que os dados são insuficientes para calcular a ETo em qualquer método.
