"""Convergence, limit and boundary-flux checks of the solver, as one table and one figure.

    uv run --extra dev python verify/checks.py

Prints a Markdown table and writes figures/verify_checks.png. Numbers only: what each check
means for the physics is left to the reader. CPU, about five minutes.

Reference point: Laue alpha = 1.3, Bragg alpha = 2.0, drive S = 1.3, alpha_ac = 5. Times
t = 0.437 (front inside the slab, off every grid node) and t = 1.437 (slab filled).
Closed forms come from the matrix exponential of the constant-coefficient system, not from the
formulas in tests/, so they are an independent reference.
"""

import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import expm
from scipy.special import jv

from tratt.core import required_nz, solve_bragg, solve_laue
from tratt.cube import front_and_full, rocking_cube
from tratt.drive import Drive
from tratt.observe import channel_stats, formation_time

ROOT = Path(__file__).resolve().parents[1]
ALPHA = {"laue": 1.3, "bragg": 2.0}
DRIVE = Drive(S=1.3, alpha_ac=5.0)
SMOOTH = Drive(S=1.3, alpha_ac=5.0, rise=0.3)
CHANNELS = (-2, -1, 0, 1, 2)
N_Z = (256, 512, 1024, 2048, 4096)
N_REF = 16384
ETA = np.linspace(-3.0 * DRIVE.q, 3.0 * DRIVE.q, 1201)

rows: list[tuple[str, str, str]] = []


def row(check: str, case: str, result: str) -> None:
    rows.append((check, case, result))
    print(f"  {check} | {case} | {result}", flush=True)


def channel_p(I: np.ndarray, eta: np.ndarray, drive: Drive = DRIVE) -> np.ndarray:
    """p_n for every channel, shape (n_channels,) for one snapshot."""
    return np.array([channel_stats(eta, I[None, :], drive, n).p[0] for n in CHANNELS])


def snapshot(geometry: str, drive: Drive, t: float, n_z: int, eta=ETA) -> np.ndarray:
    phi = drive.phi(t)
    if geometry == "laue":
        return np.abs(solve_laue(ALPHA[geometry], eta, phi=phi, n_z=n_z)[1]) ** 2
    return np.abs(solve_bragg(ALPHA[geometry], eta, phi=phi, n_z=n_z)) ** 2


def plain_ticks(ax, values) -> None:
    ax.set_xticks(values, [f"{v:g}" for v in values])
    ax.minorticks_off()


def orders(errs: np.ndarray) -> np.ndarray:
    return np.log2(errs[:-1] / errs[1:])


def exact_static(geometry: str, alpha: float, eta: np.ndarray) -> np.ndarray:
    """Unmodulated intensity from expm of the constant-coefficient linear system."""
    c = 1j * np.pi * alpha
    out = np.empty(eta.shape)
    for i, e in enumerate(eta):
        if geometry == "laue":
            d = expm(np.array([[0.0, c], [c, 1j * e]])) @ np.array([1.0, 0.0])
            out[i] = abs(d[1]) ** 2
        else:
            # R = y / x with x' = c y, y' = -c x - i eta y, integrated from zeta = 1 (R = 0) to 0
            x, y = expm(-np.array([[0.0, c], [-c, -1j * e]])) @ np.array([1.0, 0.0])
            out[i] = abs(y / x) ** 2
    return out


