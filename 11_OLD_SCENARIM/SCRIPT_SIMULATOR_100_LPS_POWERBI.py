import csv
import json
import os
import random
from pathlib import Path

# Configurações da Simulação
NUM_LPS = 100
MONTHS = 12
DAYS_PER_MONTH = 20  # Apenas dias úteis (5 dias/semana)

def get_wise_cet_benchmark(gtv_usd):
    """Retorna o CET estimado da Wise baseado nos benchmarks auditados."""
    if gtv_usd <= 100: return 0.0273
    if gtv_usd <= 200: 
        ratio = (gtv_usd - 100) / 100
        return 0.0273 - (ratio * (0.0273 - 0.0184))
    if gtv_usd <= 1000:
        ratio = (gtv_usd - 200) / 800
        return 0.0184 - (ratio * (0.0184 - 0.0116))
    if gtv_usd <= 20000:
        ratio = (gtv_usd - 1000) / 19000
        return 0.0116 - (ratio * (0.0116 - 0.0098))
    return 0.0094

# Custos Dock (Métricas de Mercado) - Rateio 50/50
DOCK_RELOAD = 2.00 # R$ 1.00 para a Fluxus, R$ 1.00 para o LP
NETWORK_COST_AVG = 0.05 

def run_simulation_with_audit():
    lps = []
    audit_data = []
    usd_rate = 4.98
    iof_rate = 0.0038
    lp_share_pct = 0.75 # REGRA DO PIONEIRO (COLD START)
    
    # Inicialização dos LPs
    for i in range(NUM_LPS):
        initial_cap = round(random.uniform(5000, 50000), 2)
        lps.append({
            "id": f"LP_{i+1:03d}",
            "initial_capital": initial_cap,
            "current_capital": initial_cap,
            "total_cycles": 0,
            "total_profit": 0
        })

    total_gtv = 0
    print(f"Iniciando Stress Test Dominância Híbrida (10% Retail / 5% Whale)...")

    for month in range(1, MONTHS + 1):
        for day in range(1, DAYS_PER_MONTH + 1):
            for lp in lps:
                cycles = random.randint(1, 3)
                lp["total_cycles"] += cycles
                
                for cycle in range(1, cycles + 1):
                    tx_value_brl = (lp["current_capital"] * 0.95) / cycles
                    tx_value_usd = tx_value_brl / usd_rate
                    
                    # Motor de Precificação
                    wise_cet = get_wise_cet_benchmark(tx_value_usd)
                    
                    if tx_value_usd <= 1000:
                        target_cet = wise_cet * 0.90
                        compliance_note = "DOMINÂNCIA_10PCT_RETAIL | 10% OFF Wise"
                    else:
                        target_cet = wise_cet * 0.95
                        compliance_note = "DOMINÂNCIA_5PCT_WHALE | 5% OFF Wise"
                    
                    applied_spread = target_cet - iof_rate
                    
                    # Cálculo de Taxas
                    fluxus_service_fee_brl = tx_value_brl * applied_spread
                    lp_gain_raw_brl = fluxus_service_fee_brl * lp_share_pct
                    iof_cost_brl = tx_value_brl * iof_rate
                    
                    # No Cold Start, Fluxus subsidia manutenção (Dock)
                    lp_maint_cost = 0.0
                    fluxus_maint_cost = (DOCK_RELOAD / 2) + (NETWORK_COST_AVG / 2)
                    
                    # Lucro Líquido do LP (75% share paga o seu próprio IOF)
                    lp_net_profit = lp_gain_raw_brl - iof_cost_brl
                    
                    # Fluxus Net Margin
                    fluxus_net = (fluxus_service_fee_brl * (1 - lp_share_pct)) - fluxus_maint_cost
                    
                    # Auditoria (Schema Legado para compatibilidade web)
                    audit_data.append({
                        "rematch_id": f"RM-ST-{month:02d}-{day:02d}-{lp['id']}-{cycle}",
                        "data_operacao": f"2025-{month:02d}-{day:02d}",
                        "timestamp_remessa_iso": f"2025-{month:02d}-{day:02d}T12:00:00",
                        "lp_id": lp["id"],
                        "gtv_brl": round(tx_value_brl, 2),
                        "usd_brl_ptax_mid": usd_rate,
                        "spread_total_brl_3_5pct": round(fluxus_service_fee_brl, 2), # Rótulo legado
                        "lp_spread_brl_42_8pct": round(lp_gain_raw_brl, 2), # Rótulo legado (agora 75%)
                        "iof_governo_brl": round(iof_cost_brl, 2),
                        "status_explicacao_pt": compliance_note,
                        "lp_current_capital": round(lp["current_capital"], 2)
                    })
                    
                    # Atualização de Capital
                    lp["current_capital"] += lp_net_profit
                    lp["total_profit"] += lp_net_profit
                    total_gtv += tx_value_brl

    # Gravação do CSV de Auditoria
    repo_root = Path(__file__).resolve().parents[1]
    csv_path = repo_root / "06_DATA" / "DATA_STRESS_TEST_AUDIT_LOG_POWERBI.csv"
    keys = audit_data[0].keys()
    with open(str(csv_path), "w", newline="", encoding="utf-8") as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(audit_data)
    
    print(f"Sucesso: {len(audit_data)} transações gravadas em {csv_path.resolve()}")

if __name__ == "__main__":
    run_simulation_with_audit()
