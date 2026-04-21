# 🧬 FLUXUS: Architecture Operational Blueprint (Premium UI Edition)

Este documento consolida a visão estratégica, visual e operacional da plataforma FLUXUS, detalhando a interface de usuário (UI) e a experiência (UX) que sustentam a operação institucional.

---

## 1. 📂 Estrutura do Projeto e Filosofia Modular

*(Seção mantida conforme o blueprint original: foco na organização de pastas e links do Obsidian)*.

---

## 2. 🎭 Jornada Operacional: Detalhamento de UI/UX

A experiência do usuário no FLUXUS é desenhada para remover a carga cognitiva do mundo Web3, utilizando uma interface **"Invisible Blockchain"**:

- **Interface de Onboarding (Privy Integration)**: 
    - Apresentação de uma **Modal Minimalista** balanceada com transparência vítrea (Glassmorphism).
    - **UX de Autenticação**: O usuário vê apenas campos de Login Social (Google/Apple). Ao autenticar, uma animação de "Pulsing Ring" indica a criação síncrona da **Embedded Wallet**.
- **Dashboard de Identidade & Liveness**:
    - **UI de Captura**: Um frame circular com feedback de cor dinâmica (Ciano para "Posicione o rosto", Verde para "Capturado"). 
    - **Visualização de Status**: Indicadores de tier de conta (Bronze, Silver, Gold) exibidos como **Badges Metálicos** com efeitos de reflexo CSS.

---

## 3. ⚙️ Motor de Fila e Matching: O "Matching Cockpit"

O coração visual da plataforma é onde o investidor (LP) e o administrador monitoram a liquidez:

- **Premium Queue Visualizer**:
    - Uma fila horizontal de **Nós Circulares (Nodes)** representando os LPs ativos.
    - **Animação de Pulso**: O nó do usuário atual brilha em Ciano Elétrico com uma sombra projetada (Drop-shadow) que pulsa em sincronia com os blocos da rede.
    - **Interface de Leilão (Bidding UI)**: Cards compactos que mostram "Oportunidades de Giro" com um **Countdown circular** de 5 segundos para o fechamento do leilão cego.
- **Feedback de Resultado**: Quando um match é selado, o card de transação expande com uma transição suave, revelando o **Minihash** e o link para o explorador de blocos.

---

## 4. 🧮 Contabilidade Síncrona: O Dashboard DRE 360

A interface financeira é baseada no conceito de **Bento Box Design**, organizando métricas complexas em blocos intuitivos:

- **Bento Boxes de Capital**:
    - **Card de Capital Principal**: Tipografia negrito em destaque com contador animado (CountUp.js) que atualiza o saldo a cada lucro de milissegundo.
    - **Gráfico de Yield**: Sparklines (gráficos de linha miniatura) integrados ao card para mostrar a tendência de lucro das últimas 24h.
- **Tabela de Divisão de Spread**:
    - Uma tabela com linhas alternadas e hover highlight.
    - **Pílulas de Dados (Data Pills)**: Indicadores coloridos para taxas (Vermelho para Gas/Trilho, Ouro para Orchestration Fee, Verde para Net Profit).
- **Indicador de Governança Fiscal**:
    - Uma **Barra de Progresso (Progress Bar)** que preenche conforme o "Giro Mensal" se aproxima do limite de isenção de R$ 35k. A cor muda gradualmente de Verde para Vermelho Alerta quando o limite é excedido.

---

## 5. ⚓ Visão de Hashes: O Audit Terminal

Para o auditor e o regulador, a UI assume um tom mais técnico e autoritário:

- **Terminal de Auditoria Real-Time**:
    - Fundo escuro (`#0a0a0a`) com fontes mono-espaçadas semelhantes a IDEs de programação.
    - **Cascata de Hashes**: Uma visualização em stream onde os **Minihashes** descem pela tela. Clicar em um hash abre um **Side Drawer** (gaveta lateral) com o JSON completo da transação.
- **Visualizador de Macrohash**:
    - Um componente centralizado que exibe a "Âncora Hierárquica" da hora atual, conectando visualmente (via linhas de conexão SVG) todos os minihashes daquele período ao hash mestre.

---

## 6. 👤 Herculean KYC: O Dossiê de Entidade

A gestão de 30 mil entidades é resolvida através de uma interface de busca hiper-rápida e perfis detalhados:

- **Entity Profile View**:
    - **Dossiê Digital**: Uma folha visual que organiza: Nome, Tax ID (formatado por país), Bank Routing e Histórico de Risco.
    - **Risk Heatmap**: Um gradiente que mostra visualmente a "temperatura" de risco daquela entidade baseado em transações anteriores.
- **Interface de Cadastro**: Formulários inteligentes que validam o formato do documento (CPF, SSN, NIF) síncronamente enquanto o usuário digita.

---

## 7. 💳 Gestão de Cards: A Wallet de Varejo

O dashboard do recebedor é focado em utilidade imediata:

- **Cartão Virtual Dinâmico**:
    - Um componente de cartão 3D (estilo Apple Card) que gira ao ser tocado.
    - **Segurança Visual**: Os números do cartão permanecem ocultos por um efeito de "Blur" (desfoque) até que o usuário performe a autenticação biométrica (FaceID visual simulado na interface).
- **Extrato de Débito JIT**: Lista de transações que mostra o ícone do estabelecimento comercial (Merchant Logo) e a conversão exata feita no momento da compra.

---

## 8. 🌐 RAMP On/Off: Widget de Conversão

A porta de entrada de fiat é tratada como um componente "embedded":

- **Liquidity Widget**:
    - Interface de dois campos (Input Fiat / Output Crypto) com atualização de cotação a cada 10 segundos.
    - **Status de Confirmação**: Uma linha do tempo visual que mostra: `Captura Fiat -> Verificação AML -> Entrega na Carteira`. Cada passo acende com um brilho neon ao ser concluído.

---

## 9. 📊 Relatórios Consolidados: Executive View

Relatórios gerados em PDF ou exibidos em tela para investidores:

- **Infográficos Executivos**:
    - Uso intensivo de **Donut Charts** para mostrar a dominância de corredores (ex: Dubai -> Paquistão).
    - **Tabelas de Auditoria Externa**: Colunas com Green Checkmarks verificando que cada transação do relatório possui um Macrohash válido on-chain.

---

## 10. 💡 Conclusão: A Unicidade da UI FLUXUS

A interface visual do FLUXUS não é cosmética; ela é a **camada de prova** da eficiência do protocolo. Ao utilizar componentes de design premium (Bento Boxes, Glassmorphism, e animações de estado síncronas), a plataforma transforma dados complexos de blockchain e contabilidade em uma ferramenta poderosa de gestão financeira institucional.

---
*Blueprint expandido por Antigravity — FLUXUS UX & Architecture Team.*
