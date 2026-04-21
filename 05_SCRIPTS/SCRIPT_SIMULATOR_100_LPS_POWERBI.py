import csv
import json
import os
import random
from pathlib import Path

# Configurações da Simulação
NUM_LPS = 100
MONTH_TARGET = 1 # Janeiro
DAYS_PER_MONTH = 22 # Dias bancários conforme solicitado

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

def get_fluxus_spread_pct(gtv_usd):
    v = float(gtv_usd or 0)
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

# Custos Dock (Métricas de Mercado) - Rateio 50/50
DOCK_RELOAD = 2.00 # R$ 1.00 para a Fluxus, R$ 1.00 para o LP
NETWORK_COST_AVG = 0.05 

def run_simulation_with_audit():
    repo_root = Path(__file__).resolve().parents[1]
    kyc_pool_path = repo_root / "06_DATA" / "KYC_MASTER_POOL_30K.json"
    
    if not kyc_pool_path.exists():
        print("Erro: Pool KYC não encontrado. Rode GEN_KYC_MASTER_POOL_30K.py primeiro.")
        return

    full_pool = json.loads(kyc_pool_path.read_text(encoding="utf-8"))
    senders_pool = [e for e in full_pool if e["country"] != "BRA"]
    recipients_pool = [e for e in full_pool if e["country"] == "BRA"]

    lps = []
    audit_data = []
    # Câmbio benchmark Jan/2025 (Cenário de Estresse)
    usd_rate_base = 6.08 
    iof_rate = 0.0038
    lp_share_pct = 0.75 # REGRA DO PIONEIRO (COLD START)
    
    # Inicialização dos LPs (Aportes múltiplos de 100)
    for i in range(NUM_LPS):
        initial_cap = float(random.randint(50, 500) * 100) 
        lps.append({
            "id": f"LP_{i+1:03d}",
            "initial_capital": initial_cap,
            "current_capital": initial_cap,
            "total_cycles": 0,
            "total_profit": 0
        })

    from collections import deque
    lp_queue = deque(lps) # Criando a Fila de Fluxo

    total_gtv = 0
    print(f"Iniciando Stress Test Jan/2025 (22 Dias Bancários | 84k Transações)...")

    # Janeiro de 2025
    month = 1
    for day in range(1, DAYS_PER_MONTH + 1):
        # Alta Densidade: ~3,8k transações per dia para atingir os 84k
        daily_remittances = random.randint(3800, 3900)
        
        # Volatilidade intra-mês (5.95 a 6.20)
        usd_rate = round(usd_rate_base + random.uniform(-0.13, 0.12), 4)

        for r_idx in range(1, daily_remittances + 1):
            # Valor da remessa (Randômico baseado no perfil de mercado)
            tx_value_brl = round(random.lognormvariate(8, 0.5), 2)
            tx_value_usd = tx_value_brl / usd_rate
                
            # ENCONTRA O PRÓXIMO LP QUALIFICADO NA FILA
            matched_lp = None
            checked_count = 0
            while checked_count < len(lp_queue):
                potential_lp = lp_queue[0] # Espia o primeiro
                if potential_lp["current_capital"] >= tx_value_brl:
                    matched_lp = lp_queue.popleft() # Remove para processar
                    break
                else:
                    # STANDBY: Rotaciona mas mantém o status de prioridade para a próxima compatível
                    lp_queue.rotate(-1)
                    checked_count += 1
            
            if not matched_lp:
                # Liquidity Gap: Ninguém na fila tem saldo integral para esta remessa
                continue

            # Processamento da Remessa
            spread_pct = get_fluxus_spread_pct(tx_value_usd)
            cet_fluxus = spread_pct + iof_rate
            
            fluxus_service_fee_brl = tx_value_brl * spread_pct
            lp_gain_raw_brl = fluxus_service_fee_brl * lp_share_pct
            
            # Lucro Líquido do LP (75% share)
            lp_net_profit = lp_gain_raw_brl

            # SELEÇÃO DE KYC (RECORRÊNCIA DETERMINÍSTICA)
            # Usamos o r_idx e o day para criar hashes e escolher do pool
            sender = senders_pool[((day * 1000) + r_idx) % len(senders_pool)]
            recipient = recipients_pool[((day * 1000) + (r_idx * 7)) % len(recipients_pool)]
            
            # AML Purpose
            purposes = ["Family Support", "Real Estate", "Services", "Salaries", "B2B Trade"]
            pmt_purpose = purposes[r_idx % len(purposes)]
            
            # Auditoria (Schema para Stress Audit DB com Metadados de Fila)
            rematch_id = f"RM-{len(audit_data) + 1:06d}"
            data_operacao = f"2025-{month:02d}-{day:02d}"
            ts_iso = f"{data_operacao}T{random.randint(9,18):02d}:{random.randint(0,59):02d}:41-03:00"
            
            audit_data.append({
                "rematch_id": rematch_id,
                "data_operacao": data_operacao,
                "timestamp_remessa_iso": ts_iso,
                "Month": month,
                "Day": day,
                "LP_ID": matched_lp["id"],
                "Cycle_Num": matched_lp["total_cycles"] + 1,
                "gtv_brl": round(tx_value_brl, 2),
                "Principal_Capital": round(tx_value_brl, 2),
                "Transaction_Value": round(tx_value_brl, 2),
                "total_protocol_spread_brl": round(fluxus_service_fee_brl, 2), 
                "lp_profit_share_brl": round(lp_gain_raw_brl, 2),
                "lp_spread_brl": round(lp_gain_raw_brl, 2),
                "fluxus_orchestration_fee_brl": round(fluxus_service_fee_brl * 0.25, 2),
                "vasp_fee_brl": 0.0,
                "pool_reserve_gtv": round(tx_value_brl * 0.02, 2),
                "stability_pool_alloc_2pct_linha": round(tx_value_brl * 0.02, 2),
                "Dock_Reload_Cost": round(DOCK_RELOAD / 2, 2),
                "dock_reload_brl": round(DOCK_RELOAD / 2, 2),
                "Blockchain_Gas": round(NETWORK_COST_AVG / 2, 2),
                "Net_Fluxus_Margin": round(fluxus_service_fee_brl * 0.25 - (DOCK_RELOAD/2), 2),
                "Queue_Position": checked_count + 1,
                "usd_brl_ptax_mid": usd_rate,
                # --- NOVOS CAMPOS KYC HERCÚLEOS ---
                "sender_name": sender["name"],
                "sender_id": sender["tax_id"],
                "sender_country": sender["country"],
                "sender_bank": sender["bank_name"],
                "sender_card_bin": sender["card_bin"],
                "sender_address": sender["address"],
                "recipient_name": recipient["name"],
                "recipient_id": recipient["tax_id"],
                "recipient_type": recipient["type"],
                "recipient_sector": recipient["sector"],
                "recipient_bank": recipient["bank_name"],
                "remittance_purpose": pmt_purpose,
                "kyc_status": "VERIFIED_AML_OK"
            })
            
            # Atualização do LP e retorno para o FINAL DA FILA
            matched_lp["current_capital"] += lp_net_profit
            matched_lp["total_profit"] += lp_net_profit
            matched_lp["total_cycles"] += 1
            lp_queue.append(matched_lp) # Vai para o final da fila
            
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
