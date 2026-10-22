# Poster fact sheet (task)

Status: assigned to worker 2026-10-19.

## Objective
Verified facts for the final poster rewrite. The supervisor writes poster text;
this sheet is the evidence. Every number needs a source (file:line or Entry N)
and, for tests, the actual value from a run today.

## Scope / ownership
Worker writes only `notes/tasks/poster_facts.md` (append a `## Facts` section
below). Everything else is read-only: poster/, figures/, notes/lab_notebook.md,
src/, tests/. No commits, no subagents, no new research runs beyond pytest.

## Needed (one short line each, with source)
1. Equations exactly as implemented in src/tratt/core.py: Laue amplitude
   equations for D0, Dh; Bragg Riccati form for R = Dh/D0, its boundary
   condition and why; integrator (fixed-step RK4? step rule, required_nz);
   normalization and dimensionless variables (zeta, t~, eta, alpha, S, q, alpha_ac).
2. Phase field / drive as implemented in src/tratt/drive.py (and cube.py:
   how I(eta, t~) is assembled per time). Exact formula for phi(zeta, t~),
   envelope A, causality, sign conventions.
3. Quasi-static argument: X-ray transit vs acoustic period ratio
   (poster used "< 1.2 %", Entry 62) and its derivation.
4. Validation: run `.venv/Scripts/python.exe -m pytest -q tests` and list each
   test file's checks with tolerance and achieved error (analytic 1e-9?
   Floquet 3e-7? convergence?). Record pass/fail counts and runtime.
5. Result 1 facts: formation law I_n = sin^2(pi alpha_n t~) Laue,
   tanh^2 Bragg, alpha_n = alpha|J_n(S)|, tau_n; conditions; validity limit
   (R <~ 0.3, error < 5 %, limit 0.34-0.57; Entries 53, 54); line-shape fact
   (0.1-0.2 %, ~52 %, Entry 23) and which figure shows what (f1, f2, f4).
6. Result 2 facts: Theta_n memory law (Entries 28, 30, 34; f3) and E67 map
   (f7) numbers; what f3 panels show exactly.
7. Assumptions list as stated in DESIGN.md / notebook: symmetric two-beam,
   absorption default, quasi-static, longitudinal strain only?, anything else.
   Also: what is NOT verified (no experiment comparison, etc.).
8. Steady-state prior work references as cited in the notebook (E7).
Flag any poster number (current or 1f9f8f8 version) that does not match source.

## Deliverable
Fact section in this file; reply in Herdr with one line: done + count of mismatches.

## Facts

Worker, 2026-10-19. Repo HEAD 892696e, python 3.14.7, numpy 2.5.2, scipy 1.18.0.
Sources are file:line or "E<n>" = notebook Entry n (notes/lab_notebook.md).
"Poster 1f9f8f8" = the committed version; "poster now" = poster/poster.md in the tree today.
Only pytest was run as a project command. Test margins in item 4 were measured with a
throwaway script in the scratchpad that re-evaluates the test expressions (nothing written in the repo).

### Mismatch summary (poster number vs source): 4 hard + 1 unsourced, all in poster 1f9f8f8; 0 in poster now

