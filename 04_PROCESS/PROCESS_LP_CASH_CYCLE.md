# FLUXUS — Protocolo de Ciclo de Caixa e Re-Liquidação (LP Cash Cycle)
**Versão:** 1.0 | **Classificação:** Confidencial — Operacional / LPs

---

## 1. Visão Geral
Este protocolo define os procedimentos técnicos e financeiros para garantir que o **Provedor de Liquidez (LP / Liquidante)** consiga fechar o "Ciclo de Capital" (Capital Loop). O objetivo é garantir que, após executar um payout local em Fiat (ex: PIX), o investidor receba o retorno de seu capital inicial + lucro de volta em sua conta bancária de origem, permitindo a continuidade da operação.

---

## 2. O Ciclo do Capital (The Loop)

O ciclo de vida do capital do liquidante é dividido em quatro fases:

1.  **Funding (Input):** Depósito de Colateral em USDT no Smart Contract do FLUXUS.
2.  **Execution (Payout):** Envio de capital Fiat local (BRL) para o destino final.
3.  **Compensation (Atomic):** Recebimento automático de USDT + Spread no Smart Contract.
4.  **Re-Liquidation (Cash-Out):** Conversão do capital on-chain de volta para Fiat na conta de origem.

---

## 3. Modalidades de Retorno ao Estado Fiat Inicial

Após a confirmação do crédito na conta do destinatário (validada via **Minihash**), o liquidante dispõe de três caminhos para reaver seu capital em Fiat:

### 3.1 Opção A: Auto-Refill (VASP Bridge Integrada)
O modelo recomendado para LPs profissionais. O FLUXUS utiliza APIs de VASPs parceiras (ex: Mercado Bitcoin, Bitso, Bridge.xyz) para automatizar a saída.

- **Gatilho:** Confirmação do estado `SETTLED`.
- **Ação:** O motor FLUXUS dispara uma ordem de venda do USDT recebido na exchange parceira.
- **Resultado:** O valor em BRL é enviado via PIX diretamente para a conta bancária pré-cadastrada do LP.
- **Vantagem:** Latência mínima; o capital volta para o banco em minutos, pronto para a próxima rodada.

### 3.2 Opção B: Arbitragem Reversa (Matching Reverso)
Utiliza a inteligência do motor de matching para evitar taxas de conversão (Gas/Exchange fees).

- **Gatilho:** Existência de uma ordem de remessa no sentido oposto (ex: Europa -> Brasil).
- **Ação:** O motor casa a necessidade do LP (que tem USDT e quer BRL) com a necessidade de um remetente (que tem BRL e quer enviar).
- **Resultado:** O LP "vende" seu lucro on-chain para outro usuário do ecossistema, recebendo o BRL de forma orgânica.
- **Vantagem:** Custo zero de conversão e blindagem fiscal total.

### 3.3 Opção C: Saque Manual (Self-Custody Liquidation)
Dá total soberania ao investidor sobre onde e como liquidar seus ativos.

- **Gatilho:** Solicitação manual de `Withdraw` no painel do Liquidante.
- **Ação:** O Smart Contract libera os fundos do Vault para a carteira externa (external wallet) do LP.
- **Resultado:** O LP realiza a liquidação em sua própria plataforma de preferência (P2P externo, OTC, ou outras Exchanges).
- **Vantagem:** Liberdade total; permite ao LP gerenciar sua própria estratégia de exposição cambial.

---

## 4. Procedimentos de Segurança e Conformidade

Para garantir a segurança do "Caminho de Volta", o protocolo exige:

1.  **Whitelisting de Contas:** O capital Fiat só pode retornar para contas de mesma titularidade (Same-Name Account) validadas no KYC inicial.
2.  **Auditoria via Minihash:** Cada etapa da re-liquidação gera um hash vinculado à transação original, permitindo total rastreabilidade para fins de Imposto de Renda (Ganho de Capital).
3.  **Limite de Exposição:** O motor de matching bloqueia novas participações se o LP atingir um limite de "Capital em Trânsito" sem a devida conclusão do ciclo de re-liquidação anterior.

---

## 5. Matriz de Estados de Re-Liquidação

| Estado | Descrição |
| :--- | :--- |
| **`PENDING_REFILL`** | USDT+Lucro liberados no contrato, aguardando gateway fiat. |
| **`VASP_PROCESSING`** | Ordem de venda executada na exchange parceira. |
| **`BANK_TRANSFER`** | PIX/TED disparado para a conta do LP. |
| **`CYCLE_COMPLETED`** | Capital inicial + Lucro confirmados na conta de origem. |

---

*Documento integrante da Arquitetura FLUXUS Core.*
*Emitido por Antigravity — Engenharia Financeira.*
