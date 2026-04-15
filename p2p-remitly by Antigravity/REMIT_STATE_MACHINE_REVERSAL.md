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

---

## 2. Cenários de Invalidação (Invalidation Endpoints)

### A. Falha de SLA (Time-out)
Se o investidor entra no estado `MATCHED` mas o status não evolui para `PROCESSING` em 15 minutos:
-   **Ação:** O contrato invalida a reserva.
-   **Resultado:** As stablecoins voltam ao investidor (+ penalidade se houver). A ordem volta para a "Fila".

### B. Falha de Destino (VASP Rejection)
Se a VASP reportar que o cartão/conta do destinatário está inativo ou inválido:
-   **Ação:** O sistema emite um Minihash de `AUTH_FAILED`.
-   **Resultado:** O contrato reverte os fundos para o Investidor. O lucro (spread) é cancelado.

---

## 3. Auditoria via Hashes

- **Macrohash:** Link persistente para a transação na Polygon.
- **Minihash:** Captura os metadados de cada mudança de estado, incluindo o `capitalGain` visível no status `SETTLED` e o `error_code` no status `REVERSED`.
