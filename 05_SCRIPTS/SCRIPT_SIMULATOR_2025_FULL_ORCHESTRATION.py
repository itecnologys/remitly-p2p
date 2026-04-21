import csv
import json
import random
import hashlib
from pathlib import Path
from collections import deque

# --- CONFIGURAÇÕES DO PLANO DE METAS 2025 ---
METAS = {
    1:  {"senders": 1.00, "receivers": 1.00, "lps": 1.00}, # Jan (Base 0)
    2:  {"senders": 1.12, "receivers": 1.15, "lps": 1.08}, # Feb
    3:  {"senders": 1.18, "receivers": 1.10, "lps": 1.21}, # Mar
    4:  {"senders": 1.09, "receivers": 1.19, "lps": 1.11}, # Apr
    5:  {"senders": 1.21, "receivers": 1.14, "lps": 1.15}, # May
    6:  {"senders": 1.11, "receivers": 1.20, "lps": 1.10}, # Jun
    7:  {"senders": 1.15, "receivers": 1.09, "lps": 1.19}, # Jul
    8:  {"senders": 1.19, "receivers": 1.17, "lps": 1.12}, # Aug
    9:  {"senders": 1.08, "receivers": 1.21, "lps": 1.14}, # Sep
    10: {"senders": 1.14, "receivers": 1.12, "lps": 1.09}, # Oct
    11: {"senders": 1.20, "receivers": 1.18, "lps": 1.16}, # Nov
    12: {"senders": 1.17, "receivers": 1.11, "lps": 1.20}  # Dec
}

# Configurações de Ticket
TICKET_PF_AVG = 2500.00
TICKET_PJ_AVG = 45000.00
PJ_RATIO = 0.15 # 15% das operações são PJ (mas representam grande volume)

# Parâmetros Base
BASE_LPS = 100
BASE_REMITTANCES_PER_DAY = 3850
DAYS_PER_MONTH = 22
DOCK_RELOAD = 2.00
LP_SHARE_PCT = 0.75 

def get_fluxus_spread_pct(v_usd):
    if v_usd <= 100: return 0.0108
    if v_usd <= 1000: return 0.0090
    if v_usd <= 5000: return 0.0073
    if v_usd <= 20000: return 0.0060
    return 0.0050

