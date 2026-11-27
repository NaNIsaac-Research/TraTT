---
title: Transit-Time Limit on Sideband Formation // in Acoustically Driven Bragg Diffraction
authors: **Isaac Yong**¹, Ouyoung Kwon¹, Hyunjung Kim¹
affiliation: ¹Center for Ultrafast Phase Transformation, Department of Physics, Sogang University, Seoul, Korea
session: Poster 10-1533 · Jeju, December 3, 2026
look: lab
flat: 1
logo_left: poster/assets/logo_iqms_a_white.png
body_pt: 28
caption_pt: 24
eq_pt: 30
footer: This work was supported by the National Research Foundation of Korea grant RS-2021-NR059920.
contact: Code, notebook and data: github.com/NaNIsaac-Research/TraTT (QR at right).
---

<!--
Printed text source for the i-QMS 2026 poster; build with python poster/build.py 150 poster/iqms.md.
Figures: uv run --with "mplume @ git+https://github.com/NaNIsaac/mplume@4c064154f8f0ff94f6c6dd300266b68a34759333"
python explore/make_poster_figs.py --iqms f11 f12 f13 f14 (figures/poster/iqms/). talk_twobeam.png is the
drawing of the October 2026 TraTT talk (NaNIsaac docs/decks/tratt/out/tratt-talk.pptx, slide 6),
copied unchanged; f13 redraws its slide 3 at S = 1.5.
v5: about half background (sections 1-3), one key result (4), one supporting result (5). Every
section opens with one sentence saying what it shows; symbols are defined where they first appear;
axes in physical units. Look: lab header and footer, flat body (no tints, navy accent).
Every number is recomputed by poster/check_numbers.py. "Si 440", "30 keV" and "6 %" carry a
no-break space (U+00A0).
-->

## Introduction

[[ 0.27 c

![Planes displaced by a shear wave; satellites at $\mathbf{Q}_n$ with kinematic weights ($S$ = 1.5).](figures/poster/iqms/f13_kinematic.png){E0}{E7}

|| 0.73 c

**Motivation.** A GHz sound wave displaces the lattice periodically in depth and time and splits an X-ray Bragg reflection into satellites (sidebands). Acoustic strain is a pump in ultrafast X-ray diffraction; acoustically driven crystals switch X-ray pulses (DeCamp et al. 2001) and are proposed as fast switches and pulse shapers at storage rings and XFELs. The build-up time of the sidebands sets their speed. Dynamical theory gives steady-state sideband intensities (Entin 1977; Iolin & Entin 1983; Polikarpov & Skadorov 1987), not their build-up in time. {E7}{E21}{E29}{E50}

> **This work.** After the sound is switched on, each sideband builds up as the acoustic wavefront enters the crystal. It is complete at the latest after the transit time (thickness / sound velocity, tens of ns in Si), not after the 0.5 ns acoustic period. {E1}{E9}{E28}

]]

## Acoustic modulation of X-ray diffraction

A sound wave turns the crystal into a moving phase grating; each grating order appears as an X-ray satellite. {E0}{E7}

[[ 0.36

The wave displaces the atoms by $u=u_0\sin(Kz-\Omega t)$ (acoustic wavelength $\Lambda_{ac}=2\pi/K$). A reflection with reciprocal-lattice vector $\mathbf{h}$ ($h=2\pi/d$, $d$ the plane spacing) sees the phase $\mathbf{h}\cdot\mathbf{u}$, which gives satellites of order $n$ at $\mathbf{Q}=\mathbf{h}-nK\hat{z}$, shifted in energy by $n\hbar\Omega$. In single scattering (kinematic theory) satellite $n$ has the weight $J_n(S)^2$, a Bessel function of $S=hu_0$: the Bessel law. {E0}{E7}{E42}

|| 0.64 c

![Left: Bessel weights against $u_0$, Si 440; dotted: $S$ = 1.5, used below. Right: surface acoustic wave on langasite, BESSY II: satellites $m$ = 0–4 against transducer drive, read from Fig. 6 of Vadilonga et al., J. Appl. Cryst. 50, 525 (2017) and redrawn (CC BY), with its $J_m^2$ lines. That wave is a surface grating; here the wave runs through the depth.](figures/poster/iqms/f12_bessel.png){E7}{E21}

]]

@pair

## Dynamical diffraction: Takagi–Taupin equations

In a thick, nearly perfect crystal X-rays are scattered many times; single scattering is no longer enough. {E0}{E20}

