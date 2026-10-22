# E67 worker audit report

Date 2026-10-19, HEAD 1f9f8f8 (uncommitted tree), python 3.14.7, numpy 2.5.2, scipy 1.18.0.
Task: `notes/tasks/e67_worker_audit.md`. Owned files only:
`explore/nb/e67_worker_audit.{py,json,log}` plus this report.

## Command

    .venv/Scripts/python.exe explore/nb/e67_worker_audit.py

One process, 26 s per run. Three runs are in the log; run 3 is the final one
and is the state the JSON holds.

## Correction round 1 (applied)

Run 1 refined the TT peak on an 11-point `linspace` between the neighbours of
the grid argmax. The grid contains the inserted approximation peak time, so the
neighbouring intervals are unequal and the grid argmax itself was not in the
set; the "refined" peak could be lower than the grid peak
(B -2.1e-6, C -9.0e-7, short rise -4.4e-6). Fix: the grid argmax is now kept in
the refinement set, dependent fields (`tt_peak_local_refined`, `tt_excess`,
`excess_error`) are recomputed from it, and a refinement error above 1e-3 would
be a finding. Run 1 overwrote nothing, but run 2 overwrote the run-1 log; the
run-1 stdout was captured in the terminal and is reproduced at the top of the
log, labelled as a reconstruction without per-line timestamps. The script now
appends to the log.

## Findings by severity

No difference exceeds the 1e-3 task threshold. Nothing in Entry 67 or the
poster needs correction on numerical grounds.

Minor, for the record:

1. Cases B (T = 1) and C (T = 2) are not on the map's rise-time grid
   (nearest rows 0.998 and 1.9855). The JSON case values are computed off-grid
   and are correct; the npz values at the nearest row differ by 3.7e-4 (B) and
   1.3e-3 (C) because the row differs, not because of an error. The poster
   markers A–C are therefore between grid rows.
2. Eight carrier phases, used for the 12 map checks in the JSON, differ from
   16 by up to 6.0e-5 at S = 6, T = 0.05 (3.6e-6 at S = 3.8, T = 4). The
   A–C case values use 16 phases and are unaffected.
3. The base `required_nz` depth resolution is the largest discretization term
   for S = 1.5 (3.4e-5 between base and doubled), consistent with the JSON's
   `tt_refinement_max_change` for A. All other cases are at or below 2.5e-6.
4. The excess at S = 6, T = 0.05 (6.03e-4 approximation, 6.19e-4 full TT) is
   real but small; it is close to the approximation error scale (8.3e-5) and
   should not be read as a feature of the map.

## Numerical results (absolute incident-intensity units)

Observable: `|Dh(1)|^2` at the single point eta = +q (`rocking` called with
`eta=[q]`), averaged over equally spaced carrier phases with the envelope
argument fixed at t. Not an angular integral, not a time window. Verified in
`e67_overshoot_map.tt_average` and reproduced with an independently laid out
wrapper (batched versus single-time evaluation differ by 0; phase average at
t = 1+T, +0.013, +0.3 spreads by 1.4e-11; eta = -q gives the same steady value).

Laue normalization in `solve_laue`: D0(0) = 1, Dh(0) = 0, no absorption, chi_0
gauged out. Unmodulated eta = 0 gives sin^2(pi alpha) to 4e-16; with the
S = 6 drive, |D0|^2 + |Dh|^2 - 1 is at most 3.8e-8.

Direct depth quadrature (`scipy.integrate.quad` on the ramp segment plus the
exact filled segment, independent of the map's cumulative Simpson
antiderivative):

| case | S | T | direct vs map law | theta(t<0) | theta(1+T) - J1(S) | excess (direct) | npz at grid T | diff |
|---|---|---|---|---|---|---|---|---|
| A | 1.5 | 1 | 2.1e-9 | 0 | 0 | 0 | 0 (T=0.998) | 0 |
| B | 3.0 | 1 | 4.3e-9 | 0 | 0 | 0.178839 | 0.178463 (T=0.998) | 9.4e-8 |
| C | 3.85 | 2 | 1.6e-8 | 0 | 0 | 0.532657 | 0.531310 (T=1.9855) | 1.0e-7 |
| map max | 3.8 | 4 | 1.7e-8 | 0 | 0 | 0.603419 | 0.603419 | 2.1e-7 |
| short rise | 6.0 | 0.05 | 3.2e-10 | 0 | 0 | 0.000603 | 0.000603 | 1.5e-7 |

