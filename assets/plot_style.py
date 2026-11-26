"""plot_style.py — house style & visual-template toolkit for explanatory figures.

Colours are built on a Tailwind ramp (100/200 fills, 500/600 strokes, slate-700
ink). Typography is Latin Modern Roman (10 pt optical master only) with Computer
Modern for math.

Quick start
-----------
    import pathlib, sys
    sys.path.insert(0, str(pathlib.Path("<skill-dir>/assets")))
    from plot_style import *
    use_style()

    fig, ax = figure(1)
    panel(ax, "a", "2.5D Column + Interval Stack")

    ax.add_patch(Rectangle((0, 0), 10, 3, **mat("substrate")))
    ax.plot(x, y, **state("initial"))
    callout(ax, (3, 4), "Thin Liner (2 nm)", xytext=(7, 5.4), color="green")
    micro(ax, "Interfaces stay exact at any thickness", "green")
    audit(fig, "fig01", strict=True)
    save(fig, "fig01.png")

Rules that the style enforces / assumes
--------------------------------------
1. One panel = one claim; the panel title names the quantity and its parameters.
2. Each concept keeps one colour across every panel and every figure
   (see MATERIAL / STATE / MODEL below).
3. Reference states are dashed and neutral; results are solid and coloured.
4. Numbers live in the annotations, not in the caption.
5. Every schematic panel ends with a one-line italic `micro()` caption that
   says *why the design matters*, not what the object is.
6. In-figure text is English. Latin Modern Roman ships no Greek letters and
   no relation symbols (no theta, <=, ~=), so any math -- including a lone
   symbol like theta -- must be written in mathtext: "$\\theta$", "$\\leq$".
   Plain minus, en dash, plus-minus and micro ARE in the font and may be typed.
"""

from __future__ import annotations

import matplotlib
from matplotlib import font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch  # noqa: F401

__all__ = [
    "C", "MATERIAL", "STATE", "MODEL", "INK", "GRID", "PANEL", "RULE",
    "use_style", "font_report", "figure", "panel", "bare", "callout",
    "micro", "note_box", "arrow", "state", "mat", "limit_bars",
    "budget_bars", "bitfield", "save", "legend", "SEQ", "seq_color", "node",
    "round_patch", "lanes", "cap_row", "note_key", "bands",
    "visual_node", "matrix_cell", "rule_badge", "zoom_connect", "audit",
]


# --------------------------------------------------------------------------- #
# palette (sampled from the reference figure sets)
# --------------------------------------------------------------------------- #
C = {
    # neutrals
    "ink":      "#334155",   # slate-700: all text, axes, spines
    "grid":     "#e2e3e6",   # gridlines
    "panel":    "#f8fafc",   # axes background wash
    "rule":     "#cbd5e1",   # legend / box hairline (slate-300)
    "white":    "#ffffff",
    # primary ramp
    "blue":     "#3b82f6", "blue_d": "#2563eb", "blue_f": "#d9ecff",
    "blue_l":   "#93c5fd",
    # mask / partner material
    "amber":    "#d97706", "amber_d": "#b45309", "amber_f": "#fef3c7",
    "amber_l":  "#fed7aa", "yellow_f": "#fef08a",
    # growth / deposition / flux
    "green":    "#059669", "green_d": "#047857", "green_f": "#d1fae5",
    "green_l":  "#6ee7b7",
    # etch / threshold / failure
    "red":      "#dc2626", "red_f": "#fee2e2",
    # alternative models / third phase / anneal
    "purple":   "#8b5cf6", "purple_d": "#7c3aed", "purple_f": "#ede9fe",
    # secondary accents
    "teal":     "#0f766e", "cyan": "#0891b2", "cyan_f": "#ccfbf1",
}

INK, GRID, PANEL, RULE = C["ink"], C["grid"], C["panel"], C["rule"]

# material fills: face / edge / matching text colour
MATERIAL = {
    "substrate": dict(facecolor=C["blue_f"],  edgecolor=C["blue_d"],  lw=1.8),
    "solid":     dict(facecolor=C["blue_f"],  edgecolor=C["blue_d"],  lw=1.8),
    "mask":      dict(facecolor=C["amber_f"], edgecolor=C["amber"],   lw=1.8),
    "partner":   dict(facecolor=C["yellow_f"], edgecolor=C["amber"],  lw=1.8),
    "film":      dict(facecolor=C["green_f"], edgecolor=C["green"],   lw=1.6),
    "deposit":   dict(facecolor=C["green_f"], edgecolor=C["green"],   lw=1.6),
    "phase_c":   dict(facecolor=C["purple_f"], edgecolor=C["purple"], lw=1.6),
    "void":      dict(facecolor="white",      edgecolor=C["ink"],     lw=1.4),
    "interface": dict(facecolor=C["cyan_f"],  edgecolor=C["cyan"],    lw=1.4),
}

MATERIAL_TEXT = {
    "substrate": C["blue_d"], "solid": C["blue_d"], "mask": C["amber_d"],
    "partner": C["amber_d"], "film": C["green_d"], "deposit": C["green_d"],
    "phase_c": C["purple_d"], "void": INK, "interface": C["teal"],
}

