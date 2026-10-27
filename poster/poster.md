---
title: Transient Formation Dynamics of Acoustic Bragg Satellites // in Dynamical X-ray Diffraction
authors: **Isaac Yong**¹, Ouyoung Kwon¹, Hyunjung Kim¹
affiliation: ¹Center for Ultrafast Phase Transformation, Department of Physics, Sogang University, Seoul, Korea
session: P2.17 · 2026 KPS Fall Meeting, Jeju, October 22, 2026
footer: This work was supported by the National Research Foundation of Korea grant RS-2021-NR059920.
---

<!--
Printed text source; build with python poster/build.py. Text as in commit 40676f4; this version
only changes the arrangement. Bands: introduction, method, the two results side by side,
conclusions. Numbers follow notes/tasks/poster_facts.md.
-->

## Introduction

[[ 0.41 c

![Right: rocking curve now; detuning $\beta$ in units of $K$, peaks at orders $n$.](figures/poster/f0_scheme.png){E0}

|| 0.59

**Motivation.** Time-resolved X-ray diffraction can follow GHz acoustic waves in crystals: satellites form over a few ns, much longer than 50–100 ps synchrotron pulses, and a strain pulse entering a Laue crystal has been used to switch X-rays (DeCamp et al., Nature 413, 825 (2001)). {E6}{E7}{E21}

**Acoustic satellites.** A displacement $u$ shifts the phase of the diffracted wave by $\phi=hu$, so a travelling acoustic wave ($K=2\pi/\Lambda_{ac}$, $\Lambda_{ac}$: wavelength, $\Omega=Kv_s$) acts as a moving phase grating with satellites $n=\pm1,\pm2,\dots$ at detuning $\beta_n=nK$ ($\beta$: detuning from the Bragg condition). In a filled crystal $e^{-i\phi}=\Sigma_n(-1)^nJ_n(S)\,e^{in(Kz-\Omega t)}$ with $S=hu_0$; $(-1)^n$ flips odd-order signs, not intensities. Satellite $n$ couples with strength $\alpha\left|J_n(S)\right|$, $\alpha=L/\Lambda_P$ ($L$: thickness, $\Lambda_P$: Pendellösung length); its intensity follows from multiple scattering (Polikarpov & Skadorov, phys. stat. sol. (b) 143, 11 (1987)). {E0}{E7}{E29}

]]

[[ 0.41 c

![](figures/poster/f6_background.png){E0}{E7}

|| 0.59 c

> **This work.** The Bessel-weighted coupling describes a crystal already filled with sound. While the wavefront enters ($t<t_{tr}=L/v_s$), the vibrating depth $v_st$ grows and the diffraction is dynamical, so we compute time-resolved rocking curves directly from the TT equations. {E0}{E7}{E28}{E33}

]]

## Theoretical Model and Numerical Methods

[[ 0.5

**1 Two-beam diffraction.** The X-ray field near a Bragg reflection consists of the transmitted wave $D_0$ and the diffracted wave $D_h$, which exchange intensity with depth $\zeta=z/L\in[0,1]$. In Laue geometry they obey the coupled Takagi–Taupin (TT) equations: {E0}

$$ $dD_0/d\zeta = i\pi\alpha\,e^{+i\phi}D_h,\qquad dD_h/d\zeta = i\pi\alpha\,e^{-i\phi}D_0 + i\eta D_h$ {E0}

$\pi\alpha$ couples the beams, $i\eta D_h$ is the detuning ($\eta=\beta L$: detuning times thickness $L$, dimensionless; satellite $n$ at $\eta_n=nKL$), and the lattice displacement enters only as the phase $e^{\pm i\phi}$ of the coupling. {E0}

**2 Travelling acoustic deformation,** $\phi(z,t)=S\,A(t-z/v_s)\,\sin(Kz-\Omega t)$; in the solver's scaled variables $\zeta=z/L$, $\tilde t=t/t_{tr}$, $KL$ and $w=\Omega t_{tr}$ ($=KL$, since $\Omega=Kv_s$): {E0}

$$ $\phi(\zeta,\tilde t)=S\,A(\tilde t-\zeta)\,\sin(KL\,\zeta-w\tilde t)$ {E0}

Causal envelope: $A=0$ ahead of the front ($\zeta>\tilde t$); its profile sets the onset. {E0}{E28}

|| 0.5

**3 Numerical solution.** The X-ray transit $L/c\approx1$ ps is 0.2 % of a 500 ps acoustic period (Si 440, 30 keV, 2 GHz, $L=296$ μm), so $\phi$ is held fixed at each $\tilde t$ (quasi-static). {E62}

- Laue: $D_0(0)=1$, $D_h(0)=0$ at the entrance; integrate forward to $\zeta=1$. {E0}
- Bragg: $D_h$ exits at the entrance, so $D_0(0)=1$, $D_h(1)=0$ sit on opposite faces; $R=D_h/D_0$ obeys a Riccati equation, integrated backward (stable): {E0}

$$ $dR/d\zeta=-i\pi\alpha\,e^{-i\phi}-i\eta R-i\pi\alpha\,e^{+i\phi}R^2,\qquad R(1)=0$ {E0}

- Both: fixed-step RK4 in depth, $\geq20$ steps per fastest oscillation. {E0}{E31}

**4 Calculated quantities.** $I(\eta,\tilde t)=\left|D_h(1)\right|^2$ (Laue) or $\left|R(0)\right|^2$ (Bragg), for every $\eta$ and $\tilde t$. {E0}

**Numerical verification.** The solver was checked against analytical solutions, step-size convergence and an independent Floquet calculation. {E0}{E42}

]]

