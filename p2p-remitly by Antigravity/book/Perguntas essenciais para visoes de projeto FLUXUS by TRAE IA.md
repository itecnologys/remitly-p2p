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
