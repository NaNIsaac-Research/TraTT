"""Entry 92: which depth sets the window law of the crystal factor.

Reads the saved Entry 75 TT results (no new TT run) and compares H(f; T)/H(f; 300 ns) with the
resonant-term form |1 - e^{-(kappa + i pi/x) T}| and with its envelope bound e^{-kappa T}.
Usage: uv run python explore/nb/e92_window_law.py
"""

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
V_L = 8433.0
LAMBDA_UM = {17.48: 11.54, 8.0: 11.33}


def main():
    d = json.loads((HERE / "e75_window_cf.json").read_text())
    f = np.array(d["f_GHz"], float)
    for key in ("E17.48_ncyc0.9", "E8_ncyc0.9"):
        c = d["cases"][key]
        kappa, lam = c["kappa"], LAMBDA_UM[c["E"]] * 1e-6
        t_unit = lam / V_L * 1e9
        x = f / (V_L / lam * 1e-9)
        z = kappa + 1j * np.pi / x
        h_ss = np.array(c["rows"][-1]["H_tt"], float)
        print(
            f"== {key}: 1/kappa = {t_unit / kappa:.2f} ns, ln(10)/kappa = {np.log(10) * t_unit / kappa:.1f} ns"
        )
        print("   f GHz            ", f.tolist())
        print("   x/pi (ns)        ", np.round(x / np.pi * t_unit, 1).tolist())
        print("   1/|kappa+ipi/x|  ", np.round(t_unit / np.abs(z), 1).tolist())
        worst_form, worst_bound = 0.0, -1.0
        for r in c["rows"]:
            t = r["T_ns"] / t_unit
            ratio = np.array(r["H_tt"], float) / h_ss
            form = np.abs(1 - np.exp(-z * t))
            if r["T_ns"] >= 5:
                worst_form = max(worst_form, float(np.max(np.abs(ratio / form - 1))))
            if r["T_ns"] < 300:
                worst_bound = max(
                    worst_bound, float(np.max(np.abs(ratio - 1) - np.exp(-kappa * t)))
                )
            print(
                f"   T = {r['T_ns']:7.2f} ns  H/H_300 {np.round(ratio, 3).tolist()}"
                f"  e^-kT {np.exp(-kappa * t):.3f}"
            )
        print(f"   max |H/H_300 / |1 - e^-zT| - 1| for T >= 5 ns: {worst_form:.4f}")
        print(
            f"   max (|H/H_300 - 1| - e^-kT) over T < 300 ns: {worst_bound:.4f} (<= 0: inside e^-kT)"
        )


if __name__ == "__main__":
    main()
