"""Poster-only figures, drawn at print size for one A0 column. Run: python explore/make_poster_figs.py [--iqms] [f0 ...]

Width FIG_W is the inner width of a poster card (poster/build.py SPEC), so a font size here is the
printed size. Panels reuse the notebook figure code; nothing is recomputed differently.

Notation is the poster's: physical depth z, time t, detuning beta (1/m) in units of the acoustic
wave vector K, Pendelloesung length Lambda_P, and times in units of a named physical time (t_tr or
tau_n). The solver's scaled variables (eta, q, zeta, t~) do not appear on an axis.

f0  schematic: Laue slab, acoustic front filling the crystal, incident / transmitted / satellite beams
f1  formation law against full TT on the axis t / tau_n, Laue and Bragg (make_poster_figure; Entries 1, 9)
f2  time-resolved rocking curve near n = 1 and its centre cut        (make_map_figure.compute; Entries 22, 23)
f3  path memory: transient-only satellite, up vs down a pulse       (make_memory_figure.panel_a/b; Entries 28, 30)
f4  population error of the independent-channel picture vs R        (make_phase_figure.merged; Entry 54)
f5  outlook: Fourier weight / kinematic law (Entry 59, e58 data) and the satellite weight of the
    first-order forms against full TT (Entry 64, e64_sw.json); reads stored results only
f6  introductory Bessel coupling weights |J_n(S)| for a sinusoidal grating
f7  linear-ramp overshoot map and three TT-checked traces (Entry 67)
f8  kinematic satellites: lattice planes without and with a shear wave, and J_n(S)^2 by order
f9  symmetric Laue and Bragg geometry: h, the acoustic polarisation that couples, boundary conditions
f10 steady sidebands against thickness: closed forms, kinematic Bessel law and full TT (Entries 1, 9)
f11 i-QMS: the closed-form first sideband against time after a step onset, Si (Entries 1, 9)
f12 i-QMS background: Bessel weights against u0, and the surface-acoustic-wave
    satellites of Vadilonga et al. 2017 (J. Appl. Cryst. 50, 525, CC BY), points read from its Fig. 6
f13 i-QMS: the Laue onset schematic of the October talk (slide 2), redrawn, and the rocking curve
    of a thin Si crystal filled with sound, S = 1.5 (own RK4)
f16 i-QMS: first sideband |D_h(z)|^2 against depth and time after a step onset, Laue, Si (own RK4 sweep)

The i-QMS figures (--iqms) use the mplume "box" style at poster size (closed frame, inward major and
minor ticks, no grid) and its a0 context (print-size type), mplume main at 4c06415 (the a0
context is not yet in a release): `uv run --with "mplume @ git+https://github.com/NaNIsaac/mplume@4c064154f8f0ff94f6c6dd300266b68a34759333"
python explore/make_poster_figs.py --iqms ...`.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "explore"))
sys.path.insert(0, str(ROOT / "src"))

from tratt.core import required_nz, rocking  # noqa: E402
from tratt.drive import Drive  # noqa: E402

OUT = ROOT / "figures" / "poster"
for _f in sorted((ROOT / "poster" / "fonts").glob("*.ttf")):
    mpl.font_manager.fontManager.addfont(str(_f))
# Same face as poster/build.py: Arial where installed (the lab posters use it), else DejaVu Sans.
FONT = ["Arial", "DejaVu Sans"]

FIG_W = 14.4  # inches = poster card inner width (~366 mm)
INTRO_W = 12.5  # inches = left column of the introduction band (~317 mm)
F1_H, F7_H, F4_H = 5.7, 7.2, 4.6  # figure heights (inches), set by the bands they sit in
BIG, SMALL = 26, 23  # printed pt; smallest label 21 pt (SMALL - 2), readable at ~1.5 m on A0
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
# The i-QMS poster (--iqms) draws the same figures into figures/poster/iqms/ with the poster's one
# blue (its heading colour), black labels and "sideband" for "satellite"; the KPS set stays as is.
IQMS = False
LABEL = BLUE  # colour of the acoustic-wave labels in f9
TERM = "satellite"


def use_iqms():
    global IQMS, OUT, BLUE, LABEL, TERM, F1_H, F7_H, F4_H
    IQMS, OUT, BLUE, LABEL, TERM = True, OUT / "iqms", "#1f4e8c", INK, "sideband"
    F1_H, F7_H, F4_H = 5.2, 4.6, 3.8  # f1 key inside the axes, f7 map only


def style():
    mpl.rcParams.update(
        {
            "font.size": BIG,
            "axes.titlesize": BIG,
            "axes.labelsize": BIG,
            "xtick.labelsize": SMALL,
            "ytick.labelsize": SMALL,
            "legend.fontsize": SMALL,
            "lines.linewidth": 3.2,
            "lines.markersize": 10,
            "axes.linewidth": 1.4,
            "xtick.major.width": 1.4,
            "ytick.major.width": 1.4,
            "xtick.major.size": 7,
            "ytick.major.size": 7,
            "axes.titlepad": 12,
            "axes.edgecolor": INK2,
            "axes.labelcolor": INK,
            "text.color": INK,
            "xtick.color": INK2,
            "ytick.color": INK2,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.facecolor": "white",
            # Opaque: the README shows these figures, and on a dark page dark text on a clear
            # background cannot be read.
            "savefig.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.dpi": 200,
            # Text in the poster's own face; math in STIX, the same pairing poster/build.py uses, so
            # an axis label and a panel equation are set identically. An all-Plex math fontset has no
            # \cdot and no \sim and falls back to DejaVu for them, and its \int is a text-sized glyph.
            "font.family": FONT,
            "mathtext.fontset": "stix",
        }
    )
    if IQMS:
        import mplume as mp

        # "box" frame with mplume's a0 context (print-size type and ticks); here only the faces
        # the poster uses, black frame and ticks, and black-edged markers.
        mp.use(
            "box",
            "a0",
            rc={
                "font.family": FONT,
                "mathtext.fontset": "stix",
                "lines.markeredgecolor": INK,
                "lines.markeredgewidth": 1.3,
                "axes.edgecolor": INK,
                "xtick.color": INK,
                "ytick.color": INK,
                "savefig.dpi": 200,
            },
        )


def finish(fig, ax, name):
    for a in np.atleast_1d(ax):
        if not IQMS:
            a.grid(color=GRID, lw=1.0)
            a.set_axisbelow(True)
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.png")
    print("wrote", OUT / f"{name}.png")


def f0():
    """Entry snapshot for half a panel width: Laue slab with depth z running left to right.

    The profile inside the slab is `Drive.phi(t)` sampled in depth, and the curve on the right is
    a real `rocking()` of that same snapshot, turned on its side. The entrance face is vertical, so
    h (in the surface plane, symmetric Laue) is vertical and the drawn transverse wiggle is the shear
    displacement u parallel to h. D0 leaves along the incident direction and Dh is deflected by h.
    """
    style()
    LAB, KEY = BIG, BIG + 4
    alpha, S, alpha_ac, t = 0.6, 1.5, 5.0, 0.62
    d = Drive(S=S, alpha_ac=alpha_ac)

    fig, (ax, axr) = plt.subplots(
        1,
        2,
        figsize=(FIG_W, 0.31 * FIG_W),
        constrained_layout=True,
        gridspec_kw=dict(width_ratios=[2.6, 1.0], wspace=0.0),
    )

    ax.set(xlim=(-3.6, 10.0), ylim=(-0.6, 10.6))
    ax.axis("off")
    x0, x1, y0, y1 = 0.0, 6.0, 2.1, 8.1
    xf = x0 + t * (x1 - x0)
    ymid = 0.5 * (y0 + y1)

    ax.add_patch(plt.Rectangle((x0, y0), x1 - x0, y1 - y0, fc="white", ec=INK2, lw=1.6, zorder=1))
    zz = np.linspace(0.0, 1.0, 1200)
    phi = d.phi(t)(zz)
    amp = 0.33 * (y1 - y0) / max(abs(phi).max(), 1e-9)
    inside = zz <= t
    ax.plot(x0 + zz[inside] * (x1 - x0), ymid + amp * phi[inside], color=BLUE, lw=2.8, zorder=3)
    ax.plot([xf, xf], [y0, y1], color=BLUE, lw=2.2, ls=(0, (4, 3)), zorder=4)
    ax.annotate(
        "",
        xy=(xf + 1.2, y1 + 0.6),
        xytext=(xf, y1 + 0.6),
        arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.2, mutation_scale=22),
    )
    ax.text(xf + 1.35, y1 + 0.6, r"$v_s$", color=BLUE, va="center", fontsize=KEY)
    ax.text(xf, y1 + 1.3, "wavefront", color=BLUE, ha="center", va="bottom", fontsize=LAB)
    ax.text(
        0.5 * (x0 + xf),
        y1 + 0.35,
        r"shear wave, $u\parallel h$",
        color=BLUE,
        ha="center",
        va="bottom",
        fontsize=LAB - 2,
    )
    ax.text(0.5 * (xf + x1), ymid, r"$u=0$", color=INK2, ha="center", va="center", fontsize=LAB)

    ty = y0 + 0.5 * (y1 - y0)
    ax.add_patch(plt.Rectangle((x0 - 0.4, y0), 0.4, ty - y0, fc=INK2, ec="none", zorder=2))
    ax.text(
        x0 - 0.55,
        0.5 * (y0 + ty),
        "transducer",
        ha="right",
        va="center",
        fontsize=LAB - 2,
        color=INK2,
    )

    # depth axis and the displaced depth on one row
    yd = y0 - 0.75
    ax.annotate(
        "",
        xy=(x1 + 0.9, yd),
        xytext=(x0, yd),
        arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.4, mutation_scale=16),
    )
    for x, lab in ((x0, "$0$"), (x1, "$L$")):
        ax.plot([x, x], [yd - 0.2, yd + 0.2], color=INK2, lw=1.2)
        ax.text(x, yd - 0.35, lab, ha="center", va="top", fontsize=LAB, color=INK2)
    ax.text(x1 + 1.05, yd, "$z$", ha="left", va="center", fontsize=KEY, color=INK2)
    ax.plot([x0, xf], [yd, yd], color=BLUE, lw=3.4, solid_capstyle="butt")
    ax.text(0.5 * (x0 + xf), yd - 0.35, r"$v_s t$", ha="center", va="top", fontsize=LAB, color=BLUE)

    # incident beam in above the transducer; D0 keeps its direction, Dh is turned by h
    dx, dy = 2.6, -1.45
    ax.annotate(
        "",
        xy=(x0, ymid + 1.5),
        xytext=(x0 - dx, ymid + 1.5 - dy),
        arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.8, mutation_scale=24),
        zorder=5,
    )
    ax.text(x0 - dx - 0.2, ymid + 1.5 - dy + 0.35, "X-ray", fontsize=KEY, color=INK)
    ex, ey = x1, ymid
    ax.annotate(
        "",
        xy=(ex + dx, ey + dy),
        xytext=(ex, ey),
        arrowprops=dict(arrowstyle="-|>", color=INK2, lw=2.4, mutation_scale=22),
    )
    ax.text(ex + dx + 0.15, ey + dy, r"$D_0$", va="center", fontsize=KEY, color=INK2)
    ax.annotate(
        "",
        xy=(ex + dx, ey - dy),
        xytext=(ex, ey),
        arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=3.0, mutation_scale=22),
    )
    ax.text(ex + dx + 0.15, ey - dy, r"$D_h$", va="center", fontsize=KEY, color=ORANGE)
    hx = x1 + 1.45
    ax.annotate(
        "",
        xy=(hx, ymid + 1.0),
        xytext=(hx, ymid - 1.0),
        arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.0, mutation_scale=18),
    )
    ax.text(hx + 0.2, ymid, r"$h$", va="center", fontsize=KEY, color=INK)

    eta = np.linspace(-2.6 * d.q, 2.6 * d.q, 4001)
    intensity = rocking(alpha, eta, phi=d.phi(t), n_z=required_nz(alpha, alpha_ac))
    axr.plot(intensity, eta / d.q, color=ORANGE, lw=2.2)
    axr.set(
        xlim=(0, 1.6 * intensity.max()),
        ylim=(-2.75, 2.75),
        xticks=[0, 0.5, 1],
        yticks=[-2, -1, 0, 1, 2],
    )
    axr.set_xlabel(r"$I_h$ at time $t$", fontsize=LAB, labelpad=2)
    axr.set_ylabel(r"detuning $\beta/K$", fontsize=LAB, labelpad=0)
    axr.tick_params(labelsize=LAB - 2, length=5)
    for s in ("top", "right"):
        axr.spines[s].set_visible(False)
    axr.grid(False)
    for n in (0, 1, 2):
        axr.annotate(
            f"$n={n}$",
            (float(np.interp(n * d.q, eta, intensity)), n),
            fontsize=LAB - 2,
            color=ORANGE,
            va="center",
            xytext=(6, 0),
            textcoords="offset points",
        )

    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "f0_scheme.png", dpi=300)
    print("wrote", OUT / "f0_scheme.png", f"(rocking-curve max {intensity.max():.3f})")


def f1():
    """Same cases, times and solver call as make_poster_figure.collapse (Entries 1, 9); the TT
    points are cached in explore/nb/poster_f1_points.npz so a restyle does not rerun them."""
    import make_poster_figure as M
    from scipy.special import jv

    style()
    cache = ROOT / "explore" / "nb" / "poster_f1_points.npz"
    t = np.linspace(0.0, 1.0, 61) + M.OFF
    if cache.exists():
        d = np.load(cache)
        laue, bragg = d["laue"], d["bragg"]
    else:
        laue = np.array([M.centre(a, S, n, t, "laue") for S, a, n in M.CASES])
        bragg = np.array([M.centre(a, S, n, t, "bragg") for S, a, n in M.CASES])
        np.savez(cache, t=t, cases=np.array(M.CASES), laue=laue, bragg=bragg)
    row = SMALL * 1.6 / 72 / F1_H  # one key row, as a fraction of the figure height
    key = 0.0 if IQMS else 3 * row + 0.02  # key strip under both panels: 2 case rows + the law
    fig, ax = plt.subplots(1, 2, figsize=(FIG_W, F1_H), constrained_layout=True, sharey=True)
    fig.get_layout_engine().set(rect=(0, key, 1, 1 - key), w_pad=0.04, h_pad=0.02)
    s = np.linspace(0, 2.3, 500)
    # alpha |J_n| t~ = t / tau_n: the solver's scaled time is shown as a physical ratio
    for a, data, law, title in (
        (ax[0], laue, np.sin(np.pi * s) ** 2, r"Laue: $\sin^2(\pi t/\tau_n)$"),
        (ax[1], bragg, np.tanh(np.pi * s) ** 2, r"Bragg: $\tanh^2(\pi t/\tau_n)$"),
    ):
        # the law is drawn over the TT markers so the comparison stays visible where they crowd
        a.plot(
            s,
            law,
            color=INK,
            lw=2.0,
            zorder=3,
            label=(
                r"closed form, $\tau_n=\Lambda_P/(v_s\left|J_n(S)\right|)$"
                if IQMS
                else r"independent-satellite model, $\tau_n=\Lambda_P/(v_s\left|J_n(S)\right|)$, "
                "no fitted parameters"
            ),
        )
        for (S, al, n), I, c, m in zip(
            M.CASES, data, (BLUE, ORANGE, AQUA, YELLOW), M.MARK, strict=False
        ):
            if IQMS:  # end of the transit, t = t_tr, where the wavefront reaches z = L
                x_tr = al * abs(jv(n, S))
                a.plot([x_tr, x_tr], [1.04, 1.13], color=c, lw=4, solid_capstyle="butt", zorder=4)
            a.plot(
                al * abs(jv(n, S)) * t,
                I,
                m,
                color=c,
                mec="white",
                mew=0.8,
                ms=9.5,
                ls="none",
                zorder=2,
                label=rf"$S={S:g},\ L={al:g}\,\Lambda_P,\ n={n}$",
            )
        a.set(
            xlim=(0, 2.3),
            ylim=(-0.03, 1.15 if IQMS else 1.08),
            title=title,
            xlabel=r"time $t/\tau_n$",
        )
    ax[0].set_ylabel(r"sideband $I_n/I_{inc}$" if IQMS else r"satellite intensity $I_n/I_{inc}$")
    ax[1].tick_params(labelleft=False)
    if IQMS:
        ax[0].set_yticks([0, 0.5, 1])
    for name, data, curve in (
        ("Laue", laue, lambda x: np.sin(np.pi * x) ** 2),
        ("Bragg", bragg, lambda x: np.tanh(np.pi * x) ** 2),
    ):
        dev = [
            np.abs(I - curve(al * abs(jv(n, S)) * t)).max()
            for (S, al, n), I in zip(M.CASES, data, strict=False)
        ]
        print(f"f1 {name}: max |TT - expression| per case", " ".join(f"{v:.3f}" for v in dev))
    if IQMS:
        # One short key inside the Bragg panel, where the curve is flat: the four cases share one
        # entry (the caption names them), the tick stands for t_tr.
        from matplotlib.legend_handler import HandlerTuple

        h, _ = ax[1].get_legend_handles_labels()
        tick = ax[1].plot([], [], "|", color=INK, ms=18, mew=4)[0]
        ax[1].legend(
            [tuple(h[1:]), h[0], tick],
            ["full TT, 4 cases", "closed form", r"$t=t_{tr}$"],
            handler_map={tuple: HandlerTuple(ndivide=None, pad=0.1)},
            loc="lower right",
            frameon=False,
            handlelength=3.2,
            handletextpad=0.5,
            borderaxespad=0.3,
            fontsize=SMALL,
        )
        finish(fig, ax, "f1_collapse")
        return
    # Shared key under both panels: the simulated cases (2 x 2, after their lead), then the curve
    # they are compared with on a row of its own.
    h, lab = ax[1].get_legend_handles_labels()
    k = 1  # handles on the law row
    sim = fig.legend(
        h[k:],
        lab[k:],
        ncol=2,
        frameon=False,
        loc="lower left",
        bbox_to_anchor=(0, 0.01 + row),
        handletextpad=0.2,
        columnspacing=2.0,
        labelspacing=0.45,
        markerscale=1.4,
        borderaxespad=0,
        borderpad=0,
    )
    law = fig.legend(
        h[:k],
        lab[:k],
        ncol=k,
        columnspacing=2.0,
        frameon=False,
        loc="lower left",
        bbox_to_anchor=(0, 0.01),
        handlelength=2.2,
        handletextpad=0.5,
        borderaxespad=0,
        borderpad=0,
    )
    fig.canvas.draw()
    lead = "Full TT:"
    probe = fig.text(0, 0, lead, fontsize=SMALL, fontweight="bold")
    wl = probe.get_window_extent().width / fig.bbox.width
    probe.remove()
    box = sim.get_window_extent()
    ws, top = box.width / fig.bbox.width, box.y1 / fig.bbox.height
    x0 = (1 - wl - 0.012 - ws) / 2  # centre the labelled block under the panels
    fig.text(x0, top, lead, fontsize=SMALL, fontweight="bold", va="top")
    sim.set_bbox_to_anchor((x0 + wl + 0.012, 0.01 + row), transform=fig.transFigure)
    law.set_bbox_to_anchor((x0, 0.01), transform=fig.transFigure)
    finish(fig, ax, "f1_collapse")


def f2():
    import make_map_figure as M

    style()
    r = M.compute()
    deta, t, I, an = r["deta"], r["t"], r["I"], r["an"]
    fig, ax = plt.subplots(
        1,
        2,
        figsize=(FIG_W, 5.2),
        constrained_layout=True,
        gridspec_kw=dict(width_ratios=[1.25, 1]),
    )
    im = ax[0].imshow(
        I,
        origin="lower",
        aspect="auto",
        cmap="Blues",
        vmin=0,
        vmax=I.max(),
        extent=[deta[0], deta[-1], t[0], t[-1]],
    )
    ax[0].set(
        xlabel=r"$\eta-q$", ylabel=r"$\tilde t=t/t_{\rm tr}$", title=r"$I(\eta,\tilde t)$, full TT"
    )
    fig.colorbar(im, ax=ax[0], shrink=0.9, pad=0.02)
    k0 = np.argmin(np.abs(deta))
    tf = np.linspace(0, 1, 400)
    ax[1].plot(
        tf, np.sin(np.pi * an * tf) ** 2, color=INK, lw=2.4, label=r"$\sin^2(\pi\alpha_1\tilde t)$"
    )
    ax[1].plot(t, I[:, k0], "o", color=BLUE, mec="white", mew=0.8, label="full TT")
    ax[1].set(
        xlabel=r"$\tilde t$",
        ylabel=r"$I(\eta=q,\tilde t)$",
        ylim=(-0.03, 1.1),
        title="intensity at the satellite centre",
    )
    for s in ("top", "right"):
        ax[0].spines[s].set_visible(True)
    finish(fig, ax[1], "f2_fringes")


def f3():
    import make_memory_figure as M

    style()
    fig, axes = plt.subplots(
        2, 2, figsize=(FIG_W, 7.2), constrained_layout=True, gridspec_kw=dict(height_ratios=[1, 3])
    )
    ax = axes[1]
    time = np.linspace(0, 3.4, 300)
    axes[0, 0].plot(time, np.clip(time / 2, 0, 1), color=INK2)
    axes[0, 1].plot([0, 1, 2], [0, 1, 0], color=BLUE)
    axes[0, 1].plot([0, 4, 8], [0, 1, 0], color=ORANGE)
    for a in axes[0]:
        a.set(
            ylim=(-0.05, 1.15),
            yticks=[0, 1],
            xlabel=r"time / $t_{tr}$",
            ylabel=r"$A(t)$",
            title="Input envelope",
        )
    M.panel_a(ax[0], small=SMALL - 2, title=r"final amplitude with $J_1(S_f)=0$")
    M.panel_b(ax[1], small=SMALL - 2, title=r"increasing vs decreasing $A$")
    for line in ax[0].lines + ax[1].lines:
        if line.get_marker() not in ("None", None, ""):
            line.set_markersize(8)
    ax[0].texts[0].set(
        position=(2.93, 0.66), ha="right", va="top", text="$A$ constant in\nthe whole crystal"
    )
    ax[0].legend(frameon=False, loc="upper left", fontsize=SMALL)
    ax[1].set_ylim(-0.02, 0.76)
    ax[1].set_xlabel(r"acoustic amplitude $S\,A(\tilde t)$")
    h, _ = ax[1].get_legend_handles_labels()
    ax[1].legend(
        h,
        [r"rise/fall time 1 $t_{\rm tr}$", r"rise/fall time 4 $t_{\rm tr}$"],
        frameon=False,
        loc="upper center",
        ncol=2,
        fontsize=SMALL - 2,
        columnspacing=1.0,
        handletextpad=0.3,
    )
    # which branch is which: every loop starts at the origin, so the lower branch is the rise
    ax[1].text(2.05, 0.09, "increase", color=BLUE, fontsize=SMALL, fontweight="bold")
    ax[1].text(0.02, 0.55, "decrease", color=BLUE, fontsize=SMALL, fontweight="bold")
    finish(fig, axes.flat, "f3_memory")


def f4():
    import make_phase_figure as M

    style()
    P = M.merged()
    fig, ax = plt.subplots(figsize=(FIG_W, F4_H), constrained_layout=True)
    Ss = sorted(set(P[:, 2]))
    hues = plt.cm.viridis(np.linspace(0, 0.9, len(Ss)))
    for c, S in zip(hues, Ss, strict=False):
        m = (P[:, 2] == S) & (P[:, 1] >= 2)
        ax.plot(
            P[m, 0] / P[m, 1],
            P[m, 3],
            "o",
            ms=8,
            color=c,
            mec="white",
            mew=0.5,
            ls="none",
            label=f"S={S:g}",
        )
    for e, lab in (
        (0.05, "5 %"),
        (0.5, "50 %"),
    ):  # 20 % dropped: its label collides with 50 % at print size
        ax.axhline(e, color=INK2, lw=1.4, ls=":")
        ax.text(1.3e-3, e * 1.12, lab, fontsize=SMALL, color=INK2)
    # the boundary the panel is about, so the result is readable without decoding the scatter
    ax.axvline(0.3, color=INK, lw=2.0, ls=(0, (5, 3)), zorder=4)
    ax.text(
        0.26,
        3.5e-5,
        "closed form holds" if IQMS else "independent satellites",
        fontsize=SMALL,
        color=INK,
        ha="right",
        va="bottom",
    )
    ax.text(
        0.35,
        3.5e-5,
        "channels couple" if IQMS else "coupled satellites",
        fontsize=SMALL,
        color=INK,
        ha="left",
        va="bottom",
    )
    ax.set(
        xscale="log",
        yscale="log",
        ylim=(2.2e-5, 1.5),
        xlim=(1e-3, 6),
        xlabel=r"$\Lambda_{ac}/\Lambda_P$",
        ylabel="relative error",
    )
    # nine S values: a discrete colour bar reads better than a nine-entry legend
    cmap = mpl.colors.ListedColormap(hues)
    norm = mpl.colors.BoundaryNorm(np.arange(len(Ss) + 1) - 0.5, len(Ss))
    cb = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, pad=0.01, aspect=25)
    cb.set_ticks(range(len(Ss)), labels=[f"{S:g}" for S in Ss])
    cb.set_label("$S$" if IQMS else "acoustic amplitude $S$")
    cb.outline.set_visible(False)
    finish(fig, ax, "f4_regime")


def f5():
    import json

    sys.path.insert(0, str(ROOT / "explore" / "nb"))
    from e59_transfer import G, T, packet, predict

    style()
    nb = ROOT / "explore" / "nb"
    alpha, kappa, S = 8.0, 6.0, 0.02
    wd = 2 * np.pi * alpha
    A = json.load(open(nb / "e58_abs.json"))
    D = json.load(open(nb / "e58_darwin.json"))
    fig, ax = plt.subplots(1, 2, figsize=(FIG_W, 5.8), constrained_layout=True)
    cases = [
        (0.05, A["S0.02"], wd / 0.05),
        (0.2, D["RD0.2"], D["RD0.2"]["q0"]),
        (0.5, D["RD0.5"], D["RD0.5"]["q0"]),
    ]
    for (RD, r, q0), c in zip(cases, (BLUE, ORANGE, AQUA), strict=False):
        eta, Wn = np.array(r["eta"]), np.array(r["W"])
        Wp, R0 = predict(alpha, kappa, S, q0, eta)
        Wk = np.abs(R0) * np.abs(G(*packet(S, q0), eta)) * np.pi * alpha * S / kappa / T
        o = np.argsort(eta)
        ax[0].plot(eta[o] / wd, (Wp / Wk)[o], "-", color=c, lw=2.4)
        ax[0].plot(
            eta / wd,
            Wn / Wk,
            "o",
            ms=7,
            color=c,
            mec="white",
            mew=0.6,
            label=rf"pulse at {1 / RD:g} $\omega_D$",
        )
    ax[0].axhline(1, color=INK2, lw=1.2, ls=":")
    ax[0].set(
        xscale="log",
        yscale="log",
        xlabel=r"phonon frequency / Darwin half-width",
        ylabel="Fourier weight / kinematic value",
        title="points: full TT, lines: formula",
    )
    ax[0].legend(frameon=False, loc="lower right", fontsize=SMALL - 2)
    E = json.load(open(nb / "e64_sw.json"))
    x, sw, ric = [], [], []
    for _k, r in E.items():
        eta, W = np.array(r["eta"]), r["W"]
        i = np.argmin(np.abs(eta - W))
        tt = abs(complex(r["TT"][0][i], r["TT"][1][i]))
        x.append(W / wd)
        sw.append(abs(complex(r["SW"][0][i], r["SW"][1][i])) / tt)
        ric.append(abs(complex(r["Riccati"][0][i], r["Riccati"][1][i])) / tt)
    o = np.argsort(x)
    x, sw, ric = np.array(x)[o], np.array(sw)[o], np.array(ric)[o]
    ax[1].plot(x, sw, "s-", color=ORANGE, ms=10, lw=2.4, label="plane-wave perturbation (2003)")
    ax[1].plot(x, ric, "o-", color=BLUE, ms=10, lw=2.4, label="this work (first order)")
    ax[1].axhline(1, color=INK2, lw=1.2, ls=":")
    ax[1].set(
        xscale="log",
        yscale="log",
        xlabel=r"phonon frequency / Darwin half-width",
        ylabel="theory / full TT",
        title="inside the Darwin width",
    )
    ax[1].set_yticks([1, 2, 4, 8], labels=["1", "2", "4", "8"])
    ax[1].yaxis.set_minor_formatter(mpl.ticker.NullFormatter())
    ax[1].legend(frameon=False, loc="upper right", fontsize=SMALL - 2)
    finish(fig, ax, "f5_outlook")


def f6():
    """Known Bessel coupling weights, not dynamical peak intensities."""
    from scipy.special import jv

    style()
    # same printed height as f0, which shares its row on the Background card
    fig, ax = plt.subplots(figsize=(INTRO_W, 2.45), constrained_layout=True)
    amplitude = np.linspace(0, 5, 501)
    for n, color in zip((0, 1, 2, 3), (INK2, BLUE, ORANGE, AQUA), strict=False):
        ax.plot(amplitude, np.abs(jv(n, amplitude)), color=color, label=rf"$n={n}$")
    ax.set(
        xlabel=r"sound amplitude $S=h u_0$",
        ylabel=r"$\left|J_n(S)\right|$",
        xlim=(0, 5),
        ylim=(0, 1.04),
        title="Sinusoidal grating: Bessel weights",
    )
    ax.legend(frameon=False, loc="center left", bbox_to_anchor=(1.0, 0.5), handlelength=1.4)
    finish(fig, ax, "f6_background")


def f7():
    import json

    style()
    data = np.load(ROOT / "explore" / "nb" / "e67_overshoot.npz")
    summary = json.loads((ROOT / "explore" / "nb" / "e67_overshoot.json").read_text())
    if IQMS:  # the map alone; the J_1 maximum bounds the region without overshoot
        from scipy.optimize import minimize_scalar
        from scipy.special import jv

        s_max = minimize_scalar(lambda s: -jv(1, s), bounds=(1, 3), method="bounded").x
        fig, ax = plt.subplots(figsize=(FIG_W, F7_H), constrained_layout=True)
        im = ax.pcolormesh(
            data["S"], data["rise"], data["excess"], shading="nearest", cmap="cividis", vmin=0
        )
        cb = fig.colorbar(im, ax=ax, pad=0.02, fraction=0.045, ticks=[0, 0.2, 0.4, 0.6])
        cb.set_label(r"$\Delta I/I_{inc}$")
        ax.axvline(s_max, color="white", ls="--", lw=2)
        ax.text(
            s_max - 0.1, 3.8, r"max of $J_1$", color="white", fontsize=SMALL, ha="right", va="top"
        )
        ax.set(
            xlabel=r"final acoustic amplitude $S$",
            ylabel=r"rise time $T_{rise}/t_{tr}$",
            yticks=[1, 2, 3, 4],
        )
        OUT.mkdir(parents=True, exist_ok=True)
        fig.savefig(OUT / "f7_overshoot.png")
        print("wrote", OUT / "f7_overshoot.png")
        return
    fig = plt.figure(figsize=(FIG_W, F7_H), constrained_layout=True)
    grid = fig.add_gridspec(
        2, 3, height_ratios=[1.2, 1.0] if IQMS else [1.78, 1.0], hspace=0.18
    )  # PR #9: show the full 2D scan
    ax = fig.add_subplot(grid[0, :])
    im = ax.pcolormesh(
        data["S"],
        data["rise"],
        data["excess"],
        shading="nearest",
        cmap="cividis" if IQMS else "YlOrRd",
        vmin=0,
    )
    cb = fig.colorbar(im, ax=ax, pad=0.02, fraction=0.045)
    cb.set_label(r"$\Delta I/I_{inc}$")
    # the map is the reduced coupling law over the scanned grid; only A-C are checked against full TT
    ax.set(
        xlabel=r"final acoustic amplitude $S$",
        ylabel=r"rise time $T_{rise}/t_{tr}$",
        title=("Closed form" if IQMS else "Reduced model")
        + r", Laue, $n=1$, $L=\Lambda_P/2$:  $\Delta I=I_{max}-I_{steady}$",
    )

    def num(v):
        if v >= 0.01:
            return f"{v:.2f}"
        m, e = f"{v:.1e}".split("e")
        return rf"${m}\times10^{{{int(e)}}}$"

    for case, color, label in zip(
        summary["cases"],
        (BLUE, ORANGE, AQUA),
        ("A: monotonic", "B: maximum above steady", r"C: final $S$ near zero of $J_1$"),
        strict=False,
    ):
        letter, S, rise = case["label"], case["S"], case["rise"]
        if IQMS:  # one hue in the map; the traces are told apart by their letter
            color = INK
        ax.plot(S, rise, "o", color=color, mec="white", mew=2, ms=13)
        ax.annotate(
            letter,
            (S, rise),
            xytext=(9, 9),
            textcoords="offset points",
            fontsize=BIG,
            fontweight="bold",
            color="white" if IQMS else INK,
        )
        a = fig.add_subplot(grid[1, ord(letter) - ord("A")])
        a.plot(data[f"{letter}_t"], data[f"{letter}_I"], color=INK if IQMS else color)
        a.plot(
            data[f"{letter}_tt_t"][::3],
            data[f"{letter}_tt_I"][::3],
            "o",
            color=BLUE if IQMS else color,
            mec="white",
            ms=8,
        )
        a.axhline(case["steady"], color=INK2, ls="--", lw=1.5)
        if letter == "B":  # mark the quantity the map shows
            k = int(np.argmax(data["B_I"]))
            tb = float(data["B_t"][k])
            a.annotate(
                "",
                xy=(tb, float(data["B_I"][k])),
                xytext=(tb, case["steady"]),
                arrowprops=dict(
                    arrowstyle="<|-|>", color=INK, lw=1.6, mutation_scale=16, shrinkA=0, shrinkB=0
                ),
            )
            if IQMS:  # above the peak it measures: clear of the TT points and the axis
                a.text(
                    tb, float(data["B_I"][k]) + 0.06, r"$\Delta I$", fontsize=SMALL + 1, ha="center"
                )
            else:
                a.text(
                    tb, case["steady"] - 0.06, r"$\Delta I$", fontsize=SMALL, ha="center", va="top"
                )
        # headroom above every curve (max 0.6) for the two-line case label, which has no backing box
        a.set(xlabel=r"time $t/t_{tr}$", ylim=(-0.025, 1.55 if IQMS else 1.3), yticks=[0, 0.5, 1])
        if IQMS:
            a.set_xlim(0, 3)  # one time axis for A-C
        peak, steady = case["peak"], case["steady"]
        if IQMS:  # 24 pt; the condition goes in the title, the two values on their own lines
            T = "t_{tr}" if rise == 1 else rf"{rise:g}\,t_{{tr}}"
            a.set_title(rf"{letter}: $S={S:g}$, $T_{{rise}}={T}$", fontsize=SMALL + 1, color=INK)
            values = (
                f"peak = steady = {num(steady)}"
                if peak - steady < 1e-9
                else f"peak {num(peak)}\nsteady {num(steady)}"
            )
            a.text(0.04, 0.95, values, transform=a.transAxes, fontsize=SMALL + 1, va="top")
        else:
            a.set_title(
                label, color=color, fontsize=SMALL - 2, fontweight="bold"
            )  # colour = map marker
            values = (
                f"peak = steady = {num(steady)}"
                if peak - steady < 1e-9
                else f"peak {num(peak)}, steady {num(steady)}"
            )
            a.text(
                0.04,
                0.95,
                rf"$S={S:g}$, $T_{{rise}}/t_{{tr}}={rise:g}$" + "\n" + values,
                transform=a.transAxes,
                fontsize=SMALL - 2,
                va="top",
                linespacing=1.25,
            )
        if letter == "A":
            a.set_ylabel(r"$I_1/I_{inc}$")
        else:
            a.tick_params(labelleft=False)
        a.grid(color=GRID, lw=1)
        a.set_axisbelow(True)
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "f7_overshoot.png")
    print("wrote", OUT / "f7_overshoot.png")


def f8():
    """Kinematic satellites (talk v4, slide 2): planes without and with a shear wave, and J_n(S)^2.

    Depth z runs down, h is horizontal (in the surface plane, symmetric Laue), and the shear
    displacement u || h bends each plane with depth. The bars are the kinematic weights; the
    satellite of order n sits at detuning beta = nK.
    """
    from scipy.special import jv

    style()
    fig, (ax, axb) = plt.subplots(
        1,
        2,
        figsize=(FIG_W, (0.37 if IQMS else 0.33) * FIG_W),
        constrained_layout=True,
        gridspec_kw=dict(width_ratios=[1.25, 1.0]),
    )
    ax.set(xlim=(-0.9, 10.4), ylim=(-0.9, 9.4))
    ax.axis("off")
    z = np.linspace(0.6, 7.6, 300)
    K = 2 * np.pi / 2.3
    for left, wave, title in ((0.0, False, "no sound"), (5.4, True, r"shear wave, $u\parallel h$")):
        for k in range(6):
            x = left + 0.75 * k + (0.28 * np.sin(K * z) if wave else np.zeros_like(z))
            ax.plot(x, z, color=INK if wave else INK2, lw=2.2)
        ax.annotate(
            "",
            xy=(left + 4.2, 8.35),
            xytext=(left, 8.35),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.8, mutation_scale=18),
        )
        ax.text(left + 4.35, 8.35, "$h$", va="center", fontsize=BIG + 2)
        ax.text(left + 2.0, 9.25, title, ha="center", va="center", fontsize=SMALL)
    ax.annotate(
        "",
        xy=(10.0, 0.6),
        xytext=(10.0, 7.6),
        arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.4, mutation_scale=20),
    )
    ax.text(10.15, 4.1, "$K$", color=BLUE, va="center", fontsize=BIG + 2)
    ax.annotate(
        "",
        xy=(-0.55, 0.4),
        xytext=(-0.55, 7.6),
        arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.4, mutation_scale=16),
    )
    ax.text(
        -0.75, 4.1, "depth $z$", rotation=90, ha="right", va="center", fontsize=SMALL, color=INK2
    )

    n = np.arange(-3, 4)
    for S, color, off in ((1.0, INK2, -0.2), (2.0, BLUE, 0.2)):
        axb.bar(n + off, jv(n, S) ** 2, width=0.38, color=color, label=f"$S={S:g}$")
    axb.set(
        xticks=n,
        ylim=(0, 0.65),
        yticks=[0, 0.2, 0.4, 0.6],
        xlabel=r"order $n$ (detuning $\beta=nK$)",
        ylabel=r"$J_n(S)^2$",
    )
    axb.set_xticklabels([f"{k:+d}".replace("-", "\N{MINUS SIGN}") if k else "0" for k in n])
    axb.legend(frameon=False, loc="upper right")
    finish(fig, axb, "f8_satellites")


def f9():
    """Symmetric Laue and Bragg geometry (talk v4, slide 3) with the acoustic polarisation that
    couples in each: phi = h.u needs u to have a component along h. Laue: h in the surface plane, a
    shear wave along z with u || h. Bragg: h along z, a longitudinal wave."""
    style()
    fig, axes = plt.subplots(1, 2, figsize=(FIG_W, 0.31 * FIG_W), constrained_layout=True)
    for ax, geo in zip(axes, ("Laue", "Bragg"), strict=True):
        ax.set(xlim=(-0.4, 10.4), ylim=(-3.3, 7.4))
        ax.axis("off")
        ax.add_patch(plt.Rectangle((0.3, 0.0), 8.4, 3.2, fc="#eef3f9", ec=INK2, lw=1.4))
        ax.text(8.85, 3.2, "$z=0$", va="center", fontsize=SMALL, color=INK2)
        ax.text(8.85, 0.0, "$z=L$", va="center", fontsize=SMALL, color=INK2)
        p = (3.2, 3.2)
        ax.annotate(
            "",
            xy=p,
            xytext=(1.2, 5.6),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.4, mutation_scale=20),
        )
        ax.text(0.5, 6.1, "incident", fontsize=SMALL)
        title = "Laue (transmission)" if geo == "Laue" else "Bragg (reflection)"
        ax.text(5.0, 7.2, title, ha="center", va="top", fontsize=BIG)
        if geo == "Laue":
            ax.annotate(
                "",
                xy=(5.85, 0.0),
                xytext=p,
                arrowprops=dict(arrowstyle="-|>", color=INK2, lw=2.4, mutation_scale=20),
            )
            ax.annotate(
                "",
                xy=(0.55, 0.0),
                xytext=p,
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2.6, mutation_scale=20),
            )
            ax.text(5.0, 1.5, "$D_0$", fontsize=BIG, color=INK2)
            ax.text(1.0, 1.5, "$D_h$", fontsize=BIG, color=ORANGE)
            ax.annotate(
                "",
                xy=(5.6, 4.4),
                xytext=(7.9, 4.4),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.8, mutation_scale=18),
            )
            ax.text(8.05, 4.4, "$h$", va="center", fontsize=BIG)
            ax.annotate(
                "",
                xy=(5.6, 5.4),
                xytext=(7.9, 5.4),
                arrowprops=dict(arrowstyle="<|-|>", color=BLUE, lw=1.8, mutation_scale=16),
            )
            ax.text(8.05, 5.4, "$u$", va="center", fontsize=BIG, color=BLUE)
            wave = r"shear wave along $z$, $u\parallel h$"
            bc = r"$D_0(0)=1,\ D_h(0)=0$"
            how = "both on the entrance face"
        else:
            ax.annotate(
                "",
                xy=(5.85, 0.0),
                xytext=p,
                arrowprops=dict(arrowstyle="-|>", color=INK2, lw=2.4, mutation_scale=20),
            )
            ax.annotate(
                "",
                xy=(6.6, 5.6),
                xytext=(3.9, 2.36),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2.6, mutation_scale=20),
            )
            ax.text(3.3, 0.6, "$D_0$", fontsize=BIG, color=INK2)
            ax.text(6.9, 4.7, "$D_h$", fontsize=BIG, color=ORANGE)
            ax.annotate(
                "",
                xy=(8.2, 6.6),
                xytext=(8.2, 4.3),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.8, mutation_scale=18),
            )
            ax.text(8.4, 5.45, "$h$", va="center", fontsize=BIG)
            ax.annotate(
                "",
                xy=(9.5, 6.6),
                xytext=(9.5, 4.3),
                arrowprops=dict(arrowstyle="<|-|>", color=BLUE, lw=1.8, mutation_scale=16),
            )
            ax.text(9.7, 5.45, "$u$", va="center", fontsize=BIG, color=BLUE)
            wave = r"longitudinal wave along $z$, $u\parallel h$"
            bc = r"$D_0(0)=1,\ D_h(L)=0$"
            how = "on opposite faces"
        ax.text(4.5, -0.55, wave, ha="center", va="top", fontsize=SMALL, color=LABEL)
        ax.text(4.5, -1.55, bc, ha="center", va="top", fontsize=SMALL)
        ax.text(4.5, -2.45, how, ha="center", va="top", fontsize=SMALL, color=INK2)
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "f9_geometry.png")
    print("wrote", OUT / "f9_geometry.png")


F10_ALPHA = np.array([0.1, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5])  # L / Lambda_P of the TT points
F10_S, F10_AAC, F10_PHASES = 1.5, 40.0, 8


def f10_points():
    """Full TT in the filled crystal (steady=True: the whole depth carries the wave), centre
    intensity at beta = nK for n = 1, 2, averaged over F10_PHASES acoustic phases. Cached in
    explore/nb/poster_f10_points.npz."""
    from tratt.cube import rocking_cube

    cache = ROOT / "explore" / "nb" / "poster_f10_points.npz"
    if cache.exists():
        d = np.load(cache)
        return d["laue"], d["bragg"]
    d = Drive(S=F10_S, alpha_ac=F10_AAC)
    # one acoustic period is 1 / alpha_ac in units of the transit time
    t = (np.arange(F10_PHASES) + 0.5) / (F10_PHASES * F10_AAC)
    eta = np.array([d.q, 2 * d.q])
    out = {}
    for geo in ("laue", "bragg"):
        out[geo] = np.array(
            [rocking_cube(a, d, eta, t, geometry=geo, steady=True).mean(axis=0) for a in F10_ALPHA]
        )
    np.savez(cache, alpha=F10_ALPHA, S=F10_S, alpha_ac=F10_AAC, **out)
    return out["laue"], out["bragg"]


def f10():
    """Steady sidebands against thickness (Entries 1, 9, 54): the independent-satellite closed
    forms sin^2(pi L |J_n| / Lambda_P) (Laue) and tanh^2 (Bragg), the kinematic Bessel law
    (pi L J_n / Lambda_P)^2, and full TT in the filled crystal. Left: Laue I_1 and I_2. Right: the
    ratio I_2 / I_1, which the kinematic law fixes at J_2^2 / J_1^2 for every thickness."""
    from scipy.special import jv

    style()
    laue, bragg = f10_points()
    j1, j2 = abs(jv(1, F10_S)), abs(jv(2, F10_S))
    a = np.linspace(1e-3, 1.6, 400)
    fig, (ax, axr) = plt.subplots(1, 2, figsize=(FIG_W, 5.4), constrained_layout=True)
    # Left: one colour per order, named on the curve; dashed = kinematic (caption). Right: one
    # colour per geometry would reuse the left pair for another meaning, so it is black and grey.
    for j, I, c, m, n, xy in (
        (j1, laue[:, 0], BLUE, "o", 1, (0.9, 1.06)),
        (j2, laue[:, 1], ORANGE, "s", 2, (1.42, 0.6)),
    ):
        ax.plot(a, np.sin(np.pi * a * j) ** 2, color=c)
        ax.plot(a, (np.pi * a * j) ** 2, color=c, ls="--", lw=2.2)
        ax.plot(F10_ALPHA, I, m, color=c, mec="white", mew=0.8, ms=11, ls="none")
        ax.text(*xy, f"$n={n}$", color=c, fontsize=BIG, ha="center", va="bottom")
    ax.set(
        xlim=(0, 1.6),
        ylim=(0, 1.22),
        yticks=[0, 0.5, 1.0],
        xlabel=r"thickness $L/\Lambda_P$",
        ylabel=r"steady $I_n/I_{inc}$ (Laue)",
    )
    kin = j2**2 / j1**2
    axr.axhline(kin, color=INK2, ls="--", lw=2.2, label=r"kinematic $J_2^2/J_1^2$")
    for law, I, ls, m, fc, name in (
        (lambda x: np.sin(np.pi * x) ** 2, laue, "-", "o", INK, "Laue"),
        (lambda x: np.tanh(np.pi * x) ** 2, bragg, "-.", "s", "white", "Bragg"),
    ):
        axr.plot(a, law(a * j2) / law(a * j1), color=INK, ls=ls, label=name)
        axr.plot(F10_ALPHA, I[:, 1] / I[:, 0], m, mfc=fc, mec=INK, mew=1.8, ms=11, ls="none")
    axr.set(
        xlim=(0, 1.6),
        ylim=(0, 1.0),
        xlabel=r"thickness $L/\Lambda_P$",
        ylabel=r"ratio $I_2/I_1$",
    )
    axr.legend(frameon=False, loc="upper left", handlelength=2.6)
    finish(fig, (ax, axr), "f10_steady")
    for name, I, law in (
        ("Laue", laue, lambda x: np.sin(np.pi * x) ** 2),
        ("Bragg", bragg, lambda x: np.tanh(np.pi * x) ** 2),
    ):
        dev = np.abs(I - law(np.outer(F10_ALPHA, [j1, j2]))).max()
        print(f"f10 {name}: max |TT - closed form| = {dev:.3f}")
    print(f"f10 kinematic J_2^2/J_1^2 = {kin:.3f}")


SI_D440 = 5.4310e-10 / np.sqrt(32)  # m
SI_H440 = 2 * np.pi / SI_D440  # 1/m
LAMBDA_LAUE = 98.76e-6  # m, Pendellosung period, Si 440, 30 keV (Entry 20)
THETA_B = np.arcsin(12.398420 / 30.0 * 1e-10 / (2 * SI_D440))
LAMBDA_BRAGG = LAMBDA_LAUE * np.tan(THETA_B)  # extinction length (Bragg)
V_SHEAR = np.sqrt(79.6e9 / 2329.0)
V_LONG = np.sqrt((165.7e9 + 63.9e9 + 2 * 79.6e9) / (2 * 2329.0))
ORDER = ("#111111", "#c8102e", "#7b4ea3", "#2e8b57", "#8c5a2b")  # sideband order n = 0..4
RED = "#d62020"  # diffracted beam D_h in the drawings, as in the October talk


def arrow(ax, a, b, color=INK, lw=2.4, style="-|>", ms=22, z=5):
    ax.annotate(
        "",
        xy=b,
        xytext=a,
        arrowprops=dict(
            arrowstyle=style, color=color, lw=lw, mutation_scale=ms, shrinkA=0, shrinkB=0
        ),
        zorder=z,
    )


def onset_sketch(ax):
    """The Laue onset schematic of the October talk (slide 2), redrawn at print size with labels of
    at least 24 pt: lattice columns of spacing d along h, displaced by the transverse wave above the
    wavefront z = v_s t and straight below it, the transducer on top, Lambda_ac, K, the incident k_0,
    D_0, and D_h with the n = +-1 sidebands. Schematic, not to scale."""
    lab = 24
    ax.set(xlim=(-2.9, 13.4), ylim=(-2.7, 6.3), aspect="equal")
    ax.axis("off")
    x0, x1, yb, yt, yw = 0.0, 10.0, 0.0, 4.0, 2.0
    lam = 1.05  # acoustic wavelength in drawing units
    ax.add_patch(plt.Rectangle((x0, yw), x1 - x0, yt - yw, fc="#e3ecf7", ec="none", zorder=0.5))
    ax.add_patch(plt.Rectangle((x0, yb), x1 - x0, yt - yb, fc="none", ec=INK, lw=2.0, zorder=4))
    ax.add_patch(plt.Rectangle((x0, yt), x1 - x0, 0.22, fc="#3a3f4b", ec="none", zorder=4))
    zs = np.arange(yb + 0.12, yt, 0.2)
    for xc in np.arange(x0 + 0.18, x1, 0.3):
        u = np.where(zs > yw, 0.08 * np.sin(2 * np.pi * (yt - zs) / lam), 0.0)
        ax.plot(xc + u, zs, color="#9aa3ad", lw=0.6, zorder=1)
        ax.plot(xc + u, zs, "o", color="#3d4654", ms=1.6, mec="none", zorder=1.5)
    ax.plot([x0, x1], [yw, yw], color=BLUE, lw=2.6, ls=(0, (5, 3)), zorder=5)
    ax.text(x1 + 0.25, yw, "$z=v_st$", fontsize=lab, va="center", color=BLUE)
    arrow(ax, (x1 + 0.55, 3.9), (x1 + 0.55, 2.55), BLUE, 2.6)
    ax.text(x1 + 0.85, 3.3, "$\\mathbf{K}$", fontsize=lab + 2, va="center", color=BLUE)
    ax.text(x1 - 0.1, yt + 0.4, "transducer", fontsize=lab, ha="right", va="bottom", color=INK2)
    arrow(ax, (0.2, yt + 0.75), (1.6, yt + 0.75), INK, 2.2, ms=18)
    ax.text(1.75, yt + 0.75, "$\\mathbf{h}$", fontsize=lab, va="center")
    ax.plot([-0.45, -0.45], [yt - 0.15, yt - 0.15 - lam], color=INK2, lw=1.6)
    for y in (yt - 0.15, yt - 0.15 - lam):
        ax.plot([-0.6, -0.3], [y, y], color=INK2, lw=1.6)
    ax.text(
        -0.7,
        yt - 0.15 - lam / 2,
        "$\\Lambda_{ac}$",
        fontsize=lab,
        ha="right",
        va="center",
        color=INK2,
    )
    arrow(ax, (-2.4, yt), (-2.4, yb), INK2, 1.6, ms=16)
    ax.text(
        -2.6,
        0.5 * (yt + yb),
        "depth $z$",
        rotation=90,
        fontsize=lab,
        ha="right",
        va="center",
        color=INK2,
    )
    for xd in (7.08, 7.38):
        ax.plot([xd, xd], [-0.3, -0.5], color=INK2, lw=1.4)
    ax.plot([7.08, 7.38], [-0.4, -0.4], color=INK2, lw=1.4)
    ax.text(7.23, -0.6, "$d$", fontsize=lab, ha="center", va="top", color=INK2)
    p_in = (3.4, yt + 0.22)
    tb = 0.28  # tan of the drawn Bragg angle
    d0_out = (p_in[0] + (p_in[1] - yb) * tb, yb)
    dh_out = (p_in[0] - (p_in[1] - yb) * tb, yb)
    ax.add_patch(plt.Polygon([p_in, d0_out, dh_out], fc="#f6dfb8", ec="none", alpha=0.75, zorder=2))
    arrow(ax, (p_in[0] - 0.42 * 1.9, p_in[1] + 1.9), p_in, INK, 3.0)
    ax.text(
        p_in[0] - 0.42 * 1.9 - 0.15,
        p_in[1] + 1.75,
        "X-rays $\\mathbf{k}_0$",
        fontsize=lab,
        ha="right",
        va="center",
    )
    arrow(ax, d0_out, (d0_out[0] + 0.55, -1.75), INK, 3.0)
    ax.text(d0_out[0] + 0.75, -1.95, "$D_0$", fontsize=lab + 2, va="top")
    for dx in (-0.3, 0.3):
        arrow(ax, dh_out, (dh_out[0] - 0.55 + dx, -1.6), "#f0a020", 2.2, ms=16)
    arrow(ax, dh_out, (dh_out[0] - 0.55, -1.75), RED, 3.0)
    ax.text(dh_out[0] - 0.6, -1.95, "$D_h$", fontsize=lab + 2, color=RED, ha="center", va="top")
    ax.text(
        dh_out[0] - 1.05, -0.9, "$n=\\pm1$", fontsize=lab, color="#d08000", ha="right", va="center"
    )


def f11():
    """i-QMS panel 4: the closed form for the driven layer v_s t, first sideband, S = 1.5,
    L = 296 um, Si 440 at 30 keV (constants as in poster/check_numbers.py): Laue oscillates until
    t_tr and then holds; Bragg saturates near tau_1. Lines are labelled where they end."""
    from scipy.special import jv

    style()
    S = 1.5
    j1, L = abs(jv(1, S)), 296e-6
    cases = (
        ("Laue", BLUE, LAMBDA_LAUE / (V_SHEAR * j1), L / V_SHEAR, lambda x: np.sin(np.pi * x) ** 2),
        (
            "Bragg",
            ORANGE,
            LAMBDA_BRAGG / (V_LONG * j1),
            L / V_LONG,
            lambda x: np.tanh(np.pi * x) ** 2,
        ),
    )
    fig, axr = plt.subplots(figsize=(FIG_W, 0.27 * FIG_W), constrained_layout=True)
    tt = np.linspace(0, 62e-9, 1500)
    for name, color, tau, t_tr, law in cases:
        axr.plot(tt * 1e9, law(np.minimum(tt, t_tr) / tau), color=color)
        axr.plot([t_tr * 1e9] * 2, [1.1, 1.22], color=color, lw=4, solid_capstyle="butt")
        axr.text(
            t_tr * 1e9,
            1.25,
            f"{name} $t_{{tr}}$",
            color=color,
            fontsize=SMALL - 2,
            ha="center",
            va="bottom",
        )
    axr.text(61, 0.62, "Laue", color=BLUE, fontsize=SMALL, ha="right", va="bottom")
    axr.text(61, 0.93, "Bragg", color=ORANGE, fontsize=SMALL, ha="right", va="top")
    axr.set(
        xlim=(0, 62),
        ylim=(0, 1.42),
        yticks=[0, 0.5, 1],
        xlabel="time after onset (ns)",
        ylabel="first sideband $I_1/I_0$",
    )
    finish(fig, axr, "f11_formation")
    for name, _, tau, t_tr, law in cases:
        print(
            f"f11 {name}: tau_1 {tau * 1e9:.1f} ns, t_tr {t_tr * 1e9:.1f} ns, I(t_tr) {law(t_tr / tau):.2f}"
        )


# Vadilonga et al., J. Appl. Cryst. 50, 525 (2017), Fig. 6 (CC BY 2.0 UK): satellite intensities of a
# Rayleigh surface acoustic wave on Y-cut langasite at BESSY II against the IDT drive amplitude (V).
# Read off the published figure (pixel positions, about +-0.01); the J_m^2 reference lines use the
# argument 0.077 V^-1 read from where its m = 0, 1, 2 lines peak or vanish.
VADILONGA = {
    0: ((0, 10, 20, 30, 40), (1.0, 0.725, 0.308, 0.107, 0.084)),
    1: ((10, 20, 30, 40), (0.066, 0.226, 0.172, 0.128)),
    2: ((20, 30, 40), (0.048, 0.115, 0.108)),
    3: ((30, 40), (0.039, 0.046)),
    4: ((30, 40), (0.005, 0.013)),
}
VADILONGA_ARG = 0.077


def f12():
    """i-QMS background: (left) Bessel weights J_n(S)^2 against the displacement amplitude u0 for
    Si 440, with S = h u0 on the top axis and S = 1.5 marked; (right) the measured surface-acoustic-
    wave satellites of Vadilonga et al. 2017 with their J_m^2 reference lines."""
    from scipy.special import jv

    style()
    fig, (ax, axv) = plt.subplots(1, 2, figsize=(FIG_W, 4.4), constrained_layout=True)
    u = np.linspace(0, 65, 600)  # pm
    S = SI_H440 * u * 1e-12
    # labels beside their curves, inside the frame: n = 0 above its falling edge, n = 3 at the right
    for n, x, y, ha in (
        (0, 15, 0.95, "left"),
        (1, 26, 0.37, "center"),
        (2, 47, 0.27, "center"),
        (3, 64, 0.25, "right"),
    ):
        ax.plot(u, jv(n, S) ** 2, color=ORDER[n])
        ax.text(x, y, f"$n={n}$", color=ORDER[n], fontsize=SMALL, ha=ha)
    u15 = 1.5 / SI_H440 * 1e12
    ax.axvline(u15, color=INK2, ls=":", lw=2.0)
    ax.text(u15 + 1, 1.02, "$S$ = 1.5", fontsize=SMALL - 2, color=INK2, va="top")
    ax.set(
        xlim=(0, 65),
        ylim=(0, 1.08),
        xlabel="displacement amplitude $u_0$ (pm), Si 440",
        ylabel="kinematic weight $J_n(S)^2$",
    )
    top = ax.secondary_xaxis(
        "top", functions=(lambda x: SI_H440 * x * 1e-12, lambda s: s / SI_H440 * 1e12)
    )
    top.set_xlabel("$S=hu_0$")
    top.tick_params(direction="in", which="both")

    v = np.linspace(0, 45, 400)
    for m, (x, y) in VADILONGA.items():
        axv.plot(v, jv(m, VADILONGA_ARG * v) ** 2, color=ORDER[m], lw=1.8)
        axv.plot(x, y, "osd^v"[m], color=ORDER[m], mec=INK, ls="none")
    for m, xy in (
        (0, (8, 0.85)),
        (1, (22, 0.37)),
        (2, (41, 0.26)),
        (3, (44, 0.185)),
        (4, (44, 0.065)),
    ):
        axv.text(
            *xy, f"$m={m}$", color=ORDER[m], fontsize=SMALL - 2, ha="center" if m < 3 else "right"
        )
    axv.set(
        xlim=(0, 45),
        ylim=(0, 1.08),
        xlabel="drive amplitude on the transducer (V)",
        ylabel="satellite intensity",
    )
    finish(fig, (ax, axv), "f12_bessel")


def f13():
    """i-QMS introduction. Left: the Laue onset schematic (onset_sketch). Right: rocking curve of the
    crystal filled with sound, Si 440 at 30 keV, S = 1.5, 2 GHz shear wave (Lambda_ac = 2.96 um),
    L = 3 Lambda_ac = 8.9 um (L << Lambda, so the peaks carry the kinematic weights), averaged over
    eight acoustic phases; the angle offset is eta / (h L), satellite n at n d / Lambda_ac. Grey: the
    same crystal without sound."""
    style()
    a_ac = 3.0
    lam_ac = V_SHEAR / 2e9
    L = a_ac * lam_ac
    alpha = L / LAMBDA_LAUE
    d = Drive(S=1.5, alpha_ac=a_ac)
    eta = np.linspace(-2.6 * d.q, 2.6 * d.q, 2001)
    shift = (2.0 + np.arange(8) / 8 * d.period)[:, None]
    n_z = required_nz(alpha, a_ac, S=1.5, eta_max=eta.max())
    I = rocking(alpha, eta, phi=d.phi(shift), n_z=n_z).mean(axis=0)
    I0 = rocking(alpha, eta, n_z=n_z)
    dth = eta / (SI_H440 * L) * 1e6  # urad
    fig, (ax, axr) = plt.subplots(
        1,
        2,
        figsize=(FIG_W, 0.34 * FIG_W),
        constrained_layout=True,
        gridspec_kw=dict(width_ratios=[1.25, 1.0], wspace=0.03),
    )
    onset_sketch(ax)
    scale = 1e2
    axr.plot(dth, I0 * scale, color=INK2, lw=1.6)
    axr.plot(dth, I * scale, color=BLUE)
    axr.text(4, 0.8 * I0.max() * scale, "no sound", color=INK2, fontsize=SMALL - 2, ha="left")
    step = d.q / (SI_H440 * L) * 1e6
    for n in range(-2, 3):
        k = np.argmin(abs(eta - n * d.q))
        lab = "$n=0$" if n == 0 else f"${n:+d}$".replace("-", "−")
        axr.text(
            n * step,
            I[k] * scale + 0.12,
            lab,
            fontsize=SMALL - 2,
            ha="center",
            va="bottom",
            color=BLUE,
        )
    axr.set(
        xlim=(dth[0], dth[-1]),
        ylim=(0, 1.15 * I0.max() * scale),
        xlabel=r"angle offset $\Delta\theta$ (μrad)",
        ylabel="$I_h/I_0$ (%)",
    )
    finish(fig, axr, "f13_rocking")
    print(
        f"f13: L {L * 1e6:.2f} um, alpha {alpha:.3f}, satellite step {step:.1f} urad, n_z {n_z}",
        "peaks",
        [round(float(I[np.argmin(abs(eta - n * d.q))] * scale), 3) for n in range(3)],
    )


F16_ALPHA, F16_AAC, F16_S, F16_PHASES = 296e-6 / LAMBDA_LAUE, 100.0, 1.5, 8  # L = 296 um, 2 GHz


def f16_profiles():
    """|D_h(z)|^2 inside a Laue crystal at the first-sideband angle (eta = q), step onset, against
    depth and time: the RK4 sweep of tratt.core.solve_laue, keeping D_h at every depth step instead
    of the exit value only (in Laue the field at depth z depends only on the layers above it).
    Vectorised over times and F16_PHASES acoustic phases (shifts of a fraction of one period),
    averaged over the phases. Cached in explore/nb/poster_f16_depth_time.npz."""
    from tratt.core import required_nz

    cache = ROOT / "explore" / "nb" / "poster_f16_depth_time.npz"
    if cache.exists() and float(np.load(cache)["alpha"]) == F16_ALPHA:
        c = np.load(cache)
        return c["zeta"], c["t"], c["I"]
    d = Drive(S=F16_S, alpha_ac=F16_AAC)
    eta = d.eta_channel(1)
    n_z = required_nz(F16_ALPHA, F16_AAC, S=F16_S, eta_max=eta)
    t = np.linspace(0.0, 1.3, 105)
    shift = np.arange(F16_PHASES) / F16_PHASES * d.period
    T = (t[:, None] + shift[None, :]).ravel()
    phi = d.phi(T)
    c, h = 1j * np.pi * F16_ALPHA, 1.0 / n_z

    def cpl(z):
        e = np.exp(1j * phi(np.float64(z)))
        return c * e, c * np.conj(e)

    def f(cp, cm, d0, dh):
        return cp * dh, cm * d0 + 1j * eta * dh

    D0 = np.ones(T.shape, dtype=np.complex128)
    Dh = np.zeros(T.shape, dtype=np.complex128)
    keep = max(1, n_z // 600)
    zeta, rows = [0.0], [np.zeros(T.shape)]
    start = cpl(0.0)
    for i in range(n_z):
        mid, end = cpl((i + 0.5) * h), cpl((i + 1) * h)
        k1a, k1b = f(*start, D0, Dh)
        k2a, k2b = f(*mid, D0 + 0.5 * h * k1a, Dh + 0.5 * h * k1b)
        k3a, k3b = f(*mid, D0 + 0.5 * h * k2a, Dh + 0.5 * h * k2b)
        k4a, k4b = f(*end, D0 + h * k3a, Dh + h * k3b)
        D0 = D0 + (h / 6.0) * (k1a + 2 * k2a + 2 * k3a + k4a)
        Dh = Dh + (h / 6.0) * (k1b + 2 * k2b + 2 * k3b + k4b)
        start = end
        if (i + 1) % keep == 0 or i + 1 == n_z:
            zeta.append((i + 1) * h)
            rows.append(np.abs(Dh) ** 2)
    I = np.array(rows).reshape(len(zeta), t.size, F16_PHASES).mean(axis=2)  # (depth, time)
    np.savez(
        cache, zeta=np.array(zeta), t=t, I=I, n_z=n_z, alpha=F16_ALPHA, alpha_ac=F16_AAC, S=F16_S
    )
    return np.array(zeta), t, I


def f16():
    """i-QMS section 5: the first sideband inside the crystal while the wave enters. Laue, Si 440 at
    30 keV, S = 1.5, L = 296 um , step onset; x = depth (um), y = time after onset (ns),
    colour = |D_h|^2 at the first-sideband angle; dashed: the wavefront z = v_s t; t_tr marked."""
    style()
    zeta, t, I = f16_profiles()
    L_um = F16_ALPHA * LAMBDA_LAUE * 1e6
    t_tr = F16_ALPHA * LAMBDA_LAUE / V_SHEAR * 1e9
    fig, ax = plt.subplots(figsize=(FIG_W, 4.4), constrained_layout=True)
    im = ax.pcolormesh(
        zeta * L_um, t * t_tr, I.T, shading="gouraud", cmap="Blues", vmin=0, vmax=1, rasterized=True
    )
    cb = fig.colorbar(im, ax=ax, pad=0.02, fraction=0.05, ticks=[0, 0.5, 1])
    cb.set_label("first sideband $|D_h|^2/I_0$")
    cb.ax.tick_params(direction="in", which="both")
    ax.plot([0, L_um], [0, t_tr], color=INK, ls="--", lw=2.0)
    ax.text(
        0.42 * L_um, 0.42 * t_tr + 2.5, "wavefront $z=v_st$", fontsize=SMALL, rotation=0, ha="right"
    )
    ax.axhline(t_tr, color=INK2, ls=":", lw=1.8)
    ax.text(8, t_tr + 1.2, f"$t_{{tr}}$ = {t_tr:.1f} ns", fontsize=SMALL, va="bottom")
    ax.set(
        xlim=(0, L_um),
        ylim=(0, t[-1] * t_tr),
        xlabel="depth $z$ (μm)",
        ylabel="time after onset (ns)",
    )
    finish(fig, ax, "f16_depth_time")
    print(
        f"f16: L {L_um:.0f} um, t_tr {t_tr:.1f} ns, exit max {I[-1].max():.3f}, exit at t_tr {np.interp(1.0, t, I[-1]):.3f}"
    )


if __name__ == "__main__":
    names = [a for a in sys.argv[1:] if a != "--iqms"]
    if "--iqms" in sys.argv:
        use_iqms()
    for name in names or ["f0", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10"]:
        globals()[name]()