The Takagi–Taupin (TT) equations describe diffraction in a distorted crystal (Takagi 1962, 1969; Taupin 1964): the transmitted wave $D_0$ and the diffracted wave $D_h$ exchange intensity with depth $z$, and a displacement $\mathbf{u}$ enters as the phase $\mathbf{h}\cdot\mathbf{u}$ on their coupling. They are needed when the thickness $L$ reaches the extinction length $\Lambda$ (the Pendellösung period in transmission). A sound wave makes $\mathbf{u}$ depend on $z$ and $t$. {E0}{E20}{E62}

![Symmetric Laue (transmission) and Bragg (reflection). Si 440, 30 keV: $\Lambda$ = 98.8 μm (Laue), 21.8 μm (Bragg).](figures/poster/iqms/talk_twobeam.png){E0}

$$ $dD_0/dz=(i\pi/\Lambda)\,e^{i\mathbf{h}\cdot\mathbf{u}}D_h$,  $\pm\,dD_h/dz=(i\pi/\Lambda)\,e^{-i\mathbf{h}\cdot\mathbf{u}}D_0+i\beta D_h$ {E0}

$\beta$: deviation from the Bragg angle (1/length); + Laue, − Bragg. {E0}

## Sideband formation during acoustic onset

After switch-on, only the layer behind the wavefront is strained; each sideband grows with that layer. {E1}{E9}

![Left: Laue onset; the layer $0<z<v_st$ above the wavefront is displaced. Right: first sideband after a step onset, Si, $L$ = 296 μm, $S$ = 1.5 ($u_0$ = 23 pm), $I_0$ incident.](figures/poster/iqms/f11_formation.png){E0}{E1}{E9}{E20}{E85}

With sound, satellite $n$ is a two-beam problem with extinction length $\Lambda/\left|J_n(S)\right|$: in a crystal filled by the wave $I_n=\sin^2(\pi L\left|J_n\right|/\Lambda)$ (Laue) or $\tanh^2(\ldots)$ (Bragg), the Bessel law for $L\ll\Lambda$. {E1}{E9}{E44}{E54}

During onset the strained layer has thickness $v_st$ ($v_s$: sound velocity); with $L\to v_st$: {E1}{E9}

$$ $I_n=\sin^2(\pi t/\tau_n)$ (Laue), $\ \tanh^2(\pi t/\tau_n)$ (Bragg), $\ \tau_n=\Lambda/(v_s\left|J_n(S)\right|)$ {E1}{E9}

The formation time $\tau_n$ is the time for the front to cross one sideband extinction length $\Lambda/\left|J_n\right|$. Bragg saturates within $\tau_n$; Laue oscillates until the front leaves the crystal at the transit time $t_{tr}=L/v_s$, then holds its steady value. {E1}{E9}{E28}

Laue $\tau_1$ = 30 ns, $t_{tr}$ = 50.6 ns; Bragg $\tau_1$ = 4.3 ns, $t_{tr}$ = 32.4 ns. {E20}{E85}

@pair

## Thickness range of the Bessel law

The ratio of two sideband intensities shows up to which thickness single scattering is enough. {E1}{E9}

[[ 0.38

For $L\ll\Lambda$ the steady intensities follow the Bessel law; as $L$ approaches $\Lambda$ they deviate. At $S$ = 1.5 the Laue ratio $I_2/I_1$ is 0.17 (Bessel law) and 0.46 at $L=\Lambda$; Bragg deviates at smaller $L$. {E1}{E9}

|| 0.62 c

![Crystal filled by the wave, $S$ = 1.5: full TT (points), two-beam form (lines).](figures/poster/iqms/f14_thickness.png){E1}{E9}{E54}

]]

## Conclusions and outlook

> Sideband formation is complete within the acoustic transit time $L/v_s$ (tens of ns in Si); the formation time $\tau_n=\Lambda/(v_s\left|J_n\right|)$, not the acoustic period, sets the switching speed. The Bessel law holds for $L\ll\Lambda$. {E1}{E9}{E67}

**Outlook.** $S$ = 1.5 corresponds to $u_0$ = 23 pm (strain $5\times10^{-5}$ at 2 GHz). Resolving the sideband centre needs a beam divergence below 0.16 μrad (Bragg) or 0.05 μrad (Laue), a fraction of the Darwin half-width. {E20}{E73}{E84}{E92}

![Method: frozen strain snapshots (X-ray transit 0.99 ps, acoustic period 500 ps), RK4, checked against an exact periodic-drive (Floquet) solver; two-beam forms within 6 % of full TT for $\Lambda_{ac}<0.3\,\Lambda$. Scope: two beams, symmetric geometry, no absorption. Not yet: experiment, back-face reflection, asymmetric cuts, realistic pulses, divergent or polychromatic beams.](none){E0}{E19}{E20}{E31}{E42}{E54}{E62}
