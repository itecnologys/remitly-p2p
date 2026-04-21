# FLUXUS Gold Standard: Modus Operandi Detalhado

Este documento define o padrão de ouro operacional do FLUXUS, focado na transparência total para o usuário final e na eficiência da liquidez P2P na "última milha".

## 1. O Fluxo "Shadow-Crypto" (Fiat-to-Fiat)

O FLUXUS opera sob a premissa de que o usuário final (Remetente e Destinatário) nunca precisa saber que Cripto está envolvido no processo. O cripto é apenas a camada de transporte.

### Trilha Operacional Step-by-Step:
1.  **Entrada (Sender):** O usuário faz login via `Login/Senha` (sem chaves privadas visíveis). Solicita o envio de moeda fiat (ex: BRL).
2.  **Conversão Interna:** O sistema converte o valor para Stablecoins (USDT/USDC).
3.  **Matching na Fila:** O pedido entra na "Fila de Liquidez". Investidores competem pelo spread.
4.  **Escrow do Investidor:** O investidor vencedor trava o valor correspondente em stablecoins no Smart Contract.
5.  **Liquidação de Última Milha (Last Mile):** O investidor usa suas stablecoins no país de destino para "comprar" a moeda local e carregar o **Cartão de Débito Pré-pago** do destinatário através de uma ponte VASP.
6.  **Saída (Receiver):** O destinatário recebe a notificação de que seu cartão está carregado e pronto para uso em qualquer rede Visa/Mastercard.

---

## 2. O Papel do Investidor (Liquidity Provider)

Diferente de pools de liquidez tradicionais, o investidor do FLUXUS é um **Exchanger Ativo**:
-   Ele busca rentabilidade na diferença entre o valor de compra da stablecoin e o valor de venda (spread) para carregar o cartão local.
-   Ele garante que o dinheiro chegue ao destino de forma instantânea, assumindo o risco operacional em troca da fatia **LP (share do spread)** dentro da precificação **Dominância/Tiered** (ver `03_TECHNICAL/TECH_FLUXUS_PRICING_CANON.md`); o ganho **anualizado** depende do número de rotações de capital.

---

## 3. Gestão de Falhas e Cancelamentos

A auditoria via **Minihash** garante que o capital do investidor nunca seja perdido:
-   **Validação:** O sistema só libera o lucro do investidor se a VASP local emitir o comprovante de carregamento do cartão.
-   **Invalidação:** Se o cartão não for carregado (ex: conta bloqueada), o Smart Contract reverte o valor das stablecoins para o investidor, emitindo um Minihash de `REMIT_REVERSED`.

---

## 4. Diferencial Competitivo
Ao contrário de empresas como Bitso ou Strike, o FLUXUS:
1.  **Não exige que o receptor tenha conta em Exchange.**
2.  **Permite que o receptor use o dinheiro em qualquer estabelecimento físico** via cartão de débito.
3.  **Descentraliza o lucro do câmbio**, antes restrito aos bancos, agora distribuído para investidores P2P.