def bragg_transmission(alpha: float, eta: np.ndarray, phi, n_z: int) -> tuple:
    """Independent RK4 of the linear Bragg system, returning (R(0), T) with T = |D0(1)/D0(0)|^2.

    x' = c e^{+i phi} y, y' = -c e^{-i phi} x - i eta y from zeta = 1 (x = 1, y = 0) to 0: the
    same equations whose Riccati form solve_bragg integrates, so R = y / x must agree with it.
    """
    c = 1j * np.pi * alpha
    x = np.ones(eta.shape, dtype=complex)
    y = np.zeros(eta.shape, dtype=complex)
    h = -1.0 / n_z

    def f(z, x, y):
        e = np.exp(1j * phi(np.float64(z)))
        return c * e * y, -c * np.conj(e) * x - 1j * eta * y

    for i in range(n_z):
        z = 1.0 + i * h
        k1 = f(z, x, y)
        k2 = f(z + h / 2, x + h / 2 * k1[0], y + h / 2 * k1[1])
        k3 = f(z + h / 2, x + h / 2 * k2[0], y + h / 2 * k2[1])
        k4 = f(z + h, x + h * k3[0], y + h * k3[1])
        x = x + h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        y = y + h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
    return y / x, 1.0 / np.abs(x) ** 2


def depth_convergence(ax) -> None:
    print("depth step n_z", flush=True)
    for geometry, marker in (("laue", "o"), ("bragg", "s")):
        for drive, t, label in (
            (DRIVE, 0.437, "step, front inside"),
            (SMOOTH, 0.437, "rise 0.3, front inside"),
            (DRIVE, 1.437, "filled"),
        ):
            ref = channel_p(snapshot(geometry, drive, t, N_REF), ETA)
            errs = np.array(
                [
                    np.max(np.abs(channel_p(snapshot(geometry, drive, t, n), ETA) - ref) / ref)
                    for n in N_Z
                ]
            )
            ax.loglog(N_Z, errs, marker=marker, label=f"{geometry}, {label}")
            o = orders(errs)
            row(
                "depth step",
                f"{geometry} alpha {ALPHA[geometry]}, {label}, t {t}",
                f"max rel. error of p_n (n = -2..2) vs n_z {N_REF}: "
                + ", ".join(f"{e:.1e}" for e in errs)
                + f" at n_z {N_Z[0]}..{N_Z[-1]}; observed order {o.min():.2f} to {o.max():.2f}",
            )
    plain_ticks(ax, N_Z)
    ax.set(xlabel="n_z", ylabel="max rel. error of p_n", title="(a) depth step")
    ax.legend(fontsize=6)


def eta_convergence() -> None:
    print("eta grid", flush=True)
    sizes = (151, 301, 601, 1201, 2401)
    vals = []
    for m in sizes:
        eta = np.linspace(-3.0 * DRIVE.q, 3.0 * DRIVE.q, m)
        vals.append(channel_p(snapshot("laue", DRIVE, 1.437, 2048, eta), eta))
    ref = vals[-1]
    errs = [np.max(np.abs(v - ref) / ref) for v in vals[:-1]]
    row(
        "eta grid",
        "laue alpha 1.3, filled, t 1.437, n_z 2048",
        "max rel. change of p_n vs 2401 points: "
        + ", ".join(f"{m}: {e:.1e}" for m, e in zip(sizes[:-1], errs, strict=True)),
    )


def time_convergence(ax) -> None:
    print("time step", flush=True)
    alpha, eta = ALPHA["laue"], np.linspace(-2.0 * DRIVE.q, 2.0 * DRIVE.q, 401)
    n_z = required_nz(alpha, DRIVE.alpha_ac, S=DRIVE.S, eta_max=float(np.max(np.abs(eta))))
    zero = Drive(S=0.0, alpha_ac=DRIVE.alpha_ac)
    static = rocking_cube(alpha, zero, eta, np.array([0.0]), n_z=n_z)
    per_period = (8, 16, 32, 64, 128)
    t_f = {n: [] for n in (-1, 0, 1)}
    for pp in per_period:
        times = DRIVE.times(t_max=2.0, per_period=pp)
        If, Is = front_and_full(alpha, DRIVE, eta, times, n_z=n_z)
        for n, values in t_f.items():
            p_static = channel_stats(eta, static, zero, n).p[0]
            F = formation_time(
                times,
                channel_stats(eta, If, DRIVE, n).p,
                channel_stats(eta, Is, DRIVE, n).p,
                DRIVE.period,
                p_static=p_static,
            )
            values.append(F.t_f if F.status == "formed" else np.nan)
    for n, v in t_f.items():
        ax.semilogx(per_period, v, marker="o", label=f"n = {n}")
        row(
            "time step",
            f"laue alpha 1.3, t_f of channel {n} (eps 0.05, induced-change scale)",
            ", ".join(f"{pp}/period: {x:.4f}" for pp, x in zip(per_period, v, strict=True))
            + f"; sample spacing {DRIVE.period / per_period[0]:.4f} to {DRIVE.period / per_period[-1]:.5f}",
        )
    plain_ticks(ax, per_period)
    ax.set(xlabel="samples per acoustic period", ylabel="t_f / t_tr", title="(b) time step")
    ax.legend(fontsize=7)


