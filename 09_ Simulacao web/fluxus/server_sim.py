# -*- coding: utf-8 -*-
"""
Servidor local FLUXUS simulação: HTML estático + API SQLite (rematches / LPs).

Uso (na pasta fluxus):
  pip install flask
  python server_sim.py

Abrir: http://127.0.0.1:8787/transaction.html
Regenerar BD rematches: python ../../05_SCRIPTS/SCRIPT_BUILD_FLUXUS_SIM_DB.py
Regenerar BD stress (Power BI): python ../../05_SCRIPTS/SCRIPT_BUILD_STRESS_AUDIT_DB.py
Stress UI: http://127.0.0.1:8787/stress-audit.html
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

BASE = Path(__file__).resolve().parent


def _db_has_rematches(path: Path) -> bool:
    try:
        c = sqlite3.connect(path)
        ok = c.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='rematches' LIMIT 1"
        ).fetchone()
        c.close()
        return ok is not None
    except OSError:
        return False


def pick_db_path() -> Path:
    """Prefere ficheiro que contém tabela rematches; entre válidos, o mais recente."""
    a = BASE / "data" / "fluxus_sim.db"
    b = BASE / "data" / "fluxus_sim_ready.db"
    candidates = [p for p in (b, a) if p.is_file() and _db_has_rematches(p)]
    if not candidates:
        return a if a.is_file() else b
    if len(candidates) == 1:
        return candidates[0]
    try:
        if candidates[0].stat().st_mtime >= candidates[1].stat().st_mtime:
            return candidates[0]
    except OSError:
        return candidates[0]
    return candidates[1]


DB_PATH = pick_db_path()

app = Flask(__name__)


def stress_db_path() -> Path:
    return BASE / "data" / "fluxus_stress.db"


def stress_conn() -> sqlite3.Connection | None:
    p = stress_db_path()
    if not p.is_file():
        return None
    c = sqlite3.connect(p, check_same_thread=False)
    c.row_factory = sqlite3.Row
    return c


def conn() -> sqlite3.Connection:
    global DB_PATH
    DB_PATH = pick_db_path()
    if not DB_PATH.is_file():
        raise FileNotFoundError(str(DB_PATH))
    c = sqlite3.connect(DB_PATH, check_same_thread=False)
    c.row_factory = sqlite3.Row
    return c


def _f(row: sqlite3.Row, k: str) -> float:
    try:
        return float(row[k])
    except Exception:
        return 0.0


def enrich_rematch(d: dict) -> dict:
    """Campos de trilho para UI + modal Status (Simulação 360º de Setup Operacional)."""
    r = dict(d)
    gtv = _f(r, "gtv_brl")
    
    iof_pct = 0.0038
    # Lógica de Partilha Institucional (75% LP) baseada no Modelo de Dominância/Tiered
    # O spread é calculado dinamicamente conforme a faixa de volume (1.08% a 0.50%)
    def get_tier_spread(v_usd):
        if v_usd <= 100: return 0.0108
        if v_usd <= 1000: return 0.0108 + ((v_usd-100)/900) * (0.0073-0.0108)
        if v_usd <= 5000: return 0.0073 + ((v_usd-1000)/4000) * (0.0060-0.0073)
        if v_usd <= 20000: return 0.0060 + ((v_usd-5000)/15000) * (0.0055-0.0060)
        return 0.0050

    spread_pct = get_tier_spread(gtv / 5.0) 
    
    # Cálculo de Giro Mensal (Alienação) para Governança Fiscal (R$ 35k Limite)
    op_date = r.get("data_operacao", "")
    month_prefix = op_date[:7] if len(op_date) >= 7 else "Unknown"
    lp_id = r.get("lp_id")
    
    c = sqlite3.connect(DB_PATH)
    giro_mensal = c.execute(
        "SELECT SUM(CAST(gtv_brl AS REAL)) FROM rematches WHERE lp_id = ? AND data_operacao LIKE ?",
        (lp_id, f"{month_prefix}%")
    ).fetchone()[0] or 0.0
    c.close()

    lp_profit_raw = gtv * (spread_pct * 0.75) 
    
    # Aplicação de IR Provisório se Giro Mensal (Alienação) > 35k
    TAX_LIMIT = 35000.0
    ir_provision = 0.0
    if giro_mensal > TAX_LIMIT:
        ir_provision = lp_profit_raw * 0.15
    
    lp_net_profit = lp_profit_raw - ir_provision
    
    r["giro_mensal_brl"] = round(giro_mensal, 2)
    r["is_taxable"] = (giro_mensal > TAX_LIMIT)
    r["ir_provision_brl"] = round(ir_provision, 2)
    r["lp_profit_gross_brl"] = round(lp_profit_raw, 2)
    
    r["capital_agregado_remessa_brl"] = round(gtv, 2)
    r["taxa_servico_fluxus_brl"] = round(gtv * spread_pct, 2)
    r["iof_governo_brl"] = round(gtv * iof_pct, 2)
    r["custo_total_sender_brl"] = round(gtv * (spread_pct + iof_pct), 2)
    r["dock_maintenance_shared_brl"] = 0.00 
    
    r["lp_spread_retorno_brl"] = round(lp_net_profit, 2)
    r["total_taxas_trilho_brl"] = round(r["taxa_servico_fluxus_brl"] + r["iof_governo_brl"], 2)
    r["valor_final_rolagem_brl"] = round(gtv + lp_net_profit, 2)
    
    r["status_trilho"] = "INSTITUTIONAL_LIQUIDITY"
    r["status_explicacao_pt"] = "Operação auditada sob protocolo de dominância tiered."
    return r


@app.after_request
def cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


@app.get("/api/health")
def health():
    return jsonify({"ok": True, "db": DB_PATH.is_file()})


@app.get("/api/rematches")
def api_rematches():
    page = max(int(request.args.get("page", 1)), 1)
    limit = min(max(int(request.args.get("limit", 40)), 1), 500)
    lp_id = request.args.get("lp_id")
    offset = (page - 1) * limit
    c = conn()
    where, args = "", []
    if lp_id:
        where, args = " WHERE lp_id = ?", [lp_id]
    total = c.execute(f"SELECT COUNT(*) FROM rematches{where}", args).fetchone()[0]
    q = f"SELECT * FROM rematches{where} ORDER BY timestamp_remessa_iso DESC LIMIT ? OFFSET ?"
    cur = c.execute(q, args + [limit, offset])
    rows = [enrich_rematch(dict(x)) for x in cur.fetchall()]
    c.close()
    return jsonify({"total": int(total), "page": page, "limit": limit, "rows": rows})


@app.get("/api/rematch/<rid>")
def api_rematch_one(rid: str):
    c = conn()
    cur = c.execute("SELECT * FROM rematches WHERE rematch_id = ?", (rid,))
    row = cur.fetchone()
    c.close()
    if not row:
        return jsonify({"error": "not_found"}), 404
    return jsonify(enrich_rematch(dict(row)))


@app.get("/api/lps")
def api_lps():
    c = conn()
    cur = c.execute(
        """
        SELECT l.*, c.nome_pt AS categoria_primaria_nome
        FROM lps l
        LEFT JOIN remittance_categories c ON c.id = l.categoria_primaria_id
        ORDER BY l.lp_id
        """
    )
    rows = [dict(x) for x in cur.fetchall()]
    c.close()
    return jsonify({"total": len(rows), "rows": rows})


@app.get("/api/lp/<lp_id>/categories") # Alias singular
@app.get("/api/lps/<lp_id>/categories")
def api_lp_cats(lp_id: str):
    c = conn()
    cur = c.execute(
        """
        SELECT s.slot, s.is_primary, c.nome_pt, c.grupo
        FROM lp_category_slots s
        JOIN remittance_categories c ON c.id = s.category_id
        WHERE s.lp_id = ?
        ORDER BY s.slot
        """,
        (lp_id,),
    )
    rows = [dict(x) for x in cur.fetchall()]
    c.close()
    return jsonify({"lp_id": lp_id, "slots": rows})


@app.get("/api/summary")
def api_summary():
    c = conn()
    gtv = c.execute("SELECT SUM(CAST(gtv_brl AS REAL)) FROM rematches").fetchone()[0]
    n = c.execute("SELECT COUNT(*) FROM rematches").fetchone()[0]
    ptax = c.execute(
        "SELECT AVG(CAST(usd_brl_ptax_mid AS REAL)) FROM rematches WHERE usd_brl_ptax_mid IS NOT NULL"
    ).fetchone()[0]
    n_lp = c.execute("SELECT COUNT(DISTINCT lp_id) FROM rematches").fetchone()[0]
    c.close()
    return jsonify(
        {
            "rematches": int(n),
            "lp_distinct": int(n_lp or 0),
            "gtv_brl": float(gtv or 0),
            "ptax_usd_brl_mid_media": round(float(ptax or 0), 4),
            "moeda_referencia": "BRL",
            "corredores_demo": ["USD", "EUR", "GBP", "BRL"],
            "nota_fx": "EUR/GBP são corredores de produto; cotação auditada no CSV é USD/BRL (PTAX BCB por data).",
        }
    )


@app.get("/api/dre")
def api_dre():
    """Demonstrativo de Resultados (DRE) baseado na simulação atual (Sincronia CET 2.47%)."""
    c = conn()
    
    # 1. GTV Total (Volume Processado)
    total_gtv = c.execute("SELECT SUM(CAST(gtv_brl AS REAL)) FROM rematches").fetchone()[0] or 0.0
    
    # 2. Receita Bruta (Fee de Orquestração - Sincronizado Opção A: 2.11%)
    # Tese: Capital destravado da Pool (1.1% redistribuído aqui).
    rev_raw = total_gtv * 0.0211
    
    # 3. Impostos Diretos (Lucro Presumido Est. 14.33% sobre a Receita Fluxus)
    taxes_direct = rev_raw * 0.1433
    
    # 4. OPEX (Folha 8 Pessoas - Projeção 12 meses)
    # 8 people * R$ 10k net * 1.8 (encargos) = R$ 144k/month = R$ 1.72M/year
    opex_payroll = 144000.0 * 12.0 
    
    # 5. Outros Custos Infra (Escritório/SaaS/Cloud)
    opex_infra = 50000.0 
    
    ebitda = rev_raw - taxes_direct - opex_payroll - opex_infra
    
    # 6. Impostos Corporativos (IRPJ/CSLL Est. 4.8% sobre Bruta no Presumido)
    taxes_corp = rev_raw * 0.048
    
    net_income = ebitda - taxes_corp
    
    c.close()
    
    return jsonify({
        "revenue_gross": round(rev_raw, 2),
        "taxes_direct": round(taxes_direct, 2),
        "opex_payroll": round(opex_payroll, 2),
        "opex_infra": round(opex_infra, 2),
        "ebitda": round(ebitda, 2),
        "taxes_corporate": round(taxes_corp, 2),
        "net_income": round(net_income, 2),
        "payroll_headcount": 8,
        "tax_regime": "Lucro Presumido (Brasil)",
        "period_months": 12,
        "fee_orchestration_avg": "1.01%",
        "status": "synchronized_v3_retail"
    })


@app.get("/api/fx/ptax_stats")
def api_fx_ptax_stats():
    """Estatísticas de oscilação PTAX USD/BRL no período dos rematches."""
    c = conn()
    row = c.execute(
        """
        SELECT
            COUNT(*) AS n,
            MIN(CAST(usd_brl_ptax_mid AS REAL)) AS ptax_min,
            MAX(CAST(usd_brl_ptax_mid AS REAL)) AS ptax_max,
            AVG(CAST(usd_brl_ptax_mid AS REAL)) AS ptax_avg
        FROM rematches
        WHERE usd_brl_ptax_mid IS NOT NULL
        """
    ).fetchone()
    std = c.execute(
        """
        WITH t AS (
            SELECT CAST(usd_brl_ptax_mid AS REAL) AS m
            FROM rematches
            WHERE usd_brl_ptax_mid IS NOT NULL
        ),
        s AS (SELECT AVG(m) AS av FROM t)
        SELECT SQRT(AVG((t.m - s.av) * (t.m - s.av)))
        FROM t, s
        """
    ).fetchone()[0]
    c.close()
    d = dict(row)
    n = int(d["n"] or 0)
    lo = float(d["ptax_min"] or 0)
    hi = float(d["ptax_max"] or 0)
    av = float(d["ptax_avg"] or 0)
    sigma = float(std or 0) if std is not None else 0.0
    amplitude = (hi - lo) if av == 0 else (hi - lo) / av
    return jsonify(
        {
            "n_observacoes": n,
            "ptax_min": round(lo, 4),
            "ptax_max": round(hi, 4),
            "ptax_avg": round(av, 4),
            "ptax_sigma": round(sigma, 5),
            "amplitude_pct": round(amplitude * 100, 3),
            "nota": "PTAX BCB por linha de rematch; dispersão mede oscilação do câmbio no período simulado.",
        }
    )


@app.get("/api/fx/ptax_daily")
def api_fx_ptax_daily():
    """Série diária PTAX (média por data_operacao) para gráficos do dashboard."""
    c = conn()
    cur = c.execute(
        """
        SELECT data_operacao AS d,
               AVG(CAST(usd_brl_ptax_mid AS REAL)) AS mid
        FROM rematches
        WHERE usd_brl_ptax_mid IS NOT NULL
          AND data_operacao IS NOT NULL
          AND TRIM(data_operacao) != ''
        GROUP BY data_operacao
        ORDER BY d
        """
    )
    rows = [{"d": x["d"], "mid": float(x["mid"] or 0)} for x in cur.fetchall()]
    c.close()
    return jsonify({"total": len(rows), "rows": rows})


@app.get("/api/index/lp_match_pairs")
def api_index_lp_match_pairs():
    """
    Pares consecutivos por LP: compra = GTV do rematch k, recompra = GTV do rematch k+1
    (proxy operacional de sequência na simulação; ver 04_PROCESS matching/rolagem).
    """
    limit = min(max(int(request.args.get("limit", 40)), 10), 300)
    c = conn()
    cur = c.execute(
        """
        WITH ordered AS (
            SELECT
                lp_id,
                rematch_id,
                timestamp_remessa_iso,
                data_operacao,
                CAST(gtv_brl AS REAL) AS gtv,
                LEAD(CAST(gtv_brl AS REAL)) OVER (
                    PARTITION BY lp_id ORDER BY timestamp_remessa_iso, rematch_id
                ) AS gtv_next,
                LEAD(rematch_id) OVER (
                    PARTITION BY lp_id ORDER BY timestamp_remessa_iso, rematch_id
                ) AS rid_next,
                LEAD(timestamp_remessa_iso) OVER (
                    PARTITION BY lp_id ORDER BY timestamp_remessa_iso, rematch_id
                ) AS ts_next
            FROM rematches
        )
        SELECT lp_id, rematch_id, timestamp_remessa_iso, data_operacao, gtv AS compra_brl,
               rid_next AS rematch_recompra, ts_next AS ts_recompra, gtv_next AS recompra_brl
        FROM ordered
        WHERE gtv_next IS NOT NULL
        ORDER BY timestamp_remessa_iso DESC, rematch_id DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = [dict(x) for x in cur.fetchall()]
    c.close()
    return jsonify({"total": len(rows), "rows": rows})


