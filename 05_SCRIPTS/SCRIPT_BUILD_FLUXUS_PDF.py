"""
FLUXUS Investor Edition PDF Generator
Elegant, dark-premium design with gold accents for investor presentation
"""
import math
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black

# ─── Brand Palette ────────────────────────────────────────────────────────────
NAVY       = HexColor('#0A1628')
NAVY_MID   = HexColor('#0F2040')
NAVY_LIGHT = HexColor('#1A3058')
GOLD       = HexColor('#C9A84C')
GOLD_LIGHT = HexColor('#E8C96A')
GOLD_PALE  = HexColor('#F5E8B8')
WHITE      = HexColor('#FFFFFF')
LIGHT_GRAY = HexColor('#E8EDF5')
MID_GRAY   = HexColor('#8A9BB5')
TEXT_BODY  = HexColor('#D4DCE8')
TEXT_DIM   = HexColor('#6A7D98')

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm

# ─── Page Background + Borders ───────────────────────────────────────────────
class PageDesigner:
    """Handles all canvas-level drawing for each page."""

    @staticmethod
    def draw(canvas_obj, doc):
        canvas_obj.saveState()
        w, h = PAGE_W, PAGE_H

        # Full-page background
        canvas_obj.setFillColor(NAVY)
        canvas_obj.rect(0, 0, w, h, fill=1, stroke=0)

        # Subtle mid-panel gradient effect (two rectangles)
        canvas_obj.setFillColor(NAVY_MID)
        canvas_obj.rect(0, h * 0.35, w, h * 0.3, fill=1, stroke=0)

        # Outer border – gold double rule
        canvas_obj.setStrokeColor(GOLD)
        canvas_obj.setLineWidth(1.5)
        canvas_obj.rect(10, 10, w - 20, h - 20, fill=0, stroke=1)
        canvas_obj.setLineWidth(0.4)
        canvas_obj.rect(14, 14, w - 28, h - 28, fill=0, stroke=1)

        # Corner ornaments
        PageDesigner._corner(canvas_obj, 10, 10, 1, 1)
        PageDesigner._corner(canvas_obj, w - 10, 10, -1, 1)
        PageDesigner._corner(canvas_obj, 10, h - 10, 1, -1)
        PageDesigner._corner(canvas_obj, w - 10, h - 10, -1, -1)

        # Top gold bar
        canvas_obj.setFillColor(GOLD)
        canvas_obj.rect(14, h - 14 - 3, w - 28, 3, fill=1, stroke=0)

        # Bottom gold bar
        canvas_obj.rect(14, 14, w - 28, 3, fill=1, stroke=0)

        # Watermark diagonal text
        canvas_obj.saveState()
        canvas_obj.setFillColor(HexColor('#0D1E38'))
        canvas_obj.setFont('Helvetica-Bold', 72)
        canvas_obj.translate(w / 2, h / 2)
        canvas_obj.rotate(35)
        canvas_obj.drawCentredString(0, 0, 'FLUXUS')
        canvas_obj.restoreState()

        # Footer
        canvas_obj.setFillColor(GOLD)
        canvas_obj.setFont('Helvetica', 7)
        footer = 'FLUXUS   |   Confidential – Investor Edition 2026'
        canvas_obj.drawCentredString(w / 2, 22, footer)

        # Page number
        page_num = canvas_obj.getPageNumber()
        canvas_obj.setFont('Helvetica-Bold', 8)
        canvas_obj.drawRightString(w - 22, 22, str(page_num))

        canvas_obj.restoreState()

    @staticmethod
    def _corner(c, x, y, sx, sy):
        """Draw a small L-shaped gold ornament at corner (x, y)."""
        size = 12
        c.setStrokeColor(GOLD)
        c.setLineWidth(2)
        c.line(x, y, x + sx * size, y)
        c.line(x, y, x, y + sy * size)


