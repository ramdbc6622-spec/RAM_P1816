Front covers and print identity for **Quantum IAS & PCS** books: source books, TATTVA notes, test booklets and compilations for UPPSC, BPSC and UPSC aspirants. Every cover carries the crest, the institute name and one clear title. Covers read as premium academic print: calm, symmetrical, serif-led.

## The crest

- Use `assets/Logos/quantum-crest.png` exactly as supplied: a circular crest with the Q-atom, the diya and the shloka *अल्पानामपि वस्तूनां संहतिः कार्यसाधिका*. Never redraw, recolour, crop into the rings or stretch it.
- On `cream` the crest sits directly on the ground. On `navy`, set it inside a 5px `gold` halo so its navy outer ring stays visible.
- Minimum size: 46px on screen, 25mm in print. Below that the Devanagari shloka stops being legible.
- Keep a clear zone around the crest of at least `space-3`. Nothing overlaps it.

## Voice

- Institute name is always **Quantum IAS & PCS** (ampersand, no "The"). On covers set it in `brand-line`: spaced capitals.
- Titles are bilingual when the book serves Hindi-medium readers: English in `cover-title`, Hindi in `cover-hindi` directly beneath. Never mix scripts in one line.
- Tagline **छोटे कदम, बड़ी छलांग** goes in the footer band of Flagship and Test Series covers only. The shloka lives inside the crest; do not repeat it as cover text.
- Exam tags are specific: "UPPSC Prelims 2026", "72nd BPSC CCE", never "All exams".
- No emoji, no stock photos, no exclamation marks. Numbers on covers must be real (PYQ ranges, question counts, marks).

## Colour

| Role | Token | Rule |
| --- | --- | --- |
| Flagship ground | `navy` | Full bleed. Text on it in `cream` or `gold-light`. |
| Source Book ground | `cream` | Titles in `navy`, brand line in `red`, gold text in `gold-deep`. |
| Ornament | `gold` | Rules, frames, halo. Never small text on cream (fails contrast). |
| Accent | `red` | One use per cover: the brand line, or the Test Series band. |
| Footer band | `gold-light` | Navy covers only, text in `navy-deep`. |

- Keep to navy, gold, red and cream. No gradients, no extra hues per subject; tell subjects apart by title and Hindi title, not colour.
- Screen pages use `surface`, `surface-raised`, `ink`, `muted`, `accent`, `hairline`; these switch for dark mode. Cover artwork uses the fixed brand tokens and looks identical in both themes.

## Type

- `display` (Playfair Display) for titles and heads; `serif` (Source Serif 4) for body; `label` (Josefin Sans) for spaced-caps tags; `deva` (Tiro Devanagari Hindi) for all Hindi.
- Load from Google Fonts: Playfair Display 500/700 + italics, Source Serif 4, Josefin Sans 600/700, Tiro Devanagari Hindi.
- Source Book titles are italic `display` at weight 500 (the TATTVA look). Flagship and Test Series titles are upright weight 700.

## Cover layouts

All covers are A4 portrait (210 × 297 mm; 1 : 1.414). Designs are specified at 300px wide; multiply by 2.48 for mm, or export at 2480 × 3508 px for 300 dpi print. Keep 3mm bleed on navy covers.

1. **Flagship** (`navy`): double gold frame inset `space-3`; brand line; crest in gold halo; exam line; title; Hindi title; short gold rule; italic subtitle; `gold-light` footer band with exam year and tagline. Use for printed subject books and complete-course sets.
2. **Source Book** (`cream`): hairline frame with 3px `gold` rules top and bottom; crest; brand line in `red`; kind line; gold rule; italic navy title; Hindi title; subtitle; PYQ range; "Prepared for …" tag and copyright at the foot. Use for TATTVA and PYQ source-book PDFs. No source citations on the cover.
3. **Test Series** (`cream` + `navy` head + `red` band): navy header with small crest and series name; red exam band; large test code (PT-08); paper title; Hindi title; a three-cell box for questions, marks and duration; gold-ruled footer with booklet series and tagline.

- Centre-align everything. Title block sits in the optical middle; the crest is always above the title.
- Square corners (`radius-0`) on every band and frame. The only round thing is the crest.
- Rules are 1px (frames) or 3px (top and bottom accents). Never more than two frames.
