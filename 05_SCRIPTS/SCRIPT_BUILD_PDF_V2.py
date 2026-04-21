"""
FLUXUS Annual Report 2026 — v2
Design: editorial annual report, 100% page coverage, multi-column, geometric blocks
Palette: White + Near-Black + Gold (#C9A84C) + chapter accent colors
"""
import json, os, textwrap, math
from pathlib import Path

from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black, Color, toColor
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from PIL import Image as PILImage

# ── Paths (raiz = remitly-p2p; dados em 06_DATA) ─────────────────────────────
_REPO = Path(__file__).resolve().parents[1]
_DATA = _REPO / "06_DATA"
BASE = str(_DATA)
OUT = str(_DATA / "DATA_FLUXUS_ANNUAL_REPORT_V2.pdf")
LOGO = str(_DATA / "DATA_FLUXUS_COVER.png")
JSON = str(_DATA / "DATA_CONTENT_RAW.json")
CHARTS = str(_DATA / "charts")
os.makedirs(CHARTS, exist_ok=True)

# ── Page geometry ──────────────────────────────────────────────────────────
W, H   = A4          # 595.27 x 841.89 pt
ML, MR = 18*mm, 18*mm
MT, MB = 16*mm, 14*mm
CW     = W - ML - MR  # content width ~559 pt

# ── Palette ────────────────────────────────────────────────────────────────
GOLD      = HexColor('#C9A84C')
GOLD_PALE = HexColor('#F5EDD6')
GOLD_DARK = HexColor('#9B7C2E')
NEAR_BLK  = HexColor('#1A1A1A')
DARK_GRAY = HexColor('#3A3A3A')
MID_GRAY  = HexColor('#888888')
LIGHT_BG  = HexColor('#F7F5F0')
WHITE     = HexColor('#FFFFFF')
DIV_DARK  = HexColor('#0D1B2A')
DIV_MID   = HexColor('#1565C0')

CHAPTER_COLORS = {
    1: HexColor('#C9A84C'),  # gold
    2: HexColor('#1B3A7A'),  # navy
    3: HexColor('#2D7D52'),  # green
    4: HexColor('#6248C0'),  # purple
    5: HexColor('#D4580A'),  # orange
    6: HexColor('#0E7FA8'),  # teal
    7: HexColor('#B82020'),  # red
}
CHAPTER_LIGHT = {
    1: HexColor('#FBF3DC'),
    2: HexColor('#DCE6FB'),
    3: HexColor('#DCFBEC'),
    4: HexColor('#ECDCFB'),
    5: HexColor('#FBEDDC'),
    6: HexColor('#DCFBFB'),
    7: HexColor('#FBDCDC'),
}

# ── Content loading ────────────────────────────────────────────────────────
with open(JSON, encoding='utf-8') as f:
    raw = json.load(f)

def clean(t):
    t = t.replace('**', '').replace('*', '').replace('`', '')
    return t.strip()

# Group into chapters → pages
chapters = []
cur_chap = None
cur_page = None
for style, text in raw:
    text = text.strip()
    if not text: continue
    if style == 'Heading 2':
        if cur_page and cur_chap is not None:
            chapters[cur_chap]['pages'].append(cur_page)
        cur_chap = len(chapters)
        chapters.append({'title': clean(text), 'pages': []})
        cur_page = None
    elif style == 'Heading 3':
        if cur_page is not None and cur_chap is not None:
            chapters[cur_chap]['pages'].append(cur_page)
        cur_page = {'title': clean(text), 'body': []}
    elif style == 'Normal' and cur_page is not None:
        cur_page['body'].append(clean(text))
if cur_page and cur_chap is not None:
    chapters[cur_chap]['pages'].append(cur_page)

# ── Chart generation ───────────────────────────────────────────────────────
GOLD_HEX   = '#C9A84C'
NAVY_HEX   = '#1B3A7A'
GREEN_HEX  = '#2D7D52'
RED_HEX    = '#B82020'
PURPLE_HEX = '#6248C0'
ORANGE_HEX = '#D4580A'
TEAL_HEX   = '#0E7FA8'

def chart_style(fig, ax):
    ax.set_facecolor('#FAFAFA')
    fig.patch.set_facecolor('#FAFAFA')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.tick_params(colors='#555555', labelsize=9)
    ax.grid(axis='y', color='#EEEEEE', linewidth=0.8)

def save(fig, name):
    path = os.path.join(CHARTS, name)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    return path

# Chart 1 — Corridor cost comparison
def chart_corridor_cost():
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    corridors = ['África do Sul→Moçambique','Dubai→Paquistão','Brasil→Portugal',
                 'Filipinas→Arábia','México→EUA','Média Global','FLUXUS (target)']
    costs = [14.0, 12.0, 7.2, 9.1, 5.8, 6.2, 1.2]
    colors = [RED_HEX,RED_HEX,ORANGE_HEX,ORANGE_HEX,ORANGE_HEX,'#888888',GREEN_HEX]
    bars = ax.barh(corridors, costs, color=colors, height=0.55, edgecolor='none')
    for bar, val in zip(bars, costs):
        ax.text(val+0.15, bar.get_y()+bar.get_height()/2, f'{val}%',
                va='center', fontsize=9.5, fontweight='bold', color='#333333')
    ax.axvline(6.2, color='#888888', linestyle='--', linewidth=1, alpha=0.7)
    ax.set_xlabel('Custo da Transação (%)', fontsize=9)
    ax.set_xlim(0, 17)
    ax.set_title('Custo Médio de Remessa por Corredor', fontsize=12, fontweight='bold', pad=10)
    chart_style(fig, ax)
    ax.grid(axis='x', color='#EEEEEE', linewidth=0.8)
    ax.grid(axis='y', visible=False)
    return save(fig, 'c1_corridors.png')