@app.get("/api/rematches/by_lp")
def api_rematches_by_lp():
    """Agregação por LP para segunda visão na UI (transaction.html)."""
    c = conn()
    cur = c.execute(
        """
        SELECT
            lp_id,
            MAX(lp_nome) AS lp_nome,
            COUNT(*) AS n_rem,
            SUM(CAST(gtv_brl AS REAL)) AS sum_gtv_brl,
            SUM(CAST(spread_total_brl_3_5pct AS REAL) + CAST(iof_governo_brl AS REAL)) AS sum_taxas_trilho_brl,
            SUM(CAST(lp_spread_brl_42_8pct AS REAL)) AS sum_lp_retorno_brl,
            SUM(CAST(spread_total_brl_3_5pct AS REAL)) AS total_protocol_spread
        FROM rematches
        GROUP BY lp_id
        ORDER BY sum_gtv_brl DESC
        """
    )
    rows = [dict(x) for x in cur.fetchall()]
    c.close()
    return jsonify({"total": len(rows), "rows": rows})


def _get_stress_where(req):
    where_parts = []
    args = []
    
    # Verificação defensiva de colunas existentes
    c = stress_conn()
    if c:
        cols = [r[1] for r in c.execute("PRAGMA table_info(stress_audit)").fetchall()]
        c.close()
    else:
        cols = []

    # Use 'lp' to match the JS state
    if lp_val := req.args.get("lp"):
        if "lp_id" in cols:
            where_parts.append("lp_id = ?")
            args.append(lp_val)
    if month := req.args.get("month"):
        if "month" in cols:
            if str(month).strip() != "":
                where_parts.append("month = ?")
                args.append(int(month))
    if region := req.args.get("region"):
        if "sender_country" in cols:
            where_parts.append("sender_country = ?")
            args.append(region)
    if sector := req.args.get("sector"):
        if "recipient_sector" in cols:
            where_parts.append("recipient_sector = ?")
            args.append(sector)
    
    wh = (" WHERE " + " AND ".join(where_parts)) if where_parts else ""
    return wh, args


