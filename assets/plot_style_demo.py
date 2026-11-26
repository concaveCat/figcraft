"""plot_style_demo.py — reference sheet for every helper in plot_style.py.

Run:  python3 plot_style_demo.py
  ->  plot_style_demo.png         (schematic / models / limit_bars)
  ->  plot_style_demo_budget.png  (budget_bars)
"""
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from plot_style import (C, INK, use_style, figure, panel, bare, callout, micro,
                        note_box, state, mat, limit_bars, budget_bars, save,
                        legend, MATERIAL_TEXT, MODEL, font_report)

OUT = tempfile.gettempdir()
use_style()
print("fonts:", {k: v.rsplit("/", 1)[-1] for k, v in font_report().items()})

fig, axes = figure(3, width=18.8, height=5.6, ratios=[1.0, 1.10, 1.42],
                   wspace=0.34)
ax1, ax2, ax3 = axes

# ------------------------------------------------------------------ (a) schematic
panel(ax1, "a", "2.5D Column $+$ Interval Stack")
W, sub, liner, mask = 11.0, 3.0, 0.22, 1.4
t0, t1 = 3.6, 7.4                       # trench opening
top = sub + liner + mask

ax1.add_patch(Rectangle((0, 0), W, sub, **mat("substrate")))
ax1.add_patch(Rectangle((0, sub + liner), t0, mask, **mat("mask")))
ax1.add_patch(Rectangle((t1, sub + liner), W - t1, mask, **mat("mask")))
ax1.add_patch(Rectangle((0, sub), W, liner, **mat("film")))
for x in np.arange(0, W + 0.1, 1.0):
    ax1.plot([x, x], [0, top], color=C["blue_d"], lw=0.6, alpha=0.30, zorder=2)
for x in (2.5, 3.5):                    # the two column boundaries of interest
    ax1.plot([x, x], [0.15, top - 0.1], color=C["red"], lw=2.4, ls="--", zorder=5)

callout(ax1, (3.0, top + 0.04), r"$\mathcal{C}(x,y)$", xytext=(5.0, top + 1.15),
        color="red")
callout(ax1, (8.55, sub + liner), "Thin Liner (2 nm)", xytext=(7.3, 2.35),
        color="green")
callout(ax1, (9.1, sub + liner + 0.75), "Mask", xytext=(9.35, top + 1.15),
        color="amber")
ax1.text(7.6, 1.75, "Substrate", color=MATERIAL_TEXT["substrate"], fontsize=12,
         ha="center")
ax1.text(7.6, 1.05, r"$[z_0,z_1]$", color=MATERIAL_TEXT["substrate"],
         fontsize=10, ha="center")
ax1.text(5.5, top - 0.60, "Air", color=INK, fontsize=11.5, ha="center")

ax1.set_xlim(-0.3, W + 0.3)
ax1.set_ylim(-0.2, top + 1.65)
ax1.set_xlabel("$x$  (column index)")
ax1.set_ylabel("$z$  (height)")
bare(ax1)
micro(ax1, "Interfaces stay exact at any thickness", "green")

# ------------------------------------------------------ (b) models on one axis
panel(ax2, "b", "Angular Models vs Visibility Decline")
th = np.linspace(0, 90, 600)
t = np.radians(th)
curves = [
    (np.cos(t), r"Basic  ($\cos\theta$)"),
    (np.clip((np.cos(t) - np.cos(np.radians(30))) / (1 - np.cos(np.radians(30))), 0, 1),
     r"Taper  ($\theta_c$ = $30^\circ$)"),
    (np.exp(-((th - 45) / 22) ** 2), r"Sputter  ($\theta_{\max}$)"),
]
for (y, lab), st in zip(curves, MODEL[:3]):
    ax2.plot(th, y, label=lab, **st)
ax2.axhline(0.35, label="Floor $=0.35$", **state("threshold"))
ax2.fill_between(th, 0, 0.35, color=C["red"], alpha=0.05, zorder=1)
callout(ax2, (70, 0.35), r"$y(\theta)\geq 0.35$", xytext=(64, 0.60), color="red",
        fs=10.5)
peak = curves[2][0].max()
ax2.plot([45], [peak], "o", ms=8, mfc=C["purple"], mec="white", mew=1.4, zorder=6)
callout(ax2, (45, peak), rf"peak $= {peak:.2f}$", xytext=(52, 1.32),
        color="purple", fs=10.5, rad=-0.15)
note_box(ax2, "AR $\\lesssim 1$:\nlocal angle suffices", xy=(0.03, 0.97),
         color="blue", va="top")
ax2.set_xlim(0, 90)
ax2.set_ylim(0, 1.46)
ax2.set_yticks(np.arange(0, 1.01, 0.2))
ax2.set_xlabel(r"Incidence angle $\theta$ (deg)")
ax2.set_ylabel("Normalized rate / yield")
bare(ax2, grid=True)
legend(ax2, loc="lower right", ncol=1, fontsize=9.5)
micro(ax2, "Zero ray tracing — one angle, one lookup", "blue")

# ------------------------------------------------------------- (c) limit_bars
labels = ["Growth thickness $A|B$", "Planar $\\pm z$ crossing",
          "Trench bottom & wall", "Sphere etch radial",
          "Sphere depo radial", "Oblique $35.3^\\circ$ plane",
          "4$\\times$ split-substep"]
vals = [0.00000, 0.00000, 0.00000, 0.01542, 0.03191, 0.08640, 0.07205]
lims = [0.60000, 0.50000, 0.60000, 0.50000, 0.50000, 0.50000, 0.50000]
limit_bars(ax3, labels, vals, lims, xlabel="Error magnitude (cells)",
           value_fmt="{:.5f}")
panel(ax3, "c", "Measured Precision vs Acceptance", on_axes=True)
micro(ax3, "Every row sits far left of its red tick — the budget is not the "
      "binding constraint", "purple", y=-0.245)

# ------------------------------------------------------------ (d) budget_bars
fig2, ax4 = plt.subplots(figsize=(7.4, 4.6))
budget_bars(ax4, ["Axis-aligned", "Oblique $35.3^\\circ$", "4$\\times$ substep"],
            [0.0, 0.08640, 0.07205], [0.5, 0.5, 0.5])
panel(ax4, "", "Budget Consumption by Scenario")
save(fig2, f"{OUT}/plot_style_demo_budget.png")

save(fig, f"{OUT}/plot_style_demo.png")
