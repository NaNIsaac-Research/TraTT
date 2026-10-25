"""A short movie of acoustic satellites forming while the sound wave enters the crystal.

Run: python examples/satellite_movie.py [--out DIR]

Conditions are those of notebook Entry 24 (Laue, S = 3, alpha = 3, alpha_ac = 60,
R = 0.05): one front drives satellites n = 1, 2, 3 through different stages at once. Each
order is shown within +-40 of its centre n*q (q = 377), the window Entry 24 used, because at
alpha_ac = 60 a satellite is far narrower than the spacing between satellites. Full
Takagi-Taupin at every frame, nothing interpolated between frames; the I(eta, t) cube is
cached in DIR so restyling does not rerun it. No random numbers are involved; the cube takes
about three minutes on one core.

The movie, 18 s at 30 fps, has four shots:

1. 0-2 s, before the sound: the crystal, the X-rays passing through it, and the rocking
   curve around each order n*q;
2. 2-13 s, the sound enters: the lattice displacement phi = h.u behind the front, the
   front at z/L = t/t_tr, and below it I(eta, t) around each order filling in up to the
   current instant, which the rocking curve on the right shows. Slow time runs as
   (frame)^1.4, so the front enters slowly and the frames are never more than 0.005 t_tr
   apart. Each satellite is marked when its centre reaches its first maximum, at
   t/t_tr = 1 / (2 alpha |J_n(S)|) by the law of README result 1;
3. 13-18 s, the centre intensity of satellites 1, 2 and 3 against time: the full TT
   calculation as points, I_n = sin^2(pi alpha |J_n(S)| t/t_tr) as lines; the Bragg
   peak n = 0, which the law does not cover, in grey;
4. a fade back to the first frame, so that the movie loops.

Captions are not in the movie: the shot times above are where nanisaac.github.io shows
them.

Writes DIR/tratt-satellites.mp4 (960x540, H.264, no audio) and DIR/tratt-satellites.png, a
frame of the comparison, the poster. Needs ffmpeg on PATH.
"""

import argparse
import subprocess
import sys
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from scipy.special import jv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from tratt.core import required_nz
from tratt.cube import rocking_cube
from tratt.drive import Drive

ALPHA, S, ALPHA_AC = 3.0, 3.0, 60.0
ORDERS = (3, 2, 1, 0)  # top to bottom
WINDOW, N_WIN = 40.0, 161  # eta - n*q within +-WINDOW
OFF = 0.0037  # keeps samples off whole acoustic periods (notebook Entry 2)
FPS, BEFORE, GROW, HOLD, COMPARE, FADE = 30, 60, 330, 15, 135, 15  # frames
LENGTH = BEFORE + GROW + HOLD + COMPARE
N_T = GROW

W, H, DPI = 960, 540, 100
PAPER, SURFACE, INK, MUTED, ACCENT, NAVY = (
    "#e8e8e3",
    "#dcdcd6",
    "#181715",
    "#63625c",
    "#bfb21a",
    "#4b5e86",
)
ORDER_COLOURS = {1: NAVY, 2: "#b5562d", 3: "#3d7a55"}


def times() -> np.ndarray:
    return np.linspace(0.0, 1.0, N_T) ** 1.4 + OFF


def first_maximum(n: int) -> float:
    return 1.0 / (2 * ALPHA * abs(jv(n, S)))


def compute(cache: Path) -> dict[str, np.ndarray]:
    """``I`` has shape ``(N_T, len(ORDERS), N_WIN)``: time, order, offset ``eta - n q``."""
    if cache.exists():
        return dict(np.load(cache))
    drive = Drive(S=S, alpha_ac=ALPHA_AC)
    offset = np.linspace(-WINDOW, WINDOW, N_WIN)
    eta = np.concatenate([n * drive.q + offset for n in ORDERS])
    t = times()
    n_z = required_nz(ALPHA, ALPHA_AC, S=S, eta_max=float(np.abs(eta).max()))
    I = rocking_cube(ALPHA, drive, eta, t, geometry="laue", n_z=n_z)
    data = {
        "offset": offset,
        "t": t,
        "I": I.reshape(N_T, len(ORDERS), N_WIN),
        "orders": np.array(ORDERS),
        "n_z": np.array(n_z),
    }
    cache.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(cache, **data)
    return data


