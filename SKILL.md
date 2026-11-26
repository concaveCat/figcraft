---
name: figcraft
description: Visual-first, anti-prose style and two-auditor workflow for explanatory scientific, engineering, and textbook figures. Use when creating, revising, or reviewing multi-panel schematics, flowcharts, model comparisons, contrast matrices, or quantitative plots with clean Latin Modern typography and annotated geometry.
---

# figcraft — Visual-First Explanatory Figures

Before drawing, inspect `assets/reference_sheet.png` (plot/schematic register)
and `assets/templates_demo.png` (high-density visual templates: illustrated-node
flowchart, small-multiple contrast matrix, annotated world, bar-nudge anatomy).

## Non-negotiables

1. **English only inside figures.** (Keep localized captions in surrounding markdown.)
2. **Latin Modern Roman 10 pt** (with `mathtext.fontset="cm"`) for text and math.
3. **One panel = one claim.** Title names the phenomenon and parameters, e.g.
   `(b) Deep Trench (AR = 3.0): Flux Shadowing`.
4. **One concept, one colour**, reused consistently across panels and figures.
5. **Reference states dashed and neutral; results solid and coloured.**
6. **Show, don't essay — zero compensatory prose.** Never fix an unclear drawing
   by adding sentences, bullet lists, rule cards, or text tables. Target
   `<= 25` prose words per panel (hard fail `> 35`), `<= 8` words per label.
7. **Every panel ends on one aligned takeaway line** (`micro()` for uniform
   panels, `cap_row()` when mixing axis-off schematics with plotted panels).
8. `dpi=200`, `savefig.bbox="tight"`, widescreen `figsize` (13–19 × 5–6.5 in).

## Conveying dense concepts without prose

When a figure must teach an unfamiliar mechanism or compare rich alternatives,
use **visual carriers** instead of explanatory text:

1. **Illustrated-node flowcharts (`visual_node`)**: Never draw boxes full of
   words. Each node embeds a mini-axes showing the actual object at that stage
   (e.g., 7-bar $Q$ vs bell-curve $\pi$, coarse mesh vs offset front) plus a
   2–4 word header and 1 compact expression.
2. **Small-multiple contrast matrices (`matrix_cell`)**: Never draw a text table.
   Each cell draws a miniature curve, distribution, or schematic glyph + a 2–4
   word tag.
3. **In-situ rule badges (`rule_badge`)**: Do not spend a panel listing rules in
   prose. Pin compact badges directly on boundary walls, transition arrows, and
   terminal cells (`bounce (0)`, `-0.04`, `+1 stop`), and link macro-to-micro
   panels with `zoom_connect()`.
4. **Arithmetic on the mark**: Print checkable numbers directly on the geometry
   ($\gamma^k$ hanging from step $k$, $\delta$ and $\alpha\delta$ drawn as bar
   lengths on a number line), not in a separate equation glossary.
5. **Compact symbol key (`note_key`)**: Strictly `<= 8` short `symbol = word`
   tokens on one grey line — never a multi-clause glossary.

## Quick start

```bash
python3 <skill-dir>/scripts/check_style.py --render
```

```python
import pathlib, sys
sys.path[:0] = [str(pathlib.Path("<skill-dir>/assets"))]
from plot_style import *
use_style()

fig, axes = figure(3, width=18.4, height=5.8, ratios=[1.05, 1.0, 1.25])
axa, axb, axc = axes

panel(axa, "a", "Illustrated Fork: Swap the Learned Object")
axa.set_xlim(0, 10); axa.set_ylim(0, 10); axa.axis("off")
ax_q = visual_node(axa, 2.0, 5.5, 3.0, 3.4, "Value $Q(s,a)$", r"$\arg\max_a Q$", color="blue")
ax_q.bar(range(5), [0.2, 0.5, 0.9, 0.4, 0.3], color=C["blue"])

# ... populate axb, axc ...

cap_row(fig, axes, [("why it matters", "blue"), ("why it matters", "purple"),
                    ("why it matters", "teal")])
note_key(fig, r"$\theta$ weights $\cdot$ $\gamma$ discount")
audit(fig, "my_fig", strict=True)
save(fig, "my_fig.png")
```

## What `assets/plot_style.py` gives you

