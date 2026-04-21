# ⚙️ FLUXUS: Orchestration Process Flow

Este relatório detalha a interatividade sistêmica e a orquestração de processos que permitem ao FLUXUS realizar remessas globais com precisão atômica e transparência total.

---

## 1. 🧬 A Gênese da Ordem: Onboarding e Identidade
A orquestração começa na primeira interação do usuário com a camada de acesso:

1.  **Handshake de Identidade (Privy)**: O login social gera um `User_ID` único. Síncronamente, o sistema orquestra a criação de uma **Embedded Wallet** (não-custodial) que servirá como a âncora on-chain do usuário.
2.  **Ativação do Motor de Compliance (SumSub)**: O `User_ID` é enviado ao Hub de KYC. A interação aqui é bidirecional:
    -   O sistema envia os documentos capturados.
    -   O SumSub retorna o `KYC_Status` e os limites de transação.
3.  **Vínculo com a Shadow-Wallet**: Apenas após a aprovação do KYC, a orquestração libera a Shadow-Wallet no banco de dados, configurando os limites de GTV (Gross Transaction Volume) baseados no score de risco.

---

## 2. ↕️ Orquestração de Entrada (RAMP & Funding)
Como o capital fiat é transformado em liquidez operacional:

1.  **Intent de Envio**: O usuário define o valor (ex: BRL). O sistema consulta os endpoints dos parceiros de **RAMP** (Alchemy Pay/Ramp.network) para obter a cotação garantida por 60 segundos.
2.  **Captura e Webhook**: Ao concluir o pagamento fiat, o parceiro de RAMP dispara um **Webhook de Sucesso** para o Backend FLUXUS.
3.  **Liquidez Síncrona**: O sistema recebe o sinal, valida o hash da transação on-chain (Polygon/Solana) e atualiza o saldo da Shadow-Wallet. **Resultado**: O capital agora está "quente" e pronto para o Matching Engine.

---

## 3. 🧠 O Motor de Decisão (Matching Engine & Reputation)
O momento em que a necessidade de remessa encontra a liquidez do investidor:

1.  **Publicação da Ordem na Blind Queue**: A ordem é anonimizada e publicada na fila de leilão cego.
2.  **Interação de Lances (Bidding)**: Os LPs (Liquidity Providers) submetem lances de spread. O sistema orquestra a validação de cada lance contra o `Reputation_Score` de cada LP (armazenado on-chain).
3.  **Algoritmo de Seleção**: O Engine Antigravity processa o melhor lance. A interação aqui é crucial: o sistema verifica se o LP vencedor tem **Colateral Suficiente** travado na Fireblocks. Se `True`, o match é selado.

---

## 4. 🔒 Confiança Atômica: Settlement e Blockchain
A transição da decisão para a garantia financeira:

1.  **Instrução de Atomic Lock**: O Matching Engine envia uma instrução para o **Smart Contract (FluxusNexus)**.
2.  **Bloqueio de Fundos**: O contrato trava simultaneamente:
    -   O capital do Sender (vindo da RAMP).
    -   O colateral do LP (garantia de payout).
3.  **Geração do Minihash**: Com os fundos travados, o sistema gera o **Minihash** (ID Universal). Este hash é enviado síncronamente para a VASP local (país de destino) como a chave de autorização para o Payout.

---

## 5. 💳 Entrega Final: Payout e Card Issuing
A orquestração na "última milha" física:

1.  **Disparo de Payout (VASP/Partner)**: A VASP recebe a instrução e o Minihash. Ela processa o carregamento do cartão (Stripe/Marqeta) no país de destino.
2.  **Confirmação de Carregamento**: O parceiro de cartões envia um sinal de sucesso. A VASP então dispara um Webhook para o FLUXUS confirmando o `fiat_delivery`.
3.  **Settlement Final On-Chain**: Com a prova de entrega, o Smart Contract libera o capital bloqueado, distribuindo as fees e o lucro do LP instantaneamente.

---

## 6. 📊 Consolidação: Hashes e DRE Síncrona
O encerramento sistêmico da transação:

1.  **Cadeia de Auditoria**: O Minihash da transação é marcado como `SETTLED` e "empacotado" no **Macrohash** daquela hora, ancorando a verdade definitiva na blockchain.
2.  **Atualização da DRE (Accounting)**: O evento de Settlement dispara a atualização síncrona dos registros contábeis. A interatividade aqui acontece entre o Smart Contract e o **SQLite/PowerBI**:
    -   O saldo do LP é atualizado com o lucro.
    -   O relatório de lucro bruto da plataforma é incrementado.
    -   O indicador de governança fiscal recalcula o "giro mensal" do investidor.

---

## 💡 Conclusão: A Orquestração como Produto
A força do FLUXUS não reside apenas nos componentes individuais, mas na **fluidez da interação** entre eles. A orquestração garante que:
-   A **Prevenção de Fraude** (KYC) impeça a **Liquidez** (RAMP).
-   A **Reputação** (Engine) garanta o **Settlement** (Blockchain).
-   A **Entrega** (Cards) valide a **Contabilidade** (DRE).

Este ecossistema interconectado é o que permite transacionar bilhões com a velocidade de um pulso digital e a segurança de um banco central.

---
*Relatório de Orquestração gerado por Antigravity — FLUXUS Protocol Engineering Team.*
