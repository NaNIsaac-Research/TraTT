---
title: Transit-Time Limit on Sideband Formation // in Acoustically Driven Bragg Diffraction
authors: **Isaac Yong**¹, Ouyoung Kwon¹, Hyunjung Kim¹
affiliation: ¹Center for Ultrafast Phase Transformation, Department of Physics, Sogang University, Seoul, Korea
session: 10-1533 · i-QMS 2026, Jeju, December 3, 2026
footer: This work was supported by the National Research Foundation of Korea grant RS-2021-NR059920.
contact: Code, notebook and data: github.com/NaNIsaac-Research/TraTT (QR at right).
---

<!--
Printed text source for the i-QMS 2026 poster; build with python poster/build.py 150 poster/iqms.md.
Figures: python explore/make_poster_figs.py --iqms f1 f4 f7 f8 f9 f10 (figures/poster/iqms/).
Story and title follow the i-QMS abstract; notation, sign convention and layout are those of
poster/poster.md. "Closed form" is the one name for the independent-channel model (sin^2, tanh^2,
Theta_n). Every number is recomputed by poster/check_numbers.py. "Si 440" and "30 keV" carry a
no-break space (U+00A0).
-->

@pair

## Floquet sidebands of a sound wave

Acoustic strain is a standard pump in ultrafast X-ray studies, and acoustic Bragg switches gate X-ray pulses: how fast diffraction follows the strain sets the time resolution of both. {E7}{E21}

![A shear wave bends the lattice planes periodically in depth; sideband $n$ sits at detuning $\beta=nK$ (Laue) with kinematic weight $J_n(S)^2$.](figures/poster/iqms/f8_satellites.png){E0}{E7}

A shear wave along the depth $z$ with $u\parallel h$, $u=u_0\,\sin(Kz-\Omega t)$, shifts the phase of the reflection $h$ by $\phi=h\cdot u=S\,\sin(Kz-\Omega t)$, with $S=hu_0$, $K=2\pi/\Lambda_{ac}$ ($\Lambda_{ac}$: acoustic wavelength) and $\Omega=Kv_s$. The drive is periodic in space and time (Floquet), so the diffracted beam splits into sidebands: {E0}{E42}

$$ $e^{-i\phi}=\Sigma_n\,(-1)^nJ_n(S)\,e^{in(Kz-\Omega t)}$ {E0}

Sideband $n$ carries momentum $nK$ and energy $n\hbar\Omega$ (8 µeV at 2 GHz, not resolved). The standard treatment assumes an instantaneous response: the Bessel law, $I_n\propto J_n(S)^2$. At high drive frequency two effects enter: the wavefront moves at $v_s$, and in a thick crystal the two beams are strongly coupled. {E0}{E7}{E29}{E85}

## Takagi–Taupin with a periodic drive

Transmitted and diffracted amplitudes $D_0$, $D_h$, slowly varying in depth $z\in[0,L]$; symmetric geometry, σ polarisation, no absorption: {E0}

$$ $dD_0/dz=(i\pi/\Lambda_P)\,e^{+i\phi}D_h$ {E0}

$$ $\pm\,dD_h/dz=(i\pi/\Lambda_P)\,e^{-i\phi}D_0+i\beta D_h$  (+ Laue, − Bragg) {E0}

In Bragg geometry $D_h$ runs back to the entrance face, hence the − sign. $\Lambda_P$ is the Pendellösung length in Laue ($I_h=\sin^2(\pi z/\Lambda_P)$) and the extinction length in Bragg ($\left|R\right|^2=\tanh^2(\pi L/\Lambda_P)$ at $\beta=0$): the depth over which the two beams exchange intensity. {E0}{E20}

Harmonic $n$ is matched at $\beta=nK$ in Laue and $-nK$ in Bragg; $\left|J_{-n}\right|=\left|J_n\right|$, so both read the same at $\pm nK$. Each sideband then forms as a two-beam problem of its own with coupling $(\pi/\Lambda_P)\left|J_n(S)\right|$: the closed form below, valid for $\Lambda_{ac}/\Lambda_P\lesssim0.3$ (panel 6). {E0}{E44}{E54}