| call | purpose |
|---|---|
| `use_style()` | rcParams: LM Roman 10 pt, sizes, ink, grid, legend, save defaults |
| `font_report()` | prints resolved faces; warns if the LM optical-size trap bites |
| `figure(ncols, width, height, ratios, wspace)` | panel row with house spacing |
| `panel(ax, "a", title)` | `(a) Title` with the right size and padding |
| `bare(ax, grid=True)` | drops top/right spines, sets `#f8fafc` panel wash |
| `callout(ax, xy, text, xytext, color)` | coloured label + arrow to the feature it names |
| `note_box(ax, text, xy, color)` | single compact caveat/bound box (`<= 1` per panel) |
| `micro(ax, text, color)` | italic one-liner under uniform panels |
| `cap_row(fig, axes, items)` | aligned caption baseline across mixed schematic/plot panels |
| `note_key(fig, text)` | compact one-line grey symbol key (`<= 8` tokens) |
| `visual_node(ax, x, y, w, h, title, ...)` | **illustrated flowchart card** returning an embedded mini-axes |
| `matrix_cell(ax, x, y, w, h, tag, ...)` | **small-multiple cell** returning a mini-axes (replaces text tables) |
| `rule_badge(ax, xy, text, color)` | compact pill badge pinned directly onto grid/wall/arrow features |
| `zoom_connect(fig, ax_src, xy_src, ax_dst, xy_dst)` | cross-panel dashed frustum linking macro detail to micro panel |
| `bands(ax, split, labels=…)` | two vertical bands sharing one x axis for two different object kinds |
| `node` / `round_patch` / `lanes` / `bitfield` | round graph nodes, SIMT/register grids, packed bit-field strips |
| `mat(...)` / `state(...)` / `MODEL[i]` / `seq_color(t)` | semantic palette & line hierarchy helpers |
| `limit_bars(...)` / `budget_bars(...)` | measured vs red acceptance limit bars |
| `audit(fig, name, strict=...)` | **automated QA**: overlaps, canvas bounds, circle roundness, WCAG contrast, prose word budget, literal LaTeX typos |
| `save(fig, path)` | 200 dpi, tight, white |

## Workflow (5-step closed loop)

Follow `references/auditors.md` strictly on every figure:

1. **Pre-draw Storyboard**: Before writing code, list `Claim -> Template (recipes.md) -> Visual carriers per panel -> Word budget (<= 25 prose words/panel)`. Reject any plan that uses text-only box flows or text tables.
2. **Render & Run `audit(fig)`**: Generate the PNG and run `plot_style.audit(fig)`. Fix all automated failures (overlaps, off-canvas text, oval circles, `< 4.2:1` contrast, `> 35` prose words/panel, literal `\%`).
3. **Two-Auditor Review (`references/auditors.md`)**:
   - **Auditor 1 (Visual-First Comprehension & Anti-Prose)**: inspects ONLY the PNG + 1-line panel claims (no code). Performs the *Cover-the-Prose 5-Second Test* and flags any compensatory text.
   - **Auditor 2 (Geometry, Typography & Craft)**: inspects the PNG + `audit()` telemetry for LM font fidelity, palette consistency, whitespace balance, and mini-figure legibility.
   *(When subagents are available, dispatch Auditor 1 and Auditor 2 in parallel as fresh-context read-only subagents from the coordinator; otherwise run them as two strict, separated passes.)*
4. **Fix Visually & Re-render**: Every Auditor 1 rejection must be fixed with a **visual replacement** (`visual_node`, `matrix_cell`, `rule_badge`, bar-nudge, `bands`), **never** by adding sentences or glossaries. Repeat until both auditors emit `VERDICT: PASS` (cap at 2 revision rounds on `BLOCKER`s).
5. **Embed** only after both gates pass.

## Traps

- **Optical-size trap**: Only 10 pt LM masters + `latinmodern-math.otf` should be
  installed (`font_report()` must print `lmroman10-regular.otf`).
- **No Greek/relations in text face**: write `$\theta$`, `$\leq$`, `$\approx$`.
- **No `\%` outside `$...$`**: in text mode matplotlib prints the backslash
  literally (`20-80\%`). Write `20-80%`.
- **`Circle` in non-equal aspect axes renders as an ellipse**: use
  `set_aspect("equal", adjustable="box")` + `set_anchor("N")`, or `round_patch()`.
- **Captions misaligned across plot/schematic panels**: use `cap_row()`.
- **Two object kinds on one y-axis read as a fit**: separate with `bands()`.

## Files

- `references/auditors.md` — Two-auditor prompts, storyboard gate, anti-prose rules.
- `references/grammar.md` — Palette hex values, typography ladder, text budget, anti-patterns.
- `references/recipes.md` — 16 panel & high-density visual templates with code patterns.
- `assets/plot_style.py` — Canonical module (style + visual primitives + `audit()`).
- `assets/plot_style_demo.py` + `assets/reference_sheet.png` — Report/plot reference sheet.
- `assets/templates_demo.py` + `assets/templates_demo.png` — High-density visual templates showcase.
- `scripts/check_style.py` — Toolchain & primitive smoke check.
- `scripts/install_fonts.sh` — Rebuilds the 10 pt Latin Modern font set.
