---
title: Transient Formation Dynamics of Acoustic Bragg Satellites // in Dynamical X-ray Diffraction
authors: **Isaac Yong**¹, Ouyoung Kwon¹, Hyunjung Kim¹
affiliation: ¹Center for Ultrafast Phase Transformation, Department of Physics, Sogang University, Seoul, Korea
session: P2.17 · 2026 KPS Fall Meeting, Jeju, October 22, 2026
footer: This work was supported by the National Research Foundation of Korea grant RS-2021-NR059920.
contact: Code, notebook and data: github.com/NaNIsaac-Research/TraTT (QR).
---

<!--
Printed text source; build with python poster/build.py. Order and claims follow the October 2026
talk (v4): why sound makes satellites, why Takagi-Taupin, numerics, what happens while the sound
enters, what is checked and what is not. Notation is physical throughout (z, t, beta in 1/m,
K, Lambda_P, v_s, S = h u0); the solver's scaled variables are not used. Every number is
recomputed by poster/check_numbers.py.
-->

@pair

## Acoustic satellites

![Kinematic picture: a shear wave bends the lattice planes periodically in depth; satellite $n$ sits at detuning $\beta=nK$ with weight $J_n(S)^2$.](figures/poster/f8_satellites.png){E0}{E7}

A shear wave along the depth $z$ with displacement $u\parallel h$, $u=u_0\sin(Kz-\Omega t)$, $K=2\pi/\Lambda_{ac}$, $\Omega=Kv_s$, shifts the phase of the reflection $h$ by $\phi=h\cdot u=S\sin(Kz-\Omega t)$, with the dimensionless amplitude $S=hu_0$ (Si 440: $S=1.5$ is $u_0=23$ pm). {E0}{E85}

$$ $e^{-i\phi}=\Sigma_n\,(-1)^nJ_n(S)\,e^{in(Kz-\Omega t)}$ {E0}

Harmonic $n$ is Bragg-matched at $\beta_n=nK$ ($\beta$: deviation from the Bragg condition, in m$^{-1}$). Kinematically satellite $n$ carries $J_n(S)^2$, with $\Sigma_nJ_n^2=1$ and equal weight for $\pm n$. In a thick crystal the diffracted wave is scattered back, so dynamical theory sets the intensities. {E0}{E7}{E29}

## Two-beam dynamical diffraction

Transmitted and diffracted waves $D_0$, $D_h$ with envelopes slowly varying in depth $z\in[0,L]$; symmetric geometry, σ polarisation, no absorption. Takagi–Taupin (TT) equations: {E0}

$$ $dD_0/dz=(i\pi/\Lambda_P)\,e^{+i\phi}D_h$ {E0}

$$ $\pm\,dD_h/dz=(i\pi/\Lambda_P)\,e^{-i\phi}D_0+i\beta D_h$  (+ Laue, − Bragg) {E0}

In Bragg geometry $D_h$ travels back to the entrance face ($\gamma_h<0$), hence the sign. $\Lambda_P$: Pendellösung length (Laue, $\phi=0$, $\beta=0$: $I_h=\sin^2(\pi z/\Lambda_P)$). The displacement enters only as the phase of the coupling. {E0}{E20}

![Laue: $h$ lies in the surface, so the wave that couples is a shear wave, $u\parallel h$. Bragg: $h\parallel z$, so it is longitudinal. Si 440, 30 keV: Laue $\Lambda_P=98.8$ μm, $v_s=5.85$ km/s; Bragg $\Lambda_P=21.8$ μm, $v_s=9.14$ km/s.](figures/poster/f9_geometry.png){E0}{E20}{E85}

@pair

## Numerical solution

An acoustic wave launched at $z=0$ at $t=0$, with envelope $A$ ($A=0$ ahead of the wavefront, $z>v_st$): {E0}

$$ $\phi(z,t)=S\,A(t-z/v_s)\,\sin(Kz-\Omega t)$ {E0}

- **Snapshots.** At each $t$ the displacement is held fixed and the static TT equations are solved over $z$, giving $I_h(\beta,t)$. The X-ray transit $L/c=0.99$ ps is 0.2 % of the 500 ps acoustic period (2 GHz, $L=296$ μm). {E0}{E62}
- **Laue.** $D_0(0)=1$, $D_h(0)=0$; fixed-step RK4 from $z=0$ to $L$; $I_h=\left|D_h(L)\right|^2$. {E0}
- **Bragg.** $D_0(0)=1$, $D_h(L)=0$; $R=D_h/D_0$ by RK4 from $R(L)=0$ back to $z=0$; $I_h=\left|R(0)\right|^2$: {E0}

$$ $dR/dz=-(i\pi/\Lambda_P)\,e^{-i\phi}-i\beta R-(i\pi/\Lambda_P)\,e^{+i\phi}R^2$ {E0}

