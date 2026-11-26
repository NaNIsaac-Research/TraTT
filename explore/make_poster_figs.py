"""Poster-only figures, drawn at print size for one A0 column. Run: python explore/make_poster_figs.py [f0 f1 f2 f3 f4]

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
F1_H, F7_H = 5.7, 7.2  # heights of the two result figures (inches), set by the results band
BIG, SMALL = 26, 23  # printed pt; smallest label 21 pt (SMALL - 2), readable at ~1.5 m on A0
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"


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


def finish(fig, ax, name):
    for a in np.atleast_1d(ax):
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
    key = 3 * row + 0.02  # key strip under both panels: 2 case rows + the law
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
            label=r"independent-satellite model, $\tau_n=\Lambda_P/(v_s\left|J_n(S)\right|)$, "
            "no fitted parameters",
        )
        for (S, al, n), I, c, m in zip(
            M.CASES, data, (BLUE, ORANGE, AQUA, YELLOW), M.MARK, strict=False
        ):
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
            ylim=(-0.03, 1.08),
            title=title,
            xlabel=r"time $t/\tau_n$",
        )
    ax[0].set_ylabel(r"satellite intensity $I_n/I_{inc}$")
    ax[1].tick_params(labelleft=False)
    # Shared key under both panels: the simulated cases (2 x 2, after their lead), then the curve
    # they are compared with on a row of its own.
    h, lab = ax[1].get_legend_handles_labels()
    sim = fig.legend(
        h[1:],
        lab[1:],
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
        h[:1],
        lab[:1],
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
    for name, data, law in (
        ("Laue", laue, lambda x: np.sin(np.pi * x) ** 2),
        ("Bragg", bragg, lambda x: np.tanh(np.pi * x) ** 2),
    ):
        dev = [
            np.abs(I - law(al * abs(jv(n, S)) * t)).max()
            for (S, al, n), I in zip(M.CASES, data, strict=False)
        ]
        print(f"f1 {name}: max |TT - expression| per case", " ".join(f"{v:.3f}" for v in dev))


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
    fig, ax = plt.subplots(figsize=(FIG_W, 4.6), constrained_layout=True)
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
        0.26, 3.5e-5, "independent satellites", fontsize=SMALL, color=INK, ha="right", va="bottom"
    )
    ax.text(0.35, 3.5e-5, "coupled satellites", fontsize=SMALL, color=INK, ha="left", va="bottom")
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
    cb.set_label("acoustic amplitude $S$")
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
    fig = plt.figure(figsize=(FIG_W, F7_H), constrained_layout=True)
    grid = fig.add_gridspec(
        2, 3, height_ratios=[1.78, 1.0], hspace=0.18
    )  # PR #9: show the full 2D scan
    ax = fig.add_subplot(grid[0, :])
    im = ax.pcolormesh(
        data["S"], data["rise"], data["excess"], shading="nearest", cmap="YlOrRd", vmin=0
    )
    cb = fig.colorbar(im, ax=ax, pad=0.02, fraction=0.045)
    cb.set_label(r"$\Delta I/I_{inc}$")
    # the map is the reduced coupling law over the scanned grid; only A-C are checked against full TT
    ax.set(
        xlabel=r"final acoustic amplitude $S$",
        ylabel=r"rise time $T_{rise}/t_{tr}$",
        title=r"Reduced model, Laue, $n=1$, $L=\Lambda_P/2$:  $\Delta I=I_{max}-I_{steady}$",
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
        ax.plot(S, rise, "o", color=color, mec="white", mew=2, ms=13)
        ax.annotate(
            letter,
            (S, rise),
            xytext=(9, 9),
            textcoords="offset points",
            fontsize=BIG,
            fontweight="bold",
            color=INK,
        )
        a = fig.add_subplot(grid[1, ord(letter) - ord("A")])
        a.plot(data[f"{letter}_t"], data[f"{letter}_I"], color=color)
        a.plot(
            data[f"{letter}_tt_t"][::3],
            data[f"{letter}_tt_I"][::3],
            "o",
            color=color,
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
            a.text(tb, case["steady"] - 0.06, r"$\Delta I$", fontsize=SMALL, ha="center", va="top")
        # headroom above every curve (max 0.6) for the two-line case label, which has no backing box
        a.set(xlabel=r"time $t/t_{tr}$", ylim=(-0.025, 1.3), yticks=[0, 0.5, 1])
        a.set_title(
            label, color=color, fontsize=SMALL - 2, fontweight="bold"
        )  # colour = map marker
        peak, steady = case["peak"], case["steady"]
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
        figsize=(FIG_W, 0.33 * FIG_W),
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
    axb.set_xticklabels([f"{k:+d}" if k else "0" for k in n])
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
        ax.text(4.5, -0.55, wave, ha="center", va="top", fontsize=SMALL, color=BLUE)
        ax.text(4.5, -1.55, bc, ha="center", va="top", fontsize=SMALL)
        ax.text(4.5, -2.45, how, ha="center", va="top", fontsize=SMALL, color=INK2)
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "f9_geometry.png")
    print("wrote", OUT / "f9_geometry.png")


if __name__ == "__main__":
    for name in sys.argv[1:] or ["f0", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9"]:
        globals()[name]()
