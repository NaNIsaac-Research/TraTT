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

When an acoustic wave is switched on in a crystal, the X-ray **sidebands do not appear at once**: each grows only behind the **acoustic wavefront**. Time-dependent Takagi–Taupin equations show that formation is **complete at the transit time** $t_{tr}=L/v_s$, **not after one acoustic period** (example: Si 440, 296 μm, 2 GHz: 50.6 ns, not 0.5 ns). {E1}{E9}{E20}{E28}

## Introduction: why the build-up time matters

[[ 0.5 c

![A sound wave displaces the lattice planes; the rocking curve gains satellites (sidebands) at offsets proportional to $n$. In a thick crystal a peak's area scales with $|J_n|$, not $J_n^2$, so together the peaks exceed the no-wave peak. Example: Si 440, $L$ = 296 μm, $S$ = 1.5, 10 μrad (FWHM) beam.](figures/poster/iqms/f13_rocking.png){E0}{E7}

|| 0.5 c

- **The question:** dynamical theory gives steady sideband intensities (Entin 1977; Iolin & Entin 1983; Polikarpov & Skadorov 1987). How fast do they build up after switch-on? {E7}{E21}{E29}

- **Why it matters:** acoustically driven crystals are proposed as fast X-ray switches and pulse shapers at storage rings and XFELs; the build-up time sets their speed. {E7}{E21}{E50}

- **Approach:** time-dependent Takagi–Taupin equations in Laue (transmission) geometry; example: Si 440 at 30 keV. {E0}{E20}

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

![Left: Bessel weights $J_n(S)^2$; $u_0$ scale for the Si 440 example, dotted: its $S$ = 1.5. Right: surface acoustic wave (a surface grating) on langasite, BESSY II: satellites $m$ = 0–4 against drive, from Fig. 6 of Vadilonga et al., J. Appl. Cryst. 50, 525 (2017), redrawn (CC BY), with $J_m^2$ lines.](figures/poster/iqms/f12_bessel.png){E7}{E21}

]]

@pair

## Takagi–Taupin equations in Laue geometry

In a thick, nearly perfect crystal X-rays scatter many times, not once. {E0}{E20}

In Laue (transmission) geometry (section 1) the Takagi–Taupin (TT) equations (Takagi 1962, 1969; Taupin 1964) couple the transmitted wave $D_0$ and the diffracted wave $D_h$ along the depth $z$; the displacement $\mathbf{u}(z,t)$ enters as the phase $\mathbf{h}\cdot\mathbf{u}$ ($\Lambda$: Pendellösung length, example: 98.8 μm for Si 440; $\beta$: deviation from the Bragg angle). {E0}{E20}{E62}

$$ $dD_0/dz=(i\pi/\Lambda)\,e^{i\mathbf{h}\cdot\mathbf{u}}D_h$,  $dD_h/dz=(i\pi/\Lambda)\,e^{-i\mathbf{h}\cdot\mathbf{u}}D_0+i\beta D_h$ {E0}

**What TT adds.** The Bessel law counts each X-ray as scattered once. In TT, $D_h$ scatters back into $D_0$, so intensity swaps between them with depth; a sideband's intensity then depends on the thickness and, while the wave enters, on time. {E0}{E20}{E44}

| | Kinematic (Bessel law) | *Dynamical (TT, this work)
| Thickness | $L\ll\Lambda$ | any; here $L$ = 3$\Lambda$
| Scattering | once | many, $D_0\leftrightarrow D_h$
| Time | steady only | onset, $L\to v_st$
| Predicts | weights $J_n(S)^2$ | $I_n(t)$, formation time {E0}{E1}{E9}{E20}

## Sideband formation: the transit-time limit

[[ 0.56 c

![](figures/poster/iqms/f17_formation.png){E0}{E1}{E9}{E20}{E85}

|| 0.44 c

After switch-on, only the layer behind the wavefront $z=v_st$ is strained; each sideband grows with that layer. {E1}{E9}

$$ $I_n=\sin^2(\pi t/\tau_n)$ {E1}{E9}

$$ $\tau_n=\Lambda/(v_s\left|J_n(S)\right|)$ {E1}{E9}

In $\tau_n$ the front crosses one extinction length $\Lambda/\left|J_n\right|$; at $t_{tr}=L/v_s$ the sideband stops at $\sin^2(\pi t_{tr}/\tau_n)$. In Bragg geometry it saturates much earlier. Example: $t_{tr}$ = 50.6 ns, $\tau_1$ = 30 ns, steady 0.73; Bragg: 4.3 ns. {E1}{E9}{E20}{E28}{E44}{E54}{E85}

]]

![Example: Laue, Si 440, $S$ = 1.5, $L$ = 296 μm, step onset; TT, phase-averaged; top: $|D_h(z)|^2$ at the first-sideband angle, bottom: its edge $z=L$. Below the front the crystal is unstrained, so $D_h$ passes down unchanged (vertical stripes); above it the field depends only on depth (horizontal stripes).](none){E1}{E9}{E20}

@pair

## Drive envelope: overshoot

With a linear ramp of the drive, the first sideband overshoots its steady value only if the final $S$ lies above the maximum of $J_1$ ($S$ = 1.84); below it the rise is monotonic. {E15}{E67}

![$\Delta I=I_{max}-I_{steady}$ of the first sideband for a linear ramp of duration $T_{rise}$, then held. Reduced model (lines; circles: full TT, also at 12 map points), Laue, $L=\Lambda/2$ (example: 49 μm, Si 440); dashed: steady value. The 296 μm example of sections 1–4 is not scanned.](figures/poster/iqms/f7_overshoot.png){E15}{E67}

## Conclusions and outlook

> **Sideband formation is complete within the acoustic transit time** $L/v_s$; the formation time $\tau_n$, not the acoustic period, sets the switching speed. The Bessel law holds for $L\ll\Lambda$. Example: 50.6 ns for 296 μm of Si. {E1}{E9}{E67}

- **Drive envelope:** a linear ramp gives an overshoot only for $S$ above the $J_1$ maximum (1.84); below it the sideband rises monotonically (section 5). {E15}{E67}

- **Outlook:** the drive is weak: $S=hu_0$ = 1.5 needs $u_0$ = 1.5/$h$ (example: 23 pm, strain $5\times10^{-5}$ at 2 GHz). Next: an experiment. Separating the satellites needs a beam narrower than their spacing (example: 10 μrad, section 1); following the centre of one sideband in time needs a divergence below a tenth of its Darwin half-width (example: 0.05 μrad). {E20}{E73}{E84}{E92}

![Method: TT equations, RK4, checked against an exact periodic-drive (Floquet) solver; two-beam forms within 6 % of full TT for $\Lambda_{ac}<0.3\,\Lambda$.](none){E0}{E19}{E20}{E31}{E42}{E54}{E62}
