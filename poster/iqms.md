---
title: Transit-Time Limit on Sideband Formation // in Acoustically Driven Bragg Diffraction
authors: **Isaac Yong**¹, Ouyoung Kwon¹, Hyunjung Kim¹
affiliation: ¹Center for Ultrafast Phase Transformation, Department of Physics, Sogang University, Seoul, Korea
session: 10-1533 · i-QMS 2026, Jeju, December 3, 2026
look: lab
body_pt: 28
caption_pt: 24
eq_pt: 30
footer: This work was supported by the National Research Foundation of Korea grant RS-2021-NR059920.
contact: Code, notebook and data: github.com/NaNIsaac-Research/TraTT (QR at right).
---

<!--
Printed text source for the i-QMS 2026 poster; build with python poster/build.py 150 poster/iqms.md.
Figures: python explore/make_poster_figs.py --iqms f4 f7 f8 f9 f10 f11 (figures/poster/iqms/).
Story and title follow the i-QMS abstract; notation, sign convention and layout are those of
poster/poster.md. v4 (declutter): a topic heading, one figure and at most three short lines per
panel; captions one line. Header, section heads, Conclusions and footer in the lab look of
the KPS print poster (look: lab). "Closed form" is the one name for the independent-channel model (sin^2,
tanh^2, Theta_n). Every number is recomputed by poster/check_numbers.py. "Si 440", "30 keV" and
"6 %" carry a no-break space (U+00A0).
-->

## Introduction

[[ 0.36 c

![Shear wave, $u\parallel h$: sideband $n$ at $\beta=nK$ (Laue), kinematic weight $J_n(S)^2$.](figures/poster/iqms/f8_satellites.png){E0}{E7}

|| 0.64 c

**Motivation.** GHz acoustic strain is used as a pump in ultrafast X-ray diffraction, and acoustically driven crystals switch X-rays (DeCamp et al. 2001) and may serve as fast switches and pulse shapers at storage-ring and XFEL sources. The sideband formation rate sets the time resolution and switching speed. Dynamical theory gives the steady-state sideband intensities (Entin 1977; Iolin & Entin 1983; Polikarpov & Skadorov 1987), not their formation in time. {E7}{E21}{E29}{E50}

> **This work.** Takagi–Taupin calculations on successive acoustic snapshots of sideband formation: the formation time $\tau_n$ of each sideband, completion within the transit time $L/v_s$, the thickness range of the Bessel law, and the transient overshoot for finite rise times. {E0}{E1}{E9}{E54}{E62}{E67}

]]

@pair

## Two-beam Takagi–Taupin model with acoustic modulation

$$ $\phi=h\cdot u=S\sin(Kz-\Omega t)$:  $e^{-i\phi}=\Sigma_n\,(-1)^nJ_n(S)\,e^{in(Kz-\Omega t)}$ {E0}

$$ $dD_0/dz=(i\pi/\Lambda_P)\,e^{+i\phi}D_h$,  $\pm\,dD_h/dz=(i\pi/\Lambda_P)\,e^{-i\phi}D_0+i\beta D_h$ {E0}

$\Lambda_P$: Pendellösung length (Laue, +), extinction length (Bragg, −) (Takagi 1962, 1969; Taupin 1964). {E0}{E20}

Sideband $n$ (momentum $nK$, energy $n\hbar\Omega$) is phase-matched at $\beta=+nK$ (Laue), $-nK$ (Bragg), with coupling $\propto\left|J_n(S)\right|$; kinematically $I_n\propto J_n(S)^2$. {E0}{E7}{E42}{E44}{E54}

![Si 440, 30 keV: Laue $\Lambda_P$ = 98.8 μm, $v_s$ = 5.85 km/s; Bragg $\Lambda_P$ = 21.8 μm, $v_s$ = 9.14 km/s.](figures/poster/iqms/f9_geometry.png){E0}{E20}{E85}

## Formation dynamics during acoustic onset

![Step onset: the layer $0<z<v_st$ is driven. Right: closed form, $n$ = 1, $S$ = 1.5, $L$ = 296 μm, Si.](figures/poster/iqms/f11_formation.png){E0}{E1}{E9}{E20}{E85}

