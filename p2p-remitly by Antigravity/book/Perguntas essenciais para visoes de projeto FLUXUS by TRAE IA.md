# Perguntas essenciais para visões de projeto FLUXUS (by TRAE IA)

Este documento consolida as perguntas essenciais para completar as visões de processo que faltam para o FLUXUS sair de “tese/arquitetura” para “operação executável”.

## 1) Produto (Sender / Receiver)

1. O receiver precisa ter conta/cartão pré-existente, ou o FLUXUS emite/abre via VASP (KYC do receiver)? Em quais países?
2. Qual payout principal do MVP: PIX, push-to-card, cartão pré-pago (VASP), mobile money? Qual ordem de priorização?
3. No corredor USA→BR, qual funding do sender no MVP: ACH, debit card, wire? Existe funding por cash/ponto físico ou não?
4. Vai existir cotação travada (quote lock) por X minutos? Quem assume o risco no intervalo (LP, reserve, plataforma)?

## 2) Mercado de LP / Fila de Liquidez

5. Como o LP compete e vence a ordem: melhor spread (leilão), score/reputação, SLA, limite por corredor, fairness? Qual regra final de desempate?
6. O LP mantém saldo pré-travado por corredor (pool) ou pode operar “just-in-time”? Se just-in-time, qual penalidade e qual timeout?
7. Quais limites por LP (por dia, por corredor, por risco, por país) e como a plataforma recalibra isso (IA/rules)?

## 3) Risco, Fraude e Proteção

8. Quais sinais bloqueiam uma remessa antes de ir para MATCHED (KYC fraco, device, velocity, geolocalização, lista sancionada, chargeback risk)?
9. Como o Security Reserve (ex.: 0.2%) funciona na prática: volatilidade FX, fraude, chargeback de funding, erro operacional do LP, falha de VASP?
10. Existem “holds”/cooldowns para casos suspeitos ou o produto é “instantâneo sempre” (com spread variando)?

## 4) Exceções e Reversões (Operação)

11. Em REVERSED, quem reembolsa o sender (plataforma, LP, reserve) e em qual moeda? Existe taxa de cancelamento?
12. Como tratar falhas parciais do rail local (ex.: debitou mas não creditou; creditou mas não confirmou; webhooks atrasados)?
13. Se funding for cartão (USA), como tratar chargeback/disputa e como isso impacta o estado da remessa e o payout?
14. A remessa pode ser “partial fill” (parte executada, parte pendente) ou é sempre “fill-or-kill”?

## 5) Compliance / Legal / Operação Regulada

15. Quem faz KYC/AML: plataforma, VASP, ou ambos (divisão de responsabilidades)? Quais níveis de KYC no MVP?
16. Quem é o merchant of record e qual o modelo contratual com VASP e LP para sustentar o “nexus tecnológico”?
17. Quais relatórios precisam existir no MVP (auditoria por transação, export por período, trilha de evidência, relatórios por país)?

## 6) Contábil, Ledger e Reconciliação

18. Onde ficam registrados saldo do sender, saldo do LP, fees do board e reserve: ledger único (Postgres/JSONB + hashes) ou serviços separados?
19. Qual é a rotina de reconciliação (diária/semanal): on-chain (USDT) vs extratos do VASP vs rails locais (PIX/push-to-card)?
20. Como é feita a apuração de receita (spread/fees) e a segregação do reserve (contabilmente e operacionalmente)?

## 7) Observabilidade e Suporte

21. Quais dashboards e alertas são mínimos (SLA do MATCHED→PROCESSING, falhas de VASP, filas, discrepâncias de reconciliação)?
22. Quais “runbooks” precisam existir (ex.: reprocessamento de payout, reversão manual, contestação, bloqueio de LP, freeze por compliance)?

## 8) “6 respostas que destravam o desenho”

Se você responder só estes 6 itens, já dá para fechar as visões de processo do MVP:

1. Corredor MVP (origem→destino) + rails de funding/payout
2. Quem faz KYC/AML (sender e receiver) e até que nível
3. Regra de matching (leilão vs score vs fila)
4. Política de reversão (quem paga e em que moeda)
5. Como o reserve é usado (gatilhos)
6. Modelo de reconciliação (qual é a fonte da verdade)

## 9) Respostas definitivas (base para construir as visões)

### 1. Corredor MVP e Rails (Origem → Destino)

- **Corredor principal:** USA (USD) → Brasil (BRL).
- **Funding rail (Sender):** Alchemy Pay (widget integrado para cartões de débito/crédito e transferências locais). O objetivo é o sender pagar em fiat e a conversão para USDT/USDC (Polygon) ocorrer na camada “Shadow” de ingestão.
- **Payout rail (Receiver):** no Brasil, PIX (Dock/BS2/Bacen). Globalmente, Push-to-card (Visa Direct / Mastercard Send) e Cartões Pré-pagos White-label (VASPs como Striga/Reap).

### 2. KYC/AML e Níveis de Verificação

- **Entidade responsável:** plataforma FLUXUS orquestra via SumSub; “Merchant of Record” varia conforme o rail (VASPs locais detêm licenças).
- **Sender:** Tier 1 (ID + liveness) obrigatório no primeiro envio; bloqueio automático de listas de sanções globais no `POST /auth/login`.
- **Receiver:** para payout via PIX, KYC simplificado (validado pelo CPF no rail local). Para Cartão Global FLUXUS, exige identidade digital básica para emissão (KYC delegado ao emissor VASP).

### 3. Regra de Matching (Leilão vs Score vs Fila)

- **Modelo:** Leilão Reverso Síncrono (Reverse Auction).
- **Lógica:** ao criar a ordem, o “Matching Brain” dispara um leilão; vence o LP que oferecer o menor spread dentro do SLA de 15 minutos.
- **Filtros de qualidade:** leilão restrito por Reputation Score (taxa de sucesso de payouts anteriores) e por colateral obrigatório JIT pré-travado na Fireblocks.

### 4. Política de Reversão

- **Quem paga:** se falhar (time-out de SLA ou erro da VASP), o principal é devolvido integralmente ao LP via smart contract.
- **Moeda de estorno:** estorno ao LP em stablecoin/USDT (moeda de transporte). Para o sender, reembolso em fiat local via on-ramp original, subtraindo apenas taxas de rede irrecorríveis.

### 5. Uso do Security Reserve (FSF - 0.2%)

- **Catástrofe de rede:** queda de nodes ou falhas em smart contracts.
- **Volatilidade extrema:** oscilações de FX entre LOCK e SETTLE que superem o colateral do LP.
- **Seguro de fraude:** cobertura de chargebacks no funding (USA) para não penalizar o pool de liquidez dos investidores.
- **Erro operacional:** casos onde a VASP debita, mas não confirma, exigindo liquidação manual pela plataforma.

### 6. Modelo de Reconciliação (Fonte da Verdade)

- **Fonte única:** Hash Ledger Síncrono (Polygon).
- **Minihashes:** registram cada troca de estado em tempo real (JSONB no Postgres + hash on-chain).
- **Macrohash:** âncora horária consolidando minihashes na Polygon, como registro imutável para reguladores e investidores institucionais.
- **Conformidade:** extrato do VASP e do rail local são evidências de suporte; a validade da transação é determinada pela finalidade atômica do smart contract.

### TIP

Com estas definições, dá para montar as jornadas completas. Foco inicial recomendado: Jornada do Investidor (LP), porque a regra de Colateral JIT garante a solvência da rede sem exigir licenças bancárias pesadas para a plataforma.
