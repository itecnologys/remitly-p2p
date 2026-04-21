# FLUXUS — Protocolo Técnico do Matching Engine
**Versão:** 1.0 | **Classificação:** Confidencial — Uso Interno / Due Diligence

> **Parâmetros comerciais de referência (spread remessa):** `TECH_FLUXUS_PRICING_CANON.md` — política Dominância/Tiered. Os exemplos JSON abaixo usam `0.012` como teto de spread para cobrir o pior caso do varejo na escada.

---

## 1. Visão Geral e Escopo

O **Matching Engine** é o núcleo algorítmico e a Propriedade Intelectual (IP) central do protocolo FLUXUS. Ele é um motor de orquestração síncrono, construído internamente (In-House), responsável por casar, em tempo real, uma **Ordem de Remessa** com um **Provedor de Liquidez** (Exchanger).

O protocolo FLUXUS é **Chain-Agnostic**, projetado para rodar sobre infraestruturas de alta performance (Solana) ou de alta compatibilidade institucional (Polygon), utilizando o sistema de **Micro-hash** como garantia de integridade entre o mundo on-chain e o payout off-chain.

Este documento especifica:
- A estrutura de dados dos ativos proprietários
- O algoritmo de matching e critérios de scoring (Elegance Function)
- O sistema de Micro-hash e conciliação atômica
- A comparação de performance entre trilhos (Solana vs Polygon)
- As APIs e a soberania tecnológica do motor

---

## 2. Objetos Core

### 2.1 Objeto: `RemittanceOrder`
Criado pelo Sender no momento da confirmação da remessa.

```json
{
  "order_id": "uuid-v4",
  "created_at": "timestamp_unix_ms",
  "sender_wallet": "address_hex_or_base58",
  "source_currency": "AED",
  "source_amount": 500.00,
  "target_currency": "PKR",
  "target_country": "PK",
  "destination_type": "bank_transfer | card_load | mobile_wallet",
  "destination_identifier": "hashed_iban_or_phone",
  "max_spread_accepted": 0.012,
  "micro_hash": "keccak256(order_id + amount + destination + salt)",
  "settlement_rail": "SOLANA | POLYGON",
  "status": "REQUESTED"
}
```

**Campo-chave:** `micro_hash` — Identificador atômico gerado no frontend. Ele âncora os termos da transação e serve como a "chave primária" para a conciliação fiscal e o payout local.

---

### 2.2 Objeto: `ExchangerProfile`
Cadastro on-chain do provedor de liquidez.

```json
{
  "exchanger_id": "uuid-v4",
  "wallet_address": "address_hex_or_base58",
  "covered_corridors": ["US->BR", "AE->PK", "GB->NG"],
  "available_collateral_usdt": 15000.00,
  "locked_collateral_usdt": 3200.00,
  "reputation_score": 847,
  "settlement_capabilities": ["SOLANA", "POLYGON", "PIX", "SEPA"],
  "avg_settlement_time_seconds": 92,
  "auto_bid_config": {
    "max_volume_per_order": 2000.00,
    "min_spread_threshold": 0.005
  }
}
```

**Campo-chave:** `reputation_score` — pontuação de 0 a 1000, calculada pelo motor de IA (ver seção 4). Determina a posição de vantagem no leilão em caso de empate de spread.

---

## 3. Algoritmo de Matching

### 3.1 Fluxo de Alto Nível

```
[Sender confirma Ordem]
         |
         v
[Motor Antigravity recebe evento]
         |
         v
[Filtragem: Exchangers elegíveis por corredor]
         |
         v
[Scoring Composto de cada candidato]
         |
         v
[Eleição do Vencedor]
         |
         v
[Atomic Lock: colateral do Exchanger + escrow do Sender]
         |
         v
[Disparo instrução de payout para VASP local]
         |
         v
[Aguarda webhook de confirmação (Time-lock: 300s)]
         |
    [OK] |           [Timeout]
         v                v
   [SETTLED]        [ROLLBACK atômico]
```

---

### 3.2 Filtragem de Elegibilidade

Antes do leilão iniciar, o engine aplica filtros **hard** (eliminatórios):

| Critério | Regra |
|---|---|
| Corredor coberto | `target_country` ∈ `exchanger.covered_corridors` |
| Solvência de Colateral | `exchanger.available_collateral_usdt` ≥ `order.source_amount_usdt * 1.05` |
| Status KYC | `exchanger.kyc_status == APPROVED` |
| Reputação mínima | `exchanger.reputation_score` ≥ 200 |
| Penalidade ativa | `exchanger.penalty_flag == false` |

