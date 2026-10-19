"""Build a TATTVA SERIES Fast Revision Pointers PDF from pointer files.

Usage: python3 tools/pointer_build.py books/indian-geography-pointers out.pdf

The folder holds book.txt ("title: ...") and pNN.txt pointer files:
  @chapter N | Title
  @meta one line under the title (PYQ count, years, focus)
  @hot ... @end          "Asked most" box; lines are pointers
  @section N.M | Title
  - pointer text {2011, 2025}   a pointer; the years in braces are the exams that asked it
  @table ... @end        pipe table, first row is the header
  @trap ... @end         trap box (lines are pointers or plain text)
  @up text               UP link line
  @last ... @end         numbered last-minute box
Inline: **bold**, *italic*.
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tattva_build as tb  # noqa: E402  (fonts, colours, styles, tables)
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.enums import TA_CENTER  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, KeepTogether,  # noqa: E402
                                NextPageTemplate, PageBreak, PageTemplate, Paragraph, Spacer, Table)
from reportlab.pdfbase.pdfmetrics import stringWidth  # noqa: E402

RIVER = colors.HexColor("#2f6f9f")
NODE_BG = colors.HexColor("#fbf6e9")


def _arrow(c, x1, y1, x2, y2, col, w=1.1, head=4.2):
    import math
    c.setStrokeColor(col)
    c.setFillColor(col)
    c.setLineWidth(w)
    c.line(x1, y1, x2, y2)
    a = math.atan2(y2 - y1, x2 - x1)
    p = c.beginPath()
    p.moveTo(x2, y2)
    p.lineTo(x2 - head * math.cos(a - 0.45), y2 - head * math.sin(a - 0.45))
    p.lineTo(x2 - head * math.cos(a + 0.45), y2 - head * math.sin(a + 0.45))
    p.close()
    c.drawPath(p, stroke=0, fill=1)


def _fit(text, font, size, width):
    """Split text into lines that fit width."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if stringWidth(t, font, size) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


class FlowChart(Flowable):
    """Vertical chain of boxes: each row 'Label | small note'."""

    def __init__(self, title, rows):
        super().__init__()
        self.title = title
        self.rows = [[x.strip() for x in r.split("|", 1)] + [""] for r in rows if r.strip()]

    def wrap(self, aw, ah):
        self.width = aw
        self.box_w = aw - 30
        self.heights = []
        for lab, note, *_ in self.rows:
            n = len(_fit(note, "Cal", 7.6, self.box_w - 12)) if note else 0
            self.heights.append(15 + 9.4 * n)
        self.gap = 13
        self.height = 18 + sum(self.heights) + self.gap * (len(self.rows) - 1) + 4
        return aw, self.height

    def draw(self):
        c = self.canv
        y = self.height
        c.setFont("Helvetica-Bold", 6.8)
        c.setFillColor(tb.MUTED)
        c.drawString(0, y - 8, self.title.upper())
        y -= 18
        x = 15
        for k, ((lab, note, *_), h) in enumerate(zip(self.rows, self.heights)):
            c.setFillColor(NODE_BG)
            c.setStrokeColor(tb.GOLD)
            c.setLineWidth(0.7)
            c.roundRect(x, y - h, self.box_w, h, 4, stroke=1, fill=1)
            c.setFillColor(tb.NAVY)
            c.setFont("Cal-B", 9)
            c.drawCentredString(x + self.box_w / 2, y - 11, lab)
            c.setFillColor(tb.INK)
            c.setFont("Cal", 7.6)
            for j, line in enumerate(_fit(note, "Cal", 7.6, self.box_w - 12) if note else []):
                c.drawCentredString(x + self.box_w / 2, y - 20.5 - 9.4 * j, line)
            y -= h
            if k < len(self.rows) - 1:
                _arrow(c, x + self.box_w / 2, y - 1, x + self.box_w / 2, y - self.gap + 1, tb.GOLD_DEEP)
                y -= self.gap


