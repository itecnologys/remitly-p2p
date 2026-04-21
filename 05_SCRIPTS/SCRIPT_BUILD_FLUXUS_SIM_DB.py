# -*- coding: utf-8 -*-
"""
Constrói SQLite leve para a simulação web FLUXUS:
  - rematches (colunas do CSV oficial DATA_DRE_BI_REMATCHES_2025.csv)
  - lps (100 LPs + KYC simulado determinístico)
  - remittance_categories (>=50 categorias)
  - lp_category_slots (4 categorias por LP, uma primária)

Saída: 09_ Simulacao web/fluxus/data/fluxus_sim.db
"""
from __future__ import annotations

import csv
import hashlib
import os
import random
import shutil
import sqlite3
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CSV_PATH = REPO / "06_DATA" / "DATA_STRESS_TEST_AUDIT_LOG_POWERBI.csv"
LP_JSON = REPO / "06_DATA" / "DATA_DRE_BI_LP_MASTER_NOV2025.json"
OUT_DB = REPO / "09_ Simulacao web" / "fluxus" / "data" / "fluxus_sim.db"
OUT_DB_TMP = REPO / "09_ Simulacao web" / "fluxus" / "data" / "fluxus_sim.build.db"

CATEGORIES_PT = [
    "Família / sustento de dependentes no exterior",
    "Educação (mensalidade universidade)",
    "Saúde (hospital / procedimento)",
    "Imóvel (compra / manutenção)",
    "Investimento em ativos no exterior",
    "Freelancer / prestação de serviço B2B",
    "Salário remoto (payroll global)",
    "Reembolso corporativo",
    "Comércio exterior (importação P2P)",
    "Turismo e viagens",
    "Emergência / repatriação",
    "Doações e ONG",
    "Casamento / eventos",
    "Pensão alimentícia",
    "Royalties e licenciamento",
    "Marketplace cross-border",
    "Dropshipping fornecedor",
    "Logística portuária (taxas)",
    "Combustível e pedágio internacional",
    "Agronegócio exportação",
    "Commodities hedge",
    "Startup equity / SAFE",
    "Fusões e aquisições SME",
    "Conta offshore funding",
    "Cartão pré-pago recarga",
    "Wallet stablecoin on-ramp",
    "Off-ramp para contas locais",
    "Pagamento de fornecedores Ásia",
    "Pagamento de fornecedores Europa",
    "Pagamento de fornecedores América",
    "Remessa estudante",
    "Remessa médica urgente",
    "Remessa micro (sub US$ 200)",
    "Remessa macro (institucional)",
    "Câmbio turismo cashless",
    "Arbitragem spread capture",
    "Liquidez para exchange regional",
    "Liquidez para PSP",
    "Liquidez para fintech wallet",
    "Corredor LATAM → NA",
    "Corredor NA → UE",
    "Corredor UE → APAC",
    "Corredor intra-LATAM",
    "Corredor intra-UE",
    "Remessa B2C varejo",
    "Remessa C2C peer",
    "Pagamento de impostos no exterior",
    "Regularização cambial",
    "Trade finance curto prazo",
    "Supply chain JIT payout",
    "Gig economy payouts",
    "Gaming / creators payout",
    "Seguros e sinistros cross-border",
    "Cripto-legacy bridge (off-ramp fiat)",
]


def rng_for_lp(lp_id: str) -> random.Random:
    h = hashlib.sha256(lp_id.encode()).hexdigest()
    return random.Random(int(h[:16], 16))


def split_nome(nome_completo: str) -> tuple[str, str]:
    parts = nome_completo.strip().split()
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], " ".join(parts[1:])


