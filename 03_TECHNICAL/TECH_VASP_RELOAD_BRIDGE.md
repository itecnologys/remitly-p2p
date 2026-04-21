# VASP Bridge: Integração de Recarga de Cartões Locais

Este documento mapeia os provedores e a lógica técnica para a "Ponte" que carrega os cartões de débito locais usando liquidez de stablecoins.

## 1. Provedores de Infraestrutura (VASP Bridges)

Para o "Last Mile" (Última Milha) em moeda fiat, o FLUXUS se integra com VASPs que oferecem Cartão-como-Serviço (CaaS).

### Principais Parceiros Mapeados:
- **Bridge.xyz / Reap.global:** APIs robustas para mover stablecoins diretamente para contas de liquidação bancária que alimentam cartões.
- **Striga / Unlimit:** Focados em Europa e América Latina, oferecem o compliance (KYC) e a emissão de cartões white-label.
- **Kulipa:** Especialista em converter stablecoins para fiat no momento do carregamento de programas de cartões Web3.

---

## 2. A Lógica da Ponte (The Reload Bridge)

O Investidor não carrega o cartão do recebedor manualmente. Ele interage com a **Ponte de Recarga**.

### Fluxo de Carregamento:
1.  **Trigger:** O Smart Contract atesta que o investidor aceitou a ordem e enviou os fundos para a `Escrow_Wallet`.
2.  **Conversion:** A ponte (VASP) liquida o par `USDT/Fiat_Local` usando a liquidez enviada pelo investidor.
3.  **Loading:** A ponte dispara uma chamada de API para o processador de cartões (ex: Visa Direct / Mastercard Send) para carregar o saldo do `CardID` do receptor.
4.  **Proof of Load:** A VASP retorna o ID da transação bancária local, que o FLUXUS processa para gerar o **Minihash Final**.

---

## 3. Estratégia de Spread na Ponte

O pacote de preço ao utilizador final de remessa segue o canônico de precificação **Dominância/Tiered** (`TECH_FLUXUS_PRICING_CANON.md`); esta secção descreve apenas **como** a ponte executa o FX e repassa provas — não redefine o spread total.

A receita do sistema é capturada aqui:
- **Preço de Mercado Real:** O sistema consulta o câmbio atual.
- **Bid do Investidor:** O investidor oferece a taxa que deseja aplicar.
- **Taxa de Gateway:** Uma pequena porcentagem fixa para cobrir os custos de rede (VASP fees e Gas).

**Resultado:** O receptor recebe exatamente o valor acordado em fiat, enquanto o investidor lucra no diferencial de câmbio transparente.
