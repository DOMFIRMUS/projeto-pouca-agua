Você é um Engenheiro de Software Full-Stack Sênior encarregado de implementar uma nova feature e corrigir bugs críticos no "Projeto Pouca Água" (uma plataforma de manejo de irrigação para agricultura familiar).

Sua tarefa é dividida em duas frentes: Frontend e Backend.

### 1. Frontend (Implementação baseada em Design)
Crie o código necessário para replicar com exatidão a interface de usuário exibida na imagem fornecida (`48.jpg`).

**Requisitos Técnicos do Frontend:**
- **Stack Tecnológica:** Utilize exclusivamente HTML5 semântico, CSS3 puro e JavaScript puro (Vanilla JS). Não utilize frameworks web como React, Vue ou Angular.
- **Responsividade:** O design deve ser estritamente Mobile-First, focando na usabilidade do agricultor familiar pelo celular.
- **Estilização:** Utilize variáveis globais no pseudo-elemento `:root` do CSS para o controle de paleta de cores, tipografia e espaçamentos (ex: `--bg-color`, `--text-color`, etc.).
- **Fidelidade Visual:** Reproduza o layout, os ícones, os cards de status (como alertas de umidade do solo: Seco, Ideal, Encharcado) e outras métricas visíveis na imagem anexa.
- O código deve ser estruturado e pronto para integrar ao diretório `/frontend` do projeto.

### 2. Backend (Refatoração de Código em Python)
No núcleo agronômico do sistema, há código redundante que precisa ser resolvido.
Acesse o arquivo `backend/models/irrigacao.py` e elimine as duplicações de métodos matemáticos que estão causando dívida técnica.

**Você deve encontrar e unificar/remover as implementações duplicadas dos seguintes métodos:**
1. `calcular_pressao_atual_ea`
2. `calcular_deficit_pressao_vapor`
3. `calcular_eto_blaney_criddle`
4. `calcular_raio_umedecido`

**Regras para o Backend:**
- Avalie as implementações duplicadas de cada função e preserve apenas a versão correta, completa e que atenda às equações originais dos modelos implementados no projeto.
- Certifique-se de manter as assinaturas (parâmetros de entrada e retornos) consistentes para não quebrar outras áreas do sistema (ex: a API em `app.py`).
- Assegure-se de que tolerâncias a erros (como não divisão por zero ou matemática com limites estritos) estejam ativas nas versões que você preservar.
- Após realizar suas modificações em `backend/models/irrigacao.py`, valide as alterações executando os testes da suíte localizados na pasta `backend/tests/` utilizando o comando `python3 -m pytest backend/`.