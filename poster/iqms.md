---
title: Transit-Time Limit on Sideband Formation // in Acoustically Driven Bragg Diffraction
authors: **Isaac Yong**¹, Ouyoung Kwon¹, Kyuseok Yun¹, Hyunjung Kim¹
affiliation: ¹Center for Ultrafast Phase Transformation, Department of Physics, Sogang University, Seoul, Korea
session: Poster 10-1533 · Jeju, December 3, 2026
look: lab
flat: 1
cards: 1
head_pt: 40
panel_gap: 5
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
python explore/make_poster_figs.py --iqms f11 f12 f13 f16 (figures/poster/iqms/). f13 redraws slide 2 of the
October 2026 TraTT talk (onset schematic) beside a computed rocking curve.
v5e: one story in Laue geometry; ICAMD 2025 card look (key-result card, overview strip, cards). Every
section opens with one sentence saying what it shows; symbols are defined where they first appear;
axes in physical units. Look: lab header and footer, flat body (no tints, navy accent).
Every number is recomputed by poster/check_numbers.py. "Si 440", "30 keV" and "6 %" carry a
no-break space (U+00A0).
-->

## * Key result

When a GHz shear wave is switched on in silicon, the X-ray **sidebands do not appear at once**: each grows only behind the **acoustic wavefront**. Time-dependent Takagi–Taupin equations (Laue geometry) show that the first sideband of a 296 μm crystal is **complete at the transit time** (50.6 ns), **not after one acoustic period** (0.5 ns). {E1}{E9}{E20}{E28}

## Introduction: why the build-up time matters