# Chart 2 — Market share pie
def chart_market_pie():
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    labels = ['Sul da Ásia','América Latina','África Subsaariana',
              'Ásia Oriental','Oriente Médio','Outros']
    sizes  = [28, 21, 18, 17, 10, 6]
    colors = [GOLD_HEX, NAVY_HEX, GREEN_HEX, PURPLE_HEX, TEAL_HEX, '#AAAAAA']
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, autopct='%1.0f%%', colors=colors,
        startangle=140, pctdistance=0.75,
        wedgeprops=dict(edgecolor='white', linewidth=2)
    )
    for t in texts: t.set_fontsize(9)
    for at in autotexts: at.set_fontsize(8.5); at.set_color('white'); at.set_fontweight('bold')
    ax.set_title('Distribuição do Mercado Global de Remessas\nUS$ 669 Bilhões', fontsize=11, fontweight='bold')
    fig.patch.set_facecolor('#FAFAFA')
    return save(fig, 'c2_market_pie.png')

# Chart 3 — Market growth line
def chart_market_growth():
    fig, ax = plt.subplots(figsize=(8.5, 4))
    years   = list(range(2018, 2031))
    actual  = [529, 554, 540, 605, 647, 669, None, None, None, None, None, None, None]
    proj    = [None,None,None,None,None,669,700,735,773,815,860,908,960]
    ax_y    = [v if v else np.nan for v in actual]
    pr_y    = [v if v else np.nan for v in proj]
    ax.plot(years, ax_y, color=NAVY_HEX, linewidth=2.5, marker='o', markersize=5, label='Realizado')
    ax.plot(years, pr_y, color=GOLD_HEX, linewidth=2.5, linestyle='--', marker='o', markersize=5, label='Projetado')
    ax.fill_between(years, [v if v else 0 for v in ax_y], alpha=0.12, color=NAVY_HEX)
    ax.fill_between(years, [v if v else 0 for v in pr_y], alpha=0.1, color=GOLD_HEX)
    ax.set_ylabel('US$ Bilhões', fontsize=9)
    ax.set_title('Crescimento do Mercado de Remessas 2018–2030', fontsize=11, fontweight='bold')
    ax.legend(fontsize=9)
    ax.set_xticks(years); ax.set_xticklabels([str(y) for y in years], rotation=35, fontsize=8)
    chart_style(fig, ax)
    return save(fig, 'c3_growth.png')

# Chart 4 — Radar competitor
def chart_radar():
    cats   = ['Custo\nBaixo','Velocidade','Cobertura','Transparência','Compliance','Resiliência']
    N      = len(cats)
    angles = [n/float(N)*2*math.pi for n in range(N)]
    angles += angles[:1]
    companies = {
        'FLUXUS':       ([9,9,7,10,8,9], GREEN_HEX),
        'Wise':         ([7,7,8,7,6,5], NAVY_HEX),
        'Remitly':      ([6,7,9,6,6,4], ORANGE_HEX),
        'Western Union':([3,4,10,2,7,6], RED_HEX),
        'Ripple/ODL':   ([8,8,5,7,5,6], PURPLE_HEX),
    }
    fig, ax = plt.subplots(figsize=(6.5, 5.5), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#FAFAFA')
    for name, (vals, color) in companies.items():
        v = vals + vals[:1]
        ax.plot(angles, v, color=color, linewidth=2, label=name)
        ax.fill(angles, v, alpha=0.06, color=color)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(cats, fontsize=9, fontweight='bold')
    ax.set_ylim(0, 10)
    ax.set_yticks([2,4,6,8,10]); ax.set_yticklabels(['','','','',''], fontsize=7)
    ax.grid(color='#DDDDDD')
    ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.12), fontsize=8.5)
    ax.set_title('Comparação Estratégica de Competidores', fontsize=11, fontweight='bold', pad=20)
    return save(fig, 'c4_radar.png')

# Chart 5 — Pre-funding capital
def chart_prefunding():
    fig, ax = plt.subplots(figsize=(8, 4))
    cos  = ['Western Union','MoneyGram','Wise','Remitly','Ripple/ODL','FLUXUS']
    vals = [8.5, 3.2, 2.1, 1.8, 0.9, 0.0]
    cols = [RED_HEX,RED_HEX,ORANGE_HEX,ORANGE_HEX,NAVY_HEX,GREEN_HEX]
    bars = ax.bar(cos, vals, color=cols, width=0.55, edgecolor='none')
    for bar, val in zip(bars, vals):
        lbl = f'US$ {val}B' if val>0 else 'ZERO'
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.1, lbl,
                ha='center', fontsize=9.5, fontweight='bold', color='#333333')
    ax.set_ylabel('US$ Bilhões', fontsize=9)
    ax.set_title('Capital Pré-Fundado Estimado por Empresa', fontsize=11, fontweight='bold')
    ax.set_ylim(0, 10.5)
    chart_style(fig, ax)
    ax.tick_params(axis='x', labelsize=9)
    return save(fig, 'c5_prefunding.png')

# Chart 6 — GTV projection dual axis
def chart_gtv():
    fig, ax1 = plt.subplots(figsize=(8.5, 4.2))
    years  = [2026, 2027, 2028, 2029, 2030]
    gtv    = [0.05, 0.5,  2.0,  8.0,  25.0]
    rev    = [0.00075, 0.005, 0.02, 0.072, 0.225]
    ax2    = ax1.twinx()
    ax1.bar(years, gtv, color=NAVY_HEX, alpha=0.75, width=0.45, label='GTV (US$ B)')
    ax2.plot(years, rev, color=GOLD_HEX, linewidth=2.5, marker='D', markersize=7, label='Receita (US$ B)')
    ax1.set_ylabel('GTV (US$ Bilhões)', fontsize=9, color=NAVY_HEX)
    ax2.set_ylabel('Receita (US$ Bilhões)', fontsize=9, color=GOLD_HEX)
    ax1.set_title('Projeção de GTV e Receita FLUXUS 2026–2030', fontsize=11, fontweight='bold')
    ax1.set_xticks(years)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1+lines2, labels1+labels2, fontsize=9, loc='upper left')
    chart_style(fig, ax1)
    ax2.spines['top'].set_visible(False)
    ax2.tick_params(colors='#555555', labelsize=9)
    return save(fig, 'c6_gtv.png')

