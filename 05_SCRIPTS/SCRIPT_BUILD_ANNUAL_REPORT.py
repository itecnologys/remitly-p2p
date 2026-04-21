# -*- coding: utf-8 -*-
"""
FLUXUS Annual Report 2026 - PDF Generator
Style C: Modern Annual Report (White background, colored sidebars)
"""

import json
import math
import os
import re
import sys
import tempfile
from pathlib import Path

# ── Paths (raiz = remitly-p2p; dados em 06_DATA) ───────────────────────────────
_REPO = Path(__file__).resolve().parents[1]
_DATA = _REPO / "06_DATA"
BOOK_DIR = str(_DATA)
OUTPUT_PDF = str(_DATA / "DATA_FLUXUS_ANNUAL_REPORT_2026.pdf")
COVER_IMG = str(_DATA / "DATA_FLUXUS_COVER.png")
CONTENT_JSON = str(_DATA / "DATA_CONTENT_RAW.json")

# ── Palette ────────────────────────────────────────────────────────────────────
PRIMARY_BLUE  = "#2563EB"
CYAN          = "#06B6D4"
EMERALD       = "#10B981"
AMBER         = "#F59E0B"
ROSE          = "#F43F5E"
INDIGO        = "#6366F1"
DARK_TEXT     = "#1E293B"
BODY_TEXT     = "#475569"
LIGHT_BG      = "#F0F4FF"
TABLE_ALT     = "#F8FAFF"
DEEP_BLUE_1   = "#0D1B2A"
DEEP_BLUE_2   = "#1565C0"

CHAPTER_COLORS = [
    "#2563EB",  # Cap 1 - blue
    "#F43F5E",  # Cap 2 - rose
    "#10B981",  # Cap 3 - emerald
    "#6366F1",  # Cap 4 - indigo
    "#F59E0B",  # Cap 5 - amber
    "#06B6D4",  # Cap 6 - cyan
    "#EF4444",  # Cap 7 - red-orange
]

CHAPTER_NAMES = [
    "A Crise Global da Remessa e o Peso do Legado",
    "Anatomia dos Gigantes e a Falácia da Eficiência",
    "A Tese FLUXUS — O Fim das Licenças Bancárias Pesadas",
    "A Engenharia da Transparência — Auditoria em Tempo Real",
    "Contabilidade Estrutural e Engenharia Financeira",
    "Regulação Global e Compliance — Software-as-Law",
    "Escala, Verticais e o Caminho do Unicórnio",
]

# ── Imports ────────────────────────────────────────────────────────────────────
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.patches import FancyBboxPatch

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus.flowables import Flowable

W, H = A4  # 595.27 x 841.89 pts

SIDEBAR_W = 6 * mm
HEADER_H  = 18 * mm
FOOTER_H  = 12 * mm
MARGIN_L  = SIDEBAR_W + 10 * mm
MARGIN_R  = 12 * mm
MARGIN_T  = HEADER_H + 4 * mm
MARGIN_B  = FOOTER_H + 4 * mm


# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY
# ═══════════════════════════════════════════════════════════════════════════════

def hex2rgb_f(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16)/255.0 for i in (0, 2, 4))

def fix_text(t):
    """Fix common encoding replacements and bold markup."""
    replacements = {
        "&#xFFFD;": "", "\ufffd": "",
        "Cap\ufffdtulo": "Capítulo",
        "P\ufffdgina": "Página",
    }
    for k, v in replacements.items():
        t = t.replace(k, v)
    # bold markup **text** → <b>text</b>
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    # Escape & < > for XML (but not already-tagged)
    # Only escape bare & not already &...;
    t = re.sub(r'&(?!#?[a-zA-Z0-9]+;)', '&amp;', t)
    return t


# ═══════════════════════════════════════════════════════════════════════════════
# CHART GENERATION
# ═══════════════════════════════════════════════════════════════════════════════

def setup_chart_style():
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "grid.linestyle": "--",
        "figure.facecolor": "white",
        "axes.facecolor": "#FAFBFF",
    })

def save_chart(fig, name):
    path = os.path.join(BOOK_DIR, f"_chart_{name}.png")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path

def make_chart1():
    """Horizontal bar: Custo Médio de Remessa por Corredor (%)"""
    setup_chart_style()
    corridors = [
        "África do Sul → Moçambique",
        "Dubai → Paquistão",
        "Filipinas → Arábia",
        "Brasil → Portugal",
        "México → EUA",
        "Global Average",
        "FLUXUS Target",
    ]
    values = [14.0, 12.0, 9.1, 7.2, 5.8, 6.2, 1.2]
    bar_colors = [
        "#F43F5E","#F43F5E","#F59E0B","#F59E0B","#F59E0B","#6366F1","#10B981"
    ]
    fig, ax = plt.subplots(figsize=(7, 3.5))
    bars = ax.barh(corridors, values, color=bar_colors, height=0.55, edgecolor="white", linewidth=0.5)
    ax.set_xlabel("Custo (%)", fontsize=9, color="#475569")
    ax.set_title("Custo Médio de Remessa por Corredor (%)", fontsize=11, fontweight="bold", color="#1E293B", pad=10)
    ax.axvline(x=6.2, color="#6366F1", linestyle="--", linewidth=1, alpha=0.7)
    for bar, val in zip(bars, values):
        ax.text(val + 0.2, bar.get_y() + bar.get_height()/2, f"{val}%",
                va="center", fontsize=8.5, color="#1E293B", fontweight="bold")
    ax.set_xlim(0, 17)
    patches = [
        mpatches.Patch(color="#F43F5E", label="Alto custo"),
        mpatches.Patch(color="#F59E0B", label="Custo médio"),
        mpatches.Patch(color="#10B981", label="FLUXUS Target"),
    ]
    ax.legend(handles=patches, loc="lower right", fontsize=8)
    ax.tick_params(colors="#475569")
    fig.tight_layout()
    return save_chart(fig, "chart1_corridors")

def make_chart2():
    """Pie chart: Distribuição do Mercado Global de Remessas US$669B"""
    setup_chart_style()
    labels = ["Sul da Ásia", "América Latina", "África\nSubsaariana", "Ásia Oriental", "Oriente\nMédio", "Outros"]
    sizes  = [28, 21, 18, 17, 10, 6]
    clrs   = ["#2563EB","#10B981","#F59E0B","#6366F1","#F43F5E","#06B6D4"]
    fig, ax = plt.subplots(figsize=(6, 4))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=clrs, autopct="%1.0f%%",
        startangle=140, pctdistance=0.75,
        wedgeprops=dict(edgecolor="white", linewidth=2)
    )
    for t in autotexts:
        t.set_fontsize(8)
        t.set_fontweight("bold")
        t.set_color("white")
    for t in texts:
        t.set_fontsize(8.5)
        t.set_color("#1E293B")
    ax.set_title("Distribuição do Mercado Global\nde Remessas — US$ 669B (2023)",
                 fontsize=11, fontweight="bold", color="#1E293B", pad=12)
    fig.tight_layout()
    return save_chart(fig, "chart2_market_dist")

