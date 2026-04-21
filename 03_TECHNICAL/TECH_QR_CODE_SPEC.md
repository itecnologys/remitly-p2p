# Especificação: Global QR Code (Remittance Trigger)

O **Global QR Code** é o ponto de entrada universal para o ecossistema FLUXUS. Ele permite que um recebedor local gere uma solicitação de pagamento em sua moeda nacional, que pode ser liquidada por qualquer carteira USDT no mundo.

## 1. O Conceito do QR Dinâmico
Ao contrário de um endereço de carteira estático, o Global QR Code é **dinâmico e temporário** (válido por 10-15 minutos) para proteger as partes da volatilidade cambial.

### Dados Contidos no QR Code (Pryload):
```json
{
  "protocol": "FLUXUS_REMIT_v1",
  "intent_id": "RF-992837",
  "target_currency": "BRL",
  "target_amount": 100.00,
  "quoted_exchange_rate": 5.12,
  "payment": {
    "network": "Polygon",
    "asset": "USDT",
    "amount": 19.53,
    "address": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
  },
  "expires_at": "2026-04-13T23:45:00Z"
}
```

## 2. Experiência do Usuário (Flow)

1. **Geração:** O vendedor/recebedor no Brasil abre o app e digita "R$ 100".
2. **Cotação:** O backend do FLUXUS calcula o valor em USDT baseado no **Pool de Liquidez P2P** disponível.
3. **Exibição:** O QR Code é gerado. Ele segue o padrão visual do PIX para facilitar a adoção, mas é um link de pagamento Web3.
4. **Pagamento:** O remetente escaneia com qualquer carteira (MetaMask, TrustWallet, Binance App).
5. **Confirmação:** Assim que a transação entra no mempool da Polygon, o app do recebedor mostra "Pagamento em Processamento".
6. **Liquidação:** Após 2 confirmações (~5 seg), o bônus de liquidez P2P é acionado e o PIX cai na conta do recebedor.

## 3. Padrão Tecnológico
Para garantir interoperabilidade, o QR Code segue os padrões:
- **EMV QRCPS:** O mesmo padrão usado pelo PIX e pelo Banco Central do Brasil.
- **ERC-681 / ERC-831:** Padrões de URL para pagamentos na Ethereum/Polygon.

## 4. Auditoria de Segurança
Cada QR Code gerado é registrado como um **Evento L0** (Pre-Audit) no sistema **Macro Hash**. Se o pagamento não for detectado na rede em até 20 minutos, o Hash é invalidado, evitando que liquidez P2P seja "reservada" para transações fantasmas.

---

### Exemplo de Uso Global:
Um turista americano em uma loja no interior do Brasil pode escanear o QR Code da loja e pagar em USDT de sua conta do PayPal/Coinbase. A loja recebe o PIX em Reais no mesmo segundo, sem que o lojista precise saber o que é uma blockchain.
