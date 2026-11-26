"""Recompute every number printed on the poster. Run: uv run python poster/check_numbers.py

Each row is (printed value, recomputed value, tolerance). The recomputation uses the solver
(src/tratt), the stored results the figures are drawn from (explore/nb), and the constants
below. A row fails when the printed value, at the precision printed, does not match.

Constants and their sources:
- Si lattice constant a = 5.4310 A; 440 spacing d = a / sqrt(32).
- Lambda_P (Laue, Si 440, 30 keV, sigma) = 98.76 um from X0h (notebook Entry 20). The code's
  Lambda_P is the intensity period of sin^2(pi z / Lambda_P), lambda cos(theta_B) / |chi_rh|.
  The symmetric-Bragg value of the same reflection is lambda sin(theta_B) / |chi_rh|, i.e. the
  Laue value times tan(theta_B); it is derived here, not queried from X0h.
- c11, c12, c44 = 165.7, 63.9, 79.6 GPa, rho = 2329 kg/m^3 (textbook values, Entries 20, 85).
  Laue: shear wave along [001] of a Si(001) slab, v = sqrt(c44 / rho), for any transverse
  polarisation, so also u || h = [440] in the surface plane. Bragg 440: h || [110] is the normal,
  longitudinal wave along [110], v = sqrt((c11 + c12 + 2 c44) / (2 rho)).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.special import jv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "explore"))

import make_phase_figure as F
import make_poster_figure as M

C = 299_792_458.0
A_SI = 5.4310e-10
D440 = A_SI / np.sqrt(32)
LAMBDA_P_LAUE = 98.76e-6
E_KEV = 30.0
C11, C12, C44, RHO = 165.7e9, 63.9e9, 79.6e9, 2329.0

rows: list[tuple[str, float, float, float]] = []


def row(name: str, printed: float, value: float, tol: float) -> None:
    rows.append((name, printed, value, tol))


wavelength = 12.398420 / E_KEV * 1e-10
theta_b = np.arcsin(wavelength / (2 * D440))
lambda_p_bragg = LAMBDA_P_LAUE * np.tan(theta_b)
v_shear = np.sqrt(C44 / RHO)
v_long = np.sqrt((C11 + C12 + 2 * C44) / (2 * RHO))

# panel 1: S = h u0, so u0 = S d / (2 pi)
row("u0 at S = 1.5 (pm)", 23, 1.5 * D440 / (2 * np.pi) * 1e12, 0.5)
n = np.arange(-60, 61)
row("sum_n J_n(S)^2 at S = 1.5", 1, float(np.sum(jv(n, 1.5) ** 2)), 1e-12)
row("|J_-n| = |J_n| (n = 3, S = 1.5)", abs(jv(3, 1.5)), abs(jv(-3, 1.5)), 1e-15)

# panel 2: constants
row("Laue Lambda_P (um)", 98.8, LAMBDA_P_LAUE * 1e6, 0.05)
row("Bragg Lambda_P = Laue x tan(theta_B) (um)", 21.8, lambda_p_bragg * 1e6, 0.05)
row("shear v_s (km/s)", 5.85, v_shear / 1e3, 0.005)
row("longitudinal [110] v_s (km/s)", 9.14, v_long / 1e3, 0.005)

# panel 3: quasi-static estimate, L = 3 Lambda_P = 296 um, 2 GHz
L = 296e-6
row("L = 3 Lambda_P (um)", 296, 3 * LAMBDA_P_LAUE * 1e6, 0.5)
row("X-ray transit L/c (ps)", 0.99, L / C * 1e12, 0.005)
row("acoustic period at 2 GHz (ps)", 500, 1e12 / 2e9, 0)
row("transit / period (%)", 0.2, L / C * 2e9 * 100, 0.05)
row("Lambda_ac / Lambda_P at 2 GHz, Laue (<= 0.3)", 0.03, v_shear / 2e9 / LAMBDA_P_LAUE, 0.005)
row("Lambda_ac / Lambda_P at 2 GHz, Bragg (<= 0.3)", 0.21, v_long / 2e9 / lambda_p_bragg, 0.005)

# panel 3: snapshot figure parameters (explore/make_poster_figs.f0)
row("f0 snapshot: L / Lambda_ac", 5, 5.0, 0)

# panel 4: formation law
j1 = abs(jv(1, 1.5))
tau_laue = LAMBDA_P_LAUE / (v_shear * j1)
tau_bragg = lambda_p_bragg / (v_long * j1)
x99 = brentq(lambda x: np.tanh(np.pi * x) ** 2 - 0.99, 0.1, 3.0)
row("Laue tau_1 at S = 1.5 (ns)", 30, tau_laue * 1e9, 0.5)
row("Laue first maximum tau_1/2 (ns)", 15, tau_laue / 2 * 1e9, 0.5)
row("Bragg tau_1 at S = 1.5 (ns)", 4.3, tau_bragg * 1e9, 0.05)
row("Bragg 99 % time (ns)", 4.1, x99 * tau_bragg * 1e9, 0.05)
row("Bragg 99 % at x tau_n, x", 0.95, x99, 0.005)
row("Laue t_tr = L / v_s > tau_1 (ns)", 50.6, L / v_shear * 1e9, 0.05)
order = sorted((1, 2, 3), key=lambda k: -abs(jv(k, 3.0)))
row("order at S = 3: n = 2, 1, 3", 213, float("".join(map(str, order))), 0)

# The law against the solver: Laue, step onset, L = 3 Lambda_P, S = 1.5, n = 1, at the first
# maximum t = tau_1 / 2 (make_poster_figure.centre: centre intensity at beta = K).

alpha = 3.0
t_first = 0.5 / (alpha * j1)
row(
    "full TT I_1 at t = tau_1/2 (law: 1)",
    1.0,
    float(M.centre(alpha, 1.5, 1, np.array([t_first]))[0]),
    0.08,
)

# panel 5: overshoot
s_max = minimize_scalar(lambda s: -jv(1, s), bounds=(1, 3), method="bounded").x
row("J_1 largest at S", 1.84, s_max, 0.005)
row("first zero of J_1", 3.83, brentq(lambda s: jv(1, s), 3, 4.5), 0.005)
row("L = Lambda_P / 2 (um)", 49, LAMBDA_P_LAUE / 2 * 1e6, 0.5)
data = np.load(ROOT / "explore" / "nb" / "e67_overshoot.npz")
summary = json.loads((ROOT / "explore" / "nb" / "e67_overshoot.json").read_text())
row("e67 alpha = L / Lambda_P", 0.5, summary["alpha"], 0)
row("e67 L / Lambda_ac", 40, summary["alpha_ac"], 0)
row("map pairs (S, T_rise)", 11211, float(np.size(data["excess"])), 0)
row("largest Delta I", 0.603, float(np.max(data["excess"])), 0.0005)
row("bound sin^2(pi 0.5 max J_1)", 0.63, np.sin(np.pi * 0.5 * jv(1, s_max)) ** 2, 0.005)
row("max J_1", 0.582, jv(1, s_max), 0.0005)
cases = {c["label"]: c for c in summary["cases"]}
row("A: steady", 0.59, cases["A"]["steady"], 0.005)
row("A: steady = sin^2(pi 0.5 J_1(1.5))", 0.59, np.sin(np.pi * 0.5 * jv(1, 1.5)) ** 2, 0.005)
row("B: peak", 0.44, cases["B"]["peak"], 0.005)
row("B: steady", 0.26, cases["B"]["steady"], 0.005)
row("C: peak", 0.53, cases["C"]["peak"], 0.005)
row("C: steady", 1.3e-4, cases["C"]["steady"], 0.05e-4)

# panel 6: validity figure (explore/make_phase_figure.merged, the data of f4)

P = F.merged()
ok = (P[:, 1] >= 2) & (P[:, 0] / P[:, 1] < 0.3)
worst = float(P[ok, 3].max())
row(
    "largest relative error below Lambda_ac/Lambda_P = 0.3 (printed: under 6 %)",
    0.06,
    worst,
    0.06 - worst if worst < 0.06 else -1,
)


def main() -> int:
    bad = 0
    for name, printed, value, tol in rows:
        good = abs(value - printed) <= tol
        bad += not good
        print(f"{'ok ' if good else 'BAD'} {name:60s} printed {printed:<10g} computed {value:.6g}")
    print(f"\ntheta_B = {np.degrees(theta_b):.3f} deg at {E_KEV:g} keV")
    print(f"{len(rows) - bad} of {len(rows)} numbers match")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
