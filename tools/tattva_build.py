"""Build a TATTVA SERIES PYQ Masterbook PDF from chapter files written in a small markup.

Usage: python3 tools/tattva_build.py books/indian-geography

The book folder holds book.txt (title lines) and chNN.txt chapter files.

Chapter markup (one directive per line, blank line = new paragraph):
  @chapter N | Title
  @unit UNIT I · NAME              starts a unit row on the contents page
  @intro ... @end                  opening paragraph; {pyqs}, {ones} are filled in
  @section N.M | Title
  @pyq EXAM TAG                     question box; lines up to @ans are the question
  @match ... @endmatch              List-I | List-II table inside a question
  @ans (c)                          answer line, closes the question body
  @note ...                         optional note under the answer (one paragraph)
  @end
  @one [EXAM TAG]                   one-liner box (no tag = tag not given in source)
  question text
  @ans answer
  @end
  @table ... @end                   pipe table, first row is the header
  @trap / @next / @pattern ... @end coloured boxes
  @up text                          "UP link:" paragraph
  @heatmap                          chapter heat map, computed from the chapter
Inline: **bold**, *italic*.
"""
import os
import re
import sys
from collections import OrderedDict

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Flowable, Frame, KeepTogether,
                                NextPageTemplate, PageBreak, PageTemplate, Paragraph, Spacer,
                                Table, TableStyle)

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
for name, f in [("Cal", "Caladea-Regular"), ("Cal-B", "Caladea-Bold"),
                ("Cal-I", "Caladea-Italic"), ("Cal-BI", "Caladea-BoldItalic")]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(FONTS, f + ".ttf")))
pdfmetrics.registerFontFamily("Cal", normal="Cal", bold="Cal-B", italic="Cal-I", boldItalic="Cal-BI")

# Brand colours (design-system/project/tokens.json)
GOLD_DEEP = colors.HexColor("#8b6914")
GOLD = colors.HexColor("#a68d5e")
NAVY = colors.HexColor("#1e3352")
INK = colors.HexColor("#1a1a1a")
MUTED = colors.HexColor("#5b6475")
HAIR = colors.HexColor("#d4c5a0")
ROW_ALT = colors.HexColor("#f6f3ea")
PYQ_BG, PYQ_BD = colors.HexColor("#fdf8ec"), colors.HexColor("#e6d5a8")
TRAP_BG, TRAP_BD = colors.HexColor("#fdeef0"), colors.HexColor("#e2a5ad")
NEXT_BG, NEXT_BD = colors.HexColor("#ecf1f8"), colors.HexColor("#a9bdd6")
PAT_BG, PAT_BD = colors.HexColor("#eef6ed"), colors.HexColor("#a8cfa5")
ANS_GREEN = colors.HexColor("#3d6b2a")
WATERMARK = colors.Color(0.65, 0.55, 0.37, alpha=0.10)

PAGE_W, PAGE_H = A4
MARGIN_X, MARGIN_TOP, MARGIN_BOTTOM, GUTTER = 42, 52, 46, 18
COL_W = (PAGE_W - 2 * MARGIN_X - GUTTER) / 2
FULL_W = PAGE_W - 2 * MARGIN_X

S = {}


def style(name, **kw):
    base = dict(fontName="Cal", fontSize=9.6, leading=13.2, textColor=INK)
    base.update(kw)
    S[name] = ParagraphStyle(name, **base)


style("body", alignment=TA_JUSTIFY, spaceAfter=6)
style("bodyL", alignment=TA_LEFT, spaceAfter=6)
style("chapno", fontName="Cal-B", fontSize=17, leading=22, textColor=GOLD_DEEP, spaceAfter=6)
style("chaptitle", fontName="Cal-B", fontSize=21, leading=25, textColor=GOLD_DEEP, spaceAfter=8)
style("section", fontName="Cal-B", fontSize=12.2, leading=15, textColor=GOLD_DEEP, spaceBefore=10, spaceAfter=5)
style("heat", fontName="Cal-B", fontSize=12.2, leading=15, textColor=GOLD_DEEP, spaceBefore=10, spaceAfter=5)
style("tag", fontName="Helvetica-Bold", fontSize=6.8, leading=9, textColor=MUTED, spaceAfter=2)
style("q", fontSize=9.2, leading=12.6)
style("opt", fontSize=9.2, leading=12.6, leftIndent=0)
style("ans", fontName="Cal-B", fontSize=9.2, leading=12.6, textColor=ANS_GREEN, spaceBefore=2)
style("note", fontSize=8.6, leading=11.6, spaceBefore=3)
style("boxlabel", fontName="Helvetica-Bold", fontSize=6.8, leading=9, textColor=MUTED, spaceAfter=2)
style("boxtext", fontSize=9.0, leading=12.4)
style("cell", fontSize=8.3, leading=10.6)
style("cellh", fontName="Cal-B", fontSize=8.3, leading=10.6, textColor=colors.white)
style("header", fontName="Cal-I", fontSize=7.6, leading=9, textColor=MUTED, alignment=TA_RIGHT)
style("center", alignment=TA_CENTER)