# Chart 7 — DRE waterfall (grouped bars)
def chart_dre():
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    years   = ['2026','2027','2028','2029','2030']
    revenue = [0.75, 5, 20, 72, 225]
    opex    = [-0.9, -7, -17, -47, -112]
    ebitda  = [-0.15, -2, 3, 25, 113]
    x = np.arange(len(years))
    w = 0.28
    ax.bar(x-w, revenue, w, label='Receita', color=GREEN_HEX, edgecolor='none')
    ax.bar(x,   [abs(o) for o in opex], w, label='OpEx', color=RED_HEX, alpha=0.8, edgecolor='none')
    ax.bar(x+w, ebitda, w, label='EBITDA', color=GOLD_HEX, edgecolor='none')
    ax.axhline(0, color='#888888', linewidth=0.8)
    ax.set_xticks(x); ax.set_xticklabels(years)
    ax.set_ylabel('US$ Milhões', fontsize=9)
    ax.set_title('DRE Projetado FLUXUS 2026–2030 (US$ M)', fontsize=11, fontweight='bold')
    ax.legend(fontsize=9)
    chart_style(fig, ax)
    return save(fig, 'c7_dre.png')

# Chart 8 — Revenue donut
def chart_revenue_donut():
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    labels = ['Orchestration\nFee 45%','FX Spread\n25%','VASP Cards\n15%',
              'B2B Treasury\n10%','Data/SaaS\n5%']
    sizes  = [45, 25, 15, 10, 5]
    colors = [GOLD_HEX, NAVY_HEX, GREEN_HEX, TEAL_HEX, PURPLE_HEX]
    wedges, texts = ax.pie(
        sizes, labels=labels, colors=colors, startangle=90,
        wedgeprops=dict(width=0.55, edgecolor='white', linewidth=2.5)
    )
    for t in texts: t.set_fontsize(9); t.set_fontweight('bold')
    ax.text(0, 0, 'RECEITA\nMIX', ha='center', va='center',
            fontsize=11, fontweight='bold', color='#1A1A1A')
    ax.set_title('Distribuição de Fontes de Receita', fontsize=11, fontweight='bold')
    fig.patch.set_facecolor('#FAFAFA')
    return save(fig, 'c8_donut.png')

# Chart 9 — Cash flow stacked bar
def chart_cashflow():
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    years  = ['2026','2027','2028','2029','2030']
    op_cf  = [-0.2, -2.5, 4, 28, 120]
    inv_cf = [-0.5, -1.5, -3, -5, -8]
    x = np.arange(len(years))
    w = 0.45
    ax.bar(x, op_cf, w, label='CF Operacional', color=NAVY_HEX, edgecolor='none')
    ax.bar(x, inv_cf, w, bottom=op_cf, label='CF Investimento', color=RED_HEX, alpha=0.8, edgecolor='none')
    ax.axhline(0, color='#555555', linewidth=1)
    ax.set_xticks(x); ax.set_xticklabels(years)
    ax.set_ylabel('US$ Milhões', fontsize=9)
    ax.set_title('Projeção de Cash Flow 2026–2030', fontsize=11, fontweight='bold')
    ax.legend(fontsize=9)
    chart_style(fig, ax)
    return save(fig, 'c9_cashflow.png')

# Chart 10 — Unicorn milestone timeline
def chart_timeline():
    fig, ax = plt.subplots(figsize=(9, 4.5))
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#FAFAFA')
    milestones = [
        ('MVP Launch',      2026.75, GREEN_HEX),
        ('10K Users',       2026.92, GREEN_HEX),
        ('US$1M/mês',       2027.08, TEAL_HEX),
        ('Series A\nUS$10M',2027.42, NAVY_HEX),
        ('5 Corredores',    2027.92, NAVY_HEX),
        ('US$100M/mês',     2028.42, PURPLE_HEX),
        ('Series B\nUS$50M',2028.67, PURPLE_HEX),
        ('UNICÓRNIO\nUS$1B',2029.5,  GOLD_HEX),
    ]
    ax.axhline(0, color='#BBBBBB', linewidth=2, zorder=1)
    for i, (label, x, color) in enumerate(milestones):
        y = 0.4 if i % 2 == 0 else -0.4
        ax.plot(x, 0, 'o', color=color, markersize=14, zorder=3)
        ax.plot([x, x], [0, y*0.85], color=color, linewidth=1.5, zorder=2)
        ax.text(x, y, label, ha='center', va='bottom' if y>0 else 'top',
                fontsize=8.5, fontweight='bold', color='#222222',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor=color, linewidth=1.2))
    ax.set_xlim(2026.4, 2030.2)
    ax.set_ylim(-1.1, 1.1)
    ax.set_xticks([2026.75, 2027, 2027.5, 2028, 2028.5, 2029, 2029.5, 2030])
    ax.set_xticklabels(['Q3\'26','Q4\'26','2027','Q1\'28','Q3\'28','2029','Q2\'29','2030'], fontsize=9)
    ax.yaxis.set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.set_title('Roadmap para o Unicórnio — FLUXUS 2026–2030', fontsize=11, fontweight='bold', pad=12)
    return save(fig, 'c10_timeline.png')

print('Generating charts...')
C1 = chart_corridor_cost()
C2 = chart_market_pie()
C3 = chart_market_growth()
C4 = chart_radar()
C5 = chart_prefunding()
C6 = chart_gtv()
C7 = chart_dre()
C8 = chart_revenue_donut()
C9 = chart_cashflow()
C10= chart_timeline()
print('All charts done.')

# ── Drawing helpers ────────────────────────────────────────────────────────
def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))

def set_fill(c, color):
    try:
        r,g,b = color.red, color.green, color.blue
        c.setFillColorRGB(r,g,b)
    except Exception:
        c.setFillColor(color)

def set_stroke(c, color):
    try:
        r,g,b = color.red, color.green, color.blue
        c.setStrokeColorRGB(r,g,b)
    except Exception:
        c.setStrokeColor(color)

def wrap_text(c, text, x, y, max_width, font, size, color, leading=None, max_height=None):
    """Draw wrapped text, return final y."""
    if leading is None: leading = size * 1.45
    set_fill(c, color)
    c.setFont(font, size)
    words = text.split()
    line  = ''
    lines = []
    for w in words:
        test = line + (' ' if line else '') + w
        if c.stringWidth(test, font, size) <= max_width:
            line = test
        else:
            if line: lines.append(line)
            line = w
    if line: lines.append(line)
    cur_y = y
    for ln in lines:
        if max_height and (y - cur_y) > max_height: break
        c.drawString(x, cur_y, ln)
        cur_y -= leading
    return cur_y