Exchangers que não passam em qualquer filtro são excluídos instantaneamente.

---

**O Exchanger com o maior S vence o leilão.** Em caso de empate exato (≤ 0.001 de diferença), o desempate é feito por `Reputation Score`. Se o empate persistir, utiliza-se `FIFO`. Isso premia a fidelidade e a performance histórica, não apenas a latência da rede.

---

### 3.4 Blind Queue & Janela de Veredito (Anti-Conluio)

O motor utiliza uma fila de licitação **cega e randômica**. Diferente de exchanges públicas, onde o order book é visível, o FLUXUS protege a margem do LP:
1. **Janela de Silêncio:** Ao receber uma ordem, o motor abre uma janela de 5 segundos.
2. **Commit-Reveal:** Exchangers submetem bids criptografados (hash do bid).
3. **Veredito Síncrono:** Após 5s, o motor "abre as cartas", calcula os scores e executa o *Atomic Lock* na blockchain escolhida.

Isso elimina o "sniping" e garante que o spread ofertado seja o melhor possível para o ecossistema, não apenas uma reação ao lance do competidor.

---

## 4. Sistema de Reputação On-Chain

### 4.1 Composição do `reputation_score`

O score é armazenado no Smart Contract `FluxusReputationRegistry` e atualizado após cada transação `SETTLED` ou `FAILED`.

| Evento | Impacto no Score |
|---|---|
| Transação `SETTLED` dentro do time-lock | +3 pontos |
| Transação `SETTLED` em < 60s (excelência) | +5 pontos |
| Transação `FAILED` por atraso do Exchanger | -15 pontos |
| Disputa julgada contra o Exchanger | -50 pontos |
| 30 dias consecutivos de operação sem falha | +10 pontos (bônus) |
| Score abaixo de 100 por 72h | Suspensão automática |

### 4.2 Tiers de Reputação

| Tier | Score | Benefício |
|---|---|---|
| Bronze | 0–299 | Acesso básico, volume por ordem até $500 |
| Silver | 300–599 | Volume até $2.000, prioridade no desempate |
| Gold | 600–849 | Volume até $10.000, acesso a ordens B2B |
| Platinum | 850–1000 | Volume ilimitado, fee de plataforma reduzida (0.8%) |

---

## 5. Colateral e Atomic Lock

### 5.1 Requisito de Colateral

Para participar do leilão, o Exchanger **deve ter colateral pré-depositado** no Smart Contract `FluxusCollateralVault`.

```
collateral_required = order_amount_usdt * 1.05
```

O fator `1.05` cobre possíveis variações de câmbio durante o settlement window de 300 segundos.

O colateral é verificado em tempo real via leitura do estado do Smart Contract. Esse processo leva **< 50ms** porque é feito diretamente no nó RPC da rede Polygon, sem intermediários off-chain.

### 5.2 Atomic Lock (Lógica do Smart Contract)

```solidity
// Contrato: FluxusNexus.sol (simplificado)
function lockFunds(
    bytes32 orderId,
    address exchangerAddress,
    uint256 senderAmountUsdt,
    uint256 exchangerCollateral,
    uint256 timeLockExpiry  // block.timestamp + 300s
) external onlyEngine {
    require(
        collateralVault.available(exchangerAddress) >= exchangerCollateral,
        "Colateral insuficiente"
    );
    senderEscrow[orderId] = senderAmountUsdt;
    exchangerLock[orderId] = exchangerCollateral;
    lockExpiry[orderId] = timeLockExpiry;
    emit FundsLocked(orderId, exchangerAddress, timeLockExpiry);
}
```

**Princípio de Atomicidade:**
- Se `lockFunds()` reverter por qualquer motivo (colateral insuficiente, gas, etc.), **nenhum capital é movimentado**. A transação reverte completamente.
- Se o payout não for confirmado antes de `timeLockExpiry`, a função `releaseOnTimeout()` pode ser chamada por qualquer address (permissionless), liberando ambos os colaterais.

---

## 6. Máquina de Estados

> **SLA em duas camadas:** (1) após `MATCHED`, o investidor deve avançar para `PROCESSING` dentro da janela de **15 minutos** (`TECH_STATE_MACHINE_REVERSAL.md`); (2) em `VALIDATING`, o webhook da VASP deve confirmar dentro de **300 s** (linha abaixo).

```
REQUESTED → MATCHING → LOCKED → DISPATCHING → VALIDATING → SETTLED
                                     ↓                ↓
                                 CANCELLED         ROLLBACK
```

