import json
import os
import random
from pathlib import Path

# Configurações da Simulação
NUM_LPS = 100
MONTHS = 12
DAYS_PER_MONTH = 20  # Apenas dias úteis (5 dias/semana)
USD_RATE = 4.98

def get_fluxus_spread_pct(amount_usd):
    v = float(amount_usd or 0)
    if v <= 0:
        return 0.0
    if v <= 100:
        return 0.0108
    if v <= 1000:
        t = (v - 100) / 900
        return 0.0108 + t * (0.0073 - 0.0108)
    if v <= 5000:
        t = (v - 1000) / 4000
        return 0.0073 + t * (0.0060 - 0.0073)
    if v <= 20000:
        t = (v - 5000) / 15000
        return 0.0060 + t * (0.0055 - 0.0060)
    if v <= 100000:
        t = (v - 20000) / 80000
        return 0.0055 + t * (0.0050 - 0.0055)
    return 0.0050

# Repartição do Spread (conforme TECH_MATCHING_ENGINE_PROTOCOL.md)
LP_SHARE = 0.428
VASP_SHARE = 0.286
FLUXUS_SHARE = 0.286

# Taxas Adicionais
POOL_FEE_RATE = 0.02 # 2% sobre GTV (Reserva de Estabilidade)

# Custos Dock (Métricas de Mercado)
DOCK_ISSUANCE = 15.00
DOCK_RELOAD = 2.00
DOCK_MAINTENANCE = 2.50

# Custos de Rede (Blockchain)
NETWORK_COST_AVG = 0.05 # R$ 0.05 por transação (considerando gas médio + RPC)

def run_simulation():
    lps = []
    
    # Inicialização dos LPs
    for i in range(NUM_LPS):
        lps.append({
            "id": f"LP_{i+1:03d}",
            "initial_capital": round(random.uniform(1000, 25000), 2),
            "current_capital": 0,
            "total_cycles": 0,
            "total_profit": 0,
            "tax_due": 0
        })
        lps[i]["current_capital"] = lps[i]["initial_capital"] - DOCK_ISSUANCE # Paga emissão no dia 0

    monthly_stats = []
    fluxus_total_revenue = 0
    fluxus_total_opex = 0
    pool_total_reserve = 0

    for month in range(1, MONTHS + 1):
        month_gtv = 0
        month_lp_profit = 0
        
        for day in range(1, DAYS_PER_MONTH + 1):
            # Lógica de Volume (picos no início do mês e segundas-feiras)
            volume_multiplier = 1.0
            if day <= 5: volume_multiplier = 1.8 # Payday peak
            if day % 5 == 1: volume_multiplier *= 1.3 # Monday peak (approx)

            for lp in lps:
                # Número de ciclos diários (1 a 6)
                cycles = random.randint(1, 6)
                lp["total_cycles"] += cycles
                
                for _ in range(cycles):
                    # O valor de cada transação é o capital disponível / ciclos (aproximadamente)
                    tx_value = (lp["current_capital"] * 0.8) / cycles # Usa 80% para segurança de margem
                    
                    # Cálculos do Ciclo
                    spread_pct = get_fluxus_spread_pct(tx_value / USD_RATE)
                    total_spread = tx_value * spread_pct
                    lp_gain = total_spread * LP_SHARE
                    fluxus_gain = total_spread * FLUXUS_SHARE
                    
                    pool_reserve = tx_value * POOL_FEE_RATE
                    
                    # Custos Operacionais
                    opex = DOCK_RELOAD + NETWORK_COST_AVG
                    
                    # Atribuição
                    lp["current_capital"] += lp_gain
                    lp["total_profit"] += lp_gain
                    
                    month_gtv += tx_value
                    month_lp_profit += lp_gain
                    fluxus_total_revenue += fluxus_gain
                    fluxus_total_opex += opex
                    pool_total_reserve += pool_reserve

        # Custos mensais de manutenção Dock
        fluxus_total_opex += (NUM_LPS * DOCK_MAINTENANCE)

        monthly_stats.append({
            "month": month,
            "gtv": round(month_gtv, 2),
            "lp_profit": round(month_lp_profit, 2),
            "fluxus_net": round(fluxus_total_revenue - fluxus_total_opex, 2)
        })

    # Cálculo Tributário Final (Simplificado BR)
    total_tax = 0
    for lp in lps:
        # Se lucro médio mensal > 35k (Raro neste cenário de cap 25k)
        avg_monthly_profit = lp["total_profit"] / MONTHS
        if avg_monthly_profit > 35000:
            lp["tax_due"] = lp["total_profit"] * 0.15
        else:
            lp["tax_due"] = 0
        total_tax += lp["tax_due"]

    result = {
        "summary": {
            "total_gtv": round(sum(m["gtv"] for m in monthly_stats), 2),
            "total_fluxus_revenue": round(fluxus_total_revenue, 2),
            "total_fluxus_opex": round(fluxus_total_opex, 2),
            "total_pool_reserve": round(pool_total_reserve, 2),
            "total_lp_profit": round(sum(lp["total_profit"] for lp in lps), 2),
            "total_tax_lp": round(total_tax, 2)
        },
        "monthly_projection": monthly_stats,
        "lp_details": lps[:10] # Amostra de 10 LPs
    }

    repo_root = Path(__file__).resolve().parents[1]
    output_path = repo_root / "06_DATA" / "DATA_CASE_STUDY_100_LPS.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)
    
    print(f"Simulação concluída. Dados salvos em {output_path.resolve()}")

if __name__ == "__main__":
    run_simulation()