def make_chart3():
    """Line chart: Crescimento do Mercado de Remessas"""
    setup_chart_style()
    years_actual   = [2018,2019,2020,2021,2022,2023]
    values_actual  = [529,554,540,605,647,669]
    years_proj     = [2023,2024,2025,2026,2027,2028,2029,2030]
    values_proj    = [669,700,735,773,815,860,908,960]
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    ax.plot(years_actual, values_actual, color="#2563EB", linewidth=2.5,
            marker="o", markersize=6, label="Dados Reais", zorder=3)
    ax.plot(years_proj, values_proj, color="#06B6D4", linewidth=2.5,
            linestyle="--", marker="o", markersize=5, label="Projeção", zorder=3)
    ax.fill_between(years_actual, values_actual, alpha=0.1, color="#2563EB")
    ax.fill_between(years_proj,   values_proj,   alpha=0.1, color="#06B6D4")
    ax.set_xlabel("Ano", fontsize=9, color="#475569")
    ax.set_ylabel("Volume (US$ Bilhões)", fontsize=9, color="#475569")
    ax.set_title("Crescimento do Mercado de Remessas (US$ Bilhões) 2018–2030",
                 fontsize=11, fontweight="bold", color="#1E293B", pad=10)
    ax.legend(fontsize=9)
    ax.axvspan(2024, 2030, alpha=0.04, color="#06B6D4")
    for y, v in zip(years_actual, values_actual):
        ax.annotate(f"${v}B", (y, v), textcoords="offset points", xytext=(0,8),
                    ha="center", fontsize=7, color="#2563EB")
    ax.set_xlim(2017.5, 2030.5)
    ax.tick_params(colors="#475569")
    fig.tight_layout()
    return save_chart(fig, "chart3_market_growth")

def make_chart4():
    """Radar chart: Comparação Estratégica de Competidores"""
    setup_chart_style()
    categories = ["Custo","Velocidade","Cobertura","Transparência","Compliance","Resiliência"]
    N = len(categories)
    companies = {
        "FLUXUS":      ([9,9,8,10,9,9], "#10B981"),
        "Wise":        ([7,8,7,8,7,6],  "#2563EB"),
        "Remitly":     ([6,7,6,6,7,6],  "#F43F5E"),
        "Western Union":([3,5,9,4,7,7], "#F59E0B"),
        "Ripple":      ([8,9,5,6,6,5],  "#6366F1"),
    }
    angles = [n / float(N) * 2 * math.pi for n in range(N)]
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(5.5, 5), subplot_kw=dict(polar=True))
    ax.set_facecolor("#FAFBFF")
    for name, (vals, clr) in companies.items():
        vals_closed = vals + vals[:1]
        ax.plot(angles, vals_closed, linewidth=2, color=clr, label=name)
        ax.fill(angles, vals_closed, alpha=0.06, color=clr)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=8.5, color="#1E293B")
    ax.set_ylim(0, 10)
    ax.set_yticks([2,4,6,8,10])
    ax.set_yticklabels(["2","4","6","8","10"], fontsize=7, color="#94a3b8")
    ax.set_title("Comparação Estratégica de Competidores",
                 fontsize=11, fontweight="bold", color="#1E293B", pad=18)
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.1), fontsize=8)
    fig.tight_layout()
    return save_chart(fig, "chart4_radar")

def make_chart5():
    """Grouped bar: Capital Pré-Fundado Estimado"""
    setup_chart_style()
    companies = ["Western\nUnion","MoneyGram","Wise","Remitly","Ripple","FLUXUS"]
    values = [8.5, 3.2, 2.1, 1.8, 0.9, 0.0]
    clrs = ["#2563EB","#6366F1","#06B6D4","#F43F5E","#F59E0B","#10B981"]
    fig, ax = plt.subplots(figsize=(7, 3.8))
    bars = ax.bar(companies, values, color=clrs, width=0.55, edgecolor="white", linewidth=1)
    ax.set_ylabel("Capital Pré-Fundado (US$ Bilhões)", fontsize=9, color="#475569")
    ax.set_title("Capital Pré-Fundado Estimado (US$ Bilhões)\nVantagem Asset-Light do FLUXUS",
                 fontsize=11, fontweight="bold", color="#1E293B", pad=10)
    for bar, val in zip(bars, values):
        label = f"${val}B" if val > 0 else "ZERO\n(Asset-Light)"
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                label, ha="center", va="bottom", fontsize=8, fontweight="bold", color="#1E293B")
    # annotate FLUXUS
    ax.annotate("FLUXUS\nVantagem", xy=(5, 0.05), fontsize=8.5, color="#10B981",
                ha="center", fontweight="bold")
    ax.tick_params(colors="#475569")
    fig.tight_layout()
    return save_chart(fig, "chart5_prefunded")

def make_chart6():
    """Two-axis area chart: GTV Projeção"""
    setup_chart_style()
    years = [2026, 2027, 2028, 2029, 2030]
    gtv = [0.05, 0.5, 2, 8, 25]
    rev = [0.00075, 0.005, 0.02, 0.072, 0.225]
    fig, ax1 = plt.subplots(figsize=(7.5, 4))
    ax2 = ax1.twinx()
    ax1.fill_between(years, gtv, alpha=0.18, color="#2563EB")
    l1, = ax1.plot(years, gtv, color="#2563EB", linewidth=2.5, marker="o", markersize=7, label="GTV (US$ Bi)")
    l2, = ax2.plot(years, rev, color="#10B981", linewidth=2.5, marker="s", markersize=7, linestyle="--", label="Receita (US$ Bi)")
    ax2.fill_between(years, rev, alpha=0.12, color="#10B981")
    ax1.set_xlabel("Ano", fontsize=9, color="#475569")
    ax1.set_ylabel("GTV (US$ Bilhões)", fontsize=9, color="#2563EB")
    ax2.set_ylabel("Receita (US$ Bilhões)", fontsize=9, color="#10B981")
    ax1.set_title("Projeção de GTV Síncrono FLUXUS (US$ Bilhões) 2026–2030",
                  fontsize=11, fontweight="bold", color="#1E293B", pad=10)
    for y, v in zip(years, gtv):
        ax1.annotate(f"${v}B", (y, v), xytext=(0, 10), textcoords="offset points",
                     ha="center", fontsize=7.5, color="#2563EB", fontweight="bold")
    for y, v in zip(years, rev):
        ax2.annotate(f"${v:.3f}B", (y, v), xytext=(0,-14), textcoords="offset points",
                     ha="center", fontsize=7.5, color="#10B981", fontweight="bold")
    lines = [l1, l2]
    ax1.legend(lines, [l.get_label() for l in lines], loc="upper left", fontsize=8.5)
    ax1.tick_params(colors="#475569")
    ax2.tick_params(colors="#475569")
    fig.tight_layout()
    return save_chart(fig, "chart6_gtv")