| # | poster 1f9f8f8 says | source says | verdict |
|---|---|---|---|
| M1 | X-ray passes the crystal in "less than 1.2 % of one acoustic period" | E62: beta = 2 pi f L / c = 1.2e-2 is a phase in rad. As a time: L/c = 0.99 ps against a 500 ps period = 0.2 % | mismatch (rad read as fraction of a period; the bound is true but 6x loose) |
| M2 | "exact Floquet solver (3x10^-7)" | E42: 3e-7 is the change under K+4 truncation and the flux defect. Floquet vs full TT is 1.6e-6 to 1.3e-5 (E42); today 5.2e-7 to 3.8e-6, test tolerance 5e-5 | mismatch (3e-7 is not the agreement with TT) |
| M3 | "~52 % of the integrated intensity remains in two side peaks" | E23: window integral at the dark point is 52 % of its own maximum (0.755 / 1.450), window abs(eta - nq) < q/2, case S=1.5, alpha=3, alpha_ac=60. Not a fraction of the total. Lobes at (eta - nq) t ~ +-6.4 | mismatch in wording |
| M4 | "Error < 5 % for R <~ 0.3; limit R = 0.34-0.57" given as the validity of the formation law | The numbers match E54, but they are the steady-state population error E_pop (binned median, phase-averaged, filled crystal, independent-channel sum). For the time-resolved centre law the error is ~0.9 R absolute (E26, S=1.5), i.e. ~0.27 at R=0.3; E19: R<=0.05 gives <=0.03, R<=0.1 gives <=0.08 | mismatch in scope (two different quantities) |
| M5 | Outlook "agreement with full TT: 2-5 %" | E59 gives median ratios 0.985-1.021 (R_D = 0.05-0.2), ratio range 0.94-1.06 at S=0.05, +-3.5 % unexplained scatter, test tolerance 3 % (tests/test_core.py:185). No line states "2-5 %" | not found as a stated number |

Everything else checked in either poster version matches (list at the end).

### 1. Equations as implemented (src/tratt/core.py)

- Variables: zeta = z/L in [0,1]; eta = deviation parameter times L (dimensionless); alpha = L/Lambda_P (real, non-absorbing); chi_0 gauged out (core.py:3-12, DESIGN.md:37-52).
- Laue, entrance D0(0)=1, Dh(0)=0, both beams +z (core.py:130-137, DESIGN.md:23-24):
  `dD0/dzeta = i pi alpha e^{+i phi} Dh`, `dDh/dzeta = i pi alpha e^{-i phi} D0 + i eta Dh`.
  Observable |Dh(1)|^2 in units of the incident intensity |D0(0)|^2 = 1. Lossless: |D0|^2+|Dh|^2 = 1.
- Bragg (core.py:179-185): `R = Dh/D0`, `dR/dzeta = -i pi alpha e^{-i phi} - i (eta + i kappa) R - i pi alpha e^{+i phi} R^2`, kappa = 0 default. Condition R(1)=0 (no diffracted wave enters from the back face; Dh travels -z). It is integrated backward from zeta=1 to 0, the stable direction, so the two-point problem becomes an initial value problem. Output R(0), reflectivity |R(0)|^2. kappa = normal absorption, enters as eta -> eta + i kappa.
- Integrator: fixed-step classical RK4, step h = 1/n_z, no adaptivity (core.py:136-150). Measured order 3.98, 4.00, 4.00 for n_z 64-512 (tests/test_analytic.py:72).
- Step rule `required_nz(alpha, alpha_ac, per_cycle=20, S, eta_max)` (core.py:64-82): `n_z = max(256, int(20 * max(alpha, alpha_ac, eta_max/(2 pi) + S alpha_ac)))`. Values used in the E67 audit (alpha=0.5, alpha_ac=40, eta_max=q): S=1.5 -> 2000, S=3 -> 3200, S=3.85 -> 3880, S=6 -> 5600.
- Time is not in the solver: one frozen phi(zeta) per call; time enters only through phi (stroboscopic).
- Verified by tests: Laue eta=0 gives sin^2(pi alpha); Bragg phi=0, eta=0 gives tanh^2(pi alpha) (tests/test_analytic.py:58).

### 2. Drive and cube (src/tratt/drive.py, cube.py)

