"""Entry 67 overshoot figure for the README and reports, drawn from the saved scan.

Run: uv run --group figures python explore/make_overshoot_figure.py

Reads explore/nb/e67_overshoot.npz and .json (written by explore/nb/e67_overshoot_map.py) and
re-simulates nothing; only the TT-minus-model differences are formed here. Writes
figures/overshoot.png (README) and figures/overshoot.pdf (paper). The poster keeps its own
version, make_poster_figs.py f7.
"""

from __future__ import annotations

import json
from pathlib import Path

import cvdkit
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
import qoraplot
from matplotlib.legend_handler import HandlerTuple
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "explore" / "nb"
OUT = ROOT / "figures"
SMALL = 7  # pt, the smallest text; still readable when GitHub scales the PNG to its page width
CASE_MARKERS = {"A": "o", "B": "s", "C": "^"}
CHECK_MARKERS = {0.2: "x", 1.0: "D", 3.0: "v"}
TITLES = {"A": "A: grows to steady", "B": "B: overshoots", "C": "C: overshoots, steady near zero"}
HALO = [pe.withStroke(linewidth=2.0, foreground="black")]


def sci(v):
    m, e = f"{v:.1e}".split("e")
    return rf"{m}$\times10^{{{int(e)}}}$"


def scan_map(ax, cbar_fig, data, summary, colors):
    im = ax.pcolormesh(
        data["S"], data["rise"], data["excess"], shading="nearest", cmap="cividis", vmin=0
    )
    cbar_fig.colorbar(im, ax=ax, pad=0.01, label=r"overshoot $\Delta I/I_0$ (reduced model)")
    cs = ax.contour(
        data["S"],
        data["rise"],
        data["excess"],
        levels=[0.1, 0.3, 0.5],
        colors="white",
        linewidths=0.6,
    )
    # left branches and the right-hand lobe, which is otherwise unlabelled
    ax.clabel(
        cs,
        fmt="%.1f",
        fontsize=SMALL,
        manual=[(2.45, 2.7), (2.9, 2.7), (3.3, 2.7), (5.6, 1.62), (5.7, 2.9)],
    )
    checks = summary["checks"]
    ax.plot(
        [c["S"] for c in checks],
        [c["rise"] for c in checks],
        "+",
        color="white",
        ms=6,
        mew=1.2,
        ls="none",
        path_effects=HALO,
    )
    for case in summary["cases"]:
        L = case["label"]
        ax.plot(
            case["S"], case["rise"], CASE_MARKERS[L], color=colors[L], mec="white", mew=0.8, ms=6
        )
        ax.annotate(
            L,
            (case["S"], case["rise"]),
            xytext=(4, 4),
            textcoords="offset points",
            color="white",
            fontweight="bold",
            path_effects=HALO,
        )
    top = summary["map_maximum"]
    ax.plot(top["S"], top["rise"], "*", color="white", mec="black", mew=0.5, ms=9, clip_on=False)
    ax.annotate(
        f"largest in scan, {top['excess']:.3f}:\non the edge, still rising",
        (top["S"], top["rise"]),
        xytext=(0.7, 3.55),
        textcoords="data",
        color="white",
        fontsize=SMALL,
        path_effects=HALO,
        arrowprops={"arrowstyle": "-", "lw": 0.6, "color": "white"},
    )
    ax.set(xlabel=r"final sound amplitude $S$", ylabel=r"rise time $T_\mathrm{rise}/t_\mathrm{tr}$")
    ax.set_title("Overshoot over 11,211 conditions (+: full-TT check)", loc="left")


def check_errors(ax, summary):
    for rise, marker in CHECK_MARKERS.items():
        rows = [c for c in summary["checks"] if c["rise"] == rise]
        x = np.arange(len(rows)) + (list(CHECK_MARKERS).index(rise) - 1) * 0.22
        ax.plot(
            x,
            [c["max_trace_error"] * 1e5 for c in rows],
            marker,
            color="black",
            ls="none",
            ms=4,
            label=rf"trace, $T_\mathrm{{rise}}={rise:g}\,t_\mathrm{{tr}}$",
        )
        ax.plot(
            x,
            [c["excess_error"] * 1e5 for c in rows],
            marker,
            color="0.6",
            ls="none",
            ms=3,
        )
    ax.set_xticks(range(4), [f"{s:g}" for s in (1.5, 3.0, 3.85, 5.0)])
    ax.set(
        xlabel=r"$S$",
        ylabel=r"$|I_\mathrm{TT} - I_\mathrm{model}|/I_0$ ($10^{-5}$)",
        ylim=(-0.4, 15),
    )
    ax.set_title("12 full-TT checks", loc="left")
    handles, labels = ax.get_legend_handles_labels()
    handles.append(Line2D([], [], color="0.6", marker="D", ls="none", ms=3))
    labels.append(r"$\Delta I$, same $T_\mathrm{rise}$ shapes")
    ax.legend(handles, labels, fontsize=SMALL, loc="upper left", handlelength=1.0, ncols=1)


