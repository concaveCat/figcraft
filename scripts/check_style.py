#!/usr/bin/env python3
"""check_style.py — verify the figure toolchain before drawing.

    python3 check_style.py            # fonts + rcParams assertions only
    python3 check_style.py --render    # also write <tmp>/plot_style_smoke.png

Exit code 0 = ready, 1 = something to fix.
"""
from __future__ import annotations

import pathlib
import sys
import tempfile

SKILL_DIR = pathlib.Path(__file__).resolve().parents[1]
ASSETS_DIR = SKILL_DIR / "assets"

fail = []


def ok(msg: str) -> None:
    print(f"  [ok]   {msg}")


def bad(msg: str) -> None:
    print(f"  [FAIL] {msg}")
    fail.append(msg)


if not (ASSETS_DIR / "plot_style.py").exists():
    bad(f"plot_style.py not found in {ASSETS_DIR}")
    sys.exit(1)

sys.path.insert(0, str(ASSETS_DIR))
import plot_style as mod  # noqa: E402
ok(f"plot_style imported from {ASSETS_DIR}")

print("fonts")
try:
    faces = mod.font_report()
    for label, path in faces.items():
        stem = path.replace("\\", "/").rsplit("/", 1)[-1]
        if stem.startswith("lmroman10-"):
            ok(f"{label:8s} -> {stem}")
        else:
            bad(f"{label:8s} -> {stem} (want lmroman10-*; run scripts/install_fonts.sh)")
except ValueError as exc:
    print(f"  [WARN] Latin Modern Roman not found ({exc}); falling back to cmr10/DejaVu Serif. "
          "Run scripts/install_fonts.sh on Linux/WSL if a TeX font tree is available.")

print("rcParams")
matplotlib_rc = mod.plt.rcParams
mod.use_style()
checks = {
    "font.family": ["serif"],
    "mathtext.fontset": "cm",
    "axes.unicode_minus": True,
    "savefig.bbox": "tight",
}
for key, want in checks.items():
    got = matplotlib_rc[key]
    same = list(got) == list(want) if isinstance(want, list) else got == want
    (ok if same else bad)(f"{key} = {got!r}")

if str(matplotlib_rc["font.serif"]).find("Latin Modern") >= 0:
    ok("serif stack starts from Latin Modern Roman")

if "--render" in sys.argv:
    import numpy as np
    from matplotlib.patches import Rectangle

    print("render")
    fig, ax = mod.figure(1, width=9.0, height=4.0)
    ax.add_patch(Rectangle((0, 0), 6, 2, **mod.mat("substrate")))
    ax.add_patch(Rectangle((0, 2.2), 2.6, 1.2, **mod.mat("mask")))
    x = np.linspace(0, 6, 400)
    for i, (y, lab) in enumerate([(np.cos(x / 6 * 1.5), "Model A"),
                                  (np.exp(-x / 3), "Model B")]):
        ax.plot(x, y, label=lab, **mod.MODEL[i])
    ax.axhline(0.35, **mod.state("threshold"))
    mod.panel(ax, "a", "Smoke Test: $\\theta \\leq \\pi$, $A\\oplus B_R$")
    mod.callout(ax, (4.4, 1.0), "gradient $\\nabla\\phi$", xytext=(1.9, 1.62),
                color="green")
    mod.note_box(ax, "AR $\\lesssim 1$", xy=(0.03, 0.97))
    mod.bare(ax, grid=True)
    mod.legend(ax, loc="center right")
    mod.rule_badge(ax, (1.3, 2.8), "etch $0$", color="amber")
    mod.micro(ax, "If this line is italic Latin Modern, the toolchain is ready",
              "purple", y=-0.12)
    res = mod.audit(fig, "smoke", strict=False)
    if not res["pass"]:
        bad(f"smoke audit failed: {res['issues']}")
    else:
        ok("audit() smoke check passed")
    out = mod.save(fig, str(pathlib.Path(tempfile.gettempdir()) / "plot_style_smoke.png"))
    ok(f"rendered {out} — compare glyphs with assets/reference_sheet.png")

print()
if fail:
    print(f"NOT READY: {len(fail)} problem(s)")
    sys.exit(1)
print("READY")