def draw_page_frame(c, page_num, chap_num, chap_title=''):
    """Draw consistent frame: top bar, left sidebar, bottom footer."""
    acc = CHAPTER_COLORS.get(chap_num, GOLD)
    # Top full-width bar (thick)
    set_fill(c, acc)
    c.rect(0, H-10, W, 10, fill=1, stroke=0)
    # Left sidebar
    c.rect(0, 0, 6*mm, H, fill=1, stroke=0)
    # Light background for content area
    set_fill(c, HexColor('#FAFAF8'))
    c.rect(6*mm, MB+8*mm, W-6*mm, H-10-MB-8*mm, fill=1, stroke=0)
    # Footer line
    set_fill(c, HexColor('#DDDDDD'))
    c.rect(6*mm, MB+8*mm, W-6*mm, 0.5, fill=1, stroke=0)
    # Footer text
    set_fill(c, HexColor('#999999'))
    c.setFont('Helvetica', 7.5)
    c.drawString(6*mm+10, MB+2*mm, 'FLUXUS  ·  Investor Edition 2026  ·  Confidential')
    c.drawRightString(W-8, MB+2*mm, f'{page_num}')
    # Chapter label in sidebar (rotated)
    c.saveState()
    c.translate(4*mm, H/2)
    c.rotate(90)
    set_fill(c, WHITE)
    c.setFont('Helvetica-Bold', 7)
    short = f'CAP. {chap_num}' if chap_num else 'FLUXUS'
    c.drawCentredString(0, -2.5, short)
    c.restoreState()

def draw_header(c, chap_num, section_label, page_title, x=None, y=None):
    """Section label + page title in header area."""
    if x is None: x = 6*mm + 12
    if y is None: y = H - 10 - 16
    acc = CHAPTER_COLORS.get(chap_num, GOLD)
    # Section label
    set_fill(c, acc)
    c.setFont('Helvetica-Bold', 7.5)
    c.drawString(x, y, section_label.upper())
    # Page title
    set_fill(c, NEAR_BLK)
    c.setFont('Helvetica-Bold', 18)
    # Wrap if long
    words = page_title.split()
    line1, line2 = '', ''
    for w in words:
        test = line1 + (' ' if line1 else '') + w
        if c.stringWidth(test, 'Helvetica-Bold', 18) < CW+10:
            line1 = test
        else:
            line2 = (line2 + ' ' + w).strip()
    c.drawString(x, y-14, line1)
    if line2:
        c.drawString(x, y-30, line2)
        return y - 40
    return y - 26

def gold_block(c, x, y, w, h, text='', subtext='', accent=None):
    """Gold-colored stat/highlight block."""
    color = accent or GOLD
    set_fill(c, color)
    c.rect(x, y, w, h, fill=1, stroke=0)
    if text:
        set_fill(c, WHITE)
        c.setFont('Helvetica-Bold', 22)
        c.drawCentredString(x+w/2, y+h/2+4, text)
    if subtext:
        set_fill(c, WHITE)
        c.setFont('Helvetica', 8.5)
        c.drawCentredString(x+w/2, y+h/2-10, subtext)

def accent_block(c, x, y, w, h, color, text='', font_size=9, text_color=None):
    set_fill(c, color)
    c.rect(x, y, w, h, fill=1, stroke=0)
    if text:
        set_fill(c, text_color or WHITE)
        c.setFont('Helvetica', font_size)
        wrap_text(c, text, x+8, y+h-font_size-6, w-16, 'Helvetica', font_size, text_color or WHITE)

def stat_pill(c, x, y, w, number, label, color=None):
    color = color or GOLD
    set_fill(c, color)
    c.roundRect(x, y, w, 48, 5, fill=1, stroke=0)
    set_fill(c, WHITE)
    c.setFont('Helvetica-Bold', 22)
    c.drawCentredString(x+w/2, y+26, number)
    c.setFont('Helvetica', 7.5)
    c.drawCentredString(x+w/2, y+10, label)

def embed_chart(c, path, x, y, w, h):
    try:
        c.drawImage(path, x, y, width=w, height=h, preserveAspectRatio=True, mask='auto')
    except: pass

def divider_line(c, x, y, w, color=None):
    set_stroke(c, color or GOLD)
    c.setLineWidth(1.2)
    c.line(x, y, x+w, y)

# ── Page builders ──────────────────────────────────────────────────────────

def page_cover(c):
    c.saveState()
    try:
        # Full-page logo as background
        c.drawImage(LOGO, 0, 0, width=W, height=H, preserveAspectRatio=False, mask='auto')
    except: pass
    # Dark overlay top portion
    c.setFillColorRGB(0.05, 0.1, 0.16, alpha=0.55)
    c.rect(0, H-90, W, 90, fill=1, stroke=0)
    # Gold top bar
    set_fill(c, GOLD)
    c.rect(0, H-5, W, 5, fill=1, stroke=0)
    # Bottom band
    c.setFillColorRGB(0.05, 0.1, 0.16, alpha=0.82)
    c.rect(0, 0, W, 100, fill=1, stroke=0)
    # Bottom content
    set_fill(c, GOLD)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(ML, 72, '— ENCYCLOPÉDIA DO NEXUS FINANCEIRO SÍNCRONO')
    set_fill(c, WHITE)
    c.setFont('Helvetica-Bold', 28)
    c.drawString(ML, 46, 'INVESTOR EDITION  2026')
    set_fill(c, HexColor('#BBBBBB'))
    c.setFont('Helvetica', 9)
    c.drawString(ML, 28, 'CONFIDENCIAL  ·  EXCLUSIVO PARA INVESTIDORES AUTORIZADOS')
    # Gold bottom line
    set_fill(c, GOLD)
    c.rect(0, 0, W, 4, fill=1, stroke=0)
    c.restoreState()
    c.showPage()