def inline(text):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", text)
    return text


def P(text, st="body"):
    return Paragraph(inline(text), S[st])


# ---------------------------------------------------------------- parsing
class Chapter:
    def __init__(self):
        self.no, self.title, self.unit = 0, "", None
        self.blocks = []            # (kind, data)
        self.sections = OrderedDict()   # "N.M title" -> list of item dicts
        self.items = []


YEAR = re.compile(r"\b(19[89]\d|20[0-2]\d)\b")


def years_of(tag):
    ys = [int(y) for y in YEAR.findall(tag or "")]
    # "2007, 2018" style lists are already caught; ranges are not used in tags
    return ys


def parse_chapter(path):
    ch = Chapter()
    lines = open(path, encoding="utf-8").read().splitlines()
    i, cur_sec = 0, None
    para = []

    def flush_para():
        if para:
            ch.blocks.append(("p", " ".join(para)))
            para.clear()

    def take_until_end(i):
        body = []
        while i < len(lines) and lines[i].strip() != "@end":
            body.append(lines[i])
            i += 1
        return body, i + 1

    while i < len(lines):
        raw = lines[i]
        line = raw.strip()
        if line.startswith("#"):          # comment
            i += 1
            continue
        if not line:
            flush_para()
            i += 1
            continue
        if not line.startswith("@"):
            para.append(line)
            i += 1
            continue
        flush_para()
        cmd, _, arg = line.partition(" ")
        arg = arg.strip()
        if cmd == "@chapter":
            no, _, title = arg.partition("|")
            ch.no, ch.title = int(no), title.strip()
            i += 1
        elif cmd == "@unit":
            ch.unit = arg
            i += 1
        elif cmd == "@intro":
            body, i = take_until_end(i + 1)
            ch.blocks.append(("intro", body))
        elif cmd == "@section":
            no, _, title = arg.partition("|")
            cur_sec = (no.strip(), title.strip())
            ch.sections[cur_sec] = []
            ch.blocks.append(("section", cur_sec))
            i += 1
        elif cmd in ("@pyq", "@one"):
            body, i = take_until_end(i + 1)
            item = parse_question(cmd[1:], arg, body)
            item["section"] = cur_sec
            if cur_sec is None:
                raise SystemExit(f"{path}: question before any @section")
            ch.sections[cur_sec].append(item)
            ch.items.append(item)
            ch.blocks.append(("q", item))
        elif cmd == "@table":
            body, i = take_until_end(i + 1)
            ch.blocks.append(("table", [r for r in body if r.strip()]))
        elif cmd in ("@trap", "@next", "@pattern"):
            body, i = take_until_end(i + 1)
            ch.blocks.append((cmd[1:], body))
        elif cmd == "@up":
            ch.blocks.append(("up", arg))
            i += 1
        elif cmd == "@heatmap":
            ch.blocks.append(("heatmap", None))
            i += 1
        else:
            raise SystemExit(f"{path}:{i + 1}: unknown directive {cmd}")
    flush_para()
    return ch


def parse_question(kind, tag, body):
    item = {"kind": kind, "tag": tag, "lines": [], "match": None, "ans": "", "note": ""}
    j = 0
    while j < len(body):
        line = body[j].strip()
        if line == "@match":
            rows = []
            j += 1
            while body[j].strip() != "@endmatch":
                if body[j].strip():
                    rows.append([c.strip() for c in body[j].split("|")])
                j += 1
            item["match"] = rows
            item["lines"].append("@MATCH")
        elif line.startswith("@ans"):
            item["ans"] = line[4:].strip()
        elif line.startswith("@note"):
            note = [line[5:].strip()]
            while j + 1 < len(body) and body[j + 1].strip() and not body[j + 1].strip().startswith("@"):
                j += 1
                note.append(body[j].strip())
            item["note"] = " ".join(note)
        elif line:
            item["lines"].append(line)
        j += 1
    item["years"] = years_of(tag)
    return item


# ---------------------------------------------------------------- flowables
def boxed(flowables, bg, bd, width=COL_W, pad=7):
    t = Table([[flowables]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.6, bd),
        ("LEFTPADDING", (0, 0), (-1, -1), pad), ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("TOPPADDING", (0, 0), (-1, -1), pad - 1), ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
    ]))
    t.spaceBefore, t.spaceAfter = 4, 8
    return t


