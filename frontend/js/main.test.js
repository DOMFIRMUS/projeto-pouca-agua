const fs = require('fs');
const path = require('path');

describe('main.js tests', () => {
    let originalFetch;
    let originalConsoleError;

    beforeEach(() => {
        document.body.innerHTML = `
            <div id="status-card"></div>
            <div id="current-moisture"></div>
            <div id="current-status"></div>
            <div id="last-update"></div>
            <div id="irrigation-minutes"></div>
            <div id="data-eto"></div>
            <div id="data-cad"></div>
            <div id="data-irn"></div>
            <ul id="history-list"></ul>
            <canvas id="pressaoChart"></canvas>
        `;

        // Save original global objects
        originalFetch = global.fetch;
        originalConsoleError = console.error;
    });

    afterEach(() => {
        // Restore globals
        global.fetch = originalFetch;
        console.error = originalConsoleError;
        jest.restoreAllMocks();
    });

    test('fetchStatus handles network error (response not ok)', async () => {
        const scriptCode = fs.readFileSync(path.resolve(__dirname, 'main.js'), 'utf8');

        // Mock fetch to simulate network error
        global.fetch = jest.fn(() =>
            Promise.resolve({
                ok: false,
                status: 500
            })
        );

        // Mock console.error
        console.error = jest.fn();

        // Eval script to load functions into global scope
        eval(scriptCode);

        // Call the function
        await fetchStatus();

        // Verify the DOM update
        expect(document.getElementById('current-status').textContent).toBe('Erro de conexão');

        // Verify console.error was called with the right arguments
        expect(console.error).toHaveBeenCalledWith('Erro ao buscar status:', expect.any(Error));
        expect(global.fetch).toHaveBeenCalledWith('http://localhost:5000/api/status');
    });

    test('fetchStatus handles thrown fetch error (e.g., DNS error)', async () => {
        const scriptCode = fs.readFileSync(path.resolve(__dirname, 'main.js'), 'utf8');

        const fetchError = new TypeError('Failed to fetch');
        global.fetch = jest.fn(() => Promise.reject(fetchError));

        console.error = jest.fn();

        eval(scriptCode);

        await fetchStatus();

        expect(document.getElementById('current-status').textContent).toBe('Erro de conexão');
        expect(console.error).toHaveBeenCalledWith('Erro ao buscar status:', fetchError);
    });

    test('fetchStatus updates UI on successful response', async () => {
        const scriptCode = fs.readFileSync(path.resolve(__dirname, 'main.js'), 'utf8');

        const mockData = {
            status_solo: 'ideal',
            umidade_atual: 45,
            timestamp: new Date().toISOString(),
            metricas_tese: {
                tempo_irrigacao_calculado_minutos: 15.5
            }
        };

        global.fetch = jest.fn(() =>
            Promise.resolve({
                ok: true,
                json: () => Promise.resolve(mockData)
            })
        );

        eval(scriptCode);

        await fetchStatus();

        expect(document.getElementById('current-status').textContent).toBe('ideal');
        expect(document.getElementById('current-moisture').textContent).toBe('45');
        expect(document.getElementById('irrigation-minutes').textContent).toBe('15.5');
    });
});