def run_simulation_2025():
    repo_root = Path(__file__).resolve().parents[1]
    kyc_pool_path = repo_root / "06_DATA" / "KYC_MASTER_POOL_30K.json"
    
    if not kyc_pool_path.exists():
        print("Erro: Pool KYC não encontrado.")
        return

    full_pool = json.loads(kyc_pool_path.read_text(encoding="utf-8"))
    # Dividindo pool em PJ e PF (como definido no gerador de 30k)
    pj_pool = [e for e in full_pool if e["type"] == "PJ"]
    pf_pool = [e for e in full_pool if e["type"] == "PF"]
    
    senders_pool = [e for e in full_pool if e["country"] != "BRA"]
    recipients_pool = [e for e in full_pool if e["country"] == "BRA"]

    lps = []
    # Inicialização Jan
    for i in range(1, BASE_LPS + 1):
        cap = float(random.randint(50, 500) * 100)
        lps.append({
            "id": f"LP_{i:03d}", "name": random.choice(full_pool)["name"],
            "current_capital": cap, "total_cycles": 0, "total_profit": 0
        })

    lp_queue = deque(lps)
    audit_data = []
    
    usd_rate_base = 5.85 # Média 2025
    
    print("Iniciando Simulacao de Orquestracao Mestre FLUXUS 2025...")

    for month in range(1, 13):
        meta = METAS[month]
        
        # Crescimento de LPs (Novos LPs entram na fila)
        current_num_lps = len(lps)
        target_lps = int(current_num_lps * (1 + (meta["lps"] - 1)))
        new_lps_count = target_lps - current_num_lps
        
        for i in range(new_lps_count):
            lp_idx = len(lps) + 1
            cap = float(random.randint(50, 500) * 100)
            new_lp = {
                "id": f"LP_{lp_idx:03d}", "name": random.choice(full_pool)["name"],
                "current_capital": cap, "total_cycles": 0, "total_profit": 0
            }
            lps.append(new_lp)
            lp_queue.append(new_lp)

        # Ajuste de demanda
        monthly_remittances_base = BASE_REMITTANCES_PER_DAY * meta["senders"]
        
        print(f"Mes {month:02d}: {len(lps)} LPs ativos | Meta Senders: {meta['senders']:.2f}x")

        for day in range(1, DAYS_PER_MONTH + 1):
            daily_count = int(monthly_remittances_base * random.uniform(0.95, 1.05))
            usd_rate = round(usd_rate_base + random.uniform(-0.2, 0.3), 4)

            for r_idx in range(1, daily_count + 1):
                # Ticket PF vs PJ
                if random.random() < PJ_RATIO:
                    tx_value_brl = round(random.lognormvariate(10.7, 0.4), 2) # Médio ~45k
                    is_pj = True
                else:
                    tx_value_brl = round(random.lognormvariate(7.8, 0.5), 2) # Médio ~2.5k
                    is_pj = False
                
                tx_value_usd = tx_value_brl / usd_rate
                
                # Matching Logic
                found_lp = False
                for _ in range(len(lp_queue)):
                    candidate = lp_queue[0]
                    if candidate["current_capital"] >= tx_value_brl:
                        matched_lp = lp_queue.popleft()
                        found_lp = True
                        break
                    else:
                        lp_queue.rotate(-1)
                
                if not found_lp: continue

                # Financials
                spread_pct = get_fluxus_spread_pct(tx_value_usd)
                total_spread_brl = tx_value_brl * spread_pct
                lp_profit = total_spread_brl * LP_SHARE_PCT
                platform_fee = total_spread_brl * 0.25
                
                # Senders/Receivers (Churn logic via random pool selection)
                s_pool = pj_pool if is_pj else pf_pool
                sender = random.choice(senders_pool)
                recipient = random.choice(recipients_pool)
                
                rematch_id = f"RM-{len(audit_data) + 1:07d}"
                dt_op = f"2025-{month:02d}-{day:02d}"
                ts_iso = f"{dt_op}T{random.randint(8,19):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}-03:00"
                
                # Minihash determinístico para auditoria
                m_hash = hashlib.sha256(f"{rematch_id}{matched_lp['id']}".encode()).hexdigest()
                minihash = f"MH0x{m_hash[:40]}"

                audit_data.append({
                    "rematch_id": rematch_id,
                    "data_operacao": dt_op,
                    "timestamp_remessa_iso": ts_iso,
                    "Month": month,
                    "Day": day,
                    "LP_ID": matched_lp["id"],
                    "lp_nome": matched_lp["name"],
                    "Principal_Capital": round(tx_value_brl, 2),
                    "Transaction_Value_USD": round(tx_value_usd, 2),
                    "total_protocol_spread_brl": round(total_spread_brl, 2),
                    "lp_profit_share_brl": round(lp_profit, 2),
                    "fluxus_fee_brl": round(platform_fee, 2),
                    "Minihash": minihash,
                    "sender_name": sender["name"],
                    "sender_type": sender["type"],
                    "recipient_name": recipient["name"],
                    "recipient_type": recipient["type"],
                    "usd_brl_ptax": usd_rate,
                    "status": "SETTLED"
                })

                # Atualiza capital do LP e volta pra fila
                matched_lp["current_capital"] += lp_profit
                matched_lp["total_cycles"] += 1
                lp_queue.append(matched_lp)

    # Save CSV
    out_path = repo_root / "06_DATA" / "DATA_STRESS_TEST_AUDIT_LOG_POWERBI.csv"
    keys = audit_data[0].keys()
    with open(str(out_path), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.header = True # Force write header manually if needed
        writer.writeheader()
        writer.writerows(audit_data)
    
    print(f"Sucesso! {len(audit_data)} transacoes geradas.")
    print(f"📂 Arquivo salvo em: {out_path}")

if __name__ == "__main__":
    run_simulation_2025()