- `phi(zeta; t) = S * A(t - zeta) * sin(q zeta - q t)` (drive.py:96, DESIGN.md:30). S = h.u0, q = K L = 2 pi alpha_ac, alpha_ac = L/Lambda_ac. Non-dispersive wave: w = Omega t_tr = q (drive.py:30-40). Only S and alpha_ac (plus rise) are drive parameters. R = Lambda_ac/Lambda_P = alpha/alpha_ac (E20).
- Retarded time s = t - zeta, so phi = -S A(s) sin(q s); the wave travels +z at v_s; t~ = t/t_tr, t_tr = L/v_s.
- Envelope A (drive.py:82-88): rise = 0 -> step, A = 1 for s >= 0 and 0 for s < 0 (A(0)=1); rise > 0 -> C1 smoothstep x^2(3-2x), x = clip(s/rise, 0, 1). Causal: A = 0 ahead of the front, i.e. zeta > t.
- The E67 map and the E28/E30 memory figures do not use Drive's smoothstep. E67 uses a linear ramp A = clip(s/T, 0, 1) (explore/nb/memory_drive.py:68); f3 uses memory_drive HistoryDrive with ramp and triangle envelopes.
- Sign convention: channel n sits at eta_n = +n q (drive.py:122-140). tests/test_core.py:55-71 pins the sign of the eta term with the Born integral `Dh(1) = i pi alpha int e^{-i phi} e^{i eta (1-zeta)}`. The docstring at tests/test_core.py:38 says "-n*q"; the code and the Born test say +n q (docstring slip only).
- cube.py: for each time t the drive gives phi at a column of times, `rocking` solves all eta at once, and times are blocked (~5e4 live elements per sweep) and stacked into I(eta, t) of shape (n_times, n_eta). `front_and_full` returns the front cube and the same-phase steady cube `phi = S sin(q zeta - q t)` on identical grids. `satellite_cube` returns |Dh(S) - Dh(0)|^2, a constructed observable, not an intensity an experiment measures (cube.py:97-113).
- No time derivative of the X-ray field and no memory between snapshots (cube.py:10-13).

### 3. Quasi-static argument (E62, DESIGN.md:14-16)

