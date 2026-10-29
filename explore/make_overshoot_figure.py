"""Entry 67 overshoot figure for the README and reports, drawn from the saved scan.

Run: uv run --group figures python explore/make_overshoot_figure.py

Reads explore/nb/e67_overshoot.npz and .json (written by explore/nb/e67_overshoot_map.py) and
recomputes nothing. Writes figures/overshoot.png (README) and figures/overshoot.pdf (paper).
The poster keeps its own version, make_poster_figs.py f7.
"""

from __future__ import annotations

import json
from pathlib import Path

import cvdkit
import matplotlib.pyplot as plt
import numpy as np
import qoraplot

ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "explore" / "nb"
OUT = ROOT / "figures"
RISES = (0.2, 1.0, 3.0)
TITLES = {"A": "A: grows to steady", "B": "B: overshoots", "C": "C: overshoots, steady near zero"}


def sci(v):
    m, e = f"{v:.1e}".split("e")
    return rf"{m}$\times10^{{{int(e)}}}$"


def draw(data, summary):
    picked = cvdkit.pick(3)
    colors = dict(zip("ABC", picked.colors, strict=True))
    markers = dict(zip("ABC", ("o", "s", "^"), strict=True))
    fig = plt.figure(figsize=(qoraplot.WIDTHS["double"], 6.6), layout="constrained")
    # separate subfigures, so the map's colorbar does not shift the trace columns below it
    upper, lower = fig.subfigures(2, 1, height_ratios=[1.45, 1.75])
    ax, d = upper.subplots(1, 2, width_ratios=[2.3, 1])
    grid = lower.add_gridspec(2, 3, height_ratios=[1.0, 0.62])
    im = ax.pcolormesh(
        data["S"], data["rise"], data["excess"], shading="nearest", cmap="cividis", vmin=0
    )
    upper.colorbar(im, ax=ax, pad=0.01, label=r"overshoot $\Delta I$ (reduced model)")
    cs = ax.contour(
        data["S"],
        data["rise"],
        data["excess"],
        levels=[0.1, 0.3, 0.5],
        colors="white",
        linewidths=0.6,
    )
    ax.clabel(cs, fmt="%.1f", fontsize=6)
    checks = summary["checks"]
    ax.plot(
        [c["S"] for c in checks],
        [c["rise"] for c in checks],
        "+",
        color="white",
        ms=5,
        mew=1.0,
        ls="none",
    )
    for case in summary["cases"]:
        L = case["label"]
        ax.plot(case["S"], case["rise"], markers[L], color=colors[L], mec="black", mew=0.6, ms=6)
        ax.annotate(
            L,
            (case["S"], case["rise"]),
            xytext=(4, 4),
            textcoords="offset points",
            color="white",
            fontweight="bold",
        )
    top = summary["map_maximum"]
    ax.plot(top["S"], top["rise"], "*", color="white", mec="black", mew=0.5, ms=9, clip_on=False)
    ax.annotate(
        f"max {top['excess']:.3f}\n(edge of scan)",
        (top["S"], top["rise"]),
        xytext=(10, -22),
        textcoords="offset points",
        color="white",
        fontsize=6.5,
    )
    ax.set(xlabel=r"final sound amplitude $S$", ylabel=r"rise time $T_\mathrm{rise}/t_\mathrm{tr}$")
    ax.set_title("Overshoot over 11,211 conditions (reduced model); + full-TT checks", loc="left")
    qoraplot.panel_label(ax, "a")

    traces, residuals = [], []
    for k, case in enumerate(summary["cases"]):
        L = case["label"]
        a = lower.add_subplot(grid[0, k], sharey=traces[0] if traces else None)
        r = lower.add_subplot(grid[1, k], sharex=a, sharey=residuals[0] if residuals else None)
        t, model = data[f"{L}_t"], data[f"{L}_I"]
        tt_t, tt = data[f"{L}_tt_t"], data[f"{L}_tt_I"]
        a.plot(t, model, color=colors[L], ls="-", marker="none", label="reduced model")
        a.plot(
            tt_t[::2],
            tt[::2],
            markers[L],
            color=colors[L],
            mfc="none",
            ls="none",
            ms=3.5,
            label="full TT",
        )
        a.axhline(case["steady"], color="0.35", ls="--", lw=0.8, label="steady value")
        a.set_title(
            TITLES[L]
            + "\n"
            + rf"$S={case['S']:g}$, $T_\mathrm{{rise}}={case['rise']:g}\,t_\mathrm{{tr}}$",
            loc="left",
            fontsize=7,
        )
        if L == "C":
            a.annotate(
                f"steady {sci(case['steady'])}",
                (t[-1], case["steady"]),
                xytext=(-2, 22),
                textcoords="offset points",
                ha="right",
                fontsize=6.5,
                arrowprops={"arrowstyle": "-", "lw": 0.5, "color": "0.35"},
            )
        # the TT times are every tenth model time, so the residual needs no interpolation
        r.semilogy(tt_t, np.abs(tt - model[::10]) + 1e-12, color=colors[L], marker="none")
        r.axhline(case["tt_refinement_max_change"], color="0.35", ls=":", lw=0.8)
        r.set_xlabel(r"time $t/t_\mathrm{tr}$")
        a.tick_params(labelbottom=False)
        if k:
            a.tick_params(labelleft=False)
            r.tick_params(labelleft=False)
        traces.append(a)
        residuals.append(r)
    traces[0].set_ylabel(r"satellite intensity $I_1/I_0$")
    traces[0].set_ylim(0, 0.68)
    traces[0].legend(loc="upper left", bbox_to_anchor=(0, 0.86), fontsize=6, handlelength=1.6)
    residuals[0].set_ylabel(r"|TT $-$ model|")
    residuals[0].set_ylim(1e-9, 3e-4)
    residuals[0].text(
        0.03,
        0.9,
        "dotted: TT change under refinement",
        transform=residuals[0].transAxes,
        fontsize=5.5,
        va="top",
    )
    qoraplot.panel_label(traces[0], "b")
    qoraplot.panel_label(residuals[0], "c")

    for j, rise in enumerate(RISES):
        rows = [c for c in summary["checks"] if c["rise"] == rise]
        x = np.arange(len(rows)) + (j - 1) * 0.22
        d.semilogy(
            x,
            [c["max_trace_error"] for c in rows],
            ("o", "s", "^")[j],
            color="black",
            mfc="black",
            ls="none",
            ms=3.5,
            label=rf"$T_\mathrm{{rise}}={rise:g}$",
        )
    d.set_xticks(range(4), [f"{s:g}" for s in (1.5, 3.0, 3.85, 5.0)])
    d.set(xlabel=r"$S$", ylabel=r"max |TT $-$ model| over trace", ylim=(1e-5, 2e-4))
    d.set_title("12 full-TT checks", loc="left")
    d.legend(fontsize=5.5, loc="upper left", handlelength=1.0)
    qoraplot.panel_label(d, "d")
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
