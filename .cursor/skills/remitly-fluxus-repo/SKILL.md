---
name: remitly-fluxus-repo
description: >-
  Orients work across the remitly-p2p documentation repository for FLUXUS (P2P
  remittance / Nexus, shadow-stablecoin rails, LP liquidity, Brazil fiscal
  framing). Maps numbered folders, key markdown specs, scripts, web prototype,
  and excluded paths. Use when editing or summarizing project docs, investor
  materials, technical architecture, process playbooks, Python generators, or
  the Flask dashboard under 08_WEB_SERVER; when the user says FLUXUS, NEXUS,
  remittance P2P, or remitly-p2p.
---

# remitly-p2p / FLUXUS — orientação do repositório

## Objetivo

Este repositório é principalmente **conhecimento e artefatos** (livros, investor pack, especificações técnicas, processos, dados, scripts Python, protótipo web). Não é um monólito de app único: trate cada pasta como um **domínio** e abra só o que a tarefa exige.

## Mapa rápido de pastas

| Pasta | Escopo |
|-------|--------|
| `01_BOOKS/` | Tese, enciclopédia, handbook do motor, comparações tradicional vs FLUXUS (Markdown e Word) |
| `02_INVESTOR/` | Pitch, MOU VASP, cold start GTM, DRE/case study, parecer jurídico-fiscal |
| `03_TECHNICAL/` | Specs: remit flow, PIX global, matching engine, QR, API/login/tokenização, state machine/reversão, liquidação, VASP bridge, blueprint; `session_logs/` com histórico de sessões |
| `04_PROCESS/` | Modus operandi LP, ciclo de caixa, dashboard LP, glossário técnico, plano tributário BR, handbook operacional |
| `05_SCRIPTS/` | Geração de PDF/Word, pitch deck, relatório anual, MOU, manual operacional, merge enciclopédia, simuladores 100 LPs (+ PowerBI export) |
| `06_DATA/` | CSVs, imagens, HTML de referência; stress Power BI: `DATA_STRESS_TEST_AUDIT_LOG_POWERBI.csv` |
| `09_ Simulacao web/fluxus/` | HTML tema + `server_sim.py` (8787): SQLite rematches + stress; `SCRIPT_BUILD_STRESS_AUDIT_DB.py` em `05_SCRIPTS/` |
| `07_LOGS/` | Backups de log de sessão (Markdown) |
| `08_WEB_SERVER/` | App **Flask** (`SERVER_FLUXUS_AUDIT.py`), templates HTML, `static/` (clone do tema crypto) — lê CSV em `06_DATA/` |
| Raiz | `README.md` (visão executiva), `DASHBOARD_STRESS_TEST.html`, `.cursorrules` (persona CFO/controle fiscal BR para o projeto) |

## Conceitos que o agente deve alinhar

- **FLUXUS**: remessa P2P global; stablecoin como trilho; cartão débito local como saída; investidor como provedor de liquidez (spread). **Spread total de referência ao remetente: 3,5%** — ver `03_TECHNICAL/TECH_FLUXUS_REMITTANCE_CANON.md` antes de citar outras percentagens de spread em docs de produto.
- **Shadow-Crypto / Fiat-to-Fiat**: usuário final não precisa enxergar cripto; foco em liquidação e compliance.
- **NEXUS**: vocabulário legado do marketplace de crédito evoluindo para o motor de remessas (documentos misturam os termos).
- **Governança fiscal BR** (quando `.cursorrules` ou docs falam disso): tripla referência BRL/USD/stable, retenções, lucro presumido, relatórios para investidor — sempre como **modelagem de negócio**, não conselho legal definitivo.

## Regras práticas ao responder ou editar

1. **Preferir Markdown editável** em `03_TECHNICAL/` e `04_PROCESS/` para mudanças de spec; Word/PDF/PPTX são artefatos gerados ou fontes estáticas.
2. **README na raiz** lista links com nomes genéricos; muitos arquivos reais estão nas subpastas com prefixos `BOOK_`, `TECH_`, `PROCESS_`, `INVESTOR_`. Se um link da raiz falhar, localizar pelo tema em `reference.md` ou com busca no repo.
3. **`Outro Projeto-nao considerar/`**: explícito no nome — **não** tratar como fonte canônica do FLUXUS salvo pedido explícito do usuário.
4. **Scripts**: ao alterar saídas (PDF/Word), conferir dependências no próprio script e caminhos relativos; simuladores alimentam dados em `06_DATA/`.
5. **Web**: rodar Flask a partir de `08_WEB_SERVER/`; CSV esperado relativo a `../06_DATA/` (ver `SERVER_FLUXUS_AUDIT.py`).

## Fluxo sugerido para uma tarefa nova

1. Classificar: estratégia / investor / técnico / operação / dados / web / script.
2. Abrir **no máximo** 1–3 documentos alvo (spec + glossário se houver termo ambíguo).
3. Se a mudança cruzar domínios (ex. spec técnica + impacto fiscal), cruzar com `04_PROCESS/` e `.cursorrules`, sem assumir obrigações legais.

## Material adicional

Para tabela de arquivos-chave por pasta e nomes típicos, ver [reference.md](reference.md).