@app.get("/api/stress/summary")
def api_stress_summary():
    c = stress_conn()
    if c is None:
        return jsonify({"error": "stress_db_missing", "hint": "python ../../05_SCRIPTS/SCRIPT_BUILD_STRESS_AUDIT_DB.py"}), 503
    
    wh, args = _get_stress_where(request)
    q = f"""
        SELECT
            COUNT(*) AS n_rows,
            SUM(transaction_value) AS sum_gtv,
            SUM(total_spread) AS sum_spread,
            SUM(lp_profit) AS sum_lp_profit,
            SUM(fluxus_fee) AS sum_fluxus_fee,
            SUM(vasp_fee) AS sum_vasp_fee,
            SUM(pool_reserve_gtv) AS sum_pool,
            SUM(dock_reload_cost) AS sum_dock,
            SUM(blockchain_gas) AS sum_gas,
            SUM(net_fluxus_margin) AS sum_net_fluxus_margin
        FROM stress_audit
        {wh}
    """
    row = c.execute(q, args).fetchone()
    c.close()
    d = dict(row)
    d["n_rows"] = int(d["n_rows"] or 0)
    for k in d:
        if d[k] is None: d[k] = 0.0
    return jsonify(d)


@app.get("/api/stress/filters")
def api_stress_filters():
    """Retorna os valores únicos para os filtros da UI Farseer com proteção contra colunas ausentes."""
    try:
        c = stress_conn()
        if c is None: return jsonify({"error": "missing_db"}), 503
        
        cols = [r[1] for r in c.execute("PRAGMA table_info(stress_audit)").fetchall()]
        
        regions = []
        if "sender_country" in cols:
            regions = [x[0] for x in c.execute("SELECT DISTINCT sender_country FROM stress_audit WHERE sender_country IS NOT NULL ORDER BY 1").fetchall()]
        
        sectors = []
        if "recipient_sector" in cols:
            sectors = [x[0] for x in c.execute("SELECT DISTINCT recipient_sector FROM stress_audit WHERE recipient_sector IS NOT NULL ORDER BY 1").fetchall()]
        
        lps = []
        if "lp_id" in cols:
            lps = [x[0] for x in c.execute("SELECT DISTINCT lp_id FROM stress_audit WHERE lp_id IS NOT NULL ORDER BY 1").fetchall()]
        
        c.close()
        return jsonify({
            "regions": regions,
            "sectors": sectors,
            "lps": lps
        })
    except Exception:
        return jsonify({"regions": [], "sectors": [], "lps": []})


