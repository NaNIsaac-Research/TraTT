---
title: Transient Formation Dynamics of Acoustic Bragg Satellites // in Dynamical X-ray Diffraction
authors: **Isaac Yong**¹, Ouyoung Kwon¹, Hyunjung Kim¹*
affiliation: ¹Center for Ultrafast Phase Transformation, Department of Physics, Sogang University, Seoul, Korea  ·  *corresponding author
footer: P2.17 · 2026 KPS Fall Meeting, Jeju, October 22, 2026 · This work was supported by the National Research Foundation of Korea grant RS-2021-NR059920.
---

<!--
Poster manuscript. This file is the only source of printed text; poster/build.py reads it and
never edits it. Every item carries {E..} tags pointing at notes/lab_notebook.md (checked).
Syntax: see the docstring of poster/build.py. Poster figures: python explore/make_poster_figs.py

Three observations, in this order, and everything else is evidence for them:
  1 each satellite has its own growth time;
  2 with a ramped drive, the satellites follow the drive history;
  3 the single-satellite picture holds up to R ~ 0.3.
These are simulation results; the text says what we saw, not more.
-->

@wide

## Introduction

A sound wave in a crystal produces extra peaks (satellites $n = \pm1, \pm2, \dots$) in the X-ray rocking curve $I(\eta)$. For a fully strained crystal they are known. We calculate them during the transit time $t_{tr} = L/v_s$, when the acoustic front is still inside the crystal ($L$: thickness, $v_s$: sound velocity). {E0}

Previous work: time-domain Pendellösung of the main peak (DeCamp et al., Nature 413, 825 (2001)); satellites of a fully strained crystal (Entin; Zolotoyabko et al.). {E7}

- Method: two-beam Takagi–Taupin (TT) equations, Laue and Bragg geometry, solved for the strain profile at each time $t$. The X-ray passes the crystal in less than 1.2 % of one acoustic period. {E0}{E62}
- Parameters: $\alpha = L/\Lambda_P$ ($\Lambda_P$: Pendellösung length), acoustic amplitude $S = h u_0$, $R = \Lambda_{ac}/\Lambda_P$. Code tested against analytic solutions ($10^{-9}$) and an exact Floquet solver ($3\times10^{-7}$). {E0}{E42}

![Calculation at $\tilde t = t/t_{tr}$ = 0.62. Left: strain inside the crystal. Right: calculated $I(\eta)$ at the same time ($\alpha$ = 0.6, $S$ = 1.5, $\alpha_{ac}$ = 5).](figures/poster/f0_scheme.png){E0}

> **Main result.** Satellite $n$ at time $t$ has the intensity of a uniform crystal of thickness $v_s t$ and coupling $\alpha\left|J_n(S)\right|$ ($J_n$: Bessel function), so its formation time is $\tau_n = \Lambda_P/(v_s\left|J_n(S)\right|)$. {E1}{E9}{E33}

## Formation time of each satellite

- Satellite intensity: $I_n = \sin^2(\pi\alpha_n \tilde t)$ (Laue) and $\tanh^2(\pi\alpha_n \tilde t)$ (Bragg), with $\alpha_n = \alpha\left|J_n(S)\right|$. {E1}{E9}

![Points: full TT calculation for four $(S, \alpha, n)$. Lines: the formulas above, **no fitting parameter**. $\tau_n$ does not depend on $L$. The satellite with the largest $\left|J_n(S)\right|$ forms first; at $S=3$ the order is $n=2$, 1, 3.](figures/poster/f1_collapse.png){E1}{E9}{E24}

## Satellite line shape at the intensity minimum

- At $\alpha_n \tilde t = 1$ the intensity at the satellite centre is **0.1–0.2 %** of its maximum. However, **≈52 %** of the integrated intensity remains in two side peaks, which move toward the centre with time. {E23}

![Satellite $n=1$, $S=1.5$, $\alpha=3$. Left: $I(\eta, \tilde t)$; the line becomes narrower with time. Right: intensity at the satellite centre.](figures/poster/f2_fringes.png){E22}{E23}

## Validity of the independent-satellite approximation

- The formulas above treat each satellite independently. Error < 5 % for $R \lesssim 0.3$; limit $R$ = **0.34–0.57**, depending on $S$. {E53}{E54}
- For larger $R$ the satellites are coupled through the forward beam. By this third-order coupling, $\pi\alpha (R/2)^2 C_n(S)$, a satellite with $J_n(S)=0$ has a small nonzero intensity. {E44}{E45}{E50}{E52}

![Error of the independent-satellite approximation. Each point: one $(\alpha, \alpha_{ac}, S)$.](figures/poster/f4_regime.png){E54}

@column

## Time-dependent acoustic amplitude

- If the amplitude $A(t)$ changes in time, satellite $n$ depends on the amplitude during the last $t_{tr}$: $\Theta_n = \int J_n(S\,A(t-\zeta))\,d\zeta$. {E28}{E30}
- If $J_1(S_f)=0$ at the final amplitude, $n=1$ is absent in the steady state but is the **strongest** satellite for some time (left). Increasing or decreasing $A$ to the same final value gives different intensities (right). {E28}{E30}{E34}

![Laue, $\alpha=0.5$. Points: full TT. Lines: formula with $\Theta_n$.](figures/poster/f3_memory.png){E28}{E30}

## Outlook: measurement of the phonon spectrum

- For small strain, the Fourier component of $R(t)$ is the strain spectrum times a transfer function $H(\omega)$, obtained analytically to first order in $S$ (agreement with full TT: 2–5 %). {E59}
- Valid inside the Darwin width, where the perturbation theory of Sondhauss & Wark (2003) differs from full TT by a factor 3–8. Comparison with previous work is not complete. {E61}{E64}

![(a) Fourier weight / kinematic value ($\kappa/2\pi\alpha$ = 0.12): three acoustic pulses give one curve. (b) First-order theory / full TT.](figures/poster/f5_outlook.png){E59}{E64}

## Conclusion

%% $\tau_n \propto 1/\left\vert J_n\right\vert$ | formation time is different for each satellite {E1}{E9}
%% $\Theta_n$ | intensity depends on the amplitude during the last $t_{tr}$ {E28}{E30}
%% $R \lesssim 0.3$ | independent-satellite approximation within 5 % {E54}

- Calculation only. Proposed experiment: Si 440, 17–30 keV, 1–2 GHz, $\tau_1$ = 17–30 ns. {E20}