def make_chart7():
    """Grouped bar: DRE Projetado 2026-2030"""
    setup_chart_style()
    years = ["2026","2027","2028","2029","2030"]
    revenue = [0.75, 5, 20, 72, 225]   # US$ Milhões
    opex    = [2.5, 8, 22, 50, 110]
    ebitda  = [-1.75, -3, -2, 22, 115]
    x = np.arange(len(years))
    w = 0.25
    fig, ax = plt.subplots(figsize=(7.5, 4))
    ax.bar(x - w, revenue, w, label="Receita (US$ M)", color="#2563EB", edgecolor="white")
    ax.bar(x,     opex,    w, label="OpEx (US$ M)",    color="#F59E0B", edgecolor="white")
    ax.bar(x + w, ebitda,  w, label="EBITDA (US$ M)",  color="#10B981", edgecolor="white")
    ax.axhline(0, color="#94a3b8", linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.set_ylabel("US$ Milhões", fontsize=9, color="#475569")
    ax.set_title("DRE Projetado — FLUXUS 2026–2030\n(US$ Milhões)",
                 fontsize=11, fontweight="bold", color="#1E293B", pad=10)
    ax.legend(fontsize=8.5)
    ax.tick_params(colors="#475569")
    # add value labels
    for bars in [ax.containers[0], ax.containers[1], ax.containers[2]]:
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + (1 if h >= 0 else -3),
                    f"{h:.0f}", ha="center", va="bottom" if h >= 0 else "top",
                    fontsize=7, color="#1E293B")
    fig.tight_layout()
    return save_chart(fig, "chart7_dre")

def make_chart8():
    """Donut chart: Distribuição de Receita por Fonte"""
    setup_chart_style()
    labels = ["Orchestration\nFee", "FX Spread", "VASP Cards", "B2B Treasury", "Data/SaaS"]
    sizes  = [45, 25, 15, 10, 5]
    clrs   = ["#2563EB","#10B981","#F43F5E","#6366F1","#F59E0B"]
    fig, ax = plt.subplots(figsize=(6, 4.5))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=clrs, autopct="%1.0f%%",
        startangle=90, pctdistance=0.78,
        wedgeprops=dict(edgecolor="white", linewidth=2.5, width=0.55)
    )
    for t in autotexts:
        t.set_fontsize(8.5)
        t.set_fontweight("bold")
        t.set_color("white")
    for t in texts:
        t.set_fontsize(8.5)
        t.set_color("#1E293B")
    ax.text(0, 0, "Receita\nTotal", ha="center", va="center",
            fontsize=9, fontweight="bold", color="#1E293B")
    ax.set_title("Distribuição de Receita por Fonte — FLUXUS",
                 fontsize=11, fontweight="bold", color="#1E293B", pad=12)
    fig.tight_layout()
    return save_chart(fig, "chart8_revenue_dist")

def make_chart9():
    """Stacked bar: Cash Flow Projeção"""
    setup_chart_style()
    years = ["2026","2027","2028","2029","2030"]
    op_cf  = [-2, -3, 5, 30, 120]  # US$ M
    inv_cf = [-0.5, -1.5, -3, -5, -8]
    x = np.arange(len(years))
    fig, ax = plt.subplots(figsize=(7.5, 4))
    bars1 = ax.bar(x, op_cf,  width=0.5, label="Operating CF",   color="#2563EB", edgecolor="white")
    bars2 = ax.bar(x, inv_cf, width=0.5, label="Investment CF",  color="#F43F5E",
                   bottom=[max(0,v) for v in op_cf], edgecolor="white")
    ax.axhline(0, color="#94a3b8", linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.set_ylabel("US$ Milhões", fontsize=9, color="#475569")
    ax.set_title("Projeção de Cash Flow (US$ M) — 2026–2030",
                 fontsize=11, fontweight="bold", color="#1E293B", pad=10)
    ax.legend(fontsize=8.5)
    ax.tick_params(colors="#475569")
    for bar in bars1:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + (1 if h >= 0 else -4),
                f"{h:.0f}M", ha="center", va="bottom" if h >= 0 else "top",
                fontsize=7.5, color="#1E293B", fontweight="bold")
    fig.tight_layout()
    return save_chart(fig, "chart9_cashflow")

def make_chart10():
    """Horizontal milestone timeline: Roadmap para Unicórnio"""
    setup_chart_style()
    milestones = [
        ("Q3\n2026", "MVP Launch\nB2C Remittances"),
        ("Q4\n2026", "VASP\nPartnerships x5"),
        ("Q1\n2027", "Série A\nUS$10M"),
        ("Q2\n2027", "GTV\nUS$50M/mês"),
        ("Q4\n2027", "20 Corredores\nAtivos"),
        ("Q2\n2028", "Break-even\nOperacional"),
        ("Q3\n2028", "Série B\nUS$50M"),
        ("2030",     "UNICÓRNIO\nUS$1B+ Valuation"),
    ]
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.set_facecolor("white")
    ax.axis("off")
    n = len(milestones)
    xs = np.linspace(0.05, 0.95, n)
    y_line = 0.5
    ax.axhline(y_line, color="#2563EB", linewidth=2.5, xmin=0.03, xmax=0.97, zorder=1)
    clrs = ["#2563EB","#06B6D4","#10B981","#6366F1","#F59E0B","#F43F5E","#EF4444","#10B981"]
    for i, (x, (label, desc)) in enumerate(zip(xs, milestones)):
        size = 120 if i < n-1 else 180
        ax.scatter(x, y_line, s=size, color=clrs[i], zorder=3, edgecolors="white", linewidth=2)
        y_text = y_line + 0.28 if i % 2 == 0 else y_line - 0.28
        y_anchor = y_line + 0.05 if i % 2 == 0 else y_line - 0.05
        ax.annotate("", xy=(x, y_anchor), xytext=(x, y_text + (-0.08 if i%2==0 else 0.08)),
                    arrowprops=dict(arrowstyle="-", color=clrs[i], lw=1.2))
        va = "bottom" if i % 2 == 0 else "top"
        ax.text(x, y_text + (0.02 if i%2==0 else -0.02), label, ha="center", va=va,
                fontsize=8, fontweight="bold", color=clrs[i])
        ax.text(x, y_text + (0.14 if i%2==0 else -0.14), desc, ha="center", va=va,
                fontsize=7, color="#475569", multialignment="center")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Roadmap para Unicórnio — Milestones Chave 2026–2030",
                 fontsize=11, fontweight="bold", color="#1E293B", y=0.97)
    fig.tight_layout()
    return save_chart(fig, "chart10_roadmap")


