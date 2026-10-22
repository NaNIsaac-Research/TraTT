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
| H is a factor-2 bias for Si 400 at 17.5 keV over 20–100 GHz | confirmed **only for a window ≫ 20 ns (long train)**; wrong for the 140 ps Chalise packet, where H is flat to 4 % | Entries 65, 71 |
| closed form in the window length, H(f; T_w) | confirmed: the packet-kept first-order form (CF-B) matches TT to 0.3 % at every window 0.14–300 ns, two energies, three packet lengths; the packet-free short form (CF-A, Entry 71's hand estimate) is **rejected** below ~100 τ by the pre-registered 1 % rule | Entry 75 |
| signal maximum ≠ Fisher-information maximum (directive B2) | **negative** for a ps packet at one angle: amplitude maxima coincide (3 GHz apart), crystal moves nothing | Entry 70 |
| formation law I_n = sin²/tanh²(πα\|J_n\|t̃), no fit | confirmed | Entries 1, 9, 19, 24; tests |
| one dimensionless number joins the two regimes (directive B3) | **falsified in strong form** | Entry 68: spread 10–14× at fixed ν |
| ν ≲ 0.1 ⇒ linear to 2 % | confirmed as a bound on the scanned domain | Entry 68 §4 |
| Chalise et al. Fig. 2 tails = second-order strain terms | consistent in location; the low-frequency deficit is only partly explained (K = 0.65–0.88 vs their ~4×) once H is removed for their window | Entries 66, 71 |

**Falsification experiment run tonight** (`explore/nb/e68_nu_collapse.py`, Entry 68). Rule fixed
before the run: if 1 − K at equal ν spreads by more than ×2 across packet length, absorption and
satellite position, the "one criterion" form is false. Result: ×14 at ν = 0.1, ×10 at ν = 0.3.
So the claim is kept only in the form above (H is the correction, ν the guarantee); the sentence
"a single dimensionless parameter governs the crossover" must not appear in the paper.

**Second correction, same night (Entry 71).** H is the infinite-window limit. It needs the
measurement window, and so the strained depth, to exceed both the absorption depth 1/κ and the
extinction-phase depth x/π (tens of ns at Si 400): for the 140 ps packet of Chalise et al. the
crystal factor is flat to 4 % and the Entry 65 "factor 2" does not apply. H is therefore a property
of **long-train** measurements — the poster's own GHz bulk-wave geometry — which puts the transfer
function and the formation law into the same experiment.

Reproduce:

```
uv run python explore/nb/e64_sw_compare.py            # S&W vs Bloch-wave first order vs TT (9 s)
uv run python explore/nb/e65_si400.py                  # H for Si 400 at 8 and 17.48 keV
uv run python explore/nb/e68_nu_collapse.py run stats fit2 fig   # tonight's falsification (28 s)
uv run python explore/nb/e70_fisher.py run fig                   # B2, one case (24 s)
uv run python explore/nb/e71_window_H.py                         # window condition for H (11 s)
uv run python explore/nb/e75_window_cf.py run posthoc fig        # H(f; T_w) closed form vs TT, boundaries (110 s)
```

**Third step, Day 2 (Entry 75).** H(f; T_w) is now one closed form from the picosecond packet to the
steady train: at Si 400 / 17.48 keV the crystal factor is flat to 1 % up to 5 ns, departs by 10 % at
20 ns (T_flat), is halfway to the Entry 65 value at 33 ns and within 10 % of it at 52 ns (T_90); it
ripples around the steady value with period 2x Λ/v_L. The packet-free short form fails by 8 % at
140 ps (packet group delay and the −η image term) and was rejected under the rule; the packet-kept
form is what goes into the paper.

**Next falsification experiments, smallest first.** (T2a, the windowed closed form, is done: Entry 75.)
1. Anomalous absorption χ_ih in Bragg (not in `solve_bragg`). If it changes H by more than the
   claimed 1 % at κ/2πα ≈ 0.01, the closed form needs a second parameter. Tier: physics (src). (T2c)
2. Asymmetric geometry (γ_0 ≠ γ_h): the χ_0 gauge of DESIGN.md fails; H may acquire a geometry
   factor. Needs a solver change.
3. A smooth strain front instead of the step front of the Entry 58 packet: changes the high-frequency
   wing, and may change the saturation route of Entry 68.
4. Read Chukhovskii & Förster 1995 and Wark & Lee 1999 (time-dependent TT) for an earlier Bloch-wave
   first-order form. If one exists, the H part drops to "application"; the ν bound and the Si 400
   number stand. (T2d)
5. B1 degeneracy at larger S (Entry 72 iii). (T2b)

## 2. Candidates, scored

Scores: N = academic novelty, E = experimental importance, D = implementation difficulty (5 = easy),
G = chance of completion before graduation (2027 spring).

| # | candidate | N | E | D | G | one-line reason |
|---|---|---|---|---|---|---|
| P1 | Transfer function H(f; T_w) + window condition + linearity bound for reading phonon spectra from time-resolved Bragg reflectivity (Entries 59, 64–66, 68, 71, 75) | 3 | 3 | 4 | 5 | Closed form done and TT-verified; after Entry 71 it corrects long-train (GHz, tens of ns) measurements, not the 140 ps Chalise packet, so its experimental weight rests on the same apparatus as P2; novelty bounded by S&W 2003 and two unread 1990s papers |
| P2 | Temporal Pendellösung of satellites behind a travelling front: formation law, Bessel ladder, period-ratio calibration of S (Entries 1, 9, 13, 19, 24) | 3 | 3 | 5 | 4 | Clean, no-fit, both geometries, tests; prior art DeCamp 2001 (n = 0 pulse) + Polikarpov 1987/88 (static extinction length) makes it "extension to every order"; needs a bulk GHz shear-wave experiment that does not yet exist |
| P3 | Path memory: Θ_n law, transient-only satellite, overshoot map (Entries 28, 30, 34, 67) | 2 | 3 | 5 | 4 | Robust in the model, but at α = 0.5 it is kinematic diffraction from a graded grating and the slow-ramp limit is the Bessel ladder (Entry 34); best as a section of P2, not a paper |
| P4 | Overlap regime: Bessel-zero resurrection with a computable third-order coupling and shifted zero (Entries 45, 51, 52, 54) | 4 | 1 | 3 | 2 | Possibly new, but observability is 4e-5 of the window integral (Entry 54) and Entin / Iolin–Entin are unread; theory only |
| P5 | Second-order strain terms in the Chalise spectrum (Entry 66) | 2 | 3 | 5 | 5 | Known in kind (Bessel expansion); its value is the size at their strain and the fluence-series criterion; a section of P1 |

**What carries the paper now (after Entry 71).** Not the Chalise correction. It is the pair
"closed-form H valid inside the Darwin width + its window condition" together with the formation law,
and both need the same measurement: a GHz bulk acoustic train read over a window longer than
max(1/κ, x/π) Λ/v_s. For Si 400 at 17.48 keV that is ≥ 22 ns (train ≥ 185 µm long); for the
poster's Si 440 Laue geometry t_tr is already 28–51 ns (Entry 20), so the same transducer drive
serves both. Entry 75 gives the window numbers for Si 400 / 17.48 keV, 20 GHz against 100 GHz:
the crystal factor is flat (within 10 %) up to **T_flat = 19.6 ns**, halfway to the steady Entry 65
value at **T_half = 32.8 ns**, and within 10 % of it from **T_90 = 52.2 ns** on (TT-confirmed to
0.002). A measurement with a 20–50 ns window sits on the steep part, where H depends on the window
length itself; the experiment should therefore read either ≤ 5 ns (H flat to 1 %, kinematic
estimator) or ≥ 52 ns (steady H), and in between must know its window to 10 %. Without such a measurement the paper is theory with a proposal. T1c (Entry 73): on
the elastic and TT side S ≤ 2 at 1–2 GHz is feasible (strain ≤ 6.6e-5, second harmonic ≤ 10 %),
S = 3–6 is at the limit (harmonics 10–30 % at 2 GHz); the drive is 6–100 W/cm² peak acoustic
intensity for S = 1–2, pulsed, and no verified GHz bulk-transducer number is in hand. A real
transducer rings up over 0.2–4 t_tr, so the observable regime is the ramp map (Entry 67), not the
step collapse.

**Recommendation.** One paper, P1 + P2, around one experiment: a GHz bulk shear wave entering a
Si crystal, read over tens of ns. Its linear regime (ν ≲ 0.1) is the H-corrected spectrometer, its
dynamical regime is the formation law, and the window condition of Entry 71 is what makes both
appear in the same measurement. P5 is a subsection on picosecond packets (where only K matters).
P3 stays inside P2. P4 is a future project (Entry 51 F). Before tonight the recommendation was P1
alone on the strength of the Chalise correction; Entry 71 removed that strength.

Risks, in order:
- No long-window (tens of ns) time-resolved satellite measurement exists yet; the paper's
  experimental relevance is a proposal. Entry 73: elastic side fine for S ≤ 2 (limit at 3–6); the
  transducer peak power (6–100 W/cm² at 1–2 GHz for S = 1–2) is unverified.
- A referee calls the Bloch-wave correction of S&W routine. Answer: the paper rests on the window
  condition, the bound and the formation law, not on the linearisation.
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
3. **Fig. 3 — a real crystal, and the window condition.** H(f; T_w) against T_w for Si 400 at
   17.48 keV, closed form (lines) with TT (circles), and the ratio H(20)/H(100) against T_w with
   T_flat, T_half, T_90 marked (`figures/paper/e75_window_H.png`, Entry 75): the suppression exists
   only when the window exceeds 1/κ and x/π. One panel with K(f) for
   a picosecond packet (`figures/si400_harmonic.png`), where only the second-order term is left.
4. **Fig. 4 — the linearity bound and the dynamical satellite.** (a) 1 − K against ν for the 24
   series of Entry 68 with the tanh² and sin² laws (`figures/paper/e68_nu_collapse.png`, left panel);
   (b) the formation law of the poster, I_n(t̃) = sin²(πα|J_n|t̃) collapse (`figures/poster/f1_collapse.png`
   re-drawn in `figures/paper/`), as the ν ~ 1 limit.

## 3b. Directive questions, where each stands (T1b)

| question | entry | result |
|---|---|---|
| B1 two fields, same steady state, different transient | 72 | confirmed, and bounded: order n reads the t_tr running mean of J_n(S A); zero-mean perturbations are degenerate at that order (TT 9e-7); order-2 breaking 1e-3 at S = 1.5, not claimed |
| B2 signal maximum vs Fisher maximum | 70 | negative for a ps packet at one angle (3 GHz apart, crystal moves nothing); open for long trains |
| B3 one dimensionless criterion | 68, 71 | falsified in strong form; ν ≲ 0.1 bound and the window condition survive |
| B4 features when independent satellites fail | 45, 51, 52, 54 (no rerun) | Bessel-zero resurrection, confirmed in model, unobservable (4e-5), "possibly new" pending Entin / Iolin–Entin |

## 4. Open decisions for Isaac

- Paper = P1 (transfer function) with P2 inside, or P2 (formation) as the first paper? P1 is
  closer to finished and tied to a current measurement; P2 is the poster's identity.
- Whether to add χ_ih and asymmetric geometry to `solve_bragg` (Tier physics) before writing.
- Library access for Chukhovskii & Förster 1995 and Wark & Lee 1999.
- Whether to tell Chalise et al. that, in this model, their low-frequency deficit is not the crystal
  factor (Entry 71) and only partly the second-order term (Entry 66); and whether to correct
  `notes/qa_prep.md` §6b (the poster itself is frozen).
