# Panel recipes

Nine shapes cover every figure in the three reference sets. Pick the recipe by
the claim, not by the data type.

---

## 1. Cross-section / stack schematic

*Reference: `assets/reference_sheet.png` (a).*

Use when the claim is about structure: layer topology, interval stacks, where a
front moves.

```python
ax.add_patch(Rectangle((0, 0), W, sub, **mat("substrate")))
ax.add_patch(Rectangle((t1, sub + liner), W - t1, mask, **mat("mask")))
ax.plot([t0, t0], [z0, z1], **state("initial"))      # reference geometry
ax.plot(x, front, **state("etch"))                   # result
callout(ax, (8.5, sub + liner), "Thin Liner (2 nm)", xytext=(7.3, 2.3), color="green")
micro(ax, "Interfaces stay exact at any thickness", "green")
```

- Build the structure from `Rectangle`s in physical units; keep the aspect
  ratio honest (a 2 nm liner must look thin, or the claim is lost).
- Column/cell guides: colour of the material at alpha 0.30, lw 0.6.
- Parameter values belong in the panel title or the legend
  (`Initial Trench (w=16, d=16)`), results in callouts.

## 2. Kernel stamp / offset envelope

Use when the claim is "one geometric operator reproduces a physics step".

```python
for p in surface_points[::k]:                        # stamp, not one giant blob
    ax.add_patch(Circle(p, R, fc=C["green_f"], ec=C["green"], alpha=.35, lw=1.0))
ax.plot(xs, ys, **state("initial"))                  # ∂A
ax.plot(xd, yd, **state("deposit"))                  # A ⊕ B_R
```

- Show the kernel repeated along the interface, semi-transparent — the point is
  that every surface point stamps its own copy.
- Corners are where the claim lives: the inner corner rounds, the outer corner
  wraps. Do not smooth the drawn result by hand.

## 3. Kernel family strip

Use to enumerate a small set of shapes/options with equal weight.

- One row, 5–6 equal panels, numbered titles
  (`1. Ball + Micro-Patch (Isotropic Capsule)`), one-line accent micro-caption
  per panel saying what the variant buys you.
- Same axis limits in every panel, dashed centre lines, centre dot in red.
- `width_ratios` all equal, `wspace ≈ 0.10`, no axis ticks (pure schematic).

## 4. Model comparison on one axis

*Reference: `assets/reference_sheet.png` (b).*

Never place the two engines' curves in two panels — overlay, so the difference
is a distance on the page.

```python
for (y, lab), st in zip(curves, MODEL[:3]):
    ax.plot(x, y, label=lab, **st)
ax.axhline(0.35, label="Floor $=0.35$", **state("threshold"))
```

- `MODEL` order carries meaning: blue solid = primary, green dashed = first
  alternative, purple dash-dot = second. Amber dotted is the fourth slot only.
- Name the parameters in the legend (`Taper ($\theta_c=30^\circ$)`).
- Mark extrema with a whitened marker + quantified callout (`peak = 1.00`).
- If one curve is a discretisation of another, its stair steps ARE the message:
  do not smooth them.

## 5. Visibility / ray-tracing diagram + decline curve

- (a)/(b) scheme: draw the medium as light fills, the ray bundle as 3–5 coloured
  segments from a single red source dot to red ✕ hits, and the blocked ray as a
  dashed red line. The blind spot of the 2.5D method should be visible as a
  region, not described in words.
- (c) quantitative: overlay the analytic kernels on one axis, then annotate the
  operating point (`AR=2 (8.7% / 5.9%)`) with an arrow from the text.
- Three panels: schematic, longer schematic, consequence — left to right.

## 6. Multi-panel causal chain

Use when the claim is a mechanism: "this gating produces that film".

- Same colours, same orientation, same scale in all panels — the reader must be
  able to flip between them without re-reading axes.
- Titles state the step (`Class I (b1): Half-Space Gated Kernels`).
- Keep annotations semantic (`Side A Gate: only $d_A$ evaluates`), not nominal.

## 7. Accuracy vs acceptance

*Reference: `assets/reference_sheet.png` (c).*

```python
limit_bars(ax, labels, values, limits, xlabel="Error magnitude (cells)")
# or, as fraction of the budget:
budget_bars(ax, labels, values, limits)
```