def enrich_lp(row: dict) -> dict[str, object]:
    lp_id = row["lp_id"]
    r = rng_for_lp(lp_id)
    pn, sn = split_nome(row["nome_completo"])
    y0 = 1968 + (int(hashlib.md5(lp_id.encode()).hexdigest()[:4], 16) % 35)
    m = 1 + r.randint(0, 11)
    d = 1 + r.randint(0, 27)
    cep = f"{r.randint(10000, 99999):05d}-{r.randint(100, 999):03d}"
    tel = f"+55 9{r.randint(1000, 9999)}9{r.randint(1000, 9999)}"
    slug = lp_id.lower().replace("_", "")
    email = f"{slug}.lp.sim@fluxus-audit.invalid"
    usr = f"UX-{int(hashlib.md5(lp_id.encode()).hexdigest()[:6], 16) % 900000 + 100000:06d}"
    kyc_ref = f"KYC-SIM-{hashlib.sha1(lp_id.encode()).hexdigest()[:12].upper()}"
    addr = f"Rua Auditoria Simulada, {r.randint(10, 9999)} — {row.get('cidade', '')}/{row.get('estado', '')}"
    return {
        **row,
        "primeiro_nome": pn,
        "sobrenome": sn,
        "data_nascimento": f"{y0:04d}-{m:02d}-{d:02d}",
        "endereco": addr,
        "cep": cep,
        "telefone": tel,
        "email": email,
        "usuario_plataforma": usr,
        "kyc_status": "APROVADO_SIMULACAO",
        "kyc_referencia": kyc_ref,
    }