class Confluence(Flowable):
    """A river trunk drawn top to bottom; rows 'L|R , tributary , place , note'."""

    def __init__(self, title, rows):
        super().__init__()
        self.title = title
        self.trunk = rows[0].split(":", 1)[1].strip() if rows and rows[0].lower().startswith("trunk") else ""
        self.end = ""
        self.rows = []
        for r in rows[1:] if self.trunk else rows:
            if not r.strip():
                continue
            if r.lower().startswith("end:"):
                self.end = r.split(":", 1)[1].strip()
                continue
            side, trib, place = [x.strip() for x in r.split("|")][:3]
            self.rows.append((side.upper(), trib, place))

    def wrap(self, aw, ah):
        self.width = aw
        self.step = 30
        self.height = 30 + self.step * len(self.rows) + (22 if self.end else 8)
        return aw, self.height

    def draw(self):
        c = self.canv
        cx = self.width * 0.5
        top = self.height - 14
        c.setFont("Helvetica-Bold", 6.8)
        c.setFillColor(tb.MUTED)
        c.drawString(0, self.height - 8, self.title.upper())
        y0, y1 = top - 10, top - 14 - self.step * len(self.rows)
        c.setFillColor(RIVER)
        c.setFont("Cal-BI", 8.6)
        c.drawCentredString(cx, y0 + 2, self.trunk)
        _arrow(c, cx, y0 - 2, cx, y1 - (6 if self.end else 0), RIVER, w=2.4, head=6)
        for k, (side, trib, place) in enumerate(self.rows):
            y = y0 - 18 - self.step * k
            sgn = -1 if side == "L" else 1
            tx = cx + sgn * 62
            _arrow(c, tx, y + 10, cx + sgn * 3, y, RIVER, w=1.2, head=3.6)
            c.setFillColor(RIVER)
            c.setFont("Cal-I", 8)
            (c.drawRightString if sgn < 0 else c.drawString)(tx + sgn * 2, y + 9, trib)
            c.setFillColor(tb.GOLD_DEEP)
            c.circle(cx, y, 2.6, stroke=0, fill=1)
            c.setFillColor(tb.INK)
            c.setFont("Cal-B", 8.2)
            (c.drawString if sgn < 0 else c.drawRightString)(cx - sgn * 7, y - 3, place)
        if self.end:
            c.setFillColor(tb.NAVY)
            c.setFont("Cal-B", 8.8)
            c.drawCentredString(cx, y1 - 16, self.end)

S, inline = tb.S, tb.inline
HOT = colors.HexColor("#b03a2e")
tb.style("pt", fontSize=9.3, leading=12.6, leftIndent=10, bulletIndent=0, spaceAfter=3.2)
tb.style("ptbox", fontSize=9.0, leading=12.2, leftIndent=10, bulletIndent=0, spaceAfter=2.6)
tb.style("meta", fontName="Cal-I", fontSize=9.4, leading=13, textColor=tb.MUTED, spaceAfter=8)
tb.style("legend", fontSize=7.8, leading=10.4, textColor=tb.MUTED)
tb.style("num", fontSize=9.0, leading=12.2, leftIndent=14, bulletIndent=0, spaceAfter=2.6,
         bulletFontName="Cal-B", bulletColor=tb.NAVY)
for base in ("pt", "ptbox"):
    tb.style(base + "_hot", parent=S[base], bulletFontName="Sym", bulletFontSize=6.5, bulletColor=HOT)
    tb.style(base + "_n", parent=S[base], bulletFontName="Cal-B", bulletColor=tb.GOLD_DEEP)


def years_tag(text):
    """Turn a trailing {2011, 2025} into a frequency mark and a small year list."""
    m = re.search(r"\{([^}]*)\}\s*$", text)
    if not m:
        return inline(text), 0
    years = [y.strip() for y in m.group(1).split(",") if y.strip()]
    body = inline(text[:m.start()].rstrip())
    n = len(years)
    years = ["one-liner" if y == "?" else y for y in years]
    col = "#b03a2e" if n >= 3 else "#8b6914"
    tag = (f' <font name="Cal-B" size="7.6" color="{col}">{n}×</font>'
           f' <font size="7.2" color="#5b6475">{", ".join(years)}</font>')
    return body + tag, n


def pointer(text, st="pt"):
    body, n = years_tag(text)
    if n >= 3:
        return Paragraph(body, S[st + "_hot"], bulletText="\u25a0")
    return Paragraph(body, S[st + "_n"], bulletText="\u2022")


def lines_to_pointers(lines, st):
    out = []
    for l in lines:
        l = l.strip()
        if not l:
            continue
        out.append(pointer(l[2:], st) if l.startswith("- ") else Paragraph(inline(l), S["boxtext"]))
    return out