def auto_widths(rows, width):
    """Give each column room for its longest word, then share the rest by text length."""
    from reportlab.pdfbase.pdfmetrics import stringWidth
    n = len(rows[0])
    minw, need = [], []
    for c in range(n):
        words = [w for r in rows for w in re.sub(r"\*\*", "", r[c]).split()] or [""]
        font = lambda k: "Cal-B" if k == 0 else "Cal"
        mw = max(stringWidth(w, "Cal-B", 8.3) for w in words) + 9
        full = max(stringWidth(re.sub(r"\*\*", "", r[c]), "Cal-B" if k == 0 else "Cal", 8.3)
                   for k, r in enumerate(rows)) + 9
        avg = sum(stringWidth(r[c], "Cal", 8.3) for r in rows) / len(rows) + 9
        minw.append(mw)
        need.append(max(mw, min(full, 0.6 * avg + 0.4 * full)))
    if sum(need) <= width:
        extra = width - sum(need)
        tot = sum(need)
        return [w + extra * w / tot for w in need]
    if sum(minw) >= width:
        tot = sum(minw)
        return [width * w / tot for w in minw]
    # shrink the flexible part proportionally
    flex = [nd - mn for nd, mn in zip(need, minw)]
    room = width - sum(minw)
    ftot = sum(flex) or 1
    return [mn + room * f / ftot for mn, f in zip(minw, flex)]