@app.get("/api/institutional/dre")
def api_institutional_dre():
    """DRE Institucional customizado com suporte a filtros e breakdown analítico."""
    try:
        c = stress_conn()
        if c is None: return jsonify({"error": "missing_db"}), 503
        
        wh, args = _get_stress_where(request)
        
        # 1. Agregação Base
        q = f"SELECT SUM(transaction_value), SUM(total_spread), SUM(lp_profit), SUM(vasp_fee), SUM(dock_reload_cost), SUM(blockchain_gas), SUM(fluxus_fee) FROM stress_audit {wh}"
        res = c.execute(q, args).fetchone()
        
        gtv = float(res[0] or 0.0)
        total_revenue = float(res[1] or 0.0)
        lp_payout = float(res[2] or 0.0)
        network_payout = float(res[3] or 0.0)
        dock_cost = float(res[4] or 0.0)
        gas_cost = float(res[5] or 0.0)
        fluxus_net_take = float(res[6] or 0.0)
    
        # 2. Custos Operacionais Adicionais (Simulados sobre a amostra filtrada)
        # Proporção: Se 84k linhas = 100% opex, aplicamos o percentual da amostra atual
        total_rows = c.execute("SELECT COUNT(*) FROM stress_audit").fetchone()[0]
        sample_rows = c.execute(f"SELECT COUNT(*) FROM stress_audit {wh}", args).fetchone()[0]
        proportion = sample_rows / total_rows if total_rows > 0 else 0
        
        # Fixos (ajustados pela proporção da simulação)
        payroll = (144000.0 * 12.0) * proportion
        infra = 50000.0 * proportion
        compliance = (gtv * 0.0005) # 5 bps para AML/KYC outsourced
        
        # Cálculos Farseer
        gross_pnl = total_revenue - lp_payout - network_payout
        opex_total = dock_cost + gas_cost + payroll + infra + compliance
        ebitda = gross_pnl - opex_total
        
        taxes_corp = total_revenue * 0.1433 # Estimativa Lucro Presumido
        net_income = ebitda - taxes_corp
        
        c.close()
        
        return jsonify({
            "gtv": gtv,
            "revenue": {
                "total": total_revenue,
                "orchestration_fee": total_revenue, 
            },
            "cogs": {
                "total": lp_payout + network_payout,
                "lp_share": lp_payout,
                "network_vasp": network_payout
            },
            "gross_margin": gross_pnl,
            "opex": {
                "total": opex_total,
                "blockchain_gas": gas_cost,
                "liquidity_dock": dock_cost,
                "payroll_est": payroll,
                "infra_est": infra,
                "compliance_aml": compliance
            },
            "ebitda": ebitda,
            "taxes": taxes_corp,
            "net_income": net_income,
            "metrics": {
                "margin_pct": (gross_pnl / total_revenue * 100) if total_revenue > 0 else 0,
                "take_rate_bps": (total_revenue / gtv * 10000) if gtv > 0 else 0
            }
        })
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": "server_error", "message": str(e)}), 500


