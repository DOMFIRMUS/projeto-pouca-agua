// Configurações
const API_BASE_URL = 'http://localhost:5000/api';
const REFRESH_INTERVAL = 30000; // 30 segundos

// Elementos do DOM
const elements = {
    statusCard: document.getElementById('status-card'),
    currentMoisture: document.getElementById('current-moisture'),
    currentStatus: document.getElementById('current-status'),
    lastUpdate: document.getElementById('last-update'),
    irrigationMinutes: document.getElementById('irrigation-minutes'),
    dataEto: document.getElementById('data-eto'),
    dataCad: document.getElementById('data-cad'),
    dataIrn: document.getElementById('data-irn'),
    historyList: document.getElementById('history-list'),
    pressaoChart: document.getElementById('pressaoChart')
};

// Variável para armazenar a instância do gráfico de pressão
let graficoPressaoInstance = null;

/**
 * Mapeia o status retornado pela API para as classes CSS
 */
function getStatusClass(status) {
    if (!status) return 'status-unknown';

    switch(status.toLowerCase()) {
        case 'ideal': return 'status-ideal';
        case 'moderado': return 'status-moderate';
        case 'crítico':
        case 'critico': return 'status-critical';
        default: return 'status-unknown';
    }
}

/**
 * Mapeia o status para as classes do histórico
 */
function getHistoryStatusClass(status) {
    if (!status) return '';

    switch(status.toLowerCase()) {
        case 'ideal': return 'hist-ideal';
        case 'moderado': return 'hist-moderate';
        case 'crítico':
        case 'critico': return 'hist-critical';
        default: return '';
    }
}

/**
 * Atualiza o painel principal com os dados de status atuais
 */
function updateStatusPanel(data) {
    if (!data) return;

    // Atualizar UI
    elements.currentMoisture.textContent = data.umidade_atual !== null ? data.umidade_atual : '--';
    elements.currentStatus.textContent = data.status_solo || data.status || 'Desconhecido';

    // Formatar data
    if (data.timestamp) {
        const date = new Date(data.timestamp);
        elements.lastUpdate.textContent = date.toLocaleTimeString('pt-BR');
    } else {
        elements.lastUpdate.textContent = new Date().toLocaleTimeString('pt-BR');
    }

    // Atualizar classes de cor
    elements.statusCard.className = 'card status-card ' + getStatusClass(data.status_solo || data.status);

    // Atualizar informações de irrigação
    if (data.metricas_tese && data.metricas_tese.tempo_irrigacao_calculado_minutos !== undefined) {
        elements.irrigationMinutes.textContent = data.metricas_tese.tempo_irrigacao_calculado_minutos.toFixed(1);
    } else if (data.tempo_irrigacao_minutos !== undefined && data.tempo_irrigacao_minutos !== null) {
        elements.irrigationMinutes.textContent = data.tempo_irrigacao_minutos;
    } else {
        elements.irrigationMinutes.textContent = '--';
    }

    // Atualizar dados da tese
    if (data.metricas_tese) {
        elements.dataEto.textContent = data.metricas_tese.evapotranspiracao_referencia_mm_dia || '--';
        elements.dataCad.textContent = data.metricas_tese.capacidade_agua_disponivel_solo_mm || '--';
        elements.dataIrn.textContent = data.metricas_tese.irrigacao_real_necessaria_max_mm || '--';
    } else if (data.dados_tese) {
        elements.dataEto.textContent = data.dados_tese.ETo || '--';
        elements.dataCad.textContent = data.dados_tese.CAD || '--';
        elements.dataIrn.textContent = data.dados_tese.IRN || '--';
    }
}

/**
 * Atualiza a lista de histórico
 */
function updateHistoryList(historico) {
    if (!historico || historico.length === 0) {
        elements.historyList.innerHTML = '<li>Nenhum dado histórico disponível.</li>';
        return;
    }

    elements.historyList.innerHTML = '';

    historico.forEach(item => {
        const li = document.createElement('li');

        const date = new Date(item.timestamp);
        const timeString = date.toLocaleTimeString('pt-BR', {hour: '2-digit', minute:'2-digit'});

        const statusClass = getHistoryStatusClass(item.status);

        li.innerHTML = `
            <span class="history-time">${timeString}</span>
            <span class="history-moisture">${item.umidade}%</span>
            <span class="history-status ${statusClass}">${item.status}</span>
        `;

        elements.historyList.appendChild(li);
    });
}

/**
 * Busca o status atual da API
 */
async function fetchStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/status`);
        if (!response.ok) throw new Error('Erro na rede');
        const data = await response.json();
        updateStatusPanel(data);
    } catch (error) {
        console.error('Erro ao buscar status:', error);
        elements.currentStatus.textContent = 'Erro de conexão';
    }
}

/**
 * Busca o histórico da API
 */
async function fetchHistory() {
    try {
        const response = await fetch(`${API_BASE_URL}/historico`);
        if (!response.ok) throw new Error('Erro na rede');
        const data = await response.json();
        updateHistoryList(data);
    } catch (error) {
        console.error('Erro ao buscar histórico:', error);
        elements.historyList.innerHTML = '<li>Erro ao carregar histórico.</li>';
    }
}

/**
 * Desenha o Gráfico de Perfil de Pressão Hidráulica
 * @param {Array} dadosPressao - Array de objetos com {x: comprimento, y: pressao}
 */
function desenharGraficoPressao(dadosPressao) {
    if (!elements.pressaoChart || !dadosPressao || dadosPressao.length === 0) return;

    // Destruir gráfico anterior se existir
    if (graficoPressaoInstance) {
        graficoPressaoInstance.destroy();
    }

    const pressaoInicial = dadosPressao[0].y;
    const pressaoFinal = dadosPressao[dadosPressao.length - 1].y;

    let corLinha = 'green';
    if (pressaoFinal <= pressaoInicial * 0.8) {
        corLinha = 'red'; // Perfil Tipo I crítico
    } else if (pressaoFinal > pressaoInicial) {
        corLinha = 'blue'; // Perfil Tipo II em declive
    }

    const ctx = elements.pressaoChart.getContext('2d');
    graficoPressaoInstance = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Perfil de Pressão',
                data: dadosPressao,
                borderColor: corLinha,
                backgroundColor: corLinha,
                borderWidth: 2,
                fill: false,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: 'linear',
                    title: {
                        display: true,
                        text: 'Comprimento da Linha (m)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Pressão (mca)'
                    }
                }
            }
        }
    });
}

/**
 * Atualiza todos os dados
 */
function refreshData() {
    fetchStatus();
    fetchHistory();

    // Mockup para demonstração do gráfico de pressão (como não temos endpoint específico na API original ainda)
    const mockDadosPressao = [
        { x: 0, y: 10 },
        { x: 10, y: 9.5 },
        { x: 20, y: 8.8 },
        { x: 30, y: 8.0 },
        { x: 40, y: 7.5 } // Queda de mais de 20%, deve ficar vermelho
    ];
    desenharGraficoPressao(mockDadosPressao);
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    refreshData();
    setInterval(refreshData, REFRESH_INTERVAL);
});