"""Entry 67 worker audit: direct depth quadrature, TT convergence, saved-map comparison.

Run: .venv/Scripts/python.exe explore/nb/e67_worker_audit.py
Writes e67_worker_audit.json and e67_worker_audit.log next to this file.
"""

from __future__ import annotations

import json
import platform
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
from scipy.special import jv

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "explore" / "nb"))

from e67_overshoot_map import intensity as map_law  # noqa: E402  (read-only import)

from tratt.core import required_nz, rocking, solve_laue  # noqa: E402

ALPHA, AAC = 0.5, 40.0
Q = 2 * np.pi * AAC
CASES = [
    ("A", 1.5, 1.0),
    ("B", 3.0, 1.0),
    ("C", 3.85, 2.0),
    ("map_max", 3.8, 4.0),
    ("short_rise", 6.0, 0.05),
]
TOL = 1e-3  # task threshold: larger differences become findings
HERE = Path(__file__).resolve().parent
LOG = open(HERE / "e67_worker_audit.log", "a", encoding="utf-8")  # append: keep earlier runs
T0 = time.perf_counter()


def say(*parts):
    line = " ".join(str(p) for p in parts)
    print(line, flush=True)
    LOG.write(f"[{time.perf_counter() - T0:7.1f}s] {line}\n")
    LOG.flush()


# ---- approximation, computed directly ----------------------------------------


def theta_direct(S, T, t):
    """int_0^1 J1(S clip((t - zeta)/T, 0, 1)) dzeta, piecewise with adaptive quad.

    Depth zeta > t: envelope not arrived (zero). t-T < zeta < t: ramp. zeta < t-T: full.
    """
    a = float(np.clip(t - T, 0.0, 1.0))
    b = float(np.clip(t, 0.0, 1.0))
    full = a * jv(1, S)
    if b <= a:
        return full
    ramp, _ = quad(lambda z: jv(1, S * (t - z) / T), a, b, epsabs=1e-13, epsrel=1e-13, limit=200)
    return full + ramp


def I_direct(S, T, t):
    return np.sin(np.pi * ALPHA * theta_direct(S, T, t)) ** 2


def peak_direct(S, T, nt=2001):
    """Grid argmax then bounded refinement; returns (t_peak, I_peak)."""
    times = np.linspace(0, 1 + T, nt)
    vals = np.array([I_direct(S, T, t) for t in times])
    k = int(np.argmax(vals))
    lo, hi = times[max(k - 2, 0)], times[min(k + 2, nt - 1)]
    r = minimize_scalar(
        lambda t: -I_direct(S, T, t), bounds=(lo, hi), method="bounded", options={"xatol": 1e-10}
    )
    if -r.fun >= vals[k]:
        return float(r.x), float(-r.fun)
    return float(times[k]), float(vals[k])


# ---- full TT, independent phase-average wrapper -------------------------------


def tt_phase_avg(S, T, times, phases, nz):
    """Carrier-phase average at fixed envelope time; eta = +q only, no time smoothing."""
    tt = np.asarray(times, dtype=float)[:, None, None]
    pp = (np.arange(phases) * 2 * np.pi / phases)[None, :, None]

    def phi(z):
        return S * np.clip((tt - z) / T, 0.0, 1.0) * np.sin(Q * (z - tt) + pp)

    I = rocking(ALPHA, np.array([Q]), phi=phi, n_z=nz)  # (nt, phases, 1)
    return I[..., 0].mean(axis=1)