def generate_all_charts():
    print("Generating charts...")
    charts = {}
    charts["chart1"] = make_chart1()
    charts["chart2"] = make_chart2()
    charts["chart3"] = make_chart3()
    charts["chart4"] = make_chart4()
    charts["chart5"] = make_chart5()
    charts["chart6"] = make_chart6()
    charts["chart7"] = make_chart7()
    charts["chart8"] = make_chart8()
    charts["chart9"] = make_chart9()
    charts["chart10"] = make_chart10()
    print(f"  {len(charts)} charts generated.")
    return charts


# ═══════════════════════════════════════════════════════════════════════════════
# CANVAS HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

class PageState:
    """Shared mutable state for onPage callbacks."""
    chapter_idx  = 0   # 0-based
    chapter_name = CHAPTER_NAMES[0]
    page_title   = ""
    page_counter = 0


def draw_content_page(c, doc, state: PageState):
    """onPage callback: sidebar + header bar + footer."""
    w, h = A4
    cap_color = HexColor(CHAPTER_COLORS[state.chapter_idx])

    # ── 2mm top bar ──
    c.setFillColor(cap_color)
    c.rect(0, h - 2*mm, w, 2*mm, fill=1, stroke=0)

    # ── 6mm left sidebar ──
    c.setFillColor(cap_color)
    c.rect(0, FOOTER_H, SIDEBAR_W, h - FOOTER_H - 2*mm, fill=1, stroke=0)

    # ── Header area ──
    hdr_y = h - 2*mm - HEADER_H
    c.setFillColor(HexColor(LIGHT_BG))
    c.rect(SIDEBAR_W, hdr_y, w - SIDEBAR_W, HEADER_H, fill=1, stroke=0)

    # chapter name (small)
    c.setFillColor(HexColor(BODY_TEXT))
    c.setFont("Helvetica", 7)
    c.drawString(SIDEBAR_W + 8*mm, hdr_y + HEADER_H - 8*mm,
                 state.chapter_name.upper())

    # page title
    c.setFillColor(HexColor(DARK_TEXT))
    c.setFont("Helvetica-Bold", 10)
    title_str = state.page_title[:80]
    c.drawString(SIDEBAR_W + 8*mm, hdr_y + 4*mm, title_str)

    # page number right
    c.setFillColor(HexColor(BODY_TEXT))
    c.setFont("Helvetica", 8)
    c.drawRightString(w - 8*mm, hdr_y + HEADER_H - 8*mm, f"Pág. {state.page_counter}")

    # thin separator line
    c.setStrokeColor(cap_color)
    c.setLineWidth(0.5)
    c.line(SIDEBAR_W, hdr_y, w, hdr_y)

    # ── Footer ──
    c.setFillColor(HexColor("#E2E8F0"))
    c.rect(SIDEBAR_W, 0, w - SIDEBAR_W, FOOTER_H, fill=1, stroke=0)
    c.setStrokeColor(cap_color)
    c.setLineWidth(0.5)
    c.line(SIDEBAR_W, FOOTER_H, w, FOOTER_H)
    c.setFillColor(HexColor(BODY_TEXT))
    c.setFont("Helvetica", 7)
    c.drawString(SIDEBAR_W + 8*mm, 4*mm,
                 "FLUXUS · Investor Edition 2026 · Confidential")
    c.drawRightString(w - 8*mm, 4*mm, f"{state.page_counter}")


# ═══════════════════════════════════════════════════════════════════════════════
# TABLE BUILDERS
# ═══════════════════════════════════════════════════════════════════════════════

def make_table_styles(accent_hex):
    accent = HexColor(accent_hex)
    return TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), accent),
        ("TEXTCOLOR",    (0,0), (-1,0), white),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,0), 8.5),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [HexColor(TABLE_ALT), white]),
        ("FONTNAME",     (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE",     (0,1), (-1,-1), 8),
        ("TEXTCOLOR",    (0,1), (-1,-1), HexColor(DARK_TEXT)),
        ("GRID",         (0,0), (-1,-1), 0.3, HexColor("#CBD5E1")),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",   (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0), (-1,-1), 4),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("FONTNAME",     (0,1), (0,-1), "Helvetica-Bold"),
    ])

def build_swift_table():
    data = [
        ["Dimensão", "SWIFT / Banca Tradicional", "FLUXUS Orquestrador"],
        ["Velocidade", "1–5 dias úteis", "< 60 segundos"],
        ["Custo", "6–15% (taxas + FX)", "0.1–1.2%"],
        ["Transparência", "Opaco — taxas ocultas", "Auditável on-chain"],
        ["Pré-funding", "Capital imobilizado 24/7", "Zero (JIT Liquidity)"],
        ["Compliance", "Manual, batch diário", "Automático em tempo real"],
        ["Disponibilidade", "Horário bancário", "24/7/365"],
    ]
    col_widths = [90, 160, 150]
    t = Table(data, colWidths=col_widths)
    t.setStyle(make_table_styles(CHAPTER_COLORS[0]))
    return t

def build_nostro_table():
    data = [
        ["Aspecto", "Modelo Tradicional (Nostro)", "FLUXUS JIT"],
        ["Capital Necessário", "US$ 1B+ imobilizado", "Zero (Asset-Light)"],
        ["Liquidez", "Pré-fundada em cada moeda", "Orquestrada sob demanda"],
        ["Risco FX", "Alto — capital exposto", "Minimizado — posição zero"],
        ["Reconciliação", "Manual, lote diário (T+1)", "Automática, atômica"],
        ["Latência", "24–72 horas", "Sub-minuto"],
        ["Custo Operacional", "Elevado (pessoal + infra)", "95% menor com IA"],
    ]
    col_widths = [100, 160, 140]
    t = Table(data, colWidths=col_widths)
    t.setStyle(make_table_styles(CHAPTER_COLORS[0]))
    return t

def build_competitive_table():
    data = [
        ["Empresa", "Modelo", "Cobertura", "Custo Médio", "Capital Pre-fund.", "Velocidade"],
        ["FLUXUS",        "Orquestrador IA",   "Global+",   "0.1–1.2%", "Zero",      "< 60s"],
        ["Wise",          "Netting Local",      "130+ países","0.5–1.5%","US$ 2.1B",  "1h–2h"],
        ["Remitly",       "Corredor Direto",    "170+ países","1.5–3%",  "US$ 1.8B",  "Minutos"],
        ["Western Union", "Rede Agente",        "200+ países","5–10%",   "US$ 8.5B",  "Minutos/Dias"],
        ["Ripple/ODL",    "Crypto Bridge",      "70+ países", "1–3%",    "US$ 0.9B",  "Segundos"],
        ["MoneyGram",     "Rede Física",        "200+ países","5–12%",   "US$ 3.2B",  "Minutos/Dias"],
    ]
    col_widths = [70, 90, 70, 65, 65, 60]
    t = Table(data, colWidths=col_widths)
    t.setStyle(make_table_styles(CHAPTER_COLORS[1]))
    return t

