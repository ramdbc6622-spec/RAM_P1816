"""Print parsed source sections compactly: python3 tools/dump_section.py ig.json 0 [1 ...]"""
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
for k in map(int, sys.argv[2:]):
    s = d[k]
    print(f"######## [{k}] {s['title']} (p{s['page']})")
    for it in s["items"]:
        if it["kind"] == "one":
            print(f"* 1L p{it['page']} [{'; '.join(it.get('tags', []))}] {it['q']} => {it['ans']}")
            if it.get("expl"):
                print("   ~", " ".join(it["expl"])[:600])
            continue
        print(f"Q{it['no']} p{it['page']} [{' | '.join(it['tags'])}] Ans {it['ans']}")
        print("   " + "\n   ".join(it["stem"]))
        for o, t in sorted(it["opts"].items()):
            print(f"   ({o}) {t}")
        print("   ~", " ".join(it["expl"])[:int(__import__("os").environ.get("EX","700"))])