- Measured = bar, acceptance = red tick at the limit, text `value (limit)`.
- Sort by magnitude; extend `xlim` so the longest label fits inside the axes.
- `budget_bars` adds the 100 % rule and dual units
  (`17.28% (0.08640/0.50)`) for slides where "are we within budget?" is the
  question.
- The micro-caption is the verdict (*"Every row sits far left of its red tick"*).

## 8. Data-layout / bit-field strip

Use when the claim is about a packed record, a LUT layout, or a struct.

```python
bitfield(ax, [("Primary", 6), ("Partner", 6), ("Flag", 1),
              ("Signed Distance", 9), ("Octahedral Normal", 10)])
```

- Colours of the fields must match the colours of the geometric features above.
- Put bit counts above each field, semantic meaning inside it.
- One strip per figure; keep it at `y0 ≈ 0.02` in axes coordinates.

## 9. Illustrated-node flowchart (Template A — rich pipelines & forks)

*Replaces text-only box chains.* When a pipeline, architecture, or fork needs to
convey dense conceptual information, **never draw boxes containing only words**.
Use `visual_node()` so every stage box renders an actual mini-figure (bars,
density curve, mesh, wave, or register slice) in an embedded inset axes, plus
only a 2–4 word header and 1 compact formula/metric.

```python
ax_q = visual_node(ax, 2.0, 5.4, 2.7, 3.2, "Value $Q(s,a)$",
                   r"$\arg\max_a Q$", color="blue")
ax_q.bar(range(7), q_vals, color=C["blue"], width=0.65)
ax_q.bar([5], [q_vals[5]], color=C["blue_d"], ec=INK, lw=1.0, width=0.65)

ax_p = visual_node(ax, 2.0, 1.4, 2.7, 3.2, r"Policy $\pi_\theta(a\mid s)$",
                   r"$a \sim \pi_\theta$", color="purple")
ax_p.plot(xs, pi, color=C["purple"], lw=1.8)
ax_p.fill_between(xs, 0, pi, color=C["purple"], alpha=0.18)
```

- Every stage shows *what kind of mathematical or physical object* lives there
  (discrete bars vs continuous distribution, coarse grid vs refined front).
- Connect stages with `arrow(..., lw=1.6)` or fork from a single junction dot.
- Keep node headers to `2–4` words and footers to `<= 1` expression/number.
- Colour per branch/stage matches the house palette; failed/removed stages use
  the red family (`color="red"`).


## 10. State graph / backup diagram

*Textbook use: MDP transition graphs, the one-step Q backup, dependency graphs.*

```python
node(ax, (1.5, 8.2), 0.42, r"$s_0$")
node(ax, (7.1, 8.2), 0.28, r"$T$", double=True)      # terminal
arrow(ax, (2.0, 8.2), (3.1, 8.2), color="ink")
ax.text(2.5, 8.35, "$p=0.8$\n$r=-1$", ha="center", va="bottom", fontsize=9)
```

- Both node centres and edge labels are annotations: the label sits *above*
  its edge, the same way for every edge.
- Self-loops: `arrow(..., rad=-1.1)` between two points on the rim; the label
  goes above the loop, not inside it.
- Never let a circle render as an ellipse: `set_aspect("equal",
  adjustable="box")` + `set_anchor("N")`, or `round_patch()`.
- A backup diagram earns a **bracket over the row that is read** and one
  arrow into the cell that is written. Words ("read the row, keep the max")
  belong under the bracket, not instead of it.

## 11. Lane / SIMT grid

*Textbook use: an execution unit's lanes, a register file, a warp, a lattice.*

```python
lanes(ax, x0, y0, rows=4, cols=8, sq=0.185, gap=0.045, fc="blue_f", ec="blue_d")
lanes(ax, x0, y0 - 1.0, rows=2, cols=8, sq=0.185, gap=0.045,
      fc="amber_f", ec="amber")
```

- One square = one unit of the thing you are counting, and the count is
  printed (`32 FP32 lanes`, `16 INT32 lanes`, `512 rows = 64 KB`).
- Highlight a *row* to show what one instruction touches; highlight a *column
  run* to show an active mask. Both get a single label, not a legend.
- If two quantities multiply (lanes x registers), print the unit chain once:
  `one row = 32 lanes x 32 b = 128 B (x 512 rows = 64 KB)`. This kills the
  "16 384 x 128 B" misreading.
