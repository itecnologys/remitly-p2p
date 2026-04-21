# FLUXUS: Visão 360º — Setup Operacional e Governança

**Versão:** 1.0 | **Status:** Implementado  
**Objetivo:** Definir a matriz de responsabilidade financeira e os perfis de autorização para taxas e custos operacionais.

---

## 1. Matriz de Responsabilidade Financeira (Fair Split)

Para garantir a competitividade de **0,8% de spread total**, os custos são distribuídos para equilibrar o peso sobre os atores:

| Item de Custo | Quem Paga? | Lógica de Cálculo |
| :--- | :--- | :--- |
| **Taxa de On-Ramp** | **Sender** | 0,4% embutido na cotação de entrada. |
| **Taxa de Off-Ramp** | **LP / Receiver** | 0,4% descontado do payout/lucro. |
| **Manutenção (Dock Fix)** | **Plataforma & LP** | Rateio de 50/50 sobre taxas fixas mensais e de recarga. |
| **Orquestração SaaS** | **Sender & LP** | Dividido proporcionalmente no spread de 0,8%. |

---

## 2. Perfis de Autorização (Setup Permissions)

O ajuste das percentagens de spread e taxas de parceiros segue uma hierarquia de segurança:

### A. Admin (Platform 360View)
- **Escopo:** Global.
- **Poder:** Pode alterar o teto de spread (ex: baixar de 1,1% para 0,8%) e o multiplicador de reserva da Stability Pool.
- **Requisito:** Assinatura Multi-Sig (2/3 Admins).

### B. Partner (VASP / Corretora)
- **Escopo:** Corredor específico (ex: USA -> BR).
- **Poder:** Pode ajustar as taxas de "Last Mile" (payout local) dentro da margem permitida pelo Admin.
- **Requisito:** Autorização via API Token vinculada ao contrato de parceria.

### C. Liquidity Provider (LP)
- **Escopo:** Sua própria carteira / Pool.
- **Poder:** Pode aceitar ou recusar ordens com spreads específicos através do "Auto-Bid Config", definindo seu retorno mínimo esperado.
- **Requisito:** Chave privada do LP via Embedded Wallet (Privy).

---

## 3. Fluxo de Autorização de Taxas

1. **Requisição:** `Partner` solicita um aumento de 0,05% na taxa de Off-Ramp por volatilidade local.
2. **Validação:** O motor `Antigravity` verifica se o novo custo total ainda respeita o teto competitivo de `0,8%`.
3. **Execução:** Se aprovado, o sistema atualiza o leilão de matching instantaneamente. Se exceder o teto, exige autorização manual do `Admin`.

---
*Documento gerado por Antigravity — Engenharia de Processos FLUXUS*