# Accessible text ink per colour name (>= 4.5:1 on white, >= 4.2:1 on 100-tint)
TEXT_COLOR = {
    "blue": C["blue_d"], "green": C["green_d"], "purple": C["purple_d"],
    "amber": C["amber_d"], "red": C["red"], "teal": C["teal"],
    "cyan": C["teal"], "ink": INK,
}


def _text_col(color: str) -> str:
    return TEXT_COLOR.get(color, C.get(color, color))

# line states: reference frames are dashed + neutral, results are solid
STATE = {
    "initial":   dict(color=INK,         lw=2.0, ls=(0, (5, 3))),
    "initial_g": dict(color="#64748b",   lw=1.8, ls=(0, (5, 3))),
    "threshold": dict(color=C["red"],    lw=2.0, ls=(0, (5, 3))),
    "result":    dict(color=C["blue"],   lw=2.8, ls="-"),
    "etch":      dict(color=C["red"],    lw=2.8, ls="-"),
    "deposit":   dict(color=C["green"],  lw=2.8, ls="-"),
    "anneal":    dict(color=C["purple"], lw=2.8, ls="-"),
    "fit":       dict(color=C["red"],    lw=1.8, ls="-"),
}

# ordered styles for "model A vs B vs C" comparisons (same axis, never 2 figures)
MODEL = [
    dict(color=C["blue"],   lw=2.8, ls="-"),
    dict(color=C["green"],  lw=2.6, ls=(0, (6, 2))),
    dict(color=C["purple"], lw=2.6, ls=(0, (7, 2, 1.5, 2))),
    dict(color=C["amber"],  lw=2.4, ls=(0, (1.6, 1.6))),
]

FONT_STACK = ["Latin Modern Roman", "cmr10", "DejaVu Serif"]


# --------------------------------------------------------------------------- #
# global style
# --------------------------------------------------------------------------- #
def use_style(base: float = 13.0, dpi: int = 200) -> None:
    """Install the global rcParams. Call once, before creating figures."""
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": FONT_STACK,
        "font.size": base,
        "mathtext.fontset": "cm",
        "axes.titlesize": base + 2,
        "axes.titleweight": "normal",
        "axes.labelsize": base,
        "axes.edgecolor": INK,
        "axes.linewidth": 1.0,
        "axes.labelcolor": INK,
        "axes.facecolor": PANEL,
        "axes.unicode_minus": True,          # LM Roman has a real minus
        "xtick.color": INK, "ytick.color": INK,
        "xtick.labelsize": base - 2, "ytick.labelsize": base - 2,
        "xtick.major.width": 1.0, "ytick.major.width": 1.0,
        "xtick.minor.width": 0.8, "ytick.minor.width": 0.8,
        "grid.color": GRID, "grid.linewidth": 0.9, "grid.alpha": 0.9,
        "legend.frameon": True, "legend.framealpha": 0.95,
        "legend.edgecolor": RULE, "legend.fontsize": base - 2.5,
        "legend.handlelength": 2.3, "legend.borderpad": 0.5,
        "lines.solid_capstyle": "round",
        "patch.linewidth": 1.6,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
        "savefig.dpi": dpi,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.12,
        "figure.autolayout": False,
    })


def font_report() -> dict:
    """Resolve the face actually used. Warns on the LM optical-size trap:
    the font ships 5/6/7/8/9/10/12/17pt masters that all share the family
    name, and matplotlib otherwise silently picks the 6pt design (20% wider)."""
    out = {}
    for label, kw in [("regular", {}),
                      ("bold", {"weight": "bold"}),
                      ("italic", {"style": "italic"})]:
        path = fm.findfont(fm.FontProperties(family="Latin Modern Roman", **kw),
                           fallback_to_default=False)
        out[label] = path
        stem = path.rsplit("/", 1)[-1]
        if stem.startswith("lmroman") and "10-" not in stem:
            print(f"[plot_style] WARNING: {label} resolved to {stem} "
                  f"(want lmroman10-*); prune the other optical sizes.")
    return out


# --------------------------------------------------------------------------- #
# layout helpers
# --------------------------------------------------------------------------- #
def figure(ncols: int = 1, width: float = 13.6, height: float = 5.0,
           ratios=None, wspace: float = 0.22, **kw):
    """Row of ncols panels with reference-matching geometry and spacing."""
    if ratios is None:
        ratios = [1.0] * ncols
    fig, axes = plt.subplots(1, ncols, figsize=(width, height),
                            gridspec_kw=dict(width_ratios=ratios, wspace=wspace),
                            **kw)
    return fig, axes


def bare(ax, grid: bool = False, keep=("left", "bottom"), facecolor: bool | None = None):
    """Strip the frame down: only the named spines survive."""
    for name in ("top", "right", "left", "bottom"):
        ax.spines[name].set_visible(name in keep)
    if facecolor is not False:
        ax.set_facecolor(PANEL if facecolor is None else facecolor)
    if grid:
        ax.grid(True, axis="both")
        ax.set_axisbelow(True)
    return ax