- Criterion: the lattice is static during one X-ray traversal if the acoustic phase advanced in that time is small: beta = Omega L / c = 2 pi f L / c, L the slab thickness, c the vacuum speed of light. The Pendellosung-length version 2 pi f Lambda_P / c is smaller, so beta is conservative.
- Worst case of the proposed window (Si 440, symmetric Laue, 30 keV, L = 296 um, f = 2 GHz): beta = 1.2e-2 rad; L/c = 0.99 ps = 0.2 % of the 500 ps period. Other rows: 17.48 keV, 163 um, 1.1 GHz: 3.8e-3; 2.0 GHz: 6.8e-3; 30 keV, 0.6 GHz: 3.7e-3.
- I recomputed: 2 pi (2e9)(296e-6)/2.998e8 = 1.24e-2; (L/c) x f = 0.00197. DESIGN.md example (1 GHz, 10 um): 2.1e-4, quoted as 2e-4.
- Correct phrasing: "0.2 % of an acoustic period" or "beta = 0.012 rad". "1.2 %" appears nowhere as a fraction of a period.
- Not covered: the X-ray response time of the crystal (~Lambda_P/c, Shvyd'ko & Lindberg regime). E62 uses L, not the slanted path L/cos(theta_B). My own arithmetic, not in the notebook: for Si 440 theta_B = 21.7 deg at 17.48 keV and 12.4 deg at 30 keV, so the path is 7 % and 2 % longer. It does not change the conclusion.

### 4. Validation: `.venv/Scripts/python.exe -m pytest -q tests` run today

Result: **54 passed, 0 failed, 46.2 s** (wall 48 s). Files: test_analytic 11 tests, test_core 14, test_floquet 9, test_formation 20.
Tolerance is the coded one. "Achieved" is my re-evaluation of the same expression today; "not measured" means the test passed and I did not re-evaluate it.

Caution: `np.allclose(a, b, atol=x)` also applies the default rtol = 1e-5. Where a test uses allclose, the effective tolerance is x + 1e-5 |b|. This matters for the nominal 1e-9 losslessness test and the 1e-12 / 1e-10 / 1e-8 / 1e-6 allclose tests below.

| test | check | coded tolerance | achieved today |
|---|---|---|---|
| analytic: Laue full rocking curve, alpha 0.3 / 1.0 / 2.7, eta in +-60, n_z 8192 | D0, Dh vs closed form | strict < 1e-9 | max abs 2.3e-11 / 7.6e-11 / 2.2e-10 |
| analytic: Bragg centre tanh^2, alpha 0.25 / 1 / 4 | abs error | 1e-10 | <= 8.9e-16 |
| analytic: RK4 order | log2 error ratios, n_z 64-512 | > 3.8 | 3.98, 4.00, 4.00 |
| analytic: unitarity defect vs n_z 64/128/256 | strictly decreasing | monotone | pass; value not measured |
| analytic: zero coupling transparent | D0=1, Dh=0 | allclose atol 1e-12 (+rtol) | not measured |
| analytic: constant phase offset | intensity unchanged | allclose atol 1e-10 (+rtol) | not measured |
| analytic: required_nz at S=6, 5q channel | n_z vs 2 n_z | allclose atol 1e-4 | not measured |
| core: Pendellosung alpha 0.25 / 0.5 / 0.9 / 1.7 | sin^2(pi alpha), n_z 2048 | 1e-8 | 1.2e-15 / 4e-16 / 5e-14 / 2e-12 |
| core: lossless with modulation | abs(D0)^2+abs(Dh)^2 = 1 | allclose atol 1e-9 (effective ~1e-5 from rtol) | 5.4e-6 at the test's default n_z (S=1.3, alpha_ac=5, alpha=0.8) |
| core: satellites at eta = n q | peak within 0.1 q | 0.1 q | pass; not measured |
| core: kinematic limit vs Born integral | rel to peak | 1e-4 | 4.3e-5 |
| core: kinematic channel heights vs J_n(S)^2, S 0.4 / 0.9 | I_n/I_0 | rel 1 % | not measured |
| core: step onset periodic after transit | repeats after one acoustic period | allclose atol 1e-10 (+rtol); also a != c at 1e-3 | not measured |
| core: Bragg total-reflection plateau | R > 0.99 inside, < 0.5 outside, <= 1+1e-9 | as stated | not measured |
| core: Bragg absorption vs Darwin-Prins root | max abs R difference | 1e-5 | 4.0e-7 |
| core: Bragg reflectivity bounded with modulation | <= 1+1e-9 | 1e-9 | not measured |
| core: Bragg Fourier weight vs first-order transfer function (E59) | ratio to 1 | atol 0.03 | not measured |
| floquet: Floquet vs full TT, 3 parameter sets | max abs intensity difference | allclose atol 5e-5; flux atol 1e-6 | 2.1e-6 / 3.8e-6 / 5.2e-7; flux defect 8e-11 / 3.3e-8 / 4e-14 |
| floquet: truncation K+4 and masked coupling | rocking change; masked -> 0 | allclose atol 1e-8; 1e-14 | 2.3e-7 for the K+4 change (the 1e-8 atol passes only through rtol); masked case not measured |
| floquet: S=0 reduces to unmodulated Laue | abs | allclose atol 1e-10 | 2.7e-15 |
| floquet: Bessel-zero third-order resurrection (E45) | P / sin^2(g_eff) - 1 | 0.02 | not measured |
| floquet: two-band gap vs 2 pi alpha abs(J_n) (E46) | gap, monodromy det | rtol 0.03; det atol 1e-5 | not measured |
| floquet: effective 2x2 Hamiltonian third order (E52) | error ~ R^4 | log-slope between 3.5 and 4.5; 1e-3, 1 % | not measured |
| floquet: exact phase average = sum of Floquet populations (E53) | b_m(phi) = e^{i m phi} b_m(0); 16-phase vs exact; 4-phase fails | 1e-12; 1e-3; > 0.1 | not measured |
| formation (20 tests) | formation-time logic, front causality, steady-state equality after transit, cube agreement, channel windows, filled-depth Pendellosung law, accumulated-coupling law, Bragg saturation, dark-centre integral, history law, two domains, chirp | tolerances in tests/test_formation.py, not itemised here | pass; not measured |

Poster claim "analytic solutions (10^-9)": supported by the strict closed-form Laue test (achieved 2.2e-10) and Bragg (1e-15). The losslessness defect is 5e-6 at the default grid; no 1e-9 claim should be attached to it.

### 5. Result 1: formation law (E1, E6, E9, E16, E19, E23, E26, E43, E53, E54)

- Law (centre intensity at eta = n q, step onset, 0 <= t~ <= 1): Laue `I_n = sin^2(pi alpha_n t~)`, Bragg `I_n = tanh^2(pi alpha_n t~)`, `alpha_n = alpha |J_n(S)|` (E1, E9). Origin: the filled layer [0, t~] is a uniform slab of coupling pi alpha_n; at exact resonance Laue transfer matrices are rotations about one axis (angles add).
- Time scale: Laue period in t~ is 1/alpha_n, first maximum at t~ = 1/(2 alpha_n); `tau_n = t_tr / alpha_n = Lambda_P / (v_s abs(J_n(S)))`, independent of L (E6; verified in the E20 table). Bragg saturates, t99 = atanh(sqrt(0.99) tanh(pi alpha_n)) / (pi alpha_n), ~0.953/alpha_n for large alpha_n, capped at 1 (E9). Laue has no saturation: only its end point is set by the transit.
- Order follows abs(J_n(S)), not n: at S=3, alpha=2 the first maxima come in the order n = 2, 1, 3 (t* sim 0.500, 0.750, 0.825; predicted 0.514, 0.737, 0.809; E1).
- Law error (max abs over t~ in [0,1], alpha_ac = 20 unless noted): Laue E1 0.000-0.079 (largest 0.079 at S=0.5, alpha=2, n=1, the static-tail case of E2); Bragg E9 0.004 / 0.006 / 0.031 / 0.043 for (S, alpha, n) = (1.5, 0.5, 1), (1.5, 1, 1), (1.5, 2, 1), (3, 2, 2).
- Validity of the centre law: error set by R = Lambda_ac/Lambda_P alone, ~0.9 R absolute, S = 1.5, single acoustic phase (E26: R = 0.0125 -> 0.005-0.013; 0.071 -> 0.015-0.062; 0.22 -> 0.05-0.19; 0.40 -> 0.18-0.40). Random non-integer conditions (E19, 30 cases): R <= 0.05 worst 0.031; 0.05-0.10 worst 0.075; 0.10-0.20 worst 0.112. E16's "R <= 0.1 within 0.05" is superseded by E19.
- Validity of the steady-state population picture (E43, E53, E54; filled crystal, Laue, non-absorbing): E_pop = order-window population error against the independent-channel sum, phase-averaged. R where the binned median reaches 5 % / 20 % / 50 % (bins x1.3; exact where available):

| S | 0.5 | 1 | 2 | 3 | 5 | 8 |
|---|---|---|---|---|---|---|
| 5 % | 0.44 | 0.34 | 0.44 | 0.34 | 0.57 | 0.57 |
| 20 % | 0.73 | 0.57 | 0.95 | 0.95 | 0.95 | 1.22 |
| 50 % | 4.40 | 2.04 | 2.04 | 1.58 | 2.64 | 2.64 |

  So "limit 0.34-0.57" is the 5 % row. It is a binned median, not a bound: for kinematic points (alpha <= 0.2) the median is 4.4e-4 and the maximum 7.4e-2 (E54). The phase-averaged map used 16 phases; the exact average differs by up to 1.3e-2 in E_pop on 437 checked points; 2 of 437 change regime at the 0.05 edge (E54). The 4-phase map of E43 was not converged (E53).
- Poster f4 plots E_pop against R for points with alpha_ac >= 2, nine S values, dashed line at R = 0.3 (explore/make_poster_figs.py:227-253); 0.3 is below every 5 % boundary above (lowest 0.34).
- Line shape (E23; Laue, n=1, S=1.5, alpha=3, alpha_ac=60, alpha_1 = 1.674): at the dark point alpha_n t~ = 1.010 the centre is 0.002 (0.1-0.2 % of its maximum 0.999); the window integral (abs(eta - nq) < q/2) is 0.755 pi^2 alpha_n against a maximum 1.450, i.e. 52 % of that maximum (see M3); side lobes at (eta - nq) t = -6.74 / +6.42 (theory +-6.36). A second case (S=1.5, alpha=2, alpha_ac=40) gives centre 0.001, window 0.751 (theory 0.771), lobes -6.46 / +6.28. Mechanism: each centre maximum is the arrival of a Pendellosung fringe moving inward in eta.
- Which figure shows what (explore/make_poster_figs.py): f1 = collapse of full TT onto the two formulas for (S, alpha, n) = (0.5, 2, 1), (1.5, 2, 1), (2, 4, 2), (1.5, 4, 1), alpha_ac = 20, n_z = 1200, Laue left, Bragg right (E1, E9). f2 = S=1.5, alpha=3, n=1, alpha_ac=60: left I(eta, t~) full TT, right centre cut against sin^2(pi alpha_1 t~) (E22, E23). f4 = see above. f0 = schematic, alpha=0.6, S=1.5, alpha_ac=5, t~=0.62, phi from `Drive.phi` and a real `rocking` curve. f6 = abs(J_n(S)), n = 0-3, S in [0, 5], known weights, no dynamics.
- The integrated-intensity law is looser than the centre law: 5-15 % of pi^2 alpha_n rms (E2b). The committed sentence "satellite n has the intensity of a uniform crystal of thickness v_s t" is exact in form for the centre, approximate for the integral.

### 6. Result 2: memory law and E67 map (E5, E15, E28, E30, E34, E67)

- Accumulated-coupling law (E5): `I_n(t~) = sin^2(pi alpha Theta_n)` (Laue), `tanh^2(pi alpha Theta_n)` (Bragg, exact at resonance for any real depth-dependent coupling, E28); `Theta_n(t) = int_0^1 J_n(S A(t - zeta)) sign_n dzeta`. The signed integral is taken before the modulus (J_0 changes sign for S=3). A finite rise adds no new time scale: it re-weights the depth integral. Leading order in pi alpha / q; residual ~ (alpha/alpha_ac)^2 (E5).
- Memory (E28, E30): the crystal holds the drive of the last t_tr, so the satellite reports the drive delayed by ~t_tr/2 and smoothed; a finite, known memory length, not thermodynamic hysteresis. E34: "transient-only" is the slow-ramp end of the steady-state Bessel ladder; the framing must not claim a new kind of peak.
- E28 numbers (Laue, alpha=0.5, alpha_ac=40, S_f = j_{1,1} = 3.8317, linear ramp T): max_t I_1 = 0.023 / 0.302 / 0.606 for T = 0.25 / 1 / 4, final I_1 = 5e-10; quasi-static limit sin^2(pi alpha max J_1) = 0.627. n=1 is the brightest order during the transient and absent at the end. Law error <= 0.008 (E30).
- Robustness (E34, ramp T=2): contrast > 30:1 survives S off by +-5 % (final/max 0.03) or 10 % acoustic loss across L (final/max 0.03); 20 % loss gives 0.13.
- E30(a), triangular pulse S_max = 3, I_1 on the way up / down at A = 0.3: Laue T=1: 0.010 / 0.494; T=4: 0.146 / 0.510; at A = 0.9, T=4 the order reverses (0.544 / 0.355) because the path crosses the J_1 maximum (S A = 1.84).
- What f3 shows (poster 1f9f8f8 only; poster now has no f3; explore/make_poster_figs.py:197-224, explore/make_memory_figure.py panel_a and panel_b): 2x2. Top row = input envelopes: left linear ramp, rise 2 t_tr; right triangles, rise = fall = 1 and 4 t_tr. Bottom left (panel a): Laue centre intensity I(nq, t~) for n = 1, 2, 3 at S_f = j_{1,1} (J_1 = 0), ramp T=2, alpha=0.5, alpha_ac=40; points full TT, lines the Theta_n law; dashed line at t~ = 3 where the ramp has left the crystal. Bottom right (panel b): I_1 against S A(t~) for the triangular pulse S_max = 3, T = 1 (blue) and 4 (orange), arrows give direction; increasing and decreasing branches differ. Panels c (S=10 revival) and d (pi flip packet) exist only in figures/poster_memory.png.
- E67 map (audited and accepted; explore/nb/e67_overshoot_map.py, e67_overshoot.json, e67_worker_audit.json): Laue, alpha = 0.5, alpha_ac = 40 (R = 0.0125), n=1, no absorption, linear ramp A = clip(s/T, 0, 1) then held. Observable = first-satellite centre intensity at eta = +q, in units of incident intensity, carrier-phase averaged at fixed envelope time. Grid 101 rise times (0.05-4) x 111 amplitudes (0.5-6) = 11,211 points. Colour = Delta I = max_t I - I_steady, I_steady = sin^2(pi alpha J_1(S)).

| case | S | T/t_tr | peak | steady | Delta I |
|---|---|---|---|---|---|
| A | 1.5 | 1 | 0.590505 | 0.590505 | 0 |
| B | 3.0 | 1 | 0.436665 | 0.257829 | 0.178836 |
| C | 3.85 | 2 | 0.532790 | 0.000133 | 0.532657 |
| map maximum | 3.8 | 4 (upper grid edge) | 0.6038 | | 0.603419 |
| short rise | 6.0 | 0.05 | 0.1779 | 0.1773 | 0.000603 |

  B peak / final = 0.436665 / 0.257829 = 1.6936 (poster "1.69" matches). The map maximum is a boundary value, still rising 4.7e-4 per grid row, bounded by 0.627. Cases B and C are not on the rise-time grid (nearest rows 0.998 and 1.9855), so the markers sit between rows. C is near but not at the J_1 zero (j_{1,1} = 3.8317).
- Audit numbers (E67 worker audit): direct depth quadrature vs map law <= 1.7e-8; TT depth, phase and time convergence all < 1e-3 (largest TT-vs-approximation difference 8.3e-5; TT excess within 5.2e-5 of the approximation). Spot checks at 5 conditions; no global error bound for the map. Mechanism = E15 (Bessel ladder sampled across the ramp; no Pendellosung since pi alpha max abs J_1 = 0.914 < pi/2); E67 adds the parameter map, not a new mechanism.

### 7. Assumptions and what is not verified

Assumptions (DESIGN.md:61-77, E62):
1. Two-beam, symmetric geometry (gamma_0 = gamma_h; needed for the chi_0 gauge).
2. Plane wave, monochromatic: no divergence or bandwidth.
3. No absorption, Im chi = 0, alpha real. Excluded: uniform absorption (harmless, common factor) and the Borrmann effect (not harmless). Bragg kappa exists in the solver (E59) but is off in the poster results; Laue absorption was estimated only (E11), not simulated.
4. chi_h chi_hbar = abs(chi_h)^2; fixed polarization factor C (sigma 1, pi cos 2 theta_B), no mixing.
5. The acoustic wave enters only as a phase phi = h.u(z,t); chi_h unchanged (no elasto-optic change, no Debye-Waller change). Strain is inside phi. The wave is a single plane wave depending on depth only, non-dispersive (w = q); no lateral structure. Nothing requires it to be longitudinal; E20's example is a shear wave, v_T = sqrt(c44/rho) = 5846 m/s (c44 textbook value).
6. Stroboscopic (quasi-static) X-ray response, beta <= 1.2e-2 in the window (item 3).
7. No acoustic nonlinearity, attenuation, transducer ringing or depth-inhomogeneous amplitude (E15 and E34 only test a simple attenuation exp(-gamma zeta)).
8. Normalized observables only; the absolute scale needs the dropped exp(-mu z) factor (DESIGN.md:43-47). eta = 0 is the refraction-corrected Bragg angle (6.5 arcsec shift for Si 111 at 8 keV).

Not verified:
- No comparison with any experiment. Everything is calculation. The Si 440 proposal (E20: 17.48-30 keV, L = 163-296 um, ~1-2 GHz, strain ~1.5-2.7e-5, tau_1 = 16.7-30.3 ns for S=1.5, L = 3 Lambda_P) is untested. Unverified in E20: c44, launching a clean ~1 GHz shear wave through 0.2-0.3 mm of Si, GHz attenuation.
- The rule "R <~ 0.3" has no analytic derivation; it comes from binned medians of a sampled map (1200 points, E43) and 437 exact checks (E54).
- The E67 map is a sampled map of an approximation, checked at five TT conditions; thickness dependence of Pendellosung overshoot, other envelopes, absorption and detector resolution are not mapped (E67 Scope).
- X-ray crystal response time (~Lambda_P/c) is not modelled (E62).
- The Bessel-zero third-order effects (E45, E53, E54) were examined for alpha=1, S=j_{1,1} only.

### 8. Steady-state prior work as cited in the notebook (E7, E21, E29)

Status words: read = full text read by an earlier session; abstract = web abstract only.
- Polikarpov & Skadorov, phys. stat. sol. (b) 143, 11 (1987) and 149, 435 (1988): quasi-static multi-wave (Floquet) treatment with Bessel couplings J_{p'-p}(tau a); weak-deformation expansion xi = tau a / 2 << 1, six waves; satellite extinction length ~ 1/xi; uniform filled crystal, no front, no transient, Bessel zeros outside scope. Read in full (E29). This is the cited source of the steady-state ingredient. The committed poster does not cite it.
- Entin 1977/1979; Iolin & Entin 1983; Dzyublik 1983; Assur & Entin 1982: cited via P87 (E29); not read. Iolin & Entin: Borrmann suppression by a deformation superlattice, steady state, abstract (E21).
- Zolotoyabko, Shilo et al., Rev. Sci. Instrum. 73, 1643 (2002): stroboscopic diffraction from 0.58 GHz standing SAWs in LiNbO3, periodic steady state, abstract (E21).
- DeCamp, Reis, Bucksbaum et al., Nature 413, 825 (2001), and PRL 91, 165502 (2003): temporal Pendellosung of the main reflection from a single short strain pulse (Borrmann switch, Ge 202 Laue, 10 keV). The Nature paper itself was not read; the 2001 APS companion report was read in full (E21): no satellites, no periodic drive, no Bessel functions. E7 marks the entry "check before citing".
- Yoshimura & Hirano, J. Synchrotron Rad. 16, 601 (2009): Pendellosung fringe oscillation without acoustic drive, unrelated; abstract (E21).
- Liss et al. 1998 (phase of an established periodic acoustic field): not read (E26 addendum).
- Sondhauss & Wark, Acta Cryst. A59 (2003): time-dependent dynamical diffraction, read (E64); relation to the Entry 59 transfer function: E60, E61, E64.
- Poster 1f9f8f8 text "satellites of a fully strained crystal (Entin; Zolotoyabko et al.)" is consistent with E7 and E21 but summarises abstracts; E29 gives the better primary citation (Polikarpov & Skadorov).
- Novelty position (E7, E21, E29): not found in this literature search: transient formation behind a travelling front, collapse onto static thickness curves, Bessel-ordered formation, accumulated-coupling law for a ramp, period-ratio calibration of S. The search was web-only and not exhaustive. The J_n(S)-scaled steady-state extinction length and temporal Pendellosung are established and not claimed. Overshoot from the Bessel ladder is E15, not new in E67.

### Poster numbers that match

Poster now: L/Lambda_P = 0.5 (E67); 11,211 = 101 x 111; Lambda_ac/Lambda_P = 0.0125 = 0.5/40; B peaks at 1.69 times final (1.6936); tau_n = Lambda_P / (v_s abs(J_n)) (E6); t_tr = L/v_s; alpha_n = alpha abs(J_n(S)); sin^2 and tanh^2 laws (E1, E9).
Poster 1f9f8f8: tau_1 = 17-30 ns (E20: 16.7 and 30.3 ns); Si 440, 17-30 keV, 1-2 GHz (E20, E62); 0.1-0.2 % centre at the dark point (E23: 0.002 of 0.999); limits 0.34-0.57 as numbers (E54, see M4 for scope); kappa/(2 pi alpha) = 0.12 (E59); "factor 3-8" at 1 to 0.5 Darwin half-widths (E64); analytic tolerance 1e-9 (closed-form test, achieved 2.2e-10).
