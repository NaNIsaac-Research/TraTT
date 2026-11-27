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
python explore/make_poster_figs.py --iqms f7 f12 f13 f17 (figures/poster/iqms/). f13 redraws slide 2 of the
October 2026 TraTT talk (onset schematic) beside a computed rocking curve.
v5l: journal register; the general result is stated first and the Si 440 case inside the sentence;
"Sec. N" cross references; ICAMD 2025 card look. Symbols are defined where they first appear; axes in
physical units. Look: lab header and footer, flat body (no tints, navy accent).
Every number is recomputed by poster/check_numbers.py. "Si 440", "30 keV" and "6 %" carry a
no-break space (U+00A0).
-->

## * Key result

**Acoustically induced X-ray sidebands form on the acoustic transit time, not on the acoustic period.** After a step onset of the drive, each sideband develops only within the strained region behind the acoustic wavefront: its intensity oscillates with the period $\tau_n$ while the wavefront crosses the crystal and reaches the steady-state value at $t_{tr}=L/v_s$. Takagi–Taupin calculations in the Laue geometry give $t_{tr}$ = 50.6 ns for a 296 μm Si 440 crystal driven at 2 GHz (acoustic period 0.5 ns). {E1}{E9}{E20}{E28}

## Introduction

[[ 0.45 c

![Left: Laue geometry with the acoustic wavefront at $z=v_st$. Right: calculated rocking curve without and with the acoustic wave ($S$ = 1.5) for Si 440, $L$ = 296 μm, convolved with a 10 μrad (FWHM) beam. Satellites of order $n$ appear at $\Delta\theta\propto n$. In a thick crystal the integrated intensity of order $n$ scales as $|J_n(S)|$ rather than $J_n^2(S)$, so the total diffracted intensity increases.](figures/poster/iqms/f13_rocking.png){E0}{E7}

|| 0.55 c

- **Background.** The dynamical theory of X-ray diffraction in acoustically excited crystals gives the steady-state sideband intensities (Entin 1977; Iolin & Entin 1983; Polikarpov & Skadorov 1987). {E7}{E21}{E29}

- **Objective.** The time scale on which the sidebands form after the drive is switched on. {E7}{E21}

- **Motivation.** Acoustically modulated crystals are candidates for fast X-ray switching and pulse shaping at storage rings and XFELs; the formation time bounds the switching speed. {E7}{E21}{E50}

- **Approach.** Takagi–Taupin equations with the time-dependent acoustic displacement in the Laue geometry; numerical results for Si 440 at 30 keV. {E0}{E20}

- **Result.** Sideband formation is limited by the acoustic transit time. {E1}{E9}{E28}

]]

## Acoustic modulation of X-ray diffraction

[[ 0.66

A coherent acoustic wave $u=u_0\sin(Kz-\Omega t)$ (wavelength $\Lambda_{ac}=2\pi/K$) imposes a travelling phase grating $\mathbf{h}\cdot\mathbf{u}$ on the reflection $\mathbf{h}$ ($h=2\pi/d$). The diffracted beam acquires satellites of order $n$ at $\mathbf{Q}=\mathbf{h}-nK\hat{z}$, shifted in energy by $n\hbar\Omega$. In the kinematic limit the satellite intensities follow the Bessel law $J_n^2(S)$, with $S=\mathbf{h}\cdot\mathbf{u}_0$ the modulation amplitude. {E0}{E7}{E42}

**Previous observations** {E7}{E21}

- Surface acoustic waves on GaAs: up to 12 satellites (Sauer et al., APL 75, 1709 (1999)). {E7}
- Picosecond acoustic pulses in GaAs, 100 ps (Rose-Petruck et al., Nature 398, 310 (1999)). {E21}
- Coherent acoustic phonons in InSb, picosecond resolution (Lindenberg et al., PRL 84, 111 (2000)). {E21}
- Sub-nanosecond acoustic X-ray switching in Laue-geometry Ge (DeCamp et al., Nature 413, 825 (2001)). {E21}
- Surface acoustic waves on langasite: satellite intensity versus drive amplitude (Vadilonga et al., J. Appl. Cryst. 50, 525 (2017)). {E7}

|| 0.34 c

![Left: kinematic weights $J_n^2(S)$ versus displacement amplitude $u_0$ for Si 440; dotted line: $S$ = 1.5. Right: measured satellite intensities $m$ = 0–4 versus transducer drive for a surface acoustic wave on langasite, with $J_m^2$ curves; data from Fig. 6 of Vadilonga et al. (2017), redrawn (CC BY). There the wave forms a surface grating; in the present work it propagates through the depth of the crystal.](figures/poster/iqms/f12_bessel.png){E7}{E21}

]]

@pair

## Dynamical theory: Takagi–Taupin equations