Each sideband is a two-beam problem with Pendellösung length $\Lambda_P/\left|J_n\right|$; the driven thickness $L\to v_st$ in the closed form (panel 4) gives {E1}{E9}

$$ $I_n=\sin^2(\pi t/\tau_n)$ (Laue), $\ \tanh^2(\pi t/\tau_n)$ (Bragg), $\ \tau_n=\Lambda_P/(v_s\left|J_n(S)\right|)$ {E1}{E9}

In Laue, $I_n$ oscillates until the front reaches $z=L$ at $t_{tr}=L/v_s$; in Bragg, it saturates after about $\tau_n$. {E1}{E9}{E28}

Laue $\tau_1$ = 30 ns, $t_{tr}$ = 50.6 ns; Bragg $\tau_1$ = 4.3 ns, $t_{tr}$ = 32.4 ns. {E20}{E85}

@pair

## Steady-state sideband intensities vs thickness

$$ $I_n=\sin^2(\pi L\left|J_n\right|/\Lambda_P)$ (Laue), $\ \tanh^2(\pi L\left|J_n\right|/\Lambda_P)$ (Bragg) {E1}{E9}

For $L\ll\Lambda_P$ both reduce to the kinematic $J_n^2$ law; for $L\sim\Lambda_P$ they deviate: at $S$ = 1.5, Laue $I_2/I_1$ = 0.17 (kinematic), 0.46 at $L=\Lambda_P$. {E1}{E9}

![Filled crystal, $S$ = 1.5: full TT (points), closed form (solid), kinematic law (dashed).](figures/poster/iqms/f10_steady.png){E1}{E9}{E54}

## Finite rise time and transient overshoot

~ ramp | **Linear rise** over $T_{rise}$; the intensity settles at $t_{tr}+T_{rise}$. {E28}{E67}

$$ $I_n\approx\sin^2(\pi L\,\Theta_n/\Lambda_P),\qquad\Theta_n(t)=(1/L)\int_0^L J_n[S\,A(t-z/v_s)]\,dz$ {E5}{E28}

For $S$ beyond the $J_1$ maximum ($S$ = 1.84), $I_1$ passes a transient maximum above its steady value that grows with $T_{rise}$. {E5}{E15}{E67}

+ The rise is monotonic for any non-decreasing envelope when $S$ is below the first maximum of $\left|J_n\right|$ and $L\left|J_n\right|/\Lambda_P<1/2$. {E5}{E67}

![Transient excess $\Delta I=I_{max}-I_{steady}$, closed form, Laue, $n$ = 1, $L=\Lambda_P/2$.](figures/poster/iqms/f7_overshoot.png){E15}{E28}{E67}

## Validation and outlook

[[ 0.5 c

![Relative error of the closed form against full TT, filled Laue crystal.](figures/poster/iqms/f4_regime.png){E19}{E44}{E54}

|| 0.5 c

The closed form agrees with full TT within 6 % for $\Lambda_{ac}/\Lambda_P<0.3$. {E19}{E44}{E54}

- **Method:** RK4 on frozen snapshots ($L/c$ = 0.99 ps $\ll$ 500 ps period), checked against an exact Floquet solver. {E0}{E31}{E42}{E62}
- **Outlook:** $S$ = 1.5 corresponds to $u_0$ = 23 pm (strain $5\times10^{-5}$ at 2 GHz); formation times are 4–30 ns. The sideband centre requires a divergence below 0.16 μrad (Bragg) or 0.05 μrad (Laue). {E20}{E73}{E84}{E92}

]]

## Conclusions

[[ 0.59 c

The formation time scales as $1/\left|J_n(S)\right|$; intensity ratios deviate from $J_n^2$ as $L$ approaches $\Lambda_P$; for $S$ beyond the $J_1$ maximum a finite rise time gives a transient overshoot. {E1}{E9}{E54}{E67}

|| 0.41 c

> Sideband formation is complete within the acoustic transit time $L/v_s$ (ns in Si); the kinematic Bessel law holds for $L\ll\Lambda_P$. {E1}{E9}{E67}

]]

![Scope: two beams, symmetric geometry, no absorption, quasi-static diffraction. Not yet: experiment, back-face reflection, asymmetric cuts, realistic pulses, divergent or polychromatic beams.](none){E0}{E20}{E62}