# ─── Custom Flowables ─────────────────────────────────────────────────────────
class GoldDivider(Flowable):
    """A decorative gold divider with a central dot."""
    def __init__(self, width=None):
        Flowable.__init__(self)
        self._width = width or (PAGE_W - 2 * MARGIN - 30)
        self.height = 8

    def draw(self):
        c = self.canv
        w = self._width
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.8)
        c.line(0, 4, w * 0.44, 4)
        c.line(w * 0.56, 4, w, 4)
        c.setFillColor(GOLD)
        c.circle(w / 2, 4, 3, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.circle(w / 2, 4, 1.5, fill=1, stroke=0)


class NetworkGraphic(Flowable):
    """Abstract network / hexagon graphic for the cover."""
    def __init__(self, width=160, height=140):
        Flowable.__init__(self)
        self.width  = width
        self.height = height

    def draw(self):
        c = self.canv
        cx, cy = self.width / 2, self.height / 2

        # Outer rings
        for r, alpha in [(65, 0.15), (50, 0.25), (35, 0.35)]:
            c.setStrokeColor(GOLD)
            c.setLineWidth(0.5)
            c.setFillAlpha(0)
            c.circle(cx, cy, r, fill=0, stroke=1)

        # Spokes + nodes
        nodes = []
        for i in range(6):
            angle = math.radians(i * 60 - 30)
            nx = cx + 50 * math.cos(angle)
            ny = cy + 50 * math.sin(angle)
            nodes.append((nx, ny))
            c.setStrokeColor(GOLD)
            c.setLineWidth(0.6)
            c.line(cx, cy, nx, ny)
            c.setFillColor(GOLD_LIGHT)
            c.circle(nx, ny, 4, fill=1, stroke=0)

        # Cross-connections
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.3)
        for i in range(len(nodes)):
            for j in range(i + 2, len(nodes)):
                if abs(i - j) != 3:
                    c.line(nodes[i][0], nodes[i][1], nodes[j][0], nodes[j][1])

        # Centre hub
        c.setFillColor(GOLD)
        c.circle(cx, cy, 8, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.circle(cx, cy, 4, fill=1, stroke=0)


class PullQuoteBox(Flowable):
    """A gold-bordered pull-quote box."""
    def __init__(self, text, width=None):
        Flowable.__init__(self)
        self._text = text
        self._width = width or (PAGE_W - 2 * MARGIN - 30)
        self.height = 48

    def draw(self):
        c = self.canv
        w = self._width
        # Background
        c.setFillColor(HexColor('#0F2A18') if False else HexColor('#12213A'))
        c.roundRect(0, 0, w, self.height, 4, fill=1, stroke=0)
        # Left accent bar
        c.setFillColor(GOLD)
        c.rect(0, 0, 4, self.height, fill=1, stroke=0)
        # Gold border
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.8)
        c.roundRect(0, 0, w, self.height, 4, fill=0, stroke=1)
        # Text
        c.setFillColor(GOLD_LIGHT)
        c.setFont('Helvetica-Oblique', 9)
        # Simple word-wrap
        words = self._text.split()
        lines, line = [], []
        for word in words:
            line.append(word)
            if c.stringWidth(' '.join(line), 'Helvetica-Oblique', 9) > w - 24:
                if len(line) > 1:
                    lines.append(' '.join(line[:-1]))
                    line = [word]
                else:
                    lines.append(' '.join(line))
                    line = []
        if line:
            lines.append(' '.join(line))
        y_start = self.height - 14
        for ln in lines[:4]:
            c.drawString(12, y_start, ln)
            y_start -= 11


# ─── Styles ───────────────────────────────────────────────────────────────────
def build_styles():
    s = {}

    s['cover_title'] = ParagraphStyle(
        'CoverTitle', fontName='Helvetica-Bold', fontSize=52,
        textColor=GOLD, alignment=TA_CENTER, leading=58,
        spaceAfter=4
    )
    s['cover_sub'] = ParagraphStyle(
        'CoverSub', fontName='Helvetica', fontSize=13,
        textColor=WHITE, alignment=TA_CENTER, leading=18,
        spaceAfter=6
    )
    s['cover_tag'] = ParagraphStyle(
        'CoverTag', fontName='Helvetica-Oblique', fontSize=11,
        textColor=GOLD_LIGHT, alignment=TA_CENTER, leading=14,
        spaceAfter=4
    )
    s['cover_edition'] = ParagraphStyle(
        'CoverEdition', fontName='Helvetica-Bold', fontSize=9,
        textColor=MID_GRAY, alignment=TA_CENTER, letterSpacing=3
    )
    s['chapter_label'] = ParagraphStyle(
        'ChapterLabel', fontName='Helvetica-Bold', fontSize=8,
        textColor=GOLD, alignment=TA_LEFT, leading=12,
        spaceAfter=2, letterSpacing=2
    )
    s['chapter_title'] = ParagraphStyle(
        'ChapterTitle', fontName='Helvetica-Bold', fontSize=22,
        textColor=WHITE, alignment=TA_LEFT, leading=26,
        spaceAfter=4, spaceBefore=8
    )
    s['section_title'] = ParagraphStyle(
        'SectionTitle', fontName='Helvetica-Bold', fontSize=14,
        textColor=GOLD_LIGHT, alignment=TA_LEFT, leading=18,
        spaceAfter=4, spaceBefore=10
    )
    s['subsection'] = ParagraphStyle(
        'SubSection', fontName='Helvetica-Bold', fontSize=11,
        textColor=GOLD, alignment=TA_LEFT, leading=14,
        spaceAfter=3, spaceBefore=6
    )
    s['body'] = ParagraphStyle(
        'Body', fontName='Helvetica', fontSize=9,
        textColor=TEXT_BODY, alignment=TA_JUSTIFY, leading=14,
        spaceAfter=6
    )
    s['bullet'] = ParagraphStyle(
        'Bullet', fontName='Helvetica', fontSize=9,
        textColor=TEXT_BODY, alignment=TA_LEFT, leading=13,
        spaceAfter=3, leftIndent=14, bulletIndent=4
    )
    s['table_header'] = ParagraphStyle(
        'TableHeader', fontName='Helvetica-Bold', fontSize=8,
        textColor=NAVY, alignment=TA_CENTER
    )
    s['table_cell'] = ParagraphStyle(
        'TableCell', fontName='Helvetica', fontSize=8,
        textColor=NAVY, alignment=TA_LEFT
    )
    s['exec_label'] = ParagraphStyle(
        'ExecLabel', fontName='Helvetica-Bold', fontSize=9,
        textColor=WHITE, alignment=TA_LEFT
    )
    s['exec_value'] = ParagraphStyle(
        'ExecValue', fontName='Helvetica-Bold', fontSize=9,
        textColor=GOLD, alignment=TA_RIGHT
    )
    s['footer_note'] = ParagraphStyle(
        'FooterNote', fontName='Helvetica-Oblique', fontSize=7.5,
        textColor=TEXT_DIM, alignment=TA_CENTER
    )

    return s