![Laue: $h$ lies in the surface, so the wave that couples is a shear wave, $u\parallel h$. Bragg: $h\parallel z$, so it is longitudinal. Si 440, 30 keV: Laue $\Lambda_P$ = 98.8 μm, $v_s$ = 5.85 km/s; Bragg $\Lambda_P$ = 21.8 μm, $v_s$ = 9.14 km/s.](figures/poster/iqms/f9_geometry.png){E0}{E20}{E85}

@pair

## Transit-time limit on formation

~ step | **Sudden onset:** at time $t$ only $0<z<v_st$ is displaced; no reflection at $z=L$. {E0}

Sideband $n$ grows over the displaced layer only. Closed form for $t\leq t_{tr}=L/v_s$: {E1}{E9}

$$ $I_n=\sin^2(\pi t/\tau_n)$ (Laue), $\ \tanh^2(\pi t/\tau_n)$ (Bragg), $\ \tau_n=\Lambda_P/(v_s\left|J_n(S)\right|)$ {E1}{E9}

$\tau_n$ does not depend on $L$. **Laue:** $I_n$ oscillates until the wavefront reaches $z=L$ and settles exactly at $t_{tr}$. **Bragg:** $I_n$ saturates at about $\tau_n$ (99 % at $0.95\,\tau_n$), before $t_{tr}$ in a thick crystal. Neither settles later than $t_{tr}$ ($t_{tr}+T_{rise}$ with a ramp). {E1}{E9}{E28}

Si 440, 30 keV, $S$ = 1.5, $n$ = 1, $L$ = 296 μm: Laue $\tau_1$ = 30 ns, $t_{tr}$ = 50.6 ns; Bragg $\tau_1$ = 4.3 ns (99 % at 4.1 ns), $t_{tr}$ = 32.4 ns. {E20}{E85}

![Full TT (points) against the closed form (lines), no fitted parameters; ticks mark $t_{tr}$ of each case, where the points end. $\Lambda_{ac}=L/20$.](figures/poster/iqms/f1_collapse.png){E1}{E9}{E19}{E26}

## Steady state: where the Bessel law fails

In the filled crystal ($t\geq t_{tr}$) the closed form gives {E1}{E9}

$$ $I_n=\sin^2(\pi L\left|J_n(S)\right|/\Lambda_P)$ (Laue), $\ \tanh^2(\pi L\left|J_n(S)\right|/\Lambda_P)$ (Bragg) {E1}{E9}

For $L\ll\Lambda_P$ both reduce to the kinematic $(\pi LJ_n/\Lambda_P)^2$, the Bessel law. In thicker crystals the strong sidebands leave the quadratic regime first (Laue: Pendellösung maximum at $L=\Lambda_P/(2\left|J_n\right|)$; Bragg: saturation), so the ratios move away from $J_n^2$. At $S$ = 1.5, $I_2/I_1$ is 0.17 kinematically, 0.22 at $L=\Lambda_P/2$ and 0.46 at $L=\Lambda_P$ (Laue). {E1}{E9}

![Full TT in the filled crystal (points, averaged over 8 acoustic phases), closed form (solid) and kinematic law (dashed), $S$ = 1.5, $\Lambda_{ac}=L/40$ (the closed form does not depend on $\Lambda_{ac}$). Right: Laue solid with filled points, Bragg dash-dot with open points.](figures/poster/iqms/f10_steady.png){E1}{E9}{E54}

@pair

## Drive envelope: overshoot and pulse shape

~ ramp | **Linear rise,** $A(s)=\min(s/T_{rise},1)$ for $s=t-z/v_s\geq0$. {E28}{E67}

Depth $z$ carries the amplitude $S\,A(t-z/v_s)$, so the sideband reads the drive accumulated over the last transit time. Closed form (Laue): {E5}{E28}{E30}

