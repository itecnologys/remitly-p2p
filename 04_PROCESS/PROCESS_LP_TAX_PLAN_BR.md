# Guia Tributário FLUXUS: Planejamento para o Liquidante (LP)

> **Tipo de artefacto:** Enquadramento fiscal do **LP** (PF) com tese de isenção até **R$ 35.000/mês** em alienações. **Não** é o DRE agregado de 100 LPs — ver `02_INVESTOR/INVESTOR_DRE_CASE_STUDY_100.md` e `05_SCRIPTS/SCRIPT_SIMULATOR_100_LPS*.py`.

**Território:** Brasil | **Regulamentação:** Instrução Normativa RFB nº 1.888

## 1. Natureza Jurídica dos Ganhos
Os lucros gerados pelo LP no protocolo FLUXUS são classificados como **Ganho de Capital em Alienação de Criptoativos**, uma vez que a operação envolve a valorização e o giro de Stablecoins (USDT/USDC).

## 2. Regra de Isenção (Pessoa Física)
A legislação brasileira (Art. 22 da Lei nº 9.250/95) estabelece isenção de Imposto de Renda sobre o ganho de capital na alienação de bens de pequeno valor.

> [!IMPORTANT]
> **Limite de Isenção:** Vendas/Alienações totais de até **R$ 35.000,00 por mês**.
> - Se o somatório das alienações (giro) no mês for inferior a R$ 35k, o lucro é **isento**.
> - No cenário FLUXUS, o "giro" é o valor convertido de volta para BRL.

## 3. Alíquotas (Acima da Isenção)
Caso o LP exceda o limite de isenção de R$ 35k/mês, aplica-se a tabela progressiva de Ganho de Capital (GCAP):
- Até R$ 5 milhões: **15%**
- De R$ 5 mi a R$ 10 mi: **17,5%**
- De R$ 10 mi a R$ 30 mi: **20%**
- Acima de R$ 30 mi: **22,5%**

## 4. Declaração Obrigatória (IN 1888)
Independentemente de pagar imposto ou não, o LP deve observar as regras de reporte:
1. **Operações em Exchanges Nacionais (VASPs parceiras da Fluxus):** A própria VASP reporta à Receita Federal. O LP apenas informa na Declaração Anual.
2. **Operações em Exchanges Estrangeiras ou P2P:** Se o volume mensal ultrapassar R$ 30k, o LP deve realizar a declaração mensal via sistema Coleta Nacional.

## 5. Simulação do Estudo de Caso (100 LPs)
Em nossa simulação de 100 LPs:
- A maioria dos LPs iniciou com R$ 1k - 25k.
- Devido ao efeito de juros compostos, alguns atingiram lucros acumulados expressivos (ex: R$ 400k/ano).
- **Estratégia Recomendada:** Para manter a isenção, o LP deve orquestrar saques (re-liquidação fiat) que não ultrapassem R$ 35.000,00 por mês-calendário.

---
*Este documento tem caráter informativo. Recomendamos consulta a um contador especializado em ativos digitais.*