def panel(ax, tag: str, title: str, sub: str | None = None,
          on_axes: bool = False, fs: float | None = None, pad: float = 10):
    """Panel heading. tag is 'a'/'b'/..., title carries the parameters."""
    text = f"({tag}) {title}" if tag else title
    if fs is None:
        fs = plt.rcParams["axes.titlesize"]
    if on_axes:
        ax.text(0.0, 1.02, text, transform=ax.transAxes, ha="left", va="bottom",
                fontsize=fs, color=INK)
    else:
        ax.set_title(text, color=INK, pad=pad, fontsize=fs)
    if sub:
        ax.text(0.5, 1.005 if not on_axes else 1.09, sub, transform=ax.transAxes,
                ha="center", va="bottom", fontsize=fs - 4, color="#64748b")
    return ax


def micro(ax, text: str, color: str = "ink", y: float = -0.165):
    """One-line italic 'why it matters' caption under a panel."""
    ax.text(0.5, y, text, transform=ax.transAxes, ha="center", va="top",
            fontsize=plt.rcParams["font.size"] - 4, color=_text_col(color),
            style="italic")


def save(fig, path, dpi: int | None = None, pad: float | None = None):
    fig.savefig(path, dpi=dpi, pad_inches=pad)
    print(f"[plot_style] wrote {path}")
    return path


# --------------------------------------------------------------------------- #
# annotation grammar
# --------------------------------------------------------------------------- #
def callout(ax, xy, text: str, xytext=None, color: str = "ink", fs: float | None = None,
            ha: str = "center", va: str = "center", rad: float = 0.0,
            arrow: bool = True, boxed: bool = False, lw: float = 1.4):
    """Coloured label pointing at the feature it names (label colour == feature)."""
    col = _text_col(color)
    if fs is None:
        fs = plt.rcParams["font.size"] - 2
    kw = {}
    if arrow:
        kw["arrowprops"] = dict(arrowstyle="->", color=C.get(color, col), lw=lw,
                                shrinkA=2, shrinkB=3,
                                connectionstyle=f"arc3,rad={rad}")
    if boxed:
        kw["bbox"] = dict(boxstyle="round,pad=0.35", fc="white", ec=C.get(color, col), lw=1.0)
    return ax.annotate(text, xy=xy, xytext=xytext, color=col, fontsize=fs,
                       ha=ha, va=va, zorder=8, **kw)


def note_box(ax, text: str, xy=(0.03, 0.97), color: str = "blue",
             va: str = "top", ha: str = "left", fs: float | None = None):
    """Boxed aside (caveat, acceptance bound, calibration note)."""
    col = _text_col(color)
    ec = C.get(color, col)
    if fs is None:
        fs = plt.rcParams["font.size"] - 3
    return ax.text(xy[0], xy[1], text, transform=ax.transAxes, color=col,
                   fontsize=fs, ha=ha, va=va, zorder=9, linespacing=1.35,
                   bbox=dict(boxstyle="round,pad=0.45", fc="white", ec=ec,
                             lw=1.0, alpha=0.94))


def arrow(ax, start, end, color: str = "blue", lw: float = 1.6,
          rad: float = 0.0, head: str = "-|>", ms: float = 9, **kw):
    """Plain schematic arrow (no text). rad curves it; on matplotlib >= 3.10
    FancyArrowPatch no longer takes `rad`, so it becomes a connectionstyle."""
    if rad:
        kw["connectionstyle"] = f"arc3,rad={rad}"
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle=head,
                                 mutation_scale=ms, lw=lw,
                                 color=C.get(color, color), zorder=7,
                                 shrinkA=0, shrinkB=0, **kw))


def state(name: str, **override) -> dict:
    """Line kwargs for a named state, e.g. ax.plot(x, y, **state('initial'))."""
    kw = dict(STATE[name])
    kw.update(override)
    return kw


def mat(name: str, **override) -> dict:
    """Patch kwargs for a material, e.g. ax.add_patch(Rectangle(..., **mat('mask')))."""
    kw = dict(MATERIAL[name])
    kw.update(override)
    return kw


