# FLUXUS — Estratégia de Cold Start & GTM para Exchangers
**Versão:** 1.0 | **Classificação:** Confidencial — Uso Estratégico

---

## 1. O Problema do Cold Start

Todo marketplace bilateral enfrenta o dilema do ovo e da galinha:
- **Sem Exchangers** → Senders não têm liquidez → plataforma não funciona
- **Sem Senders** → Exchangers não têm ordens → não há retorno sobre o colateral

A Uber resolveu pagando motoristas garantidos por hora. O Airbnb resolveu fazendo fotos profissionais dos primeiros anfitriões. **O FLUXUS resolve com uma estratégia em 3 fases sequenciais, cada uma financiada pela anterior.**

---

## 2. Princípio Design: Começar com 1 Corredor, 1 Perfil

Antes de lançar, o FLUXUS define um único **Corridor Zero**:

```
Corridor Zero: UAE (Dubai) → Brasil (PIX)
  - Diáspora estimada: ~300.000 brasileiros nos Emirados
  - Volume médio por trabalhador/mês: AED 1.500 (~$410)
  - Mercado endereçável Corredor Zero: ~$123M/ano
  - Exchanger Profile alvo: Investidores BR com USDT (poupadores DeFi)
```

**Por que este corredor?**
- PIX no Brasil é real-time 24/7 → o payout é o mais previsível do mundo
- Alta demanda (trabalhadores brasileiros no Golfo são comunidade ativa no WhatsApp)
- Custo de aquisição de Exchanger é baixo (brasileiros com USDT são numerosos e organizados)

---

## 3. Fase 1: "Seeded Liquidity" — Os 50 Primeiros Exchangers (Mês 1–2)

### 3.1 Objetivo
Ter **50 Exchangers ativos** com pelo menos **$2.000 de colateral cada** antes de abrir para os primeiros Senders. Total de liquidez inicial: **~$100.000 em USDT disponíveis no Nexus**.

### 3.2 Tática: Recrutamento Cirúrgico (Não é Marketing em Massa)

**Canal 1 — Network do Fundador (Semana 1–2)**
- O fundador faz contato 1:1 com 100 pessoas de sua rede que possuem USDT/Stablecoins.
- Pergunta-chave: *"Você tem USDT parado em exchange ganhando 0%? Quero te propor 1.5% por ordem em 2 minutos de trabalho."*
- Meta: converter 20 desses 100 em Exchangers Beta.

**Canal 2 — Comunidades DeFi Brasileiras (Semana 2–4)**
- Grupos de Telegram/WhatsApp: Traders BR, Holders USDT, Comunidades Coinbase BR.
- Discurso: Não é cripto especulativa. É rendimento real em fiat (PIX). Yield previsível.
- KPI: 30 Exchangers recrutados via comunidade.

**Canal 3 — Influenciadores Micro-Financeiros (Semana 3–6)**
- Parceria com 5 criadores de conteúdo de finanças pessoais no YouTube/Instagram (50K–200K seguidores).
- Deal: fee de afiliado — $50 por Exchanger ativo trazido.
- Conteúdo sugerido: *"Coloquei $5.000 de USDT no FLUXUS. Olha o que aconteceu em 30 dias."*

### 3.3 Proposta de Valor para Exchanger Beta

| Benefício | Detalhe |
|---|---|
| **Yield garantido no beta** | Se a ordem não for completada em 300s por falha da plataforma, o FLUXUS paga o yield mínimo de qualquer forma (válido para as 500 primeiras ordens) |
| **Tier Platinum imediato** | Os 50 primeiros Exchangers recebem status Platinum por 12 meses independente do score |
| **Acesso ao Dashboard Beta** | Dashboard exclusivo com analytics de giro e projeção de rendimento |
| **Participação no Protocolo** | Uma vaga em votações de governança do smart contract futuro |

### 3.4 Onboarding dos 50 Primeiros Exchangers

O processo de onboarding na Fase 1 é **assistido manualmente** (não espere que o produto seja perfeito):