def page_toc(c):
    set_fill(c, HexColor('#FAFAF8'))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # Left gold band
    set_fill(c, GOLD)
    c.rect(0, 0, 6*mm, H, fill=1, stroke=0)
    c.rect(0, H-10, W, 10, fill=1, stroke=0)
    # Big number background
    set_fill(c, HexColor('#F0EDE5'))
    c.setFont('Helvetica-Bold', 180)
    c.drawString(W-160, 20, '7')
    # Title
    set_fill(c, NEAR_BLK)
    c.setFont('Helvetica-Bold', 32)
    c.drawString(ML+6, H-52, 'CONTEÚDO')
    set_fill(c, GOLD)
    c.rect(ML+6, H-57, 100, 3, fill=1, stroke=0)
    c.setFont('Helvetica', 9)
    set_fill(c, HexColor('#888888'))
    c.drawString(ML+6, H-70, 'FLUXUS · Encyclopédia do Nexus Financeiro Síncrono · 2026')

    toc_items = [
        (1, 'Capítulo 1', 'A Crise Global da Remessa e o Peso do Legado',        '04'),
        (2, 'Capítulo 2', 'Anatomia dos Gigantes e a Falácia da Eficiência',      '12'),
        (3, 'Capítulo 3', 'A Tese FLUXUS — O Fim das Licenças Bancárias Pesadas', '20'),
        (4, 'Capítulo 4', 'A Engenharia da Transparência — Auditoria em Tempo Real','28'),
        (5, 'Capítulo 5', 'Contabilidade Estrutural e Engenharia Financeira',      '38'),
        (6, 'Capítulo 6', 'Regulação Global e Compliance — Software-as-Law',       '48'),
        (7, 'Capítulo 7', 'Escala, Verticais e o Caminho do Unicórnio',            '56'),
    ]
    y = H - 100
    for num, chap, title, pg in toc_items:
        acc = CHAPTER_COLORS[num]
        # Color chip
        set_fill(c, acc)
        c.rect(ML+6, y-2, 28, 24, fill=1, stroke=0)
        set_fill(c, WHITE)
        c.setFont('Helvetica-Bold', 8)
        c.drawCentredString(ML+6+14, y+7, chap.split()[0])
        c.drawCentredString(ML+6+14, y-0.5, chap.split()[1])
        # Title
        set_fill(c, NEAR_BLK)
        c.setFont('Helvetica-Bold', 12.5)
        c.drawString(ML+44, y+11, title[:60])
        # Dots + page
        set_fill(c, HexColor('#CCCCCC'))
        dot_x = ML+44 + c.stringWidth(title[:60], 'Helvetica-Bold', 12.5) + 8
        c.setFont('Helvetica', 9)
        dots = '.' * int((W-MR-dot_x-30) / c.stringWidth('.','Helvetica',9))
        c.drawString(dot_x, y+11, dots)
        set_fill(c, acc)
        c.setFont('Helvetica-Bold', 12.5)
        c.drawRightString(W-MR, y+11, pg)
        # Divider
        set_fill(c, HexColor('#EEEEEE'))
        c.rect(ML+6, y-10, W-ML-MR, 0.5, fill=1, stroke=0)
        y -= 88

    # Footer
    set_fill(c, HexColor('#999999'))
    c.setFont('Helvetica', 7.5)
    c.drawString(6*mm+10, MB+2*mm, 'FLUXUS  ·  Investor Edition 2026  ·  Confidential')
    c.drawRightString(W-8, MB+2*mm, '02')
    c.showPage()

def page_exec_summary(c):
    set_fill(c, HexColor('#FAFAF8'))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    draw_page_frame(c, 3, 0, '')
    # Dark header area
    set_fill(c, NEAR_BLK)
    c.rect(6*mm, H-10-88, W-6*mm, 88, fill=1, stroke=0)
    set_fill(c, GOLD)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(6*mm+14, H-30, 'EXECUTIVE SUMMARY')
    set_fill(c, WHITE)
    c.setFont('Helvetica-Bold', 30)
    c.drawString(6*mm+14, H-64, 'Por que o FLUXUS vence?')
    set_fill(c, HexColor('#AAAAAA'))
    c.setFont('Helvetica', 10)
    c.drawString(6*mm+14, H-82, 'O Nexus de Orquestração que nenhum gigante construiu ainda.')

    # 6 stat pills in 3x2 grid
    stats = [
        ('US$ 669B', 'Mercado Anual de Remessas', GOLD),
        ('6.2%',     'Taxa Média Global (Banco Mundial)', HexColor('#B82020')),
        ('<60s',     'Liquidação FLUXUS', HexColor('#2D7D52')),
        ('0',        'Capital Pré-Fundado Exigido', HexColor('#1B3A7A')),
        ('US$ 10T',  'Capital Aprisionado em Nostro/Vostro', HexColor('#6248C0')),
        ('US$ 1B+',  'Valuation Alvo (2030)', HexColor('#D4580A')),
    ]
    cols = 3; pill_w = (CW - 20) / cols
    y_start = H - 10 - 88 - 62
    for i, (num, label, col) in enumerate(stats):
        row, col_i = divmod(i, cols)
        px = 6*mm + 12 + col_i * (pill_w + 10)
        py = y_start - row * 58
        stat_pill(c, px, py, pill_w, num, label, col)

    # Bullet "why" section
    y = H - 10 - 88 - 62 - 130
    set_fill(c, NEAR_BLK)
    c.setFont('Helvetica-Bold', 14)
    c.drawString(6*mm+12, y, 'O que nos diferencia:')
    divider_line(c, 6*mm+12, y-6, 200)
    bullets = [
        'Zero capital institucional pré-fundado — liquidez Just-in-Time via investidores P2P locais',
        'Custo de transação < 1% vs. média de 6.2% do mercado (redução de 85%)',
        'Liquidação em < 60 segundos vs. T+2 a T+5 nos bancos tradicionais',
        'Shadow-Crypto: blockchain invisível ao usuário, auditável ao regulador',
        'Resiliência descentralizada: imune ao de-risking bancário global',
        'Modelo Asset-Light: margem EBITDA de 50%+ projetada para 2030',
    ]
    y -= 20
    for b in bullets:
        set_fill(c, GOLD)
        c.rect(6*mm+12, y+2, 4, 4, fill=1, stroke=0)
        set_fill(c, DARK_GRAY)
        c.setFont('Helvetica', 10)
        wrap_text(c, b, 6*mm+22, y+3, CW-20, 'Helvetica', 10, DARK_GRAY, leading=13)
        y -= 18

    # Quote box at bottom
    qy = MB + 8*mm + 12
    set_fill(c, NEAR_BLK)
    c.rect(6*mm+12, qy, CW-10, 52, fill=1, stroke=0)
    set_fill(c, GOLD)
    c.rect(6*mm+12, qy, 5, 52, fill=1, stroke=0)
    set_fill(c, WHITE)
    c.setFont('Helvetica-Oblique', 10)
    c.drawString(6*mm+25, qy+33, '"A era do capital aprisionado e dos intermediários opacos chegou ao fim.')
    c.drawString(6*mm+25, qy+18, 'A era da orquestração síncrona começou."')
    set_fill(c, GOLD)
    c.setFont('Helvetica-Bold', 8.5)
    c.drawString(6*mm+25, qy+5, '— FLUXUS Founding Team, 2026')
    c.showPage()