# --------------------------------------------------------------------------- #
# quantitative panels
# --------------------------------------------------------------------------- #
def limit_bars(ax, labels, values, limits, unit: str = "",
               value_fmt: str = "{:.5f}", color: str = "blue",
               xlabel: str = "Error magnitude", sort: bool = True,
               threshold_label: str = "Acceptance threshold", fs: float | None = None):
    """fig13 idiom: measured error as a bar, the acceptance limit as a red tick,
    and 'value (limit)' written next to each row, sorted by magnitude."""
    import numpy as np
    if fs is None:
        fs = plt.rcParams["font.size"] - 3
    values = np.asarray(values, float)
    limits = np.asarray(limits, float)
    labels = list(labels)
    if sort:
        order = np.argsort(values)
        values, limits = values[order], limits[order]
        labels = [labels[i] for i in order]
    y = np.arange(len(labels))
    ax.barh(y, values, height=0.62, color=C.get(color, color),
            edgecolor="white", lw=0.8, zorder=3, label="Measured")
    span = max(float(values.max()), float(limits.max()))
    xmax = span * 1.62                    # room on the right for the labels
    ax.set_xlim(0, xmax)
    for yi, v, lim in zip(y, values, limits):
        ax.plot([lim, lim], [yi - 0.26, yi + 0.26], color=C["red"], lw=2.6,
                solid_capstyle="butt", zorder=5,
                label=None if yi else threshold_label)
        ax.text(lim + 0.018 * xmax, yi,
                f"{value_fmt.format(v)}  (limit {value_fmt.format(lim)})",
                va="center", ha="left", fontsize=fs, color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel(xlabel if not unit else f"{xlabel} ({unit})")
    ax.set_ylim(-0.9, len(labels) - 0.2)
    bare(ax, grid=True, keep=("left", "bottom",))
    ax.grid(False, axis="y")
    ax.grid(True, axis="x")
    legend(ax, loc="lower right", bbox_to_anchor=(1.0, 0.0))
    return ax


def budget_bars(ax, labels, values, limits, xlabel: str = "% of acceptance limit",
                value_fmt: str = "{:.5f}", color: str = "blue",
                fs: float | None = None, limit_label: str = "100% limit"):
    """fig14 idiom: same data as fraction of the budget, 100% line, dual units."""
    import numpy as np
    if fs is None:
        fs = plt.rcParams["font.size"] - 3
    pct = 100.0 * np.asarray(values, float) / np.asarray(limits, float)
    x = np.arange(len(labels))
    ax.bar(x, pct, width=0.55, color=C.get(color, color), edgecolor="none",
           zorder=3)
    ax.axhline(100, **{**STATE["threshold"], "lw": 2.2})
    ax.text(len(labels) - 0.5, 103, limit_label, ha="right", va="bottom",
            color=C["red"], fontsize=fs)
    for xi, p, v, l in zip(x, pct, values, limits):
        ax.text(xi, max(p, 0) + 4, f"{p:.2f}%\n({value_fmt.format(v)}/{value_fmt.format(l)})",
                ha="center", va="bottom", fontsize=fs, color=INK, linespacing=1.25)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 125)
    ax.set_ylabel(xlabel)
    ax.set_xlim(-0.6, len(labels) - 0.4)
    bare(ax, keep=("left", "bottom"))
    ax.grid(True, axis="y")
    ax.set_axisbelow(True)
    return ax


def bitfield(ax, fields, y0: float = 0.02, height: float = 0.085,
             colors=("blue", "teal", "amber", "green", "purple", "cyan"),
             fs: float | None = None, show_counts: bool = True):
    """fig01 idiom: draw the data layout as a colour strip aligned with the
    geometry above it. fields = [(label, nbits), ...]."""
    if fs is None:
        fs = plt.rcParams["font.size"] - 3.5
    total = float(sum(n for _, n in fields))
    x = 0.0
    for i, (label, nbits) in enumerate(fields):
        w = nbits / total
        col = C.get(colors[i % len(colors)], colors[i % len(colors)])
        ax.add_patch(Rectangle((x, y0), w, height, transform=ax.transAxes,
                               fc=col, ec="white", lw=1.2, clip_on=False, zorder=6))
        ax.text(x + w / 2, y0 + height / 2, label, transform=ax.transAxes,
                ha="center", va="center", color="white", fontsize=fs,
                linespacing=1.2, zorder=7)
        if show_counts:
            ax.text(x + w / 2, y0 + height + 0.028, f"{nbits} bit"
                    if nbits == 1 else f"{nbits} bits",
                    transform=ax.transAxes, ha="center", va="bottom",
                    color=INK, fontsize=fs - 1, zorder=7)
        x += w
    return ax



# --------------------------------------------------------------------------- #
# textbook primitives: what the report recipes do not cover
# --------------------------------------------------------------------------- #
SEQ = ["#f8fafc", "#dbeafe", "#bfdbfe", "#93c5fd", "#60a5fa", "#3b82f6",
       "#2563eb", "#1d4ed8"]


def seq_color(t: float, ramp=None):
    """Sequential single-hue colour for a value field: t in [0, 1] -> hex.
    Use it instead of a rainbow when a filled cell encodes a magnitude."""
    from matplotlib.colors import LinearSegmentedColormap, to_hex
    ramp = ramp or SEQ
    cmap = LinearSegmentedColormap.from_list("seq", ramp)
    return to_hex(cmap(float(min(max(t, 0.0), 1.0))))


def node(ax, xy, r: float = 0.45, label: str = "", double: bool = False,
         fc: str = "white", ec: str = None, lw: float = 1.8, fs: float = 12,
         color: str = None, zorder: int = 4):
    """Graph node. `double=True` draws the terminal-state double ring.
    In a panel whose aspect is not equal, use round_patch() instead."""
    from matplotlib.patches import Circle
    ec = ec or INK
    ax.add_patch(Circle(xy, r, fc=fc, ec=ec, lw=lw, zorder=zorder))
    if double:
        ax.add_patch(Circle(xy, r * 1.22, fc="none", ec=ec, lw=lw * 0.9,
                            zorder=zorder))
    if label:
        ax.text(xy[0], xy[1], label, ha="center", va="center", fontsize=fs,
                color=color or INK, zorder=zorder + 1)


