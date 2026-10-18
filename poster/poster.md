---
title: Transient Formation Dynamics of Acoustic Bragg Satellites // in Dynamical X-ray Diffraction
authors: **Isaac Yong**¹, Ouyoung Kwon¹, Hyunjung Kim¹
affiliation: ¹Center for Ultrafast Phase Transformation, Department of Physics, Sogang University, Seoul, Korea
session: P2.17 · 2026 KPS Fall Meeting, Jeju, October 22, 2026
footer: This work was supported by the National Research Foundation of Korea grant RS-2021-NR059920.
---

<!--
Printed text source; build with python poster/build.py.
Reading order: full-width background and question; left column theory, method and
result 1; right column result 2, solver checks and conclusion. Numbers follow notes/tasks/poster_facts.md.
-->

@wide

## Background: acoustic satellites and the question

**Acoustic satellites.** Sound displaces the lattice planes by $u$ and shifts the diffracted X-ray phase by $\phi=h u$. This moving phase grating adds satellites $n=\pm1,\pm2,\dots$ to the rocking curve $I(\eta)$ at $\eta=nq$, $q=2\pi L/\Lambda_{ac}$ ($\eta$: angle deviation, $L$: thickness, $\Lambda_{ac}$: acoustic wavelength). {E0}

**Steady state (known).** With sound in the whole crystal, $e^{i\phi}=\Sigma_n J_n(S)\,e^{in(q\zeta-q\tilde t)}$, $S=h u_0$. Satellite $n$ couples with strength $\alpha\left|J_n(S)\right|$, $\alpha=L/\Lambda_P$ ($\Lambda_P$: Pendellösung length). $J_n$ is a coupling weight; multiple scattering sets the intensity. Multi-wave theory: Polikarpov & Skadorov, phys. stat. sol. (b) 143, 11 (1987). {E0}{E7}{E29}

**Before the steady state.** The front moves at $v_s$. For $t<t_{tr}=L/v_s$ only the depth $v_s t$ vibrates. {E0}{E7}

> **Question.** How do the satellites form while the front crosses the crystal, and how does a gradual turn-on change their intensity in time? {E0}{E28}{E33}

![](figures/poster/f0_scheme.png){E0}

![](figures/poster/f6_background.png){E0}{E7}

## Theory and numerical method

**1. Two-beam Takagi–Taupin (TT) equations.** Amplitudes $D_0$, $D_h$ vs depth $\zeta=z/L\in[0,1]$; $\eta$ in units of $1/L$: {E0}

$$ $dD_0/d\zeta = i\pi\alpha\,e^{+i\phi}D_h,\qquad dD_h/d\zeta = i\pi\alpha\,e^{-i\phi}D_0 + i\eta D_h$ {E0}

**2. Travelling sound as a phase field,** $\tilde t=t/t_{tr}$: {E0}

$$ $\phi(\zeta,\tilde t)=S\,A(\tilde t-\zeta)\,\sin(q\zeta-q\tilde t)$ {E0}

Causal envelope: $A=0$ for $\zeta>\tilde t$, so only the layer behind the front is modulated. Step $A$: sudden turn-on; linear ramp over $T_{rise}$: gradual. {E0}{E28}

**3. Laue: initial-value problem.** $D_0(0)=1$, $D_h(0)=0$; integrate to $\zeta=1$, $I=\left|D_h(1)\right|^2$. {E0}

**4. Bragg: Riccati form.** $D_h$ exits through the entrance face, so $D_0(0)=1$, $D_h(1)=0$ sit on opposite faces. For $R=D_h/D_0$: {E0}

$$ $dR/d\zeta=-i\pi\alpha\,e^{-i\phi}-i\eta R-i\pi\alpha\,e^{+i\phi}R^2,\qquad R(1)=0$ {E0}

Integrated backward from $\zeta=1$ (stable): no shooting; $I=\left|R(0)\right|^2$. {E0}

**5. RK4 in depth.** Fixed step, $\geq 20$ per fastest oscillation; all $\eta$ in one sweep. {E0}{E31}

**6. Quasi-static time.** X-ray transit $L/c\approx1$ ps is 0.2 % of a 500 ps acoustic period (worst case: Si 440, 30 keV, 2 GHz, $L=296$ μm), so each time step is a frozen snapshot: {E62}