def build_dre_table():
    data = [
        ["Indicador (US$ M)", "2026", "2027", "2028", "2029", "2030"],
        ["GTV Total",         "50",   "500",  "2.000","8.000","25.000"],
        ["Receita Bruta",     "0.75", "5",    "20",   "72",   "225"],
        ["OpEx Total",        "2.5",  "8",    "22",   "50",   "110"],
        ["EBITDA",            "(1.75)","(3)",  "(2)",  "22",   "115"],
        ["Margem EBITDA",     "N/A",  "N/A",  "N/A",  "30%",  "51%"],
        ["Headcount",         "12",   "35",   "85",   "200",  "400"],
    ]
    col_widths = [110, 60, 60, 60, 60, 60]
    t = Table(data, colWidths=col_widths)
    t.setStyle(make_table_styles(CHAPTER_COLORS[4]))
    return t

def build_vasp_table():
    data = [
        ["Jurisdição", "Framework", "Status FLUXUS", "Requisito Chave"],
        ["União Europeia",   "MiCA 2024",          "Parceiro VASP",  "CASP License via VASP"],
        ["EUA",              "FinCEN / MSB",        "Modelo B2B",     "AML/KYC via VASP"],
        ["Brasil",           "Banco Central VASP",  "Parceiro Local", "Registro BCB Obrigatório"],
        ["Dubai (DIFC)",     "VARA / DFSA",         "Parceiro VASP",  "VARA License via VASP"],
        ["Singapura",        "MAS PSA",             "Parceiro MAS",   "Major Payment Institution"],
        ["Nigéria",          "CBN PSSP",            "Via VASP",       "PSB License Parceiro"],
        ["Global",           "FATF Rec. 15+16",     "Compliant",      "Travel Rule Integrado"],
    ]
    col_widths = [80, 90, 85, 155]
    t = Table(data, colWidths=col_widths)
    t.setStyle(make_table_styles(CHAPTER_COLORS[5]))
    return t


# ═══════════════════════════════════════════════════════════════════════════════
# STYLES
# ═══════════════════════════════════════════════════════════════════════════════

def build_styles(cap_color_hex="#2563EB"):
    cap_color = HexColor(cap_color_hex)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        "FluxH3",
        fontName="Helvetica-Bold",
        fontSize=13,
        textColor=cap_color,
        spaceAfter=6,
        spaceBefore=8,
        leading=16,
    ))
    styles.add(ParagraphStyle(
        "FluxBody",
        fontName="Helvetica",
        fontSize=9.5,
        textColor=HexColor(BODY_TEXT),
        spaceAfter=5,
        leading=15,
        alignment=TA_JUSTIFY,
    ))
    styles.add(ParagraphStyle(
        "FluxBullet",
        fontName="Helvetica",
        fontSize=9.5,
        textColor=HexColor(BODY_TEXT),
        spaceAfter=3,
        leading=14,
        leftIndent=12,
        bulletIndent=0,
    ))
    styles.add(ParagraphStyle(
        "FluxCaption",
        fontName="Helvetica-Oblique",
        fontSize=8,
        textColor=HexColor(BODY_TEXT),
        spaceAfter=4,
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        "FluxPageTitle",
        fontName="Helvetica-Bold",
        fontSize=14,
        textColor=HexColor(DARK_TEXT),
        spaceAfter=8,
        spaceBefore=2,
        leading=18,
    ))
    styles.add(ParagraphStyle(
        "TocEntry",
        fontName="Helvetica",
        fontSize=10,
        textColor=HexColor(DARK_TEXT),
        spaceAfter=4,
        leading=14,
    ))
    styles.add(ParagraphStyle(
        "TocChapter",
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=HexColor(PRIMARY_BLUE),
        spaceAfter=3,
        spaceBefore=8,
        leading=16,
    ))
    return styles


# ═══════════════════════════════════════════════════════════════════════════════
# STAT BOX
# ═══════════════════════════════════════════════════════════════════════════════

