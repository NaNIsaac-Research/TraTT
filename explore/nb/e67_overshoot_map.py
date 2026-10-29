"""Entry 67: linear-ramp overshoot map and phase-averaged TT spot checks."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import cumulative_simpson
from scipy.special import jv

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from tratt.core import required_nz, rocking  # noqa: E402

ALPHA, AAC = 0.5, 40.0
CASES = [("A", 1.5, 1.0), ("B", 3.0, 1.0), ("C", 3.85, 2.0)]
OUT = ROOT / "explore" / "nb"


def intensity(S, rise, times, samples=4097):
    """Sliding one-transit integral, using an antiderivative of the ramp."""
    x = np.linspace(0, 1, samples)
    integral = cumulative_simpson(jv(1, S * x), x=x, initial=0)

    def primitive(s):
        return rise * np.interp(np.clip(s / rise, 0, 1), x, integral) + np.maximum(
            s - rise, 0
        ) * jv(1, S)

    theta = primitive(times) - primitive(times - 1)
    return np.sin(np.pi * ALPHA * theta) ** 2


def scan(amplitudes, rises, nt=1001, samples=4097):
    steady = np.sin(np.pi * ALPHA * jv(1, amplitudes)) ** 2
    excess = np.empty((len(rises), len(amplitudes)))
    for j, rise in enumerate(rises):
        times = np.linspace(0, 1 + rise, nt)
        for i, S in enumerate(amplitudes):
            excess[j, i] = max(0, float(intensity(S, rise, times, samples).max() - steady[i]))
    return excess


def tt_average(S, rise, times, phases=8, refinement=1):
    """Average carrier phase at fixed envelope time; do not smooth time traces."""
    q = 2 * np.pi * AAC
    t = np.repeat(times, phases)[:, None]
    phase = np.tile(np.arange(phases) * 2 * np.pi / phases, len(times))[:, None]

    def phi(z):
        return S * np.clip((t - z) / rise, 0, 1) * np.sin(q * z - q * t + phase)

    nz = refinement * required_nz(ALPHA, AAC, S=S, eta_max=q)
    values = rocking(ALPHA, np.array([q]), phi=phi, n_z=nz)
    return values.reshape(len(times), phases).mean(axis=1)


def main():
    amplitudes = np.linspace(0.5, 6, 111)
    rises = np.linspace(0.05, 4, 101)
    excess = scan(amplitudes, rises)
    refined = scan(amplitudes, rises, nt=2001, samples=8193)
    map_change = float(np.max(np.abs(excess - refined)))
    results = dict(
        alpha=ALPHA,
        alpha_ac=AAC,
        order=1,
        envelope="linear ramp, then held",
        grid=[len(rises), len(amplitudes)],
        map_refinement_max_change=map_change,
        observable="carrier-phase-averaged intensity at eta=q, incident intensity=1",
        map_method="independent-satellite accumulated-coupling approximation",
        geometry="laue",
        trace_window="0 <= t/t_tr <= rise + 1",
        tt_checks=dict(phases=8, depth_grid="required_nz", times=101),
        tt_cases=dict(
            phases=16,
            depth_grid="2 x required_nz",
            times=61,
            refinement_reference=dict(phases=8, depth_grid="required_nz"),
        ),
        cases=[],
        checks=[],
    )
    arrays = dict(S=amplitudes, rise=rises, excess=refined)
    checks = [(S, rise) for S in (1.5, 3.0, 3.85, 5.0) for rise in (0.2, 1.0, 3.0)]
    for S, rise in checks:
        times = np.linspace(0, 1 + rise, 101)
        approx = intensity(S, rise, times, samples=8193)
        tt = tt_average(S, rise, times)
        steady = float(np.sin(np.pi * ALPHA * jv(1, S)) ** 2)
        result = dict(
            S=S,
            rise=rise,
            max_trace_error=float(np.max(np.abs(tt - approx))),
            excess_error=float(abs((tt.max() - tt[-1]) - (approx.max() - steady))),
        )
        results["checks"].append(result)
        print(result, flush=True)
    for label, S, rise in CASES:
        times = np.linspace(0, 1 + rise, 601)
        coarse_times = np.linspace(0, 1 + rise, 61)
        trace = intensity(S, rise, times, samples=8193)
        tt = tt_average(S, rise, coarse_times)
        fine_tt = tt_average(S, rise, coarse_times, phases=16, refinement=2)
        steady = float(np.sin(np.pi * ALPHA * jv(1, S)) ** 2)
        results["cases"].append(
            dict(
                label=label,
                S=S,
                rise=rise,
                peak=float(trace.max()),
                steady=steady,
                excess=float(trace.max() - steady),
                tt_refinement_max_change=float(np.max(np.abs(tt - fine_tt))),
                max_trace_error=float(np.max(np.abs(fine_tt - intensity(S, rise, coarse_times)))),
            )
        )
        arrays.update(
            {
                f"{label}_t": times,
                f"{label}_I": trace,
                f"{label}_tt_t": coarse_times,
                f"{label}_tt_I": fine_tt,
            }
        )
    j, i = np.unravel_index(np.argmax(refined), refined.shape)
    results["map_maximum"] = dict(
        S=float(amplitudes[i]), rise=float(rises[j]), excess=float(refined[j, i])
    )
    np.savez_compressed(OUT / "e67_overshoot.npz", **arrays)
    (OUT / "e67_overshoot.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2), flush=True)


if __name__ == "__main__":
    main()