def static_limit(ax) -> None:
    print("S = 0 limit", flush=True)
    eta = np.linspace(-30.0, 30.0, 241)
    zero = Drive(S=0.0, alpha_ac=DRIVE.alpha_ac)
    for geometry in ("laue", "bragg"):
        alpha = ALPHA[geometry]
        exact = exact_static(geometry, alpha, eta)
        for n_z in (512, 2048):
            # through the drive (S = 0, front inside and filled), as the sweeps call it
            for t in (0.437, 1.437):
                cube = rocking_cube(alpha, zero, eta, np.array([t]), geometry=geometry, n_z=n_z)[0]
                err = np.max(np.abs(cube - exact))
                row(
                    "S = 0 limit",
                    f"{geometry} alpha {alpha}, n_z {n_z}, t {t}",
                    f"max abs. diff. from static closed form over |eta| <= 30: {err:.1e}",
                )
        ax.semilogy(
            eta,
            np.abs(
                rocking_cube(alpha, zero, eta, np.array([0.437]), geometry=geometry, n_z=512)[0]
                - exact
            )
            + 1e-18,
            label=f"{geometry}, n_z 512",
        )
    ax.set(xlabel="eta", ylabel="|I - I_static exact|", title="(c) S = 0 against static TT")
    ax.legend(fontsize=7)


def steady_state(ax) -> None:
    print("steady state", flush=True)
    alpha, d = ALPHA["laue"], DRIVE
    eta = np.linspace(-3.0 * d.q, 3.0 * d.q, 601)
    n_z = required_nz(alpha, d.alpha_ac, S=d.S, eta_max=3.0 * d.q)
    t = 1.0 + np.arange(16) / 16 * d.period
    front = rocking_cube(alpha, d, eta, t, n_z=n_z)
    later = rocking_cube(alpha, d, eta, t + d.period, n_z=n_z)
    full = rocking_cube(alpha, d, eta, t, n_z=n_z, steady=True)
    row(
        "steady state",
        "laue alpha 1.3, step, t in [1, 1 + period)",
        f"max |I(t + period) - I(t)|: {np.max(np.abs(later - front)):.1e}; max |I_front - I_steady|: {np.max(np.abs(front - full)):.1e}",
    )

    S, a = 1.5, 0.5
    for n in (0, 1, 2):
        want = np.sin(np.pi * a * abs(jv(n, S))) ** 2
        devs = []
        acs = (5.0, 10.0, 20.0, 40.0)
        for aac in acs:
            dd = Drive(S=S, alpha_ac=aac)
            e = np.array([dd.eta_channel(n)])
            nz = 2 * required_nz(a, aac, S=S, eta_max=abs(e[0]))
            ts = 1.0 + np.arange(8) / 8 * dd.period
            I = rocking_cube(a, dd, e, ts, n_z=nz)[:, 0]
            devs.append(np.max(np.abs(I - want)))
        devs = np.array(devs)
        ax.loglog([a / x for x in acs], devs, marker="o", label=f"n = {n}")
        row(
            "steady state",
            f"laue alpha {a}, S {S}, centre of channel {n} vs sin^2(pi alpha |J_n(S)|) = {want:.4f}",
            "max deviation over one period: "
            + ", ".join(
                f"alpha/alpha_ac {a / x:.4f}: {v:.1e}" for x, v in zip(acs, devs, strict=True)
            )
            + f"; observed order {orders(devs).min():.2f} to {orders(devs).max():.2f}",
        )
    plain_ticks(ax, [a / x for x in acs])
    ax.set(
        xlabel="alpha / alpha_ac",
        ylabel="max |I_centre - sin^2(pi alpha |J_n|)|",
        title="(d) steady state, Bessel slab",
    )
    ax.legend(fontsize=7)