def page_chapter_divider(c, chap_num, title, subtitle, page_num):
    """Full-bleed chapter divider with large ghosted number."""
    # Background gradient simulation
    set_fill(c, HexColor('#0D1B2A'))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # Accent color left panel
    acc = CHAPTER_COLORS[chap_num]
    set_fill(c, acc)
    c.rect(0, 0, W*0.38, H, fill=1, stroke=0)
    # Large ghost chapter number
    set_fill(c, HexColor('#0F2235'))
    c.setFont('Helvetica-Bold', 300)
    c.drawString(W*0.3, -40, str(chap_num))
    # White divider line
    set_fill(c, WHITE)
    c.rect(W*0.38, 0, 3, H, fill=1, stroke=0)
    # Chapter label
    set_fill(c, WHITE)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(W*0.42, H-70, f'CAPÍTULO  {chap_num}')
    set_fill(c, acc)
    c.rect(W*0.42, H-76, 120, 3, fill=1, stroke=0)
    # Main title
    set_fill(c, WHITE)
    c.setFont('Helvetica-Bold', 26)
    # Word wrap title
    words = title.split()
    lines, line = [], ''
    for w in words:
        test = (line+' '+w).strip()
        if c.stringWidth(test,'Helvetica-Bold',26) < W*0.55:
            line = test
        else:
            lines.append(line); line = w
    if line: lines.append(line)
    ty = H-110
    for ln in lines:
        c.drawString(W*0.42, ty, ln); ty -= 34
    # Subtitle
    set_fill(c, HexColor('#AABBCC'))
    c.setFont('Helvetica', 11)
    c.drawString(W*0.42, ty-8, subtitle)
    # Page number in accent panel
    set_fill(c, WHITE)
    c.setFont('Helvetica-Bold', 72)
    c.drawCentredString(W*0.19, H/2-36, str(chap_num))
    set_fill(c, HexColor('#FFFFFF'))
    c.setFont('Helvetica', 9)
    c.drawCentredString(W*0.19, H/2-60, f'CAPÍTULO')
    # Bottom bar
    set_fill(c, WHITE)
    c.rect(0, 0, W, 4, fill=1, stroke=0)
    set_fill(c, HexColor('#888888'))
    c.setFont('Helvetica', 7)
    c.drawCentredString(W/2, 10, f'FLUXUS  ·  Investor Edition 2026  ·  {page_num}')
    c.showPage()