@app.get("/api/stress/by_month")
def api_stress_by_month():
    c = stress_conn()
    if c is None:
        return jsonify({"error": "stress_db_missing"}), 503
    cur = c.execute(
        """
        SELECT
            month,
            COUNT(*) AS n_rows,
            SUM(transaction_value) AS sum_gtv,
            SUM(total_spread) AS sum_spread,
            SUM(lp_profit) AS sum_lp_profit,
            SUM(fluxus_fee) AS sum_fluxus_fee,
            SUM(vasp_fee) AS sum_vasp_fee,
            SUM(pool_reserve_gtv) AS sum_pool,
            SUM(net_fluxus_margin) AS sum_net_fluxus_margin
        FROM stress_audit
        GROUP BY month
        ORDER BY month
        """
    )
    rows = [dict(x) for x in cur.fetchall()]
    c.close()
    return jsonify({"total": len(rows), "rows": rows})


@app.get("/api/stress/by_lp")
def api_stress_by_lp():
    c = stress_conn()
    if c is None:
        return jsonify({"error": "stress_db_missing"}), 503
    cur = c.execute(
        """
        SELECT
            lp_id,
            COUNT(*) AS n_rows,
            SUM(transaction_value) AS sum_gtv,
            SUM(total_spread) AS sum_spread,
            SUM(lp_profit) AS sum_lp_profit,
            SUM(fluxus_fee) AS sum_fluxus_fee,
            SUM(vasp_fee) AS sum_vasp_fee,
            SUM(pool_reserve_gtv) AS sum_pool,
            SUM(net_fluxus_margin) AS sum_net_fluxus_margin
        FROM stress_audit
        GROUP BY lp_id
        ORDER BY sum_gtv DESC
        """
    )
    rows = [dict(x) for x in cur.fetchall()]
    c.close()
    return jsonify({"total": len(rows), "rows": rows})