- **Satellite $n$.** $I_n(t)=I_h(nK,t)$, in units of the incident intensity. {E0}
- **Checks.** $\sin^2(\pi L/\Lambda_P)$; $\left|D_0\right|^2+\left|D_h\right|^2=1$ (Laue); Bragg total reflection; steps 256–4096 against 16384; a Floquet calculation. {E0}{E31}{E42}

![Snapshot at $t=0.62\,L/v_s$ ($L=0.6\,\Lambda_P$, $\Lambda_{ac}=L/5$, $S=1.5$): satellites at $\beta=nK$ before the wave has filled the crystal.](figures/poster/f0_scheme.png){E0}

## Satellite formation while the sound enters

~ step | **Sudden onset,** $A=1$ behind the wavefront: at time $t$ the displaced layer is $0<z<v_st$. {E0}

Each satellite as an independent two-beam problem with coupling $(\pi/\Lambda_P)\left|J_n(S)\right|$ over the displaced layer ($\Lambda_{ac}/\Lambda_P\lesssim0.3$), for $t\leq t_{tr}=L/v_s$: {E1}{E9}{E54}

$$ $I_n=\sin^2(\pi t/\tau_n)$ (Laue), $\ \tanh^2(\pi t/\tau_n)$ (Bragg), $\ \tau_n=\Lambda_P/(v_s\left|J_n(S)\right|)$ {E1}{E9}

$\tau_n$ does not depend on $L$; the order follows $\left|J_n(S)\right|$, not $n$ ($S=3$: $n=2,1,3$). Si 440, 30 keV, $S=1.5$, $n=1$: Laue $\tau_1=30$ ns, first maximum at 15 ns; Bragg $\tau_1=4.3$ ns, 99 % at 4.1 ns. {E1}{E9}{E20}{E85}

![Full TT (points) against the formulas (lines), no fitted parameters.](figures/poster/f1_collapse.png){E1}{E9}{E19}{E26}

@pair

## Gradual onset: a maximum above the steady value

~ ramp | **Linear rise,** $A(s)=\min(s/T_{rise},1)$ for $s\geq0$, with $s=t-z/v_s$ (a time). {E28}{E67}

During the transit depth $z$ carries the amplitude $S\,A(t-z/v_s)$, so the crystal holds a range of amplitudes. Reduced model, Laue: {E5}{E28}

$$ $I_n\approx\sin^2(\pi L\,\Theta_n/\Lambda_P),\qquad\Theta_n(t)=\frac{1}{L}\int_0^L J_n[S\,A(t-z/v_s)]\,dz$ {E5}{E28}

$J_1$ is not monotonic (largest at $S=1.84$, zero at 3.83), so $I_1$ can pass through a maximum above its steady value. This panel uses a thinner crystal, $L=\Lambda_P/2$ (49 μm for Si 440 at 30 keV), with $\Lambda_{ac}=L/40$. {E67}

![Top: $\Delta I$ from the reduced model over 11,211 pairs $(S,T_{rise})$; largest 0.603, below the bound $\sin^2(\pi\cdot0.5\cdot0.582)=0.63$. Bottom: cases A–C, reduced model (lines) and full TT (points) at $\beta=K$, averaged over the acoustic phase; dashed: steady value.](figures/poster/f7_overshoot.png){E15}{E28}{E67}

## What is checked and what is not

- **Known.** Acoustic X-ray satellites and their Bessel weights; TT theory; time-resolved acoustic X-ray diffraction and switching (DeCamp et al., Nature 413, 825 (2001)); Bessel coupling in dynamical diffraction (Polikarpov & Skadorov, phys. stat. sol. (b) 143, 11 (1987)). {E7}{E21}{E29}
- **This work.** TT calculations for successive displacement snapshots while the acoustic wave crosses the crystal; the formation law and the reduced model agree with full TT for $\Lambda_{ac}/\Lambda_P\lesssim0.3$. {E0}{E1}{E9}{E54}{E67}

![Satellite populations of the independent-satellite model against full TT in a filled Laue crystal, relative error $\Sigma_n\left|p_n-p_n^{ind}\right|/\Sigma_np_n^{ind}$: below $\Lambda_{ac}/\Lambda_P=0.3$ it stays under 6 %.](figures/poster/f4_regime.png){E19}{E54}

- **Not yet.** Comparison with experiment; absorption; asymmetric geometry; realistic acoustic pulse shapes; divergent or polychromatic X-rays. {E0}{E20}
- **Numbers.** X-ray constants from X0h; elastic constants are textbook values for a Si(001) slab ($v_s=\sqrt{c_{44}/\rho}$ for the shear wave). {E20}{E85}

> In these calculations satellite $n$ forms on its own time $\tau_n=\Lambda_P/(v_s\left|J_n(S)\right|)$, and with a finite rise time its intensity can exceed the steady value. {E1}{E67}