> $\tilde t\ \rightarrow\ \phi(\zeta,\tilde t)\ \rightarrow\ $ RK4 in $\zeta$ $\rightarrow\ I(\eta,\tilde t)\ \rightarrow$ next $\tilde t$ {E0}{E62}

## Result 1: satellite formation (sudden turn-on)

Centre intensity of satellite $n$ while the front crosses. The filled layer acts as a uniform crystal of thickness $\tilde t$ and coupling $\alpha_n=\alpha\left|J_n(S)\right|$: {E1}{E9}

$$ $I_n=\sin^2(\pi\alpha_n\tilde t)$ (Laue), $\qquad I_n=\tanh^2(\pi\alpha_n\tilde t)$ (Bragg) {E1}{E9}

Time scale $\tau_n=\Lambda_P/(v_s\left|J_n(S)\right|)$, independent of $L$. The order follows $\left|J_n\right|$, not $n$: at $S=3$ the first maxima come as $n=2,1,3$. {E1}{E6}

![Points: full TT for four $(S,\alpha,n)$. Lines: the formulas, **no fitted parameter**. Over the notebook test cases ($\alpha_{ac}=20$) the deviation is at most 0.079 (Laue) and 0.043 (Bragg).](figures/poster/f1_collapse.png){E1}{E9}

**Validity** (approximation, not solver error): satellites are treated as independent; centre-intensity error $\approx0.9\,\Lambda_{ac}/\Lambda_P$ at $S=1.5$, $\leq0.03$ for $\Lambda_{ac}/\Lambda_P\leq0.05$ (30 random cases). {E19}{E26}

@column

## Result 2: transient overshoot (gradual turn-on)

During a ramp, each depth holds a different amplitude, and the satellite sums their couplings: {E5}{E28}

$$ $\Theta_n(\tilde t)=\int_0^1 J_n(S\,A(\tilde t-\zeta))\,d\zeta,\qquad I_n\approx\sin^2(\pi\alpha\,\Theta_n)$ (Laue) {E5}{E28}

**Overshoot**: $\Delta I=I_{max}-I_{steady}>0$ (incident-intensity units). Scan of $S$ and $T_{rise}$; first Laue satellite, $L/\Lambda_P=0.5$. {E67}

![Top: $\Delta I$ from the $\Theta_n$ law, 11,211 conditions, $\Lambda_{ac}/\Lambda_P=0.0125$. Bottom: A–C traces; lines, law; dots, full TT; dashed, steady value. Phase-averaged centre intensity.](figures/poster/f7_overshoot.png){E67}

- A ($S=1.5$): monotonic. B ($S=3$): the ramp passes larger $\left|J_1\right|$, so the peak is 1.69 × the final value. C (near $J_1=0$): 0.53 during turn-on, $1.3\times10^{-4}$ at the end. {E15}{E28}{E67}
- Largest $\Delta I$: 0.603 at the scan edge $T_{rise}=4t_{tr}$ (bound 0.627). Full TT at five points agrees with the law to $8\times10^{-5}$. {E28}{E67}

## Numerical checks of the TT solver

%% $<10^{-9}$ | vs closed form, no sound {E0}
%% 4th order | RK4 convergence in depth step {E0}
%% $\sim10^{-5}$ | vs Floquet solver, filled crystal {E42}

- Also lossless, $\left|D_0\right|^2+\left|D_h\right|^2=1$; satellites at $\eta=nq$; doubling the depth steps changes the overshoot traces by $\leq 3.4\times10^{-5}$. Solver accuracy only; the limits of the simple laws are in panel 3. {E0}{E42}{E67}

## Conclusion

- We calculated satellite formation behind a travelling acoustic front with TT equations, Laue and Bragg. Each satellite forms on its own time scale, $\tau_n\propto1/\left|J_n(S)\right|$. {E0}{E1}{E9}
- A gradual turn-on can give non-monotonic growth and overshoot; the steady-state intensity alone does not describe the transient. {E28}{E67}
- Calculation only, not compared with experiment. Two-beam, symmetric, non-absorbing, quasi-static; the simple laws need small $\Lambda_{ac}/\Lambda_P$. Proposed, untested: Si 440, 17–30 keV, 1–2 GHz, $\tau_1\approx17$–30 ns. {E0}{E20}{E54}{E62}