@app.get("/api/lp/performance/<lp_id>") # Alias singular
@app.get("/api/lps/performance/<lp_id>")
def api_lp_performance(lp_id: str):
    """Calcula KPIs temporais (Dia/Semana/Trimestre/Ano) para um LP específico."""
    c = stress_conn()
    if c is None:
        return jsonify({"error": "stress_db_missing"}), 503
    
    # 1. Anual (Total)
    yearly = c.execute(
        "SELECT SUM(transaction_value) as gtv, SUM(lp_profit) as profit FROM stress_audit WHERE lp_id = ?",
        (lp_id,)
    ).fetchone()
    
    # 2. Trimestral (Q4 - Último Quarter)
    quarterly = c.execute(
        "SELECT SUM(transaction_value) as gtv, SUM(lp_profit) as profit FROM stress_audit WHERE lp_id = ? AND month BETWEEN 10 AND 12",
        (lp_id,)
    ).fetchone()
    
    # 3. Semanal (Projetado como os últimos 7 dias da simulação)
    weekly = c.execute(
        "SELECT SUM(transaction_value) as gtv, SUM(lp_profit) as profit FROM stress_audit WHERE lp_id = ? AND month = 12 AND day >= 24",
        (lp_id,)
    ).fetchone()
    
    # 4. Diário (Último dia disponível)
    daily = c.execute(
        "SELECT SUM(transaction_value) as gtv, SUM(lp_profit) as profit FROM stress_audit WHERE lp_id = ? AND month = 12 AND day = 31",
        (lp_id,)
    ).fetchone()

    # 5. Timeline (Para o gráfico de crescimento)
    timeline = c.execute(
        "SELECT month, SUM(lp_profit) as m_profit FROM stress_audit WHERE lp_id = ? GROUP BY month ORDER BY month",
        (lp_id,)
    ).fetchall()

    # 6. Capital Atual (Fila para Qualificar)
    current_cap = c.execute(
        "SELECT principal_capital FROM stress_audit WHERE lp_id = ? ORDER BY month DESC, day DESC, cycle_num DESC LIMIT 1",
        (lp_id,)
    ).fetchone()
    current_capital = float(current_cap[0] or 0) if current_cap else 0.0

    # 7. Giro Mensal (Projetado/Atual do mês 12 da simulação)
    giro_m_row = c.execute(
        "SELECT SUM(transaction_value) FROM stress_audit WHERE lp_id = ? AND month = 12",
        (lp_id,)
    ).fetchone()
    giro_m = float(giro_m_row[0] or 0.0)

    c.close()

    def _v(row):
        return {"gtv": float(row["gtv"] or 0), "profit": float(row["profit"] or 0)} if row else {"gtv": 0, "profit": 0}

    TAX_LIMIT = 35000.0
    return jsonify({
        "lp_id": lp_id,
        "daily": _v(daily),
        "weekly": _v(weekly),
        "quarterly": _v(quarterly),
        "yearly": _v(yearly),
        "current_capital": current_capital,
        "monthly_giro": float(giro_m),
        "tax_limit": TAX_LIMIT,
        "is_taxable": giro_m > TAX_LIMIT,
        "timeline": [{"month": x["month"], "profit": float(x["m_profit"] or 0)} for x in timeline]
    })


