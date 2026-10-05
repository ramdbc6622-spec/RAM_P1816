"""Expand a chapter spec into builder markup, pulling questions from parsed JSON.

python3 tools/gen_chapter.py source.json spec.txt out.txt

Spec lines are copied as they are, except:
  @q S:a-b     questions a..b of source section S (and the one-liners that sit
               after them in the source), written as @pyq / @one blocks
  @q S:a       a single question
  @src S:n     marks question n of section S as written by hand in the spec
               (it is then left out of every @q range)
  @src1 S:k    the same for the k-th one-liner of section S
  @qnote S:n | text   adds an @note to generated question n
At the end every section touched is checked: each question 1..max and every
one-liner must appear exactly once.  Questions that still look broken are
listed on stderr so they can be written by hand.
"""
import json
import re
import sys

TAGRX = re.compile(r"(U\.?\s?P\.|UPPSC|UPPCS|R\.O\.|Lower Sub|B\.E\.O|GIC|U\.D\.A|L\.D\.A|\(Pre\)|\(Mains\))")
YEAR = re.compile(r"(19|20)\d\d")
JUNK = re.compile(r"\s*(FREEPDFHALL|Click here -@F|estion Papers|uestion Papers)\s*")
NEWLINE_START = re.compile(
    r"^(\d+\.\s|[A-H]\.\s|\([ivx]+\)|[ivx]+\.\s|Select|Choose|Code|Which|Consider|"
    r"Statement|Assertion|Reason|List|Find|Of the|Mark|Read|Given|What|How)"
)


def tidy(s):
    s = JUNK.sub(" ", s)
    s = re.sub(r"(\d)\s?[oº]\s?([CF])\b", "\\1°\\2", s)
    s = re.sub(r"(?<=\s)[oº]([CF])\b", "°\\1", s)
    return re.sub(r"\s+", " ", s).strip()


def repair(q):
    """Move option and tag lines that the parser left in the explanation."""
    rest = list(q["expl"])
    moved = True
    while rest and moved:
        moved = False
        line = rest[0]
        m = re.match(r"^\(([a-e])\)\s*(.*)$", line)
        if m and (len(q["opts"]) < 4):
            parts = re.split(r"\(([a-e])\)\s*", line)
            for i in range(1, len(parts) - 1, 2):
                q["opts"][parts[i]] = parts[i + 1].strip()
            rest.pop(0)
            moved = True
            continue
        if TAGRX.search(line) and YEAR.search(line) and len(line) < 120 and not q["tags"]:
            q["tags"].append(line)
            rest.pop(0)
            moved = True
            while rest and TAGRX.search(rest[0]) and YEAR.search(rest[0]) and len(rest[0]) < 120:
                q["tags"].append(rest.pop(0))
            continue
    q["expl"] = rest
    return q


def tagtext(tags):
    lines, buf = [], ""
    for t in tags:
        t = tidy(t)
        t = re.sub(r"^\d+\s+(?=U)", "", t)
        if not YEAR.search(t):
            buf = (buf + " " + t).strip()
            continue
        lines.append((buf + " " + t).strip())
        buf = ""
    if buf:
        lines.append(buf)
    out = []
    for t in lines:
        out += [x.strip() for x in re.split(r"[|;]", t) if x.strip()]
    return re.sub(r";\s*(\((Pre|Mains|Spl\.?)\))", r" \1", "; ".join(out))


def stem_lines(stem):
    out = []
    for raw in stem:
        line = tidy(raw)
        if not line:
            continue
        if out and not NEWLINE_START.match(line):
            if out[-1].endswith("-") and not out[-1].endswith(" -"):
                out[-1] = out[-1][:-1] + line
            else:
                out[-1] += " " + line
        else:
            out.append(line)
    return out


def problems(q):
    p = []
    if sorted(q["opts"]) != ["a", "b", "c", "d"]:
        p.append("opts=" + "".join(sorted(q["opts"])))
    if not q["tags"]:
        p.append("no-tag")
    if not re.match(r"^\([a-e*]\)$", q["ans"] or ""):
        p.append("ans=" + repr(q["ans"]))
    text = " ".join(q["stem"]) + " " + " ".join(q["opts"].values())
    if re.search(r"List|Column|Codes?\s*:|A\s+B\s+C\s+D", text):
        p.append("match?")
    if re.search(r"\(\s*[a-d]\s*\)", " ".join(q["opts"].values())):
        p.append("opt-in-opt")
    if any(len(v) > 160 for v in q["opts"].values()):
        p.append("long-opt")
    return p