def round_patch(ax, xy, r: float, **kw):
    """Circle that still renders round when the axes aspect is not equal:
    the height is corrected by the data-per-pixel ratio."""
    from matplotlib.patches import Ellipse
    ax.figure.canvas.draw()
    inv = ax.transData.inverted()
    x0, _ = inv.transform((0, 0))
    x1, _ = inv.transform((100, 0))
    _, y0 = inv.transform((0, 0))
    _, y1 = inv.transform((0, 100))
    h = 2 * r * abs(y1 - y0) / abs(x1 - x0)
    return Ellipse(xy, 2 * r, h, **kw)


def lanes(ax, x0, y0, rows: int, cols: int, sq: float, gap: float,
          fc="blue_f", ec="blue_d", lw: float = 0.9, row_gap: float = None):
    """Grid of small squares: execution lanes, a register file, a bitfield of
    instanced data. row_gap defaults to gap; rows grow upward."""
    from matplotlib.patches import Rectangle
    from matplotlib.colors import to_rgba
    row_gap = gap if row_gap is None else row_gap
    for r in range(rows):
        for c in range(cols):
            ax.add_patch(Rectangle((x0 + c * (sq + gap), y0 + r * (sq + row_gap)),
                                   sq, sq, fc=C.get(fc, fc), ec=C.get(ec, ec),
                                   lw=lw))


def cap_row(fig, axes, items, y: float = 0.050, fs: float = 11.0):
    """One caption baseline per figure. items = [(text, color), ...] in axes
    order. Use this instead of micro() when the panels mix axis-off
    schematics with plotted panels, whose xlabels sit at different heights."""
    for ax, (text, col) in zip(axes, items):
        box = ax.get_position()
        fig.text(box.x0 + box.width / 2, y, text, ha="center", va="bottom",
                 fontsize=fs, style="italic", color=_text_col(col))


def note_key(fig, text: str, y: float = 0.012, fs: float = 8.8,
             color: str = "#64748b"):
    """Symbol key, one grey line under the captions. A teaching figure has to
    decode its own notation; a report figure can lean on the prose."""
    fig.text(0.5, y, text, ha="center", va="bottom", fontsize=fs, color=color)


def bands(ax, split: float, top=1.0, labels=(("", "blue"), ("", "purple")),
          divider_lw: float = 1.0):
    """Split the y axis into two bands sharing one x axis, for two objects of
    different kind (bars = a value per action, curve = a density). Returns
    (map_lower, map_upper) so each object is scaled into its own band.
    Never put the two on one axis: a curve over bars reads as a fit."""
    lo, hi = ax.get_ylim()
    ax.axhline(split, color=RULE, lw=divider_lw, zorder=1)
    span_low, span_high = split - lo, hi - split

    def lower(v):
        return lo + v * span_low

    def upper(v):
        return split + v * span_high

    for (lab, col), ytxt in zip(labels, (hi - 0.18 * span_high,
                                         split - 0.18 * span_low)):
        if lab:
            ax.text(ax.get_xlim()[0] + 0.02 * (ax.get_xlim()[1] - ax.get_xlim()[0]),
                    ytxt, lab, ha="left", va="center", fontsize=9.5,
                    color=C.get(col, col))
    return lower, upper


def legend(ax, **kw):
    """Legend with the house frame (hairline, near-opaque, no fancy)."""
    kw.setdefault("loc", "best")
    kw.setdefault("framealpha", 0.95)
    return ax.legend(**kw)


