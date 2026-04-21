# FLUXUS Remit: Tese de Negócio e Estratégia de Spread

> **Fonte da verdade (precificação):** `03_TECHNICAL/TECH_FLUXUS_PRICING_CANON.md`.

## 1. Visão Geral
O **FLUXUS Remit** expande a infraestrutura do NEXUS de um Marketplace de Crédito para um **Hub de Liquidez P2P Cross-Border**. A tese central é que as remessas internacionais não precisam depender de bancos correspondentes lentos, mas sim de uma rede descentralizada de investidores locais que provêem liquidez imediata em troca de spreads competitivos.

## 2. O Papel do Investidor (Liquidity Provider - LP)
No modelo FLUXUS, o investidor (Aplicante) deixa de apenas "emprestar" para "garantir liquidez".
- **Aporte em Corredores:** O investidor aloca capital em corredores específicos (ex: USD/BRL).
- **Remuneração:** Em vez de juros mensais, ele ganha uma fatia do **Spread de Câmbio** e taxas de transação em tempo real.
- **Liquidação Instantânea:** O capital do investidor fica em **Escrow** para garantir que, assim que um remetente envia USD no exterior, o destinatário receba BRL instantaneamente via PIX.

## 3. Estratégia de Spread e Monetização
A estratégia oficial é **Dominância/Tiered**: o spread varia por **faixa de volume** (escada) e por corredor, mantendo transparência (PTAX + taxas explícitas) e competitividade estrutural. A Wise é usada como **benchmark de validação** e auditoria, não como “driver” de precificação.

| Componente | Referência sobre notional | Destino |
| :--- | :--- | :--- |
| **Yield LP (Exchanger)** | Variável (share do spread) | Ganho do Provedor de Liquidez |
| **Trilho VASP / local** | Variável (fees do trilho) | Custódia, compliance e saída fiat/cartão |
| **Orquestração FLUXUS** | Variável (share do spread) | Software, Macro Hash, matching e resiliência |

Reservas de risco, prémios de velocidade ou incentivos de cold start **repartem** estas fatias ou reduzem temporariamente a fatia da plataforma — não acrescentam um segundo spread total em narrativa de produto.

## 4. Remuneração do Board e da Plataforma
Diferente dos ganhos do investidor, o lucro da plataforma (o "Board") é focado no volume e na gestão da infraestrutura:

1. **Orchestration fee (dentro do spread):** A parcela de plataforma sobre o notional alimenta a operação tecnológica e conformidade; detalhe matemático no canónico de precificação.
2. **Transaction Service Fees:** Taxa operacional fixa por remessa **quando aplicável ao corredor** (ex.: US$ 1,99–2,00) para cobrir custos marginais de KYC, AML e processamento — **adicional** ao spread, não substituto.
3. **Management Fee sobre Pools:** Taxa de administração anual (AUM) sobre o capital alocado pelos investidores nos corredores de liquidez, remunerando a gestão de risco e rebalanceamento por IA.
4. **Float & Treasury:** Ganho financeiro sobre o capital em trânsito (dinheiro parado em contas de liquidação antes de ser disparado para o destino).

### Variáveis de Ajuste:
- **Volatilidade:** Em moedas de alta flutuação, o leilão pode priorizar LPs com melhor preço; o **teto** comunicado ao remetente permanece alinhado ao canónico salvo excepção explícita no produto.
- **Velocidade:** Remessas "Instantâneas" (liquidação em segundos) podem usar prémios pagos **dentro** das fatias do spread, sem alterar o referencial de documentação.

## 5. Corredores Prioritários
1. **Core Corridor (USD → BRL):** Foco em brasileiros residentes nos EUA.
2. **LatAm Expansion (BRL ↔ MXN / COP):** Foco em comércio regional P2P.
3. **Stablecoin Corridor (USDC/USDT → BRL):** Liquidação de ativos digitais para economia real.

## 6. Diferenciais Competitivos
- **Auditabilidade Extrema:** Cada remessa gera um bloco no **Macro Hash**, permitindo que o investidor e o órgão regulador vejam o caminho exato do dinheiro.
- **Custo Zero de Intermediário:** Ao usar liquidez P2P local, eliminamos as taxas de SWIFT e bancos correspondentes.
- **Yield Superior:** Para o investidor, o giro rápido das remessas pode gerar um APY (Retorno Anual) superior ao do crédito tradicional, com menor risco de inadimplência (já que o dinheiro não é "emprestado" por meses, mas sim "trocado" em segundos).
