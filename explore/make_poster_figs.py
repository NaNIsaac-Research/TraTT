"""Poster-only figures, drawn at print size for one A0 column. Run: python explore/make_poster_figs.py [f0 f1 f2 f3 f4]

Width FIG_W is the inner width of a poster card (poster/build.py SPEC), so a font size here is the
printed size. Panels reuse the notebook figure code; nothing is recomputed differently.

f0  schematic: Laue slab, acoustic front filling the crystal, incident / transmitted / satellite beams
f1  filled-depth mapping: Laue sin^2 and Bragg tanh^2 collapse      (make_poster_figure.collapse; Entries 1, 9)
f2  time-resolved rocking curve near n = 1 and its centre cut        (make_map_figure.compute; Entries 22, 23)
f3  path memory: transient-only satellite, up vs down a pulse       (make_memory_figure.panel_a/b; Entries 28, 30)
f4  population error of the independent-channel picture vs R        (make_phase_figure.merged; Entry 54)
f5  outlook: Fourier weight / kinematic law (Entry 59, e58 data) and the satellite weight of the
    first-order forms against full TT (Entry 64, e64_sw.json); reads stored results only
f6  introductory Bessel coupling weights for a sinusoidal grating
f7  linear-ramp overshoot map and three TT-checked traces (Entry 67)
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
for _f in sorted((ROOT / "poster" / "fonts").glob("*.ttf")):  # same typeface as the poster text
    mpl.font_manager.fontManager.addfont(str(_f))
FONT = "IBM Plex Sans"  # same face as poster/build.py (f1 still carries Source Sans 3: redrawing it reruns TT)

FIG_W = 14.4  # inches = poster card inner width (~366 mm)
INTRO_W = 12.5  # inches = left column of the introduction band (~317 mm)
F1_H, F7_H = 7.15, 8.35  # heights of the two result figures (inches), set by the results band
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
            "savefig.facecolor": "none",
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
    """Schematic for half a wide card (text sits on the other half), so FIG_W / 2 wide.

    Everything here is computed, like the other four figures: the profile inside the slab is
    `Drive.phi(t)` sampled in depth, and the curve on the right is a real `rocking()` of that
    same snapshot, turned on its side so each satellite peak faces the beam it belongs to.
    The earlier version drew sine curves wiggling along the transverse direction, i.e. the
    modulation varying across the beam rather than with depth -- the opposite of the drive.
    """
    style()
    LAB, KEY = BIG + 4, BIG + 8  # the lead schematic of the introduction, read from a distance
    alpha, S, alpha_ac, t = 0.6, 1.5, 5.0, 0.62
    d = Drive(S=S, alpha_ac=alpha_ac)

    fig, (ax, axr) = plt.subplots(
        1,
        2,
        figsize=(INTRO_W, 0.35 * INTRO_W),
        constrained_layout=True,
        gridspec_kw=dict(width_ratios=[2.5, 1.0], wspace=0.0),
    )

    ax.set(xlim=(-3.3, 9.6), ylim=(-0.3, 10.4))
    ax.axis("off")
    x0, x1, y0, y1 = 0.0, 6.0, 2.1, 8.1  # slab; depth zeta runs left to right
    xf = x0 + t * (x1 - x0)  # acoustic front
    ymid = 0.5 * (y0 + y1)

    ax.add_patch(plt.Rectangle((x0, y0), x1 - x0, y1 - y0, fc="#f4f7fb", ec=INK2, lw=1.6, zorder=1))
    ax.add_patch(plt.Rectangle((x0, y0), xf - x0, y1 - y0, fc="#e7effa", ec="none", zorder=1))

    zz = np.linspace(0.0, 1.0, 1200)
    phi = d.phi(t)(zz)
    amp = 0.33 * (y1 - y0) / max(abs(phi).max(), 1e-9)
    # Draw the propagating acoustic displacement only where the wave has arrived.
    # A flat phi=0 line ahead of the front can be mistaken for the X-ray path.
    vibrating = zz <= t
    ax.plot(
        x0 + zz[vibrating] * (x1 - x0),
        ymid + amp * phi[vibrating],
        color=BLUE,
        lw=2.8,
        zorder=3,
        solid_capstyle="round",
    )
    ax.plot([xf, xf], [y0, y1], color=BLUE, lw=2.4, ls=(0, (4, 3)), zorder=4)
    # Separate the physical sound field (blue oscillation) from the X-ray probe
    # (dark straight incoming arrow) using a directly associated label.
    ax.text(
        x0 + 1.57,
        y1 + 0.36,
        "acoustic wave",
        color=BLUE,
        ha="center",
        va="bottom",
        fontsize=LAB - 4,
        fontweight="medium",
    )

    # transducer on the lower part of the entrance face, so the beam enters clear of it
    ty = y0 + 0.58 * (y1 - y0)
    ax.add_patch(plt.Rectangle((x0 - 0.44, y0), 0.44, ty - y0, fc=INK2, ec="none", zorder=2))
    ax.text(
        x0 - 0.62, 0.5 * (y0 + ty), "transducer", ha="right", va="center", fontsize=LAB, color=INK2
    )

    # front marker, and the two regions it separates
    ax.annotate(
        "",
        xy=(xf + 1.25, y1 + 0.70),
        xytext=(xf, y1 + 0.70),
        arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.2, mutation_scale=22),
    )
    ax.text(xf + 1.45, y1 + 0.70, r"$v_s$", color=BLUE, va="center", fontsize=KEY)
    ax.text(xf, y1 + 1.55, "wavefront", color=BLUE, ha="center", va="bottom", fontsize=LAB)
    ax.text(
        0.5 * (xf + x1) + 0.1,
        ymid,
        "unstrained",
        color=INK2,
        ha="center",
        va="center",
        rotation=90,
        fontsize=LAB - 3,
    )

    # one dimension row: the slab thickness, with the filled part picked out on the same line
    yd = y0 - 0.72
    ax.annotate(
        "",
        xy=(x1, yd),
        xytext=(x0, yd),
        arrowprops=dict(arrowstyle="<|-|>", color=INK2, lw=1.2, mutation_scale=13),
    )
    for x in (x0, xf, x1):
        ax.plot([x, x], [yd - 0.22, yd + 0.22], color=INK2, lw=1.1)
    ax.plot([x0, xf], [yd, yd], color=INK, lw=3.2, solid_capstyle="butt")
    ax.text(x1 + 0.22, yd, r"$L$", ha="left", va="center", fontsize=LAB, color=INK2)
    ax.text(
        0.5 * (x0 + xf),
        yd - 0.38,
        r"vibrating depth $v_s t$",
        ha="center",
        va="top",
        fontsize=LAB,
        color=INK,
    )

    # beams: in above the transducer, forward and diffracted out
    ax.annotate(
        "",
        xy=(x0 + 0.08, ymid + 1.25),
        xytext=(-2.8, ymid + 2.85),
        arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.8, mutation_scale=26),
        zorder=5,
    )
    ax.text(-2.9, ymid + 3.2, "X-ray", fontsize=KEY, color=INK)
    ax.annotate(
        "",
        xy=(9.0, ymid + 1.65),
        xytext=(x1, ymid + 0.1),
        arrowprops=dict(arrowstyle="-|>", color=INK2, lw=2.4, mutation_scale=22),
    )
    ax.text(9.2, ymid + 1.8, r"$D_0$", va="center", fontsize=KEY, color=INK2)
    ax.annotate(
        "",
        xy=(9.0, ymid - 1.65),
        xytext=(x1, ymid - 0.1),
        arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=3.0, mutation_scale=22),
    )
    ax.text(9.2, ymid - 1.8, r"$D_h$", va="center", fontsize=KEY, color=ORANGE)

    eta = np.linspace(-2.6 * d.q, 2.6 * d.q, 4001)
    I = rocking(alpha, eta, phi=d.phi(t), n_z=required_nz(alpha, alpha_ac))
    axr.plot(I, eta / d.q, color=ORANGE, lw=2.2)
    axr.fill_betweenx(eta / d.q, 0, I, color=ORANGE, alpha=0.16)
    axr.set(xlim=(0, 1.55 * I.max()), ylim=(-2.75, 2.75), xticks=[], yticks=[-2, -1, 0, 1, 2])
    axr.set_xlabel(r"$I(\beta)$", fontsize=LAB, labelpad=1)
    axr.set_ylabel(r"$\beta / K$", fontsize=LAB, labelpad=0)
    axr.tick_params(labelsize=LAB, length=4)
    for s in ("top", "right", "bottom"):
        axr.spines[s].set_visible(False)
    axr.grid(False)
    for n in (0, 1, 2):
        axr.annotate(
            f"$n={n}$",
            (float(np.interp(n * d.q, eta, I)), n),
            fontsize=LAB,
            color=ORANGE,
            va="center",
            xytext=(6, 0),
            textcoords="offset points",
        )

    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "f0_scheme.png", dpi=300)
    print("wrote", OUT / "f0_scheme.png")


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
    # the laws themselves are written in the panel text, so the titles only name the geometry
    for a, data, law, title in (
        (ax[0], laue, np.sin(np.pi * s) ** 2, "Laue geometry"),
        (ax[1], bragg, np.tanh(np.pi * s) ** 2, "Bragg geometry"),
    ):
        # the law is drawn over the TT markers so the comparison stays visible where they crowd
        a.plot(
            s,
            law,
            color=INK,
            lw=2.0,
            zorder=3,
            label="Independent-satellite approximation (no fitted parameters)",
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
                label=rf"$S={S:g},\ \alpha={al:g},\ n={n}$",
            )
        a.set(
            xlim=(0, 2.3),
            ylim=(-0.03, 1.08),
            title=title,
            xlabel=r"$\alpha_n\tilde t$,  $\alpha_n=\alpha\left|J_n(S)\right|$",
        )
    ax[0].set_ylabel(r"centre intensity $I_n$")
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
    lead = "Full TT simulation:"
    probe = fig.text(0, 0, lead, fontsize=SMALL, fontweight="semibold")
    wl = probe.get_window_extent().width / fig.bbox.width
    probe.remove()
    box = sim.get_window_extent()
    ws, top = box.width / fig.bbox.width, box.y1 / fig.bbox.height
    x0 = (1 - wl - 0.012 - ws) / 2  # centre the labelled block under the panels
    fig.text(x0, top, lead, fontsize=SMALL, fontweight="semibold", va="top")
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
    fig, ax = plt.subplots(figsize=(FIG_W, 4.2), constrained_layout=True)
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
        xlabel=r"$R=\Lambda_{ac}/\Lambda_P$",
        ylabel="intensity error",
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
        ylabel=r"$|J_n(S)|$",
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
    cb.set_label(r"overshoot $\Delta I$")
    # the map is the reduced coupling law over the scanned grid; only A-C are checked against full TT
    ax.set(
        xlabel=r"final sound amplitude $S$",
        ylabel=r"rise time $T_{rise}/t_{tr}$",
        title=r"Parameter scan, reduced coupling model: first satellite ($n=1$)",
    )

    def num(v):
        if v >= 0.01:
            return f"{v:.2f}"
        m, e = f"{v:.1e}".split("e")
        return rf"${m}\times10^{{{int(e)}}}$"

    for case, color, label in zip(
        summary["cases"],
        (BLUE, ORANGE, AQUA),
        ("A: monotonic growth", "B: finite overshoot", "C: near-zero steady state"),
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
            a.text(
                tb + 0.08,
                case["steady"] + 0.3 * (float(data["B_I"][k]) - case["steady"]),
                r"$\Delta I$",
                fontsize=SMALL,
                va="center",
                color=INK,
            )
        a.set(xlabel=r"time / $t_{tr}$", ylim=(-0.025, 1.0))  # headroom for the two-line case label
        a.set_title(
            label, color=color, fontsize=SMALL, fontweight="semibold"
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
            bbox=dict(facecolor="white", edgecolor="none", pad=2),
        )
        if letter == "A":
            a.set_ylabel("satellite intensity")
        else:
            a.tick_params(labelleft=False)
        a.grid(color=GRID, lw=1)
        a.set_axisbelow(True)
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "f7_overshoot.png")
    print("wrote", OUT / "f7_overshoot.png")


if __name__ == "__main__":
    for name in sys.argv[1:] or ["f0", "f1", "f2", "f3", "f4", "f5", "f6", "f7"]:
        globals()[name]()
