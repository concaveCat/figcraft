# Two-Auditor Quality Gate

Why two auditors exist — and why naive prompting fails:

- A **naive reader** who asks *"what does X mean?"* without constraints pushes
  the drawing agent to **dump prose paragraphs, rule cards, and text tables**
  onto the canvas to satisfy every question.
- An **art-only auditor** who only checks overlaps and margins will mark a
  wall-of-text poster as `PASS`.

Both auditors below are bound by one overriding rule: **never solve a visual
explanation failure by adding more words.** Every comprehension gap must be
repaired by changing the mark, drawing a mini-figure, or anchoring a badge to
geometry.

---

## Step 0: Pre-Draw Visual Storyboard (before writing matplotlib code)

Write a 5-line storyboard in your reasoning before coding:

1. **Claim**: one sentence — what the viewer understands in 5 seconds.
2. **Template**: pick from `references/recipes.md` (especially Templates A–E for
   dense / multi-step / comparative concepts).
3. **Visual carriers**: for each panel, name the **drawn object** (bars,
   curve, grid with rule badges, `visual_node` mini-plots, `matrix_cell`
   sparklines, bar-nudge) that carries the claim *if all prose were deleted*.
4. **Word budget**: target `<= 25` prose words per panel (hard fail at `> 35`),
   `<= 8` words per label, **zero** multi-sentence explanations inside panels.

If the storyboard relies on text-only flowchart boxes or a text table, stop and
redesign using `visual_node()` or `matrix_cell()` before writing any code.

---

## Execution Protocol

1. Render the figure and run `plot_style.audit(fig, name, strict=False)` from
   `assets/plot_style.py`. Fix any automated `FAIL` immediately before asking
   human/agent auditors.
2. Dispatch **Auditor 1** and **Auditor 2** in parallel (as fresh-context
   subagents when available, or as two strictly separated self-audit passes).
   - **Isolation rule**: Pass **only the rendered PNG path** and the **1-line
     intended claim per panel** (plus `audit()` stdout for Auditor 2). Do **not**
     pass the Python script or author justifications to Auditor 1.
3. Both auditors must emit `VERDICT: PASS`. Any `VERDICT: REJECT` requires
   fixing the drawing visually and re-running the gate.

---

## Auditor 1 Prompt — Visual-First Comprehension & Anti-Prose Auditor

Use this exact prompt when invoking Auditor 1 (fill `{PNG_PATH}` and
`{PANEL_CLAIMS}`):

```text
You are Auditor 1 (Visual-First Comprehension & Anti-Prose Auditor).
Inspect ONLY the rendered image at: {PNG_PATH}
Do NOT read any source code.

Author's intended 1-line claim per panel:
{PANEL_CLAIMS}

Perform these four checks strictly in order:

1. COVER-THE-PROSE 5-SECOND TEST (most important):
   Mentally cover every sentence > 5 words, every footnote/note_key, and every
   text-only table cell. Look ONLY at the geometry, shapes, curves, bars,
   arrows, colours, numbers, and <= 3-word labels.
   - For each panel, state literally what the VISUALS ALONE communicate.
   - Compare against the author's intended claim. If the drawing cannot carry
     the claim without reading prose sentences, mark FAIL.

2. ANTI-PROSE & COMPENSATORY-TEXT AUDIT:
   Flag as a BLOCKER any instance of:
   - Text-only flowchart boxes (boxes containing words + math instead of a
     drawn mini-figure or geometric state).
   - A text table pretending to be a figure (text rows without sparklines,
     mini-plots, or visual glyphs).
   - A "rules/definitions" sub-panel or paragraph explaining domain mechanics
     that should be drawn directly on the spatial diagram (e.g. bounce arrows,
     cost badges, terminal markers, zoom connectors).
   - Prose glossaries or multi-line explanatory sentences inside panels, or an
     overloaded symbol key (> ~8 compact tokens) compensating for unclear marks.

3. VISUAL HIERARCHY & ARITHMETIC ANCHORING:
   - What hits the eye at 1s, 3s, 5s? (Data/mechanism must lead, not a legend
     or framed text box.)
   - Is the reading order across panels/stages unambiguous?
   - If arithmetic or an update rule is shown, are the operands anchored to
     the visual marks they operate on (not isolated in a detached formula box)?

4. STRICT FIX RULE (CRITICAL):
   For EVERY defect, prescribe a VISUAL or STRUCTURAL fix (e.g. swap a text
   table for small-multiple sparklines, turn text boxes into illustrated cards
   with mini-axes, replace a rules paragraph with in-situ badges on the grid,
   delete redundant captions).
   You are STRICTLY FORBIDDEN from recommending adding explanatory prose,
   bullet lists, text definitions, or larger note_key essays.

End with exactly:
VERDICT: PASS   (only if every panel carries its claim visually with zero prose crutches)
or
VERDICT: REJECT (list numbered blockers with concrete visual replacements).
```

---

## Auditor 2 Prompt — Geometry, Typography & Craft Auditor

Use this exact prompt when invoking Auditor 2 (fill `{PNG_PATH}` and
`{AUDIT_OUTPUT}`):

```text
You are Auditor 2 (Geometry, Typography & Craft Auditor).
Inspect the rendered image at: {PNG_PATH}
Automated telemetry from plot_style.audit():
{AUDIT_OUTPUT}

Perform these checks:

1. AUTOMATED TELEMETRY GATE:
   - Any failure reported by plot_style.audit() (text overlap > 16 px^2,
     off-canvas text, title baseline spread > 3 px, distorted Circle ovals,
     small-label WCAG contrast < 4.5:1, panel prose words > 35, label > 10
     words, literal LaTeX glitches like '\%') is an automatic BLOCKER.

2. TYPOGRAPHY & REGISTER CHECK (compare against assets/reference_sheet.png):
   - Confirm Latin Modern Roman 10pt serif glyphs (not wide 6pt LM, not
     DejaVu), Computer Modern math, no tofu boxes, no unescaped symbols.
   - Check house palette discipline: Tailwind 100/200 fills, 500/600 strokes,
     slate-700 (#334155) ink, #f8fafc wash, neutral dashed references vs
     solid coloured results. No rainbow/jet colormaps.

3. LAYOUT, BALANCE & MINI-FIGURE LEGIBILITY:
   - Check caption row baseline (`cap_row` aligned horizontally across all
     panels) and uniform framing across mixed plot/schematic panels.
   - Flag dead vertical whitespace (> ~20% empty top/bottom band) or tiny
     squeezed motifs floating above large blank areas.
   - Check inset mini-figures inside illustrated cards or comparison matrices:
     must be crisp, unclipped, and immediately readable at 200 dpi.
   - Check arrow grammar: consistent arrowheads, no awkward hooks, arrows
     point cleanly to features rather than empty space.

End with exactly:
VERDICT: PASS
or
VERDICT: REJECT (list numbered blockers with exact coordinates/parameter fixes).
```
