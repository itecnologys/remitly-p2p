# FLUXUS: DRE Consolidado — Estudo de Caso (100 LPs) — **Pacote BI / Excel**

> **Cópia de trabalho** do ficheiro `INVESTOR_DRE_CASE_STUDY_100.md` com extensão para **Power BI / Excel**: **pacote canónico 2025** com **100 LPs**, **3–6 ciclos aleatórios por dia com transação**, **uma linha por rematch** (~84k linhas), **macro_hash por dia civil com atividade**, minihashes ligadas ao macro, **GTV e totais DRE batendo linha-a-linha** com o quadro executivo (**R$ 1.409.813.152,46** GTV), PTAX **USD/BRL BCB** (2025-01-01 → 2025-12-31).

## BI — Pacote 2025 full (canónico)

| Artefacto | Caminho | Uso |
| :--- | :--- | :--- |
| **Workbook Excel** | `06_DATA/DATA_DRE_BI_WORKBOOK_2025.xlsx` | Abas `REFERENCIA`, `PTAX_DIARIO`, `LP_MASTER`, `REMATCHES` (amostra formatada nas primeiras linhas da aba rematches por performance de escrita). |
| **PTAX (JSON)** | `06_DATA/DATA_DRE_BI_PTAX_2025.json` | Séries consumíveis pelo Power BI; fonte documentada no JSON. |
| **LPs (JSON)** | `06_DATA/DATA_DRE_BI_LP_MASTER_2025.json` | Dimensão LP (100 registos). |
| **Rematches (CSV)** | `06_DATA/DATA_DRE_BI_REMATCHES_2025.csv` | Fact table completa: **1 linha = 1 rematch**; totais GTV / Dock reload / Orch 1% / Stability 2% alinhados ao DRE. |
| **Script regenerador** | `05_SCRIPTS/SCRIPT_BUILD_DRE_BI_EXCEL_2025_FULL.py` | Puxa PTAX BCB, regera workbook + CSV + JSON. |

### Legado (amostra Nov/2025)

| Artefacto | Caminho |
| :--- | :--- |
| Workbook amostra | `06_DATA/DATA_DRE_BI_WORKBOOK_NOV2025.xlsx` (se existir no disco) |
| Script | `05_SCRIPTS/SCRIPT_BUILD_DRE_BI_EXCEL_NOV2025.py` |

### Regras de honestidade contábil (simulação)

1. **Câmbio:** cada linha usa o **PTAX do Banco Central** (`cotacaoCompra` / `cotacaoVenda` → média) da **data da transação**, com carry-forward para dias sem cotação nova.
2. **Spread (legado do pacote BI 2025):** repartição **42,8% / 28,6% / 28,6%** sobre spread total **3,5%** do GTV do ciclo. A precificação atual do produto está em `03_TECHNICAL/TECH_FLUXUS_PRICING_CANON.md`.
3. **Minihash / Macro Hash:** `macro_hash` = **um por dia civil com atividade**; `minihash` por rematch; `vinculo_minihash_macrohash` explicita o vínculo para auditoria.
4. **Âmbito:** o pacote **2025 full** reproduz **GTV total e rubricas DRE chave** (Dock reload, Orch, Stability) **somatórios exatos** alinhados ao quadro executivo abaixo; LP profit permanece referência agregada no DRE, não necessariamente soma de colunas de spread por linha.

### Documentação de hashes (projeto)

- Estados e Minihash: `03_TECHNICAL/TECH_STATE_MACHINE_REVERSAL.md`, `03_TECHNICAL/TECH_API_LOGIN_TOKENIZATION.md`
- Macro Hash L1–L5 / fluxo: `03_TECHNICAL/TECH_REMIT_FLOW_ARCHITECTURE.md`
- Minihash vs Macrohash (visão institucional): `03_TECHNICAL/TECH_FLUXUS_BLUEPRINT.md`

---

# FLUXUS: DRE Consolidado — Estudo de Caso (100 LPs)

> **Tipo de artefacto:** Demonstração numérica / stress test com **100 LPs** e GTV agregado de simulação. **Não** é o mesmo documento que o guia de isenção tributária mensal (R$ 35k) do LP — ver `04_PROCESS/PROCESS_LP_TAX_PLAN_BR.md`.

> **Spread ao cliente (remessa):** este pacote BI 2025 usa **3,5%** como referencial de simulação. A precificação atual do produto segue Dominância/Tiered em `03_TECHNICAL/TECH_FLUXUS_PRICING_CANON.md`. Este DRE usa **1,0%** como *Orchestration Fee* sobre GTV na simulação; não duplicar como “taxa extra” ao mesmo spread.

**Período:** 12 Meses | **Cenário:** Estresse Operacional (1-6 ciclos/dia) | **Moeda:** BRL (R$)

## 1. Resumo Executivo
Este DRE reflete a performance da plataforma FLUXUS atuando como orquestradora para uma base de 100 Liquidantes (LPs) com capital reinvestido integralmente.

| Métrica | Valor Acumulado (12 Meses) |
| :--- | :--- |
| **GTV (Gross Transaction Volume)** | **R$ 1.409.813.152,46** |
| **Receita Bruta Fluxus (1% Fee)** | **R$ 14.112.229,66** |
| **Stability Pool Reserve (2% GTV)** | **R$ 28.196.263,05** |
| **Lucro Líquido dos LPs** | **R$ 21.119.001,02** |

---

## 2. Demonstração do Resultado (DRE)

### (+) RECEITA OPERACIONAL BRUTA: R$ 14.112.229,66
- **Orchestration Fees (Match Engine):** 1.0% sobre o GTV processado.

### (-) CUSTOS OPERACIONAIS (OPEX): R$ 175.966,70
Os custos são otimizados pela arquitetura *Asset-Light* e uso de infraestrutura *Serverless*.

| Item de Custo | Base de Cálculo | Valor Total |
| :--- | :--- | :--- |
| **Dock: Emissão de Cartões** | R$ 15,00 x 100 LPs | R$ 1.500,00 |
| **Dock: Taxas de Recarga (Reload)** | R$ 2,00 por Rematch | R$ 168.214,40 |
| **Dock: Manutenção de Conta** | R$ 2,50/mês por LP | R$ 3.000,00 |
| **Blockchain (Solana/Polygon Gas)** | R$ 0,05 Médio por Tx | R$ 3.252,30 |
| **VASP Bridge Fees** | *Incluso no spread do pacote BI 2025* | *(Zero no DRE Fluxus)* |

---

### (=) LUCRO LÍQUIDO OPERACIONAL: R$ 13.936.262,96
### **Margem Líquida: 98.7%**

> [!NOTE]
> **Eficiência de Rede:** A margem extremamente alta é explicada pela delegação da liquidez para terceiros (LPs) e da infraestrutura bancária para parceiros (Dock/VASP), permitindo que a Fluxus capture valor apenas pela **orquestração algorítmica**.

---

## 3. Alocação de Destino (Reserva Estratégica)
Além do lucro líquido, a operação gerou uma **Reserva de Estabilidade (Stability Pool)** de **R$ 28.196.263,05**.
- **Finalidade:** Cobertura de riscos cambiais, estornos e colaterização de rotas de alta volatilidade.
- **Custódia:** Armazenado em Vault MPC (Fireblocks) em Stablecoins pareadas ao BRL.

---
*Relatório gerado por Antigravity Finance Engine — Due Diligence Versão 1.5*