def style() -> None:
    for f in sorted((ROOT / "poster" / "fonts").glob("IBMPlexSans-*.ttf")):
        mpl.font_manager.fontManager.addfont(str(f))
    mpl.rcParams.update(
        {
            "font.family": "IBM Plex Sans",
            "font.size": 11,
            "text.color": INK,
            "axes.labelcolor": MUTED,
            "axes.edgecolor": MUTED,
            "axes.linewidth": 0.8,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.facecolor": PAPER,
            "axes.facecolor": PAPER,
        }
    )


def ease(x: float) -> float:
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def pixels(fig) -> np.ndarray:
    fig.canvas.draw()
    return np.asarray(fig.canvas.buffer_rgba(), dtype=np.float32)[..., :3]


def growth(data: dict[str, np.ndarray]):
    """The crystal and the rocking curves while the sound enters; a function of the frame."""
    drive = Drive(S=S, alpha_ac=ALPHA_AC)
    offset, t, I = data["offset"], data["t"], data["I"]

    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI)
    left, right = 0.085, 0.655
    ax_slab = fig.add_axes((left, 0.70, right - left, 0.12))
    zeta = np.linspace(0.0, 1.0, 2400)
    phase = LinearSegmentedColormap.from_list("phase", [NAVY, SURFACE, ACCENT])
    slab = ax_slab.imshow(
        np.zeros((1, zeta.size)),
        extent=(0, 1, 0, 1),
        aspect="auto",
        cmap=phase,
        vmin=-S,
        vmax=S,
        interpolation="antialiased",
    )
    ax_slab.set(xlim=(0, 1), ylim=(0, 1), yticks=[])
    ax_slab.xaxis.tick_top()
    ax_slab.set_xticks([0, 0.5, 1])
    for side in ("left", "right", "bottom", "top"):
        ax_slab.spines[side].set_visible(True)
        ax_slab.spines[side].set_color(INK)
    fig.text(left, 0.935, "Crystal, Laue geometry", fontsize=13, va="center")
    fig.text(
        left,
        0.89,
        "lattice displacement h·u of the sound wave, against depth  z / L",
        color=MUTED,
        va="center",
    )
    arrow = {"arrowstyle": "-|>", "color": MUTED, "lw": 1.0}
    fig.add_artist(
        mpl.patches.FancyArrowPatch(
            (0.012, 0.76), (left - 0.008, 0.76), transform=fig.transFigure, **arrow
        )
    )
    fig.text(0.012, 0.735, "X-rays", color=MUTED, fontsize=9, va="top")
    flash = ax_slab.axvspan(0, 0.012, color=ACCENT, alpha=0.0, lw=0)
    flash_label = ax_slab.text(
        0.015, 0.5, "laser pulse: sound starts here", va="center", fontsize=10, color=INK, alpha=0.0
    )
    front = ax_slab.axvline(0, color=ACCENT, lw=3.0, alpha=0.0)
    front_label = ax_slab.text(
        0, -0.28, "front  z = v_s t", ha="center", va="top", fontsize=10, color=INK, alpha=0.0
    )

    bottom, top, gap = 0.115, 0.585, 0.022
    band = (top - bottom - gap * (len(ORDERS) - 1)) / len(ORDERS)
    ink = LinearSegmentedColormap.from_list("ink", [PAPER, INK])
    ink.set_bad(PAPER)
    edges = np.concatenate([[0.0], (t[1:] + t[:-1]) / 2, [t[-1] + (t[-1] - t[-2]) / 2]])
    o_edges = np.linspace(offset[0], offset[-1], N_WIN + 1)
    maps, curves, cursors, marks = [], [], [], {}
    for j, n in enumerate(ORDERS):
        y0 = top - (j + 1) * band - j * gap
        ax_map = fig.add_axes((left, y0, right - left, band))
        ax_rc = fig.add_axes((0.70, y0, 0.27, band), sharey=ax_map)
        maps.append(
            ax_map.pcolormesh(
                edges,
                o_edges,
                np.ma.masked_array(np.zeros((N_WIN, N_T)), mask=True),
                cmap=ink,
                vmin=0,
                vmax=1,
                shading="flat",
                rasterized=True,
            )
        )
        ax_map.set(xlim=(0, 1), ylim=(offset[0], offset[-1]), yticks=[])
        ax_map.set_ylabel(f"n = {n}", rotation=0, ha="right", va="center", color=INK)
        cursors.append(ax_map.axvline(0, color=ACCENT, lw=2.2))
        curves.append(ax_rc.plot(np.zeros(N_WIN), offset, color=INK, lw=1.2)[0])
        ax_rc.set(xlim=(0, 1.05), xticks=[0, 0.5, 1])
        ax_rc.tick_params(labelleft=False)
        last = j == len(ORDERS) - 1
        ax_map.tick_params(labelbottom=last)
        ax_rc.tick_params(labelbottom=last)
        if n:
            tn = first_maximum(n)
            tick = ax_map.plot(
                [tn],
                [offset[-1]],
                marker="v",
                color=ORDER_COLOURS[n],
                ms=7,
                clip_on=False,
                alpha=0.0,
            )[0]
            note = ax_map.text(
                tn + 0.012,
                offset[-1] - 6,
                f"n = {n} at its first maximum, t = {tn:.2f}",
                va="top",
                fontsize=9.5,
                color=ORDER_COLOURS[n],
                alpha=0.0,
            )
            marks[n] = (tn, tick, note)
        if j == 0:
            ax_map.set_title(
                "Rocking curve over time, ±40 in η around each satellite nq",
                loc="left",
                fontsize=13,
                pad=8,
            )
            ax_rc.set_title("Now", loc="left", fontsize=13, pad=8)
        if last:
            ax_map.set_xticks([0, 0.5, 1])
            ax_map.set_xlabel("time  t / t$_{\\rm tr}$", labelpad=3)
            ax_rc.set_xlabel("intensity  I", labelpad=3)
    link = mpl.lines.Line2D(
        [0, 0], [0, 0], transform=fig.transFigure, color=ACCENT, lw=1.0, ls=(0, (3, 3))
    )
    fig.add_artist(link)
    clock = fig.text(0.70, 0.785, "", fontsize=20, va="center")
    fig.text(
        0.70,
        0.715,
        f"S = {S:g},  α = L/Λ$_{{\\rm P}}$ = {ALPHA:g},  L/Λ$_{{\\rm ac}}$ = {ALPHA_AC:g}",
        color=MUTED,
        fontsize=10,
    )

    def draw(f: int) -> np.ndarray:
        k = min(max(f - BEFORE, -1), N_T - 1)  # -1: before the sound
        tk = 0.0 if k < 0 else t[k]
        entered = min(1.0, (f - BEFORE + 20) / 20)
        slab.set_data(drive.phi(tk)(zeta)[None, :] if k >= 0 else np.zeros((1, zeta.size)))
        flash.set_alpha(0.9 * max(0.0, 1 - abs(f - BEFORE) / 20))
        flash_label.set_alpha(ease(min((f - BEFORE + 25) / 10, (BEFORE + 60 - f) / 15)))
        front.set_xdata([min(tk, 1.0)] * 2)
        front.set_alpha(max(0.0, entered))
        front_label.set_position((min(max(tk, 0.06), 0.94), -0.28))
        front_label.set_alpha(ease(min((f - BEFORE - 20) / 15, (BEFORE + 200 - f) / 20)))
        for j in range(len(ORDERS)):
            img = np.ma.masked_array(np.zeros((N_WIN, N_T)), mask=True)
            if k >= 0:
                img[:, : k + 1] = I[: k + 1, j].T
            maps[j].set_array(img)
            cursors[j].set_xdata([tk] * 2)
            cursors[j].set_alpha(max(0.0, entered))
            curves[j].set_xdata(I[max(k, 0), j])  # before the sound: the first sample, t = OFF
        for tn, tick, note in marks.values():
            since = (tk - tn) / 0.01 if k >= 0 else -1
            tick.set_alpha(1.0 if since >= 0 else 0.0)
            # the note stays for a second and a half after the satellite peaks, then goes
            shown = 0 <= since and f <= BEFORE + np.searchsorted(t, tn) + 45
            note.set_alpha(ease(since / 3) if shown else 0.0)
        x = left + (right - left) * min(tk, 1.0)
        link.set_data([x, x], [top, 0.70])
        link.set_alpha(max(0.0, entered))
        clock.set_text(f"t = {tk:.2f} t$_{{\\rm tr}}$")
        return pixels(fig)

    return draw


