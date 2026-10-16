"""Adaptive-step (solve_ivp RK45) two-beam TT propagation, kept from the old `calculate` sketch.

Source: https://github.com/NaNIsaac/calculate (src/ftt_solve.py, RK45TTIntegrator).
The package solvers use fixed-step RK4 in dimensionless units, with the Floquet
solver as the independent check; this is the only adaptive-error integrator and
the only one in physical units (wavelength, chi_0, chi_h). Its couplings set the
geometry factors to 1 and use eta as an added susceptibility, so it is not
checked against tratt.core.solve_laue. Run: python explore/calculate_rk45.py
"""

import numpy as np
from scipy.integrate import solve_ivp


def propagate_rk45(wavelength_m, chi_0, chi_h, chi_hbar, eta, z_grid_m, phi_z,
                   D0_in=1.0 + 0.0j, Dh_in=0.0 + 0.0j, rtol=1e-7, atol=1e-10):
    """Exit amplitudes (Dh, D0) after integrating through z_grid_m with phase phi_z sampled on it."""
    pref = 1j * np.pi / wavelength_m  # i k / 2

    def rhs(z, y):
        D0 = y[0] + 1j * y[1]
        Dh = y[2] + 1j * y[3]
        ph = np.interp(z, z_grid_m, phi_z)
        dD0 = pref * (chi_0 * D0 + chi_hbar * np.exp(+1j * ph) * Dh)
        dDh = pref * ((chi_0 + eta) * Dh + chi_h * np.exp(-1j * ph) * D0)
        return [dD0.real, dD0.imag, dDh.real, dDh.imag]

    y0 = [D0_in.real, D0_in.imag, Dh_in.real, Dh_in.imag]
    yL = solve_ivp(rhs, (z_grid_m[0], z_grid_m[-1]), y0, method="RK45", rtol=rtol, atol=atol).y[:, -1]
    return yL[2] + 1j * yL[3], yL[0] + 1j * yL[1]


if __name__ == "__main__":
    # unmodulated, eta = 0: Pendelloesung |Dh|^2 = sin^2(pi chi_h L / lambda), flux conserved
    lam, chi_h, L = 1e-10, 1.3e-6, 300e-6
    z = np.linspace(0.0, L, 150)
    Dh, D0 = propagate_rk45(lam, -1e-6, chi_h, chi_h, 0.0, z, np.zeros_like(z))
    print(f"|Dh|^2 = {abs(Dh)**2:.6f} (analytic {np.sin(np.pi * chi_h * L / lam)**2:.6f}), "
          f"|D0|^2 + |Dh|^2 = {abs(D0)**2 + abs(Dh)**2:.6f}")
