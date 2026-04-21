# FLUXUS Remit — Canónico de spread e repartição (OLD SCENARIO: 0,8% fixo)

**Versão:** 1.0 | **Classificação:** Uso interno / arquivo histórico  
**Status:** OLD SCENARIO — substituído pela política Dominância/Tiered (ver `03_TECHNICAL/TECH_FLUXUS_PRICING_CANON.md`).

---

## 1. Fonte da verdade (spread ao remetente)

- **Taxa de Serviço FLUXUS (Spread Operacional):** **0,8%** sobre o montante da ordem.
- **Encargos Fiscais (IOF):** **0,38%** (Extra-Spread). O custo total efetivo (CET) para o remetente é de aproximadamente **1,18%**.

Este valor posiciona o FLUXUS como **líder mundial em custo**, mantendo uma margem saudável para os LPs e para a plataforma.

---

## 2. Repartição do spread total (do “bolo” de 0,8%)

A fatia **0,8%** é repartida proporcionalmente para garantir a sustentabilidade de todos os atores:

| Destino | % do spread (0,8%) | Aprox. % sobre notional |
|--------|-------------------|-----------------------------------------------|
| **LP / Exchanger (yield)** | 42,8% | ~**0,342%** |
| **VASP / trilho local** | 28,6% | ~**0,229%** |
| **Plataforma FLUXUS** | 28,6% | ~**0,229%** |

**Exemplo (notional US$ 1.000, spread efetivo = 0,8%):**

- Spread em valor: US$ 8,00  
- LP: US$ 3,42 | VASP: US$ 2,29 | Plataforma: US$ 2,29

Reserva de estabilidade, prémios de velocidade ou ajustes por volatilidade **consomem** estas fatias ou são contabilizados **dentro** delas — não introduzir segundo “spread total” em documentação de produto sem atualizar este canónico.

---

## 3. Corredor e liquidação

- **Corredor** inclui **PIX (ou equivalente instantâneo)** e **cartão / push-to-card** conforme região — ver `TECH_GLOBAL_PIX_ARCHITECTURE.md` e `TECH_LIQUIDATION_BARRIERS.md`.
- O fluxo de ledger e estados mantém-se em `TECH_REMIT_FLOW_ARCHITECTURE.md` e `TECH_STATE_MACHINE_REVERSAL.md`.

---

## 4. SLAs (referência cruzada)

- Janela operacional de falha/reversão e consistência **300 s / 15 min** estão harmonizadas em `TECH_STATE_MACHINE_REVERSAL.md` e `TECH_API_LOGIN_TOKENIZATION.md` (não duplicar valores conflituosos noutros docs).

---

## 5. O que não é este documento

- **Tributação LP (R$ 35k/mês, etc.):** `04_PROCESS/PROCESS_LP_TAX_PLAN_BR.md`.
- **DRE stress 100 LPs:** `02_INVESTOR/INVESTOR_DRE_CASE_STUDY_100.md` (métricas de simulação; spread agregado ao cliente continua a obedecer a este canónico quando citado).
- **NEXUS / MDR 2,5%** e logs em `Outro Projeto-nao considerar/` ou `session_logs/`: produto à parte.

---

*Arquivo histórico: Abril 2026 — canônico de spread fixo 0,8% (CET ~1,18%).*
