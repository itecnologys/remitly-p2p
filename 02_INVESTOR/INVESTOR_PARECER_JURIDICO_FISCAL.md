# FLUXUS — Parecer Jurídico-Fiscal (Brasil)
**Natureza:** Análise Interna de Due Diligence Jurídica
**Versão:** 1.0 | **Data:** Abril 2026
**Classificação:** Confidencial

> ⚠️ **AVISO IMPORTANTE:** Este documento é uma análise técnica interna preparada para orientação estratégica e due diligence. **Não substitui opinião de advogado regularmente inscrito na OAB.** Recomenda-se a contratação de escritório especializado em direito regulatório financeiro e tributário para opinião formal antes de qualquer captação de investimento ou operação.

---

## 1. Sumário Executivo

O modelo FLUXUS opera em uma camada de **orquestração tecnológica**, sem deter ativos financeiros próprios, sem realizar câmbio direto e sem emitir instrumentos de pagamento. Essa estrutura oferece ao projeto um posicionamento jurídico favorável no Brasil, especialmente à luz do **Marco Legal dos Criptoativos (Lei nº 14.478/2022)** e das **Resoluções BCB 519, 520 e 521 (2026)**.

Contudo, três questões jurídicas centrais precisam ser respondidas com precisão para que o modelo opere com segurança legal plena:

1. **A plataforma FLUXUS é uma PSAV (Prestadora de Serviços de Ativos Virtuais)?** → E quais obrigações isso implica?
2. **Como o Exchanger (Investidor P2P) é qualificado fiscal e juridicamente?** → Pessoa Física ou Jurídica? Que imposto incide sobre o yield?
3. **O spread capturado pela plataforma tem natureza de câmbio ilegal?** → Ou é uma taxa de serviço tecnológico legítima?

---

## 2. Enquadramento da Plataforma FLUXUS

### 2.1 Natureza Jurídica do FLUXUS

O FLUXUS **não** se enquadra como:
- Banco ou Instituição de Pagamento (IP) → não emite moeda eletrônica, não detém conta de pagamento de usuários em moeda corrente
- Corretora de Câmbio → não opera compra/venda de moeda estrangeira diretamente
- Exchange de Cripto → não opera um order book próprio de ativos digitais

O FLUXUS **se enquadra como:**
- **Plataforma de Tecnologia (Software)** que orquestra terceiros
- **Possivelmente PSAV** sob a Lei 14.478/2022, dependendo da interpretação do BCB sobre "prestação de serviços de conversão de ativos virtuais"

### 2.2 A Questão da PSAV

A Lei nº 14.478/2022 define PSAV como toda pessoa jurídica que presta, como atividade principal ou secundária, serviços de:
- Intercâmbio entre ativos virtuais e moeda nacional ou estrangeira
- Transferência de ativos virtuais

**Análise de risco:**
- Se o BCB interpretar que o FLUXUS "intermedia" a conversão de USDT para BRL, ele será classificado como PSAV e precisará de autorização (Resolução BCB 519).
- A estratégia de mitigação é operar em regime de **White Label**, acoplado a VASPs já autorizadas, onde **a VASP é a PSAV**, e o FLUXUS é apenas o software de orquestração.

**Estrutura Recomendada (Curto Prazo):**
```
FLUXUS (Software/Tecnologia)
    ↓ fornece protocolo de orquestração
VASP Parceira (PSAV autorizada BCB)
    ↓ realiza o câmbio e o payout
Destinatário Final (recebe BRL via PIX)
```

Nessa estrutura, o FLUXUS fatura uma **taxa de licenciamento de software / API** da VASP, que é fiscal e juridicamente inequívoca.

### 2.3 Marco Legal 2026 — Resoluções BCB

| Resolução | Conteúdo | Impacto no FLUXUS |
|---|---|---|
| **BCB nº 519** | Autorização de PSAVs. | FLUXUS opera via parceiros autorizados até obter sua própria licença. |
| **BCB nº 520** | Segregação de patrimônio cliente/empresa. Os Minihashes provam esta segregação matematicamente. | **VANTAGEM COMPETITIVA**: FLUXUS já atende por design. |
| **BCB nº 521** | Permite uso de ativos virtuais em câmbio oficial. | **HABILITADOR CHAVE**: legitima o uso de USDT como transporte de valor no modelo. |

---

## 3. Enquadramento Fiscal do Exchanger (Investidor P2P)

### 3.1 O Problema

O Exchanger deposita USDT no sistema, recebe uma ordem de payout (transfere BRL ao destinatário via PIX de sua conta pessoal) e recebe de volta USDT + spread. A questão é: **qual a natureza dessa receita para o Exchangers?**

### 3.2 Análise por Regime

**Cenário A — Exchanger Pessoa Física (CPF)**

O ganho obtido pelo Exchanger pode ser interpretado pela Receita Federal como:

| Natureza Possível | Alíquota | Risco |
|---|---|---|
| Ganho de Capital (Art. 21, Lei 8.981/95) | 15% a 22.5% progressivo | Médio — exige apuração mensal |
| Rendimentos de Capital (Art. 36, RIR) | 22.5% (Carnê-Leão se do exterior) | Médio |
| Rendimentos de Criptoativos (IN RFB 1.888/2019) | 15% a 22.5% | Baixo — legislação já clara |

**Tese mais favorável (Pessoa Física):** Enquadrar o yield do Exchanger como **rendimentos de criptoativos** sob a IN RFB 1.888/2019. O Exchanger declara mensalmente as transações via GCAP (Ganhos de Capital) ou DIRPF. A plataforma emite **relatório mensal de operações** para facilitar a declaração.

> **Obrigação FLUXUS:** Emitir comprovante de rendimentos do Exchanger ao final de cada ano, discriminando o valor total em BRL das operações e o yield recebido.

**Cenário B — Exchanger Pessoa Jurídica (CNPJ)**

Se o Exchanger for pessoa jurídica (recomendado para quem opera acima de R$ 5.000/mês de yield):

- **Lucro Presumido:** Alíquota efetiva total de ~14.5% sobre o faturamento bruto (IRPJ + CSLL + PIS/Cofins). É o regime mais eficiente para essa atividade.
- **Simples Nacional:** Possível se a atividade não for enquadrada como "operações financeiras" (limite de faturamento: R$ 4.8M/ano).
- **Lucro Real:** Desnecessário na maioria dos casos.

**Recomendação para Exchangers que operam com escala:** Constituir uma **empresa de serviços de tecnologia ou consultoria financeira no Simples ou Lucro Presumido**, com CNAE: 6619-3/99 (Outras atividades auxiliares dos serviços financeiros).

---

### 3.3 O Risco da "Operação de Câmbio Ilegal"

**A questão mais crítica:** Um Exchanger que recebe e paga em moeda estrangeira (USDT) e em BRL sem ser uma instituição autorizada pelo BCB pode ser enquadrado como **"doleiro"** (Art. 22, parágrafo único, Lei 7.492/86)?

**Análise:**
- A lei pune quem "opera câmbio sem autorização do Banco Central".
- O Exchanger no FLUXUS **não compra nem vende moeda estrangeira**. Ele provê **liquidez em stablecoin** (um ativo virtual, não moeda estrangeira legalmente falando) e recebe um **pagamento em BRL como fee de serviço**.
- A Resolução BCB nº 521 permite explicitamente o uso de ativos virtuais em operações cambiais quando intermediados por VASP autorizada.

**Tese de defesa:**
O Exchanger é um **prestador de serviço de liquidez tecnológica**. Sua relação com o FLUXUS é contratual (contrato de prestação de serviços / SLA). Ele não está "operando câmbio"; ele está fornecendo infraestrutura de pagamento local para um protocolo de tecnologia licenciado a uma VASP autorizada.

**Mitigação necessária:**
- Contrato formal entre FLUXUS e cada Exchanger (Termo de Participação na Rede)
- Cláusula explícita de que o Exchanger está "prestando serviços de liquidez tecnológica", não realizando operação de câmbio
- O PIX emitido pelo Exchanger deve ter descritivo padronizado (ex: "Serviço FLUXUS Ref#XXXXX")

---

## 4. Enquadramento Fiscal da Receita da Plataforma FLUXUS

### 4.1 Receita da Orchestration Fee (1.0% sobre GTV)

A receita da plataforma tem natureza de **prestação de serviços de tecnologia** (SaaS/API).

**Regime Recomendado para a Holding FLUXUS:** Lucro Presumido

| Imposto | Base de Cálculo | Alíquota | Observação |
|---|---|---|---|
| IRPJ | 8% do faturamento (presunção) | 15% + 10% adicional | Presunção de lucro de 8% para serviços de tecnologia |
| CSLL | 32% do faturamento | 9% | Presunção mais alta para serviços |
| PIS | Faturamento bruto | 0.65% | Regime cumulativo |
| Cofins | Faturamento bruto | 3.0% | Regime cumulativo |
| ISS | Faturamento bruto | 2–5% (varia por município) | Base: "serviços de processamento de dados" |
| **Total Aproximado** | | **~14–16%** | Varia com ISS municipal |

> **Otimização possível:** Headquartering em municípios com ISS mínimo de 2% (ex: Barueri-SP, Itajaí-SC). Redução de ~3% na carga total.

### 4.2 Receita de MDR/Interchange (Card Business)

A receita de interchange gerada pelo uso dos cartões é mais complexa:
- Tratada como **receita financeira** se for intercâmbio formal com Visa/Mastercard.
- Incluída no Lucro Presumido com presunção de 38.4% de margem.
- Alíquota efetiva sobre receita bruta: ~16–18%.

---

## 5. Estrutura Societária Recomendada

Para blindar o modelo jurídico, a estrutura recomendada é:

```
┌─────────────────────────────────────────┐
│  FLUXUS HOLDINGS Ltda (Holding)         │
│  Lucro Presumido — CNPJ BR              │
│  Sócios: Fundadores + Futuros Investidores │
└────────────────┬────────────────────────┘
                 │
       ┌─────────┴──────────┐
       │                    │
┌──────▼──────┐      ┌──────▼──────┐
│ FLUXUS TECH │      │ FLUXUS OPS  │
│ Ltda        │      │ Ltda        │
│ (Protocolo  │      │ (Rede de    │
│ e Software) │      │ Exchangers) │
│ ISS 2%      │      │ Op. local   │
└─────────────┘      └─────────────┘
```

- **FLUXUS TECH:** Detém o software, os smart contracts, licenças de parceiros (Sumsub, Fireblocks, Marqeta). Fatura as VASPs pelo uso do protocolo.
- **FLUXUS OPS:** Gerencia o relacionamento com Exchangers, emite os relatórios fiscais, assina os contratos de participação na rede.

---

## 6. Obrigações Acessórias e Compliance Fiscal

| Obrigação | Base Legal | Frequência | Responsável |
|---|---|---|---|
| Declaração de Operações com Criptoativos | IN RFB 1.888/2019 | Mensal (se >R$ 30K/mês) | FLUXUS OPS |
| SPED Contábil / ECD | Lei 8.218/91 | Anual | FLUXUS TECH |
| DECRED (Declaração de Informações sobre Movimentação Financeira) | IN RFB 1.571/2015 | Anual | FLUXUS OPS |
| Relatório de Atividade Suspeita (RAS) | COAF Resolução 36/2021 | Quando identificado | FLUXUS OPS |
| Cadastro no COAF | Law 9.613/98 (PLD/FT) | Uma única vez (registro) | FLUXUS HOLDINGS |

**Nota sobre COAF:** O FLUXUS, ao intermediar transações com ativos virtuais, tem **obrigação legal de se cadastrar no COAF** e implementar política de PLD (Prevenção à Lavagem de Dinheiro). Essa obrigação existe independentemente de ser classificado como PSAV. O Minihash/Macrohash facilitam tremendamente o cumprimento, mas a política formal precisa existir documentalmente.

---

## 7. Riscos Jurídicos Residuais e Ações Mitigadoras

| Risco | Nível | Ação Necessária |
|---|---|---|
| Reclassificação do FLUXUS como PSAV pelo BCB | Médio | Iniciar processo de autorização BCB 519 em paralelo |
| Exchanger PF autuado por câmbio irregular | Médio-Alto | Formalizar Termo de Participação em Rede com cláusula de serviço de liquidez |
| Autuação fiscal sobre yield do Exchanger PF | Médio | Emitir relatório mensal e orientar Exchangers sobre GCAP |
| Operação de câmbio sem autorização (dolarização) | Baixo (se estrutura VASP correta) | Garantir que a VASP parceira é quem faz o câmbio formal |
| Responsabilidade por fraude do Exchanger | Baixo | Contrato + KYC rigoroso + colateral on-chain |

---

## 8. Próximos Passos Jurídicos Recomendados (Antes da Captação)

### Prazo Imediato (30 dias)
- [ ] Contratar escritório especializado (sugestão de perfil: Haddad Advogados, Stocche Forbes ou Machado Meyer — todos com prática em fintech e cripto)
- [ ] Emitir Opinião Legal Formal sobre enquadramento do FLUXUS como PSAV ou não
- [ ] Redigir o Termo de Participação em Rede para Exchangers

### Prazo Curto (60–90 dias)
- [ ] Registrar FLUXUS TECH e FLUXUS OPS no CNPJ com CNAEs adequados
- [ ] Cadastro no COAF
- [ ] Implementar Política Formal de PLD/FT (documento interno)
- [ ] Definir município de sede para otimização de ISS

### Prazo Médio (6–12 meses)
- [ ] Protocolar pedido de autorização BCB 519 (via VASP parceira ou diretamente)
- [ ] Estruturar regime tributário definitivo com contabilidade especializada em cripto
- [ ] Avaliar restructuring internacional (holding em Portugal ou Cayman) se captação for de fundos estrangeiros

---

## 9. Referências Normativas

| Norma | Ementa |
|---|---|
| Lei nº 14.478/2022 | Marco Legal dos Criptoativos no Brasil |
| Resolução BCB nº 519/2024 | Autorização e funcionamento de PSAVs |
| Resolução BCB nº 520/2024 | Governança e segregação patrimonial de PSAVs |
| Resolução BCB nº 521/2024 | Criptoativos no mercado de câmbio oficial |
| IN RFB nº 1.888/2019 | Obrigações dos exchanges e usuários de criptoativos |
| Lei nº 7.492/1986 | Crimes contra o Sistema Financeiro Nacional |
| Lei nº 9.613/1998 | Lavagem de dinheiro e prevenção |
| COAF Resolução nº 36/2021 | Comunicações ao COAF para prestadores de serviços de ativos virtuais |

---

*Análise preparada por Antigravity — FLUXUS Legal & Compliance Team*
*Versão 1.0 — Abril 2026*
*Esta análise deve ser validada por advogado inscrito na OAB antes de uso institucional.*