def content_page_standard(c, chap_num, page_title, section_label, body_paras,
                            page_num, chart_path=None, table_data=None,
                            stat_num=None, stat_label=None, quote=None):
    """
    Full-coverage content page with:
    - Header block (dark) with title
    - Two-column body text
    - Optional chart (right column or full-width)
    - Optional stat pill
    - Quote box or accent block at bottom
    """
    acc  = CHAPTER_COLORS.get(chap_num, GOLD)
    light= CHAPTER_LIGHT.get(chap_num, GOLD_PALE)

    # Background
    set_fill(c, HexColor('#FAFAF8'))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    draw_page_frame(c, page_num, chap_num)

    # Dark header block
    set_fill(c, NEAR_BLK)
    c.rect(6*mm, H-10-72, W-6*mm, 72, fill=1, stroke=0)
    set_fill(c, acc)
    c.setFont('Helvetica-Bold', 8)
    c.drawString(6*mm+12, H-26, section_label.upper())
    set_fill(c, WHITE)
    c.setFont('Helvetica-Bold', 20)
    # Clip title
    title_short = page_title[:65]
    c.drawString(6*mm+12, H-50, title_short)
    if len(page_title) > 65:
        c.setFont('Helvetica-Bold', 16)
        c.drawString(6*mm+12, H-68, page_title[65:120])

    # Accent top-right block
    set_fill(c, acc)
    c.rect(W-70, H-10-72, 70, 72, fill=1, stroke=0)
    set_fill(c, WHITE)
    c.setFont('Helvetica-Bold', 28)
    c.drawCentredString(W-35, H-52, str(chap_num))
    c.setFont('Helvetica', 7)
    c.drawCentredString(W-35, H-68, 'CAP.')

    content_top = H - 10 - 72 - 10
    content_bot = MB + 8*mm + 60  # leave room for bottom element
    content_h   = content_top - content_bot

    if chart_path and table_data is None:
        # LEFT: text column (55%), RIGHT: chart (45%)
        col1_w = CW * 0.52
        col2_w = CW * 0.44
        col1_x = 6*mm + 10
        col2_x = col1_x + col1_w + 12

        # Body text left column
        all_text = ' '.join(body_paras)
        ty = content_top - 4
        words = all_text.split()
        line = ''; lines = []
        c.setFont('Helvetica', 10)
        for w in words:
            test = (line+' '+w).strip()
            if c.stringWidth(test,'Helvetica',10) < col1_w - 4:
                line = test
            else:
                lines.append(line); line = w
        if line: lines.append(line)
        set_fill(c, DARK_GRAY)
        c.setFont('Helvetica', 10)
        for ln in lines:
            if ty < content_bot + 20: break
            c.drawString(col1_x, ty, ln)
            ty -= 15

        # Chart right column
        ch_h = min(content_h * 0.80, 220)
        ch_y = content_top - ch_h - 4
        embed_chart(c, chart_path, col2_x, ch_y, col2_w, ch_h)

    elif table_data:
        # Full-width table
        from reportlab.platypus import Table as RLTable, TableStyle as RLTableStyle
        headers, rows = table_data
        col_count = len(headers)
        col_w = (CW - 10) / col_count
        data = [headers] + rows
        tbl = RLTable(data, colWidths=[col_w]*col_count)
        tbl.setStyle(RLTableStyle([
            ('BACKGROUND',(0,0),(-1,0), acc),
            ('TEXTCOLOR',(0,0),(-1,0), white),
            ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
            ('FONTSIZE',(0,0),(-1,-1),9),
            ('FONTNAME',(0,1),(-1,-1),'Helvetica'),
            ('TEXTCOLOR',(0,1),(-1,-1),NEAR_BLK),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[white,HexColor('#F2F4FF')]),
            ('GRID',(0,0),(-1,-1),0.5,HexColor('#DDDDDD')),
            ('LINEBELOW',(0,0),(-1,0),2,acc),
            ('TOPPADDING',(0,0),(-1,-1),7),
            ('BOTTOMPADDING',(0,0),(-1,-1),7),
            ('LEFTPADDING',(0,0),(-1,-1),8),
            ('ALIGN',(0,0),(-1,-1),'LEFT'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ]))
        tw, th = tbl.wrapOn(c, CW-10, content_h*0.6)
        tbl.drawOn(c, 6*mm+10, content_top - th - 4)
        # Text below table
        ty = content_top - th - 18
        text = ' '.join(body_paras[:2]) if body_paras else ''
        words = text.split()
        line=''; lines=[]
        c.setFont('Helvetica', 10)
        for w in words:
            test = (line+' '+w).strip()
            if c.stringWidth(test,'Helvetica',10) < CW-20:
                line=test
            else:
                lines.append(line); line=w
        if line: lines.append(line)
        set_fill(c, DARK_GRAY)
        for ln in lines:
            if ty < content_bot+20: break
            c.drawString(6*mm+10, ty, ln); ty -= 15

    else:
        # Two-column text layout
        col_w = (CW - 20) / 2
        col1_x = 6*mm + 10
        col2_x = col1_x + col_w + 14

        all_text = ' '.join(body_paras)
        words = all_text.split()
        lines = []; line = ''
        c.setFont('Helvetica', 10.5)
        for w in words:
            test = (line+' '+w).strip()
            if c.stringWidth(test,'Helvetica',10.5) < col_w - 4:
                line = test
            else:
                lines.append(line); line = w
        if line: lines.append(line)

        max_lines_per_col = int(content_h / 15)
        set_fill(c, DARK_GRAY)
        c.setFont('Helvetica', 10.5)
        ty = content_top - 4
        for i, ln in enumerate(lines):
            if i < max_lines_per_col:
                c.drawString(col1_x, ty, ln); ty -= 15
            elif i == max_lines_per_col:
                ty = content_top - 4
                c.drawString(col2_x, ty, ln); ty -= 15
            else:
                c.drawString(col2_x, ty, ln); ty -= 15
                if ty < content_bot + 20: break

    # Bottom area — stat + quote OR accent block
    by = MB + 8*mm + 6
    if stat_num:
        stat_pill(c, 6*mm+10, by, 110, stat_num, stat_label or '', acc)
        # Quote alongside
        if quote:
            set_fill(c, light)
            c.rect(6*mm+130, by, CW-140, 48, fill=1, stroke=0)
            set_fill(c, acc)
            c.rect(6*mm+130, by, 4, 48, fill=1, stroke=0)
            set_fill(c, DARK_GRAY)
            c.setFont('Helvetica-Oblique', 9.5)
            wrap_text(c, f'"{quote}"', 6*mm+140, by+34, CW-155,
                      'Helvetica-Oblique', 9.5, DARK_GRAY, leading=14)
    elif quote:
        set_fill(c, NEAR_BLK)
        c.rect(6*mm+10, by, CW-10, 48, fill=1, stroke=0)
        set_fill(c, acc)
        c.rect(6*mm+10, by, 5, 48, fill=1, stroke=0)
        set_fill(c, WHITE)
        c.setFont('Helvetica-Oblique', 10)
        wrap_text(c, f'"{quote}"', 6*mm+22, by+34, CW-30,
                  'Helvetica-Oblique', 10, WHITE, leading=15)
    else:
        # Full-width accent block
        set_fill(c, light)
        c.rect(6*mm+10, by, CW-10, 48, fill=1, stroke=0)
        set_fill(c, acc)
        c.rect(6*mm+10, by, 5, 48, fill=1, stroke=0)
        if body_paras:
            last = body_paras[-1][:180]
            set_fill(c, DARK_GRAY)
            wrap_text(c, last, 6*mm+22, by+34, CW-30, 'Helvetica', 9.5, DARK_GRAY, leading=14)
    c.showPage()