```
Passo 1: Call de 15 min com o fundador ou equipe
Passo 2: KYC via SumSub (link direto, ~5 min)
Passo 3: Depósito de colateral mínimo ($500 em USDT Polygon)
Passo 4: Treinamento no Cockpit (vídeo loom de 8 minutos)
Passo 5: Primeira ordem supervisionada (fundador monitora em tempo real)
```

---

## 4. Fase 2: "Demand Seeding" — Os 500 Primeiros Senders (Mês 2–4)

### 4.1 Objetivo
Ativar demanda real de forma controlada. Não lançar publicamente — fazer **lançamento invite-only** para validar o funil sem stress de escala.

### 4.2 Tática: A Comunidade dos Senders

**Canal 1 — Comunidades de Brasileiros em Dubai (Alvo Cirúrgico)**
- Grupos de WhatsApp de brasileiros nos Emirados (existem dezenas, com milhares de membros)
- Parceria com 3 líderes de comunidade (embaixadores pagos: $200/mês + fee por usuário ativo)
- Mensagem: *"Manda PIX pra família sem pagar 8% de taxa. Testei aqui, chegou em 2 minutos."*

**Canal 2 — Igreja/Comunidade Evangelical Brasileira no UAE**
- Comunidades religiosas são o principal veículo de confiança para remessas de diáspora globalmente (é assim que a Remitly cresceu na rede filipina).
- Parceria com 2 pastores líderes: apresentação da plataforma após o culto.
- ROI esperado: taxa de conversão 3–5x maior do que via anúncio pago.

**Canal 3 — Boca a Boca Estruturado (Referral)**
- Todo Sender que convida 3 amigos que completam a primeira remessa recebe a próxima remessa com taxa ZERO.
- Custo do referral: $3–5 por novo usuário (muito abaixo do CAC de mercado de $35–80).

### 4.3 Meta Fase 2

```
Mês 2: 100 Senders ativos, GTV = $50.000
Mês 3: 250 Senders ativos, GTV = $150.000
Mês 4: 500 Senders ativos, GTV = $350.000
```

Esse volume é **suficiente para os 50 Exchangers beta terem giro de 2–3x/semana**, gerando yields reais que eles vão postar espontaneamente nas redes sociais.

---

## 5. Fase 3: "Flywheel" — Expansão de Corredores (Mês 4–12)

### 5.1 A Lógica da Expansão

Cada Corredor novo segue o mesmo playbook, mas com um custo marginal menor porque:
- O produto já está refinado pelo feedback dos primeiros 500 usuários
- A marca FLUXUS já tem prova social (depoimentos, GTV, screenshots)
- Os Exchangers existentes já têm reputação e podem oraçarem em novos corredores (especialmente os que cobrem múltiplas VASPs)

### 5.2 Ordem de Expansão de Corredores (Baseada em ROI/Fricção)

| Prioridade | Corredor | Razão Estratégica |
|---|---|---|
| **1** | UAE → Brasil | Corredor Zero. PIX real-time. |
| **2** | UK → Brasil | ~120K brasileiros no Reino Unido |
| **3** | USA → México | Maior corredor de remessas do mundo. Validação de escala. |
| **4** | UAE → Índia | Maior volume global de remessas. Gateway para o Sul da Ásia. |
| **5** | UAE → Paquistão | Alto volume, custo atual de bancário 12–15%. Margem enorme. |
| **6** | USA → Brasil | Expansão natural do corredor BR |
| **7** | Europa → Nigéria | Alto custo atual. Gig Economy nigeriana crescendo. |

---

## 6. Estratégia de Precificação para Crescimento

> **Fonte da verdade:** `03_TECHNICAL/TECH_FLUXUS_PRICING_CANON.md` (Dominância/Tiered). A Wise é benchmark de validação, não driver.

