# Remit Logic: State Machine & Reversal

Este documento define a lógica formal dos contratos inteligentes do FLUXUS para garantir a custódia segura e o tratamento de falhas.

## 1. Estados da Remessa

Cada transação FLUXUS deve passar pelos seguintes estados imutáveis, registrados via Minihash:

| Estado | Gatilho | Ação do Contrato |
| :--- | :--- | :--- |
| **`INITIATED`** | Pedido via API (Login) | Gera Minihash de Intenção. |
| **`MATCHED`** | Investidor aceita o Bid | Trava as Stablecoins no Escrow. |
| **`PROCESSING`** | VASP inicia recarga fiat | Bloqueia cancelamento unilateral. |
| **`SETTLED`** | VASP confirma o "Load" | Libera principal + lucro para o Investidor. |
| **`REVERTING`** | Falha na recarga (VASP Error) | Prepara o estorno. |
| **`REVERSED`** | Estorno concluído | Devolve principal ao Investidor. |
| **`CYCLE_COMPLETED`** | Re-liquidação Fiat concluída | Capital + Lucro confirmados na conta do LP. |

---

## 2. Cenários de Invalidação (Invalidation Endpoints)

### A. Falha de SLA (Time-out) — handoff pós-match
Se o investidor entra no estado `MATCHED` mas o status não evolui para `PROCESSING` em **15 minutos**:
-   **Ação:** O contrato invalida a reserva.
-   **Resultado:** As stablecoins voltam ao investidor (+ penalidade se houver). A ordem volta para a "Fila".

> **Nota (harmonização com o protocolo de matching):** Os **15 minutos** medem a **janela operacional** entre match e início do processamento (claim / handoff à VASP). Já a janela de **300 segundos** em `TECH_MATCHING_ENGINE_PROTOCOL.md` aplica-se sobretudo à fase **VALIDATING** (aguardar confirmação de payout após despacho). São dois temporizadores em etapas diferentes do ciclo.

### B. Falha de Destino (VASP Rejection)
Se a VASP reportar que o cartão/conta do destinatário está inativo ou inválido:
-   **Ação:** O sistema emite um Minihash de `AUTH_FAILED`.
-   **Resultado:** O contrato reverte os fundos para o Investidor. O lucro (spread) é cancelado.

---

## 3. Auditoria via Hashes

- **Macrohash:** Link persistente para a transação na Polygon.
- **Minihash:** Captura os metadados de cada mudança de estado, incluindo o `capitalGain` visível no status `SETTLED` e o `error_code` no status `REVERSED`.
