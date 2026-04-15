# Sessão 02: Estratégia FLUXUS Remit & Global PIX
**Data:** 13 de Abril de 2026
**Status:** Planejamento Estratégico e Arquitetura de Redirecionamento

---

## 1. Rebranding e Identidade
Nesta sessão, decidimos pivotar a marca original (NEXUS) para uma nova identidade focada em fluxo e remessas globais.

- **Novo Nome:** **FLUXUS** (by Remitly).
- **Conceito:** "Família Nexus", mantendo o sufixo "-US", mas focando em fluidez (Flux).
- **Identidade Visual (Electric Liquid):**
  - Primária: Indigo Elétrico (`#6366F1`)
  - Fluxo: Cyan (`#06B6D4`)
  - Acento: Rose (`#F43F5E`)
  - Fundo: Slate Dark (`#0F172A`)

## 2. Tese de Negócio: Remessa P2P
A plataforma evolui de um marketplace de crédito para um hub de liquidez cross-border.

- **Provedores de Liquidez (LP):** O investidor (Ex-Aplicante) agora aloca capital em corredores de câmbio para lucrar com spreads.
- **Spread P2P:** Dividido entre o lucro do investidor e a rentabilidade da plataforma (Board).
- **Modelo de Rendimento:** Baseado em frequência de transação e arbitragem cambial.

## 3. Arquitetura Técnica: Motor Global PIX
O "Graal" do projeto é a criação de um PIX Global via USDT.

- **Camada de Transporte:** **USDT na rede Polygon** (Custo por transação: R$ 0,01 - R$ 0,05).
- **Gatilho (Global QR Code):** Padrão dinâmico baseado em EMV QRCPS (mesmo do PIX) que permite disparar pagamentos em USDT a partir de uma solicitação de moeda local.
- **Last Mile Engine:** 
  - Brasil: API PIX nativa.
  - Global: Visa Direct / Mastercard Send (Push-to-card) e Mobile Money (M-Pesa).
- **Auditabilidade (Macro Hash):** Integração total dos TXIDs da blockchain no ledger de auditoria L1→L5.

## 4. Remuneração do Board (Plataforma)
Definimos 4 pilares de receita para a sustentabilidade da operação:
1. **Retention Spread:** % fixa sobre o diferencial cambial intermediado.
2. **Transaction Fees:** Taxa fixa de serviço por remessa (ex: US$ 1.99).
3. **Management Fees (AUM):** Taxa sobre a gestão dos pools de liquidez dos investidores.
4. **Float:** Ganho sobre o capital em trânsito (Cash management).

## 5. Mapeamento de Barreiras de Liquidação
- **USA:** Challenge de fragmentação bancária. Solução via Push-to-card.
- **Brasil:** Cenário ideal via PIX.
- **África/Ásia:** Foco em Mobile Money devido à baixa bancarização.
- **Fatores 2026:** Nova taxa de 1% sobre remessas físicas no USA favorece o modelo digital completo do FLUXUS.

---
**Notas Adicionais:**
Todo o detalhamento estratégico e técnico desta sessão foi arquivado na pasta `Antigravity/` do projeto `remitly-p2p`.
**Próximos Passos Sugeridos:** Adaptação dos protótipos visuais e implementação do Blockchain Listener experimental.
---
*Log gerado automaticamente pela Inteligência Antigravity.*
