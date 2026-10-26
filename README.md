# TraTT — X-ray diffraction satellites while a sound wave enters a crystal

[![PyPI](https://img.shields.io/pypi/v/tratt)](https://pypi.org/project/tratt/) [![Tests](https://github.com/NaNIsaac-Research/TraTT/actions/workflows/ci.yml/badge.svg)](https://github.com/NaNIsaac-Research/TraTT/actions/workflows/ci.yml) [![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

TraTT is a time-dependent Takagi–Taupin solver: it simulates what an X-ray diffraction
measurement would see while a GHz sound wave is still entering a perfect crystal, before it has
filled the whole crystal. It is for people working on time-resolved X-ray diffraction from acoustic
waves, who want to know how the acoustic satellites of a Bragg peak build up in time. The
repository contains the solver (`pip install tratt`), the analysis scripts, a lab notebook of the
results, and the source of a conference poster.

![Full TT (points) and the formulas of result 1 (lines)](https://raw.githubusercontent.com/NaNIsaac-Research/TraTT/main/figures/poster/f1_collapse.png)

Main result, a calculation: satellite n forms in τ<sub>n</sub> = Λ<sub>P</sub>/(v<sub>s</sub>|J<sub>n</sub>(S)|), independent of the crystal thickness, and full TT (points) follows the closed formulas (lines) without a fitting parameter (notebook Entries 1, 9, 24). The physics background, the question and the dimensionless numbers are in [docs/background.md](docs/background.md).

## Install

```
pip install tratt
```

With [uv](https://docs.astral.sh/uv/), in a new environment:

<!-- test unix -->
```bash
uv venv
uv pip install tratt
.venv/bin/python -c "import tratt"
```

<!-- test windows -->
```powershell
uv venv
uv pip install tratt
.venv\Scripts\python -c "import tratt"
```

Requires Python 3.12+; the package is the solver (`src/tratt`, numpy and scipy only). Notebooks, figure scripts and the poster build need a
clone of this repository.

## Results

These are calculation results only; no experiment has been compared yet. Each item gives the
notebook entries with the numbers, scripts and limitations.

![Schematic: the acoustic front fills the crystal; on the right, the rocking curve of that instant](https://raw.githubusercontent.com/NaNIsaac-Research/TraTT/main/figures/poster/f0_scheme.png)

**1. Formation time of each satellite** (Entries 1, 9, 24). Satellite n at time t has the
intensity of a uniform, unstrained crystal of thickness v<sub>s</sub>t with coupling
α|J<sub>n</sub>(S)|: I<sub>n</sub> = sin²(πα|J<sub>n</sub>|t̃) in Laue and
tanh²(πα|J<sub>n</sub>|t̃) in Bragg geometry. These formulas agree with the full TT calculation
without a fitting parameter. The formation time of satellite n is therefore
τ<sub>n</sub> = Λ<sub>P</sub>/(v<sub>s</sub>|J<sub>n</sub>(S)|). It does not depend on the
crystal thickness, and the satellite with the largest |J<sub>n</sub>(S)| forms first. The figure at the top shows it.

**2. Gradual turn-on and overshoot** (Entries 28, 30, 67). If the amplitude A(t) changes in
time, different depths of the crystal have different amplitudes. Satellite n then depends on the
amplitude during the last transit time, Θ<sub>n</sub> = ∫J<sub>n</sub>(S A(t−ζ)) dζ, and not only
on the present amplitude. With a linear turn-on over T<sub>rise</sub> the satellite can overshoot:
its maximum during the turn-on exceeds the steady value. In a scan of 11,211 (S, T<sub>rise</sub>)
conditions for the first Laue satellite (α = 0.5, R = 0.0125) the largest overshoot is 0.603 of the
incident intensity, at the edge of the scan (T<sub>rise</sub> = 4t<sub>tr</sub>). The map comes from
the Θ<sub>n</sub> law; full TT at five points agrees with it to 8×10⁻⁵. Near a Bessel zero
(J<sub>1</sub> = 0 at the final amplitude) the satellite reaches 0.53 during the turn-on and
1.3×10⁻⁴ at the end.

![Overshoot map from the Θ<sub>n</sub> law and three traces checked against full TT](https://raw.githubusercontent.com/NaNIsaac-Research/TraTT/main/figures/poster/f7_overshoot.png)

**3. Validity of the independent-satellite approximation** (Entries 19, 26, 52–54). Results 1
and 2 treat each satellite independently, so their error grows with
R = Λ<sub>ac</sub>/Λ<sub>P</sub>. For the satellite centre intensity in time it is about 0.9R at
S = 1.5 and at most 0.03 for R ≤ 0.05 (30 random cases). The steady-state satellite populations
of the filled crystal reach a 5 % median error at R = 0.34–0.57. For larger R the satellites are
coupled through the forward beam. This is a limit of the approximate laws, not of the TT solver.

**Solver checks.** Against the closed-form Laue and Bragg solutions without sound the error is
below 10⁻⁹; the RK4 step converges at fourth order; against the independent Floquet solver for a
filled crystal the agreement is about 10⁻⁵ (Entry 42). The 54 tests in `tests/` cover these.

**4. Outlook: measurement of the phonon spectrum** (Entries 59, 64). For small strain, the Fourier
component of the reflectivity at frequency ω is the strain spectrum multiplied by a crystal
transfer function H(ω). We obtained H(ω) analytically to first order. Inside the Darwin width (the
angular range of strong reflection) it agrees with full TT, while the perturbation theory of
Sondhauss & Wark (2003) differs from full TT by a factor of 3–8. Comparison with previous work is
not complete (Entries 60, 61).

![First-order theory and full TT inside the Darwin width](https://raw.githubusercontent.com/NaNIsaac-Research/TraTT/main/figures/poster/f5_outlook.png)

Every study in the repository, with its notebook entries, status and reproduce commands: [docs/research/README.md](docs/research/README.md).

## Poster

**KPS 2026 Fall Meeting, poster P2.17** (Jeju, 22 October 2026). Isaac Yong, Ouyoung Kwon,
Hyunjung Kim — Center for Ultrafast Phase Transformation, Sogang University.

<p align="center">
  <img src="https://raw.githubusercontent.com/NaNIsaac-Research/TraTT/main/figures/poster/poster_preview.jpg" width="640" alt="KPS 2026 poster P2.17">
</p>

## Setup

```
uv sync --extra dev
uv run pytest -q                        # 54 tests: analytic limits, Floquet cross-check, formation law
uv run python explore/make_poster_figs.py   # poster figures -> figures/poster/
uv run python poster/build.py               # poster/poster.md -> poster/out/poster.pdf
```

The banner and the Sogang and CUPT logos are in `poster/assets/`.

## Layout

```
src/tratt/      solver package
  core.py         Laue IVP and Bragg Riccati (RK4, vectorised over eta and time; Bragg absorption kappa, kappa_h)
  drive.py        travelling acoustic drive phi(zeta; t): front, rise, amplitude profile
  floquet.py      exact Floquet solver for a uniformly filled crystal (independent cross-check)
  observe.py      channel windows, formation time, peak width
  cube.py         rocking curve over time (I(eta, t) cubes)
  sweep.py        parameter grids
tests/          analytic ground truth as asserts
notes/          lab_notebook.md: every result, with its script and its caveats (numbered entries)
explore/nb/     one script per notebook entry (eNN_*.py), with small cached results
explore/        figure scripts; make_poster_figs.py draws the poster figures
examples/       satellite_movie.py: an 18 s movie of the satellites forming (Entry 24 conditions)
poster/         poster.md (the only source of poster text), build.py (layout + checks), fonts
figures/        figures referenced by the notebook and the poster
DESIGN.md       physics conventions, analytic limits, assumptions
```

## Acknowledgement

This work was supported by the National Research Foundation of Korea, grant RS-2021-NR059920.

## Citation

See [CITATION.cff](CITATION.cff).

## License

MIT, see [LICENSE](LICENSE).
