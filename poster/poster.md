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

## Introduction: acoustic satellites while the sound is still entering the crystal

In a thick perfect crystal the X-ray beams exchange intensity over the Pendellösung length $\Lambda_P$. A GHz sound wave adds satellites $n$ with weight $J_n(S)$ to the rocking curve $I(\eta)$. We simulate how they **grow** during the transit $t_{tr} = L/v_s$, before the sound fills the crystal. {E0}

Known: Pendellösung in time of the main peak (DeCamp et al., Nature 413, 825 (2001)); steady-state satellites (Entin; Zolotoyabko et al.). {E7}

- Two-beam Takagi–Taupin equations, Laue and Bragg; $\alpha = L/\Lambda_P$, $S = h\cdot u_0$, $R = \Lambda_{ac}/\Lambda_P$. Lattice frozen per instant: $\beta \leq 1.2\times10^{-2}$. {E0}{E62}
- Solver checked against analytic limits ($10^{-9}$) and an independent exact Floquet solver ($3\times10^{-7}$). {E0}{E42}

![Snapshot at $\tilde t$ = 0.62: the profile inside the slab is the drive, the curve on the right the solved $I(\eta)$ of that same instant ($\alpha$ = 0.6, $S$ = 1.5, $\alpha_{ac}$ = 5).](figures/poster/f0_scheme.png){E0}

> **Main observation.** Each satellite grows like a crystal of depth $v_s t$ with its coupling reduced by $\left|J_n(S)\right|$, so it has its own growth time $\tau_n = \Lambda_P/(v_s\left|J_n(S)\right|)$. {E1}{E9}{E33}

## Satellite growth follows a thin-crystal formula

- Satellite $n$ behaves like an unmodulated crystal of depth $v_s t$ with coupling $\alpha_n = \alpha\left|J_n(S)\right|$: $I_n \propto \sin^2(\pi\alpha_n \tilde t)$ in Laue, $\tanh^2(\pi\alpha_n \tilde t)$ in Bragg. {E1}{E9}

![Points: full Takagi–Taupin for four $(S, \alpha, n)$; lines: the formulas above, **no fitted parameter**. The Laue period $\Lambda_P/(v_s\left|J_n(S)\right|)$ does not depend on $L$. The order in which satellites form follows $\left|J_n(S)\right|$, so it changes with $S$ — at $S=3$: $n=2$, then 1, then 3.](figures/poster/f1_collapse.png){E1}{E9}{E24}

## The satellite centre goes dark, its intensity does not

- At $\alpha_n \tilde t = 1$ the centre drops to **0.1–0.2 %** of its maximum, but **≈52 %** of the integrated satellite intensity remains, in two side lobes that move toward the centre. {E23}

![Satellite $n=1$, $S=1.5$, $\alpha=3$: the line gets narrower and its centre oscillates as the front fills the crystal.](figures/poster/f2_fringes.png){E22}{E23}

## When can each satellite be treated separately?

- The single-satellite formulas stay within 5 % for $R \lesssim 0.3$; the computed limit is $R$ = **0.34–0.57**, depending on $S$. {E53}{E54}
- For larger $R$ the satellites couple through side components of the forward beam. The same third-order path, $\pi\alpha (R/2)^2 C_n(S)$, makes an order with $J_n(S)=0$ weakly visible again. {E44}{E45}{E50}{E52}

![Population error of the single-satellite picture. Each point is one $(\alpha, \alpha_{ac}, S)$, averaged exactly over the acoustic phase.](figures/poster/f4_regime.png){E54}

@column

## Ramped amplitude: satellites follow its history

- If the amplitude $A$ rises gradually, each depth holds sound emitted at a different time. Satellite $n$ then follows the amplitude over the last $t_{tr}$, $\Theta_n = \int J_n(S\,A(t-\zeta))\,d\zeta$, not the present one. An order with $J_1(S_f)=0$ at the final amplitude, absent in the steady state, is the **brightest** line for a while. Ramping the same final strain up or down gives different curves (right). {E28}{E30}{E34}

![Laue, $\alpha=0.5$: points full TT, lines the $\Theta_n$ formula.](figures/poster/f3_memory.png){E28}{E30}

## Outlook: phonon spectrum from Bragg oscillations

- For weak strain, the Fourier components of the reflectivity $R(t)$ are the strain spectrum times a crystal response $H(\omega)$, closed form at first order in $S$; full TT agrees to 2–5 %. {E59}
- It also holds inside the Darwin width, where the plane-wave perturbation of Sondhauss & Wark (2003) differs from full TT by ×3–8 (Si 400 at 17 keV: **×2** at 20 GHz). Prior art still being checked. {E61}{E64}{E65}

![(a) Fourier weight over the kinematic value vs phonon frequency, $\kappa/2\pi\alpha$ = 0.12: three acoustic packets fall on one curve, so dividing by it recovers the spectrum. (b) Satellite weight of the first-order formulas over full TT, single mode.](figures/poster/f5_outlook.png){E59}{E64}

## Summary

%% $\tau_n \propto 1/\left\vert J_n\right\vert$ | each satellite has its own growth time {E1}{E9}
%% $\Theta_n$ | ramped drive: satellites follow the last $t_{tr}$ of the amplitude {E28}{E30}
%% $R \lesssim 0.3$ | single-satellite formulas within 5 % {E54}

- Simulation only so far. Si 440, 17–30 keV, 1–2 GHz: $\tau_1$ = 17–30 ns. {E20}