def data_table(rows, width=COL_W, header=True, small=False, col_widths=None, shade=None):
    rows = [r if isinstance(r, list) else [c.strip() for c in r.split("|")] for r in rows]
    n = max(len(r) for r in rows)
    rows = [r + [""] * (n - len(r)) for r in rows]
    if col_widths is None:
        col_widths = auto_widths(rows, width)
    st_h, st_c = S["cellh"], S["cell"]
    data = []
    for k, r in enumerate(rows):
        stl = st_h if (header and k == 0) else st_c
        data.append([Paragraph(inline(c), stl) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    cmds = [
        ("GRID", (0, 0), (-1, -1), 0.4, HAIR),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if header:
        cmds.append(("BACKGROUND", (0, 0), (-1, 0), GOLD_DEEP))
    start = 1 if header else 0
    for k in range(start, len(rows)):
        if (k - start) % 2 == 1:
            cmds.append(("BACKGROUND", (0, k), (-1, k), ROW_ALT))
    if shade:
        cmds += shade
    t.setStyle(TableStyle(cmds))
    t.spaceBefore, t.spaceAfter = 4, 9
    return t


def tag_text(item):
    if item["tag"]:
        return item["tag"].upper()
    return "UPPSC (EXAM TAG NOT GIVEN IN SOURCE)"


def question_box(item):
    inner = [Paragraph(inline(tag_text(item)), S["tag"])]
    first = True
    for line in item["lines"]:
        if line == "@MATCH":
            inner.append(data_table(item["match"], width=COL_W - 16))
            continue
        if first:
            inner.append(Paragraph("<b>Q.</b> " + inline(line), S["q"]))
            first = False
        else:
            inner.append(Paragraph(inline(line), S["opt"]))
    if item["kind"] == "one":
        inner.append(Paragraph("<b>Ans.</b> " + inline(item["ans"]), S["q"]))
    else:
        inner.append(Paragraph("Ans. " + inline(item["ans"]), S["ans"]))
    if item["note"]:
        inner.append(Paragraph(inline("Note: " + item["note"]), S["note"]))
    return boxed(inner, PYQ_BG, PYQ_BD)


def label_box(label, body, bg, bd, width=COL_W):
    paras, cur = [], []
    for l in body + [""]:
        if l.strip():
            cur.append(l.strip())
        elif cur:
            paras.append(" ".join(cur))
            cur = []
    inner = [Paragraph(label, S["boxlabel"])] + [Paragraph(inline(p), S["boxtext"]) for p in paras]
    return boxed(inner, bg, bd, width=width)


# ---------------------------------------------------------------- statistics
def decade(y):
    return f"{y // 10 * 10}s"


def trend(items):
    ys = sorted({y for it in items for y in it["years"]})
    n = len(items)
    if not ys:
        return "Tag not given", "-"
    span = f"{ys[0]}" if ys[0] == ys[-1] else f"{ys[0]}-{ys[-1]}"
    recent = ys[-1] >= 2021
    if n >= 4:
        t = f"Recurring, recent ({ys[-1]})" if recent else "Recurring"
    elif n >= 2:
        t = f"Recent ({ys[-1]})" if recent else ("Steady" if ys[-1] >= 2010 else "Low recent frequency")
    else:
        t = f"Recent ({ys[-1]})" if recent else "Occasional"
    return t, span


def chapter_stats(ch):
    pyqs = sum(1 for it in ch.items if it["kind"] == "pyq")
    ones = sum(1 for it in ch.items if it["kind"] == "one")
    dec = {d: 0 for d in ("1990s", "2000s", "2010s", "2020s")}
    for it in ch.items:
        for d in {decade(y) for y in it["years"]}:
            if d in dec:
                dec[d] += 1
    return pyqs, ones, dec


def heatmap_flowables(ch):
    rows = [["Topic", "PYQs", "Years", "Trend"]]
    secs = [(t, items) for (n, t), items in ch.sections.items() if items]
    secs.sort(key=lambda s: -len(s[1]))
    for title, items in secs:
        tr, span = trend(items)
        rows.append([title, str(len(items)), span, tr])
    w = COL_W
    t = data_table(rows, width=w, col_widths=[w * 0.44, w * 0.11, w * 0.2, w * 0.25])
    return [CondPageBreak(120), Paragraph(f"Chapter {ch.no}: Topic Heat Map", S["heat"]), t]


# ---------------------------------------------------------------- page decoration
class Marker(Flowable):
    """Zero-size flowable that records the page a chapter starts on."""

    def __init__(self, key, registry):
        super().__init__()
        self.key, self.registry = key, registry
        self.width = self.height = 0

    def draw(self):
        self.registry[self.key] = self.canv.getPageNumber()


def draw_watermark(c):
    c.saveState()
    c.setFillColor(WATERMARK)
    c.setFont("Cal-B", 64)
    c.translate(PAGE_W / 2, PAGE_H / 2)
    c.rotate(52)
    c.drawCentredString(0, -20, "QUANTUM IAS & PCS")
    c.restoreState()


def make_doc(path, book):
    doc = BaseDocTemplate(path, pagesize=A4, leftMargin=MARGIN_X, rightMargin=MARGIN_X,
                          topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOTTOM,
                          title=f"TATTVA SERIES · UPPSC Prelims PYQ Masterbook: {book['title']}",
                          author="Quantum IAS & PCS")
    body_h = PAGE_H - MARGIN_TOP - MARGIN_BOTTOM
    left = Frame(MARGIN_X, MARGIN_BOTTOM, COL_W, body_h, id="L", leftPadding=0, rightPadding=0,
                 topPadding=0, bottomPadding=0)
    right = Frame(MARGIN_X + COL_W + GUTTER, MARGIN_BOTTOM, COL_W, body_h, id="R", leftPadding=0,
                  rightPadding=0, topPadding=0, bottomPadding=0)
    full = Frame(MARGIN_X, MARGIN_BOTTOM, FULL_W, body_h, id="F", leftPadding=0, rightPadding=0,
                 topPadding=0, bottomPadding=0)
    header = f"Quantum IAS &amp; PCS · TATTVA SERIES · UPPSC Prelims PYQ Masterbook: {book['title']}"

    def content_page(c, d):
        draw_watermark(c)
        c.saveState()
        hp = Paragraph(header, S["header"])
        hp.wrapOn(c, FULL_W, 20)
        hp.drawOn(c, MARGIN_X, PAGE_H - 34)
        c.setStrokeColor(HAIR)
        c.setLineWidth(0.5)
        c.line(MARGIN_X, PAGE_H - 40, PAGE_W - MARGIN_X, PAGE_H - 40)
        c.setFont("Cal", 8)
        c.setFillColor(MUTED)
        c.drawCentredString(PAGE_W / 2, 24, str(c.getPageNumber()))
        c.restoreState()

    def cover_page(c, d):
        c.saveState()
        c.setStrokeColor(HAIR)
        c.setLineWidth(0.6)
        c.rect(34, 34, PAGE_W - 68, PAGE_H - 68)
        c.setStrokeColor(GOLD_DEEP)
        c.setLineWidth(2.2)
        c.line(140, PAGE_H - 34, PAGE_W - 140, PAGE_H - 34)
        c.line(140, 34, PAGE_W - 140, 34)
        c.restoreState()

    def plain_page(c, d):
        draw_watermark(c)

    def copyright_frame_page(c, d):
        c.saveState()
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.6)
        c.line(CP_X, 71, PAGE_W - CP_X, 71)
        c.setFillColor(CP_NAVY)
        c.setFont("Cal-B", 7)
        c.drawString(CP_X, 57, "© QUANTUM IAS & PCS", charSpace=1.1)
        c.setFillColor(GOLD_DEEP)
        c.setFont("Cal", 7)
        right = f"TATTVA SERIES · {book['title'].upper()}"
        c.drawRightString(PAGE_W - CP_X, 57, right, charSpace=1.1)
        c.restoreState()

    def contents_page(c, d):
        draw_watermark(c)
        c.saveState()
        c.setFont("Cal", 7.5)
        c.setFillColor(colors.HexColor("#666666"))
        c.drawCentredString(PAGE_W / 2, 28, str(c.getPageNumber()))
        c.restoreState()

    doc.addPageTemplates([
        PageTemplate("cover", [full], onPage=cover_page),
        PageTemplate("plain", [full], onPage=plain_page),
        PageTemplate("copyright", [Frame(CP_X, 90, CP_W, PAGE_H - 90 - 58, id="C", leftPadding=0,
                                         rightPadding=0, topPadding=0, bottomPadding=0)],
                     onPage=copyright_frame_page),
        PageTemplate("contents", [Frame(CT_X, MARGIN_BOTTOM, CT_W, PAGE_H - 52 - MARGIN_BOTTOM, id="T",
                                        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)],
                     onPage=contents_page),
        PageTemplate("full", [full], onPage=content_page),
        PageTemplate("cols", [left, right], onPage=content_page),
    ])
    return doc


# ---------------------------------------------------------------- front matter
def spaced(text):
    return " ".join(text)


def cover(book, chapters, tot_pyq, tot_one, y0, y1):
    def st(**kw):
        base = dict(fontName="Cal", alignment=TA_CENTER, textColor=INK)
        base.update(kw)
        return ParagraphStyle("c", **base)
    n = len(chapters)
    out = [Spacer(1, 150),
           Paragraph(spaced("QUANTUM") + "&nbsp;&nbsp;&nbsp;" + spaced("IAS") + "&nbsp;&nbsp;&nbsp;"
                     + "&amp; &nbsp;" + spaced("PCS"),
                     st(fontName="Helvetica-Bold", fontSize=10, leading=14, textColor=GOLD_DEEP)),
           Spacer(1, 22),
           Paragraph(spaced("TATTVA") + "&nbsp;&nbsp;&nbsp;" + spaced("SERIES"),
                     st(fontName="Cal-B", fontSize=12.5, leading=16, textColor=NAVY)),
           Spacer(1, 4),
           Paragraph("U P P S C &nbsp; P R E L I M S &nbsp;&nbsp; | &nbsp;&nbsp; P Y Q &nbsp; M A S T E R B O O K",
                     st(fontName="Helvetica", fontSize=7.5, leading=10, textColor=MUTED)),
           Spacer(1, 42),
           Paragraph(book["title"], st(fontName="Cal-I", fontSize=34, leading=40)),
           Spacer(1, 6),
           Paragraph(f"Complete Edition · Chapters 1 to {n}", st(fontName="Cal-I", fontSize=12, leading=16)),
           Spacer(1, 10),
           Paragraph("Previous Year Questions | Topic-wise Analysis | Conceptual Linkages | Exam-Oriented Revision",
                     st(fontName="Cal-I", fontSize=8.5, leading=11)),
           Spacer(1, 22),
           Table([[""]], colWidths=[220], style=[("LINEABOVE", (0, 0), (-1, -1), 2.2, GOLD_DEEP)]),
           Spacer(1, 10),
           Paragraph(f"{tot_pyq} Original UPPSC PYQs + {tot_one} One-liners · {y0} to {y1}",
                     st(fontSize=8.5, leading=12)),
           Paragraph("Concept Clusters · PYQ Patterns · Trap Alerts · Heat Maps", st(fontSize=8.5, leading=12)),
           Spacer(1, 24),
           Paragraph("P R E P A R E D &nbsp; F O R &nbsp; U P P S C &nbsp; P R E L I M S &nbsp; 2 0 2 6",
                     st(fontName="Helvetica", fontSize=6.8, leading=9, textColor=GOLD_DEEP)),
           Spacer(1, 30),
           Paragraph("© Quantum IAS &amp; PCS. All rights reserved.", st(fontSize=7, leading=9, textColor=MUTED)),
           ]
    return out


class Tracked(Flowable):
    """One line of letter-spaced text (Paragraph cannot track characters)."""

    def __init__(self, text, font, size, color, space=0.0, after=0.0):
        super().__init__()
        self.text, self.font, self.size, self.color, self.space, self.after = text, font, size, color, space, after

    def wrap(self, aw, ah):
        return aw, self.size * 1.2 + self.after

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.setFont(self.font, self.size)
        self.canv.drawString(0, self.after + self.size * 0.25, self.text, charSpace=self.space)


class Rule(Flowable):
    def __init__(self, width, thickness, color, before=0, after=0):
        super().__init__()
        self.w, self.t, self.color, self.before, self.after = width, thickness, color, before, after

    def wrap(self, aw, ah):
        return self.w, self.before + self.t + self.after

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.t)
        y = self.after + self.t / 2
        self.canv.line(0, y, self.w, y)


CP_X, CP_W = 51, PAGE_W - 102          # copyright page text block
CT_X, CT_W = 45, PAGE_W - 90           # contents page text block
CP_NAVY, CP_BLUE, CP_LINK = colors.HexColor("#1f2a3c"), colors.HexColor("#2f4f7f"), colors.HexColor("#1f4e8c")
CP_GREY, CP_LABEL, CP_RED = colors.HexColor("#555555"), colors.HexColor("#6b85a8"), colors.HexColor("#8b1a1a")
CP_PINK, CT_UNIT, CT_SEP = colors.HexColor("#fdecec"), colors.HexColor("#f6f0e2"), colors.HexColor("#e6dfcf")


def copyright_page(book, y0, y1):
    blue = ParagraphStyle("cpb", fontName="Cal", fontSize=8.6, leading=12.6, textColor=CP_BLUE)
    grey = ParagraphStyle("cpg", fontName="Cal", fontSize=8.4, leading=12.2, textColor=CP_GREY, alignment=TA_JUSTIFY)
    red = ParagraphStyle("cpr", fontName="Cal-B", fontSize=8.6, leading=12.4, textColor=CP_RED)
    head = lambda t: Tracked(t, "Cal-B", 10.5, CP_NAVY, 1.3, after=6)
    warn = Table([["", Paragraph("This material is intended solely for personal and educational use. Unauthorized "
                                 "reproduction or redistribution, including uploading on other Telegram channels, "
                                 "websites, social-media platforms, or paid groups, is strictly prohibited.", red)]],
                 colWidths=[3, CP_W - 3])
    warn.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, 0), CP_RED), ("BACKGROUND", (1, 0), (1, 0), CP_PINK),
                              ("LEFTPADDING", (0, 0), (0, 0), 0), ("RIGHTPADDING", (0, 0), (0, 0), 0),
                              ("LEFTPADDING", (1, 0), (1, 0), 10), ("RIGHTPADDING", (1, 0), (1, 0), 10),
                              ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 10)]))
    out = [Tracked("TATTVA SERIES", "Cal-B", 17, CP_NAVY, 2.2, after=6),
           Tracked("UPPSC PRELIMS | PYQ MASTERBOOK", "Cal-B", 8.5, GOLD_DEEP, 1.4, after=3),
           Paragraph("<i>Previous Year Questions | Topic-wise Analysis | Conceptual Linkages | Exam-Oriented "
                     "Revision</i>", ParagraphStyle("cpt", fontName="Cal-I", fontSize=9, leading=12,
                                                    textColor=colors.HexColor("#444444"))),
           Rule(CP_W, 2, colors.black, before=6, after=20),
           Paragraph("© 2026 Quantum IAS &amp; PCS. All Rights Reserved.",
                     ParagraphStyle("cpc", fontName="Cal-B", fontSize=9.5, leading=13, textColor=colors.black)),
           Spacer(1, 6),
           Paragraph("This publication is an original educational resource prepared by Quantum IAS &amp; PCS for the "
                     "academic and examination-preparation purposes of aspirants.", blue),
           Spacer(1, 8),
           Paragraph("No part of this publication may be reproduced, copied, modified, distributed, uploaded, or "
                     "commercially exploited, in whole or in part, without prior written permission from "
                     "Quantum IAS &amp; PCS.", blue),
           Spacer(1, 22), warn, Spacer(1, 22),
           head("DISCLAIMER"), Spacer(1, 6),
           Paragraph("Every effort has been made to ensure the accuracy and relevance of the information presented "
                     "in this book. However, factual information, government data, statistics, rankings, schemes, "
                     "and other dynamic information may change over time. Readers are advised to refer to official "
                     "sources wherever necessary. Facts in this edition are updated to 30 September 2026.", grey),
           Spacer(1, 8),
           Paragraph(f"All questions in this book are original previous-year questions from UPPSC and other Uttar "
                     f"Pradesh state-level examinations held between {y0} and {y1}, cited with their paper and year. "
                     "Where an answer key is marked (*), is disputed, or has been overtaken by later changes in law "
                     "or fact, the original key is retained and a Note explains the position at the time of the "
                     "examination and today.", grey),
           Spacer(1, 8),
           Paragraph("This publication is not affiliated with, endorsed by, or sponsored by UPPSC, UPSC, or any "
                     "government institution.", grey),
           Spacer(1, 16), head("FOR ACADEMIC USE"), Spacer(1, 6)]
    val = ParagraphStyle("cpv", fontName="Cal-B", fontSize=8.6, leading=11, textColor=CP_LINK)
    rows = [["PUBLISHED BY", "Quantum IAS & PCS"], ["SERIES", "Tattva Series"],
            ["TITLE", f"UPPSC Prelims PYQ Masterbook: {book['title']}"], ["EDITION", "1st Edition | 2026"],
            ["YEAR OF PUBLICATION", "2026"], ["CONNECT", "YouTube @QuantumPCSAcademy"]]
    t = Table([[Tracked(a, "Cal", 7.5, CP_LABEL, 0.96), Paragraph(inline(b), val)] for a, b in rows],
              colWidths=[142, CP_W - 142], rowHeights=19.3)
    t.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 0), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    out.append(t)
    return out


