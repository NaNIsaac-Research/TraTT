"""Numerical convergence of the modulated problem, and the steady-state Bessel limit.

tests/test_analytic.py certifies fourth-order RK4 only for phi = 0. This file covers
the modulated cases the sweeps actually run:

1. Smooth phase profiles (front past the exit face, or a finite rise) keep the
   fourth order in both geometries.
2. A hard step onset with the front inside the slab does not. phi is continuous
   at the front (sin(q zeta - q t) vanishes at zeta = t) but its derivative jumps,
   so the one RK4 step that straddles the front has an O(h^2) local error and the
   global error is O(h^2) with a constant set by where the front sits inside that
   step. Put the front on a grid node and the fourth order comes back, which pins
   the mechanism. The solver is not changed here; runs with rise = 0 and t < 1
   are second order in n_z.
3. Formation times are quantized by the time grid and must converge as it is
   refined.
4. Steady state (step onset, t >= 1): channel n is a Laue slab of coupling
   alpha |J_n(S)| and full thickness, so its centre intensity tends to
   sin^2(pi alpha |J_n(S)|). The approach is second order in R = alpha / alpha_ac,
   the order of the Schrieffer-Wolff correction of notebook Entry 52.
"""

import numpy as np
import pytest
from scipy.special import jv

from tratt.core import required_nz, rocking, solve_bragg, solve_laue
from tratt.cube import front_and_full
from tratt.drive import Drive
from tratt.observe import channel_stats, formation_time

ETA = np.linspace(-40.0, 40.0, 41)
N_Z = (128, 256, 512, 1024)
N_REF = 8192


def _exit(geometry, phi, n_z):
    if geometry == "laue":
        return solve_laue(0.8, ETA, phi=phi, n_z=n_z)[1]
    return solve_bragg(2.0, ETA, phi=phi, n_z=n_z)


def _errors(geometry, phi):
    ref = _exit(geometry, phi, N_REF)
    return np.array([np.max(np.abs(_exit(geometry, phi, n) - ref)) for n in N_Z])


def _orders(errs):
    return np.log2(errs[:-1] / errs[1:])


@pytest.mark.parametrize("geometry", ["laue", "bragg"])
@pytest.mark.parametrize(
    "drive, t",
    [(Drive(S=1.3, alpha_ac=5.0), 1.437), (Drive(S=1.3, alpha_ac=5.0, rise=0.3), 0.437)],
    ids=["filled", "rise-inside"],
)
def test_smooth_modulated_profile_is_fourth_order(geometry, drive, t):
    orders = _orders(_errors(geometry, drive.phi(t)))
    assert np.all(orders > 3.8), orders


@pytest.mark.parametrize("geometry", ["laue", "bragg"])
def test_step_front_order_loss_comes_from_its_grid_offset(geometry):
    drive = Drive(S=1.3, alpha_ac=5.0)
    # t = 7/16 is a node of every grid in N_Z (Bragg steps from zeta = 1, same nodes)
    on_node = _errors(geometry, drive.phi(7 / 16))
    assert np.all(_orders(on_node) > 3.8), on_node

    off_node = _errors(geometry, drive.phi(0.437))
    h = 1.0 / np.array(N_Z)
    assert np.all(off_node < 60.0 * h**2), off_node / h**2  # global second order
    assert off_node[-1] > 10.0 * on_node[-1]  # and genuinely worse than the smooth case


@pytest.mark.parametrize("rise", [0.0, 0.3])
def test_laue_is_lossless_with_the_front_inside(rise):
    """Unitarity while the wavefront is still crossing; the existing check is at t = 1.4."""
    drive = Drive(S=1.3, alpha_ac=5.0, rise=rise)
    defects = []
    for n_z in (256, 1024):
        D0, Dh = solve_laue(0.8, ETA, phi=drive.phi(0.437), n_z=n_z)
        defects.append(np.max(np.abs(np.abs(D0) ** 2 + np.abs(Dh) ** 2 - 1.0)))
    assert defects[1] < defects[0], defects
    assert defects[1] < 1e-6, defects


def test_formation_time_converges_with_time_sampling():
    """Refining per_period must move t_f by less than the coarser sample spacing."""
    alpha, d = 1.3, Drive(S=0.5, alpha_ac=5.0)
    eta = np.linspace(-2.0 * d.q, 2.0 * d.q, 401)
    n_z = required_nz(alpha, d.alpha_ac)
    per_period = (8, 16, 32)
    t_f = {n: [] for n in (0, 1, -1)}
    for pp in per_period:
        times = d.times(t_max=1.4, per_period=pp)
        If, Is = front_and_full(alpha, d, eta, times, n_z=n_z)
        for n, values in t_f.items():
            F = formation_time(
                times, channel_stats(eta, If, d, n).p, channel_stats(eta, Is, d, n).p, d.period
            )
            assert F.status == "formed", (n, pp, F.status)
            values.append(F.t_f)
    for n, values in t_f.items():
        for k, pp in enumerate(per_period[:-1]):
            step = d.period / pp
            assert abs(values[k] - values[k + 1]) <= step + 1e-12, (n, values)


@pytest.mark.parametrize("n", [0, 1, 2])
def test_steady_state_channel_tends_to_bessel_coupled_slab(n):
    """Front past the exit face: centre of channel n -> sin^2(pi alpha |J_n(S)|),
    with the deviation O(R^2), R = alpha / alpha_ac, over a whole acoustic period."""
    S, alpha = 1.5, 0.5
    want = np.sin(np.pi * alpha * abs(jv(n, S))) ** 2
    devs = []
    for aac in (10.0, 20.0, 40.0):
        d = Drive(S=S, alpha_ac=aac)
        eta = np.array([d.eta_channel(n)])
        n_z = 2 * required_nz(alpha, aac, S=S, eta_max=abs(eta[0]))
        ts = 1.0 + np.arange(8) / 8 * d.period
        I = np.array([rocking(alpha, eta, phi=d.phi(t), n_z=n_z)[0] for t in ts])
        devs.append(np.max(np.abs(I - want)))
    orders = _orders(np.array(devs))
    assert np.all((orders > 1.8) & (orders < 2.2)), (devs, orders)
    assert devs[-1] < 1e-3, devs