def boundary_flux(ax_laue, ax_bragg) -> None:
    print("boundary flux", flush=True)
    eta = np.linspace(-3.0 * DRIVE.q, 3.0 * DRIVE.q, 601)
    for drive, t, label in (
        (DRIVE, 0.437, "step, front inside"),
        (SMOOTH, 0.437, "rise 0.3, front inside"),
        (DRIVE, 1.437, "filled"),
    ):
        defects = []
        for n_z in N_Z:
            D0, Dh = solve_laue(ALPHA["laue"], eta, phi=drive.phi(t), n_z=n_z)
            defects.append(np.max(np.abs(np.abs(D0) ** 2 + np.abs(Dh) ** 2 - 1.0)))
        ax_laue.loglog(N_Z, defects, marker="o", label=label)
        row(
            "boundary flux",
            f"laue alpha 1.3, {label}, t {t}",
            "max ||D0|^2 + |Dh|^2 - 1| at the exit: "
            + ", ".join(f"{e:.1e}" for e in defects)
            + f" at n_z {N_Z[0]}..{N_Z[-1]}",
        )

    for drive, t, label in ((DRIVE, 0.437, "step, front inside"), (DRIVE, 1.437, "filled")):
        for n_z in (512, 2048):
            r_solver = solve_bragg(ALPHA["bragg"], eta, phi=drive.phi(t), n_z=n_z)
            r_lin, T = bragg_transmission(ALPHA["bragg"], eta, drive.phi(t), n_z)
            R = np.abs(r_lin) ** 2
            row(
                "boundary flux",
                f"bragg alpha 2.0, {label}, t {t}, n_z {n_z}",
                f"max |R + T - 1|: {np.max(np.abs(R + T - 1)):.1e}; max |R_solver - R_linear| (amplitude): {np.max(np.abs(r_solver - r_lin)):.1e}; max R: {R.max():.6f}",
            )
            if n_z == 2048:
                ax_bragg.semilogy(eta, np.abs(R + T - 1) + 1e-18, label=label)
    plain_ticks(ax_laue, N_Z)
    ax_laue.set(xlabel="n_z", ylabel="max ||D0|^2 + |Dh|^2 - 1|", title="(e) Laue energy at exit")
    ax_laue.legend(fontsize=7)
    ax_bragg.set(xlabel="eta", ylabel="|R + T - 1|", title="(f) Bragg R + T, n_z 2048")
    ax_bragg.legend(fontsize=7)


def main() -> None:
    start = time.perf_counter()
    fig, axes = plt.subplots(2, 3, figsize=(15, 8.5))
    depth_convergence(axes[0, 0])
    eta_convergence()
    time_convergence(axes[0, 1])
    static_limit(axes[0, 2])
    steady_state(axes[1, 0])
    boundary_flux(axes[1, 1], axes[1, 2])
    fig.suptitle("TraTT solver checks (verify/checks.py)")
    fig.tight_layout()
    out = ROOT / "figures" / "verify_checks.png"
    fig.savefig(out, dpi=130)
    print("\n| check | case | result |\n|---|---|---|")
    for r in rows:
        print("| " + " | ".join(r) + " |")
    print(f"\nwrote {out.relative_to(ROOT)}; {time.perf_counter() - start:.0f} s")


if __name__ == "__main__":
    main()
