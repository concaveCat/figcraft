# Visual grammar

Numbers below were sampled from the reference PNGs (dominant-colour histograms
per file), not estimated. Hex values are the Tailwind ramp the reference figures
were built on: 100/200 for fills, 500/600 for strokes, slate-700 for ink.

## Palette

| role | stroke / text | fill | used for |
|---|---|---|---|
| primary solid | `#3b82f6` `#2563eb` | `#d9ecff` `#93c5fd` | substrate, current build, "our" model |
| mask / partner | `#d97706` `#b45309` | `#fef3c7` `#fef08a` | mask, hard mask, second material across an interface |
| growth / flux | `#059669` `#047857` | `#d1fae5` `#6ee7b7` | deposited film, offset front, visible flux |
| etch / threshold | `#dc2626` | `#fee2e2` `#fef4f4` | etch direction, acceptance limit, failure region |
| alternative model | `#8b5cf6` `#7c3aed` | `#ede9fe` | third phase, anneal, variant kernel, "the other engine" |
| secondary | `#0f766e` `#0891b2` | `#ccfbf1` | bit fields, interface frames, footnote accents |
| neutral | `#334155` ink, `#cbd5e1` rule, `#e2e3e6` grid, `#f8fafc` wash | | text, spines, reference states |

Rule of thumb: **never invent a new colour for an existing concept**; a new
colour means a new concept, and it must stay the same concept in every figure of
the same report.

## Sequential ramp (one hue, for a value field)

`seq_color(t)` with `SEQ = #f8fafc -> #1d4ed8`. Use it when a filled cell
encodes a magnitude (a value function, a density, a count). Keep the printed
number in ink: the ramp must never be the only carrier of the value, and text
contrast must stay >= 4.5:1 at 11 pt, which caps the darkest fill used under
text at about `#93c5fd`.

Do not ramp *and* overpaint the extremes with a second meaning (red for a pit,
green for a goal): the ramp then stops encoding order. Put the second meaning
on the **border** or a **corner tag** instead, and say so in the caption.

## Typography ladder (base = 13 pt, dpi = 200)

| element | size | style |
|---|---|---|
| figure/panel title `(a) …` | 15–16 | regular Latin Modern (the refs use bold only in `fig01_cell_anatomy`) |
| axis label | 13 | with units, parenthesised |
| tick label | 11 | |
| legend | 10.5 | hairline frame `#cbd5e1`, alpha 0.95 |
| callout / annotation | 10–11 | colour = feature colour |
| `micro()` caption | 9.5 | italic, accent colour, `y ≈ -0.17` axes coords |
| bit-field label | 9.5 | white on the field colour, counts above |
| symbol key (`note_key`) | 8.5-9 | grey `#64748b`, centred, one line, last |
| world line | 9-9.5 | inside the panel: "5x5 grid, step -0.04, gamma = 0.9" |

Math is always `mathtext` with `fontset="cm"`; a lone symbol in prose
(`θ`, `≤`, `≈`) still goes in `$…$`, because the LM text face has no Greek.

## Line hierarchy

| role | width | style |
|---|---|---|
| result / after | 2.6–2.8 | solid, concept colour |
| reference / initial | 1.8–2.0 | neutral `#334155` or `#64748b`, `(0,(5,3))` dash |
| acceptance limit | 2.0–2.2 | red `(0,(5,3))` dash + optional 5 % fill below |
| material edge | 1.4–1.8 | concept colour, no shadow |
| cell/column网格辅助 | 0.6 | concept colour at alpha 0.30 |
| schematic arrow | 1.4–1.6 | `-|>`, `mutation_scale≈9` |

Never draw two overlapping dashed lines in the same colour family — vary hue,
not dash pattern, when two reference states coexist.

## Geometry & spacing

- Panel row: `figsize ≈ (13–19, 5–6.5)`, `wspace 0.26–0.34`. Long y-tick labels
  need the wider value plus a wider ratio for that panel.
- `dpi=200` → 2400–3800 px wide, which is what the reference PNGs are.
- Panel background `#f8fafc`, top/right spines off, grid `#e2e3e6` at alpha 0.9
  and only where a reader must actually read a value.
- Schematic coordinate systems: draw in physical units with the aspect ratio
  fixed by hand; label axes `$x$ (column index)`, `$z$ (height)`,
  `X (cells)` — the reference figures never omit units.

## Annotation & text-budget rules

1. Label colour == the colour of the feature it names.
2. Arrow points at the feature, not at empty space; avoid crossing two other
   labelled features.
3. Quantify: `Thin Liner (2 nm)`, `Open Top Etch: 3.50 cells`,
   `42% visibility throttling`, `R²=0.961, MAE=4.29 nm`, `17.28%
   (0.08640/0.50)`. A number on the mark beats a sentence in the caption.
4. Spell the consequence, not the name: *"Only amber interface cells emit
   seeds"*, *"0.08640 cells crossing err"*.
5. At most one `note_box` per panel (caveat, accepted bound, calibration note).
6. **Hard text budget (anti-prose rule)**: target `<= 25` prose words per panel
   (automated `audit()` hard-fails at `> 35`), and `<= 8` words per callout or
   label (hard-fail at `> 10`). Never put multi-sentence explanations inside a
   panel.
7. **Compact symbol key**: `note_key()` is strictly for `<= 8` short
   `symbol = word` pairs on one line, never a multi-clause glossary essay.
8. **No LaTeX text-mode escapes**: write `20-80%`, never `20-80\%` outside
   `$...$` (matplotlib renders the backslash literally outside math mode).

## Anti-patterns seen and rejected

- 3D perspective with default `mplot3d` lighting/background — breaks the flat register.
- Legend larger than the data region it covers; legends that repeat the title.
- Rainbow/`jet` colormaps: the refs use two-tone ramps of one hue.
- Text that explains what is already visible (*"this is a trench"*).
- **Text-only flowchart boxes** (boxes containing 3 lines of prose + math instead
  of an embedded mini-figure via `visual_node()`).
- **Text tables pretending to be figures** (replace with a `matrix_cell()`
  small-multiples grid of sparklines/glyphs).
- **Separate "rules paragraph" panels** (place `rule_badge()` glyphs directly
  on the grid boundary, transition arrow, or terminal cell).
- Chinese inside a Latin Modern figure (no glyphs, and it breaks the register).
- Equal-size panels when content density differs — use `width_ratios`.
- Untitled multi-panel figures: every panel gets `(a)`/`(b)`/….
