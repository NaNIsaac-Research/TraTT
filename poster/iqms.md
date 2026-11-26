---
title: Transit-Time Limit on Sideband Formation // in Acoustically Driven Bragg Diffraction
authors: **Isaac Yong**¹, Ouyoung Kwon¹, Hyunjung Kim¹
affiliation: ¹Center for Ultrafast Phase Transformation, Department of Physics, Sogang University, Seoul, Korea
session: i-QMS 2026, Jeju, Nov. 29 – Dec. 4, 2026
footer: This work was supported by the National Research Foundation of Korea grant RS-2021-NR059920.
contact: Code, notebook and data: github.com/NaNIsaac-Research/TraTT (QR).
---

<!--
Printed text source for the i-QMS 2026 poster; build with python poster/build.py 150 poster/iqms.md.
Story and title follow the i-QMS abstract (Floquet sidebands, the transit-time limit, the
dynamical-regime deviation from the Bessel law, the drive envelope, the outlook); notation, sign
convention and layout are those of poster/poster.md. Every number is recomputed by
poster/check_numbers.py.
-->

@pair

## Floquet sidebands of a sound wave

![A shear wave bends the lattice planes periodically in depth; sideband $n$ sits at detuning $\beta=nK$ with kinematic weight $J_n(S)^2$.](figures/poster/f8_satellites.png){E0}{E7}

A shear wave along the depth $z$ with $u\parallel h$, $u=u_0\sin(Kz-\Omega t)$, $\Omega=Kv_s$, shifts the phase of the reflection $h$ by $\phi=h\cdot u=S\sin(Kz-\Omega t)$, $S=hu_0$. The drive is periodic in time, so the diffracted beam splits into Floquet channels: {E0}{E42}

$$ $e^{-i\phi}=\Sigma_n\,(-1)^nJ_n(S)\,e^{in(Kz-\Omega t)}$ {E0}

Sideband $n$ is Bragg-matched at $\beta_n=nK$ ($\beta$: deviation from the Bragg condition, in m$^{-1}$). The standard treatment assumes an instantaneous response and gives the Bessel law, $I_n\propto J_n(S)^2$. It does not say how fast this is reached. Two effects enter at high drive frequency: the drive arrives with a wavefront moving at $v_s$, and in a thick crystal the transmitted and diffracted beams are strongly coupled. {E0}{E7}{E29}

## Takagi–Taupin with a periodic drive

Transmitted and diffracted waves $D_0$, $D_h$ with envelopes slowly varying in depth $z\in[0,L]$; symmetric geometry, σ polarisation, no absorption: {E0}

$$ $dD_0/dz=(i\pi/\Lambda_P)\,e^{+i\phi}D_h$ {E0}

$$ $\pm\,dD_h/dz=(i\pi/\Lambda_P)\,e^{-i\phi}D_0+i\beta D_h$  (+ Laue, − Bragg) {E0}

In Bragg geometry $D_h$ travels back to the entrance face ($\gamma_h<0$), hence the sign. $\Lambda_P$: Pendellösung length. Projected onto channel $n$, each sideband is a two-beam problem of its own with coupling $(\pi/\Lambda_P)\left|J_n(S)\right|$, valid while the channels are separated, $\Lambda_{ac}/\Lambda_P\lesssim0.3$. {E0}{E20}{E44}{E54}

![Laue: $h$ lies in the surface, so the wave that couples is a shear wave, $u\parallel h$. Bragg: $h\parallel z$, so it is longitudinal. Si 440, 30 keV: Laue $\Lambda_P=98.8$ μm, $v_s=5.85$ km/s; Bragg $\Lambda_P=21.8$ μm, $v_s=9.14$ km/s.](figures/poster/f9_geometry.png){E0}{E20}{E85}

@pair

## Transit-time limit on formation

~ step | **Sudden onset:** at time $t$ only the layer $0<z<v_st$ is displaced. {E0}

While the wavefront crosses, channel $n$ grows over the displaced layer only. Closed forms for $t\leq t_{tr}=L/v_s$: {E1}{E9}

$$ $I_n=\sin^2(\pi t/\tau_n)$ (Laue), $\ \tanh^2(\pi t/\tau_n)$ (Bragg), $\ \tau_n=\Lambda_P/(v_s\left|J_n(S)\right|)$ {E1}{E9}

At $t=t_{tr}$ the crystal is filled and $I_n$ stops at its steady value: the sideband distribution cannot settle before the wavefront has crossed the crystal. $\tau_n$ does not depend on $L$, and the order follows $\left|J_n(S)\right|$, not $n$. Si 440, 30 keV, $S=1.5$, $n=1$: Laue $\tau_1=30$ ns ($L=296$ μm: $t_{tr}=50.6$ ns), Bragg $\tau_1=4.3$ ns. {E1}{E9}{E20}{E85}

