# -*- coding: utf-8 -*-
"""
Carrega DATA_STRESS_TEST_AUDIT_LOG_POWERBI.csv (simulador 100 LPs / Power BI)
para SQLite usado pela simulação web em 09_ Simulacao web/fluxus.

Origem do CSV: SCRIPT_SIMULATOR_100_LPS_POWERBI.py
Saída: 09_ Simulacao web/fluxus/data/fluxus_stress.db

Colunas normalizadas (sem pontos nos nomes) para SQL estável.
"""
from __future__ import annotations

import csv
import sqlite3
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CSV_PATH = REPO / "06_DATA" / "DATA_STRESS_TEST_AUDIT_LOG_POWERBI.csv"
OUT_DB = REPO / "09_ Simulacao web" / "fluxus" / "data" / "fluxus_stress.db"
OUT_TMP = REPO / "09_ Simulacao web" / "fluxus" / "data" / "fluxus_stress.build.db"

DDL = """
CREATE TABLE stress_audit (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  month INTEGER NOT NULL,
  day INTEGER NOT NULL,
  lp_id TEXT NOT NULL,
  cycle_num INTEGER NOT NULL,
  principal_capital REAL,
  transaction_value REAL,
  total_spread REAL,
  lp_profit REAL,
  fluxus_fee REAL,
  vasp_fee REAL,
  pool_reserve_gtv REAL,
  dock_reload_cost REAL,
  blockchain_gas REAL,
  net_fluxus_margin REAL,
  queue_position INTEGER,
  -- KYC HERCÚLEO
  sender_name TEXT,
  sender_id TEXT,
  sender_country TEXT,
  sender_bank TEXT,
  sender_card_bin TEXT,
  sender_address TEXT,
  recipient_name TEXT,
  recipient_id TEXT,
  recipient_type TEXT,
  recipient_sector TEXT,
  recipient_bank TEXT,
  remittance_purpose TEXT,
  kyc_status TEXT,
  usd_brl_ptax_mid REAL
);
CREATE INDEX idx_stress_lp ON stress_audit (lp_id);
CREATE INDEX idx_stress_month ON stress_audit (month);
CREATE INDEX idx_stress_month_day ON stress_audit (month, day);
"""


def row_from_csv(d: dict) -> tuple:
    # d["data_operacao"] está no formato YYYY-MM-DD
    iso_date = d["data_operacao"]
    yy, mm, dd = map(int, iso_date.split("-"))
    
    gtv = float(d["gtv_brl"])
    lp_s = float(d["lp_profit_share_brl"])
    flux_f = float(d["fluxus_orchestration_fee_brl"])
    cet_total = float(d["total_protocol_spread_brl"])
    
    return (
        mm,
        dd,
        str(d.get("LP_ID", d.get("lp_id", ""))),
        int(d.get("Cycle_Num", d.get("ciclo_id", 0))),
        gtv,       # principal_capital
        gtv,       # transaction_value
        cet_total, # total_spread
        lp_s,      # lp_profit
        flux_f,    # fluxus_fee
        0.0,       # vasp_fee
        float(d.get("stability_pool_alloc_2pct_linha", 0)), # pool_reserve_gtv
        float(d.get("dock_reload_brl", 0)), # dock_reload_cost
        0.01,      # blockchain_gas (flat)
        flux_f,    # net_fluxus_margin (inicial)
        int(d.get("Queue_Position", 0)), # Posição na Fila
        # KYC
        d.get("sender_name", ""),
        d.get("sender_id", ""),
        d.get("sender_country", ""),
        d.get("sender_bank", ""),
        d.get("sender_card_bin", ""),
        d.get("sender_address", ""),
        d.get("recipient_name", ""),
        d.get("recipient_id", ""),
        d.get("recipient_type", ""),
        d.get("recipient_sector", ""),
        d.get("recipient_bank", ""),
        d.get("remittance_purpose", ""),
        d.get("kyc_status", ""),
        float(d.get("usd_brl_ptax_mid", 0))
    )


def main() -> None:
    if not CSV_PATH.is_file():
        raise SystemExit(f"CSV não encontrado: {CSV_PATH}")

    OUT_DB.parent.mkdir(parents=True, exist_ok=True)
    if OUT_TMP.is_file():
        OUT_TMP.unlink()

    con = sqlite3.connect(OUT_TMP)
    con.executescript(DDL)

    insert_sql = """
    INSERT INTO stress_audit (
      month, day, lp_id, cycle_num, principal_capital, transaction_value,
      total_spread, lp_profit, fluxus_fee, vasp_fee, pool_reserve_gtv,
      dock_reload_cost, blockchain_gas, net_fluxus_margin, queue_position,
      sender_name, sender_id, sender_country, sender_bank, sender_card_bin,
      sender_address, recipient_name, recipient_id, recipient_type,
      recipient_sector, recipient_bank, remittance_purpose, kyc_status,
      usd_brl_ptax_mid
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """

    batch: list[tuple] = []
    n = 0
    with CSV_PATH.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            batch.append(row_from_csv(row))
            n += 1
            if len(batch) >= 8000:
                con.executemany(insert_sql, batch)
                con.commit()
                batch.clear()
    if batch:
        con.executemany(insert_sql, batch)
        con.commit()

    con.close()
    if OUT_DB.is_file():
        OUT_DB.unlink()
    OUT_TMP.rename(OUT_DB)
    print(f"OK: {n} linhas -> {OUT_DB}")


if __name__ == "__main__":
    main()
