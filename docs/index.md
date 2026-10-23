# TraTT

TraTT is a time-dependent Takagi–Taupin solver. It computes what an X-ray rocking curve of a
perfect crystal looks like while a GHz sound wave is still entering the crystal, before the wave
has filled it: how the acoustic satellites of the Bragg peak build up between the moment the wave
is launched and its transit time $t_\mathrm{tr} = L/v_s$. For each time it freezes the lattice
displacement, solves the two-beam Takagi–Taupin equations through the crystal for every rocking
angle, and stacks the rocking curves into a map $I(\eta, t)$. Every result is an analysis of such
maps.

The results so far are calculations only; no experiment has been compared yet. They were
presented as poster P2.17 at the KPS 2026 Fall Meeting. The README's
[Results](../README.md#results) section lists them with the notebook entries that hold the numbers:
the formation time of each satellite, the overshoot under a gradual turn-on, where the
independent-satellite approximation holds, and a first-order transfer function between the strain
spectrum and the reflectivity.

Work toward a paper (the transfer function in more detail, its dependence on the measurement
window, and the conditions a real beam's divergence and bandwidth put on it) is on the branch
`research/paper-viability`, [TraTT#16](https://github.com/NaNIsaac/TraTT/pull/16). It is a draft
and its conclusions are being verified; they are not summarized on this site.

## Install

Python 3.12 or later.

```sh
uv venv
uv pip install tratt
```

`pip install tratt` works as well. The README's [Setup](../README.md#setup) section covers a
clone with the analysis scripts and tests.

## First run

Satellite $n$ of a Laue crystal, read at its centre $\eta_n = nq$, grows like a crystal of
thickness $v_s t$ with its coupling reduced by $|J_n(S)|$:
$I_n = \sin^2(\pi\alpha|J_n(S)|\,\tilde t)$ (README, result 1). This compares the full solver with
that law for the first satellite:

```python
import numpy as np
from scipy.special import jv

from tratt import Drive, rocking

alpha = 0.5  # crystal thickness L in Pendelloesung lengths
drive = Drive(S=1.5, alpha_ac=10.0)  # modulation strength, L in acoustic wavelengths
eta1 = drive.eta_channel(1)  # centre of the first satellite on the eta axis

print("  t/t_tr   satellite 1   sin^2(pi alpha |J1(S)| t)")
for t in (0.25, 0.5, 0.75, 1.0):
    intensity = rocking(alpha, eta1, phi=drive.phi(t), geometry="laue", n_z=2048)
    predicted = np.sin(np.pi * alpha * abs(jv(1, drive.S)) * t) ** 2
    print(f"  {t:6.2f}   {float(intensity):11.4f}   {predicted:11.4f}")
```

Output with tratt 0.1.0 from PyPI (Python 3.13):

```
  t/t_tr   satellite 1   sin^2(pi alpha |J1(S)| t)
    0.25        0.0489        0.0472
    0.50        0.1789        0.1800
    0.75        0.3744        0.3733
    1.00        0.5891        0.5905
```

`drive.phi(t)` is the frozen phase profile at time $t/t_\mathrm{tr}$: the sound wave of strength
$S$ fills the depth $\zeta < t$ and the rest of the crystal is still at rest. The two columns
differ by at most 0.002 here, where the acoustic wavelength is 0.05 Pendellösung lengths; the
README's result 3 says how the difference grows with that ratio.

## Where to go next

- [Equations](equations.md), on this site: the Laue and Bragg equations, the drive and the satellite channels as the solver implements them.
- [DESIGN.md](../DESIGN.md): the physics conventions, every assumption and what it discards, and the analytic limits used as tests.
- [Lineage](lineage.md), on this site: where TraTT came from, which script produced which notebook entry, and which claims stand or were withdrawn.
- The lab notebook, [`notes/lab_notebook.md`](../notes/lab_notebook.md), holds every entry the results cite.
- The Python API page lists the public functions and classes of the `tratt` package with their docstrings.