"diff" compares the direct excess recomputed at the grid row with the saved
npz value. Causality holds (theta = 0 before arrival) and the fully filled
endpoint equals the steady value exactly.

Time sampling of the approximation peak (optimizer peak minus grid maximum):
at the map's 2001 samples at most 2.0e-7; at the 101 samples used for the
JSON TT checks up to 3.7e-5 (C) and 1.9e-5 (map max).

Full TT, 16 phases, base and doubled `required_nz`, 63 times including the
approximation peak and t = 1+T:

| case | nz | depth 1x vs 2x (max/peak/steady) | phase 16 vs 32 | phase 8 vs 16 | approx error (max/peak/steady) | TT excess | approx excess | excess error |
|---|---|---|---|---|---|---|---|---|
| A | 2000 | 3.4e-5 / 3.4e-5 / 3.4e-5 | 2e-15 | 3.7e-8 | 1.4e-5 / 9.9e-6 / 9.9e-6 | 0 | 0 | 0 |
| B | 3200 | 2.5e-6 / 2.4e-6 / 1.6e-6 | 1e-11 | 1.8e-6 | 3.9e-5 / 1.3e-5 / 3.9e-5 | 0.178890 | 0.178839 | 5.2e-5 |
| C | 3880 | 1.2e-6 / 1.2e-6 / 3e-10 | 8e-12 | 3.6e-7 | 1.2e-5 / 6.3e-6 / 4.9e-7 | 0.532663 | 0.532657 | 5.8e-6 |
| map max | 3840 | 1.4e-6 / 1.4e-6 / 1e-9 | 2e-11 | 3.6e-6 | 3.3e-5 / 6.0e-6 / 9.3e-7 | 0.603414 | 0.603419 | -5.0e-6 |
| short rise | 5600 | 7.4e-8 / 6.0e-8 / 7.4e-8 | 1.5e-8 | 6.0e-5 | 8.3e-5 / 5.4e-6 / 1.0e-5 | 0.000619 | 0.000603 | 1.6e-5 |

TT time refinement (grid argmax retained, 11 extra points between its
neighbours): 0 in every case, so the inserted approximation peak time is the
TT maximum at this resolution. TT at t = 0 is 1.5e-8 in every case: this is
the unmodulated main-line tail at eta = q, not a causality defect.

## Pendellösung and mechanism

|Theta_1| <= max |J_1| = 0.5819 for every S, so pi alpha |Theta_1| <= 0.914
< pi/2 at alpha = 0.5. sin^2 is monotone on the reachable range; no
intensity-exchange maximum is crossed, and the reachable intensity is bounded
by 0.627. Largest |Theta_1| over the five cases 0.567, largest TT intensity
0.604. The map maximum 0.6034 at T = 4 is still rising at the boundary
(4.7e-4 per grid row) toward the quasi-static limit 0.627 already stated in
Entry 28, so it is a boundary value, not an optimum. The overshoot is the
Entry 15 re-weighting of the Entry 5 depth integral through the Bessel ladder.
Entry 67 contributes the parameter map and the checks; no new mechanism.

## Limitations

- Five sampled conditions plus the saved-map comparison; no global error
  bound for the 11,211-point map is claimed.
- TT convergence is assessed by one doubling of depth and of phases; no
  Richardson estimate.
- The approximation error (1e-5 to 8e-5) is the dominant term at these
  conditions and is specific to alpha/alpha_ac = 0.0125, n = 1, Laue, no
  absorption.
- Run-1 per-line timestamps are lost; its numbers are from the terminal capture.

## Changed files

- `explore/nb/e67_worker_audit.py` (new)
- `explore/nb/e67_worker_audit.json` (new, run 3)
- `explore/nb/e67_worker_audit.log` (new, runs 1–3)
- `notes/tasks/e67_worker_report.md` (this file)

No other file was modified. `explore/make_poster_qr.py` and
`figures/poster/qr_repo.png` appeared in the tree during the session and are
not mine.