def comparison(data: dict[str, np.ndarray]):
    """Centre intensity of each order against time, the full TT beside the formation law."""
    t, I = data["t"], data["I"]
    centre = I[:, :, N_WIN // 2]
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI)
    ax = fig.add_axes((0.085, 0.14, 0.62, 0.66))
    fine = np.linspace(0, 1, 400)
    every = np.unique(np.searchsorted(t, np.linspace(t[0], t[-1], 34)))
    order_index = {n: j for j, n in enumerate(ORDERS)}
    ax.plot(t, centre[:, order_index[0]], color="#a5a49d", lw=1.2, zorder=1)
    pieces = []
    for n in (1, 2, 3):
        c, tn = ORDER_COLOURS[n], first_maximum(n)
        law = ax.plot(fine, np.sin(np.pi * ALPHA * abs(jv(n, S)) * fine) ** 2, color=c, lw=1.6)[0]
        dots = ax.plot(
            t[every], centre[every, order_index[n]], "o", color=c, ms=4.5, mfc=PAPER, mew=1.3
        )[0]
        mark = ax.axvline(tn, color=c, lw=1.0, ls=(0, (3, 3)), ymax=0.93)
        # n = 1 and n = 3 peak close together: their labels go to either side of the mark
        side = {1: ("right", -0.008), 2: ("center", 0.0), 3: ("left", 0.008)}[n]
        label = ax.text(
            tn + side[1],
            1.08,
            f"n = {n}\n{tn:.2f}",
            ha=side[0],
            va="bottom",
            color=c,
            fontsize=10.5,
        )
        pieces.append((tn, law, dots, mark, label))
    ax.set(xlim=(0, 1.0), ylim=(0, 1.05), xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.5, 1])
    ax.set_xlabel("time  t / t$_{\\rm tr}$")
    ax.set_ylabel("intensity at the centre  η = nq")
    fig.text(0.085, 0.935, "Each satellite peaks at its own time", fontsize=15, va="center")
    fig.text(
        0.085,
        0.89,
        "first maximum at t / t$_{\\rm tr}$ = 1 / (2α|J$_n$(S)|), "
        "set by the sound amplitude S, not by the crystal thickness",
        color=MUTED,
        va="center",
    )
    key = fig.add_axes((0.75, 0.38, 0.22, 0.26))
    key.set_axis_off()
    key.plot([0.02, 0.2], [0.8, 0.8], color=INK, lw=1.6)
    key.text(0.26, 0.8, "sin²(πα|J$_n$(S)| t / t$_{\\rm tr}$)", va="center", fontsize=10)
    key.plot([0.11], [0.45], "o", color=INK, ms=4.5, mfc=PAPER, mew=1.3)
    key.text(0.26, 0.45, "full Takagi–Taupin", va="center", fontsize=10)
    key.plot([0.02, 0.2], [0.1, 0.1], color="#a5a49d", lw=1.2)
    key.text(
        0.26,
        0.1,
        "n = 0, the Bragg peak\n(the law is for n ≥ 1)",
        va="center",
        fontsize=10,
        color="#8b8a83",
    )
    key.set(xlim=(0, 1), ylim=(0, 1))

    def draw(k: int) -> np.ndarray:
        for i, (_, law, dots, mark, label) in enumerate(pieces):
            shown = ease((k - 12 * i) / 18)
            for artist in (law, dots, mark, label):
                artist.set_alpha(shown)
        return pixels(fig)

    return draw