### 6.1 Modelo canônico (cold start e escala)
- **Pricing:** escada (tiered) por faixa de volume, com envelope competitivo e transparência (PTAX + taxas explícitas).
- **CET (cliente):** calculado como `Spread_FLUXUS + IOF`, variando por ticket/corredor.
- **Repartição:** LP / VASP / plataforma são shares sobre o spread e podem ser ajustados em cold start sem alterar o CET exibido como “Spread + IOF”.
- **Objetivo:** dominar no varejo sem colapsar margem no atacado; promoções temporárias ajustam shares, não criam “segundo spread”.

### 6.2 Ancoragem Psicológica do Preço

No front-end, o Sender pode ver valor absoluto e comparação com banco, não obrigatoriamente um rótulo de percentagem fixa. Exemplo alinhado ao canónico:

```
┌─────────────────────────────────────────┐
│  Você envia:      AED 1.500             │
│  Taxa FLUXUS:     AED 52.50 (Spread+IOF)│
│  Família recebe:  R$ 2.187,00           │
│                                         │
│  Banco tradicional custaria: R$ 1.987   │
│  Você economiza:  R$ 200,00             │
└─────────────────────────────────────────┘
```

A comparação com o banco é o principal gatilho de conversão.

---

## 7. KPIs de Cold Start por Fase

| KPI | Fase 1 (Mês 1–2) | Fase 2 (Mês 2–4) | Fase 3 (Mês 4–12) |
|---|---|---|---|
| Exchangers Ativos | 50 | 100 | 500+ |
| Colateral Total no Nexus | $100K | $300K | $3M+ |
| Senders Ativos/Mês | 0–50 (controlado) | 500 | 5.000+ |
| GTV Mensal | $25K | $350K | $5M+ |
| Pricing (canônico) | Tiered | Tiered | Tiered |
| Receita Mensal (Plataforma) | $75 | $10.5K | $175K |
| CAC Sender | $5 (referral) | $8 | $12 |
| CAC Exchanger | $50 (manual) | $30 | $15 |
| NPS (meta) | > 50 | > 65 | > 75 |

> *Valores de receita na linha “Receita Mensal (Plataforma)” derivam de modelo anterior de fases; recalibrar folhas financeiras ao canônico Dominância/Tiered e à repartição em próxima revisão de DRE.*

---

## 8. Riscos do Cold Start e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Exchangers com colateral insuficiente | Alta | Alto | Limite mínimo de $500 + verificação em tempo real |
| Sender faz chargeback no On-Ramp | Média | Médio | Parceria com Alchemy Pay que absorve esse risco |
| Exchanger demora no payout | Média | Alto | Time-lock 300s + penalidade automática de reputação |
| Regulação BR bloqueia operação | Baixa | Alto | Operar via VASP licenciada (Resolução BCB 519) |
| Concorrente (Wise/Remitly) ataca com preço | Alta | Médio | Vantagem estrutural: crowdsourced liquidity = custo menor |
| Fraud tentativa no marketplace | Média | Alto | Colateral pré-depositado + KYF on-chain via Chainalysis |

---

## 9. Orçamento Estimado — Fase 1 e 2

| Item | Custo Estimado |
|---|---|
| Sumsub KYC (150 Exchangers + 500 Senders) | $875 |
| Alchemy Pay On-Ramp (integração) | $0 (rev share) |
| Privy (500 MAU) | ~$200/mês |
| Embaixadores de comunidade (3 × $200/mês) | $600/mês |
| Yield garantido Fase 1 (500 ordens × $5 avg) | $2.500 (one-time) |
| Afiliados Micro-influenciadores (50 Exchanger × $50) | $2.500 |
| Infrastructure (Polygon, Alchemy RPC, AWS) | ~$800/mês |
| **Total Runway necessário para MVP validado** | **~$15.000** |

> **Nota:** Este orçamento assume que o eng. de smart contract e o backend foram desenvolvidos anteriormente. O cold start não exige capital institucional — exige execução de rede.

---

*Documento gerado por Antigravity — FLUXUS Growth Team*
*Versão 1.0 — Abril 2026*
