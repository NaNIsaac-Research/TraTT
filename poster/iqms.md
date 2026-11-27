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

**Acoustically induced X-ray sidebands form on the acoustic transit time, not on the acoustic period.** After the drive is switched on, each sideband develops only within the strained region behind the acoustic wavefront. Time-dependent Takagi–Taupin calculations in the Laue geometry show that the first sideband is complete at $t_{tr}=L/v_s$: 50.6 ns for a 296 μm Si 440 crystal driven at 2 GHz (acoustic period 0.5 ns). {E1}{E9}{E20}{E28}

## Introduction

[[ 0.42 c

![Left: Laue geometry with the acoustic wavefront at $z=v_st$. Right: calculated rocking curve without and with the acoustic wave ($S$ = 1.5) for Si 440, $L$ = 296 μm, convolved with a 10 μrad (FWHM) beam. Satellites of order $n$ appear at $\Delta\theta\propto n$. In a thick crystal the integrated intensity of order $n$ scales as $|J_n(S)|$ rather than $J_n^2(S)$, so the total diffracted intensity increases.](figures/poster/iqms/f13_rocking.png){E0}{E7}

|| 0.58 c

- **Background.** The dynamical theory of X-ray diffraction in acoustically excited crystals gives the stationary sideband intensities (Entin 1977; Iolin & Entin 1983; Polikarpov & Skadorov 1987). {E7}{E21}{E29}

- **Open problem.** The transient response after switch-on, i.e. the time scale on which the sidebands form. {E7}{E21}

- **Motivation.** Acoustically modulated crystals are candidates for fast X-ray switching and pulse shaping at storage rings and XFELs; the formation time bounds the switching speed. {E7}{E21}{E50}

- **Approach.** Time-dependent Takagi–Taupin equations in the Laue geometry; numerical results for Si 440 at 30 keV. {E0}{E20}

- **Result.** Sideband formation is limited by the acoustic transit time. {E1}{E9}{E28}

]]

## Acoustic modulation of X-ray diffraction