def render_q(q):
    lines = ["@pyq " + tagtext(q["tags"])]
    lines += stem_lines(q["stem"])
    for k in sorted(q["opts"]):
        lines.append(f"({k}) {tidy(q['opts'][k])}")
    ans = re.sub(r"^\w+–", "", tidy(q["ans"] or ""))
    lines.append("@ans " + ans)
    lines.append("@end")
    return "\n".join(lines)


def render_one(o):
    qtext = tidy(o["q"])
    ans = tidy(o["ans"])
    if not ans:
        m = re.match(r"^(.*?)\s*[—–-]{1,2}\s*([^—–-]+)$", qtext)
        if m:
            qtext, ans = m.group(1).strip(), m.group(2).strip()
    tag = tagtext(o.get("tags", []))
    return f"@one {tag}".rstrip() + f"\n{qtext}\n@ans {ans}\n@end"


def main():
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    spec = open(sys.argv[2], encoding="utf-8").read().splitlines()
    for s in data:
        for it in s["items"]:
            if it["kind"] == "q":
                repair(it)
    hand_q, hand_1, notes = set(), set(), {}
    for line in spec:
        m = re.match(r"^@qnote (\d+):(\d+) \| (.+)$", line)
        if m:
            notes[(int(m.group(1)), int(m.group(2)))] = m.group(3).strip()
        m = re.match(r"^@src (\d+):(\d+)\s*$", line)
        if m:
            hand_q.add((int(m.group(1)), int(m.group(2))))
        m = re.match(r"^@src1 (\d+):(\d+)\s*$", line)
        if m:
            hand_1.add((int(m.group(1)), int(m.group(2))))

    used_q, used_1, touched = [], [], set()
    out, warn = [], []
    for line in spec:
        if re.match(r"^@src1? \d+:\d+\s*$", line) or line.startswith("@qnote "):
            continue
        m = re.match(r"^@q (\d+):(\d+)(?:-(\d+))?\s*$", line)
        if not m:
            out.append(line)
            continue
        si, a = int(m.group(1)), int(m.group(2))
        b = int(m.group(3) or a)
        touched.add(si)
        items = data[si]["items"]
        one_idx = 0
        cur = 0          # number of the last question seen
        for it in items:
            if it["kind"] == "q":
                cur = it["no"]
            else:
                one_idx += 1
            if not (a <= cur <= b) and not (a == 1 and cur == 0):
                continue
            if it["kind"] == "q":
                if (si, cur) in hand_q:
                    continue
                used_q.append((si, cur))
                block = render_q(it)
                if (si, cur) in notes:
                    block = block[:-len("@end")] + "@note " + notes.pop((si, cur)) + "\n@end"
                out.append(block)
                pr = problems(it)
                if pr:
                    warn.append(f"[{si}:{cur}] {', '.join(pr)} | {' '.join(it['stem'])[:70]}")
            else:
                if (si, one_idx) in hand_1:
                    continue
                used_1.append((si, one_idx))
                out.append(render_one(it))
                if not it.get("ans") and not re.search(r"[—–-]", it["q"]):
                    warn.append(f"[{si}:1L{one_idx}] one-liner without answer | {it['q'][:70]}")
            out.append("")
    for k in notes:
        warn.append(f"unused @qnote {k}")
    # coverage
    for si in sorted(touched | {s for s, _ in hand_q} | {s for s, _ in hand_1}):
        items = data[si]["items"]
        nums = [it["no"] for it in items if it["kind"] == "q"]
        top = max(nums)
        have = [n for s, n in used_q + list(hand_q) if s == si]
        for n in range(1, top + 1):
            c = have.count(n)
            if c != 1:
                warn.append(f"COVERAGE section {si} Q{n} appears {c} times")
        n1 = sum(1 for it in items if it["kind"] == "one")
        h1 = [k for s, k in used_1 + list(hand_1) if s == si]
        for k in range(1, n1 + 1):
            if h1.count(k) != 1:
                warn.append(f"COVERAGE section {si} one-liner {k} appears {h1.count(k)} times")
    open(sys.argv[3], "w", encoding="utf-8").write("\n".join(out).rstrip() + "\n")
    for w in warn:
        print(w, file=sys.stderr)


if __name__ == "__main__":
    main()
