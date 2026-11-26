"""templates_demo.py — high-density visual templates showcase.

Demonstrates how to convey dense conceptual / textbook information WITHOUT
compensatory prose, text-only boxes, or text tables:
  (a) Template A: Illustrated-node flowchart (visual_node)
  (b) Template B: Small-multiple visual contrast matrix (matrix_cell)
  (c) Templates C+D: In-situ rule badges + visual bar-nudge algebra (rule_badge)

Run:
    python3 templates_demo.py
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
import numpy as np

from plot_style import (
    C, INK, RULE, arrow, audit, cap_row, figure, mat, matrix_cell,
    note_key, panel, rule_badge, save, state, use_style, visual_node,
)

OUT = pathlib.Path(__file__).resolve().parent / "templates_demo.png"
use_style()

fig, axes = figure(3, width=19.2, height=6.4, ratios=[1.18, 1.05, 1.02], wspace=0.14)
fig.subplots_adjust(left=0.025, right=0.985, top=0.875, bottom=0.145)
axa, axb, axc = axes

# =========================================================================== #
# (a) Template A: Illustrated-Node Flowchart (Value vs Policy fork)
# =========================================================================== #
panel(axa, "a", "Template A: Illustrated-Node Flowchart")
axa.set_xlim(0, 10.6)
axa.set_ylim(0.2, 9.8)
axa.axis("off")

# Input state node (mini 4x4 gridworld)
ax_s = visual_node(axa, 0.20, 3.30, 1.85, 3.20, "State $s$", r"$4\times 4$ grid",
                   color="ink", header_frac=0.22, footer_frac=0.18,
                   header_fill=False, title_fs=9.8, sub_fs=8.4)
ax_s.set_xlim(0, 4)
ax_s.set_ylim(0, 4)
for r in range(4):
    for c in range(4):
        fc = C["green_f"] if (r, c) == (3, 3) else ("#ffffff" if (r, c) != (1, 1) else C["blue_f"])
        ec = C["green"] if (r, c) == (3, 3) else (C["blue_d"] if (r, c) == (1, 1) else RULE)
        ax_s.add_patch(Rectangle((c, r), 1, 1, fc=fc, ec=ec, lw=0.9))
ax_s.plot([1.5], [1.5], "o", ms=5.5, color=C["blue_d"])

# Junction fork dot
jx, jy = 2.40, 4.90
axa.plot([2.05, jx], [4.90, jy], color=INK, lw=1.6)
axa.plot([jx], [jy], "o", ms=5.5, color=INK, zorder=6)

# Top branch: Value -> Argmax
a_idx = np.arange(1, 8)
q_vals = np.array([0.18, 0.30, 0.45, 0.68, 0.84, 1.00, 0.72])

ax_v1 = visual_node(axa, 2.95, 5.45, 2.75, 3.70, "Value $Q(s,a)$",
                    "score per $a$", color="blue", title_fs=9.6, sub_fs=8.4)
ax_v1.bar(a_idx, q_vals, width=0.66, color=C["blue_l"], ec=C["blue_d"], lw=0.8)
ax_v1.set_xlim(0.3, 7.7)
ax_v1.set_ylim(0, 1.18)

ax_v2 = visual_node(axa, 6.20, 5.45, 2.55, 3.70, r"Greedy $\arg\max$",
                    r"pick $a^{*}=6$", color="blue", title_fs=9.6, sub_fs=8.4)
cols_v2 = [C["rule"] if i != 6 else C["blue_d"] for i in a_idx]
ax_v2.bar(a_idx, q_vals, width=0.66, color=cols_v2)
ax_v2.plot([6], [1.07], "o", ms=4.5, color=C["blue_d"])
ax_v2.set_xlim(0.3, 7.7)
ax_v2.set_ylim(0, 1.22)

# Bottom branch: Policy -> Sample
xs = np.linspace(0.4, 7.6, 200)
pi = np.exp(-((xs - 5.0) ** 2) / (2 * 1.15 ** 2))

ax_p1 = visual_node(axa, 2.95, 0.75, 2.75, 3.70, r"Policy $\pi_\theta(a\mid s)$",
                    "density over $a$", color="purple", title_fs=9.6, sub_fs=8.4)
ax_p1.fill_between(xs, 0, pi, color=C["purple"], alpha=0.18)
ax_p1.plot(xs, pi, color=C["purple"], lw=1.8)
ax_p1.set_xlim(0.3, 7.7)
ax_p1.set_ylim(0, 1.18)

ax_p2 = visual_node(axa, 6.20, 0.75, 2.55, 3.70, r"Sample $a \sim \pi_\theta$",
                    "3 random draws", color="purple", title_fs=9.6, sub_fs=8.4)
ax_p2.fill_between(xs, 0, pi, color=C["purple"], alpha=0.10)
ax_p2.plot(xs, pi, color=C["purple"], lw=1.4, alpha=0.7)
for xd in (3.7, 5.1, 6.5):
    yd = float(np.exp(-((xd - 5.0) ** 2) / (2 * 1.15 ** 2)))
    ax_p2.plot([xd, xd], [0, yd], color=C["purple_d"], lw=1.1, ls=(0, (2, 1.5)))
    ax_p2.plot([xd], [0.05], "o", ms=4.0, color=C["purple_d"])
ax_p2.set_xlim(0.3, 7.7)
ax_p2.set_ylim(0, 1.18)

# Output action badge
axa.add_patch(Rectangle((9.25, 4.10), 1.15, 1.60, fc="white", ec=INK, lw=1.5))
axa.text(9.825, 5.10, r"$a$", ha="center", va="center", color=INK, fontsize=13.5)
axa.text(9.825, 4.50, "action", ha="center", va="center", color=INK, fontsize=8.8)

# Flow connectors
arrow(axa, (jx, jy), (2.93, 7.30), color="blue", lw=1.6, ms=10, rad=0.18)
arrow(axa, (jx, jy), (2.93, 2.60), color="purple", lw=1.6, ms=10, rad=-0.18)
arrow(axa, (5.72, 7.30), (6.18, 7.30), color="blue", lw=1.6, ms=10)
arrow(axa, (5.72, 2.60), (6.18, 2.60), color="purple", lw=1.6, ms=10)
arrow(axa, (8.77, 7.30), (9.23, 5.20), color="blue", lw=1.6, ms=10, rad=-0.12)
arrow(axa, (8.77, 2.60), (9.23, 4.60), color="purple", lw=1.6, ms=10, rad=0.12)

# =========================================================================== #
# (b) Template B: Visual Contrast Matrix (replaces text tables)
# =========================================================================== #
panel(axb, "b", "Template B: Visual Contrast Matrix")
axb.set_xlim(0, 10.2)
axb.set_ylim(0.2, 9.8)
axb.axis("off")

x_lbl, x_c1, x_c2 = 0.05, 2.05, 6.15
cw = 3.85

# Column headers
axb.add_patch(Rectangle((x_c1, 8.85), cw, 0.70, fc=C["blue_f"], ec=C["blue_d"], lw=1.4))
axb.text(x_c1 + cw / 2, 9.20, "Value-based", ha="center", va="center",
         color=C["blue_d"], fontsize=10.5)
axb.add_patch(Rectangle((x_c2, 8.85), cw, 0.70, fc=C["purple_f"], ec=C["purple_d"], lw=1.4))
axb.text(x_c2 + cw / 2, 9.20, "Policy-based", ha="center", va="center",
         color=C["purple_d"], fontsize=10.5)

row_ys = [6.05, 3.25, 0.45]
rh = 2.45
row_names = ["Breaks first", "Cheap fix", "Data reuse"]
for y_r, rname in zip(row_ys, row_names):
    axb.text(x_lbl + 0.05, y_r + rh * 0.55, rname, ha="left", va="center",
             color=INK, fontsize=9.8)

t = np.linspace(0, 1, 80)

# Row 1: Failure modes
m11 = matrix_cell(axb, x_c1, row_ys[0], cw, rh, "optimistic overshoot", color="blue")
m11.plot(t, 0.2 + 0.85 * np.sin(np.pi * t) - 0.55 * t ** 2, color=C["blue"], lw=1.7)
m11.axhline(0.62, **state("threshold", lw=1.1))
m11.set_ylim(0, 1.05)

m12 = matrix_cell(axb, x_c2, row_ys[0], cw, rh, "early collapse", color="purple")
m12.plot(t, 0.25 + 0.22 * (1 - np.exp(-6 * t)), color=C["purple"], lw=1.7)
m12.axhline(0.75, **state("threshold", lw=1.1))
m12.set_ylim(0, 1.05)

# Row 2: Fixes
m21 = matrix_cell(axb, x_c1, row_ys[1], cw, rh, "freeze target", color="blue")
m21.plot(t, 0.45 + 0.12 * np.sin(10 * t) * np.exp(-1.5 * t), color=C["blue"], lw=1.5)
m21.step([0, 0.35, 0.70, 1.0], [0.40, 0.50, 0.56, 0.56], where="post",
         color=INK, ls="--", lw=1.2)
m21.set_ylim(0.1, 0.9)

m22 = matrix_cell(axb, x_c2, row_ys[1], cw, rh, "entropy widens $\\pi$", color="purple")
xx = np.linspace(-3, 3, 100)
m22.plot(xx, np.exp(-xx ** 2 / 0.3), color=INK, ls="--", lw=1.1)
m22.fill_between(xx, 0, 0.7 * np.exp(-xx ** 2 / 1.8), color=C["purple"], alpha=0.20)
m22.plot(xx, 0.7 * np.exp(-xx ** 2 / 1.8), color=C["purple"], lw=1.6)
m22.set_ylim(0, 1.15)

# Row 3: Data reuse
m31 = matrix_cell(axb, x_c1, row_ys[2], cw, rh, "reuses buffer", color="blue")
for k in range(5):
    m31.add_patch(Rectangle((0.4 + k * 0.7, 0.22), 0.48, 0.52,
                            fc=C["blue_f"] if k < 3 else C["blue"], ec=C["blue_d"], lw=0.9))
m31.set_xlim(0, 4.2)
m31.set_ylim(0, 1.0)

m32 = matrix_cell(axb, x_c2, row_ys[2], cw, rh, "needs fresh rollouts", color="purple")
for k in range(5):
    m32.add_patch(Rectangle((0.4 + k * 0.7, 0.22), 0.48, 0.52,
                            fc="white" if k < 3 else C["purple"],
                            ec=RULE if k < 3 else C["purple_d"], lw=0.9))
m32.set_xlim(0, 4.2)
m32.set_ylim(0, 1.0)

# =========================================================================== #
# (c) Templates C+D: In-Situ Rule Badges + Bar-Nudge Algebra
# =========================================================================== #
panel(axc, "c", "Templates C+D: In-Situ Rules $+$ Bar-Nudge")
axc.set_xlim(0, 10.0)
axc.set_ylim(0.2, 9.8)
axc.axis("off")

# Top: 4-cell strip with rules drawn ON the geometry (no prose paragraph!)
gw, gh = 1.65, 1.65
gx0, gy0 = 0.85, 6.20
for i in range(4):
    fc = C["red_f"] if i == 2 else (C["green_f"] if i == 3 else "#f8fafc")
    ec = C["red"] if i == 2 else (C["green"] if i == 3 else RULE)
    lw = 1.8 if i in (2, 3) else 1.2
    axc.add_patch(Rectangle((gx0 + i * gw, gy0), gw, gh, fc=fc, ec=ec, lw=lw))
    axc.text(gx0 + (i + 0.5) * gw, gy0 + 0.45, f"$s_{i}$", ha="center", va="center",
             color=INK, fontsize=10.5)

# Wall bounce rule on left border
axc.add_patch(FancyArrowPatch((gx0 + 0.16, gy0 + 0.92), (gx0 + 0.16, gy0 + 1.34),
                              connectionstyle="arc3,rad=-1.7", arrowstyle="-|>",
                              mutation_scale=9, lw=1.4, color=INK, zorder=6))
rule_badge(axc, (gx0 + 0.45, gy0 + 2.35), "wall bounce (0)", color="ink", fs=8.5)
axc.annotate("", xy=(gx0 + 0.10, gy0 + 1.48), xytext=(gx0 + 0.45, gy0 + 2.10),
             arrowprops=dict(arrowstyle="->", color=INK, lw=1.0))

# Step cost on interior transition arrow (s0 -> s1)
arrow(axc, (gx0 + 0.72 * gw, gy0 + 1.15), (gx0 + 1.28 * gw, gy0 + 1.15),
      color="blue", lw=1.6, ms=9)
rule_badge(axc, (gx0 + 1.45 * gw, gy0 + 2.35), r"step $-0.04$", color="blue", fs=8.5)
axc.annotate("", xy=(gx0 + 1.00 * gw, gy0 + 1.25), xytext=(gx0 + 1.40 * gw, gy0 + 2.10),
             arrowprops=dict(arrowstyle="->", color=C["blue_d"], lw=1.0))

# Terminal badges directly on pit (s2) & goal (s3) cells
rule_badge(axc, (gx0 + 2.5 * gw, gy0 + 1.32), r"$-1$ stop", color="red", fs=8.5)
rule_badge(axc, (gx0 + 3.5 * gw, gy0 + 1.32), r"$+1$ stop", color="green", fs=8.5)

axc.text(5.0, 5.45, r"$4$-cell world, $\gamma = 0.9$",
         ha="center", va="center", color="#64748b", fontsize=8.8)

# Bottom: Template D bar-nudge algebra for Q <- Q + alpha * delta
axc.plot([0.8, 9.2], [4.75, 4.75], color=RULE, lw=0.9)
axc.text(0.8, 4.25, "TD update:", ha="left", va="center",
         color=INK, fontsize=9.8)

# Number line 0..1 mapped to x = 1.2 .. 8.8
nx0, nx1 = 1.2, 8.8
def nx(val):
    return nx0 + val * (nx1 - nx0)

y_line = 2.65
axc.plot([nx0, nx1], [y_line, y_line], color=INK, lw=1.2)
for v in (0.0, 0.5, 1.0):
    axc.plot([nx(v), nx(v)], [y_line - 0.12, y_line + 0.12], color=INK, lw=1.0)
    axc.text(nx(v), y_line - 0.30, f"{v:.1f}", ha="center", va="top",
             color="#64748b", fontsize=8.5)

q_old, y_tgt, alpha = 0.35, 0.80, 0.30
q_new = q_old + alpha * (y_tgt - q_old)

# Bar showing old Q -> new Q -> target y
axc.add_patch(Rectangle((nx(0), y_line + 0.15), nx(q_old) - nx(0), 0.38,
                        fc=C["blue_f"], ec=C["blue_d"], lw=1.4))
axc.add_patch(Rectangle((nx(q_old), y_line + 0.15), nx(q_new) - nx(q_old), 0.38,
                        fc=C["amber_f"], ec=C["amber"], lw=1.4))
axc.plot([nx(y_tgt), nx(y_tgt)], [y_line - 0.10, y_line + 0.80],
         color=C["green"], lw=2.2)

axc.text(nx(q_old) / 2 + nx(0) / 2, y_line + 0.34, r"$Q_{\mathrm{old}}=0.35$",
         ha="center", va="center", color=C["blue_d"], fontsize=8.8)
axc.text(nx(y_tgt), y_line + 0.96, r"$y = r + \gamma\max_{a'} Q(s',a') = 0.80$",
         ha="center", va="bottom", color=C["green_d"], fontsize=9.0)

# Bracket for delta = y - Q_old
yb = 1.65
axc.plot([nx(q_old), nx(y_tgt)], [yb, yb], color=C["red"], lw=1.3)
for xx in (nx(q_old), nx(y_tgt)):
    axc.plot([xx, xx], [yb, yb + 0.14], color=C["red"], lw=1.3)
axc.text((nx(q_old) + nx(y_tgt)) / 2, yb - 0.16,
         r"error $\delta = +0.45$", ha="center", va="top", color=C["red"], fontsize=9.2)

# Arrow for alpha * delta nudge
axc.annotate(r"nudge $\alpha\,\delta$", xy=((nx(q_old) + nx(q_new)) / 2, y_line + 0.56),
             xytext=(nx(q_old) + 0.25, y_line + 1.22),
             color=C["amber_d"], fontsize=9.0, ha="center",
             arrowprops=dict(arrowstyle="->", color=C["amber_d"], lw=1.2))

cap_row(fig, axes, [
    ("Draw the object inside each node, not its name in words", "blue"),
    ("Compare failure shapes directly instead of writing a table", "purple"),
    ("Anchor rules and algebra to geometry — zero prose paragraphs", "green")],
    y=0.052)

note_key(fig, r"$s$ state $\cdot$ $a$ action $\cdot$ $Q$ action value $\cdot$ $\pi_\theta$ policy $\cdot$ $\gamma$ discount $\cdot$ $\alpha$ step size $\cdot$ $\delta$ TD error")

audit(fig, "templates_demo", strict=True)
save(fig, str(OUT))