def contents(book, chapters, pages):
    out = [Paragraph("TATTVA SERIES&nbsp;&nbsp;·&nbsp;&nbsp;UPPSC PRELIMS | PYQ MASTERBOOK",
                     ParagraphStyle("ctt", fontName="Cal-B", fontSize=7.5, leading=10, textColor=GOLD_DEEP)),
           Spacer(1, 4),
           Paragraph("Contents", ParagraphStyle("ct", fontName="Cal-B", fontSize=22, leading=26, textColor=CP_NAVY)),
           Spacer(1, 10)]
    hdr = ParagraphStyle("cth", fontName="Helvetica", fontSize=6.5, leading=8, textColor=colors.HexColor("#666666"))
    num = ParagraphStyle("ctn", fontName="Cal-B", fontSize=11, leading=13, textColor=GOLD_DEEP)
    ttl = ParagraphStyle("ctx", fontName="Cal", fontSize=10, leading=12.5, textColor=INK)
    qst = ParagraphStyle("ctq", fontName="Cal", fontSize=8, leading=10, textColor=colors.HexColor("#666666"),
                         alignment=TA_RIGHT)
    pge = ParagraphStyle("ctp", fontName="Cal-B", fontSize=10, leading=12.5, textColor=CP_NAVY, alignment=TA_RIGHT)
    unit = ParagraphStyle("ctu", fontName="Helvetica-Bold", fontSize=7.2, leading=9, textColor=GOLD_DEEP)
    data = [[Paragraph("NO.", hdr), Paragraph("CHAPTER", hdr), Paragraph("QUESTIONS", ParagraphStyle(
        "cthr", parent=hdr, alignment=TA_RIGHT)), Paragraph("PAGE", ParagraphStyle("cthp", parent=hdr, alignment=TA_RIGHT))]]
    unit_rows, total = [], 0
    for ch in chapters:
        if ch.unit:
            unit_rows.append(len(data))
            data.append([Paragraph(inline(ch.unit).replace("·", "&nbsp;·&nbsp;"), unit), "", "", ""])
        p, o, _ = chapter_stats(ch)
        total += p + o
        data.append([Paragraph(f"{ch.no:02d}", num), Paragraph(inline(ch.title), ttl), Paragraph(str(p + o), qst),
                     Paragraph(str(pages.get(f"ch{ch.no}", "")), pge)])
    data.append(["", Paragraph(f"<i>Appendix: PYQ Heat Map of the {book['title']} Book</i>", ttl), "",
                 Paragraph(str(pages.get("appendix", "")), pge)])
    t = Table(data, colWidths=[46, CT_W - 46 - 70 - 50, 70, 50], repeatRows=1)
    cmds = [("LINEBELOW", (0, 0), (-1, 0), 0.9, GOLD), ("LINEBELOW", (0, 1), (-1, -1), 0.5, CT_SEP),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4), ("TOPPADDING", (0, 1), (-1, -1), 3.6),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 3.6), ("TOPPADDING", (0, 0), (-1, 0), 2),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 5)]
    for k in unit_rows:
        cmds += [("SPAN", (0, k), (-1, k)), ("BACKGROUND", (0, k), (-1, k), CT_UNIT),
                 ("TOPPADDING", (0, k), (-1, k), 6), ("BOTTOMPADDING", (0, k), (-1, k), 6),
                 ("LINEBELOW", (0, k), (-1, k), 0, colors.white)]
    t.setStyle(TableStyle(cmds))
    out.append(t)
    return out