# --------------------------------------------------------------------------- #
# rich-information visual primitives (illustrated cards, small-multiples, QA)
# --------------------------------------------------------------------------- #
def visual_node(ax, x: float, y: float, w: float, h: float, title: str,
                subtitle: str = "", color: str = "blue",
                header_frac: float = 0.23, footer_frac: float | None = None,
                pad_x: float = 0.06, pad_y: float = 0.05,
                title_fs: float = 10.0, sub_fs: float = 8.8,
                fc: str = "white", ec: str | None = None,
                header_fill: bool = True, lw: float = 1.6, zorder: int = 3):
    """Illustrated flowchart node: a framed card whose centre is a real
    matplotlib inset Axes for drawing a mini-figure (bars, curve, grid, stack),
    with only a short title header and optional compact formula/metric footer.
    Returns the inset Axes (tagged ``_is_visual_inset=True``)."""
    fill_key = f"{color}_f" if f"{color}_f" in C else "panel"
    edge_key = f"{color}_d" if f"{color}_d" in C else color
    edge_col = C.get(ec, ec) if ec else C.get(edge_key, INK)
    txt_col = C.get(edge_key, INK)

    if footer_frac is None:
        footer_frac = 0.19 if subtitle else 0.04

    # outer card
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=edge_col, lw=lw,
                           zorder=zorder))
    # tinted header band
    hh = h * header_frac
    if header_fill:
        ax.add_patch(Rectangle((x, y + h - hh), w, hh,
                               fc=C.get(fill_key, PANEL), ec=edge_col, lw=lw,
                               zorder=zorder + 0.5))
    ax.text(x + w / 2, y + h - hh / 2, title, ha="center", va="center",
            color=txt_col, fontsize=title_fs, zorder=zorder + 2)

    if subtitle:
        fh = h * footer_frac
        ax.text(x + w / 2, y + fh * 0.50, subtitle, ha="center", va="center",
                color=INK, fontsize=sub_fs, zorder=zorder + 2)

    # embedded mini-axes in data coordinates
    ix = x + w * pad_x
    iw = w * (1.0 - 2.0 * pad_x)
    iy = y + h * (footer_frac + pad_y * 0.6)
    ih = h * (1.0 - header_frac - footer_frac - 1.4 * pad_y)
    ax_mini = ax.inset_axes([ix, iy, iw, max(ih, 0.1 * h)],
                            transform=ax.transData, zorder=zorder + 1)
    ax_mini._is_visual_inset = True
    ax_mini.set_facecolor(PANEL)
    ax_mini.set_xticks([])
    ax_mini.set_yticks([])
    for name in ("top", "right", "left", "bottom"):
        ax_mini.spines[name].set_color(RULE)
        ax_mini.spines[name].set_linewidth(0.7)
    return ax_mini


def matrix_cell(ax, x: float, y: float, w: float, h: float, tag: str = "",
                color: str = "blue", tag_fs: float = 8.8,
                tag_frac: float = 0.24, pad_x: float = 0.06,
                pad_y: float = 0.06, fc: str = "#f8fafc",
                ec: str | None = None, lw: float = 0.9, zorder: int = 3):
    """Small-multiple visual comparison cell (replaces text tables):
    returns an inset Axes in the upper region and prints a short 2-5 word
    tag underneath."""
    edge_key = f"{color}_d" if f"{color}_d" in C else color
    txt_col = C.get(edge_key, INK)
    edge_col = C.get(ec, ec) if ec else RULE

    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=edge_col, lw=lw,
                           zorder=zorder))
    th = h * (tag_frac if tag else 0.05)
    if tag:
        ax.text(x + w / 2, y + th * 0.48, tag, ha="center", va="center",
                color=txt_col, fontsize=tag_fs, zorder=zorder + 2)

    ix = x + w * pad_x
    iw = w * (1.0 - 2.0 * pad_x)
    iy = y + th + h * pad_y * 0.4
    ih = h - th - h * pad_y * 1.4
    ax_mini = ax.inset_axes([ix, iy, iw, max(ih, 0.1 * h)],
                            transform=ax.transData, zorder=zorder + 1)
    ax_mini._is_visual_inset = True
    ax_mini.set_facecolor("white")
    ax_mini.set_xticks([])
    ax_mini.set_yticks([])
    for name in ("top", "right"):
        ax_mini.spines[name].set_visible(False)
    for name in ("left", "bottom"):
        ax_mini.spines[name].set_color(RULE)
        ax_mini.spines[name].set_linewidth(0.8)
    return ax_mini


def rule_badge(ax, xy, text: str, color: str = "ink", fs: float = 8.6,
               fc: str = "white", pad: float = 0.25, lw: float = 1.1,
               ha: str = "center", va: str = "center", zorder: int = 9):
    """Compact pill badge placed directly on a spatial feature (wall, step,
    terminal cell) so domain rules live on the geometry, not in prose."""
    col = C.get(f"{color}_d", C.get(color, color))
    return ax.text(xy[0], xy[1], text, ha=ha, va=va, color=col, fontsize=fs,
                   zorder=zorder,
                   bbox=dict(boxstyle=f"round,pad={pad}", fc=fc, ec=col, lw=lw))


def zoom_connect(fig, ax_src, xy_src, ax_dst, xy_dst, color: str = "ink",
                 lw: float = 1.1, ls: str = "--", alpha: float = 0.75):
    """Draw a cross-panel dashed connector from a macro detail in ax_src to
    a zoomed-in panel ax_dst using ConnectionPatch."""
    from matplotlib.patches import ConnectionPatch
    col = C.get(color, color)
    con = ConnectionPatch(xyA=xy_src, coordsA="data", axesA=ax_src,
                          xyB=xy_dst, coordsB="data", axesB=ax_dst,
                          color=col, lw=lw, ls=ls, alpha=alpha, zorder=8)
    fig.add_artist(con)
    return con


def _prose_word_count(text: str) -> int:
    """Count natural-language words outside $...$ math spans (each math span
    counts as 1 symbol token so equations are not penalised as prose; pure
    numeric ticks are excluded)."""
    import re
    stripped = re.sub(r"\$[^$]*\$", " MATH ", text.strip())
    tokens = []
    for t in re.split(r"\s+", stripped):
        if not t or t in ("·", "—", "-", "=", "|", "•"):
            continue
        if re.fullmatch(r"[+-]?\d+(?:\.\d+)?%?", t):
            continue
        tokens.append(t)
    return len(tokens)


