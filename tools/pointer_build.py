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
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, NextPageTemplate,  # noqa: E402
                                PageBreak, PageTemplate, Paragraph, Spacer, Table)

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
    ch = {"no": 0, "title": "", "blocks": []}
    lines = open(path, encoding="utf-8").read().split("\n")
    i = 0
    while i < len(lines):
        l = lines[i]
        if l.startswith("@chapter"):
            no, title = l[8:].split("|", 1)
            ch["no"], ch["title"] = int(no), title.strip()
        elif l.startswith("@meta"):
            ch["blocks"].append(("meta", l[5:].strip()))
        elif l.startswith("@section"):
            ch["blocks"].append(("section", l[8:].strip().replace(" | ", "  ")))
        elif l.startswith("@up"):
            ch["blocks"].append(("up", l[3:].strip()))
        elif l.startswith(("@hot", "@table", "@trap", "@last")):
            kind = l[1:].split()[0]
            body = []
            i += 1
            while not lines[i].startswith("@end"):
                body.append(lines[i])
                i += 1
            ch["blocks"].append((kind, body))
        elif l.startswith("- "):
            ch["blocks"].append(("pt", l[2:]))
        elif l.strip():
            ch["blocks"].append(("para", l.strip()))
        i += 1
    return ch


def chapter_flowables(ch):
    out = [NextPageTemplate("cols"), PageBreak(),
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
    story = cover(title, chapters)
    for ch in chapters:
        story += chapter_flowables(ch)
    doc.build(story)
    print(f"{out_path}: {len(chapters)} chapter(s)")


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
