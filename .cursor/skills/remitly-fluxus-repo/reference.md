# Referência — arquivos e convenções

## 03_TECHNICAL (specs em Markdown)

Arquivos frequentes (nomes exatos no repo):

- `TECH_FLUXUS_REMITTANCE_CANON.md` — **fonte da verdade**: spread total 3,5% (FLUXUS Remit) e repartição LP/VASP/plataforma
- `TECH_REMIT_FLOW_ARCHITECTURE.md` — fluxo de remessa
- `TECH_GLOBAL_PIX_ARCHITECTURE.md` — escala corredores / PIX
- `TECH_MATCHING_ENGINE_PROTOCOL.md` — fila / matching
- `TECH_QR_CODE_SPEC.md` — QR
- `TECH_API_LOGIN_TOKENIZATION.md` — login e tokenização
- `TECH_STATE_MACHINE_REVERSAL.md` — escrow, falhas, reversão
- `TECH_LIQUIDATION_BARRIERS.md` — barreiras de liquidação
- `TECH_VASP_RELOAD_BRIDGE.md` — ponte VASP / recarga de cartão
- `TECH_FLUXUS_BLUEPRINT.md` — blueprint longo (onboarding, parceiros, UX)
- `session_logs/` — transcrições e QA de sessão

PDFs em `03_TECHNICAL/`: literatura acadêmica P2P / crédito (referência externa).

## 04_PROCESS

- `PROCESS_MODUS_OPERANDI.md` — padrão ouro operacional (shadow-crypto)
- `PROCESS_USDT_MODUS_OPERANDI.md` — trilha Macro/Minihash e auditoria
- `PROCESS_LP_CASH_CYCLE.md`, `PROCESS_LP_DASHBOARD_SPEC.md` — LP
- `PROCESS_TECHNICAL_GLOSSARY.md` — termos
- `PROCESS_LP_TAX_PLAN_BR.md` — enquadramento fiscal BR (documento de projeto)

## 02_INVESTOR

Markdown editáveis: pitch script, cold start GTM, MOU parceria VASP, case DRE, parecer jurídico-fiscal; PDFs/DOCX como entregáveis.

## 05_SCRIPTS (Python)

Padrão de nome `SCRIPT_*.py`: todos assumem a **raiz do repositório** como `Path(__file__).parents[1]` e escrevem principalmente em `01_BOOKS/`, `02_INVESTOR/`, `04_PROCESS/`, `06_DATA/`.

- PDFs anuais / v2: leem `06_DATA/DATA_CONTENT_RAW.json`, capa `06_DATA/DATA_FLUXUS_COVER.png`, gráficos em `06_DATA/charts/`.
- Simulador FLUXUS: `06_DATA/DATA_DRE_SIMULATION.txt`.
- Simuladores 100 LPs: `06_DATA/DATA_CASE_STUDY_100_LPS.json` e `06_DATA/DATA_STRESS_TEST_AUDIT_LOG_POWERBI.csv` (SQL local: `python 05_SCRIPTS/SCRIPT_BUILD_STRESS_AUDIT_DB.py` → `09_ Simulacao web/fluxus/data/fluxus_stress.db`).
- Pitch deck autogerado: `02_INVESTOR/INVESTOR_PITCH_DECK_AUTOGEN.pptx` (imagens opcionais em `06_DATA/pitch_deck_assets/`).
- MoU Word: `02_INVESTOR/INVESTOR_MOU_VASP_PARTNERSHIP_AUTOGEN.docx`.

## 08_WEB_SERVER

- Entrada: `SERVER_FLUXUS_AUDIT.py`
- Dados: `06_DATA/DATA_STRESS_TEST_AUDIT_LOG_POWERBI.csv` (quando existir)
- Front: `templates/`, `static/`

## 01_BOOKS

Conteúdo estratégico e enciclopédico longo; versões `.md` e `.docx`.

- **Anais estratégicos (sponsors):** fonte Markdown `BOOK_STRATEGIC_ANNALS_2026.md`; regenerar com `python 05_SCRIPTS/SCRIPT_GENERATE_SPONSOR_BOOK.py` (gera `BOOK_STRATEGIC_ANNALS_AUTOGEN.docx` e copia para `BOOK_STRATEGIC_ANNALS_2026.docx`, `FLUXUS_STRATEGIC_ANNALS_2026.docx`, `LIVRO_ESTRATEGICO.docx`).
- **Angel Success / Remit Word:** `python 05_SCRIPTS/SCRIPT_CONVERT_BOOK_TO_WORD.py` (padrão Success); ou `python 05_SCRIPTS/SCRIPT_CONVERT_BOOK_TO_WORD.py 01_BOOKS/BOOK_ANGEL_REMIT_BOOK.md 01_BOOKS/BOOK_ANGEL_REMIT_BOOK.docx "cabeçalho"`.
- **DRE 100 LPs + Excel/BI (2025 full, ~84k rematches, PTAX BCB):** `python 05_SCRIPTS/SCRIPT_BUILD_DRE_BI_EXCEL_2025_FULL.py` → `06_DATA/DATA_DRE_BI_WORKBOOK_2025.xlsx` (+ `DATA_DRE_BI_REMATCHES_2025.csv`, JSON PTAX/LP). Guia: `02_INVESTOR/INVESTOR_DRE_CASE_STUDY_100_BI_NOV2025.md` (documento único; nome histórico). Amostra legada: `SCRIPT_BUILD_DRE_BI_EXCEL_NOV2025.py`.

## Exclusões

- `Outro Projeto-nao considerar/`: outro escopo (Nexus platform, Antigravity, protótipos paralelos) — ignorar por defeito.
