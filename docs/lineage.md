# Lineage of TraTT

Where TraTT came from, which script produced which notebook entry, which claims stand, which were withdrawn, and how to rerun the main computations. Written 2026-10-23 for the repository audit (NaNIsaac BACKLOG A2) from git history, `notes/lab_notebook.md`, `notes/paper_draft.md` and Isaac's project files. It adds no new result and does not reinterpret any; where a status is quoted it is quoted from the notebook or the draft.

The research notes (`notes/`) belong to the TraTT research lane and are not changed here. Entries 68-88 and `notes/paper_draft.md` are on the branch `research/paper-viability` (PR #16, draft), not yet on `main`; links below say so.

## 1. Earlier work and names

| Name | What it was | Where the record is | Relation to TraTT |
|---|---|---|---|
| FTT (Floquet-Takagi-Taupin) | Isaac's first line on X-ray diffraction from a crystal modulated by a bulk acoustic wave: Floquet channels of the two-beam Takagi-Taupin (TT) equations. Manuscript drafts "Floquet-Takagi-Taupin" v1 and v2, slides "Floquet-Takagi-Taupin" and "DynamicFTT" | Isaac's Drive project folder `01_Projects/X-AOM/` (`05_Paper/`, `04_Slides/`); not in any repository | same physics question. TraTT's first design document was titled "DynamicFTT" (`DynamicFTT_Research_Handoff.md`, added in 1216ff8, 2026-09-30, removed from the tree in 7438afe, 2026-10-15; still in history) |
| `calculate` | first code of the FTT line (2026-01-15, 0bff8d2): `FTTSolver` with Euler and RK45 TT integrators for a travelling-wave phase, and a notebook of Bessel sideband weights and satellite angles | [NaNIsaac/calculate](https://github.com/NaNIsaac/calculate) (private); its working copy is in the same Drive folder, `02_Src/calculate` | one function copied: `explore/calculate_rk45.py` (b91b15b, 2026-10-16) keeps the adaptive RK45 integrator. TraTT's solvers in `src/tratt/` were written separately and are not derived from it |
| FTT package (`src/ftt/`) | a later FTT code base described in Isaac's notes of 2026-08-04: `tt.py` (stroboscopic RK4 TT solver, Laue), `model.py` (travelling drive, parameters S, q, w), `floquet.py` (channel projection), `metrics.py`, `experiment.py`, `tdtt.py` (time-derivative channel-coupled engine), `transient/` (Landau-Zener overshoot, realization map) | not found on this PC or in any NaNIsaac repository | TraTT has modules with the same roles (`core.py`, `drive.py`, `floquet.py`, `observe.py`); whether code moved cannot be checked without the source |
| AW_TT_EXP | an experiment-feasibility calculator (`spec_calc.py`): from X-ray energy, acoustic frequency, sound speed, Bragg angle, rocking width, crystal thickness, pixel size and distance, decides whether the ±1 acoustic satellites are separable in angle or on the detector | described in the same notes; source not found | no counterpart in TraTT; the realisability tables of Entries 20, 73 and 85 answer a related question with verified constants |
| TrTT | the name used for TraTT's KPS 2026 Fall poster preparation (`TrTT_presentation_handbook`, `TrTT_last_minute`, in `01_Projects/Conferences/2026_KPS_Fall/`) | Drive | the same project; the handbook names the repository NaNIsaac/TraTT and the package `tratt` |

Order in time, from git and file dates (Drive file dates are copy dates and only bound the authoring date from above): FTT manuscript drafts and slides by early 2026; `calculate` 2026-01-15; FTT package by 2026-08-04; TraTT initial commit e761142 on 2026-08-28 (DESIGN.md, `core.py`, `drive.py`, tests); transient-formation pipeline and notebook Entries 0-9 on 2026-09-30; poster at KPS 2026 Fall on 2026-10-22; paper-viability work (Entries 68-88) on 2026-10-22/23.

`calculate`'s README said "Merged into TraTT"; that is being corrected in NaNIsaac/calculate#1. Only the one integrator above was copied.

## 2. Scripts and notebook entries

Scripts are in `explore/nb/` unless a path is given; `explore/make_*.py` draw the poster and notebook figures. Run from the repository root with `uv run python <script> [args]`; the arguments are the ones written in the entry or in the script's docstring. "(PR #16)" marks scripts that are only on `research/paper-viability`.

| Entry | Topic | Script(s) |
|---|---|---|
| 0 | starting point | — |
| 1 | formation order, n = 0 two-layer law | `e1_order.py` |
| 2 | +12 % excess is the static tail | `e2_tail.py` |
| 3 | peak shift is kinematic (negative) | `e3_shift.py`, `e3b_shift_scan.py` |
| 4 | satellite width narrowing | `e4_width.py` |
| 5 | finite rise time, accumulated coupling | `e5_rise.py` |
| 6 | units, temporal Pendellösung period | `e6_units.py` |
| 7 | prior art | — |
| 8 | transient ±n asymmetry | `e8_asym.py` |
| 9 | Bragg geometry, t_f ~ 1/α_n | `e9_bragg.py` |
| 10 | poster summary figure | `explore/make_poster_figure.py` |
| 11 | absorption (estimate only) | `e11_absorb.py` |
| 12 | claims and evidence (first table) | — |
| 13 | in-situ S calibration | `e13_calib.py` |
| 14 | three-mode, two-layer model | `e14_threemode.py` |
| 15 | ramp through the Bessel ladder | `e15_cancel.py` |
| 16 | validity of the filled-depth law | `e16_validity.py` |
| 17 | Bragg satellite width | `e17_bragg_width.py` |
| 18 | overshoot table without a fit | `explore/make_feature_figure.py` |
| 19 | random conditions | `e19_random.py` |
| 20 | experiment mapping, X0h constants | `e20_units_x0h.py` |
| 21 | prior art, second pass | — |
| 22 | time-resolved rocking curve picture | `explore/make_map_figure.py` |
| 23 | dark point, inward fringes | `e23_dark.py` |
| 24 | one front, three satellites | `explore/make_ladder_map.py` |
| 25 | Bessel zero, slow clock stops | `e25_zero.py` |
| 26 | regime map | `explore/make_regime_map.py` |
| 27 | claims table, additions 20-26 | — |
| 28 | transient-only satellite | `e28_transient_only.py`, `memory_drive.py` |
| 29 | Polikarpov & Skadorov read | — |
| 30 | formation remembers the path | `e30_history.py`, `explore/make_memory_figure.py` |
| 31 | brightest order switches; grid-rule bug | `e31_switch.py` |
| 32 | two co-propagating waves | `e32_two_waves.py` |
| 33 | claims table, additions 28-32 | — |
| 34 | is the transient-only satellite real | — |
| 35 | its robustness and failure boundary | `e35_robust.py`, `nonideal.py`, `explore/make_robust_figure.py` |
| 36 | up vs down (mostly negative) | `e36_updown.py`, `explore/make_updown_figure.py` |
| 37 | two acoustic domains | `e37_domains.py`, `explore/make_domain_figure.py` |
| 38 | chirped waves, Landau-Zener plateau | `e38_chirp.py`, `qmod.py` |
| 39 | acoustic domain walls | `e39_walls.py` |
| 40 | automated anomaly search | `e40_search.py`, `explore/make_search_figure.py` |
| 41 | validation and conservative summary of 38-40 | `e41_validate.py` |
| 42 | exact Floquet solver (`src/tratt/floquet.py`) | `e46_bands.py` |
| 43 | regime map, micromotion | `e43_phase.py`, `explore/make_phase_figure.py` |
| 44 | hierarchy of Floquet paths | `e44_mechanism.py`, `e44b_sidebands.py` |
| 45 | Bessel-zero resurrection | `e45_zero.py`, `e45b_shifted_zero.py`, `explore/make_zero_figure.py` |
| 46 | Floquet bands, gap folding | `e46_bands.py`, `e48_trajectories.py`, `explore/make_floquet_figures.py` |
| 47 | dark windows with strong coupling | `e47_dark.py`, `e47b_darkmap.py`, `explore/make_darkmap_figure.py` |
| 48 | time-resolved formation across regimes | `e49_time.py` |
| 49 | anomaly ranking | `e50_anomaly.py` |
| 50 | prior art, overlap regime | — |
| 51 | summary of the overlap-regime project | `e43_phase.py`, `e50_anomaly.py` |
| 52 | effective 2×2 Hamiltonian | `e52_heff.py` |
| 53 | phase-average convergence | `e53_phaseavg.py check`, `e53b_map_check.py`, `e53c_boundary.py`, `e53d_affected.py`, `explore/make_phaseavg_figure.py` |
| 54 | exact phase-averaged map | `e54_exactmap.py`, `e54b_width.py base eps map res`, `e54c_summary.py` |
| 55, 56 | acoustic walls vs stacking-fault theory | `e55_fault_check.py`, `e39_walls.py` |
| 57 | Chalise et al., what "spectral weight" means | — |
| 58 | first Chalise reference case (invalid) | `e58_chalise_ref.py` |
| 59 | absorbing reference, closed-form transfer function | `e58_chalise_ref.py`, `e59_transfer.py` |
| 60, 61, 62 | literature status, quasi-static number | — |
| 63 | surface acoustic waves | `e63_saw.py` |
| 64 | Sondhauss & Wark (2003) vs Entry 59 | `e64_sw_compare.py` |
| 65 | transfer function for Si 400 | `e65_si400.py [tt] [fig]`, `e65_conv.py`, `e65_packet.py` |
| 66 | Chalise Fig. 2 tails in full TT | `e66_harmonic.py` |
| 67 | overshoot map | `e67_overshoot_map.py`, `e67_worker_audit.py`, `explore/make_poster_figs.py` |
| 68 | one-number linearity limit (falsification run) | `e68_nu_collapse.py run stats fit2 fig` (PR #16) |
| 69 | S&W vs Entry 59 term by term | `e64_sw_compare.py` (PR #16) |
| 70 | signal max vs Fisher-information max | `e70_fisher.py run fig` (PR #16) |
| 71 | H needs a long window | `e71_window_H.py` (PR #16) |
| 72 | histories that cannot be told apart | `e72_history_degeneracy.py` (PR #16) |
| 73 | what S = 0.5-6 means physically | `e73_realisability.py` (PR #16) |
| 74 | directive questions B3, B4 (no computation) | — |
| 75 | H as a closed form in window length | `e75_window_cf.py run posthoc fig` (PR #16) |
| 76 | degeneracy class at larger S | `e76_degeneracy_S.py runA runB fig` (PR #16) |
| 77 | anomalous absorption χ_ih | `e77_chi_ih.py run ttp ttm conv60 fig` (PR #16) |
| 78 | ±η side asymmetry | `e78_side_asymmetry.py run fig` (PR #16) |
| 79 | coupling ratio R and the degeneracy class | `e79_degeneracy_R.py run fig` (PR #16) |
| 80 | corrections to Entry 73 | — |
| 81 | asymmetric Bragg as a rescaling | `e81_asym_map.py run` (PR #16) |
| 82 | beam divergence and H | `e82_divergence.py run fig` (PR #16) |
| 83 | beam condition at GHz-train frequencies | `e83_lowx.py run fig` (PR #16) |
| 84 | beam divergence and the centre formation law | `e84_satellite_divergence.py run fig` (PR #16) |
| 85 | Si 440 / 17.48 keV, 1-2 GHz case | `e85_si440_case.py` (PR #16) |
| 86 | integrated population and the beam condition | `e86_population_divergence.py run fig` (PR #16) |
| 87 | Laue integrated population at 3 w_n | `e87_population_laue.py run fig` (PR #16) |
| 88 | polarisation and Debye-Waller as rescalings | `e88_polarisation_dw.py` (PR #16) |

Script names follow the entry numbers except in 42 (`e46_bands.py`), 48 (`e49_time.py`) and 49 (`e50_anomaly.py`). Not cited by any entry: `explore/calculate_rk45.py` (see §1), `explore/make_collapse_figure.py`, `explore/make_dephasing_figure.py`, `explore/make_poster_qr.py`, `explore/p0_equations.ipynb` (static penetration-depth table from the initial commit) and `explore/nb/paper_figs.py` (paper figures, `notes/paper_draft.md` §3).

## 3. Claims

### Current table

This is `notes/paper_draft.md` §4 as of ffa4d9c (2026-10-23, research/paper-viability), copied verbatim; §4 is authoritative and this copy is not re-judged. "Confirmed" there means confirmed in the model by full TT or a closed form, and, for the rows the physics lane reviewed, cross-checked between AI lanes; it is not an experimental confirmation. No long-window satellite measurement exists.

| # | claim | status | evidence |
|---|---|---|---|
| 1 | First-order linearisation of TT for a phonon | prior art | Sondhauss & Wark 2003 eq. 25–29 (Entries 64, 69) |
| 2 | Closed-form H with the Bloch-wave (Riccati) depth dependence, valid inside the Darwin width where the plane-wave form is off by 3–8× | confirmed in the model; novelty bounded by **unread** Chukhovskii & Förster 1995, Wark & Lee 1999 | Entries 59, 64, 65 |
| 3 | H needs a long window: the strain must travel ≥ max(1/κ, x/π) Λ during it; closed form H(f; T_w) exact to first order at every window 0.14–300 ns | confirmed (TT 0.3 %); packet-free short form rejected below ~100 τ | Entries 71, 75 |
| 4 | Design numbers Si 400 / 17.48 keV: T_flat 19.6, T_half 32.8, T_90 52.2 ns; ripple with period 2x Λ/v | confirmed (TT to 0.002) | Entry 75 |
| 5 | Chalise et al. 140 ps window sees no crystal factor (H flat to 4 %); their low-frequency deficit is only partly the second-order term K = 0.65–0.88 | confirmed in the model; their normalisation unknown; any real beam also flattens the crystal factor (Entry 82) | Entries 66, 71, 82 |
| 6 | χ_ih is a second tabulated crystal parameter: 0.9 % steady, 1.4 % at 52 ns, 3–4 % at 8 keV | confirmed; pre-registered rule fired | Entry 77 |
| 7 | ±η side asymmetry, strain-spectrum-free, reads χ_ih/χ_i0 (1.9–6.2 %, sensitivity 0.02–0.07) | predicted and confirmed in the model (TT 0.06 %); unobserved; a single-ray observable: odd in δ, it averages to zero over a symmetric beam (Entry 82) | Entries 77, 78, 82 |
| 8 | Asymmetric Bragg = exact rescaling; one geometry factor g(√b + 1/√b)/2; T_90 shortens with Λ_asym | confirmed (TT 1e-16) | Entry 81 |
| 8b | Beam divergence / bandwidth: for σ_η ≫ κ + π/x the crystal factor is flat, κ√(π/2)/σ_η, at every window (x ≳ 10); H(f; T_w) and the ±η asymmetry are single-ray (meV, sub-µrad) observables; at x = 1–5 the tolerance is 0.3–0.6 µrad / 4–7 meV (8 keV) and the beam-averaged factor is non-monotonic in σ | confirmed (TT beam average vs closed form 0.02–0.24 %) | Entries 82, 83 |
| 9 | ν ≲ 0.1 ⇒ weight linear to 2 % (1 − K ≤ 1.8 ν²) | confirmed as a bound on the scanned domain (Bragg, x ∈ {2, 5}, one packet family, weight at the peak) | Entry 68 |
| 10 | "One dimensionless criterion joins the regimes" | falsified (spread ×10–14 at fixed ν) | Entry 68 |
| 11 | Formation law I_n = sin²/tanh²(πα\|J_n\|t̃), Bessel ladder, period-ratio calibration | confirmed; prior art in kind DeCamp 2001 (n = 0), Polikarpov 1987/88 (static); as a centre observable it needs the beam condition of 12b | Entries 1, 9, 13, 19, 24; tests |
| 12 | Order n reads the one-transit running mean of J_n(S A); zero-mean perturbations degenerate (≤ 3e-6 for S ≤ 6); boundary R = 0.2 | confirmed with a boundary | Entries 72, 76, 79 |
| 12b | Beam condition for the centre formation law: σ_η ≲ 0.3 w_n (0.1–0.3 µrad, Si 440 / 17.48 keV Laue; 0.6–1.4 µrad, Si 400 / 8 keV Bragg); at σ_η = w_n the first maximum loses 13–40 % | confirmed (full TT beam average, 8 cases) | Entry 84 |
| 8c | Polarisation: π = σ form with α → Cα (κ fixed), unpolarised = two-term closed-form sum (TT 0.02 %); negligible at Si 400 / 8 keV (C² = 0.12), 20–32 % at Si 440 / 17.48 keV; static Debye–Waller already in the X0h constants | confirmed | Entry 88 |
| 12c | Integrated Laue satellite population: flat-beam shape from σ_η ≈ 5 w_n (2–5 µrad, step) and 10 w_n (10 µrad, 1 t_tr ramp) with a one-channel detector (9–18 µrad); formation curve from TT (tabulated; 13–25 % off ∫J_0); Bragg population not clean | pre-registered threshold falsified: 3 w_n failed in 3 of 5 runs (Entry 87; Entry 86 failed under its own rule). 5 w_n (step) and 10 w_n (ramp) are post-hoc conditions from the same cases; confirmation needs a pre-registered run on new cases (T2s) | Entries 86, 87 |
| 13 | Signal maximum = Fisher-information maximum for a ps packet at one angle | negative result | Entry 70 |
| 14 | Bessel-zero resurrection at third order | confirmed in the model, unobservable (4e-5); **unread** Entin, Iolin–Entin | Entries 45, 51, 52, 54 (not in this paper; P4) |
| 15 | Realisability: S ≤ 6 at 1–2 GHz clean on the elastic side; drive power 6–900 W/cm² peak | constants only; harmonic column withdrawn (shear symmetry); transducer number unverified | Entries 73, 80 |

### Withdrawn, falsified or corrected

Hypotheses in this list are not to be reopened without new evidence (tratt brief, BACKLOG T1).

| Where | What | By |
|---|---|---|
| Entry 12 | "the peak position shifts dynamically" | withdrawn: kinematic interference (Entry 3) |
| Entry 12 | "the ±n asymmetry is a transit/dynamical effect" | withdrawn: a first-acoustic-wavelength effect, ∝ 1/α_ac (Entry 8) |
| Entry 12 | "no additional timescale" (session 1) | withdrawn: t_tr/α_n exists |
| Entry 9 | t_f ~ 1/α in Bragg | corrected to 1/α_n |
| Entry 31 | grid rule | bug found and fixed in the entry |
| Entry 41 | Entries 38-40 (chirp, walls, anomaly search) | "nothing qualitatively new": each effect has a known analogue |
| Entry 51 | dynamical localisation or diffusion in order space; single-phase breakdown metrics | absent; micromotion that averages away |
| Entry 56 | any "new mechanism" claim for the Entry 39 phase wall | withdrawn: it is a stacking fault per satellite (Authier & Simon 1968) |
| Entry 65 §2, Entry 66 §3 | "17 keV under-reads 20 GHz by a factor 2" for the Chalise packet; "two factors multiply, 0.33-0.45" | withdrawn for the 140 ps window by Entry 71; holds only for long windows (the strain travels ≥ max(1/κ, x/π) Λ during the window; a 10 ps packet read over 52 ns shows it, Entry 75) |
| Entry 68 | one dimensionless number sets the linearity limit (directive B3, strong form) | falsified: 1 − K spreads ×10-14 at equal ν |
| Entry 70 | directive B2 (crystal moves the signal maximum away from the information maximum) | negative in the case computed |
| Entry 73 | ε2/ε column and harmonic verdicts for the shear geometry | withdrawn by Entry 80 |
| Entry 75 | packet-free short form of H(f; T_w) | rejected below ~100 τ |
| Entry 65 §3(a) | the `tt` run at 24 RK4 steps per cycle (x ≥ 30) | not converged; "do not quote it" (48 steps per cycle is converged to < 0.5 %) |
| Entry 73 §1 | "u0 = 7.6 pm × S" | corrected to 15.3 pm × S by Entry 80 (7.6 is the S = 0.5 row) |
| Entry 82 | "an ordinary beam sees the kinematic law × a flat factor" | limited by Entry 83 to σ_η ≫ κ + π/x (x ≳ 10, the ps-packet band); at GHz-train frequencies the beam-averaged factor depends on x and σ |
| Entry 82 | "1e-4 bandwidth = 35 µrad-equivalent" (angle and bandwidth added in quadrature) | corrected in the Entry 82–83 addendum (c): after a crystal monochromator angle and energy are DuMond-correlated and σ_η must be computed from the optics |
| Entry 85 | first version with shear v_T | withdrawn, replaced by longitudinal [110] |
| Entries 86, 87 | integrated population beam-tolerant at 3 w_n | Entry 86 failed under its own rule (amplitude metric error recorded); Entry 87's pre-registered 3 w_n failed in 3 of 5 runs |

## 4. Reproducing the main computations

```bash
git clone https://github.com/NaNIsaac-Research/TraTT.git
cd TraTT
uv sync --extra dev
uv run pytest -q         # solver tests: analytic limits, Floquet cross-check, formation law
```

Poster-era entries (0-67) run on `main`:

```bash
uv run python explore/nb/e1_order.py          # Entry 1, formation order
uv run python explore/nb/e9_bragg.py          # Entry 9, Bragg
uv run python explore/nb/e59_transfer.py      # Entry 59, closed-form transfer function
uv run python explore/nb/e65_si400.py tt fig  # Entry 65, Si 400 with the full-TT check
uv run python explore/make_poster_figs.py     # poster figures (poster/ is frozen)
```

Paper-viability entries (68-88) need the branch:

```bash
git switch research/paper-viability
uv run python explore/nb/e68_nu_collapse.py run stats fit2 fig
uv run python explore/nb/e75_window_cf.py run posthoc fig
uv run python explore/nb/e82_divergence.py run fig
uv run python explore/nb/paper_figs.py fig1     # likewise fig2, fig4b
```

Run times and convergence checks are in each entry. Several sweeps take minutes; on the shared machines they are scheduled as heavy runs. These commands were collected from the entries and docstrings; they were not rerun for this document.

## 5. Open questions and implementation tasks

From `notes/paper_draft.md` §5 and §7, `notes/paper_candidates.md` and the tratt handoff; listed, not re-ranked.

- Novelty of claim 2 depends on three unread papers (Sondhauss & Wark 2003 in full, Chukhovskii & Förster 1995, Wark & Lee 1999) and six more named in the cross-review (T2d, waiting for the PDFs).
- Paper scope: P1 + P2 in one paper or P1 alone; whether to propose the ±η asymmetry as a measurement; asymmetric cut; whether to accept the 5 w_n condition (Isaac's decisions, tratt handoff).
- Claim 12c needs a pre-registered confirmation run on new cases (T2s).
- Model limits stated for the paper: two-beam, plane wave, quasi-static, centrosymmetric; Laue lossless only; strain as a phase only (no elasto-optic change of χ_h); first order in S for the closed form.
- Experimental side: no long-window satellite measurement; transducer peak power unverified.
- Future project named in Entry 51: a perturbative theory of the overlap regime and its comparison with the Entin / Iolin-Entin resonance theory.
- Missing sources for the lineage itself: the FTT package (`src/ftt/`) and `AW_TT_EXP/spec_calc.py` were not found; if they exist on another machine, their place in §1 can be checked against code.
