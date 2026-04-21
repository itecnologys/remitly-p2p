# FLUXUS Remit — Canónico de Precificação (Dominância/Tiered) + Benchmark (Wise)

**Versão:** 2.0 | **Classificação:** Uso interno / fonte da verdade  
**Escopo:** FLUXUS Remit (remessa cross-border P2P, stablecoin + liquidação local).  
**Objetivo:** manter o FLUXUS estruturalmente mais barato e previsível no varejo, sem destruir margem no atacado.

---

## 1. Política oficial (driver)

A política oficial é **Dominância/Tiered**:

- **Driver:** a tabela de spread por faixa de volume (escada) + regras de transparência.
- **Resultado:** **CET (cliente)** varia por ticket e corredor, mas fica dentro de um envelope competitivo.
- **Benchmark:** a Wise é usada para **validação** (comparação e auditoria), não como fórmula que “dita” o preço.

Documentos de referência:

- `02_INVESTOR/INVESTOR_TIERED_PRICING_MODEL.md` (escada/canais)
- `02_INVESTOR/STRATEGY_DOMINANCE_10PCT_WISE.md` (regra 10% / 5% como critério de dominância)

---

## 2. Como calcular CET e decomposição

- **CET_FLUXUS = Spread_FLUXUS + IOF**
- **IOF (BR):** 0,38% como linha separada, sempre explícita.
- **Transparência:** PTAX mid-market, sem spread oculto no câmbio.

---

## 3. Escada de spread (fonte da verdade operacional)

Esta escada é a referência canônica de pricing (valores percentuais do notional):

| Faixa (USD) | Spread alvo (intervalo) | Regra |
|---|---:|---|
| 10 – 100 | 1,08% | Varejo com margem saudável |
| 100 – 1.000 | 1,08% → 0,73% | Interpolação por volume |
| 1.000 – 5.000 | 0,73% → 0,60% | Interpolação por volume |
| 5.000 – 20.000 | 0,60% → 0,55% | Interpolação por volume |
| 20.000 – 100.000 | 0,55% → 0,50% | Interpolação por volume |

Se houver conflito entre documentos, este canônico prevalece e a tabela deve ser atualizada antes de citar números em pitch/marketing.

---

## 4. Dominância: critério de validação (Wise)

Para cada faixa, o sistema calcula (ou audita) um **Wise_CET_Benchmark** e registra:

- **delta_abs = Wise_CET − CET_FLUXUS**
- **delta_rel = 1 − (CET_FLUXUS / Wise_CET)**

Critérios operacionais (referência):

- **Varejo:** meta de dominância mais agressiva.
- **Atacado:** meta de dominância sustentável, preservando margem do LP.

---

## 5. Repartição (LP / Plataforma / VASP)

A repartição é aplicada sobre o **Spread_FLUXUS** (não sobre o IOF):

- A regra do **Cold Start** pode privilegiar LP (ex.: share maior) sem alterar CET do cliente.
- O modelo de share não deve alterar a transparência: CET exibido ao cliente permanece “Spread + IOF”.

---

## 6. Compatibilidade com a tese

Esta mudança **não altera a tese**:

- Continua a meta de “liderança de custo” com transparência (PTAX + taxas explícitas).
- Apenas troca o “número fixo universal” por um **envelope de precificação** que domina concorrentes sem colapsar margem.
