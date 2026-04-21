# FLUXUS — Glossário Técnico e Operacional
**Versão:** 1.0 | **Público:** Investidores, LPs e Parceiros Institucionais

Este documento define os termos fundamentais da engenharia financeira e tecnológica do sistema FLUXUS.

---

## 1. Métricas de Volume e Performance

### **GTV (Gross Transaction Volume)**
**Volume Bruto de Transações.** Representa a soma total de todos os valores nominais processados pela plataforma ou por um LP específico em um determinado período. 
*Exemplo:* Se você liquidou 10 ordens de R$ 1.000, seu GTV é de R$ 10.000, independentemente do lucro gerado.

### **Capital Velocity (Giro de Capital)**
A frequência com que o capital inicial de um LP é "limpo" e retorna para a conta bancária para ser reutilizado. 
*Importância:* Um giro alto permite que um capital pequeno gere um GTV grande, maximizando o ROI.

### **Netting (Compensação)**
O processo de casar ordens de sentidos opostos (Ex: Brasil -> Europa e Europa -> Brasil) para liquidar as obrigações sem a necessidade de conversão externa para Fiat. Isso elimina taxas de câmbio e de rede.

---

## 2. Entidades e Papéis

### **LP (Liquidity Provider / Liquidante)**
O agente que "aluga" sua liquidez local para o protocolo. Ele é responsável por realizar o payout final (ex: enviar o PIX) e recebe em troca ativos digitais (USDT) acrescidos de spread.

### **VASP (Virtual Asset Service Provider)**
Instituições reguladas (Exchanges) que fazem a ponte entre o mundo cripto e o sistema bancário tradicional. No FLUXUS, as VASPs são usadas para o *Auto-Refill* (recompra de Fiat).

### **Matching Engine (Motor de Casamento)**
O algoritmo proprietário que seleciona o melhor LP para cada ordem, baseando-se em Score de Reputação, Spread Ofertado e Disponibilidade de Colateral.

---

## 3. Protocolos de Auditoria

### **Minihash**
Um identificador criptográfico gerado para cada mudança de estado da transação. É a "assinatura eletrônica" que prova que o dinheiro foi enviado antes de liberar os fundos no blockchain.

### **Macrohash**
O link persistente e imutável gravado na blockchain (Polygon/Solana) que ancora todos os Minihashes de uma operação, garantindo auditabilidade total para Bancos Centrais e órgãos fiscais.

---

## 4. Operações de Fluxo de Caixa

### **Auto-Refill (Recompra Automática)**
O processo de converter automaticamente o lucro em USDT de volta para a moeda Fiat (BRL/EUR) através de uma API de VASP, devolvendo o dinheiro para a conta bancária do LP.

### **Atomic Lock (Trava Atômica)**
Mecanismo de Smart Contract que garante que, se uma parte da transação falhar, os fundos de todos os envolvidos retornem automaticamente para seus donos originais, eliminando o risco de contraparte.

### **Hybrid Allocation (Alocação Híbrida)**
Estratégia onde o LP divide seu capital entre liquidação imediata (Auto-Refill) e espera tática por ordens inversas (Netting), buscando o equilíbrio entre liquidez e maximização de lucro.

---

*Documento gerado por Antigravity — Engenharia Financeira FLUXUS.*
