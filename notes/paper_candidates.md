# Paper candidates — what in TraTT can carry a journal paper

Written 2026-10-22 (night), for Isaac's directive of the same day (`docs/isaac-directive-20261022.md`
in the NaNIsaac workspace), BACKLOG T1d. Every statement points to a notebook entry. Status words:
**confirmed** = full TT in this model, converged, no fit; **prior art** = in the literature we have
read in full; **hypothesis** = stated, not tested. Scores are 1–5 (5 = best), each with its reason.

## 1. Central claim (one), and tonight's attempt to break it

**Claim.** An acoustic satellite of a Bragg reflection is a dynamical reflection with its own
amplitude. Written to first order in the strain, that amplitude gives a closed-form transfer function
H(ω; κ/2πα) between the strain spectrum and the time-Fourier weight of the reflectivity, valid
inside the Darwin width where the Sondhauss–Wark (2003) plane-wave form fails (Entries 59, 64, 65).
When the amplitude is not small the satellite forms dynamically with extinction length
Λ_P/|J_n(S)|, which is the poster's formation law (Entries 1, 9). The first-order amplitude ν is a
sufficient linearity criterion: ν ≲ 0.1 keeps the weight linear to 2 % (Entry 68).

Where each part stands:

| part | status | evidence |
|---|---|---|
| first-order linearisation of TT for a phonon | prior art | Sondhauss & Wark 2003 eq. 25–29 (Entry 64) |
| kinematic heterodyne weighting W ∝ \|r0\| \|ε̂\|/ω | probably known in kind | Shayduk 2013 names the oscillation (Entry 60); not seen written as a transfer function |
| closed form H, Bloch-wave ansatz, valid inside the Darwin width | confirmed | TT to 1 % at κ/2πα = 0.12 incl. plateau; 0.5 % at 0.010 and 0.046 out to x = 100 (Entries 59, 64, 65) |
| S&W eq. 29 fails within ~1 Darwin width (factor 3–8) | confirmed, in our variables | Entry 64 §5 |
| H is a factor-2 bias for Si 400 at 17.5 keV over 20–100 GHz | confirmed (closed form + TT) | Entry 65 |
| formation law I_n = sin²/tanh²(πα\|J_n\|t̃), no fit | confirmed | Entries 1, 9, 19, 24; tests |
| one dimensionless number joins the two regimes (directive B3) | **falsified in strong form** | Entry 68: spread 10–14× at fixed ν |
| ν ≲ 0.1 ⇒ linear to 2 % | confirmed as a bound on the scanned domain | Entry 68 §4 |
| Chalise et al. Fig. 2 tails = second-order strain terms | consistent in location and size, not a match | Entry 66 |

**Falsification experiment run tonight** (`explore/nb/e68_nu_collapse.py`, Entry 68). Rule fixed
before the run: if 1 − K at equal ν spreads by more than ×2 across packet length, absorption and
satellite position, the "one criterion" form is false. Result: ×14 at ν = 0.1, ×10 at ν = 0.3.
So the claim is kept only in the form above (H is the correction, ν the guarantee); the sentence
"a single dimensionless parameter governs the crossover" must not appear in the paper.

Reproduce:

```
uv run python explore/nb/e64_sw_compare.py            # S&W vs Bloch-wave first order vs TT (9 s)
uv run python explore/nb/e65_si400.py                  # H for Si 400 at 8 and 17.48 keV
uv run python explore/nb/e68_nu_collapse.py run stats fit2 fig   # tonight's falsification (28 s)
```

**Next falsification experiments, smallest first.**
1. Anomalous absorption χ_ih in Bragg (not in `solve_bragg`). If it changes H by more than the
   claimed 1 % at κ/2πα ≈ 0.01, the closed form needs a second parameter. Tier: physics (src).
2. Asymmetric geometry (γ_0 ≠ γ_h): the χ_0 gauge of DESIGN.md fails; H may acquire a geometry
   factor. Needs a solver change.
3. A smooth strain front instead of the step front of the Entry 58 packet: changes the high-frequency
   wing, and may change the saturation route of Entry 68.
4. Read Chukhovskii & Förster 1995 and Wark & Lee 1999 (time-dependent TT) for an earlier Bloch-wave
   first-order form. If one exists, the H part drops to "application"; the ν bound and the Si 400
   number stand.

## 2. Candidates, scored

Scores: N = academic novelty, E = experimental importance, D = implementation difficulty (5 = easy),
G = chance of completion before graduation (2027 spring).

