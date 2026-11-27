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
Figures: python explore/make_poster_figs.py --iqms f1 f4 f7 f8 f9 f10 (figures/poster/iqms/).
Story and title follow the i-QMS abstract; notation, sign convention and layout are those of
poster/poster.md. v4 (declutter): a claim heading, one figure and at most three short lines per
panel; captions one line. Header, section heads, Conclusions and footer in the lab look of
the KPS print poster (look: lab). "Closed form" is the one name for the independent-channel model (sin^2,
tanh^2, Theta_n). Every number is recomputed by poster/check_numbers.py. "Si 440", "30 keV" and
"6 %" carry a no-break space (U+00A0).
-->

@pair

## A sound wave splits the reflection into sidebands

How fast does diffraction follow sound? It sets the speed of acoustic X-ray gates. {E7}{E21}

![Shear wave, $u\parallel h$: sideband $n$ at $\beta=nK$ (Laue), kinematic weight $J_n(S)^2$.](figures/poster/iqms/f8_satellites.png){E0}{E7}

$$ $\phi=S\sin(Kz-\Omega t)$:  $e^{-i\phi}=\Sigma_n\,(-1)^nJ_n(S)\,e^{in(Kz-\Omega t)}$ {E0}

With $S=hu_0$, sideband $n$ carries momentum $nK$ and energy $n\hbar\Omega$; an instant response gives the Bessel law $I_n\propto J_n(S)^2$. {E0}{E7}{E42}

## Each sideband is a two-beam problem of its own

$$ $dD_0/dz=(i\pi/\Lambda_P)\,e^{+i\phi}D_h$ {E0}

$$ $\pm\,dD_h/dz=(i\pi/\Lambda_P)\,e^{-i\phi}D_0+i\beta D_h$  (+ Laue, − Bragg) {E0}

$\Lambda_P$: Pendellösung length (Laue), extinction length (Bragg). {E0}{E20}

Sideband $n$ is matched at $\beta=+nK$ (Laue), $-nK$ (Bragg), with coupling $\propto\left|J_n(S)\right|$. {E0}{E44}{E54}

![Si 440, 30 keV: Laue $\Lambda_P$ = 98.8 μm, $v_s$ = 5.85 km/s; Bragg $\Lambda_P$ = 21.8 μm, $v_s$ = 9.14 km/s.](figures/poster/iqms/f9_geometry.png){E0}{E20}{E85}

@pair

## Sidebands form within the transit time

~ step | **Step onset:** only $0<z<v_st$ is driven, until $t_{tr}=L/v_s$. {E0}

$$ $I_n=\sin^2(\pi t/\tau_n)$ (Laue), $\ \tanh^2(\pi t/\tau_n)$ (Bragg), $\ \tau_n=\Lambda_P/(v_s\left|J_n(S)\right|)$ {E1}{E9}

**Laue** settles at $t_{tr}$; **Bragg** at about $\tau_n$, before $t_{tr}$ in a thick crystal. {E1}{E9}{E28}

$L$ = 296 μm, $S$ = 1.5: Laue $\tau_1$ = 30 ns, $t_{tr}$ = 50.6 ns; Bragg $\tau_1$ = 4.3 ns, $t_{tr}$ = 32.4 ns. {E20}{E85}

![Full TT, four cases (points), against the closed form (line), no fitted parameters.](figures/poster/iqms/f1_collapse.png){E1}{E9}{E19}{E26}

## Thick crystals break the Bessel law

$$ $I_n=\sin^2(\pi L\left|J_n\right|/\Lambda_P)$ (Laue), $\ \tanh^2(\pi L\left|J_n\right|/\Lambda_P)$ (Bragg) {E1}{E9}

Only for $L\ll\Lambda_P$: at $S$ = 1.5, Laue $I_2/I_1$ is 0.17 kinematically, 0.46 at $L=\Lambda_P$. {E1}{E9}

![Filled crystal, $S$ = 1.5: full TT (points), closed form (solid), kinematic law (dashed).](figures/poster/iqms/f10_steady.png){E1}{E9}{E54}

@pair

## A slow drive ramp overshoots

~ ramp | **Linear rise** over $T_{rise}$; settled at $t_{tr}+T_{rise}$. {E28}{E67}

$$ $I_n\approx\sin^2(\pi L\,\Theta_n/\Lambda_P),\qquad\Theta_n(t)=(1/L)\int_0^L J_n[S\,A(t-z/v_s)]\,dz$ {E5}{E28}

Beyond the $J_1$ maximum ($S$ = 1.84), $I_1$ overshoots, more for a slower rise. {E5}{E15}{E67}

+ Monotonic rise for any non-decreasing envelope if $S$ is below the first maximum of $\left|J_n\right|$ and $L\left|J_n\right|/\Lambda_P<1/2$. {E5}{E67}

![Overshoot $\Delta I=I_{max}-I_{steady}$ from the closed form, Laue, $n$ = 1, $L=\Lambda_P/2$.](figures/poster/iqms/f7_overshoot.png){E15}{E28}{E67}

## Checked against full Takagi–Taupin

![Error of the closed form against full TT, filled Laue crystal.](figures/poster/iqms/f4_regime.png){E19}{E44}{E54}

The closed form holds below $\Lambda_{ac}/\Lambda_P\approx0.3$ (error under 6 %). {E19}{E44}{E54}

- **Known:** steady acoustic satellites (Entin 1977; Iolin & Entin 1983; Polikarpov & Skadorov 1987); acoustic switching (DeCamp et al. 2001); TT (Takagi 1962, 1969; Taupin 1964). {E7}{E21}{E29}{E50}
- **Method:** RK4 on frozen snapshots ($L/c$ = 0.99 ps $\ll$ 500 ps period), Floquet check. {E0}{E31}{E42}{E62}
- **Outlook:** $S$ = 1.5 is $u_0$ = 23 pm, strain $5\times10^{-5}$ at 2 GHz; formation takes 4–30 ns. The sideband centre needs a divergence below 0.16 μrad (Bragg), 0.05 μrad (Laue). {E20}{E73}{E84}{E92}

## Conclusions

[[ 0.59 c

Full Takagi–Taupin calculations of an acoustically driven crystal give one formation clock per sideband, $\tau_n=\Lambda_P/(v_s\left|J_n(S)\right|)$, a transit-time limit on settling, steady ratios away from the Bessel law, and an overshoot for slow ramps past the $J_1$ maximum. {E0}{E1}{E9}{E54}{E67}

|| 0.41 c

> Sidebands form within the transit time $L/v_s$, nanoseconds in Si; the Bessel law needs $L\ll\Lambda_P$. {E1}{E9}{E67}

]]

![Scope: two beams, symmetric geometry, no absorption, quasi-static diffraction. Not yet: experiment, back-face reflection, asymmetric cuts, realistic pulses, divergent or polychromatic beams.](none){E0}{E20}{E62}
