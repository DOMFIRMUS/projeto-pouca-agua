const API_BASE_URL = 'http://localhost:5000/api';

const elements = {
    tbody: document.getElementById('bancos-tbody'),
    modal: document.getElementById('modal-add-banco'),
    btnAdd: document.getElementById('btn-add-banco'),
    form: document.getElementById('form-banco'),
    closeBtns: document.querySelectorAll('.close-btn, .close-btn-action')
};

// Open Modal
elements.btnAdd.addEventListener('click', () => {
    elements.form.reset();
    elements.modal.style.display = 'flex';
});

// Close Modal
elements.closeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        elements.modal.style.display = 'none';
    });
});

// Close Modal when clicking outside
window.addEventListener('click', (e) => {
    if (e.target === elements.modal) {
        elements.modal.style.display = 'none';
    }
});

/**
 * Fetch and display bancos
 */
async function loadBancos() {
    try {
        const response = await fetch(`${API_BASE_URL}/bancos`);
        if (!response.ok) throw new Error('Erro ao buscar bancos');
        const bancos = await response.json();

        elements.tbody.innerHTML = '';

        if (bancos.length === 0) {
            elements.tbody.innerHTML = '<tr><td colspan="3" class="text-center">Nenhum banco cadastrado.</td></tr>';
            return;
        }

        bancos.forEach(banco => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${banco.nome}</td>
                <td>${banco.taxa_mensal.toFixed(2)}%</td>
                <td>
                    <button class="btn btn-danger btn-sm" onclick="deleteBanco(${banco.id})">Remover</button>
                </td>
            `;
            elements.tbody.appendChild(tr);
        });
    } catch (error) {
        console.error(error);
        elements.tbody.innerHTML = '<tr><td colspan="3" class="text-center text-danger">Erro ao carregar os bancos.</td></tr>';
    }
}

/**
 * Add novo banco
 */
elements.form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const nome = document.getElementById('nome').value;
    const taxa_mensal = document.getElementById('taxa_mensal').value;

    try {
        const response = await fetch(`${API_BASE_URL}/bancos`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ nome, taxa_mensal })
        });

        if (!response.ok) throw new Error('Erro ao salvar banco');

        elements.modal.style.display = 'none';
        elements.form.reset();
        loadBancos();
    } catch (error) {
        console.error(error);
        alert('Erro ao adicionar banco.');
    }
});

/**
 * Delete banco
 */
window.deleteBanco = async function(id) {
    if (!confirm('Tem certeza que deseja remover este banco?')) return;

    try {
        const response = await fetch(`${API_BASE_URL}/bancos/${id}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Erro ao remover banco');

        loadBancos();
    } catch (error) {
        console.error(error);
        alert('Erro ao remover banco.');
    }
};

// Initialize
document.addEventListener('DOMContentLoaded', loadBancos);
