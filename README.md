# TraTT — X-ray diffraction satellites while a sound wave enters a crystal

[![PyPI](https://img.shields.io/pypi/v/tratt)](https://pypi.org/project/tratt/) [![Tests](https://github.com/NaNIsaac/TraTT/actions/workflows/tests.yml/badge.svg)](https://github.com/NaNIsaac/TraTT/actions/workflows/tests.yml) [![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

This repository simulates what an X-ray diffraction measurement would see while a sound wave is
still entering a crystal, before it has filled the whole crystal. It contains the solver, the
analysis scripts, a lab notebook of everything tried so far, and the source of a conference poster.

**KPS 2026 Fall Meeting, poster P2.17** (Jeju, 22 October 2026). Isaac Yong, Ouyoung Kwon,
Hyunjung Kim — Center for Ultrafast Phase Transformation, Sogang University.

<p align="center">
  <img src="https://raw.githubusercontent.com/NaNIsaac/TraTT/main/figures/poster/poster_preview.jpg" width="640" alt="KPS 2026 poster P2.17">
</p>

## Introduction

### Background

**X-ray diffraction from a crystal.** An X-ray beam hitting a crystal is reflected strongly only
near one angle, the Bragg angle, where the reflections from successive atomic planes add up in
phase. Scanning the crystal angle through that point and recording the reflected intensity gives
the *rocking curve* I(η), where η is the (dimensionless) angular offset from the Bragg angle.

**Dynamical diffraction.** In a thin or imperfect crystal each X-ray is scattered at most once
(kinematic theory). In a thick, perfect crystal such as a silicon wafer the diffracted beam is
scattered back into the forward direction, and the two beams trade intensity back and forth as
they go deeper. The depth for one full exchange is the *Pendellösung length* Λ<sub>P</sub>,
typically 15–100 µm in silicon. The **Takagi–Taupin (TT) equations** describe this: two coupled
differential equations, along the depth, for the amplitude of the forward beam D<sub>0</sub> and
of the diffracted beam D<sub>h</sub>. They also allow the lattice to be locally displaced, which
is what a sound wave does.

**Two geometries.** In *Laue* (transmission) geometry the diffracted beam leaves through the back
surface, and the whole thickness contributes. In *Bragg* (reflection) geometry it leaves through
the front surface, and mainly the top ~Λ<sub>P</sub> contributes.

**Acoustic satellites.** A sound wave (here a GHz acoustic wave of wavelength Λ<sub>ac</sub>)
shifts the atomic planes periodically. For the X-rays this is a periodic phase modulation, so the
rocking curve gains extra peaks, *satellites*, on both sides of the main peak, spaced by the
acoustic wave vector. Satellite n carries the weight J<sub>n</sub>(S), a Bessel function of the
modulation strength S = h·u<sub>0</sub> (reciprocal lattice vector times displacement amplitude).
This steady state, with the whole crystal already vibrating, has been known for decades.

### The question

The sound wave is launched at one surface at t = 0 and travels at speed v<sub>s</sub>. At time t
only the depth v<sub>s</sub>t is vibrating; the rest of the crystal is still undisturbed. After
the transit time t<sub>tr</sub> = L/v<sub>s</sub> (L = crystal thickness) the wave fills the
crystal and the known steady state applies. **How do the satellites grow during
0 < t < t<sub>tr</sub>?** That is the question this repository works on.

### What the code computes

For each time t the solver freezes the displacement profile (sound present down to depth
v<sub>s</sub>t, nothing below), solves the TT equations through the crystal for every η, and
stores the rocking curve. Stacking these gives a map I(η, t). Every result below is an analysis of
such maps.

Freezing the lattice is safe here: the X-rays cross the crystal in about 1 ps, while one acoustic
period is about 500 ps, so the lattice moves by less than 1 % of a period during one crossing
(notebook Entry 62).

The problem reduces to a few dimensionless numbers:

| symbol | meaning |
|---|---|
| α = L/Λ<sub>P</sub> | crystal thickness in units of the Pendellösung length |
| S = h·u<sub>0</sub> | strength of the acoustic modulation |
| R = Λ<sub>ac</sub>/Λ<sub>P</sub> | acoustic wavelength in units of the Pendellösung length |
| t̃ = t/t<sub>tr</sub> | time in units of the transit time (t̃ = 1: the sound reaches the back surface) |

Main simplifications: two beams only, symmetric geometry, a plane monochromatic X-ray wave, no
absorption (an optional uniform absorption exists for Bragg geometry), and the sound acts only as
a displacement of the lattice. Details in [DESIGN.md](DESIGN.md).

A realistic case (notebook Entry 20): the Si 440 reflection at 17–30 keV, a crystal 150–300 µm
thick, a 1–2 GHz shear wave with strain ~2–3×10⁻⁵. The transit time is then 20–50 ns, long
compared with a synchrotron X-ray pulse (~100 ps), so the growth could in principle be resolved.

## What we have seen so far

These are simulation results only. Nothing has been compared with an experiment yet, and the
literature check is not finished. Each item points to the notebook entries with the numbers,
scripts and caveats.

![Schematic: the acoustic front fills the crystal; on the right, the rocking curve of that instant](https://raw.githubusercontent.com/NaNIsaac/TraTT/main/figures/poster/f0_scheme.png)

**1. Each satellite grows like an undisturbed crystal of depth v<sub>s</sub>t with a weaker
coupling** (Entries 1, 9, 24). In the simulations, satellite n at time t behaves as if it were
diffracted by a plain crystal of thickness v<sub>s</sub>t whose coupling is reduced by the factor
|J<sub>n</sub>(S)|. This gives simple formulas with no fitted parameter,
I<sub>n</sub> ∝ sin²(πα|J<sub>n</sub>|t̃) in Laue and tanh²(πα|J<sub>n</sub>|t̃) in Bragg, which
match the full TT calculation. So each satellite has its own growth time,
τ<sub>n</sub> = Λ<sub>P</sub>/(v<sub>s</sub>|J<sub>n</sub>(S)|), independent of the crystal
thickness, and changing S changes which satellite forms first.

![Full TT (points) against the closed formulas (lines)](https://raw.githubusercontent.com/NaNIsaac/TraTT/main/figures/poster/f1_collapse.png)

**2. If the sound amplitude changes in time, the satellites follow its recent history** (Entries
28, 30). When the amplitude ramps up instead of switching on at once, different depths hold sound
emitted at different times. A satellite then responds to the amplitude averaged over the last
transit time, Θ<sub>n</sub> = ∫J<sub>n</sub>(S A(t−ζ)) dζ, not to the current amplitude. One case
we found: a satellite with J<sub>n</sub> = 0 at the final amplitude (absent in the steady state)
can be the brightest satellite for a while during the growth.

**3. Item 1 holds only while the acoustic wavelength is short enough** (Entries 52–54). Treating
each satellite separately stays within about 5 % of the full calculation for
R = Λ<sub>ac</sub>/Λ<sub>P</sub> ≲ 0.3. For longer acoustic wavelengths the satellites exchange
intensity through the forward beam, and the simple formulas stop working.

**4. Side result: weak strain maps linearly onto the time signal** (Entries 59, 64). For weak
strain, the frequency components of the reflectivity R(t) are, to first order, the strain spectrum
multiplied by a crystal response function H(ω) that can be written in closed form. Inside the
Darwin width (the angular range of strong reflection) this agrees with full TT in our checks,
whereas the plane-wave perturbation of Sondhauss & Wark (2003) differs from full TT by a factor of
3–8 there. How much of this is already in the literature is still open (Entries 60, 61).

![First-order formulas against full TT inside the Darwin width](https://raw.githubusercontent.com/NaNIsaac/TraTT/main/figures/poster/f5_outlook.png)

## Install

```
pip install tratt
```

Requires Python 3.12+; the package is the solver (`src/tratt`, numpy and scipy only). Notebooks, figure scripts and the poster build need a
clone of this repository.

## Setup

```
uv sync --extra dev
uv run pytest -q                        # 54 tests: analytic limits, Floquet cross-check, formation law
uv run python explore/make_poster_figs.py   # poster figures -> figures/poster/
uv run python poster/build.py               # poster/poster.md -> poster/out/poster.pdf
```

## Layout

```
src/tratt/      solver package
  core.py         Laue IVP and Bragg Riccati (RK4, vectorised over eta and time; Bragg absorption kappa)
  drive.py        travelling acoustic drive phi(zeta; t): front, rise, amplitude profile
  floquet.py      exact Floquet solver for a uniformly filled crystal (independent cross-check)
  observe.py      channel windows, formation time, peak width
  cube.py         rocking curve over time (I(eta, t) cubes)
  sweep.py        parameter grids
tests/          analytic ground truth as asserts
notes/          lab_notebook.md: every result, with its script and its caveats (numbered entries)
explore/nb/     one script per notebook entry (eNN_*.py), with small cached results
explore/        figure scripts; make_poster_figs.py draws the poster figures
poster/         poster.md (the only source of poster text), build.py (layout + checks), fonts
figures/        figures referenced by the notebook and the poster
DESIGN.md       physics conventions, analytic limits, assumptions
```

Every item on the poster carries a tag pointing to a notebook entry. `poster/build.py` refuses to
pass if a tag points to an entry that does not exist.

## Notebooks

`explore/*.ipynb` are tracked with `nbstripout` as a git filter (`.gitattributes`). Outputs are
removed at commit time and stay in your working copy. If you move the repository or rebuild the
venv, re-register the filter:

```
uv run nbstripout --install --attributes .gitattributes
```

## Acknowledgement

This work was supported by the National Research Foundation of Korea, grant RS-2021-NR059920.

## Citation

See [CITATION.cff](CITATION.cff).

## License

MIT, see [LICENSE](LICENSE).