def render(data: dict[str, np.ndarray], out: Path) -> None:
    style()
    grow = growth(data)
    compare = comparison(data)
    out.mkdir(parents=True, exist_ok=True)
    movie = out / "tratt-satellites.mp4"
    ffmpeg = subprocess.Popen(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-s",
            f"{W}x{H}",
            "-r",
            str(FPS),
            "-i",
            "-",
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "slow",
            "-crf",
            "24",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(movie),
        ],
        stdin=subprocess.PIPE,
    )
    assert ffmpeg.stdin is not None
    first = grow(0)
    start = BEFORE + GROW + HOLD  # the comparison fades in over the last frames of the hold
    for f in range(LENGTH):
        if f < start - FADE:
            picture = grow(f)
        elif f < start:
            w = (f - (start - FADE) + 1) / (FADE + 1)
            picture = (1 - w) * grow(f) + w * compare(f - start)
        else:
            picture = compare(f - start)
            if f == start + 90:
                plt.imsave(out / "tratt-satellites.png", picture.astype(np.uint8))
        if f >= LENGTH - FADE:  # back to the first frame, so that the loop has no seam
            w = (f - (LENGTH - FADE) + 1) / FADE
            picture = (1 - w) * picture + w * first
        ffmpeg.stdin.write(np.clip(np.rint(picture), 0, 255).astype(np.uint8).tobytes())
    ffmpeg.stdin.close()
    if ffmpeg.wait():
        raise SystemExit("ffmpeg failed")
    print(f"{movie} ({movie.stat().st_size / 1e6:.2f} MB)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render the satellite-formation movie.")
    parser.add_argument("--out", type=Path, default=ROOT / "data" / "movie")
    args = parser.parse_args()
    render(compute(args.out / "satellite_cube.npz"), args.out)


if __name__ == "__main__":
    main()