- Keep squares >= 0.18 data units at 200 dpi, else the grid greys to a haze.

## 12. Two bands, one x axis

*Textbook use: value per action vs policy density; counts vs rate; two
objects of different kind over the same domain.*

```python
lower, upper = bands(ax, split=1.4, labels=((r"$Q$", "blue"), (r"$\pi$", "purple")))
ax.bar(a, upper(q) - 1.4, bottom=1.4, width=0.66, color=C["blue"], alpha=.85)
ax.plot(xs, lower(pi), color=C["purple"], lw=2.6)
ax.set_yticks([])                       # each band is rescaled, say so in the key
```

- Never overlay a density on value bars on one axis: it reads as a fit.
- The divider is a hairline; the two band labels are the y axis.
- Everything on the x axis stays shared: same ticks, same label, one `a^{*}`.

## 13. Visual contrast matrix (Template B — replaces text tables)

*Use instead of text tables for: "neither wins", failure modes, trade-off
comparisons, regime galleries.* Never fill a panel with a prose table. Put
methods in columns (coloured header pills) and comparison axes in rows, where
each cell is a `matrix_cell()` mini-plot + a `2–4` word tag.

```python
c1 = matrix_cell(ax, x1, y, w, h, tag="optimistic blow-up", color="blue")
c1.plot(t, blowup_curve, color=C["blue"], lw=1.6)
c1.axhline(1.0, **state("threshold"))

c2 = matrix_cell(ax, x2, y, w, h, tag="collapses to 1 action", color="purple")
c2.bar(range(5), [0.02, 0.03, 0.91, 0.02, 0.02], color=C["purple"])
```

- Header pills are the only filled title bars; cells carry tiny, clean
  sparklines, bar shapes, or schematic glyphs (`<= 4` words per cell tag).
- The decisive claim row goes **first**, not last.
- If the title says "different" (not "better"), both columns must show a
  distinct failure/trade-off shape rather than reading as a `high/low` scoreboard.

## 14. Annotated world with rule badges (Template C — spatial rules in-situ)

*Textbook/TCAD use: grid worlds, boundary conditions, PDE/process domains.*
Never spend an entire panel writing a bullet list of environment rules. Draw the
spatial domain once and pin `rule_badge()` directly where each rule acts:

- Wall/border rule: U-turn bounce arrow at the boundary + `rule_badge(..., "bounce (0)")`.
- Interior step cost: transition arrow inside a cell + `rule_badge(..., "step -0.04")`.
- Terminal cells: thick green/red border + corner badge `+1 (stop)` / `-1 (stop)`
  (keep ink >= 4.5:1 contrast; do not let overpainted terminals break the value ramp).

## 15. Visual algebra / bar-nudge anatomy (Template D — update rules)

*Textbook use: Q-learning backup, gradient step, relaxation/smoothing step.*
Instead of pairing a tiny schematic with a 3-row prose-gloss table (`target /
error / update`), draw the arithmetic directly as geometric lengths:

- Show the source row read (`max` bracket) flowing through $\times\gamma + r$ to
  a **target marker** $y$ on a horizontal bar/number-line.
- Draw the **old estimate** $Q(s,a)$ on the same scale, bracket the gap
  $\delta = y - Q$, and shade the fraction $\alpha\delta$ nudging the old marker
  toward $y$.
- Every symbol ($r, \gamma, y, \delta, \alpha$) sits on the mark that computes it.

## 16. Macro–micro–trace zoom triptych (Template E — systems & mechanisms)

*Textbook/EDA use: hardware floorplan -> execution lane -> trace; solver ->
stencil -> convergence.*

- `(a)` Macro architecture, `(b)` zoomed mechanism, `(c)` measured consequence.
- Use `zoom_connect(fig, axa, xy_block, axb, xy_corner)` so ownership between
  macro and micro is visually wired without prose explanations.
- For hardware divergence/branching, draw the split (`if / else` paths feeding
  active vs idle lanes) directly above the lane mask rather than explaining it
  in two sentences.

---

## Composition notes

- Two-panel figures are the workhorse (`1.0 : 1.2`); three-panel when the story
  is schematic → mechanism → consequence.
- Give the densest panel the widest ratio; never let a y-tick label spill into
  the neighbouring axes (increase `wspace`, shorten the label, or both).
- Caption in the report stays Chinese; every glyph inside the figure is English.