$$ $I_n\approx\sin^2(\pi L\,\Theta_n/\Lambda_P),\qquad\Theta_n(t)=(1/L)\int_0^L J_n[S\,A(t-z/v_s)]\,dz$ {E5}{E28}

Settling ends at $t_{tr}+T_{rise}$. $J_1$ is largest at $S$ = 1.84 and zero at 3.83: a drive beyond the maximum passes stronger coupling on the way, and $I_1$ overshoots its steady value. The overshoot grows with $T_{rise}$ (largest $\Delta I$ 0.010 at $T_{rise}=0.05\,t_{tr}$, 0.60 at $4\,t_{tr}$); a fast rise avoids it and settles soonest. {E5}{E15}{E67}

**Pulse-shape rule.** With $S$ below the first maximum of $\left|J_n\right|$ and $L\left|J_n(S)\right|/\Lambda_P<1/2$, $\Theta_n$ and $I_n$ rise monotonically for any non-decreasing envelope. {E5}{E67}

![Top: $\Delta I$ from the closed form, $L=\Lambda_P/2$, $\Lambda_{ac}=L/40$; largest 0.603 at the $T_{rise}=4\,t_{tr}$ edge, still rising toward $\sin^2(\pi\cdot0.5\cdot0.582)$ = 0.63 (0.582 = max $J_1$). Bottom: A–C, closed form (lines) and full TT (points, averaged over the acoustic phase) at $\beta=K$; dashed: steady value.](figures/poster/iqms/f7_overshoot.png){E15}{E28}{E67}

## Method, checks and outlook

- **Known.** TT equations (Takagi 1962, 1969; Taupin 1964); steady Bessel coupling of acoustic satellites (Entin 1977; Iolin & Entin 1983; Polikarpov & Skadorov 1987); temporal Pendellösung of the main reflection and acoustic switching (DeCamp et al. 2001). {E7}{E21}{E29}{E50}
- **This work.** One clock per sideband, scaled by $\left|J_n(S)\right|$; the transit-time limit; where the Bessel law fails; the envelope overshoot; all checked against full TT. {E0}{E1}{E9}{E54}{E67}

![Closed form against full TT, filled Laue crystal, error $\Sigma_n\left|p_n-p_n^{cf}\right|/\Sigma_np_n^{cf}$ of the sideband populations: under 6 % below $\Lambda_{ac}/\Lambda_P$ = 0.3; above, the channels couple through sidebands of the transmitted beam.](figures/poster/iqms/f4_regime.png){E19}{E44}{E54}

- **Method.** Frozen snapshots ($L/c$ = 0.99 ps is 0.2 % of the 500 ps period at 2 GHz); RK4, Bragg via $R=D_h/D_0$ from $R(L)=0$; checked by analytic limits, grid refinement and an exact Floquet solver. {E0}{E31}{E42}{E62}
- **Not yet.** Experiment; absorption; acoustic reflection at the back face; asymmetric geometry; realistic pulse shapes; divergent or polychromatic X-rays. {E0}{E20}
- **Outlook.** $S$ = 1.5 is $u_0$ = 23 pm, a strain $Ku_0=5\times10^{-5}$ at 2 GHz (Laue). Formation times of 4–30 ns are long against storage-ring (~100 ps) and XFEL (fs) pulses. The closed form is for the sideband centre: it needs a divergence below $0.3\,w_n$ (Bragg) or $0.1\,w_n$ (Laue), $w_n=\left|J_n(S)\right|$ Darwin half-widths, here 0.16 and 0.05 μrad. With an ordinary beam one measures the channel-integrated intensity (Laue, beam $\gtrsim5\,w_n$), its time course from full TT. {E20}{E73}{E84}{E86}{E87}{E92}

> An acoustically driven crystal reaches its final sidebands no later than the transit time $L/v_s$, and in Laue not before it: nanoseconds in Si. The Bessel-law intensities hold only for crystals much thinner than $\Lambda_P$. {E1}{E9}{E67}
