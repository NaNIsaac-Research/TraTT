# Findings

What this repository has shown so far, newest first. Each item links its evidence.

All results are calculations; no experiment has been compared. F numbers follow the study numbers in
[docs/research](research/README.md) and do not change.

## F8: Under a linear turn-on, the first satellite overshoots its steady value by up to 0.603 within the scan
- Question: Where does a linearly increasing amplitude give a first-satellite centre intensity above its filled steady value?
- Result: Over 11,211 (S, T) pairs from the Θ<sub>n</sub> law, the largest excess is 0.603 at S = 3.8 and T/t<sub>tr</sub> = 4, on the rise-time boundary of the scan; full TT at selected conditions agrees to 8.65×10⁻⁵.
- Figure: [overshoot.png](../figures/overshoot.png)
- Data and script: [e67_overshoot.npz](../explore/nb/e67_overshoot.npz), [e67_overshoot.json](../explore/nb/e67_overshoot.json), [e67_overshoot_map.py](../explore/nb/e67_overshoot_map.py), [make_overshoot_figure.py](../explore/make_overshoot_figure.py)
- Status: checked
- Limits: Selected checks, not a global error bound; one thickness, geometry, order and envelope; a centre observable, not an integrated population. The mechanism is the one of Entry 15. Checked: full TT at twelve conditions and three traced cases (Entry 67).
- Report: [8. Overshoot map under a linear turn-on](research/README.md#8-overshoot-map-under-a-linear-turn-on-entry-67) (2026-10-19)

## F6: The reflectivity spectrum is the strain spectrum times a closed-form crystal transfer function
- Question: When can the frequency content of a measured diffracted intensity be read as the frequency content of the acoustic wave?
- Result: The Fourier weight is the strain spectrum times a crystal transfer function, given in closed form and matching TT with no fit parameter (medians 0.984-1.021, Entry 59).
- Figure: [f5_outlook.png](../figures/poster/f5_outlook.png)
- Data and script: [e58_abs.json](../explore/nb/e58_abs.json), [e58_darwin.json](../explore/nb/e58_darwin.json), [e64_sw.json](../explore/nb/e64_sw.json), [e59_transfer.py](../explore/nb/e59_transfer.py), [make_poster_figs.py](../explore/make_poster_figs.py) (f5)
- Status: checked
- Limits: The closed form is the infinite-window limit: Entry 71 on [PR #16](https://github.com/NaNIsaac-Research/TraTT/pull/16) withdraws Entry 65 §2 and Entry 66 §3 for a 140 ps measurement. The first-order linearisation is prior art (Sondhauss & Wark 2003, Entry 64). Checked: closed form against full TT with no fit parameter (Entry 59).
- Report: [6. Transfer function from strain spectrum to reflectivity](research/README.md#6-transfer-function-from-strain-spectrum-to-reflectivity-entries-57-61-64-66) (2026-10-15)

## F7: An X-ray crossing is quasi-static, and no result transfers to surface waves as it stands
- Question: Is the quasi-static condition met, and do the results carry over to a surface acoustic wave?
- Result: In the poster's window an X-ray crossing takes 0.99 ps, 0.2 % of a 500 ps acoustic period (Entry 62). A surface wave cannot fill the extinction depth and keep its satellites resolved (Entry 63).
- Figure: none
- Data and script: Entry 62 is arithmetic; [e63_saw.py](../explore/nb/e63_saw.py)
- Status: draft
- Limits: Entry 62 is an estimate and Entry 63 a negative result for SAW geometry; no independent check is recorded.
- Report: [7. Quasi-static condition and surface waves](research/README.md#7-quasi-static-condition-and-surface-waves-entries-62-63) (2026-10-08)

## F5: Acoustic phase walls are known stacking-fault physics
- Question: Are the Entry 39 wall effects a known stacking-fault effect or a new capability?
- Result: For n = 1 and 2 the full TT integrals of Entry 39 follow the 1968 plane-wave stacking-fault formula of Authier & Simon within 1-3 %; the new-mechanism claim is withdrawn (Entry 56).
- Figure: none
- Data and script: Entry 39 numbers typed into [e55_fault_check.py](../explore/nb/e55_fault_check.py) (no TT solver)
- Status: checked
- Limits: The q-wall comparison needs part II of that paper, which was not read. Checked: against the independent 1968 formula (Entry 56).
- Report: [5. Acoustic phase walls](research/README.md#5-acoustic-phase-walls-entries-55-56) (2026-10-02)

## F4: An exact Floquet solver shows where independent satellites fail in a filled crystal
- Question: For a uniformly filled crystal, where does the picture of independent satellites break down as the acoustic wavelength approaches the Pendellösung length, and what replaces it?
- Result: An exact Floquet solver agrees with full TT to 1.6×10⁻⁶-1.3×10⁻⁵ (Entry 42); with the exact phase average, the 5 % population error is reached at R = 0.34-0.57 depending on S (Entry 54).
- Figure: [regime_phase_diagram.png](../figures/regime_phase_diagram.png)
- Data and script: [cache_e43_exact/](../explore/nb/cache_e43_exact), [make_phase_figure.py](../explore/make_phase_figure.py), [floquet.py](../src/tratt/floquet.py)
- Status: checked
- Limits: Filled crystal, steady state, non-absorbing; not the transient with a front inside the crystal (Entry 53). Nothing here may be called new before Entin and Iolin-Entin (1983) are read in full (Entry 50). Checked: Floquet solver against full TT (Entry 42); [tests/test_floquet.py](../tests/test_floquet.py).
- Report: [4. Floquet picture and the limit of independent satellites](research/README.md#4-floquet-picture-and-the-limit-of-independent-satellites-entries-42-54) (2026-10-02)

## F3: Chirps, phase walls and an automated search found nothing qualitatively new
- Question: Are there transient effects other than centre-intensity changes when the local acoustic wave vector changes?
- Result: A chirp raises the integrated satellite up to 5.3× with no focusing (Entry 38) and a π phase wall up to 2.58× (Entry 39); 250 automated cases found nothing that lowers the integrated satellite by more than 16 % (Entry 40).
- Figure: [search_summary.png](../figures/search_summary.png)
- Data and script: [e40_search.json](../explore/nb/e40_search.json), [make_search_figure.py](../explore/make_search_figure.py)
- Status: draft
- Limits: A negative result ("Nothing qualitatively new appeared tonight", Entry 41); no independent check is recorded. The wall effects of Entry 39 follow known stacking-fault theory (F5).
- Report: [3. Chirps, walls and the anomaly search](research/README.md#3-chirps-walls-and-the-anomaly-search-entries-38-41) (2026-10-01)

## F2: Satellite formation remembers the drive, and a satellite can exist only during the transient
- Question: Does formation depend on the path of the drive, and can a satellite exist only during the transient?
- Result: A satellite can reach 0.998 during the turn-on and 2×10⁻⁶ at the end (Entry 28), and the same amplitude reached up and down gives 0.010 and 0.494 (Entry 30); a > 30:1 transient-to-final contrast survives a 5 % error in S or 10 % acoustic loss (Entry 34).
- Figure: [poster_memory.png](../figures/poster_memory.png)
- Data and script: no saved data, the script recomputes; [make_memory_figure.py](../explore/make_memory_figure.py)
- Status: checked
- Limits: Not claimed as a new kind of peak (Entry 34); the Entry 35 statement holds for the satellite centre only (Entry 37); the steady-state extinction length is prior art (Polikarpov & Skadorov 1987, Entry 29). Checked: claims 21-29 verified (Entry 33); [tests/test_formation.py](../tests/test_formation.py).
- Report: [2. Path memory and the transient-only satellite](research/README.md#2-path-memory-and-the-transient-only-satellite-entries-28-37) (2026-10-01)

## F1: Each satellite forms like a filled-depth slab, in a time independent of the crystal thickness
- Question: While the sound fills the crystal, is satellite n a Laue (or Bragg) slab of the filled depth with coupling πα|J<sub>n</sub>(S)|, and what follows for its timing, order, width and observability?
- Result: The first maximum falls at t* = 1/(2α|J<sub>n</sub>(S)|) to within the time grid plus ~2 % (Entry 1), Bragg follows tanh² to ~1-3 % (Entry 9), and the characteristic time τ<sub>n</sub> = t<sub>tr</sub>/(α|J<sub>n</sub>(S)|) does not depend on the crystal thickness (Entry 6).
- Figure: [f1_collapse.png](../figures/poster/f1_collapse.png)
- Data and script: [poster_f1_points.npz](../explore/nb/poster_f1_points.npz), [make_poster_figs.py](../explore/make_poster_figs.py) (f1)
- Status: checked
- Limits: Two beams, symmetric, non-absorbing Laue with a step onset unless stated; centre intensities, not integrated orders; no acoustic nonlinearity or attenuation (Entry 15). Some claims are estimates (tables in Entries 12, 16, 27), and three early claims were withdrawn. Checked: against full TT with no fit parameter.
- Report: [1. Formation laws](research/README.md#1-formation-laws-entries-0-27) (2026-10-01)