def parse(path):
    ch = {"no": 0, "title": "", "blocks": [], "unit": None, "points": 0}
    lines = open(path, encoding="utf-8").read().split("\n")
    i = 0
    while i < len(lines):
        l = lines[i]
        if l.startswith("@chapter"):
            no, title = l[8:].split("|", 1)
            ch["no"], ch["title"] = int(no), title.strip()
        elif l.startswith("@unit"):
            ch["unit"] = l[5:].strip()
        elif l.startswith("@meta"):
            ch["blocks"].append(("meta", l[5:].strip()))
        elif l.startswith("@section"):
            ch["blocks"].append(("section", l[8:].strip().replace(" | ", "  ")))
        elif l.startswith("@up"):
            ch["blocks"].append(("up", l[3:].strip()))
        elif l.startswith(("@hot", "@table", "@trap", "@last", "@flow", "@join")):
            kind = l[1:].split()[0]
            if kind in ("flow", "join"):
                ttl = l[len(kind) + 1:].strip()
            body = []
            i += 1
            while not lines[i].startswith("@end"):
                body.append(lines[i])
                i += 1
            ch["blocks"].append((kind, (ttl, body) if kind in ("flow", "join") else body))
        elif l.startswith("- "):
            ch["blocks"].append(("pt", l[2:]))
            ch["points"] += 1
        elif l.strip():
            ch["blocks"].append(("para", l.strip()))
        i += 1
    return ch


def chapter_flowables(ch, pages):
    out = [NextPageTemplate("cols"), PageBreak(), tb.Marker(f"ch{ch['no']}", pages),
           Paragraph(f"Chapter {ch['no']}", S["chapno"]),
           Paragraph(inline(ch["title"]), S["chaptitle"])]
    legend = ('<font name="Sym" color="#b03a2e">■</font> asked 3 or more times &nbsp;&nbsp; '
              '<font color="#8b6914">•</font> asked once or twice &nbsp;&nbsp; '
              '<font name="Cal-B" color="#b03a2e">4×</font> times asked, followed by the exam years')
    head, rest = [], list(ch["blocks"])
    while rest and rest[0][0] in ("meta", "hot"):
        head.append(rest.pop(0))
    for kind, data in head:
        if kind == "meta":
            out.append(Paragraph(inline(data), S["meta"]))
        else:
            out.append(tb.boxed([Paragraph("ASKED MOST · REVISE FIRST", S["boxlabel"])]
                                + lines_to_pointers(data, "ptbox"), tb.TRAP_BG, tb.TRAP_BD))
    out += [Paragraph(legend, S["legend"]), Spacer(1, 4)]
    for kind, data in rest:
        if kind == "section":
            out.append(Paragraph(inline(data), S["section"]))
        elif kind == "pt":
            out.append(pointer(data))
        elif kind == "para":
            out.append(Paragraph(inline(data), S["bodyL"]))
        elif kind == "up":
            out.append(tb.boxed([Paragraph("UP LINK", S["boxlabel"]), Paragraph(inline(data), S["boxtext"])],
                                tb.PAT_BG, tb.PAT_BD))
        elif kind == "table":
            out.append(tb.data_table([r for r in data if r.strip()]))
        elif kind == "trap":
            out.append(tb.boxed([Paragraph("TRAP ALERT", S["boxlabel"])] + lines_to_pointers(data, "ptbox"),
                                tb.TRAP_BG, tb.TRAP_BD))
        elif kind == "flow":
            out += [Spacer(1, 3), FlowChart(*data), Spacer(1, 8)]
        elif kind == "join":
            out += [Spacer(1, 3), Confluence(*data), Spacer(1, 8)]
        elif kind == "last":
            items = [l.strip()[2:] if l.strip().startswith("- ") else l.strip() for l in data if l.strip()]
            paras = [Paragraph(inline(t), S["num"], bulletText=f"{k}.") for k, t in enumerate(items, 1)]
            out.append(KeepTogether(tb.boxed([Paragraph("LAST-MINUTE 10", S["boxlabel"])] + paras,
                                             tb.NEXT_BG, tb.NEXT_BD)))
    return out