def main() -> None:
    import json

    if not CSV_PATH.is_file():
        raise SystemExit(f"CSV não encontrado: {CSV_PATH}")
    if not LP_JSON.is_file():
        raise SystemExit(f"LP JSON não encontrado: {LP_JSON}")

    OUT_DB.parent.mkdir(parents=True, exist_ok=True)
    if OUT_DB_TMP.is_file():
        try:
            OUT_DB_TMP.unlink()
        except OSError:
            pass

    lps_raw: list[dict] = json.loads(LP_JSON.read_text(encoding="utf-8"))
    lps_enriched = [enrich_lp(dict(x)) for x in lps_raw]

    con = sqlite3.connect(OUT_DB_TMP)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute(
        """
        CREATE TABLE remittance_categories (
            id INTEGER PRIMARY KEY,
            nome_pt TEXT NOT NULL,
            grupo INTEGER NOT NULL
        )
        """
    )
    for i, nome in enumerate(CATEGORIES_PT, 1):
        g = 1 + ((i - 1) % 4)
        cur.execute("INSERT INTO remittance_categories (id, nome_pt, grupo) VALUES (?,?,?)", (i, nome, g))

    cur.execute(
        """
        CREATE TABLE lps (
            lp_id TEXT PRIMARY KEY,
            nome_completo TEXT,
            genero TEXT,
            cidade TEXT,
            estado TEXT,
            primeiro_nome TEXT,
            sobrenome TEXT,
            data_nascimento TEXT,
            endereco TEXT,
            cep TEXT,
            telefone TEXT,
            email TEXT,
            usuario_plataforma TEXT,
            kyc_status TEXT,
            kyc_referencia TEXT,
            categoria_primaria_id INTEGER,
            capital_inicial REAL,
            saldo_carteira_brl REAL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE lp_category_slots (
            lp_id TEXT NOT NULL,
            slot INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            is_primary INTEGER NOT NULL,
            PRIMARY KEY (lp_id, slot)
        )
        """
    )

    # slots 4 categorias por LP
    ncat = len(CATEGORIES_PT)
    for lp in lps_enriched:
        rr = rng_for_lp(lp["lp_id"])
        picks = rr.sample(range(1, ncat + 1), 4)
        primary = picks[0]
        lp["categoria_primaria_id"] = primary
        for slot, cid in enumerate(picks, 1):
            cur.execute(
                "INSERT INTO lp_category_slots (lp_id, slot, category_id, is_primary) VALUES (?,?,?,?)",
                (lp["lp_id"], slot, cid, 1 if cid == primary else 0),
            )

    for lp in lps_enriched:
        cur.execute(
            """INSERT INTO lps VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                lp["lp_id"],
                lp["nome_completo"],
                lp["genero"],
                lp["cidade"],
                lp["estado"],
                lp["primeiro_nome"],
                lp["sobrenome"],
                lp["data_nascimento"],
                lp["endereco"],
                lp["cep"],
                lp["telefone"],
                lp["email"],
                lp["usuario_plataforma"],
                lp["kyc_status"],
                lp["kyc_referencia"],
                lp["categoria_primaria_id"],
                lp["capital_inicial"],
                0.0,
            ),
        )

    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        assert fields is not None
        cols_sql = ", ".join(f'"{c}" TEXT' for c in fields)
        cur.execute(f"CREATE TABLE rematches ({cols_sql})")
        placeholders = ", ".join(["?"] * len(fields))
        qcols = ",".join(f'"{c}"' for c in fields)
        ins = f"INSERT INTO rematches ({qcols}) VALUES ({placeholders})"

        batch: list[list[str]] = []
        for row in reader:
            batch.append([row[c] for c in fields])
            if len(batch) >= 2000:
                cur.executemany(ins, batch)
                batch.clear()
        if batch:
            cur.executemany(ins, batch)

    # saldo carteira = capital inicial + soma de lucros provisionados (Tiered 75% LP)
    cur.execute(
        """
        UPDATE lps SET saldo_carteira_brl = capital_inicial + (
            SELECT COALESCE(SUM(CAST(lp_profit_share_brl AS REAL)), 0)
            FROM rematches r WHERE r.LP_ID = lps.lp_id
        )
        """
    )

    # Valor final por linha (auditável) + início da cadeia: próxima operação carrega valor final anterior (mesmo LP)
    cur.execute("ALTER TABLE rematches ADD COLUMN valor_final_rolagem_brl REAL")
    cur.execute("ALTER TABLE rematches ADD COLUMN inicio_pool_com_lucro_rolado_brl REAL")

    # Uma passagem SQL: valor final; início = GTV (1ª do LP) ou valor final anterior (próxima carrega lucro)
    con.execute(
        """
        WITH t AS (
          SELECT
            rematch_id,
            ROUND(
              CAST(Principal_Capital AS REAL)
              + CAST(lp_profit_share_brl AS REAL),
              2
            ) AS vf,
            ROUND(
              COALESCE(
                LAG(
                  CAST(Principal_Capital AS REAL)
                  + CAST(lp_profit_share_brl AS REAL)
                ) OVER (
                  PARTITION BY LP_ID
                  ORDER BY CAST(Month AS INTEGER) ASC, CAST(Day AS INTEGER) ASC, rematch_id ASC
                ),
                CAST(Principal_Capital AS REAL)
              ),
              2
            ) AS ini
          FROM rematches
        )
        UPDATE rematches
        SET
          valor_final_rolagem_brl = t.vf,
          inicio_pool_com_lucro_rolado_brl = t.ini
        FROM t
        WHERE rematches.rematch_id = t.rematch_id
        """
    )

    cur.execute("CREATE INDEX idx_rm_lp ON rematches (lp_id)")
    cur.execute("CREATE INDEX idx_rm_data ON rematches (data_operacao)")
    cur.execute("CREATE INDEX idx_rm_ts ON rematches (timestamp_remessa_iso)")

    con.commit()
    con.close()

    try:
        os.replace(OUT_DB_TMP, OUT_DB)
        print("OK", OUT_DB)
    except OSError as e:
        alt = OUT_DB.parent / "fluxus_sim_ready.db"
        shutil.copy2(OUT_DB_TMP, alt)
        print("AVISO: não foi possível substituir", OUT_DB, "—", e)
        print("BD gerada em", alt, "(feche server_sim.py e copie/rename para fluxus_sim.db)")
        try:
            OUT_DB_TMP.unlink()
        except OSError:
            pass


if __name__ == "__main__":
    main()