def appendix(book, chapters, registry):
    out = [NextPageTemplate("full"), PageBreak(), Marker("appendix", registry),
           Paragraph(f"Appendix: PYQ Heat Map of the {book['title']} Book", S["chaptitle"]),
           P("Every chapter in one view. **PYQs** are full questions, **1-L** are one-liners, and **Total** is "
             "their sum. The decade columns count how many items were asked at least once in that decade, so a "
             "question repeated across decades is counted in each. Use the table to decide revision order: high "
             "totals with strong 2020s counts come first.")]
    rows = [["Ch", "Chapter", "PYQs", "1-L", "Total", "1990s", "2000s", "2010s", "2020s"]]
    tot = [0] * 7
    stats = []
    for ch in chapters:
        p, o, dec = chapter_stats(ch)
        vals = [p, o, p + o, dec["1990s"], dec["2000s"], dec["2010s"], dec["2020s"]]
        stats.append((ch, vals))
        tot = [a + b for a, b in zip(tot, vals)]
        rows.append([str(ch.no), ch.title] + [str(v) for v in vals])
    rows.append(["", "**Total**"] + [f"**{v}**" for v in tot])
    mx = max(v[2] for _, v in stats) or 1
    shade = []
    for k, (_, v) in enumerate(stats, start=1):
        a = 0.15 + 0.6 * v[2] / mx
        shade.append(("BACKGROUND", (4, k), (4, k), colors.Color(0.85, 0.70, 0.35, alpha=a)))
    shade.append(("BACKGROUND", (0, len(rows) - 1), (-1, len(rows) - 1), colors.HexColor("#efe6cf")))
    w = FULL_W
    cw = [w * 0.05, w * 0.47] + [w * 0.06] * 7
    out.append(data_table(rows, width=w, col_widths=cw, shade=shade))
    heavy = sorted(stats, key=lambda s: -s[1][2])[:5]
    recent = sorted([s for s in stats if s[1][6]], key=lambda s: -s[1][6])[:7]
    txt = ("Exam Insight: The five heaviest chapters are "
           + ", ".join(f"{c.title} ({v[2]})" for c, v in heavy) + ". ")
    if recent:
        txt += ("The chapters with the most items asked in the 2020s are "
                + ", ".join(f"{c.title} ({v[6]})" for c, v in recent) + ". ")
    txt += "Revise these first, then move down the Total column."
    out.append(label_box("UPPSC PATTERN", [txt], PAT_BG, PAT_BD, width=FULL_W))
    return out