| Estado | Descrição | Responsável | Duração Máxima |
|---|---|---|---|
| `REQUESTED` | Ordem criada, intent_minihash gerado | Sender App | Instantâneo |
| `MATCHING` | Leilão em andamento | Engine Antigravity | 5 segundos |
| `LOCKED` | Colateral bloqueado on-chain | Smart Contract | – |
| `DISPATCHING` | Instrução enviada para VASP | Engine → VASP API | 10 segundos |
| `VALIDATING` | Aguardando webhook de confirmação | VASP → Engine | 300 segundos |
| `SETTLED` | Payout confirmado, lucro distribuído | Smart Contract | Permanente |
| `ROLLBACK` | Timeout ou falha no payout | Smart Contract | Permanente |
| `CANCELLED` | Falha no leilão (sem Exchanger elegível) | Engine | Permanente |

---

## 7. Distribuição de Receita no Estado SETTLED

Quando o webhook de confirmação chega, o contrato executa a distribuição atômica:

```
Total Spread Capturado = sender_amount × spread_efetivo

  1. Exchanger Yield     = spread_efetivo × 42.8%  (yield ao investidor)
  2. VASP Fee            = spread_efetivo × 28.6%  (custo do trilho local)
  3. Plataforma FLUXUS   = spread_efetivo × 28.6%  (Orchestration Fee)
  
Exemplo prático (ticket = $500, spread Tiered ~0.92%):
  - Total spread: ~$4.62
  - Exchanger:    ~$1.98
  - VASP:         ~$1.32
  - FLUXUS:       ~$1.32
```

### 7.1 Ciclo de Re-Liquidação do Liquidante (Capital Loop)

Para garantir que o Exchanger mantenha sua liquidez operativa em moeda Fiat, o motor Antigravity suporta o fechamento automático do ciclo de caixa. O retorno do capital e lucro do estado "On-Chain" para a "Conta Bancária de Origem" segue o protocolo canónico em [`../04_PROCESS/PROCESS_LP_CASH_CYCLE.md`](../04_PROCESS/PROCESS_LP_CASH_CYCLE.md) (legado interno: `FLUXUS_LP_CASH_CYCLE_PROTOCOL.md`), baseado em três pilares:

1.  **Auto-Refill via VASP:** Conversão automática de USDT para BRL via API de parceiros regulados.
2.  **Matching Reverso:** Compensação orgânica entre ordens de fluxo oposto.
3.  **Withdrawal Soberano:** Saque manual para liquidação em plataforma de preferência do LP.

---
Essa distribuição é hardcoded no contrato — **nenhum admin pode alterá-la unilateralmente**. Mudanças requerem votação on-chain com quórum de 66% dos Exchangers Platinum.

---

## 8. APIs e Integrações

### 8.1 Endpoints do Motor (REST + Webhook)

| Endpoint | Método | Descrição |
|---|---|---|
| `/v1/orders` | POST | Cria nova RemittanceOrder |
| `/v1/orders/{id}/status` | GET | Consulta estado da ordem |
| `/v1/exchangers/bid` | POST | Exchanger submete lance |
| `/v1/exchangers/profile` | GET | Dados de reputação e colateral |
| `/v1/webhooks/vasp-confirm` | POST | VASP notifica sucesso do payout |
| `/v1/webhooks/vasp-fail` | POST | VASP notifica falha (inicia Rollback) |

### 8. Stack Tecnológico e Matriz de Decisão (Dual-Stack)

O protocolo FLUXUS é flexível, permitindo que a transação ocorra no trilho mais adequado para o perfil do cliente ou do corredor.

### 8.1 Comparativo de Trilhos (Rails)

| Atributo | Polygon PoS | Solana | Vantagem FLUXUS |
|---|---|---|---|
| **Velocidade (Block Time)** | ~2.0s | **~0.4s** | Experiência "Real-time PIX" |
| **Custo tx (Gas)** | ~$0.01 | **<$0.001** | Margem em micro-remessas |
| **Concorrência** | Sequencial (EVM) | **Paralela (Sealevel)** | Escalabilidade Global |
| **Ecossistema** | Alta compatibilidade | Performance pura | Flexibilidade estratégica |
| **Finalidade** | Probabilística | Determinística rápida | Segurança no Matching |

### 8.2 Matriz de Decisão: Quando usar qual?