=> time $\tilde t$ // acoustic snapshot | fix $\phi(\zeta,\tilde t)$ // quasi-static | RK4 in $\zeta$ // Laue forward, Bragg backward, all $\eta$ | $I(\eta,\tilde t)$ // time-resolved rocking curve | $I_n(\tilde t)=I(\eta_n,\tilde t)$ // satellite $n$ {E0}{E62}

@pair

## Satellite Formation Dynamics

~ step | **Sudden acoustic onset:** $A(s)=H(s)$, $s=\tilde t-\zeta$ {E0}

With the satellites treated as independent, the strained layer acts as a uniform crystal of thickness $\tilde t$ and coupling $\alpha_n=\alpha\left|J_n(S)\right|$: {E1}{E9}

$$ $I_n=\sin^2(\pi\alpha_n\tilde t)$ (Laue), $\qquad I_n=\tanh^2(\pi\alpha_n\tilde t)$ (Bragg) {E1}{E9}

The characteristic time $\tau_n=\Lambda_P/(v_s\left|J_n(S)\right|)$ (Laue: one period, first maximum at $\tau_n/2$; Bragg: 99 % at $0.95\,\tau_n$) is independent of $L$, and the order follows $\left|J_n(S)\right|$ rather than $n$ (at $S=3$: $n=2,1,3$). {E1}{E6}

![Deviations of the TT markers from the lines reflect the approximation, not numerical solver error.](figures/poster/f1_collapse.png){E1}{E9}{E19}{E26}

## Transient Intensity Overshoot

~ ramp | **Gradual acoustic onset:** $A(s)=\min(s/T_{rise},\,1)$ for $s\geq0$ {E28}{E67}

The depth-dependent amplitude gives satellite $n$ a depth-averaged coupling: {E5}{E28}

$$ $\Theta_n(\tilde t)=\int_0^1 J_n(S\,A(\tilde t-\zeta))\,d\zeta,\qquad I_n\approx\sin^2(\pi\alpha\,\Theta_n)$ (Laue) {E5}{E28}

Overshoot: $\Delta I=I_{max}-I_{steady}$ in incident-intensity units, for the first Laue satellite at $L/\Lambda_P=0.5$, $0.5\leq S\leq6$, $0.05\leq T_{rise}/t_{tr}\leq4$. {E67}

![Top: $\Delta I$ from the reduced coupling model $\Theta_n$ over 11,211 parameter sets (maximum 0.603). Bottom: cases A–C, reduced model (lines) checked against full TT (dots); dashed: steady state. Overshoot can remain strong when the final Bessel coupling is small.](figures/poster/f7_overshoot.png){E15}{E28}{E67}

## Conclusions

[[ 0.59 c

We calculated the formation of acoustic diffraction satellites while an acoustic wavefront propagates through the crystal, using the two-beam Takagi–Taupin equations. The simulations show satellite-dependent characteristic times, $\tau_n\propto1/\left|J_n(S)\right|$, and a transient intensity overshoot for finite acoustic rise times. {E0}{E1}{E9}{E67}

|| 0.41 c

> Steady-state satellite intensities alone do not determine their transient evolution. {E28}{E67}

]]

![Scope: two beams, symmetric geometry, no absorption, quasi-static diffraction; the simple expressions require small $\Lambda_{ac}/\Lambda_P$. No experimental comparison yet.](none){E0}{E20}{E62}