[[ 0.5 c

![A sound wave displaces the lattice planes; the rocking curve gains satellite peaks (sidebands) at angle offsets proportional to $n$. Si 440, $L$ = 296 μm. Peak widths are set by the 10 μrad (FWHM) beam; in this thick crystal a peak's area scales with $|J_n|$, not $J_n^2$, so together the peaks exceed the no-wave peak.](figures/poster/iqms/f13_rocking.png){E0}{E7}

|| 0.5 c

- **The question:** dynamical theory gives steady sideband intensities (Entin 1977; Iolin & Entin 1983; Polikarpov & Skadorov 1987). How fast do they build up after switch-on? {E7}{E21}{E29}

- **Why it matters:** acoustically driven crystals are proposed as fast X-ray switches and pulse shapers at storage rings and XFELs; the build-up time sets their speed. {E7}{E21}{E50}

- **Approach:** time-dependent Takagi–Taupin equations, Laue (transmission) geometry, Si 440 at 30 keV. {E0}{E20}

- **Result:** each sideband builds up behind the acoustic wavefront and is complete at the transit time. {E1}{E9}{E28}

]]

## Acoustic modulation of X-ray diffraction: theory and observations

A sound wave turns the crystal into a moving phase grating; each grating order appears as an X-ray satellite. {E0}{E7}

[[ 0.6

The wave displaces the atoms by $u=u_0\sin(Kz-\Omega t)$ (acoustic wavelength $\Lambda_{ac}=2\pi/K$). A reflection with reciprocal-lattice vector $\mathbf{h}$ ($h=2\pi/d$, $d$ the plane spacing) sees the phase $\mathbf{h}\cdot\mathbf{u}$, which gives satellites of order $n$ at $\mathbf{Q}=\mathbf{h}-nK\hat{z}$, shifted in energy by $n\hbar\Omega$. In single scattering (kinematic theory) satellite $n$ has the weight $J_n(S)^2$, a Bessel function of $S=hu_0$: the Bessel law. {E0}{E7}{E42}

**Observed so far.** {E7}{E21}

- 1999, GaAs, surface wave: up to 12 satellites (Sauer et al., APL 75, 1709). {E7}
- 1999, GaAs: 100 ps acoustic pulse (Rose-Petruck et al., Nature 398, 310). {E21}
- 2000, InSb: coherent acoustic phonons, ps resolved (Lindenberg et al., PRL 84, 111). {E21}
- 2001, APS, Ge Laue: sub-ns acoustic X-ray switch (DeCamp et al., Nature 413, 825). {E21}
- 2017, BESSY II, langasite surface wave: satellites against drive (right). {E7}

|| 0.4 c

![Left: Bessel weights against $u_0$, Si 440; dotted: $S$ = 1.5, used below. Right: surface acoustic wave on langasite, BESSY II: satellites $m$ = 0–4 against transducer drive, read from Fig. 6 of Vadilonga et al., J. Appl. Cryst. 50, 525 (2017), and redrawn (CC BY), with its $J_m^2$ lines. That wave is a surface grating; here the wave runs through the depth.](figures/poster/iqms/f12_bessel.png){E7}{E21}

]]

@pair

## Takagi–Taupin equations in Laue geometry

In a thick, nearly perfect crystal X-rays are scattered many times; single scattering is no longer enough. {E0}{E20}

In Laue (transmission) geometry the X-rays cross the slab from the top face to the bottom face (section 1). The Takagi–Taupin (TT) equations (Takagi 1962, 1969; Taupin 1964) couple the transmitted wave $D_0$ and the diffracted wave $D_h$ along the depth $z$; the displacement $\mathbf{u}(z,t)$ enters as the phase $\mathbf{h}\cdot\mathbf{u}$ ($\Lambda$: Pendellösung length, 98.8 μm; $\beta$: deviation from the Bragg angle). {E0}{E20}{E62}

$$ $dD_0/dz=(i\pi/\Lambda)\,e^{i\mathbf{h}\cdot\mathbf{u}}D_h$,  $dD_h/dz=(i\pi/\Lambda)\,e^{-i\mathbf{h}\cdot\mathbf{u}}D_0+i\beta D_h$ {E0}

**What TT adds.** The Bessel law counts each X-ray as scattered once. In TT, $D_h$ scatters back into $D_0$, so intensity swaps between them with depth; a sideband's intensity then depends on the thickness and, while the wave enters, on time. {E0}{E20}{E44}

| | Kinematic (Bessel law) | *Dynamical (TT, this work)
| Thickness | $L\ll\Lambda$ | any; here $L$ = 3$\Lambda$
| Scattering | once | many, $D_0\leftrightarrow D_h$
| Time | steady only | onset, $L\to v_st$
| Predicts | weights $J_n(S)^2$ | $I_n(t)$, formation time {E0}{E1}{E9}{E20}

## Sideband formation: the transit-time limit

After switch-on, only the layer behind the wavefront is strained; each sideband grows with that layer. {E1}{E9}

![First sideband after a step onset, Laue, Si, $L$ = 296 μm, $S$ = 1.5 ($u_0$ = 23 pm); schematic in section 1.](figures/poster/iqms/f11_formation.png){E0}{E1}{E9}{E20}{E85}

Satellite $n$ is a two-beam problem with extinction length $\Lambda/\left|J_n(S)\right|$: a filled crystal gives $I_n=\sin^2(\pi L\left|J_n\right|/\Lambda)$; during onset the strained layer has thickness $v_st$ ($v_s$: sound velocity), so $L\to v_st$: {E1}{E9}{E44}{E54}

$$ $I_n=\sin^2(\pi t/\tau_n)$,  $\tau_n=\Lambda/(v_s\left|J_n(S)\right|)$ {E1}{E9}

In the formation time $\tau_n$ the front crosses one sideband extinction length; the sideband oscillates until the front leaves the crystal at $t_{tr}=L/v_s$, then holds ($\tau_1$ = 30 ns, $t_{tr}$ = 50.6 ns). In reflection (Bragg) geometry it saturates already at about $\tau_1$ = 4.3 ns. {E1}{E9}{E20}{E28}{E85}

@pair

## Build-up inside the crystal: depth–time map

[[ 0.62 c

![](figures/poster/iqms/f16_depth_time.png){E1}{E9}{E20}

|| 0.38 c

Behind the wavefront $z=v_st$ the sideband builds up; the crystal is complete when the front reaches $z=L$ at $t_{tr}$. {E1}{E9}

![Laue, Si 440, $S$ = 1.5, $L$ = 296 μm, step onset: $|D_h(z)|^2$ at the first-sideband angle (TT, phase-averaged). Below the front the crystal is unstrained, so $D_h$ passes down unchanged (vertical stripes); above it the field depends only on depth (horizontal stripes). The bottom edge $z=L$ is the section 4 curve.](none){E1}{E9}{E20}

]]

## Conclusions and outlook

> **Sideband formation is complete within the acoustic transit time** $L/v_s$ (tens of ns in Si); the formation time $\tau_n$, not the acoustic period, sets the switching speed. The Bessel law holds for $L\ll\Lambda$. {E1}{E9}{E67}

- **Outlook:** $S$ = 1.5 is $u_0$ = 23 pm (strain $5\times10^{-5}$ at 2 GHz). Next: an experiment. Separating the satellites needs only a 10 μrad beam (section 1); following the centre of one sideband in time needs a divergence below 0.05 μrad, a fraction of the Darwin half-width. {E20}{E73}{E84}{E92}

![Method: TT equations, RK4, checked against an exact periodic-drive (Floquet) solver; two-beam forms within 6 % of full TT for $\Lambda_{ac}<0.3\,\Lambda$.](none){E0}{E19}{E20}{E31}{E42}{E54}{E62}
