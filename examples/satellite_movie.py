"""A short movie of acoustic satellites forming while the sound wave enters the crystal.

Run: python examples/satellite_movie.py [--out DIR]

Conditions are those of notebook Entry 24 (Laue, S = 3, alpha = 3, alpha_ac = 60,
R = 0.05): one front drives satellites n = 1, 2, 3 through different stages at once. Each
order is shown within +-40 of its centre n*q (q = 377), the window Entry 24 used, because at
alpha_ac = 60 a satellite is far narrower than the spacing between satellites. Full
Takagi-Taupin at every frame, nothing interpolated between frames; the I(eta, t) cube is
cached in DIR so restyling does not rerun it. No random numbers are involved; the cube takes
about two minutes on one core.

Layout: top, the crystal with the lattice displacement phi = h.u the solver sees (depth runs
left to right); bottom, I(eta, t) around each order filling in as time runs, its time axis
under the depth axis because the front sits at z/L = t/t_tr; right, the rocking curve of the
current instant on the same eta windows.

Writes DIR/tratt-satellites.mp4 (960x540, H.264, no audio) and DIR/tratt-satellites.png, the
final frame, which the movie also holds for its last seconds. Needs ffmpeg on PATH.
"""

import argparse
import subprocess
import sys
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from tratt.core import required_nz
from tratt.cube import rocking_cube
from tratt.drive import Drive

ALPHA, S, ALPHA_AC = 3.0, 3.0, 60.0
ORDERS = (3, 2, 1, 0)  # top to bottom
WINDOW, N_WIN = 40.0, 161  # eta - n*q within +-WINDOW
N_T = 216
OFF = 0.0037  # keeps samples off whole acoustic periods (notebook Entry 2)
FPS, HOLD = 24, 36  # 9 s of growth, then 1.5 s on the final frame

W, H, DPI = 960, 540, 100
PAPER, SURFACE, INK, MUTED, ACCENT, NAVY = (
    "#e8e8e3",
    "#dcdcd6",
    "#181715",
    "#63625c",
    "#bfb21a",
    "#4b5e86",
)


def compute(cache: Path) -> dict[str, np.ndarray]:
    """``I`` has shape ``(N_T, len(ORDERS), N_WIN)``: time, order, offset ``eta - n q``."""
    if cache.exists():
        return dict(np.load(cache))
    drive = Drive(S=S, alpha_ac=ALPHA_AC)
    offset = np.linspace(-WINDOW, WINDOW, N_WIN)
    eta = np.concatenate([n * drive.q + offset for n in ORDERS])
    t = np.linspace(0.0, 1.0, N_T) + OFF
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


def render(data: dict[str, np.ndarray], out: Path) -> None:
    style()
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
    front = ax_slab.axvline(0, color=INK, lw=1.6)

    bottom, top, gap = 0.115, 0.585, 0.022
    band = (top - bottom - gap * (len(ORDERS) - 1)) / len(ORDERS)
    ink = LinearSegmentedColormap.from_list("ink", [PAPER, INK])
    ink.set_bad(PAPER)
    dt = t[1] - t[0]
    maps, curves, cursors = [], [], []
    for j, n in enumerate(ORDERS):
        y0 = top - (j + 1) * band - j * gap
        ax_map = fig.add_axes((left, y0, right - left, band))
        ax_rc = fig.add_axes((0.70, y0, 0.27, band), sharey=ax_map)
        maps.append(
            ax_map.imshow(
                np.full((N_WIN, N_T), np.nan),
                extent=(t[0] - dt / 2, t[-1] + dt / 2, offset[0], offset[-1]),
                origin="lower",
                aspect="auto",
                cmap=ink,
                vmin=0,
                vmax=1,
                interpolation="antialiased",
            )
        )
        ax_map.set(xlim=(0, 1), ylim=(offset[0], offset[-1]), yticks=[])
        ax_map.set_ylabel(f"n = {n}", rotation=0, ha="right", va="center", color=INK)
        cursors.append(ax_map.axvline(0, color=ACCENT, lw=1.6))
        curves.append(ax_rc.plot(np.zeros(N_WIN), offset, color=INK, lw=1.2)[0])
        ax_rc.set(xlim=(0, 1.05), xticks=[0, 0.5, 1])
        ax_rc.tick_params(labelleft=False)
        last = j == len(ORDERS) - 1
        ax_map.tick_params(labelbottom=last)
        ax_rc.tick_params(labelbottom=last)
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

    def draw(k: int) -> np.ndarray:
        tk = t[k]
        slab.set_data(drive.phi(tk)(zeta)[None, :])
        front.set_xdata([min(tk, 1.0)] * 2)
        for j in range(len(ORDERS)):
            img = np.full((N_WIN, N_T), np.nan)
            img[:, : k + 1] = I[: k + 1, j].T
            maps[j].set_data(img)
            cursors[j].set_xdata([tk] * 2)
            curves[j].set_xdata(I[k, j])
        x = left + (right - left) * min(tk, 1.0)
        link.set_data([x, x], [top, 0.70])
        clock.set_text(f"t = {tk:.2f} t$_{{\\rm tr}}$")
        fig.canvas.draw()
        return np.asarray(fig.canvas.buffer_rgba())[..., :3]

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
    for k in range(N_T - 1):
        ffmpeg.stdin.write(draw(k).tobytes())
    final = draw(N_T - 1)
    for _ in range(1 + HOLD):
        ffmpeg.stdin.write(final.tobytes())
    ffmpeg.stdin.close()
    if ffmpeg.wait():
        raise SystemExit("ffmpeg failed")
    plt.imsave(out / "tratt-satellites.png", final)
    print(f"{movie} ({movie.stat().st_size / 1e6:.2f} MB)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render the satellite-formation movie.")
    parser.add_argument("--out", type=Path, default=ROOT / "data" / "movie")
    args = parser.parse_args()
    render(compute(args.out / "satellite_cube.npz"), args.out)


if __name__ == "__main__":
    main()