# ── Extra data tables ───────────────────────────────────────────────────────
TABLE_SWIFT = (
    ['Feature', 'SWIFT / Banco Tradicional', 'FLUXUS'],
    [['Tipo de mensagem','MT103 Flat File','Smart Contract'],
     ['Liquidação','T+2 a T+5','Real-time (<60s)'],
     ['Intermediários','3–7 bancos','Zero'],
     ['Intervenção humana','Alta','Nenhuma'],
     ['Transparência','Opaca','Trilha completa blockchain'],
     ['Custo médio','6–15%','< 1%'],
     ['Capital pré-fundado','US$ Bilhões','Zero']]
)
TABLE_NOSTRO = (
    ['Modelo','Capital Exigido','Liquidação','Custo'],
    [['Banco Tradicional (Nostro/Vostro)','US$ Bilhões pré-fundados','T+2 a T+5','6–15%'],
     ['FLUXUS JIT P2P','Zero institutional','<60 segundos','0.5–2%']]
)
TABLE_COMPETITORS = (
    ['Empresa','Modelo','Pre-funding','Cobertura','Vuln. De-risking','Vantagem FLUXUS'],
    [['Wise','Netting Centralizado','Alto','80+ países','Alta','JIT descentralizado'],
     ['Remitly','Parceria Bancária','Muito Alto','170+ países','Muito Alta','Zero dependência'],
     ['Western Union','Rede de Agentes','Extremo','200+ países','Média','Digital-first'],
     ['Ripple/ODL','Ponte Cripto','Médio','40+ corredores','Baixa','Melhor UX'],
     ['FLUXUS','P2P Orchestration','ZERO','Expansível','Mínima','O Nexus']]
)
TABLE_DRE = (
    ['Ano','Volume (US$)','Receita','EBITDA Margin','Estágio'],
    [['2026','US$ 50M','US$ 750K','-120%','Seed'],
     ['2027','US$ 500M','US$ 5M','-40%','Series A'],
     ['2028','US$ 2B','US$ 20M','15%','Series B'],
     ['2029','US$ 8B','US$ 72M','35%','Series C'],
     ['2030','US$ 25B','US$ 225M','50%','Unicórnio+']]
)
TABLE_VASP = (
    ['Jurisdição','Tipo de Licença','Status','Timeline'],
    [['UAE (DFSA)','VASP / Payment Institution','Target','Q3 2026'],
     ['Brasil (BCB)','Instituição de Pagamento','Target','Q4 2026'],
     ['EU (EBA)','EMI License','Target','Q1 2027'],
     ['UK (FCA)','EMI / API','Target','Q2 2027'],
     ['USA (FinCEN)','MSB + State MTL','Target','Q4 2027']]
)

# ── Master build ────────────────────────────────────────────────────────────
CHAPTER_SUBTITLES = {
    1: 'Análise do mercado global de remessas e suas ineficiências estruturais',
    2: 'Como os maiores players falham e onde o FLUXUS se posiciona',
    3: 'O modelo de orquestração P2P e o fim do pre-funding institucional',
    4: 'Blockchain invisível, trilha de auditoria e transparência radical',
    5: 'DRE, balanço asset-light e projeções financeiras até 2030',
    6: 'Compliance como diferenciador estratégico — Software-as-Law',
    7: 'Verticais de crescimento, roadmap e o caminho para US$ 1 bilhão',
}

# Assign charts to specific pages (chapter_idx, page_idx within chapter)
# chapters[0] = Cap 1, chapters[0]['pages'][0] = page 1, etc.
CHART_MAP = {
    (0, 0): C1,   # Cap1 pg1
    (0, 1): C2,   # Cap1 pg2
    (0, 7): C3,   # Cap1 pg8
    (1, 5): C4,   # Cap2 pg14 (competitive comparison)
    (1, 6): C5,   # Cap2 pg15 (pre-funding)
    (2, 7): C6,   # Cap3 pg24 (GTV)
    (4, 0): C7,   # Cap5 pg35 (DRE)
    (4, 3): C8,   # Cap5 pg38/39 (donut revenue)
    (4, 9): C9,   # Cap5 pg44 (cashflow)
    (6, 6): C10,  # Cap7 pg59 (timeline)
}
TABLE_MAP = {
    (0, 1): TABLE_SWIFT,
    (0, 2): TABLE_NOSTRO,
    (1, 5): TABLE_COMPETITORS,
    (4, 0): TABLE_DRE,
    (5, 0): TABLE_VASP,
}
STAT_MAP = {
    (0,0): ('US$ 669B', 'Mercado Global / Ano'),
    (0,1): ('6,2%', 'Custo Médio Global'),
    (0,2): ('US$ 10T', 'Capital Aprisionado'),
    (0,4): ('De-risk', 'Bancos vs FLUXUS'),
    (1,2): ('0', 'Pre-funding FLUXUS'),
    (2,0): ('< 60s', 'Liquidação'),
    (3,0): ('Shadow', 'Crypto Layer'),
    (4,0): ('50%', 'EBITDA 2030'),
    (6,6): ('US$ 1B+', 'Valuation Alvo'),
}
QUOTE_MAP = {
    (0,0): 'O FLUXUS não reinventa a roda do dinheiro — reinventa os trilhos por onde ele corre.',
    (0,7): 'Com 0,1% do mercado global, o FLUXUS já processa US$ 600M+ anuais.',
    (1,5): 'Enquanto os gigantes correm sobre gelo fino, o FLUXUS constrói o leito do rio.',
    (2,7): 'O caminho matemático para o unicórnio não é um sonho — é a consequência natural da escala síncrona.',
    (4,3): 'Nosso lucro vem de orquestrar a eficiência, não de esconder taxas.',
    (6,6): 'O Unicórnio não é um objetivo — é o resultado inevitável de executarmos com precisão milimétrica.',
}

def build_pdf():
    c = rl_canvas.Canvas(OUT, pagesize=A4)
    c.setTitle('FLUXUS Annual Report 2026 — Investor Edition')
    c.setAuthor('FLUXUS Founding Team')

    # 1. Cover
    page_cover(c)
    # 2. TOC
    page_toc(c)
    # 3. Executive Summary
    page_exec_summary(c)

    page_num = 4
    for ci, chap in enumerate(chapters):
        chap_num = ci + 1
        # Chapter divider
        page_chapter_divider(c, chap_num, chap['title'],
                             CHAPTER_SUBTITLES.get(chap_num, ''),
                             page_num)
        page_num += 1

        for pi, page in enumerate(chap['pages']):
            chart  = CHART_MAP.get((ci, pi))
            tdata  = TABLE_MAP.get((ci, pi))
            snum, slabel = STAT_MAP.get((ci,pi), (None,None))
            quote  = QUOTE_MAP.get((ci,pi))
            section_label = f'Capítulo {chap_num}  ·  {chap["title"][:40]}'

            # If table + chart on same page, drop chart (table takes priority)
            if tdata and chart:
                chart = None

            content_page_standard(
                c,
                chap_num=chap_num,
                page_title=page['title'],
                section_label=section_label,
                body_paras=page['body'],
                page_num=page_num,
                chart_path=chart,
                table_data=tdata,
                stat_num=snum,
                stat_label=slabel,
                quote=quote,
            )
            page_num += 1

    c.save()
    print(f'\nPDF saved: {OUT}')
    print(f'Pages: ~{page_num}')

if __name__ == '__main__':
    build_pdf()
