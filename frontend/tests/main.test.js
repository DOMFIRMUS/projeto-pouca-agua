// Test environment setup
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

// Extract functions to be tested and make them available
// Note: Normally we'd use modules, but main.js is written as a browser script
const fs = require('fs');
const path = require('path');
const mainJsCode = fs.readFileSync(path.resolve(__dirname, '../js/main.js'), 'utf8');

// Use eval to execute main.js in the current context so we can test its functions
// We have to mock fetch before evaluating
global.fetch = jest.fn();
// Mock Chart.js
global.Chart = jest.fn().mockImplementation(() => ({
    destroy: jest.fn()
}));

eval(mainJsCode);

describe('getStatusClass', () => {
    it('should return status-unknown for falsy values', () => {
        expect(getStatusClass('')).toBe('status-unknown');
        expect(getStatusClass(null)).toBe('status-unknown');
        expect(getStatusClass(undefined)).toBe('status-unknown');
        expect(getStatusClass(false)).toBe('status-unknown');
    });

    it('should return status-ideal for ideal status', () => {
        expect(getStatusClass('ideal')).toBe('status-ideal');
        expect(getStatusClass('Ideal')).toBe('status-ideal');
        expect(getStatusClass('IDEAL')).toBe('status-ideal');
    });

    it('should return status-moderate for moderado status', () => {
        expect(getStatusClass('moderado')).toBe('status-moderate');
        expect(getStatusClass('Moderado')).toBe('status-moderate');
        expect(getStatusClass('MODERADO')).toBe('status-moderate');
    });

    it('should return status-critical for critico/crítico status', () => {
        expect(getStatusClass('critico')).toBe('status-critical');
        expect(getStatusClass('crítico')).toBe('status-critical');
        expect(getStatusClass('Critico')).toBe('status-critical');
        expect(getStatusClass('Crítico')).toBe('status-critical');
        expect(getStatusClass('CRITICO')).toBe('status-critical');
        expect(getStatusClass('CRÍTICO')).toBe('status-critical');
    });

    it('should return status-unknown for unrecognized status', () => {
        expect(getStatusClass('desconhecido')).toBe('status-unknown');
        expect(getStatusClass('bom')).toBe('status-unknown');
        expect(getStatusClass('ruim')).toBe('status-unknown');
        expect(getStatusClass('123')).toBe('status-unknown');
    });
});