| # | candidate | N | E | D | G | one-line reason |
|---|---|---|---|---|---|---|
| P1 | Transfer function + linearity bound for reading phonon spectra from time-resolved Bragg reflectivity (Entries 59, 64–66, 68) | 3 | 4 | 4 | 5 | Correction the 2026 Chalise measurement needs and the 2023 Bargheer review does not use; closed form done, TT-verified; novelty bounded by S&W 2003 and by two unread 1990s papers |
| P2 | Temporal Pendellösung of satellites behind a travelling front: formation law, Bessel ladder, period-ratio calibration of S (Entries 1, 9, 13, 19, 24) | 3 | 3 | 5 | 4 | Clean, no-fit, both geometries, tests; prior art DeCamp 2001 (n = 0 pulse) + Polikarpov 1987/88 (static extinction length) makes it "extension to every order"; needs a bulk GHz shear-wave experiment that does not yet exist |
| P3 | Path memory: Θ_n law, transient-only satellite, overshoot map (Entries 28, 30, 34, 67) | 2 | 3 | 5 | 4 | Robust in the model, but at α = 0.5 it is kinematic diffraction from a graded grating and the slow-ramp limit is the Bessel ladder (Entry 34); best as a section of P2, not a paper |
| P4 | Overlap regime: Bessel-zero resurrection with a computable third-order coupling and shifted zero (Entries 45, 51, 52, 54) | 4 | 1 | 3 | 2 | Possibly new, but observability is 4e-5 of the window integral (Entry 54) and Entin / Iolin–Entin are unread; theory only |
| P5 | Second-order strain terms in the Chalise spectrum (Entry 66) | 2 | 3 | 5 | 5 | Known in kind (Bessel expansion); its value is the size at their strain and the fluence-series criterion; a section of P1 |

**Recommendation.** P1 as the paper, with P2 as its "beyond linearity" section (the satellite's own
extinction length is what sets ν, Entry 65 §4) and P5 as a subsection. P2 alone is a second, shorter
paper only if an experiment is planned. P3 stays in P2. P4 is a future project (Entry 51 F).

Risks, in order:
- A referee calls the Bloch-wave correction of S&W routine. Answer: the paper rests on the measurement
  correction (factor 2 at Si 400 / 17.5 keV) and the bound, not on the linearisation.
- An earlier first-order Bloch-wave form exists (Chukhovskii & Förster, Wark & Lee). Not read.
- Chalise's energy and normalisation are unknown; the comparison stays "same sign, same order".
- Model limits: symmetric, σ, normal absorption only, plane wave, no instrument resolution.

## 3. Figure plan (figures go to `figures/paper/`; poster figures are frozen)

1. **Fig. 1 — the estimator and the crystal factor.** (a) R(t) at one detuning for a packet, with its
   Fourier component at ω = |η| marked; (b) W/W_kin against ω/ω_D: the one-curve collapse for three
   packet spectra at κ/2πα = 0.12 (`e59_transfer.py fig`, `figures/chalise_transfer.png` b).
2. **Fig. 2 — where the plane-wave first order fails.** |F_pred|/|F_TT| at the satellite against
   ω/ω_D for S&W eq. 29, S&W normalised, and the Bloch-wave (Riccati) form; the near-main-peak
   error alongside (`e64_sw.json`). Message: the Bloch-wave depth dependence is what keeps first
   order valid inside the Darwin width.
3. **Fig. 3 — a real crystal.** H(f) for Si 400 at 8 and 17.48 keV over 1–400 GHz with the Chalise
   band shaded (`figures/si400_transfer.png`), and the strain non-linearity K(f) for their packet
   (`figures/si400_harmonic.png`, one panel).
4. **Fig. 4 — the linearity bound and the dynamical satellite.** (a) 1 − K against ν for the 24
   series of Entry 68 with the tanh² and sin² laws (`figures/paper/e68_nu_collapse.png`, left panel);
   (b) the formation law of the poster, I_n(t̃) = sin²(πα|J_n|t̃) collapse (`figures/poster/f1_collapse.png`
   re-drawn in `figures/paper/`), as the ν ~ 1 limit.

## 4. Open decisions for Isaac

- Paper = P1 (transfer function) with P2 inside, or P2 (formation) as the first paper? P1 is
  closer to finished and tied to a current measurement; P2 is the poster's identity.
- Whether to add χ_ih and asymmetric geometry to `solve_bragg` (Tier physics) before writing.
- Library access for Chukhovskii & Förster 1995 and Wark & Lee 1999.