[[ 0.66

A coherent acoustic wave $u=u_0\sin(Kz-\Omega t)$ (wavelength $\Lambda_{ac}=2\pi/K$) imposes a travelling phase grating $\mathbf{h}\cdot\mathbf{u}$ on the reflection $\mathbf{h}$ ($h=2\pi/d$). The diffracted beam acquires satellites of order $n$ at $\mathbf{Q}=\mathbf{h}-nK\hat{z}$, shifted in energy by $n\hbar\Omega$. In the kinematic limit the satellite intensities follow the Bessel law $J_n^2(S)$, with $S=hu_0$ the modulation amplitude. {E0}{E7}{E42}

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

For $L\gtrsim\Lambda$ multiple scattering couples the transmitted and diffracted waves and the kinematic result no longer holds. In the symmetric Laue geometry the Takagi–Taupin (TT) equations (Takagi 1962, 1969; Taupin 1964) for the transmitted amplitude $D_0$ and the diffracted amplitude $D_h$ read {E0}{E20}{E62}

$$ $dD_0/dz=(i\pi/\Lambda)\,e^{i\mathbf{h}\cdot\mathbf{u}}D_h$,  $dD_h/dz=(i\pi/\Lambda)\,e^{-i\mathbf{h}\cdot\mathbf{u}}D_0+i\beta D_h$ {E0}

where $\Lambda$ is the Pendellösung length (98.8 μm for Si 440 at 30 keV), $\beta$ the deviation from the Bragg condition and $\mathbf{u}(z,t)$ the acoustic displacement. {E0}{E20}{E62}

**Beyond the kinematic limit.** Energy is exchanged between $D_0$ and $D_h$ over the depth (Pendellösung effect). The sideband intensity therefore depends on the crystal thickness and, during the onset of the wave, on time. {E0}{E20}{E44}

| | Kinematic (Bessel law) | *Dynamical (TT, this work)
| Thickness | $L\ll\Lambda$ | arbitrary ($L=3\Lambda$ in this work)
| Scattering | single | multiple, $D_0\leftrightarrow D_h$
| Time dependence | stationary | transient, strained depth $v_st$
| Result | $J_n^2(S)$ | $I_n(t)$, formation time $\tau_n$ {E0}{E1}{E9}{E20}

## Sideband formation: transit-time limit

[[ 0.48 c

![](figures/poster/iqms/f17_formation.png){E0}{E1}{E9}{E20}{E85}

|| 0.52 c

For satellite $n$ the coupling is reduced by $|J_n(S)|$, and in the two-beam approximation the growing strained layer gives {E1}{E9}{E44}{E54}

$$ $I_n(t)=\sin^2(\pi t/\tau_n)$, {E1}{E9}

$$ $\tau_n=\Lambda/(v_s\left|J_n(S)\right|)$ {E1}{E9}

for $t<t_{tr}=L/v_s$, with $I_n$ constant for $t>t_{tr}$. The formation time $\tau_n$ is the time in which the wavefront traverses one extinction length $\Lambda/|J_n|$ of satellite $n$. For Si 440 with $S$ = 1.5 and $L$ = 296 μm: $\tau_1$ = 30 ns, $t_{tr}$ = 50.6 ns and a stationary intensity of 0.73. In the Bragg (reflection) geometry the corresponding time is $\tau_1$ = 4.3 ns. {E1}{E9}{E20}{E28}{E85}

]]

![Top: $|D_h(z,t)|^2$ at the first-sideband angle after a step onset (TT, averaged over the acoustic phase). Bottom: intensity at the exit surface, $I_1(t)$. Ahead of the wavefront the crystal is unstrained and $D_h$ propagates unchanged; behind it the field is stationary and depends only on depth. Si 440, $S$ = 1.5, $L$ = 296 μm.](none){E1}{E9}{E20}

@pair

## Drive envelope and overshoot

For a drive amplitude ramped linearly over $T_{rise}$, the first sideband exceeds its stationary value only when the final amplitude lies beyond the first maximum of $J_1$ ($S$ = 1.84); otherwise the rise is monotonic. {E15}{E67}

![Overshoot $\Delta I=I_{max}-I_{steady}$ of the first sideband versus final amplitude $S$ and rise time $T_{rise}/t_{tr}$. Reduced model (independent satellites; lines), verified against the full TT solution (symbols) at 12 points and for cases A–C; dashed: stationary value. Laue geometry, $L=\Lambda/2$ (49 μm Si 440); the $L=3\Lambda$ crystal of Secs. 1–4 has not been scanned. A: monotonic rise. B: maximum above the stationary value. C: final $S$ near the first zero of $J_1$.](figures/poster/iqms/f7_overshoot.png){E15}{E67}

## Conclusions and outlook

> **Sideband formation is limited by the acoustic transit time** $t_{tr}=L/v_s$. The formation time $\tau_n=\Lambda/(v_s|J_n(S)|)$, not the acoustic period, sets the switching speed (tens of ns in Si). {E1}{E9}{E67}

- **Thick crystals.** For $L>\Lambda$ the satellite intensities deviate from the Bessel law, which is recovered for $L\ll\Lambda$. {E0}{E44}

- **Drive envelope.** A ramped drive produces an overshoot only for $S$ beyond the first maximum of $J_1$ (1.84) (Sec. 5). {E15}{E67}

- **Outlook.** Time-resolved measurement on Si 440: $S$ = 1.5 corresponds to $u_0$ = 23 pm (strain $5\times10^{-5}$ at 2 GHz). A beam divergence of 10 μrad resolves the satellites (Sec. 1); tracking a single satellite in time requires a divergence below 0.05 μrad, a fraction of the Darwin half-width. {E20}{E73}{E84}{E92}

![Numerics: TT equations integrated with RK4 and validated against an exact Floquet solution for a periodic drive; the two-beam expressions agree with full TT within 6 % for $\Lambda_{ac}<0.3\,\Lambda$.](none){E0}{E19}{E20}{E31}{E42}{E54}{E62}
