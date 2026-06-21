# 💧 Projeto Pouca Água

O **Projeto Pouca Água** é uma plataforma digital desenvolvida para apoiar o agricultor familiar no manejo eficiente da irrigação. Através de uma interface otimizada para celulares e integrada a sensores de baixo custo, o sistema ajuda a economizar água, tempo e energia, garantindo a produtividade da lavoura através de dados precisos.

## 🚀 Funcionalidades Principais (Roadmap)
- **Painel do Agricultor:** Visualização em tempo real do status de umidade do solo (Seco, Ideal, Encharcado).
- **Alerta de Irrigação:** Notificação de quando e quanto irrigar com base no tipo de cultura.
- **Calculadora Hidráulica:** Dimensionamento simplificado de subunidades de irrigação localizada (gotejamento/microaspersão) com base em modelos computacionais científicos.
- **Histórico de Consumo:** Relatórios simples de economia de água.

## 🛠️ Tecnologias Utilizadas
- **Frontend:** HTML5, CSS3 (Mobile-First), JavaScript.
- **Backend:** Python (Flask/FastAPI) para processamento dos dados meteorológicos e equações hidráulicas.
- **Hardware:** Sensores de umidade do solo (Capacitivos) + Microcontrolador ESP32/NodeMCU.

## 📂 Estrutura do Projeto
- `/frontend`: Interface responsiva para o celular do agricultor.
- `/backend`: API de processamento e inteligência agronômica/hidráulica.
- `/iot_sensors`: Código-fonte para leitura e envio dos dados dos sensores de campo.
