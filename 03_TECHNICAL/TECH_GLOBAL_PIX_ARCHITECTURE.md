# Global PIX: Arquitetura do Motor de Liquidação Cross-Border

Esta arquitetura define como o FLUXUS escala o conceito de "PIX" (pagamento instantâneo) para qualquer país usando **USDT na rede Polygon** como trilho de transporte global.

> **Preço (remessa):** a referência de precificação é **Dominância/Tiered** — `TECH_FLUXUS_PRICING_CANON.md`. O motor abaixo calcula *como* aplicar e auditar o spread por corredor (PIX ou push-to-card).

## 1. As 3 Camadas do Motor Global

Para funcionar em qualquer país, o motor é dividido em camadas agnósticas:

### A. Camada de Ingestão (Gateway USDT)
- **Tecnologia:** Polygon Chain (USDT PoS).
- **Função:** Fornece um endereço de depósito único ou contrato inteligente de Escrow para cada transação.
- **Vantagem:** Taxa zero/baixa e confirmação em < 5 segundos.

### B. Camada de Inteligência (The Matching Brain)
- **Tecnologia:** FastAPI + Redis + Celery.
- **Função:** No momento que o USDT é detectado, a IA do FLUXUS busca o "Corredor de Liquidez" correspondente.
- **Lógica:** 
  1. Identifica a moeda de destino (ex: BRL).
  2. Bloqueia o saldo em BRL no pool de um investidor local (P2P LP).
  3. Calcula o spread final e confirma a reserva.

### C. Camada de Liquidação (The Last Mile Rails)
A plataforma possui adaptadores para diferentes rails nacionais:

| Rail de Destino | Região | API / Interface |
| :--- | :--- | :--- |
| **PIX Engine** | Brasil | Integração via Dock/BS2/Bacen. |
| **Push-to-Card** | USA / Europa | Integração via Visa Direct / Mastercard Send. |
| **Mobile Money Hub**| África / Ásia | Integração via M-Pesa / MTN / GrabPay. |

## 2. Rastreabilidade via Macro Hash (Audit Trail)
O "PIX Global" não é apenas rápido, ele é 100% auditável:

- **Hash L1 (`REMIT_FUNDED`):** Link entre o ID do QR Code e o TXID da Polygon.
- **Hash L2 (`FX_LOCKED`):** Registro da taxa de câmbio e do investidor que proveu a liquidez local.
- **Hash L3 (`SETTLE_DISBURSED`):** ID da transação no sistema bancário local (ex: End-to-End ID do PIX).

## 3. Estratégia de Expansão Global
A estratégia para oferecer o serviço em qualquer país segue o modelo de **"Nós de Liquidez"**:

1. **Países com Banco Central Moderno:** Conexão direta via API de Pagamentos Instantâneos (PIX, FedNow, UPI).
2. **Países Tradicionais:** Uso de redes de cartões (Push-to-card) para simular o comportamento do PIX.
3. **Países sem Bancarização:** Parcerias com redes de varejo para saque via código (Cash-out).

## 4. Segurança e Anti-Fraude
O sistema utiliza um **Double-Check de Liquidez**:
- O PIX só é disparado após 2 confirmações na rede Polygon (viblidade final).
- O capital do investidor local é mantido em um sub-ledger bloqueado durante os 10 minutos de validade do QR Code para evitar falhas de liquidação.
