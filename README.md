# FLUXUS Global Remit: Manual Executivo do Padrão de Ouro

Seja bem-vindo ao **FLUXUS**, a evolução do Marketplace de Crédito **NEXUS** para um motor global de remessas P2P.

O FLUXUS resolve o gargalo das remessas internacionais ao transformar o investidor P2P em um provedor de liquidez de "última milha", utilizando stablecoins como trilho invisível e cartões de débito locais (ou rails instantâneos como PIX, conforme o **corredor**) como destino final.

No mesmo ecossistema de documentação mantém-se o material do **NEXUS** (crédito P2P / arranjos fechados) em `Outro Projeto-nao considerar/` e logs de sessão — ver secção "Dois produtos" abaixo.

## Dois produtos no repositório

| Produto | Descrição curta | Onde aprofundar |
|--------|------------------|-----------------|
| **FLUXUS Remit** | Remessa cross-border, LP, VASP, shadow-stablecoin | `01_BOOKS/`, `02_INVESTOR/`, `03_TECHNICAL/`, `04_PROCESS/` |
| **NEXUS** | Plataforma de crédito P2P, closed-loop, FIDC (linha paralela de docs) | `Outro Projeto-nao considerar/p2p-lending by Claude Code/nexus-platform/` e `03_TECHNICAL/session_logs/` |

## Guia de Documentação (caminhos reais no repo)

### 1. Visão e Estratégia

- [Tese de negócio / spread](01_BOOKS/BOOK_REMIT_THESIS.md) — alinhada ao [canónico de precificação (Dominância/Tiered)](03_TECHNICAL/TECH_FLUXUS_PRICING_CANON.md)
- [Modus operandi shadow-crypto](04_PROCESS/PROCESS_MODUS_OPERANDI.md)
- [Tradicional vs FLUXUS](01_BOOKS/BOOK_TRADITIONAL_VS_FLUXUS.md)
- [Manual executivo investidor anjo](01_BOOKS/BOOK_ANGEL_SUCCESS_BOOK.md)

### 2. Arquitetura Técnica

- [Canónico de precificação (Dominância/Tiered)](03_TECHNICAL/TECH_FLUXUS_PRICING_CANON.md)
- [Canónico legado (cenário antigo)](03_TECHNICAL/TECH_FLUXUS_REMITTANCE_CANON.md)
- [Fluxo de remessa + Macro Hash L1–L5](03_TECHNICAL/TECH_REMIT_FLOW_ARCHITECTURE.md)
- [Motor global tipo PIX / rails](03_TECHNICAL/TECH_GLOBAL_PIX_ARCHITECTURE.md)
- [Ponte VASP / recarga de cartão](03_TECHNICAL/TECH_VASP_RELOAD_BRIDGE.md)
- [Login, API e fila de liquidez](03_TECHNICAL/TECH_API_LOGIN_TOKENIZATION.md)
- [Matching engine](03_TECHNICAL/TECH_MATCHING_ENGINE_PROTOCOL.md)
- [Máquina de estados e reversão](03_TECHNICAL/TECH_STATE_MACHINE_REVERSAL.md)
- [QR Code global](03_TECHNICAL/TECH_QR_CODE_SPEC.md)
- [Barreiras de liquidação](03_TECHNICAL/TECH_LIQUIDATION_BARRIERS.md)
- [Blueprint operacional (longo)](03_TECHNICAL/TECH_FLUXUS_BLUEPRINT.md)

### 3. Governança, LP e Fiscal (Brasil)

- [USDT como camada de transporte](04_PROCESS/PROCESS_USDT_MODUS_OPERANDI.md)
- [Ciclo de caixa do LP](04_PROCESS/PROCESS_LP_CASH_CYCLE.md)
- [Dashboard LP (spec)](04_PROCESS/PROCESS_LP_DASHBOARD_SPEC.md)
- [Glossário técnico](04_PROCESS/PROCESS_TECHNICAL_GLOSSARY.md)
- [Guia tributário LP — isenção até R$ 35.000/mês](04_PROCESS/PROCESS_LP_TAX_PLAN_BR.md)
- [Parecer jurídico-fiscal (due diligence interna)](02_INVESTOR/INVESTOR_PARECER_JURIDICO_FISCAL.md)

### 4. Investidor, GTM e Cenários financeiros

- [Cold start / GTM](02_INVESTOR/INVESTOR_COLD_START_GTM.md)
- [Roteiro do pitch (slides)](02_INVESTOR/INVESTOR_PITCH_DECK_SCRIPT.md)
- [MoU VASP (template)](02_INVESTOR/INVESTOR_MOU_VASP_PARTNERSHIP.md)
- [DRE estudo de caso 100 LPs](02_INVESTOR/INVESTOR_DRE_CASE_STUDY_100.md) — *cenário de simulação agregada; ver nota no ficheiro*

### 5. Scripts e Dados

- [Scripts Python](05_SCRIPTS/) — geram PDF/Word, simulações; caminhos relativos à raiz do repositório
- [Dados e CSV de stress test](06_DATA/) — p.ex. `DATA_STRESS_TEST_AUDIT_LOG_POWERBI.csv` (gerado por `SCRIPT_SIMULATOR_100_LPS_POWERBI.py`)
- [Protótipo Flask / auditoria (pandas + templates)](08_WEB_SERVER/SERVER_FLUXUS_AUDIT.py) — lê o CSV de stress em tempo de arranque

### 5b. Simulação web local (pasta 09)

- [Protótipo estático + SQLite](09_ Simulacao%20web/fluxus/) — `server_sim.py` na porta **8787**: rematches DRE (`fluxus_sim.db` via `SCRIPT_BUILD_FLUXUS_SIM_DB.py`) e **stress Power BI** (`fluxus_stress.db` via `SCRIPT_BUILD_STRESS_AUDIT_DB.py`); páginas `transaction.html`, `stress-audit.html`, `index.html`
- Instruções rápidas: [09_ Simulacao web/fluxus/README_SIM.txt](09_ Simulacao web/fluxus/README_SIM.txt)

### 6. Regras do agente (Cursor)

- [`.cursorrules`](.cursorrules) — persona CFO / controle fiscal FLUXUS Brasil
- [Skill de navegação do repo](.cursor/skills/remitly-fluxus-repo/SKILL.md)

---

## Status

**Estrutura descritiva** consolidada no repositório `remitly-p2p` com pastas numeradas `01`–`08`, simulação web em **`09_ Simulacao web/`**, logs em `07_LOGS/` e material histórico em `Outro Projeto-nao considerar/`.

**Autor da narrativa principal:** ANTIGRAVITY (documentação); ajustes de caminhos e coerência de SLAs: manutenção de repositório.