@app.get("/api/lps/performance_range/<lp_id>")
def api_lp_performance_range(lp_id: str):
    """Calcula performance para um range customizado de Month/Day."""
    sm = int(request.args.get("start_m", 1))
    sd = int(request.args.get("start_d", 1))
    em = int(request.args.get("end_m", 12))
    ed = int(request.args.get("end_d", 31))
    
    c = stress_conn()
    if c is None: return jsonify({"error": "stress_db_missing"}), 503

    # Simplificação: assume ordem cronológica dentro do ano (sem wrap)
    q = """
        SELECT SUM(transaction_value) as gtv, SUM(lp_profit) as profit, COUNT(*) as cycles
        FROM stress_audit 
        WHERE lp_id = ? 
          AND ((month > ?) OR (month = ? AND day >= ?))
          AND ((month < ?) OR (month = ? AND day <= ?))
    """
    row = c.execute(q, (lp_id, sm, sm, sd, em, em, ed)).fetchone()
    
    # Cálculo de dias no range (aproximado 30 dias/mês para simulação)
    days = (em - sm) * 30 + (ed - sd) + 1
    days = max(days, 1)
    
    profit = float(row["profit"] or 0)
    projected_annual = (profit / days) * 365
    
    c.close()
    return jsonify({
        "lp_id": lp_id,
        "range_days": days,
        "gtv": float(row["gtv"] or 0),
        "profit": profit,
        "cycles": int(row["cycles"] or 0),
        "projected_annual_profit": round(projected_annual, 2)
    })