| Cenário | Trilho Recomendado | Justificativa |
|---|---|---|
| **Varejo / Micro-remessa** | **Solana** | Custo de gas não corrói o lucro do LP. |
| **Institucional / B2B** | **Polygon** | Compatibilidade com custódias tradicionais (EVM). |
| **Corredores de Alta Volatilidade** | **Solana** | Latência menor reduz risco de variação cambial. |
| **Integração com Drex (Brasil)** | **Polygon** | Padronização com o real digital brasileiro. |

### 8.3 Infraestrutura de Suporte

| Camada | Tecnologia | Justificativa |
|---|---|---|
| Custódia | Fireblocks MPC | Grau institucional, suporte multi-chain. |
| Smart Contracts | Solana Anchor / Solidity | Auditável, máxima segurança. |
| Monitoramento | Chainalysis | KYF real-time, rastreamento total. |

---

## 9. Métricas de Performance Alvo

| KPI | Meta | Benchmark Atual (SWIFT) |
|---|---|---|
| Latência de Matching | < 5 segundos | N/A |
| Latência de Settlement | < 120 segundos (P95) | 24–48 horas |
| Taxa de Sucesso Atômica | > 99.5% | ~98% (com erros manuais) |
| Capital Efficiency (giro/dia) | 3x–5x por Exchanger | < 0.1x (Nostro/Vostro) |
| Custo por Transação (OPEX) | < 0.3% do GTV | 2–4% |
| Disponibilidade do Motor | 99.95% (SLA) | 95–98% |

---

## 10. Roadmap de Evolução do Protocolo

| Fase | Milestone | Prazo Estimado |
|---|---|---|
| **v1.0** | Corredor único (BR↔EU), Matching básico, colateral manual | T+0 (atual) |
| **v1.5** | Auto-bidding IA, Reputation Score on-chain, 3 corredores | T+6 meses |
| **v2.0** | Liquidez institucional (Market Makers), B2B API, 10 corredores | T+12 meses |
| **v2.5** | Integração Drex (Real Digital), Settlement < 10s P99 | T+18 meses |
| **v3.0** | Cross-chain (Stellar, TON), Atomic Swaps multi-rede | T+24 meses |

---

## 11. Deep Dive: Sistema de Micro-hash (O Elo Atômico)

O **Micro-hash** é a inovação proprietária da FLUXUS que resolve o problema da conciliação entre trilhos heterogêneos (Cripto vs Fiat Local).

### 11.1 Geração e Estrutura
O hash é gerado de forma determinística no momento da solicitação:
`MicroHash = Keccak256(OrderID + Amount + TargetIdentifier + salt)`

Este hash é o **ID Universal** da transação, presente em:
1. Meta-data da transação On-chain.
2. Instrução de Payout enviada à VASP.
3. Campo "Informações Complementares" do PIX/Transferência bancária local.

### 11.2 Fluxo de Verificação (Atomic Reconciliation)
O motor Antigravity monitora continuamente os webhooks das VASPs e o Open Finance dos parceiros:
- **Passo 1:** Recebe notificação de depósito bancário.
- **Passo 2:** Extrai o Micro-hash dos dados da transferência.
- **Passo 3:** Compara com o `micro_hash` travado no Smart Contract.
- **Passo 4:** Se `Match == True`, o contrato libera os fundos instantaneamente.

Isso elimina a necessidade de "comprovantes de tela", tornando o sistema imune a fraudes de Photoshop e erros de digitação manual.

---

## 12. Soberania Tecnológica e Propriedade Intelectual (IP)

O protocolo FLUXUS não é um "wrapper" de APIs existentes, mas um sistema de engenharia financeira construído do zero.

### 12.1 Ativos de Propriedade da FLUXUS
- **Matching Algorithm:** O código-fonte do motor de leilão cego e scoring.
- **Reputation Logic:** Modelos de dados que definem o risco e o benefício dos Exchangers.
- **Micro-hash Protocol:** A metodologia de vinculação entre hashes criptográficos e transações PIX/Fiat.
- **Smart Contract Suite:** A suíte de contratos (Solana/EVM) que governa o vault e as penalidades.

### 12.2 Desenvolvimento In-House
Toda a lógica de orquestração de liquidez e o motor de decisão são desenvolvidos internamente. A utilização de blockchains públicas (Solana/Polygon) é estritamente para o **Settlement Layer**, garantindo que a FLUXUS mantenha total soberania sobre a inteligência do negócio e o relacionamento com o cliente.

---

*Documento gerado por Antigravity — FLUXUS Protocol Engineering Team*
*Versão 1.1 — Abril 2026 (Dual-Stack Upgrade)*
