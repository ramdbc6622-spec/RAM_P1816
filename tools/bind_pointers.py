"""Bind the Fast Revision Pointers books into one volume with continuous page numbers.

Usage: python3 tools/bind_pointers.py out.pdf

Order: copyright page, a one-page subject contents, then each subject book (its cover, its own
chapter contents and its chapters). The "How to Use This Book" page appears once, in the first subject.
"""
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tattva_build as tb  # noqa: E402
from pypdf import PdfReader, PdfWriter  # noqa: E402
from reportlab.lib.enums import TA_RIGHT  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.platypus import NextPageTemplate, PageBreak, Paragraph, Spacer, Table, TableStyle  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TITLE = "General Studies"
SUBJECTS = [  # (folder, name in the contents)
    ("ancient-history-pointers", "Ancient History"),
    ("medieval-history-pointers", "Medieval History"),
    ("modern-history-pointers", "Modern History"),
    ("indian-polity-pointers", "Indian Polity"),
    ("indian-geography-pointers", "Indian Geography"),
    ("world-geography-pointers", "World Geography"),
    ("environment-pointers", "Environment and Ecology"),
    ("economics-pointers", "Economics and Social Development"),
    ("general-science-pointers", "General Science"),
]
FRONT = 2  # copyright page + contents page


def subject_contents(starts):
    out = [Paragraph("TATTVA SERIES&nbsp;&nbsp;·&nbsp;&nbsp;UPPSC PRELIMS | FAST REVISION POINTERS",
                     ParagraphStyle("btt", fontName="Cal-B", fontSize=8.5, leading=11, textColor=tb.GOLD_DEEP)),
           Spacer(1, 6),
           Paragraph("Contents", ParagraphStyle("bt", fontName="Cal-B", fontSize=30, leading=36,
                                                textColor=tb.CP_NAVY)),
           Spacer(1, 26)]
    hdr = ParagraphStyle("bth", fontName="Helvetica", fontSize=8, leading=10, textColor=tb.MUTED)
    num = ParagraphStyle("btn", fontName="Cal-B", fontSize=17, leading=21, textColor=tb.GOLD_DEEP)
    ttl = ParagraphStyle("btx", fontName="Cal-B", fontSize=16, leading=20, textColor=tb.INK)
    pge = ParagraphStyle("btp", fontName="Cal-B", fontSize=16, leading=20, textColor=tb.CP_NAVY, alignment=TA_RIGHT)
    data = [[Paragraph("NO.", hdr), Paragraph("SUBJECT", hdr),
             Paragraph("PAGE", ParagraphStyle("bthp", parent=hdr, alignment=TA_RIGHT))]]
    for k, ((_, name), start) in enumerate(zip(SUBJECTS, starts), 1):
        data.append([Paragraph(f"{k:02d}", num), Paragraph(name, ttl), Paragraph(str(start), pge)])
    t = Table(data, colWidths=[60, tb.CT_W - 60 - 70, 70])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 1.2, tb.GOLD),
                           ("LINEBELOW", (0, 1), (-1, -1), 0.6, tb.CT_SEP),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("TOPPADDING", (0, 1), (-1, -1), 14), ("BOTTOMPADDING", (0, 1), (-1, -1), 14),
                           ("BOTTOMPADDING", (0, 0), (-1, 0), 6)]))
    return out + [t]


def front_matter(path, starts):
    book = {"title": TITLE}
    doc = tb.make_doc(path, book)
    doc.title = f"TATTVA SERIES · UPPSC Prelims Fast Revision Pointers: {TITLE}"
    story = [NextPageTemplate("copyright")] + tb.copyright_page(
        book, 1990, 2025, line="UPPSC PRELIMS | FAST REVISION POINTERS",
        title=f"UPPSC Prelims Fast Revision Pointers: {TITLE} (Complete Edition)",
        source="Every pointer in this book is drawn from original previous-year questions of UPPSC and other "
               "Uttar Pradesh state-level examinations held between 1990 and 2025, tagged with the years in which "
               "it was asked. Where an answer key is marked (*), is disputed, or has been overtaken by later "
               "changes in law or fact, the pointer says so and gives the correct position.")
    story += [NextPageTemplate("contents"), PageBreak()] + subject_contents(starts)
    doc.build(story)


def build_subjects(tmp, starts):
    counts = []
    for k, ((folder, _), start) in enumerate(zip(SUBJECTS, starts)):
        out = os.path.join(tmp, f"{k:02d}.pdf")
        cmd = [sys.executable, os.path.join(HERE, "pointer_build.py"), os.path.join(ROOT, "books", folder), out,
               "--start", str(start)] + ([] if k == 0 else ["--no-howto"])
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
        counts.append(len(PdfReader(out).pages))
    return counts


def starts_for(counts):
    starts, page = [], FRONT + 1
    for n in counts:
        starts.append(page)
        page += n
    return starts


def bind(out_path):
    with tempfile.TemporaryDirectory() as tmp:
        counts = build_subjects(tmp, [1] * len(SUBJECTS))
        starts = starts_for(counts)
        counts2 = build_subjects(tmp, starts)
        assert counts2 == counts, "page counts changed with numbering"
        front = os.path.join(tmp, "front.pdf")
        front_matter(front, starts)
        assert len(PdfReader(front).pages) == FRONT, "front matter must be two pages"
        w = PdfWriter()
        w.append(front)
        w.add_outline_item("Contents", 1)
        for k, ((_, name), start) in enumerate(zip(SUBJECTS, starts)):
            w.append(os.path.join(tmp, f"{k:02d}.pdf"))
            w.add_outline_item(name, start - 1)
        w.add_metadata({"/Title": f"TATTVA SERIES · UPPSC Prelims Fast Revision Pointers: {TITLE}",
                        "/Author": "Quantum IAS & PCS"})
        with open(out_path, "wb") as fh:
            w.write(fh)
    print(f"{out_path}: {FRONT + sum(counts)} pages")
    for (_, name), start, n in zip(SUBJECTS, starts, counts):
        print(f"  p{start:>3}  {name} ({n} pages)")


if __name__ == "__main__":
    bind(sys.argv[1])