For $L\gtrsim\Lambda$ multiple scattering couples the transmitted and diffracted waves and the kinematic result no longer holds. In the symmetric Laue geometry the time-dependent Takagi–Taupin (TT) equations (Takagi 1962, 1969; Taupin 1964; Lindberg & Shvyd'ko 2012) for the transmitted amplitude $D_0$ and the diffracted amplitude $D_h$ read {E0}{E20}{E62}

$$ $(\partial_z+\frac{1}{c\gamma}\partial_t)D_0=(i\pi/\Lambda)\,e^{i\mathbf{h}\cdot\mathbf{u}}D_h$,  $(\partial_z+\frac{1}{c\gamma}\partial_t)D_h=(i\pi/\Lambda)\,e^{-i\mathbf{h}\cdot\mathbf{u}}D_0+i\beta D_h$ {E0}

where $\Lambda$ is the Pendellösung length (98.8 μm for Si 440 at 30 keV), $\beta$ the deviation from the Bragg condition, $\mathbf{u}(z,t)$ the acoustic displacement and $\gamma=\cos\theta_B$. The X-ray transit time $L/(c\gamma)\approx1$ ps is much shorter than the acoustic period, so the $\partial_t$ terms are neglected in the calculations: the displacement is frozen during each transit and time enters only through $\mathbf{u}(z,t)$ (quasi-static approximation). Absorption is neglected. {E0}{E20}{E62}

| | Kinematic (Bessel law) | *Dynamical (TT, this work)
| Thickness | $L\ll\Lambda$ | arbitrary ($L=3\Lambda$ in Secs. 1–4)
| Scattering | single | multiple, $D_0\leftrightarrow D_h$
| Onset of the wave | grows monotonically with the strained depth | oscillates with period $\tau_n$ until $t_{tr}$
| Result | $J_n^2(S)$ | $I_n(t)$, formation time $\tau_n$ {E0}{E1}{E9}{E20}

## Sideband formation: transit-time limit

[[ 0.48 c

![](figures/poster/iqms/f17_formation.png){E0}{E1}{E9}{E20}{E85}

|| 0.52 c

For satellite $n$ the coupling is reduced by $|J_n(S)|$, and in the independent-satellite approximation the growing strained layer gives {E1}{E9}{E44}{E54}

$$ $I_n(t)=\sin^2(\pi t/\tau_n)$, {E1}{E9}

$$ $\tau_n=\Lambda/(v_s\left|J_n(S)\right|)$ {E1}{E9}

for $t<t_{tr}=L/v_s$, with $I_n$ constant for $t>t_{tr}$. The formation time $\tau_n$ is the time in which the wavefront traverses one extinction length $\Lambda/|J_n|$ of satellite $n$. For Si 440 with $S$ = 1.5 and $L$ = 296 μm: $\tau_1$ = 30 ns, $t_{tr}$ = 50.6 ns and a steady-state intensity of 0.73. In the Bragg (reflection) geometry the corresponding time is $\tau_1$ = 4.3 ns. {E1}{E9}{E20}{E28}{E85}

]]

![Top: unconvolved $|D_h(z,t)|^2$ at the centre of the first sideband after a step onset (TT, averaged over the acoustic phase). Bottom: intensity at the exit surface, $I_1(t)$. Ahead of the wavefront the crystal is unstrained and the diffracted intensity remains unchanged; behind it the field is in the steady state and depends only on depth. Si 440, $S$ = 1.5, $L$ = 296 μm.](none){E1}{E9}{E20}

@pair

## Drive envelope and overshoot

For a thin crystal ($L=\Lambda/2$) and a drive amplitude ramped linearly over $T_{rise}$, the first sideband exceeds its steady-state value only when the final amplitude lies beyond the first maximum of $J_1$ ($S$ = 1.84); otherwise the rise is monotonic. In the thick crystal of Sec. 4 a step onset overshoots already at $S$ = 1.5. {E15}{E67}

![Overshoot $\Delta I=I_{max}-I_{steady}$ of the first sideband versus final amplitude $S$ and rise time $T_{rise}/t_{tr}$. Reduced model (independent satellites; lines), verified against the full TT solution (symbols) at 12 points and for cases A–C; dashed: steady-state value. Laue geometry, $L=\Lambda/2$ (49 μm Si 440); the $L=3\Lambda$ crystal of Secs. 1–4 has not been scanned.](figures/poster/iqms/f7_overshoot.png){E15}{E67}

## Conclusions and outlook

> **Sideband formation is limited by the acoustic transit time** $t_{tr}=L/v_s$. The formation time $\tau_n=\Lambda/(v_s|J_n(S)|)$, not the acoustic period, sets the time scale of the transient (tens of ns in Si). {E1}{E9}{E67}

- **Thick crystals.** For $L>\Lambda$ the satellite intensities deviate from the Bessel law, which is recovered for $L\ll\Lambda$. {E0}{E44}

- **Drive envelope.** In a thin crystal ($L=\Lambda/2$) a ramped drive produces an overshoot only for $S$ beyond the first maximum of $J_1$ (1.84) (Sec. 5). {E15}{E67}

- **Outlook.** Time-resolved measurement on Si 440: $S$ = 1.5 corresponds to $u_0$ = 23 pm (displacement gradient $Ku_0=5\times10^{-5}$ at 2 GHz). A beam divergence of 10 μrad resolves the satellites (Sec. 1); tracking a single satellite in time calls for a divergence of about 0.05 μrad (rms), a tenth of the satellite's rocking half-width. {E20}{E73}{E84}{E92}

![Numerics: TT equations integrated with RK4 and validated against an exact Floquet solution for a periodic drive; for an acoustically filled crystal the independent-satellite model reproduces the phase-averaged integrated satellite intensities of full TT within 6 % for $\Lambda_{ac}<0.3\,\Lambda$.](none){E0}{E19}{E20}{E31}{E42}{E54}{E62}
