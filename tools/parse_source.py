"""Parse the column-by-column text of the UPPSC solved-paper book into questions.

Input: text made by extract_source.sh (one "@@PAGE n L|R" marker per column).
Output: JSON list of sections, each with its full questions and one-liners,
in source order, with the source's own explanation kept for reference.
"""
import json
import re
import sys

JUNK = re.compile(
    r"^(Click here.*|General G.*|I+\. Indian G.*|Geography|uestion Papers|\*UPPSC Qu.*|"
    r"Studies \(General Geography\)|General Studies.*|\d{3,4})$"
)
TAG = re.compile(
    r"(U\.?\s?P\.|UPPSC|U\.P\.P\.S\.C|R\.O\.|Lower Sub|B\.E\.O|GIC|U\.D\.A|L\.D\.A|"
    r"Revenue Inspector|Spl\.|\(Pre\)|\(Mains\))"
)
OPT = re.compile(r"\(([a-e])\)\s*")
ANS = re.compile(r"^Ans\.?\s*(.*)$")
QSTART = re.compile(r"^(\d{1,3})\.\s*(.*)$")


def clean(line):
    line = re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", "", line)
    return re.sub(r"\s+", " ", line.replace("\t", " ")).strip()


INLINE_ONE = re.compile(r"^(.*?)\[([^\]]+)\]\s*[-–]\s*(.+)$")
DASH_ONE = re.compile(r"^(.*?[?:)\w])\s+[-–]\s+(.+)$|^(.*?\?)\s*[-–]\s*(.+)$")


def finish_one(one):
    """Close a one-liner written as 'question [exam tag] - answer'."""
    m = INLINE_ONE.match(one["q"])
    if m:
        one["q"], one["tags"], one["ans"] = m.group(1).strip(), [m.group(2).strip()], m.group(3).strip()
        return True
    if "[" in one["q"]:
        return False   # tag still open: wait for "] - answer"
    m = DASH_ONE.match(one["q"])
    if m:
        qq, aa = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
        one["q"], one["tags"], one["ans"] = qq.strip(), [], aa.strip()
        return True
    return False


def parse(lines):
    sections, sec = [], None
    q = None          # question being read
    state = "idle"    # idle | stem | opts | tags | expl | oneliner
    one = None
    page = None

    def close_q():
        nonlocal q
        if q is not None:
            sec["items"].append(q)
            q = None

    def close_one():
        nonlocal one
        if one is not None:
            sec["items"].append(one)
            one = None

    for raw in lines:
        if raw.startswith("@@PAGE"):
            page = int(raw.split()[1])
            continue
        line = clean(raw)
        if not line or JUNK.match(line):
            continue
        m = re.match(r"^r (.+)$", line)
        if m:
            close_one()
            close_q()
            sec = {"title": m.group(1), "page": page, "items": []}
            sections.append(sec)
            state, last_no = "idle", 0
            continue
        if sec is None:
            continue

        # one-liner: "*" line, question text, then "– answer"
        if line == "*" or (line.startswith("* ") and state in ("expl", "idle", "oneliner")):
            close_one()
            close_q()
            one = {"kind": "one", "q": line[1:].strip(), "ans": "", "page": page}
            state = "expl_one" if finish_one(one) else "oneliner"
            continue
        m = QSTART.match(line)
        if (m and state in ("idle", "expl", "expl_one", "oneliner")
                and last_no < int(m.group(1)) <= last_no + 3):
            close_one()
            close_q()
            last_no = int(m.group(1))
            q = {"kind": "q", "no": last_no, "page": page, "stem": [], "opts": {},
                 "tags": [], "ans": "", "expl": []}
            if m.group(2):
                q["stem"].append(m.group(2))
            state = "stem"
            continue
        if state == "oneliner":
            if line.startswith(("–", "-")) and not one["ans"]:
                one["ans"] = line.lstrip("–- ").strip()
                state = "expl_one"
                continue
            if not one["ans"]:
                one["q"] = (one["q"] + " " + line).strip()
                if finish_one(one):
                    state = "expl_one"
                elif one["q"].count(" ") > 60:
                    state = "expl_one"
                continue

        if state == "expl_one":
            # text after a one-liner's answer that is not a new item: attach as note
            one.setdefault("expl", []).append(line)
            continue
        if q is None:
            continue

        a = ANS.match(line)
        if a and state in ("stem", "opts", "tags"):
            q["ans"] = a.group(1).strip()
            state = "expl"
            continue
        if state in ("stem", "opts") and OPT.match(line):
            parts = OPT.split(line)
            # parts: ['', 'a', 'text', 'b', 'text', ...]
            for i in range(1, len(parts) - 1, 2):
                q["opts"][parts[i]] = parts[i + 1].strip()
            state = "opts"
            continue
        if state == "opts" and TAG.search(line) and not OPT.match(line):
            q["tags"].append(line)
            state = "tags"
            continue
        if state == "tags":
            q["tags"].append(line)
            continue
        if state == "opts":
            # continuation of the last option
            k = sorted(q["opts"])[-1]
            q["opts"][k] += " " + line
            continue
        if state == "stem":
            if TAG.search(line) and re.search(r"(19|20)\d\d", line) and not q["opts"]:
                q["tags"].append(line)   # one-line question with no options
                state = "tags"
                continue
            q["stem"].append(line)
            continue
        if state == "expl":
            q["expl"].append(line)
    close_one()
    close_q()
    return sections


if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    secs = parse(open(src, encoding="utf-8").read().splitlines())
    json.dump(secs, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for s in secs:
        nq = sum(1 for i in s["items"] if i["kind"] == "q")
        no = sum(1 for i in s["items"] if i["kind"] == "one")
        bad = [i["no"] for i in s["items"] if i["kind"] == "q" and (not i["ans"] or not i["tags"])]
        print(f"p{s['page']:>4}  {s['title'][:45]:45} Q={nq:3} 1L={no:3} missing={bad[:12]}")
