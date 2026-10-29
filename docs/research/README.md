# Studies

Every result in TraTT is a numbered entry in [`notes/lab_notebook.md`](../../notes/lab_notebook.md):
the question, the setup, the numbers, the script that produced them and the limits. This page groups
the entries into studies and says where each one stands. The notebook is the record; when this page
and an entry differ, the entry holds. All results are calculations; no experiment has been compared.

Status words are the notebook's: **verified** (against full TT, no fit), **estimate**, **negative
result**, **known** (prior art found), **withdrawn** or **corrected** by a later entry, **open**.
Rules fixed before a run (a pass/fail threshold written before the numbers) start at Entry 68; earlier
entries state a hypothesis before the setup but no threshold.

| # | Study | Entries | Status | In the README / poster |
|---|---|---|---|---|
| 1 | Formation laws: each satellite as a filled-depth slab | 0-27 | verified or estimate, per claim (tables in Entries 12, 16, 27); three early claims withdrawn (Entry 12) | README results 1 and 3, poster |
| 2 | Formation remembers the drive: path memory and the transient-only satellite | 28-37 | verified (claims 21-29, Entry 33); framing bounded by Entries 34-37 | README result 2, poster |
| 3 | Chirps, acoustic walls and an automated anomaly search | 38-41 | negative: "nothing qualitatively new" (Entry 41) | no |
| 4 | Floquet picture of the filled crystal and where independent satellites fail | 42-54 | verified within the model; boundary made S-dependent by Entries 53-54; novelty open until Entin and Iolin-Entin are read (Entry 50) | README result 3, solver checks |
| 5 | Acoustic phase walls against stacking-fault theory | 55-56 | known physics, reproduced within 1-3 % by the 1968 formula (Entry 56) | no |
| 6 | Strain spectrum to reflectivity: the transfer function H | 57-61, 64-66 | closed form verified (Entry 59); its linearisation is prior art (Entry 64); Entry 65 §2 and Entry 66 §3 withdrawn for short windows by Entry 71 (PR #16) | README result 4 |
| 7 | The quasi-static condition, and why a surface wave does not do it | 62-63 | estimate (Entry 62); negative for SAW geometry (Entry 63) | README, poster (Entry 62) |
| 8 | Overshoot map under a linear turn-on | 67 | verified at selected points (Entry 67); mechanism already in Entry 15 | README result 2, poster |
| 9 | Paper viability, T1 and T2 | 68-88 | draft on [PR #16](https://github.com/NaNIsaac-Research/TraTT/pull/16); conclusions being verified | no |

## 1. Formation laws (Entries 0-27)

**Question.** While the sound fills the crystal, is satellite n a Laue (or Bragg) slab of the filled
depth with coupling πα|J<sub>n</sub>(S)|, and what follows for its timing, order, width and
observability?

**Results.** The first maximum falls at t* = 1/(2α|J<sub>n</sub>(S)|) to within the time grid plus
~2 %, and at S = 3 the order is n = 2, 1, 3 (Entry 1); Bragg follows tanh² with
t<sub>99</sub> ≈ 0.953/(α|J<sub>n</sub>(S)|) to ~1-3 % (Entry 9); the characteristic time τ<sub>n</sub> = t<sub>tr</sub>/(α|J<sub>n</sub>(S)|) does not depend
on the crystal thickness (Entry 6); S can be read from two periods to ~1 % (Entry 13); the law holds
to a worst 0.031 in the 12 of 30 random cases with Λ<sub>ac</sub>/Λ<sub>P</sub> ≤ 0.05 (Entry 19), with an error of about 0.9 Λ<sub>ac</sub>/Λ<sub>P</sub>
(Entry 26). Realistic case: Si 440 at 17-30 keV, 150-300 µm, a 1-2 GHz shear wave (Entry 20).

**Withdrawn inside the study.** A dynamical peak shift (kinematic instead, Entry 3), the ±n asymmetry
as a dynamical effect (Entry 8), and "no additional timescale" (Entry 12).

**Limits.** Two beams, symmetric, non-absorbing Laue with a step onset unless stated; centre
intensities, not integrated orders (Entries 0, 1, 9). Acoustic nonlinearity and attenuation are not in
the model (Entry 15).

**Reproduce.** `explore/nb/e1_order.py` to `e25_zero.py` (one script per entry, named in it);
figures `explore/make_poster_figs.py`. Entry 31 fixed the depth-grid rule; the entries with S ≤ 3 and n ≤ 3 had used a hand-set grid and were not
re-run.

## 2. Path memory and the transient-only satellite (Entries 28-37)

**Question.** Satellite n reads the drive amplitude over the last transit time,
Θ<sub>n</sub> = ∫J<sub>n</sub>(S A(t−ζ)) dζ (Entry 28). Does formation depend on the path of the
drive, and can a satellite exist only during the transient?

**Results.** A satellite can reach 0.998 during the turn-on and 2×10⁻⁶ at the end (Entry 28); the
same amplitude reached up and down gives 0.010 and 0.494 (Entry 30); the brightest order switches in
time and lags the drive by about t<sub>tr</sub>/2 (Entry 31); a > 30:1 transient-to-final contrast
survives a 5 % error in S or 10 % acoustic loss (Entry 34), with contrast ∝ 1/r² (Entry 35).

**Framing.** "Do not claim it as a new kind of peak" (Entry 34); the condition is Θ<sub>1</sub>(final) = 0
(Entry 35); the Entry 35 statement holds for the satellite centre only (Entry 37). The steady-state
extinction length is prior art (Polikarpov & Skadorov 1987, Entry 29).

**Reproduce.** `explore/nb/memory_drive.py`, `e28_transient_only.py` to `e37_domains.py`; tests in
`tests/test_formation.py` and `tests/test_analytic.py`.

## 3. Chirps, walls and the anomaly search (Entries 38-41)

**Question.** Are there transient effects other than centre-intensity changes when the local acoustic
wave vector changes (Entry 38)?

**Results.** A chirp gives a Landau-Zener plateau and raises the integrated satellite up to 5.3× with
no focusing (Entry 38); a π phase wall gives up to 2.58× (Entry 39); 250 automated cases found
nothing that lowers the integrated satellite by more than 16 % (Entry 40). Verdict: "Nothing
qualitatively new appeared tonight" (Entry 41).

**Reproduce.** `explore/nb/e38_chirp.py`, `e39_walls.py`, `e40_search.py`, `e41_validate.py`.

## 4. Floquet picture and the limit of independent satellites (Entries 42-54)

**Question.** For a uniformly filled crystal, where does the picture of independent satellites break
down as the acoustic wavelength approaches the Pendellösung length, and what replaces it?

**Results.** An exact Floquet solver agrees with full TT to 1.6×10⁻⁶-1.3×10⁻⁵ (Entry 42). A
nominally dark order becomes fully bright near R ~ 1, and the Bessel zero is renormalised (Entries 45,
52). With the exact phase average, the 5 % population error is reached at R = 0.34-0.57 depending on S
(Entry 54). No localisation in order space (Entry 43).

**Corrections.** Entry 52 corrects Entry 45 and Entry 49; Entry 53 finds the 4-phase average not
converged and Entry 54 replaces it with the exact average.

**Limits.** Filled crystal, steady state, non-absorbing; not the transient with a front inside the
crystal (Entry 53). Nothing here may be called new before Entin and Iolin-Entin (1983) are read in full
(Entry 50).

**Reproduce.** `src/tratt/floquet.py`; `explore/nb/e43_phase.py` to `e54b_width.py`, for example
`python explore/nb/e54_exactmap.py` (about 25 min in parallel, Entry 54) and
`python explore/nb/e54c_summary.py`; caches are committed next to the scripts.

## 5. Acoustic phase walls (Entries 55-56)

**Question.** Are the Entry 39 wall effects a known stacking-fault effect or a new capability?

**Result.** For n = 1 and 2 the full TT integrals of Entry 39 follow the 1968 plane-wave
stacking-fault formula of Authier & Simon within 1-3 %; "any 'new mechanism' claim for C is
withdrawn" (Entry 56). The q-wall comparison needs part II of that paper, which was not read.

**Reproduce.** `python explore/nb/e55_fault_check.py` (no TT solver; Entry 39 numbers typed in).

## 6. Transfer function from strain spectrum to reflectivity (Entries 57-61, 64-66)

**Question.** When can the frequency content of a measured diffracted intensity be read as the
frequency content of the acoustic wave (Chalise et al., arXiv:2603.28071)?

**Results.** The Fourier weight is the strain spectrum times a crystal transfer function, given in
closed form and matching TT with no fit parameter (medians 0.984-1.021, Entry 59). The first-order
linearisation is prior art (Sondhauss & Wark 2003); with the Bloch wave restored it equals Entry 59
exactly (Entry 64). For Si 400 at 17.48 keV, H(20 GHz)/H(100 GHz) = 0.51 for a long train (Entry 65).

**Corrected on PR #16.** Entry 71 withdraws Entry 65 §2 and Entry 66 §3 for a 140 ps measurement:
the closed form is the infinite-window limit.

**Reproduce.** `explore/nb/e58_chalise_ref.py`, `e59_transfer.py`, `e64_sw_compare.py` (9 s),
`e65_si400.py`, `e66_harmonic.py`. Do not quote the `tt` run in `e65_si400.log` (not converged at
x ≥ 30, Entry 65).

## 7. Quasi-static condition and surface waves (Entries 62-63)

**Results.** In the poster's window an X-ray crossing takes 0.99 ps, 0.2 % of a 500 ps acoustic period
(Entry 62). "No result of this work transfers to SAW geometry as it stands": a surface wave cannot fill
the extinction depth and keep its satellites resolved (Entry 63).

**Reproduce.** Entry 62 is arithmetic; `explore/nb/e63_saw.py`.

## 8. Overshoot map under a linear turn-on (Entry 67)

**Question.** Where does a linearly increasing amplitude give a first-satellite centre intensity
above its filled steady value?

**Results.** 11,211 (S, T) pairs from the Θ<sub>n</sub> law; the largest excess, 0.603 at S = 3.8 and
T/t<sub>tr</sub> = 4, lies on the rise-time boundary of the scan. Full TT at selected conditions
agrees to 8.65×10⁻⁵. The mechanism is the one of Entry 15; the new part is the map and its checks.

**Limits.** Selected checks, not a global error bound; one thickness, geometry, order and envelope;
a centre observable, not an integrated population.

**Figure.** [`figures/overshoot.png`](../../figures/overshoot.png) (PDF beside it): the map, the twelve
full-TT checks, the three traced cases against full TT and their difference in time; caption in the
[README, result 2](../../README.md#results).

**Reproduce.** `explore/nb/e67_overshoot_map.py`, `e67_worker_audit.py` write
`explore/nb/e67_overshoot.npz` and `.json`;
`uv run --group figures python explore/make_overshoot_figure.py` draws the figure from them without
recomputing, and `uv run python explore/make_poster_figs.py f7` the poster version.

## 9. Paper viability (Entries 68-88, PR #16)

Draft work toward a paper on [PR #16](https://github.com/NaNIsaac-Research/TraTT/pull/16)
(branch `research/paper-viability`): T1 (Entries 68-74, 80) and T2 (Entries 75-79, 81-88). Every
computational entry there has a rule written before its run. The conclusions are being verified and are
not summarised here; the branch notebook gives each entry's verdict, and its `notes/paper_candidates.md`
the candidate papers. The scripts (`explore/nb/e68_*.py` to `e88_*.py`) exist on that branch only.

## Not in a study

`results_sweep_laue.json` is the first-session sweep; Entry 31 calls its convergence times
uninformative and asks for a re-run with the new grid rule if they are used.