def cover(title, chapters):
    def st(**kw):
        base = dict(fontName="Cal", alignment=TA_CENTER, textColor=tb.INK)
        base.update(kw)
        return ParagraphStyle("c", **base)
    sub = "Sample Chapter" if len(chapters) == 1 else f"Chapters 1 to {len(chapters)}"
    return [Spacer(1, 160),
            Paragraph("Q U A N T U M &nbsp;&nbsp; I A S &nbsp;&nbsp; &amp; &nbsp;&nbsp; P C S",
                      st(fontName="Helvetica-Bold", fontSize=10, leading=14, textColor=tb.GOLD_DEEP)),
            Spacer(1, 22),
            Paragraph("T A T T V A &nbsp;&nbsp; S E R I E S", st(fontName="Cal-B", fontSize=12.5, leading=16,
                                                                  textColor=tb.NAVY)),
            Spacer(1, 4),
            Paragraph("U P P S C &nbsp; P R E L I M S &nbsp;&nbsp; | &nbsp;&nbsp; F A S T &nbsp; R E V I S I O N",
                      st(fontName="Helvetica", fontSize=7.5, leading=10, textColor=tb.MUTED)),
            Spacer(1, 42),
            Paragraph(title, st(fontName="Cal-I", fontSize=34, leading=40)),
            Spacer(1, 6),
            Paragraph("PYQ-Based Revision Pointers", st(fontName="Cal-I", fontSize=14, leading=18)),
            Spacer(1, 6),
            Paragraph(sub, st(fontName="Cal-I", fontSize=11, leading=15, textColor=tb.MUTED)),
            Spacer(1, 22),
            Table([[""]], colWidths=[220], style=[("LINEABOVE", (0, 0), (-1, -1), 2.2, tb.GOLD_DEEP)]),
            Spacer(1, 10),
            Paragraph("Every pointer comes from an actual UPPSC question · Frequency marks · Year tags",
                      st(fontSize=8.5, leading=12)),
            Paragraph("Asked-Most Boxes · Trap Alerts · Quick Tables · Last-Minute 10", st(fontSize=8.5, leading=12)),
            Spacer(1, 40),
            Paragraph("© Quantum IAS &amp; PCS. All rights reserved.", st(fontSize=7, leading=9,
                                                                         textColor=tb.MUTED))]