def main():
    head = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True
    ).stdout.strip()
    say("==== run start ====")
    say(
        "e67 worker audit",
        date.today().isoformat(),
        "python",
        platform.python_version(),
        "numpy",
        np.__version__,
        "scipy",
        scipy.__version__,
        "HEAD",
        head,
    )
    say("command: .venv/Scripts/python.exe explore/nb/e67_worker_audit.py")
    saved = json.loads((HERE / "e67_overshoot.json").read_text(encoding="utf-8"))
    npz = np.load(HERE / "e67_overshoot.npz")
    out = dict(
        date=date.today().isoformat(),
        git_head=head,
        alpha=ALPHA,
        alpha_ac=AAC,
        python=platform.python_version(),
        numpy=np.__version__,
        scipy=scipy.__version__,
        tolerance=TOL,
        findings=[],
    )

    # 1. observable definition -------------------------------------------------
    say("\n== 1. observable: single eta = +q, carrier-phase average at fixed envelope time ==")
    S, T = 3.0, 1.0
    nz = required_nz(ALPHA, AAC, S=S, eta_max=Q)
    t_probe = np.array([0.7, 1.3])
    batched = tt_phase_avg(S, T, t_probe, 8, nz)
    single = np.array([tt_phase_avg(S, T, [t], 8, nz)[0] for t in t_probe])
    batch_diff = float(np.max(np.abs(batched - single)))
    # steady: phase average is time independent once filled, and eta=-q is the mirror channel
    t_full = np.array([1 + T, 1 + T + 0.3, 1 + T + 0.013])
    steady_tt = tt_phase_avg(S, T, t_full, 16, nz)
    steady_spread = float(np.ptp(steady_tt))
    tt_m = np.asarray([1 + T])[:, None, None]
    pp = (np.arange(16) * 2 * np.pi / 16)[None, :, None]
    I_minus = rocking(
        ALPHA,
        np.array([-Q]),
        n_z=nz,
        phi=lambda z: S * np.clip((tt_m - z) / T, 0, 1) * np.sin(Q * (z - tt_m) + pp),
    )[..., 0].mean()
    say(f"batched vs single-time evaluation max diff {batch_diff:.2e}")
    say(f"steady TT at t=1+T, +0.3, +0.013: {steady_tt}  spread {steady_spread:.2e}")
    say(f"eta=+q vs eta=-q steady phase-avg: {steady_tt[0]:.6f} vs {I_minus:.6f}")
    out["observable"] = dict(
        definition="|Dh(1)|^2 at the single point eta=+q (rocking called with eta=[q]); "
        "mean over equally spaced carrier phases with the envelope argument fixed at t; "
        "no eta integral, no time window",
        map_script_same="e67_overshoot_map.tt_average: eta=np.array([q]); envelope uses t only, "
        "phase enters sin() only; traces are not smoothed",
        batched_vs_single_max_diff=batch_diff,
        steady_phase_avg_time_spread=steady_spread,
        steady_eta_plus_q=float(steady_tt[0]),
        steady_eta_minus_q=float(I_minus),
        steady_law=float(np.sin(np.pi * ALPHA * jv(1, S)) ** 2),
    )

    # 2. Laue normalization in source ------------------------------------------
    say("\n== 2. Laue normalization ==")
    I0 = float(rocking(ALPHA, 0.0, n_z=2048))
    pend_err = abs(I0 - np.sin(np.pi * ALPHA) ** 2)
    S, T = 6.0, 0.05
    nz6 = required_nz(ALPHA, AAC, S=S, eta_max=Q)
    tt_m = np.array([0.03, 0.6, 1.05])[:, None, None]
    D0, Dh = solve_laue(
        ALPHA,
        np.array([Q]),
        n_z=nz6,
        phi=lambda z: S * np.clip((tt_m - z) / T, 0, 1) * np.sin(Q * (z - tt_m) + pp),
    )
    lossless_err = float(np.max(np.abs(np.abs(D0) ** 2 + np.abs(Dh) ** 2 - 1)))
    say(
        f"unmodulated eta=0: |Dh|^2={I0:.10f}, sin^2(pi alpha)={np.sin(np.pi * ALPHA) ** 2:.10f}, err {pend_err:.1e}"
    )
    say(
        f"lossless |D0|^2+|Dh|^2-1 at S=6,T=0.05, eta=q, 3 times x 16 phases: max {lossless_err:.1e}"
    )
    out["laue_normalization"] = dict(
        source="solve_laue: D0(0)=1, Dh(0)=0, both beams +z; intensity |Dh(1)|^2 is a fraction of "
        "the unit incident intensity; chi_0 gauged out, no absorption (real alpha)",
        pendelloesung_err=pend_err,
        lossless_max_err=lossless_err,
    )

    # 3. direct quadrature: causality, endpoint, map-law comparison -------------
    say("\n== 3. direct depth quadrature vs saved map law ==")
    quad_block = {}
    for label, S, T in CASES:
        th_neg = theta_direct(S, T, -0.1)
        th_end = theta_direct(S, T, 1 + T)
        th_after = theta_direct(S, T, 1 + T + 0.5)
        steady = float(np.sin(np.pi * ALPHA * jv(1, S)) ** 2)
        times = np.linspace(0, 1 + T, 2001)
        direct = np.array([I_direct(S, T, t) for t in times])
        law = map_law(S, T, times, samples=8193)
        law_diff = float(np.max(np.abs(direct - law)))
        t_pk, I_pk = peak_direct(S, T)
        grid_err = {
            nt: float(I_pk - np.max([I_direct(S, T, t) for t in np.linspace(0, 1 + T, nt)]))
            for nt in (101, 601, 1001, 2001)
        }
        excess = max(0.0, I_pk - steady)
        i, j = int(np.argmin(abs(npz["S"] - S))), int(np.argmin(abs(npz["rise"] - T)))
        grid_excess = float(npz["excess"][j, i])
        grid_T = float(npz["rise"][j])
        # saved excess at the exact grid T, recomputed directly
        ex_at_grid = excess if grid_T == T else max(0.0, peak_direct(S, grid_T)[1] - steady)
        q = dict(
            S=S,
            T=T,
            steady=steady,
            theta_before_arrival=float(th_neg),
            theta_end_minus_J1=float(th_end - jv(1, S)),
            theta_after_minus_J1=float(th_after - jv(1, S)),
            I_end_minus_steady=float(np.sin(np.pi * ALPHA * th_end) ** 2 - steady),
            direct_vs_map_law_max=law_diff,
            t_peak=t_pk,
            I_peak=I_pk,
            excess=excess,
            time_sampling_peak_err=grid_err,
            npz_nearest=dict(S=float(npz["S"][i]), T=grid_T, excess=grid_excess),
            direct_excess_at_npz_T=ex_at_grid,
            npz_excess_diff=float(ex_at_grid - grid_excess),
        )
        for c in saved["cases"]:
            if c["label"] == label:
                q["json_case"] = dict(peak=c["peak"], excess=c["excess"])
                q["json_peak_diff"] = float(I_pk - c["peak"])
        if label == "map_max":
            q["json_map_maximum"] = saved["map_maximum"]
        quad_block[label] = q
        say(
            f"{label}: S={S} T={T} theta(t<0)={th_neg:.1e} theta(1+T)-J1={th_end - jv(1, S):.1e} "
            f"|direct-maplaw|max={law_diff:.2e} peak={I_pk:.6f}@t={t_pk:.5f} excess={excess:.6f} "
            f"npz({npz['S'][i]:.2f},{grid_T:.4f})={grid_excess:.6f} diff={ex_at_grid - grid_excess:.1e} "
            f"grid peak err {grid_err}"
        )
    out["quadrature"] = dict(
        method="scipy.integrate.quad on the ramp segment [clip(t-T),clip(t)] plus "
        "exact J1(S)*clip(t-T) for the filled segment; map uses cumulative "
        "Simpson antiderivative of J1(Sx)",
        cases=quad_block,
    )

    # 4. full TT: depth, phase, time, approximation ----------------------------
    say("\n== 4. full TT convergence (separated) ==")
    tt_block = {}
    for label, S, T in CASES:
        t_pk = quad_block[label]["t_peak"]
        steady = quad_block[label]["steady"]
        times = np.unique(np.concatenate([np.linspace(0, 1 + T, 61), [t_pk, 1 + T]]))
        k_pk, k_end = int(np.argmin(abs(times - t_pk))), len(times) - 1
        nz = required_nz(ALPHA, AAC, S=S, eta_max=Q)
        t1 = time.perf_counter()
        base16 = tt_phase_avg(S, T, times, 16, nz)
        dbl16 = tt_phase_avg(S, T, times, 16, 2 * nz)
        base32 = tt_phase_avg(S, T, times, 32, nz)
        base8 = tt_phase_avg(S, T, times, 8, nz)
        dt = time.perf_counter() - t1
        direct = np.array([I_direct(S, T, t) for t in times])
        depth = np.abs(dbl16 - base16)
        phase = np.abs(base32 - base16)
        phase8 = np.abs(base16 - base8)
        best = dbl16  # finest depth; phase at 16 (32 agrees to the level reported)
        approx = np.abs(best - direct)
        tt_peak_grid = float(best.max())
        tt_excess = max(0.0, tt_peak_grid - float(best[k_end]))
        # local time refinement around the TT grid peak
        kk = int(np.argmax(best))
        # keep the grid argmax itself in the refinement set: with the inserted t_peak the
        # neighbouring intervals are unequal and a plain linspace drops it (correction round 1)
        loc = np.unique(
            np.concatenate(
                [np.linspace(times[max(kk - 1, 0)], times[min(kk + 1, k_end)], 11), [times[kk]]]
            )
        )
        loc_tt = tt_phase_avg(S, T, loc, 16, 2 * nz)
        tt_peak_loc = float(loc_tt.max())
        r = dict(
            S=S,
            T=T,
            nz_base=nz,
            nz_double=2 * nz,
            n_times=len(times),
            seconds=dt,
            depth_change=dict(
                max=float(depth.max()), at_peak=float(depth[k_pk]), at_steady=float(depth[k_end])
            ),
            phase_change_16_vs_32=dict(
                max=float(phase.max()), at_peak=float(phase[k_pk]), at_steady=float(phase[k_end])
            ),
            phase_change_8_vs_16=dict(
                max=float(phase8.max()), at_peak=float(phase8[k_pk]), at_steady=float(phase8[k_end])
            ),
            approx_error=dict(
                max_trace=float(approx.max()),
                t_of_max=float(times[int(np.argmax(approx))]),
                at_peak=float(approx[k_pk]),
                at_steady=float(approx[k_end]),
            ),
            tt_at_t0=float(best[0]),
            tt_steady=float(best[k_end]),
            tt_steady_minus_law=float(best[k_end] - steady),
            tt_peak_grid=tt_peak_grid,
            tt_peak_local_refined=tt_peak_loc,
            tt_time_sampling_peak_err=float(tt_peak_loc - tt_peak_grid),
            tt_excess=max(0.0, tt_peak_loc - float(best[k_end])),
            approx_excess=quad_block[label]["excess"],
            excess_error=float(
                max(0.0, tt_peak_loc - float(best[k_end])) - quad_block[label]["excess"]
            ),
            max_tt_intensity=float(max(best.max(), loc_tt.max())),
        )
        tt_block[label] = r
        say(
            f"{label}: nz={nz} {dt:.1f}s depth[max/peak/steady]={depth.max():.1e}/{depth[k_pk]:.1e}/{depth[k_end]:.1e} "
            f"phase16v32={phase.max():.1e} phase8v16={phase8.max():.1e} "
            f"approx[max/peak/steady]={approx.max():.1e}/{approx[k_pk]:.1e}/{approx[k_end]:.1e} "
            f"TT(0)={best[0]:.1e} TTsteady-law={best[k_end] - steady:.1e} "
            f"TTexcess={r['tt_excess']:.6f} approx={r['approx_excess']:.6f} err={r['excess_error']:.1e}"
        )
    out["tt"] = tt_block

    # 5. Pendelloesung bound and mechanism --------------------------------------
    say("\n== 5. Pendelloesung bound ==")
    x = np.linspace(0, 6, 60001)
    j1max = float(np.max(np.abs(jv(1, x))))
    bound = np.pi * ALPHA * j1max
    max_theta = max(
        abs(theta_direct(S, T, t)) for _, S, T in CASES for t in np.linspace(0, 1 + T, 401)
    )
    max_tt = max(r["max_tt_intensity"] for r in tt_block.values())
    say(
        f"max|J1| on [0,6] = {j1max:.5f}; pi*alpha*max|J1| = {bound:.4f} < pi/2 = {np.pi / 2:.4f}; "
        f"sin^2 bound {np.sin(bound) ** 2:.4f}; max|theta| over cases {max_theta:.4f}; max TT intensity {max_tt:.4f}; "
        f"npz excess growth at T boundary for S=3.8: {quad_block['map_max']['npz_nearest']['excess'] - float(npz['excess'][-2, int(np.argmin(abs(npz['S'] - 3.8)))]):.2e}"
    )
    out["pendelloesung"] = dict(
        max_abs_J1=j1max,
        pi_alpha_max_J1=bound,
        half_pi=float(np.pi / 2),
        reachable_intensity_bound=float(np.sin(bound) ** 2),
        max_abs_theta_cases=float(max_theta),
        max_tt_intensity_cases=max_tt,
        reason="|Theta_1| <= max|J1| = 0.5819 for any S, so pi*alpha*|Theta_1| <= 0.914 < pi/2 at alpha=0.5: "
        "sin^2 is monotone on the reachable range and no intensity-exchange maximum is crossed. "
        "Overshoot is the Entry 15 Bessel-ladder re-weighting of the depth integral (Entry 5 law), "
        "and the T=4 boundary value approaches the Entry 28 quasi-static limit sin^2(pi alpha max J1).",
        map_max_is_boundary=bool(
            npz["excess"][-1, int(np.argmin(abs(npz["S"] - 3.8)))]
            > npz["excess"][-2, int(np.argmin(abs(npz["S"] - 3.8)))]
        ),
    )

    # 6. findings from thresholds ----------------------------------------------
    for label, r in tt_block.items():
        for key in ("depth_change", "phase_change_16_vs_32", "approx_error"):
            v = r[key]["max" if key != "approx_error" else "max_trace"]
            if v > TOL:
                out["findings"].append(dict(severity="major", case=label, quantity=key, value=v))
        if r["tt_time_sampling_peak_err"] > TOL:
            out["findings"].append(
                dict(
                    severity="major",
                    case=label,
                    quantity="tt_time_sampling_peak_err",
                    value=r["tt_time_sampling_peak_err"],
                )
            )
        if abs(r["excess_error"]) > TOL:
            out["findings"].append(
                dict(severity="major", case=label, quantity="excess_error", value=r["excess_error"])
            )
        if r["approx_excess"] > 0 and r["approx_excess"] < 3 * r["approx_error"]["max_trace"]:
            out["findings"].append(
                dict(
                    severity="minor",
                    case=label,
                    quantity="excess_below_approximation_error",
                    value=r["approx_excess"],
                    approx_error=r["approx_error"]["max_trace"],
                    note="map excess is not resolved above the approximation error at this point",
                )
            )
    for label, q in quad_block.items():
        if abs(q["npz_excess_diff"]) > 1e-5 or q["direct_vs_map_law_max"] > 1e-5:
            out["findings"].append(
                dict(
                    severity="minor",
                    case=label,
                    quantity="map_law_reproduction",
                    npz_excess_diff=q["npz_excess_diff"],
                    law_diff=q["direct_vs_map_law_max"],
                )
            )
    out["elapsed_s"] = time.perf_counter() - T0
    (HERE / "e67_worker_audit.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    say(f"\nfindings: {json.dumps(out['findings'], indent=1)}")
    say(f"elapsed {out['elapsed_s']:.1f}s; wrote e67_worker_audit.json")


if __name__ == "__main__":
    main()