# ---------------------------------------------------------------- chapter body
def chapter_flowables(ch, registry):
    out = [NextPageTemplate("cols"), PageBreak(), Marker(f"ch{ch.no}", registry),
           Paragraph(f"Chapter {ch.no}", S["chapno"]), Paragraph(inline(ch.title), S["chaptitle"])]
    pyqs, ones, _ = chapter_stats(ch)
    pending_section = None
    for kind, data in ch.blocks:
        if kind == "intro":
            text = " ".join(l.strip() for l in data if l.strip())
            text = text.replace("{pyqs}", str(pyqs)).replace("{ones}", str(ones))
            out.append(P(text))
        elif kind == "section":
            pending_section = Paragraph(inline(f"{data[0]}&nbsp;&nbsp;{data[1]}").replace("&amp;nbsp;", "&nbsp;"),
                                        S["section"])
            continue
        else:
            f = block_flowable(ch, kind, data)
            if pending_section is not None:
                f = [KeepTogether([pending_section] + (f if isinstance(f, list) else [f]))]
                pending_section = None
            out += f if isinstance(f, list) else [f]
    return out


def block_flowable(ch, kind, data):
    if kind == "p":
        if data.startswith("UP link:"):
            return P("**UP link:**" + data[8:])
        return P(data)
    if kind == "q":
        return question_box(data)
    if kind == "table":
        return data_table(data)
    if kind == "trap":
        return label_box("TRAP ALERT", data, TRAP_BG, TRAP_BD)
    if kind == "next":
        return label_box("LIKELY NEXT ANGLE", data, NEXT_BG, NEXT_BD)
    if kind == "pattern":
        p, o, _ = chapter_stats(ch)
        body = list(data)
        body[0] = f"Exam Insight: {p + o} items ({p} PYQs + {o} one-liners). " + body[0].strip()
        return label_box("UPPSC PATTERN", body, PAT_BG, PAT_BD)
    if kind == "up":
        return P("**UP link:** " + data)
    if kind == "heatmap":
        return heatmap_flowables(ch)
    raise ValueError(kind)