def _contrast_ratio(rgb_fg, rgb_bg) -> float:
    def _lum(rgb):
        vals = []
        for c in rgb[:3]:
            vals.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
        return 0.2126 * vals[0] + 0.7152 * vals[1] + 0.0722 * vals[2]
    l1, l2 = _lum(rgb_fg), _lum(rgb_bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def _bg_under_text(ax, cx: float, cy: float):
    """Estimate background RGB under display point (cx, cy) from topmost patch."""
    from matplotlib.colors import to_rgba
    bg = to_rgba("white")
    ax_fc = ax.get_facecolor()
    if ax.patch.get_visible() and ax_fc[3] > 0:
        bg = ax_fc
    best_z = -1e9
    for p in ax.patches:
        if not p.get_visible():
            continue
        try:
            contains, _ = p.contains_point((cx, cy))
        except Exception:
            contains = False
        if contains and p.get_zorder() >= best_z:
            fc = p.get_facecolor()
            if len(fc) == 4 and fc[3] > 0.05:
                a = fc[3]
                bg = (a * fc[0] + (1 - a) * bg[0],
                      a * fc[1] + (1 - a) * bg[1],
                      a * fc[2] + (1 - a) * bg[2], 1.0)
                best_z = p.get_zorder()
    return bg[:3]


def audit(fig, name: str = "fig", *, max_words_per_panel: int = 35,
          max_words_per_label: int = 10, overlap_px: float = 16.0,
          min_contrast: float = 4.2, strict: bool = False) -> dict:
    """Automated quantitative QA & anti-prose check on a rendered Figure.

    Checks:
      1. Text-text overlaps (> overlap_px px^2)
      2. Text past canvas bounds
      3. Title & caption baseline alignment across top-level panels
      4. Circle patch aspect distortion (> 5%)
      5. Small-label WCAG contrast (< min_contrast for fs <= 10.5)
      6. Anti-prose telemetry: prose words per top-level panel & per label
      7. Unescaped LaTeX artifacts outside $...$ (e.g. '\\%')
    """
    import re
    from matplotlib.patches import Circle
    from matplotlib.colors import to_rgb

    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    W, H = fig.canvas.get_width_height()

    top_axes = [ax for ax in fig.axes if not getattr(ax, "_is_visual_inset", False)]

    # Map every visible text object to (owner_panel_idx_or_-1, text_obj, kind)
    entries = []
    for t in fig.texts:
        if t.get_visible() and t.get_text().strip():
            entries.append((-1, fig.axes[0] if fig.axes else None, t, "fig_text"))

    for p_idx, ax in enumerate(top_axes):
        all_sub = [ax] + [c for c in ax.child_axes if getattr(c, "_is_visual_inset", False)]
        for sub in all_sub:
            for t in sub.texts:
                if t.get_visible() and t.get_text().strip():
                    kind = "micro" if t.get_position()[1] < 0 and t.get_transform() == sub.transAxes else "label"
                    entries.append((p_idx, sub, t, kind))
            if sub.title.get_visible() and sub.title.get_text().strip():
                entries.append((p_idx, sub, sub.title, "title"))
            if sub.axison:
                for t in (sub.xaxis.label, sub.yaxis.label):
                    if t.get_visible() and t.get_text().strip():
                        entries.append((p_idx, sub, t, "axis_label"))
                for t in sub.get_xticklabels() + sub.get_yticklabels():
                    if t.get_visible() and t.get_text().strip():
                        entries.append((p_idx, sub, t, "tick"))
                if sub.get_legend() is not None:
                    for t in sub.get_legend().get_texts():
                        if t.get_visible() and t.get_text().strip():
                            entries.append((p_idx, sub, t, "legend"))

    # 1. Text-text overlaps & 2. Canvas bounds
    bboxes = [(p_idx, ax, t, kind, t.get_window_extent(r))
              for (p_idx, ax, t, kind) in entries]
    overlaps = []
    for i in range(len(bboxes)):
        for j in range(i + 1, len(bboxes)):
            a, b = bboxes[i][4], bboxes[j][4]
            ow = min(a.x1, b.x1) - max(a.x0, b.x0)
            oh = min(a.y1, b.y1) - max(a.y0, b.y0)
            if ow > 1 and oh > 1 and ow * oh > overlap_px:
                overlaps.append((round(ow * oh),
                                 bboxes[i][2].get_text().replace("\n", " ")[:28],
                                 bboxes[j][2].get_text().replace("\n", " ")[:28]))

    off_canvas = []
    panel_spill = []
    top_ax_bbs = {i: ax.get_window_extent(r) for i, ax in enumerate(top_axes)}
    tight_mode = plt.rcParams.get("savefig.bbox") == "tight"
    for p_idx, _, t, kind, bb in bboxes:
        if kind != "micro" and (bb.x0 < -2 or bb.x1 > W + 2 or (not tight_mode and (bb.y0 < -2 or bb.y1 > H + 2))):
            off_canvas.append((t.get_text().replace("\n", " ")[:28],
                               round(bb.x0), round(bb.x1 - W)))
        if kind == "label" and p_idx >= 0:
            ax_bb = top_ax_bbs[p_idx]
            if bb.x0 < ax_bb.x0 - 8 or bb.x1 > ax_bb.x1 + 8:
                panel_spill.append((p_idx, t.get_text().replace("\n", " ")[:28]))

    # 3. Title baseline spread
    title_y = [bb.y0 for (_, _, _, kind, bb) in bboxes if kind == "title"]
    title_spread = (max(title_y) - min(title_y)) if len(title_y) > 1 else 0.0

    # 4. Circle aspect check
    ovals = []
    for ax in fig.axes:
        for p in ax.patches:
            if isinstance(p, Circle) and p.get_visible():
                bb = p.get_window_extent(r)
                if max(bb.width, bb.height) > 2:
                    dev = abs(bb.width - bb.height) / max(bb.width, bb.height)
                    if dev > 0.05:
                        ovals.append((round(bb.width, 1), round(bb.height, 1)))

    # 5. Contrast check on small labels
    low_contrast = []
    for _, ax, t, kind, bb in bboxes:
        if kind in ("tick",) or ax is None:
            continue
        if t.get_fontsize() <= 10.5:
            bbox_p = t.get_bbox_patch()
            if bbox_p is not None and bbox_p.get_facecolor()[3] > 0.1:
                fc_b = bbox_p.get_facecolor()
                bg = (fc_b[0], fc_b[1], fc_b[2])
            else:
                cx, cy = (bb.x0 + bb.x1) / 2, (bb.y0 + bb.y1) / 2
                bg = _bg_under_text(ax, cx, cy)
            fg = to_rgb(t.get_color())
            cr = _contrast_ratio(fg, bg)
            if cr < min_contrast:
                low_contrast.append((round(cr, 2), t.get_fontsize(),
                                     t.get_text().replace("\n", " ")[:28]))

    # 6. Anti-prose telemetry & 7. Literal LaTeX artifact check
    panel_words = {i: 0 for i in range(len(top_axes))}
    long_labels = []
    latex_glitches = []
    for p_idx, _, t, kind, _ in bboxes:
        txt = t.get_text()
        outside_math = re.sub(r"\$[^$]*\$", " ", txt)
        if re.search(r"\\[%&_#]|\\text\{|\\mathrm\{", outside_math):
            latex_glitches.append(txt.replace("\n", " ")[:36])
        if kind in ("label", "legend", "axis_label") and p_idx >= 0:
            wc = _prose_word_count(txt)
            panel_words[p_idx] += wc
            if kind == "label" and wc > max_words_per_label:
                long_labels.append((p_idx, wc, txt.replace("\n", " ")[:40]))

    prose_panels = {k: v for k, v in panel_words.items() if v > max_words_per_panel}

    issues = []
    if overlaps:
        issues.append(f"{len(overlaps)} text overlap(s)")
    if off_canvas:
        issues.append(f"{len(off_canvas)} off-canvas text(s)")
    if panel_spill:
        issues.append(f"{len(panel_spill)} label(s) spilling outside panel")
    if title_spread > 3.0:
        issues.append(f"title baseline spread {title_spread:.1f} px")
    if ovals:
        issues.append(f"{len(ovals)} distorted Circle(s)")
    if low_contrast:
        issues.append(f"{len(low_contrast)} low-contrast small label(s)")
    if prose_panels:
        issues.append(f"prose overload in panel(s) {prose_panels}")
    if long_labels:
        issues.append(f"{len(long_labels)} prose label(s) > {max_words_per_label} words")
    if latex_glitches:
        issues.append(f"{len(latex_glitches)} literal LaTeX glitch(es)")

    print(f"\n=== audit({name}) [{'PASS' if not issues else 'FAIL'}] ===")
    print(f"  canvas {W}x{H} px | panel prose words: {panel_words}")
    if overlaps:
        print(f"  overlaps: {overlaps[:6]}")
    if off_canvas:
        print(f"  off_canvas: {off_canvas[:6]}")
    if panel_spill:
        print(f"  panel_spill: {panel_spill[:6]}")
    if title_spread > 3.0:
        print(f"  title_spread: {title_spread:.1f} px")
    if ovals:
        print(f"  ovals (w,h px): {ovals[:6]}")
    if low_contrast:
        print(f"  low_contrast (<{min_contrast}:1): {low_contrast[:6]}")
    if long_labels:
        print(f"  long_labels: {long_labels[:6]}")
    if latex_glitches:
        print(f"  latex_glitches: {latex_glitches[:6]}")

    res = {
        "pass": len(issues) == 0,
        "issues": issues,
        "panel_words": panel_words,
        "overlaps": overlaps,
        "off_canvas": off_canvas,
        "title_spread": title_spread,
        "ovals": ovals,
        "low_contrast": low_contrast,
        "long_labels": long_labels,
        "latex_glitches": latex_glitches,
    }
    if strict and issues:
        raise AssertionError(f"audit({name}) failed: {'; '.join(issues)}")
    return res