def traces(lower, data, summary, colors):
    grid = lower.add_gridspec(2, 3, height_ratios=[1.0, 0.62])
    top, bottom = [], []
    for k, case in enumerate(summary["cases"]):
        L = case["label"]
        a = lower.add_subplot(grid[0, k], sharey=top[0] if top else None)
        r = lower.add_subplot(grid[1, k], sharex=a, sharey=bottom[0] if bottom else None)
        t, model = data[f"{L}_t"], data[f"{L}_I"]
        tt_t, tt = data[f"{L}_tt_t"], data[f"{L}_tt_I"]
        a.plot(t, model, color=colors[L], ls="-", marker="none")
        a.plot(tt_t[::2], tt[::2], CASE_MARKERS[L], color=colors[L], mfc="none", ls="none", ms=3.5)
        a.axhline(case["steady"], color="0.35", ls="--", lw=0.8)
        a.set_title(
            TITLES[L]
            + "\n"
            + rf"$S={case['S']:g}$, $T_\mathrm{{rise}}={case['rise']:g}\,t_\mathrm{{tr}}$",
            loc="left",
            fontsize=SMALL + 1,
        )
        peak, steady = case["peak"], case["steady"]
        if peak - steady < 1e-9:
            values, where = f"peak = steady = {peak:.3f}", (0.97, 0.06, "right", "bottom")
        elif steady < 0.01:
            values, where = f"peak {peak:.3f}\nsteady {sci(steady)}", (0.97, 0.95, "right", "top")
        else:
            values, where = f"peak {peak:.3f}\nsteady {steady:.3f}", (0.97, 0.06, "right", "bottom")
        a.text(
            where[0],
            where[1],
            values,
            transform=a.transAxes,
            ha=where[2],
            va=where[3],
            fontsize=SMALL,
        )
        if L == "B":  # the quantity the map shows
            i = int(np.argmax(model))
            a.annotate(
                "",
                xy=(t[i], peak),
                xytext=(t[i], steady),
                arrowprops={
                    "arrowstyle": "<|-|>",
                    "lw": 0.8,
                    "color": "black",
                    "shrinkA": 0,
                    "shrinkB": 0,
                    "mutation_scale": 7,
                },
            )
            a.text(t[i] + 0.05, (peak + steady) / 2, r"$\Delta I$", fontsize=SMALL + 1)
        # the TT times are every tenth model time, so the difference needs no interpolation
        r.semilogy(tt_t, np.abs(tt - model[::10]), color=colors[L], marker="none")
        r.axhline(case["tt_refinement_max_change"], color="0.35", ls=":", lw=0.9)
        r.set_xlabel(r"time $t/t_\mathrm{tr}$")
        a.tick_params(labelbottom=False)
        if k:
            a.tick_params(labelleft=False)
            r.tick_params(labelleft=False)
        top.append(a)
        bottom.append(r)
    top[0].set_ylabel(r"$I_1(\eta=q)/I_0$, phase-averaged")
    top[0].set_ylim(0, 0.68)
    top[0].legend(
        [
            Line2D([], [], color="0.35"),
            tuple(
                Line2D([], [], color="0.35", marker=m, mfc="none", ls="none", ms=3.5)
                for m in CASE_MARKERS.values()
            ),
            Line2D([], [], color="0.35", ls="--", lw=0.8),
        ],
        ["reduced model", "full TT", "steady value"],
        handler_map={tuple: HandlerTuple(ndivide=None)},
        loc="upper left",
        bbox_to_anchor=(0, 0.86),
        fontsize=SMALL,
        handlelength=2.2,
    )
    bottom[0].set_ylabel(r"$|I_\mathrm{TT} - I_\mathrm{model}|/I_0$")
    bottom[0].set_ylim(1e-9, 3e-4)
    bottom[0].text(
        0.97,
        0.06,
        "dotted: TT change\nunder refinement",
        transform=bottom[0].transAxes,
        ha="right",
        fontsize=SMALL,
    )
    return top[0], bottom[0]


def draw(data, summary):
    colors = dict(zip("ABC", cvdkit.pick(3).colors, strict=True))
    fig = plt.figure(figsize=(qoraplot.WIDTHS["double"], 6.9), layout="constrained")
    # separate subfigures, so the map's colorbar does not shift the trace columns below it
    upper, lower = fig.subfigures(2, 1, height_ratios=[1.45, 1.8])
    ax, d = upper.subplots(1, 2, width_ratios=[2.3, 1])
    scan_map(ax, upper, data, summary, colors)
    check_errors(d, summary)
    first_trace, first_residual = traces(lower, data, summary, colors)
    for panel, label in zip((ax, d, first_trace, first_residual), "abcd", strict=True):
        qoraplot.panel_label(panel, label)
    return fig


def main():
    data = np.load(NB / "e67_overshoot.npz")
    summary = json.loads((NB / "e67_overshoot.json").read_text(encoding="utf-8"))
    with qoraplot.style("house", "paper"):
        fig = draw(data, summary)
        collisions = cvdkit.check(fig)
        if collisions:
            raise SystemExit(f"colour-vision check failed: {collisions}")
        OUT.mkdir(exist_ok=True)
        fig.savefig(OUT / "overshoot.pdf")
        fig.savefig(OUT / "overshoot.png", dpi=220)
    print("wrote", OUT / "overshoot.png", OUT / "overshoot.pdf")


if __name__ == "__main__":
    main()