# ─── Table Helper ─────────────────────────────────────────────────────────────
def make_table(headers, rows, col_widths=None, style=None):
    """Build a dark-themed styled table."""
    avail = PAGE_W - 2 * MARGIN - 30
    if col_widths is None:
        n = len(headers)
        col_widths = [avail / n] * n

    data = [headers] + rows

    base_style = TableStyle([
        # Header row
        ('BACKGROUND',  (0, 0), (-1, 0),  GOLD),
        ('TEXTCOLOR',   (0, 0), (-1, 0),  NAVY),
        ('FONTNAME',    (0, 0), (-1, 0),  'Helvetica-Bold'),
        ('FONTSIZE',    (0, 0), (-1, 0),  8),
        ('ALIGN',       (0, 0), (-1, 0),  'CENTER'),
        ('VALIGN',      (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING',  (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        # Data rows alternating
        ('BACKGROUND',  (0, 1), (-1, -1), NAVY_LIGHT),
        ('TEXTCOLOR',   (0, 1), (-1, -1), TEXT_BODY),
        ('FONTNAME',    (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE',    (0, 1), (-1, -1), 8),
        # Grid
        ('GRID',        (0, 0), (-1, -1), 0.5, GOLD),
        ('LINEBELOW',   (0, 0), (-1, 0),  1.5, GOLD),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [NAVY_LIGHT, HexColor('#152844')]),
    ])
    if style:
        base_style.add(*style)

    t = Table(data, colWidths=col_widths)
    t.setStyle(base_style)
    return t


# ─── Content Builders ─────────────────────────────────────────────────────────
def cover_page(s):
    story = []
    story.append(Spacer(1, 28 * mm))
    story.append(Paragraph('FLUXUS', s['cover_title']))
    story.append(Spacer(1, 3 * mm))
    story.append(GoldDivider())
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph('Encyclopedia of the Synchronized Financial Nexus', s['cover_sub']))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph('"Orchestrating the Future of Global Remittance"', s['cover_tag']))
    story.append(Spacer(1, 10 * mm))
    story.append(NetworkGraphic(width=160, height=130))
    story.append(Spacer(1, 10 * mm))
    story.append(GoldDivider())
    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph('INVESTOR EDITION  ·  2026', s['cover_edition']))
    story.append(Spacer(1, 8 * mm))

    # Tagline strip
    tagline_data = [['P2P Orchestration'], ['Blockchain + AI'], ['Just-in-Time Liquidity']]
    tag_table = Table(
        [['P2P Orchestration  ·  Blockchain + AI  ·  Just-in-Time Liquidity']],
        colWidths=[PAGE_W - 2 * MARGIN - 30]
    )
    tag_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), NAVY_LIGHT),
        ('TEXTCOLOR',  (0, 0), (-1, -1), GOLD),
        ('FONTNAME',   (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE',   (0, 0), (-1, -1), 9),
        ('ALIGN',      (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BOX',        (0, 0), (-1, -1), 1.2, GOLD),
    ]))
    story.append(tag_table)
    story.append(PageBreak())
    return story


def exec_summary(s):
    story = []
    story.append(Paragraph('CAPÍTULO 0', s['chapter_label']))
    story.append(Paragraph('Executive Summary', s['chapter_title']))
    story.append(GoldDivider())
    story.append(Spacer(1, 4 * mm))

    # Key metrics table
    metrics = [
        ['Global Remittance Market', 'US$ 669 Billion / year'],
        ['Average Fee (World Bank)', '6.2% per transaction'],
        ['Capital Trapped in Nostro/Vostro', 'US$ 10 Trillion'],
        ['FLUXUS Target (0.1% of market)', 'US$ 600M+ annually'],
        ['Business Model', 'P2P Orchestration + VASP'],
        ['Core Technology', 'Blockchain + Smart Contracts + AI'],
        ['Key Innovation', 'Just-in-Time Liquidity (JIT)'],
        ['Pre-funding Required', 'Zero institutional pre-funding'],
        ['Settlement Speed', '<60 seconds'],
    ]

    exec_table = Table(
        [['METRIC', 'VALUE']] + metrics,
        colWidths=[240, 200]
    )
    exec_table.setStyle(TableStyle([
        ('BACKGROUND',  (0, 0), (-1, 0),  GOLD),
        ('TEXTCOLOR',   (0, 0), (-1, 0),  NAVY),
        ('FONTNAME',    (0, 0), (-1, 0),  'Helvetica-Bold'),
        ('FONTSIZE',    (0, 0), (-1, -1), 9),
        ('ALIGN',       (1, 1), (-1, -1), 'RIGHT'),
        ('FONTNAME',    (0, 1), (0, -1),  'Helvetica'),
        ('FONTNAME',    (1, 1), (1, -1),  'Helvetica-Bold'),
        ('TEXTCOLOR',   (0, 1), (0, -1),  TEXT_BODY),
        ('TEXTCOLOR',   (1, 1), (1, -1),  GOLD),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [NAVY_LIGHT, HexColor('#152844')]),
        ('GRID',        (0, 0), (-1, -1), 0.5, GOLD),
        ('LINEBELOW',   (0, 0), (-1, 0),  1.5, GOLD),
        ('TOPPADDING',  (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN',      (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(exec_table)
    story.append(Spacer(1, 6 * mm))

    story.append(PullQuoteBox(
        '"FLUXUS is not just another remittance company — we are the synchronized '
        'financial nexus. The orchestration layer that makes global capital flow '
        'as efficiently as information."  — FLUXUS Founding Team, 2026'
    ))
    story.append(PageBreak())
    return story


def chapter1(s):
    story = []
    story.append(Paragraph('CAPÍTULO 1', s['chapter_label']))
    story.append(Paragraph('A Crise Global da Remessa e o Peso do Legado', s['chapter_title']))
    story.append(GoldDivider())
    story.append(Spacer(1, 3 * mm))

    # Pg 1
    story.append(Paragraph('Página 1: A Gênese do Movimento de Valor', s['section_title']))
    story.append(Paragraph(
        'A história da civilização humana é uma tapeçaria tecida pelo movimento — não apenas de pessoas, '
        'mas do valor intrínseco gerado pelo seu trabalho. Desde as rotas de especiarias na Antiguidade '
        'até os modernos centros financeiros de Dubai e Nova York, a necessidade de transacionar valor '
        'através de fronteiras tem sido o combustível do progresso. O sistema de remessa global que '
        'herdamos hoje é uma estrutura de "confiança mediada" que parou no tempo.',
        s['body']
    ))
    story.append(Paragraph(
        'Em 2023, o volume total de remessas enviadas para países de renda baixa e média atingiu '
        'inacreditáveis <b>US$ 669 bilhões</b>. Contudo, essa gigantesca artéria financeira sofre '
        'de uma "trombose institucional". O modelo atual baseia-se em camadas sobre camadas de '
        'intermediários, cada um extraindo uma fração do valor sob a justificativa de "garantir a '
        'segurança". O que o mercado ainda não percebeu é que o verdadeiro lucro advém de '
        '<b>Orquestrar os Atores</b> para que performem de forma síncrona.',
        s['body']
    ))

    # KPI box
    kpi_rows = [
        ['Custo médio por US$ 200 enviado', '6,2%  (Banco Mundial)'],
        ['Corredores de alta fricção (ex.: Dubai-Africa)', 'Até 15% de custo'],
        ['Capital retirado dos mais necessitados / ano', 'US$ 40 bilhões'],
    ]
    kpi_t = make_table(['INDICADOR', 'VALOR'], kpi_rows, col_widths=[300, 155])
    story.append(kpi_t)
    story.append(Spacer(1, 4 * mm))

    # Pg 2 – SWIFT
    story.append(Paragraph('Página 2: O Império SWIFT e as Mensagens MT103', s['section_title']))
    story.append(Paragraph(
        'O SWIFT (<i>Society for Worldwide Interbank Financial Telecommunication</i>), criado em 1973, '
        'não é um sistema de transferência de dinheiro, mas um sistema de mensagens de alta segurança — '
        'o equivalente a um WhatsApp blindado para bancos. Quando um banco "envia" dinheiro via SWIFT, '
        'ele está apenas enviando um arquivo de texto estruturado chamado <b>MT103</b>. Se uma vírgula '
        'estiver fora do lugar, a transação para e um exército de "Back-Office" intervém manualmente — '
        'custo repassado integralmente ao remetente.',
        s['body']
    ))

    swift_rows = [
        ['Tipo de mensagem', 'MT103 Flat File', 'Smart Contract'],
        ['Liquidação', 'T+2 até T+5', 'Real-time (<60s)'],
        ['Intermediários', '3–7 bancos', 'Zero'],
        ['Intervenção humana', 'Alta', 'Nenhuma'],
        ['Transparência', 'Opaca', 'Trilha completa de auditoria'],
        ['Custo médio', '6–15%', '<1%'],
    ]
    story.append(make_table(['FEATURE', 'SWIFT', 'FLUXUS'], swift_rows, col_widths=[185, 140, 130]))
    story.append(Spacer(1, 3 * mm))

    # Pg 3 – Nostro/Vostro
    story.append(Paragraph('Página 3: Nostro, Vostro e o Capital Aprisionado', s['section_title']))
    story.append(Paragraph(
        'No coração da ineficiência bancária estão as contas <b>Nostro</b> e <b>Vostro</b>. '
        'Para que um banco brasileiro pague em dólares nos EUA, ele precisa ter dólares '
        '"pré-fundados" em uma conta Nostro no Chase ou Citibank. Estima-se que mais de '
        '<b>US$ 10 trilhões</b> em liquidez global estejam parados nessas contas — inativos, '
        'sem gerar investimentos produtivos, sofrendo com a desvalorização inflacionária.',
        s['body']
    ))

    nostro_rows = [
        ['Banco Tradicional (Nostro)', 'US$ Bilhões pré-fundados', 'T+2 a T+5', '6–15%'],
        ['FLUXUS JIT P2P', 'Zero institutional pre-funding', '<60 segundos', '0,5–2%'],
    ]
    story.append(make_table(
        ['MODELO', 'CAPITAL EXIGIDO', 'LIQUIDAÇÃO', 'CUSTO'],
        nostro_rows, col_widths=[155, 175, 80, 45]
    ))
    story.append(Spacer(1, 3 * mm))

    # Pg 4 – Custo social
    story.append(Paragraph('Página 4: O Custo Social e a Hemorragia da Pobreza', s['section_title']))
    story.append(Paragraph(
        'As remessas internacionais representam, muitas vezes, a única linha de vida para famílias '
        'no Paquistão, Índia, Filipinas, Brasil e Nigéria. O sistema bancário atual aplica o que o '
        'Banco Mundial chama de "Taxa de Pobreza": quanto menor o valor enviado, maior a taxa '
        'percentual cobrada. O compromisso do FLUXUS é com a <b>Transparência Radical</b> — '
        'o spread real é negociado em marketplace aberto. Lucramos orquestrando volume, não '
        'escondendo taxas.',
        s['body']
    ))
    story.append(Spacer(1, 3 * mm))

    # Pg 5 – Geopolítica
    story.append(Paragraph('Página 5: Geopolítica da Fricção e o De-risking Bancário', s['section_title']))
    story.append(Paragraph(
        'O <b>De-risking Bancário</b> — grandes bancos globais cancelando relações com '
        'bancos menores em mercados emergentes — cria "Desertos Financeiros" onde populações '
        'inteiras perdem acesso ao sistema financeiro. O FLUXUS introduz a <b>Resiliência '
        'Descentralizada</b>: não dependemos da permissão de nenhum gigante bancário global. '
        'Se um nó da rede falha por razões políticas, o FLUXUS encontra outro caminho '
        'síncrono através de nossa rede de investidores e VASPs.',
        s['body']
    ))
    story.append(Spacer(1, 3 * mm))

    # Pg 6–8 – Hawala + Market Size
    story.append(Paragraph('Páginas 6–8: Hawala Digital e o Mercado de US$ 669 Bilhões', s['section_title']))
    story.append(Paragraph(
        'O FLUXUS surge como a <b>Digitalização Institucional do Hawala</b> — pegamos a '
        'inteligência do "Netting" geográfico e a orquestramos através de Smart Contracts e '
        'Stablecoins, oferecendo a velocidade e o baixo custo do P2P informal com a segurança '
        'e a transparência de um banco de Wall Street.',
        s['body']
    ))

    scale_rows = [
        ['Conservador',  '0,1%', 'US$ 669M / ano',   'US$ 6,7M / ano'],
        ['Base Case',    '0,5%', 'US$ 3,35B / ano',  'US$ 33,5M / ano'],
        ['Otimista',     '2,0%', 'US$ 13,4B / ano',  'US$ 134M / ano'],
        ['Unicórnio',    '5,0%', 'US$ 33,45B / ano', 'US$ 334M / ano'],
    ]
    story.append(make_table(
        ['CENÁRIO', 'MARKET SHARE', 'VOLUME PROCESSADO', 'RECEITA (taxa 1%)'],
        scale_rows, col_widths=[100, 80, 140, 135]
    ))
    story.append(PageBreak())
    return story


def chapter2(s):
    story = []
    story.append(Paragraph('CAPÍTULO 2', s['chapter_label']))
    story.append(Paragraph('Anatomia dos Gigantes e a Falácia da Eficiência', s['chapter_title']))
    story.append(GoldDivider())
    story.append(Spacer(1, 3 * mm))

    story.append(Paragraph('Wise vs FLUXUS — Análise Competitiva', s['section_title']))
    story.append(Paragraph(
        'A Wise popularizou o <b>Netting Local</b>, mas possui um ponto cego estrutural: '
        'a dependência absoluta de centenas de contas bancárias comerciais ativas em '
        'quase todos os países onde opera. Se um banco local onde a Wise guarda reservas '
        'decidir encerrar a conta (de-risking), a operação naquele país para instantaneamente. '
        'O FLUXUS resolve isso com liquidez descentralizada Just-in-Time.',
        s['body']
    ))

    comp_rows = [
        ['Wise',            'Netting Centralizado', 'Alto',         '80+ países',     'Alta',    'Liquidez descentralizada JIT'],
        ['Remitly',         'Parceria Bancária',    'Muito Alto',   '170+ países',    'Muito Alta','Zero dependência bancária'],
        ['Western Union',   'Rede de Agentes',      'Extremo',      '200+ países',    'Média',   'Digital-first'],
        ['Ripple/ODL',      'Ponte Cripto',         'Médio',        '40+ corredores', 'Baixa',   'Melhor UX'],
        ['FLUXUS',          'P2P Orchestration',    'Zero',         'Expansível',     'Mínima',  'O Nexus'],
    ]
    story.append(make_table(
        ['EMPRESA', 'MODELO', 'PRÉ-FUNDING', 'COBERTURA', 'DE-RISK VULN.', 'VANTAGEM FLUXUS'],
        comp_rows,
        col_widths=[72, 80, 58, 72, 70, 103]
    ))
    story.append(PageBreak())
    return story


def chapter3(s):
    story = []
    story.append(Paragraph('CAPÍTULO 3', s['chapter_label']))
    story.append(Paragraph('Arquitetura do Nexus — Smart Contracts e Orquestração P2P', s['chapter_title']))
    story.append(GoldDivider())
    story.append(Spacer(1, 3 * mm))

    story.append(Paragraph('Visão Geral da Arquitetura Técnica', s['section_title']))

    arch_rows = [
        ['Orchestration Layer',  'AI + Smart Contracts',     'Roteamento de transações'],
        ['Liquidity Network',    'Pool de Investidores P2P', 'Funding Just-in-Time'],
        ['Settlement Rail',      'Blockchain + Rails Locais', 'Entrega final (PIX/UPI)'],
        ['Compliance Layer',     'AML/KYC Automatizado',     'Conformidade regulatória'],
        ['User Interface',       'App Mobile',               'UX para remetente/receptor'],
        ['VASP Integration',     'Parceiros licenciados',    'Emissão de cartão'],
    ]
    story.append(make_table(
        ['COMPONENTE', 'TECNOLOGIA', 'FUNÇÃO'],
        arch_rows, col_widths=[145, 160, 150]
    ))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph('Fluxo de Transação — 7 Passos Síncronos', s['section_title']))
    steps = [
        '<b>1. Sender</b> inicia a transferência via app FLUXUS',
        '<b>2. Smart Contract</b> trava os parâmetros da transação na blockchain',
        '<b>3. AI Engine</b> identifica a rota ótima de liquidez/investidor',
        '<b>4. Local Investor</b> provê liquidez na moeda de destino (JIT)',
        '<b>5. VASP</b> entrega ao receptor via PIX / UPI / cartão local',
        '<b>6. Blockchain</b> registra trilha imutável de auditoria (MiniHash)',
        '<b>7. Settlement</b> completo em menos de 60 segundos',
    ]
    for step in steps:
        story.append(Paragraph(step, s['bullet']))

    story.append(PageBreak())
    return story


def chapter4(s):
    story = []
    story.append(Paragraph('CAPÍTULO 4', s['chapter_label']))
    story.append(Paragraph('Engenharia da Transparência — Auditoria em Tempo Real', s['chapter_title']))
    story.append(GoldDivider())
    story.append(Spacer(1, 3 * mm))

    story.append(Paragraph('Shadow-Crypto: Blockchain Invisível ao Usuário', s['section_title']))
    story.append(Paragraph(
        'O modelo <b>Shadow-Crypto</b> mantém a blockchain e os smart contracts totalmente '
        'invisíveis para o usuário final, enquanto aproveita todo o seu poder para a '
        'liquidação. Cada transação gera um <b>MiniHash</b> de auditoria — tornando o '
        'FLUXUS aceitável para reguladores e bancos centrais sem sacrificar a experiência '
        'do usuário.',
        s['body']
    ))

    shadow_rows = [
        ['Intermediários', 'Opacos / Desconhecidos', 'Trilha blockchain completa'],
        ['Liquidação',     'T+2 a T+5',              'Real-time'],
        ['Reconciliação',  'Manual (humana)',         'Smart contracts automatizados'],
        ['Conformidade',   'Fricção regulatória',     'Compliance embutido'],
        ['Custo',          '6–15%',                   '<1%'],
    ]
    story.append(make_table(
        ['DIMENSÃO', 'SISTEMA TRADICIONAL', 'FLUXUS SHADOW-CRYPTO'],
        shadow_rows, col_widths=[130, 175, 150]
    ))
    story.append(PageBreak())
    return story


def chapter5(s):
    story = []
    story.append(Paragraph('CAPÍTULO 5', s['chapter_label']))
    story.append(Paragraph('Modelo de Receita e Projeções Financeiras', s['chapter_title']))
    story.append(GoldDivider())
    story.append(Spacer(1, 3 * mm))

    story.append(Paragraph('Fontes de Receita', s['section_title']))
    rev_rows = [
        ['Orchestration Fee',   '% de cada transação',              '0,3–0,8%'],
        ['Investor Spread Share','Parte do spread FX',              '0,1–0,3%'],
        ['VASP Card Fees',      'Emissão / manutenção de cartão',   'Taxa fixa'],
        ['B2B Treasury',        'Remessa corporativa',              '0,5–1,5%'],
        ['Data & Analytics',    'Inteligência da rede',             'SaaS'],
    ]
    story.append(make_table(
        ['FONTE DE RECEITA', 'DESCRIÇÃO', 'MARGEM'],
        rev_rows, col_widths=[150, 225, 80]
    ))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph('Projeções Financeiras — 5 Anos', s['section_title']))
    fin_rows = [
        ['2026', 'US$ 50M',   'US$ 750K',  '-120%', 'Seed'],
        ['2027', 'US$ 500M',  'US$ 5M',    '-40%',  'Series A'],
        ['2028', 'US$ 2B',    'US$ 20M',   '15%',   'Series B'],
        ['2029', 'US$ 8B',    'US$ 72M',   '35%',   'Series C'],
        ['2030', 'US$ 25B',   'US$ 225M',  '50%',   'Unicórnio+'],
    ]
    story.append(make_table(
        ['ANO', 'VOLUME (US$)', 'RECEITA', 'EBITDA MARGIN', 'ESTÁGIO'],
        fin_rows, col_widths=[45, 110, 90, 100, 110]
    ))
    story.append(PageBreak())
    return story


def chapter6(s):
    story = []
    story.append(Paragraph('CAPÍTULO 6', s['chapter_label']))
    story.append(Paragraph('Compliance, Regulação e Estratégia de Licenciamento', s['chapter_title']))
    story.append(GoldDivider())
    story.append(Spacer(1, 3 * mm))

    story.append(Paragraph('Roadmap Regulatório Global', s['section_title']))
    reg_rows = [
        ['UAE (DFSA)',    'VASP / Payment Institution', 'Target', 'Q3 2026'],
        ['Brasil (BCB)', 'Instituição de Pagamento',   'Target', 'Q4 2026'],
        ['EU (EBA)',     'EMI License',                'Target', 'Q1 2027'],
        ['UK (FCA)',     'EMI / API',                  'Target', 'Q2 2027'],
        ['USA (FinCEN)', 'MSB + State MTL',            'Target', 'Q4 2027'],
    ]
    story.append(make_table(
        ['JURISDIÇÃO', 'TIPO DE LICENÇA', 'STATUS', 'TIMELINE'],
        reg_rows, col_widths=[115, 185, 70, 85]
    ))
    story.append(PageBreak())
    return story


def chapter7(s):
    story = []
    story.append(Paragraph('CAPÍTULO 7', s['chapter_label']))
    story.append(Paragraph('Escala, Verticais e o Caminho do Unicórnio', s['chapter_title']))
    story.append(GoldDivider())
    story.append(Spacer(1, 3 * mm))

    story.append(Paragraph('Verticais de Crescimento', s['section_title']))
    vert_rows = [
        ['B2C Remittances',    'US$ 669B',  'Launch 2026',     'Transaction fee'],
        ['B2B SME Payments',   'US$ 2T',    'Expansion 2027',  'Volume spread'],
        ['Treasury Management','US$ 500B',  'Launch 2028',     'SaaS + spread'],
        ['Digital Asset Bridge','US$ 100B', 'Pilot 2027',      'Conversion fee'],
        ['Embedded Finance',   'Ilimitado', '2028+',           'API licensing'],
    ]
    story.append(make_table(
        ['VERTICAL', 'MERCADO', 'TIMELINE', 'MODELO DE RECEITA'],
        vert_rows, col_widths=[140, 80, 100, 135]
    ))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph('Unicorn Milestone Map', s['section_title']))
    mile_rows = [
        ['MVP Launch',              'Q3 2026', 'Primeira transação real'],
        ['10K Users',               'Q4 2026', 'Validação B2C'],
        ['US$ 1M Monthly Volume',   'Q1 2027', 'Prova de unit economics'],
        ['Series A',                'Q2 2027', 'Captação US$ 10M'],
        ['5 Corredores Ativos',     'Q4 2027', 'Expansão geográfica'],
        ['US$ 100M Monthly Volume', 'Q2 2028', 'Inflexão de escala'],
        ['Series B',                'Q3 2028', 'Captação US$ 50M'],
        ['Unicórnio (US$ 1B+)',     '2029–30', 'Valuation US$ 1B+'],
    ]
    story.append(make_table(
        ['MILESTONE', 'TARGET DATE', 'KPI'],
        mile_rows, col_widths=[195, 100, 160]
    ))
    story.append(Spacer(1, 5 * mm))

    story.append(PullQuoteBox(
        '"The age of trapped capital and opaque intermediaries is over. '
        'The age of synchronized orchestration has begun. '
        'FLUXUS is the Nexus through which the capital of the new millennium will flow." '
        '— FLUXUS Founding Team, 2026'
    ))
    story.append(PageBreak())
    return story


def back_cover(s):
    story = []
    story.append(Spacer(1, 40 * mm))
    story.append(Paragraph('FLUXUS', s['cover_title']))
    story.append(GoldDivider())
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph(
        '"FLUXUS is not just another remittance company. We are the synchronized financial '
        'nexus — the orchestration layer that makes global capital flow as efficiently as '
        'information. The age of trapped capital and opaque intermediaries is over. '
        'The age of synchronized orchestration has begun."',
        s['cover_tag']
    ))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph('— FLUXUS Founding Team, 2026', s['cover_edition']))
    story.append(Spacer(1, 12 * mm))
    story.append(GoldDivider())
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph('CONFIDENTIAL — FOR AUTHORIZED INVESTORS ONLY', s['cover_edition']))
    return story


# ─── Main ─────────────────────────────────────────────────────────────────────
def build_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN + 8,
        rightMargin=MARGIN + 8,
        topMargin=MARGIN + 14,
        bottomMargin=MARGIN + 14,
        title='FLUXUS — Investor Edition 2026',
        author='FLUXUS Founding Team',
        subject='Encyclopedia of the Synchronized Financial Nexus',
    )

    s = build_styles()
    story = []
    story += cover_page(s)
    story += exec_summary(s)
    story += chapter1(s)
    story += chapter2(s)
    story += chapter3(s)
    story += chapter4(s)
    story += chapter5(s)
    story += chapter6(s)
    story += chapter7(s)
    story += back_cover(s)

    doc.build(
        story,
        onFirstPage=PageDesigner.draw,
        onLaterPages=PageDesigner.draw,
    )
    print(f'PDF gerado com sucesso: {output_path}')


if __name__ == '__main__':
    from pathlib import Path

    repo_root = Path(__file__).resolve().parents[1]
    out = str(repo_root / "01_BOOKS" / "BOOK_FLUXUS_ENCYCLOPEDIA_INVESTOR_EDITION.pdf")
    build_pdf(out)
