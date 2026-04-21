# API Specs: Login & Tokenização da Fila de Liquidez

Este documento descreve as interfaces técnicas (endpoints) para o acesso simplificado do usuário e a orquestração da fila de investidores.

## 1. Autenticação e Portal do Usuário (Shadow-Wallet)

O objetivo é abstrair a complexidade da blockchain.

### `POST /auth/login`
- **Descrição:** Login tradicional via e-mail/senha.
- **Payload:** `{ "email": "user@example.com", "password": "hashed_password" }`
- **Response:** JWT Token + `userProfile` (Fiat balances only).
- **Nota:** O sistema mapeia este login para uma `Safe-Wallet` (Gnosis Safe) controlada por Smart Contracts, sem que o usuário precise gerenciar chaves.

### `POST /remit/initiate`
- **Descrição:** Inicia o processo de remessa.
- **Payload:**
  ```json
  {
    "senderFiatAmount": 1000.00,
    "sourceCurrency": "BRL",
    "destCurrency": "PHP",
    "receiverID": "REC_12345",
    "payoutMethod": "VISA_PREPAID_CARD"
  }
  ```
- **Ação:** Emite o **Minihash de Intenção** na Polygon.

---

## 2. Liquidity Queue (A Fila de Investidores)

Os investidores interagem com uma API de "Marketplace de Ordens".

### `GET /liquidity/queue`
- **Descrição:** Lista ordens pendentes para investidores.
- **Filtros:** `destCurrency`, `minSpread`, `availability`.

### `POST /liquidity/claim`
- **Descrição:** Investidor "assume" a ordem.
- **Payload:** `{ "orderID": "ORD_001", "investorSignature": "SIG_..." }`
- **Ação:** O Smart Contract trava as stablecoins do investidor no Escrow. Inicia o cronômetro de **15 minutos (SLA)** para o investidor fazer o handoff até `PROCESSING` (ver `TECH_STATE_MACHINE_REVERSAL.md`). A confirmação de payout na VASP segue a janela de **300 s** do motor de matching após o despacho.

---

## 3. Payout Bridge (Last Mile)

### `POST /bridge/load-card`
- **Descrição:** Integrado com VASPs (ex: Reap, Striga).
- **Payload:**
  ```json
  {
    "orderID": "ORD_001",
    "cardID": "CARD_67890",
    "fiatAmount": 15000.00,
    "currency": "PHP"
  }
  ```
- **Ação:** A VASP converte as stablecoins do Escrow e carrega o cartão. Após sucesso, emite o Minihash de **`SETTLE_SUCCESS`**.