# ---------------------------------------------------------------- main
def read_book(folder):
    meta = {}
    for line in open(os.path.join(folder, "book.txt"), encoding="utf-8"):
        k, _, v = line.partition(":")
        if v.strip():
            meta[k.strip()] = v.strip()
    files = sorted(f for f in os.listdir(folder) if re.match(r"ch\d+\.txt$", f))
    chapters = [parse_chapter(os.path.join(folder, f)) for f in files]
    return meta, chapters


def build(folder, out_path):
    book, chapters = read_book(folder)
    all_items = [it for ch in chapters for it in ch.items]
    tot_pyq = sum(1 for it in all_items if it["kind"] == "pyq")
    tot_one = sum(1 for it in all_items if it["kind"] == "one")
    ys = [y for it in all_items for y in it["years"]] or [1990, 2025]
    y0, y1 = min(ys), max(ys)
    pages = {}
    for _ in range(2):              # second pass fills the contents page numbers
        registry = {}
        story = [NextPageTemplate("cover")] + cover(book, chapters, tot_pyq, tot_one, y0, y1)
        story += [NextPageTemplate("copyright"), PageBreak()] + copyright_page(book, y0, y1)
        story += [NextPageTemplate("contents"), PageBreak()] + contents(book, chapters, pages)
        for ch in chapters:
            story += chapter_flowables(ch, registry)
        story += appendix(book, chapters, registry)
        make_doc(out_path, book).build(story)
        pages = registry
    print(f"{out_path}: {len(chapters)} chapters, {tot_pyq} PYQs + {tot_one} one-liners, years {y0}-{y1}")
    for ch in chapters:
        p, o, _ = chapter_stats(ch)
        print(f"  ch{ch.no:02d} p{pages.get(f'ch{ch.no}')}: {ch.title} — {p} PYQs + {o} one-liners")


if __name__ == "__main__":
    folder = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(folder, "book.pdf")
    build(folder, out)
