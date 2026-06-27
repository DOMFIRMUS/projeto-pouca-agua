const API_BASE_URL = 'http://localhost:5000/api';

const elements = {
    tbody: document.getElementById('culturas-tbody')
};

/**
 * Fetch and display culturas
 */
async function loadCulturas() {
    try {
        const response = await fetch(`${API_BASE_URL}/culturas`);
        if (!response.ok) throw new Error('Erro ao buscar culturas');
        const culturas = await response.json();

        elements.tbody.innerHTML = '';

        if (culturas.length === 0) {
            elements.tbody.innerHTML = '<tr><td colspan="4" class="text-center">Nenhuma cultura cadastrada.</td></tr>';
            return;
        }

        culturas.forEach(cultura => {
            const tr = document.createElement('tr');

            const kcInicial = (cultura.kc_inicial || 0).toFixed(2);
            const kcMedia = (cultura.kc_media || 0).toFixed(2);
            const kcFinal = (cultura.kc_final || 0).toFixed(2);

            const diasInicial = cultura.dias_fase_inicial || 0;
            const diasMeia = cultura.dias_meia_estacao || 0;
            const diasFinal = cultura.dias_fase_final || 0;

            const minCe = (cultura.min_ce || 0).toFixed(1);
            const maxCe = (cultura.max_ce || 0).toFixed(1);

            tr.innerHTML = `
                <td>${cultura.nome}</td>
                <td>${kcInicial} / ${kcMedia} / ${kcFinal}</td>
                <td>${diasInicial} / ${diasMeia} / ${diasFinal}</td>
                <td>${minCe} - ${maxCe} dS/m</td>
            `;
            elements.tbody.appendChild(tr);
        });
    } catch (error) {
        console.error(error);
        elements.tbody.innerHTML = '<tr><td colspan="4" class="text-center text-danger">Erro ao carregar as culturas.</td></tr>';
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', loadCulturas);