@app.get("/api/lps/activity/<lp_id>")
def api_lp_activity(lp_id: str):
    """Retorna o extrato (ledger) de liquidação e recebimento."""
    limit = min(int(request.args.get("limit", 20)), 100)
    c = stress_conn()
    if c is None: return jsonify({"error": "stress_db_missing"}), 503
    
    # Busca os últimos ciclos com posição na fila
    cur = c.execute(
        "SELECT month, day, principal_capital, lp_profit, queue_position FROM stress_audit WHERE lp_id = ? ORDER BY month DESC, day DESC, cycle_num DESC LIMIT ?",
        (lp_id, limit)
    )
    
    activity = []
    for r in cur.fetchall():
        m, d = r["month"], r["day"]
        cap = float(r["principal_capital"] or 0)
        yield_val = float(r["lp_profit"] or 0)
        q_pos = int(r["queue_position"] or 0)
        
        # Simulação simples de IR no extrato se lucro for alto (provisório)
        # Na vida real, o server-side já calculou isso no enrich_rematch
        ir_prov = 0.0
        if cap > 20000: # Heurística simples para o Extrato: capital alto costuma gerar giro alto
            ir_prov = yield_val * 0.15

        # 1. Entrada de Liquidação (Saída da conta)
        activity.append({
            "date": f"{m:02d}/{d:02d}",
            "type": "DEBIT",
            "label": "Liquidação: Orquestração de Remessa",
            "amount": -cap,
            "status": "SETTLED",
            "queue_pos": q_pos
        })
        
        if ir_prov > 0:
             activity.append({
                "date": f"{m:02d}/{d:02d}",
                "type": "DEBIT",
                "label": "Provisão IR GCAP (15%)",
                "amount": -ir_prov,
                "status": "PROVISIONED"
            })

        # 2. Recebimento (Volta para conta com lucro)
        activity.append({
            "date": f"{m:02d}/{d:02d}",
            "type": "CREDIT",
            "label": "Recebimento: Re-liquidação + Yield",
            "amount": cap + yield_val,
            "status": "SETTLED"
        })
        
    c.close()
    return jsonify({"lp_id": lp_id, "activity": activity})


@app.get("/api/stress/rows")
def api_stress_rows():
    c = stress_conn()
    if c is None:
        return jsonify({"error": "stress_db_missing"}), 503
    page = max(int(request.args.get("page", 1)), 1)
    limit = min(max(int(request.args.get("limit", 40)), 1), 500)
    
    wh, args = _get_stress_where(request)
    
    total = c.execute(f"SELECT COUNT(*) FROM stress_audit{wh}", args).fetchone()[0]
    offset = (page - 1) * limit
    q = f"SELECT * FROM stress_audit{wh} ORDER BY month, day, lp_id, cycle_num LIMIT ? OFFSET ?"
    try:
        cur = c.execute(q, args + [limit, offset])
        rows = [dict(x) for x in cur.fetchall()]
    except sqlite3.OperationalError:
        rows = []
    c.close()
    return jsonify({"total": int(total), "page": page, "limit": limit, "rows": rows})


def _safe_path(rel: str) -> Path | None:
    # Whitelist para as rotas de API não caírem no forbidden do static handler
    if rel.startswith("api/"):
        return None
    # Proteção de arquivos sensíveis
    if rel.startswith("data/") or rel.endswith(".py") or rel.endswith(".db"):
        return None
    
    target = (BASE / rel).resolve()
    base = BASE.resolve()
    
    if target == base:
        return base / "index.html"
    
    try:
        target.relative_to(base)
    except ValueError:
        return None
        
    return target if target.is_file() else None


@app.get("/")
def root():
    return send_from_directory(BASE, "index.html")


@app.get("/<path:rel>")
def static_or_404(rel: str):
    # Se começar com api/, mas chegou aqui, é porque não bateu em nenhuma rota definida
    if rel.startswith("api/"):
         return jsonify({"error": "api_route_not_found"}), 404

    target = (BASE / rel).resolve()
    base = BASE.resolve()
    
    # Check if inside BASE
    try:
        target.relative_to(base)
    except ValueError:
        return jsonify({"error": "forbidden"}), 403

    # Check forbidden extensions/folders
    if rel.startswith("data/") or rel.endswith(".py") or rel.endswith(".db"):
        return jsonify({"error": "forbidden"}), 403

    if not target.exists():
        return jsonify({"error": "not_found"}), 404
        
    if not target.is_file():
        return jsonify({"error": "not_a_file"}), 404

    return send_from_directory(BASE, rel)


if __name__ == "__main__":
    print("FLUXUS sim — http://127.0.0.1:8787/transaction.html")
    print("Stress Power BI — http://127.0.0.1:8787/stress-audit.html")
    app.run(host="127.0.0.1", port=8787, debug=True)