![Full TT (points) against the closed forms (lines), no fitted parameters; time in units of $\tau_n$.](figures/poster/f1_collapse.png){E1}{E9}{E19}{E26}

## Steady state: where the Bessel law fails

In the filled crystal the same channel picture gives {E1}{E9}

$$ $I_n=\sin^2(\pi L\left|J_n(S)\right|/\Lambda_P)$ (Laue), $\ \tanh^2(\pi L\left|J_n(S)\right|/\Lambda_P)$ (Bragg) {E1}{E9}

For $L\ll\Lambda_P$ both reduce to the kinematic $(\pi LJ_n/\Lambda_P)^2$, the Bessel law. As $L$ approaches $\Lambda_P$ the strong sidebands saturate first, so the ratios move away from $J_n^2$: at $S=1.5$, $I_2/I_1=0.17$ kinematically, 0.22 at $L=\Lambda_P/2$ and 0.46 at $L=\Lambda_P$ (Laue). {E1}{E9}

![Full TT in the filled crystal (points, averaged over 8 acoustic phases), closed forms (lines) and the kinematic law (dashed), $S=1.5$, $\Lambda_{ac}=L/40$.](figures/poster/f10_steady.png){E1}{E9}{E54}

When the channels overlap ($\Lambda_{ac}/\Lambda_P\gtrsim0.3$) they couple through sidebands of the transmitted beam, and only full TT or Floquet calculations apply. {E44}{E54}

@pair

## Drive envelope: overshoot and pulse shape

~ ramp | **Linear rise,** $A(s)=\min(s/T_{rise},1)$ for $s\geq0$, with $s=t-z/v_s$ (a time). {E28}{E67}

Depth $z$ carries the amplitude $S\,A(t-z/v_s)$, so the sideband reads the drive accumulated over the last transit time: {E5}{E28}{E30}

$$ $I_n\approx\sin^2(\pi L\,\Theta_n/\Lambda_P),\qquad\Theta_n(t)=\frac{1}{L}\int_0^L J_n[S\,A(t-z/v_s)]\,dz$ {E5}{E28}

Settling ends at $t_{tr}+T_{rise}$. $J_1$ is largest at $S=1.84$ and zero at 3.83, so a drive beyond the maximum passes through stronger coupling on the way and $I_1$ overshoots its steady value. Pulse-shape condition from this form: with $S$ below the maximum of $J_n$ and $L\left|J_n(S)\right|/\Lambda_P<1/2$, $\Theta_n$ and $I_n$ rise monotonically for any ramp. {E5}{E15}{E67}

![Top: overshoot $\Delta I$ above the steady value, reduced model over 11,211 pairs $(S,T_{rise})$, $L=\Lambda_P/2$, $\Lambda_{ac}=L/40$; largest 0.603, below the bound 0.63. Bottom: cases A–C, reduced model (lines) and full TT (points) at $\beta=K$, averaged over the acoustic phase; dashed: steady value.](figures/poster/f7_overshoot.png){E15}{E28}{E67}

## Method, checks and outlook

- **Snapshots.** At each $t$ the displacement is frozen and the static TT equations are solved over $z$: the X-ray transit $L/c=0.99$ ps is 0.2 % of the 500 ps acoustic period (2 GHz, $L=296$ μm). Laue by RK4 from $z=0$; Bragg by the Riccati equation for $R=D_h/D_0$ from $R(L)=0$. {E0}{E62}
- **Checks.** $\sin^2(\pi L/\Lambda_P)$; $\left|D_0\right|^2+\left|D_h\right|^2=1$ (Laue); Bragg total reflection; grid refinement against 16384 steps; an exact Floquet solver. {E0}{E31}{E42}
- **Known.** Acoustic X-ray satellites and their Bessel weights; TT theory; time-resolved acoustic X-ray diffraction and switching (DeCamp et al., Nature 413, 825 (2001)); Bessel coupling in dynamical diffraction (Polikarpov & Skadorov, phys. stat. sol. (b) 143, 11 (1987)). {E7}{E21}{E29}
- **This work.** The sideband dynamics while the drive enters: the transit-time limit, the closed forms against full TT, the thickness at which the Bessel law fails, and the envelope effect. {E0}{E1}{E9}{E54}{E67}
- **Not yet.** Comparison with experiment; absorption; asymmetric geometry; realistic acoustic pulse shapes; divergent or polychromatic X-rays. {E0}{E20}
- **Outlook.** Formation times of ns (Si 440: 4.3–30 ns) are long against storage-ring ($\sim$100 ps) and XFEL (fs) pulses, so time-resolved diffraction from an acoustically driven crystal can follow them. {E20}{E85}

> No sideband settles before the acoustic wavefront has crossed the crystal; channel $n$ forms on its own time $\tau_n=\Lambda_P/(v_s\left|J_n(S)\right|)$, and the Bessel law holds only for $L\ll\Lambda_P$. {E1}{E9}{E67}