class StatBox(Flowable):
    def __init__(self, number, label, color_hex, width=120, height=55):
        Flowable.__init__(self)
        self.number = number
        self.label  = label
        self.color  = HexColor(color_hex)
        self.width  = width
        self.height = height

    def draw(self):
        c = self.canv
        c.setFillColor(self.color)
        c.roundRect(0, 0, self.width, self.height, 6, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(self.width/2, self.height - 24, self.number)
        c.setFont("Helvetica", 8)
        c.drawCentredString(self.width/2, 8, self.label)

    def wrap(self, avW, avH):
        return self.width, self.height


class StatBoxRow(Flowable):
    """Row of stat boxes."""
    def __init__(self, stats, cap_color_hex):
        Flowable.__init__(self)
        self.stats = stats  # list of (number, label)
        self.color = cap_color_hex
        self._height = 60

    def draw(self):
        c = self.canv
        n = len(self.stats)
        box_w = 110
        gap   = 8
        total_w = n * box_w + (n-1) * gap
        start_x = 0
        for i, (num, lbl) in enumerate(self.stats):
            x = start_x + i * (box_w + gap)
            box = StatBox(num, lbl, self.color, box_w, 55)
            box.canv = c
            c.saveState()
            c.translate(x, 0)
            box.draw()
            c.restoreState()

    def wrap(self, avW, avH):
        return avW, self._height


# ═══════════════════════════════════════════════════════════════════════════════
# CONTENT PARSING
# ═══════════════════════════════════════════════════════════════════════════════

def parse_content():
    """Parse JSON into structure: list of chapters, each with list of pages."""
    with open(CONTENT_JSON, "r", encoding="utf-8", errors="replace") as f:
        raw = json.load(f)

    chapters = []
    current_chapter = None
    current_page    = None

    for item in raw:
        style, text = item[0], item[1]
        text = fix_text(text)

        if style == "Heading 2":
            if current_chapter is not None:
                if current_page:
                    current_chapter["pages"].append(current_page)
                chapters.append(current_chapter)
            current_chapter = {"title": text, "pages": []}
            current_page = None

        elif style == "Heading 3":
            if current_page and current_chapter:
                current_chapter["pages"].append(current_page)
            current_page = {"title": text, "paragraphs": []}

        elif style == "Normal":
            if current_page is None:
                current_page = {"title": "Introdução", "paragraphs": []}
            current_page["paragraphs"].append(text)

    # flush last
    if current_page and current_chapter:
        current_chapter["pages"].append(current_page)
    if current_chapter:
        chapters.append(current_chapter)

    return chapters


def clean_page_title(title):
    """Strip 'Página N: ' prefix."""
    m = re.match(r"P[aá]gina\s+\d+:\s*(.*)", title, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return title.strip()


# ═══════════════════════════════════════════════════════════════════════════════
# COVER PAGE (canvas)
# ═══════════════════════════════════════════════════════════════════════════════

def draw_cover(c, doc):
    w, h = A4
    # Draw cover image if available
    if os.path.exists(COVER_IMG):
        c.drawImage(COVER_IMG, 0, 0, width=w, height=h, preserveAspectRatio=False)
    else:
        # fallback gradient
        c.setFillColor(HexColor(DEEP_BLUE_1))
        c.rect(0, 0, w, h, fill=1, stroke=0)

    # Dark overlay for text readability
    c.setFillColor(HexColor("#0D1B2A"))
    c.setFillAlpha(0.45)
    c.rect(0, 0, w, h/2 + 40, fill=1, stroke=0)
    c.setFillAlpha(1)

    # Top branding bar
    c.setFillColor(HexColor(PRIMARY_BLUE))
    c.rect(0, h - 18*mm, w, 18*mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(20*mm, h - 11*mm, "FLUXUS · Nexus de Orquestração Financeira")
    c.setFont("Helvetica", 9)
    c.drawRightString(w - 15*mm, h - 11*mm, "CONFIDENTIAL — INVESTOR EDITION 2026")

    # Main title area (bottom center)
    c.setFillColor(HexColor(EMERALD))
    c.rect(0, h*0.27 - 2, w, 3, fill=1, stroke=0)

    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(w/2, h*0.27 + 18, "RELATÓRIO ANUAL 2026")

    c.setFillColor(HexColor(CYAN))
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(w/2, h*0.27 - 12, "Investor Edition 2026")

    c.setFillColor(HexColor("#CBD5E1"))
    c.setFont("Helvetica", 11)
    c.drawCentredString(w/2, h*0.27 - 30,
                        "Encyclopédia do Nexus Financeiro Síncrono")

    # Bottom
    c.setFillColor(HexColor(DEEP_BLUE_1))
    c.rect(0, 0, w, 22*mm, fill=1, stroke=0)
    c.setFillColor(HexColor("#64748B"))
    c.setFont("Helvetica", 8)
    c.drawString(20*mm, 8*mm, "© 2026 FLUXUS Technologies Ltd. · All Rights Reserved")
    c.drawRightString(w - 15*mm, 8*mm, "fluxus.io")


# ═══════════════════════════════════════════════════════════════════════════════
# TOC PAGE
# ═══════════════════════════════════════════════════════════════════════════════

def draw_toc(c, doc):
    w, h = A4

    # Background
    c.setFillColor(white)
    c.rect(0, 0, w, h, fill=1, stroke=0)

    # Top bar
    c.setFillColor(HexColor(PRIMARY_BLUE))
    c.rect(0, h - 22*mm, w, 22*mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(20*mm, h - 14*mm, "SUMÁRIO — ÍNDICE DE CONTEÚDO")
    c.setFont("Helvetica", 9)
    c.drawRightString(w - 15*mm, h - 14*mm, "FLUXUS Investor Edition 2026")

    # Left accent bar
    c.setFillColor(HexColor(PRIMARY_BLUE))
    c.rect(0, 0, 6*mm, h - 22*mm, fill=1, stroke=0)

    # Chapter list
    chapters_data = [
        ("Capítulo 1", "A Crise Global da Remessa e o Peso do Legado",        4,  11),
        ("Capítulo 2", "Anatomia dos Gigantes e a Falácia da Eficiência",      12, 19),
        ("Capítulo 3", "A Tese FLUXUS — O Fim das Licenças Bancárias Pesadas", 20, 27),
        ("Capítulo 4", "A Engenharia da Transparência — Auditoria em Tempo Real",28, 37),
        ("Capítulo 5", "Contabilidade Estrutural e Engenharia Financeira",     38, 47),
        ("Capítulo 6", "Regulação Global e Compliance — Software-as-Law",      48, 55),
        ("Capítulo 7", "Escala, Verticais e o Caminho do Unicórnio",           56, 63),
    ]

    y = h - 40*mm
    for i, (chap_num, title, pg_start, pg_end) in enumerate(chapters_data):
        cap_clr = HexColor(CHAPTER_COLORS[i])

        # colored chip
        c.setFillColor(cap_clr)
        c.roundRect(8*mm, y - 3, 28*mm, 16, 4, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(22*mm, y + 2, chap_num)

        # title
        c.setFillColor(HexColor(DARK_TEXT))
        c.setFont("Helvetica-Bold", 11)
        c.drawString(42*mm, y + 2, title[:60])

        # page range
        c.setFillColor(HexColor(BODY_TEXT))
        c.setFont("Helvetica", 9)
        c.drawRightString(w - 15*mm, y + 2, f"Págs. {pg_start}–{pg_end}")

        # dotted line
        c.setStrokeColor(HexColor("#CBD5E1"))
        c.setLineWidth(0.5)
        c.setDash([2, 3])
        c.line(42*mm, y - 2, w - 30*mm, y - 2)
        c.setDash()

        y -= 22*mm

    # Bottom note
    c.setFillColor(HexColor(BODY_TEXT))
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(w/2, 25*mm,
        "Este relatório contém informações confidenciais destinadas exclusivamente a investidores qualificados.")

    # Footer
    c.setFillColor(HexColor("#E2E8F0"))
    c.rect(6*mm, 0, w - 6*mm, 14*mm, fill=1, stroke=0)
    c.setFillColor(HexColor(BODY_TEXT))
    c.setFont("Helvetica", 7)
    c.drawString(10*mm, 5*mm, "FLUXUS · Investor Edition 2026 · Confidential")
    c.drawRightString(w - 10*mm, 5*mm, "2")


# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTIVE SUMMARY PAGE
# ═══════════════════════════════════════════════════════════════════════════════

def draw_exec_summary(c, doc):
    w, h = A4

    c.setFillColor(white)
    c.rect(0, 0, w, h, fill=1, stroke=0)

    # Top bar
    c.setFillColor(HexColor(PRIMARY_BLUE))
    c.rect(0, h - 22*mm, w, 22*mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(20*mm, h - 14*mm, "SUMÁRIO EXECUTIVO")
    c.setFont("Helvetica", 9)
    c.drawRightString(w - 15*mm, h - 14*mm, "FLUXUS · 2026")

    # Sidebar
    c.setFillColor(HexColor(PRIMARY_BLUE))
    c.rect(0, 0, 6*mm, h - 22*mm, fill=1, stroke=0)

    # Intro text
    intro = (
        "O FLUXUS representa a próxima geração de infraestrutura financeira global — "
        "um orquestrador de liquidez agnóstico de tecnologia que elimina o capital pré-fundado, "
        "reduz custos de remessa em até 90%, e conecta VASPs, investidores e trilhos locais em "
        "sintonia síncrona. Nosso modelo asset-light e nossa camada de compliance automatizada "
        "posicionam o FLUXUS para capturar o mercado de US$ 669 bilhões de remessas globais."
    )
    c.setFillColor(HexColor(DARK_TEXT))
    c.setFont("Helvetica", 9.5)
    # word-wrap simple
    words = intro.split()
    line = ""
    y = h - 32*mm
    for word in words:
        test = (line + " " + word).strip()
        if c.stringWidth(test, "Helvetica", 9.5) < w - 30*mm:
            line = test
        else:
            c.drawString(12*mm, y, line)
            y -= 13
            line = word
    if line:
        c.drawString(12*mm, y, line)

    y -= 10

    # Key metrics boxes
    metrics = [
        ("US$ 669B", "Mercado Global 2023"),
        ("< 60s",    "Liquidação Síncrona"),
        ("0.1-1.2%", "Custo FLUXUS"),
        ("ZERO",     "Capital Pré-fundado"),
        ("US$ 25B",  "GTV 2030 Target"),
        ("51%",      "Margem EBITDA 2030"),
    ]
    box_w = (w - 30*mm) / 3 - 4
    box_h = 52
    cols  = 3
    y -= 5
    for idx, (num, lbl) in enumerate(metrics):
        col = idx % cols
        row = idx // cols
        x = 10*mm + col * (box_w + 4)
        by = y - row * (box_h + 6)
        clr = HexColor(CHAPTER_COLORS[idx % len(CHAPTER_COLORS)])
        c.setFillColor(clr)
        c.roundRect(x, by - box_h, box_w, box_h, 5, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(x + box_w/2, by - 22, num)
        c.setFont("Helvetica", 7.5)
        c.drawCentredString(x + box_w/2, by - box_h + 8, lbl)

    y_after_boxes = y - 2 * (box_h + 6) - 14

    # Section: Why FLUXUS
    c.setFillColor(HexColor(LIGHT_BG))
    c.rect(8*mm, y_after_boxes - 82, w - 20*mm, 80, fill=1, stroke=0)
    c.setFillColor(HexColor(PRIMARY_BLUE))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(12*mm, y_after_boxes - 10, "POR QUE O FLUXUS VENCE")
    bullet_pts = [
        "Orquestração agnóstica: integra SWIFT, Crypto, PIX, UPI, mobile money sem burocracia bancária",
        "Compliance-as-Software: Travel Rule, KYT on-chain, KYC invisível automatizados nativamente",
        "Modelo Revenue: Orchestration Fee (45%) + FX Spread (25%) + VASP Cards (15%) + B2B + SaaS",
        "Roadmap de Unicórnio: Break-even 2028, US$ 1B+ valuation projetado para 2030",
    ]
    c.setFillColor(HexColor(DARK_TEXT))
    c.setFont("Helvetica", 8.5)
    by2 = y_after_boxes - 26
    for bp in bullet_pts:
        c.drawString(14*mm, by2, "▸  " + bp[:100])
        by2 -= 13

    # Footer
    c.setFillColor(HexColor("#E2E8F0"))
    c.rect(6*mm, 0, w - 6*mm, 14*mm, fill=1, stroke=0)
    c.setFillColor(HexColor(BODY_TEXT))
    c.setFont("Helvetica", 7)
    c.drawString(10*mm, 5*mm, "FLUXUS · Investor Edition 2026 · Confidential")
    c.drawRightString(w - 10*mm, 5*mm, "3")


# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER DIVIDER PAGE
# ═══════════════════════════════════════════════════════════════════════════════

def draw_chapter_divider(c, doc, chapter_idx, chapter_title, chapter_subtitle=""):
    w, h = A4
    cap_color = HexColor(CHAPTER_COLORS[chapter_idx])

    # Full-bleed blue gradient simulation (two rects)
    c.setFillColor(HexColor(DEEP_BLUE_1))
    c.rect(0, 0, w, h, fill=1, stroke=0)
    c.setFillColor(HexColor(DEEP_BLUE_2))
    c.rect(0, 0, w, h * 0.45, fill=1, stroke=0)

    # Accent bar left
    c.setFillColor(cap_color)
    c.rect(0, 0, 8*mm, h, fill=1, stroke=0)

    # Chapter number large ghosted text
    cap_num = chapter_idx + 1
    c.setFillColor(HexColor("#1E40AF"))
    c.setFont("Helvetica-Bold", 180)
    c.drawRightString(w - 10*mm, 30*mm, str(cap_num).zfill(2))

    # Chapter label
    c.setFillColor(cap_color)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(18*mm, h * 0.52 + 40, f"CAPÍTULO {cap_num:02d}")

    # Horizontal rule
    c.setStrokeColor(cap_color)
    c.setLineWidth(2)
    c.line(18*mm, h * 0.52 + 30, w - 18*mm, h * 0.52 + 30)

    # Title
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 28)
    # Simple line-break at ~50 chars
    title_words = chapter_title.split()
    line1, line2 = "", ""
    for word in title_words:
        if c.stringWidth(line1 + " " + word, "Helvetica-Bold", 28) < w - 40*mm:
            line1 = (line1 + " " + word).strip()
        else:
            line2 = (line2 + " " + word).strip()
    if line2:
        c.drawString(18*mm, h * 0.52 - 5, line1)
        c.drawString(18*mm, h * 0.52 - 35, line2)
    else:
        c.drawString(18*mm, h * 0.52, line1)

    # Subtitle / year
    c.setFillColor(HexColor("#93C5FD"))
    c.setFont("Helvetica", 14)
    c.drawString(18*mm, h * 0.52 - 60,
                 chapter_subtitle or "Encyclopédia do Nexus Financeiro Síncrono · 2026")

    # Bottom stripe
    c.setFillColor(cap_color)
    c.rect(0, 0, w, 12*mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica", 8)
    c.drawString(18*mm, 4*mm, "FLUXUS · Investor Edition 2026 · Confidential")
    c.drawRightString(w - 12*mm, 4*mm, "fluxus.io")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN BUILD
# ═══════════════════════════════════════════════════════════════════════════════

def build_pdf():
    print("Parsing content JSON...")
    chapters = parse_content()
    print(f"  {len(chapters)} chapters parsed.")

    print("Generating charts...")
    charts = generate_all_charts()

    print("Building PDF...")
    state = PageState()

    c = rl_canvas.Canvas(OUTPUT_PDF, pagesize=A4)
    c.setTitle("FLUXUS Annual Report 2026 — Investor Edition")
    c.setAuthor("FLUXUS Technologies")
    c.setSubject("Encyclopédia do Nexus Financeiro Síncrono")

    # ── Page 1: Cover ─────────────────────────────────────────────────────────
    draw_cover(c, None)
    c.showPage()

    # ── Page 2: TOC ───────────────────────────────────────────────────────────
    draw_toc(c, None)
    c.showPage()

    # ── Page 3: Executive Summary ─────────────────────────────────────────────
    draw_exec_summary(c, None)
    c.showPage()

    global_page = 3  # after cover, toc, exec summary

    # ── Chapters ──────────────────────────────────────────────────────────────
    # Chart assignment: which chart goes on which (chapter_idx, page_within_chapter) 0-based
    CHART_PLACEMENT = {
        (0, 0): charts["chart1"],   # Cap1 pg1
        (0, 1): charts["chart2"],   # Cap1 pg2
        (0, 7): charts["chart3"],   # Cap1 pg8
        (1, 0): charts["chart4"],   # Cap2 pg9 (first page of cap2)
        (1, 6): charts["chart5"],   # Cap2 pg15
        (2, 7): charts["chart6"],   # Cap3 pg24
        (4, 0): charts["chart7"],   # Cap5 pg35
        (4, 4): charts["chart8"],   # Cap5 pg39
        (4, 9): charts["chart9"],   # Cap5 pg44
        (6, 7): charts["chart10"],  # Cap7 pg59
    }

    # Table placement: (chapter_idx, page_within_chapter) -> builder fn
    TABLE_PLACEMENT = {
        (0, 1): build_swift_table,
        (0, 2): build_nostro_table,
        (1, 5): build_competitive_table,
        (4, 0): build_dre_table,
        (5, 0): build_vasp_table,
    }

    w, h = A4

    for cap_idx, chapter in enumerate(chapters):
        cap_color_hex = CHAPTER_COLORS[cap_idx % len(CHAPTER_COLORS)]
        cap_color     = HexColor(cap_color_hex)
        styles        = build_styles(cap_color_hex)

        # ── Divider page ──
        state.chapter_idx  = cap_idx
        state.chapter_name = CHAPTER_NAMES[cap_idx] if cap_idx < len(CHAPTER_NAMES) else chapter["title"]
        global_page += 1
        draw_chapter_divider(c, None, cap_idx, chapter["title"])
        c.showPage()

        # ── Content pages ──
        pages = chapter["pages"]
        for pg_idx, page in enumerate(pages):
            global_page += 1
            state.page_counter = global_page
            page_title_clean   = clean_page_title(page["title"])
            state.page_title   = page_title_clean

            # --- Draw page background + decorations via canvas ---
            c.saveState()
            draw_content_page(c, None, state)
            c.restoreState()

            # --- Build content using platypus-like drawing on canvas ---
            # We'll draw text manually on the canvas for simplicity and control

            content_x = SIDEBAR_W + 10*mm
            content_w = w - content_x - MARGIN_R
            content_y_top = h - MARGIN_T - 8*mm
            content_y_bot = FOOTER_H + 4*mm
            max_h = content_y_top - content_y_bot

            # Page Title
            c.setFillColor(cap_color)
            c.setFont("Helvetica-Bold", 13)
            # draw title
            title_y = content_y_top
            title_lines = []
            words = page_title_clean.split()
            line = ""
            for word in words:
                test = (line + " " + word).strip()
                if c.stringWidth(test, "Helvetica-Bold", 13) < content_w:
                    line = test
                else:
                    if line:
                        title_lines.append(line)
                    line = word
            if line:
                title_lines.append(line)
            for tline in title_lines[:2]:
                c.drawString(content_x, title_y, tline)
                title_y -= 16
            title_y -= 4

            # Thin rule under title
            c.setStrokeColor(cap_color)
            c.setLineWidth(0.7)
            c.line(content_x, title_y, content_x + content_w, title_y)
            title_y -= 8

            cur_y = title_y

            def available_h():
                return cur_y - content_y_bot

            # Paragraphs
            for para_text in page["paragraphs"]:
                if cur_y < content_y_bot + 30:
                    break
                # strip bold tags for plain canvas drawing
                plain = re.sub(r'<b>(.*?)</b>', r'\1', para_text)
                plain = re.sub(r'&amp;', '&', plain)
                plain = plain.strip()
                if not plain:
                    continue

                # word-wrap at 9.5pt
                c.setFillColor(HexColor(BODY_TEXT))
                c.setFont("Helvetica", 9.5)
                words_p = plain.split()
                lines_p = []
                cur_line = ""
                for w_word in words_p:
                    test = (cur_line + " " + w_word).strip()
                    if c.stringWidth(test, "Helvetica", 9.5) < content_w:
                        cur_line = test
                    else:
                        if cur_line:
                            lines_p.append(cur_line)
                        cur_line = w_word
                if cur_line:
                    lines_p.append(cur_line)

                for ln in lines_p:
                    if cur_y < content_y_bot + 12:
                        break
                    c.drawString(content_x, cur_y, ln)
                    cur_y -= 14
                cur_y -= 4  # paragraph spacing

            # ── Chart ──
            chart_key = (cap_idx, pg_idx)
            if chart_key in CHART_PLACEMENT:
                chart_path = CHART_PLACEMENT[chart_key]
                if os.path.exists(chart_path):
                    ch_avail = cur_y - content_y_bot - 5
                    ch_h = min(120, ch_avail)
                    ch_h = max(ch_h, 60)
                    aspect = 7.5 / 4.0  # default W/H ratio
                    ch_w = min(content_w, ch_h * aspect)
                    ch_h = ch_w / aspect
                    if cur_y - ch_h > content_y_bot:
                        c.drawImage(chart_path, content_x,
                                    cur_y - ch_h, width=ch_w, height=ch_h,
                                    preserveAspectRatio=True, mask="auto")
                        cur_y -= ch_h + 6
                        # caption
                        c.setFillColor(HexColor(BODY_TEXT))
                        c.setFont("Helvetica-Oblique", 7.5)
                        c.drawCentredString(content_x + content_w/2, cur_y,
                                            f"Figura {len(CHART_PLACEMENT)} · Análise FLUXUS")
                        cur_y -= 12

            # ── Table ──
            table_key = (cap_idx, pg_idx)
            if table_key in TABLE_PLACEMENT:
                tbl_fn  = TABLE_PLACEMENT[table_key]
                tbl_obj = tbl_fn()
                tbl_w, tbl_h = tbl_obj.wrap(content_w, cur_y - content_y_bot - 10)
                if cur_y - tbl_h > content_y_bot:
                    tbl_obj.drawOn(c, content_x, cur_y - tbl_h)
                    cur_y -= tbl_h + 8

            c.showPage()

    # ── Save ──────────────────────────────────────────────────────────────────
    c.save()
    print(f"PDF saved: {OUTPUT_PDF}")


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    build_pdf()

    # Verify
    import struct
    size = os.path.getsize(OUTPUT_PDF)
    # count pages
    with open(OUTPUT_PDF, "rb") as f:
        content = f.read()
    page_count = content.count(b"/Type /Page\n") + content.count(b"/Type/Page\n") + content.count(b"/Type /Page\r")
    if page_count < 5:
        # fallback: count showPage markers via EOF markers
        page_count = content.count(b"%%EOF") or content.count(b"endobj")

    print(f"\n{'='*50}")
    print(f"SUCCESS: FLUXUS_ANNUAL_REPORT_2026.pdf")
    print(f"File size : {size:,} bytes ({size/1024/1024:.2f} MB)")
    print(f"Output    : {OUTPUT_PDF}")
    print(f"{'='*50}")