def build(folder, out_path):
    title = "Indian Geography"
    for l in open(os.path.join(folder, "book.txt"), encoding="utf-8"):
        if l.startswith("title:"):
            title = l.split(":", 1)[1].strip()
    chapters = [parse(p) for p in sorted(glob.glob(os.path.join(folder, "p*.txt")))]
    W, H = tb.PAGE_W, tb.PAGE_H
    body_h = H - tb.MARGIN_TOP - tb.MARGIN_BOTTOM
    fr = dict(leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    left = Frame(tb.MARGIN_X, tb.MARGIN_BOTTOM, tb.COL_W, body_h, id="L", **fr)
    right = Frame(tb.MARGIN_X + tb.COL_W + tb.GUTTER, tb.MARGIN_BOTTOM, tb.COL_W, body_h, id="R", **fr)
    full = Frame(tb.MARGIN_X, tb.MARGIN_BOTTOM, tb.FULL_W, body_h, id="F", **fr)
    header = f"Quantum IAS &amp; PCS · TATTVA SERIES · UPPSC Prelims Fast Revision Pointers: {title}"

    def content_page(c, d):
        tb.draw_watermark(c)
        c.saveState()
        hp = Paragraph(header, S["header"])
        hp.wrapOn(c, tb.FULL_W, 20)
        hp.drawOn(c, tb.MARGIN_X, H - 34)
        c.setStrokeColor(tb.HAIR)
        c.setLineWidth(0.5)
        c.line(tb.MARGIN_X, H - 40, W - tb.MARGIN_X, H - 40)
        c.setFont("Cal", 8)
        c.setFillColor(tb.MUTED)
        c.drawCentredString(W / 2, 24, str(c.getPageNumber()))
        c.restoreState()

    def cover_page(c, d):
        c.saveState()
        c.setStrokeColor(tb.HAIR)
        c.setLineWidth(0.6)
        c.rect(34, 34, W - 68, H - 68)
        c.setStrokeColor(tb.GOLD_DEEP)
        c.setLineWidth(2.2)
        c.line(140, H - 34, W - 140, H - 34)
        c.line(140, 34, W - 140, 34)
        c.restoreState()

    doc = BaseDocTemplate(out_path, pagesize=(W, H), title=f"TATTVA SERIES · Fast Revision Pointers: {title}",
                          author="Quantum IAS & PCS")
    doc.addPageTemplates([PageTemplate("cover", [full], onPage=cover_page),
                          PageTemplate("full", [full], onPage=content_page),
                          PageTemplate("cols", [left, right], onPage=content_page)])
    pages = {}

    def story():
        st = cover(title, chapters)
        if len(chapters) > 1:
            st += [NextPageTemplate("full"), PageBreak()] + contents(title, chapters, pages)
        st += [NextPageTemplate("full"), PageBreak()] + how_to_use()
        for ch in chapters:
            st += chapter_flowables(ch, pages)
        return st

    doc.build(story())
    first = dict(pages)
    doc.build(story())
    if pages != first:
        doc.build(story())
    print(f"{out_path}: {len(chapters)} chapter(s), {sum(c['points'] for c in chapters)} pointers")


def contents(title, chapters, pages):
    hdr = ParagraphStyle("cth", fontName="Helvetica", fontSize=6.5, leading=8, textColor=tb.MUTED)
    num = ParagraphStyle("ctn", fontName="Cal-B", fontSize=11, leading=13, textColor=tb.GOLD_DEEP)
    ttl = ParagraphStyle("ctx", fontName="Cal", fontSize=10, leading=12.5, textColor=tb.INK)
    rt = ParagraphStyle("ctr", fontName="Cal", fontSize=8, leading=10, textColor=tb.MUTED, alignment=2)
    pge = ParagraphStyle("ctp", fontName="Cal-B", fontSize=10, leading=12.5, textColor=tb.NAVY, alignment=2)
    unit = ParagraphStyle("ctu", fontName="Helvetica-Bold", fontSize=7.2, leading=9, textColor=tb.GOLD_DEEP)
    data = [[Paragraph("NO.", hdr), Paragraph("CHAPTER", hdr),
             Paragraph("POINTERS", ParagraphStyle("h2", parent=hdr, alignment=2)),
             Paragraph("PAGE", ParagraphStyle("h3", parent=hdr, alignment=2))]]
    units = []
    for ch in chapters:
        if ch["unit"]:
            units.append(len(data))
            data.append([Paragraph(inline(ch["unit"]), unit), "", "", ""])
        data.append([Paragraph(f"{ch['no']:02d}", num), Paragraph(inline(ch["title"]), ttl),
                     Paragraph(str(ch["points"]), rt), Paragraph(str(pages.get(f"ch{ch['no']}", "")), pge)])
    W = tb.FULL_W
    t = Table(data, colWidths=[40, W - 40 - 60 - 45, 60, 45], repeatRows=1)
    cmds = [("LINEBELOW", (0, 0), (-1, 0), 0.9, tb.GOLD), ("LINEBELOW", (0, 1), (-1, -1), 0.4, tb.HAIR),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 1), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 3)]
    for k in units:
        cmds += [("SPAN", (0, k), (-1, k)), ("BACKGROUND", (0, k), (-1, k), tb.ROW_ALT)]
    from reportlab.platypus import TableStyle
    t.setStyle(TableStyle(cmds))
    return [Paragraph("Contents", ParagraphStyle("ct", fontName="Cal-B", fontSize=22, leading=26,
                                                 textColor=tb.NAVY)), Spacer(1, 10), t]


def how_to_use():
    H = ParagraphStyle("hh", fontName="Cal-B", fontSize=20, leading=24, textColor=tb.GOLD_DEEP, spaceAfter=10)
    rows = [
        ("Every pointer is a real question.", "Each pointer is the answer to a UPPSC question asked between "
         "1990 and 2025, written as a fact you can revise in seconds, with the related fact you need for the "
         "next variation."),
        ("Frequency marks.", '<font name="Sym" color="#b03a2e">\u25a0</font> and a red count (e.g. '
         '<font name="Cal-B" color="#b03a2e">4×</font>) mark a fact asked 3 or more times. '
         '<font color="#8b6914">•</font> and a gold count mark facts asked once or twice. The years follow; '
         '"one-liner" means a short starred question in the source with no year given.'),
        ("Asked Most box.", "Each chapter opens with the facts UPPSC repeats most. Revise these first."),
        ("Diagrams.", "Flowcharts and river diagrams turn sequences (river courses, confluences, processes, "
         "orders from west to east) into one picture."),
        ("Trap Alerts.", "The places where the obvious answer is wrong or two facts are commonly swapped."),
        ("Last-Minute 10.", "The ten lines to read on the morning of the exam."),
        ("Pairs with the Masterbook.", "Use this book for revision after the TATTVA PYQ Masterbook, which has "
         "the full questions, options and explanations."),
    ]
    out = [Paragraph("How to Use This Book", H)]
    for a, b in rows:
        out.append(Paragraph(f"<b>{a}</b> {b}", S["body"]))
    return out


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
