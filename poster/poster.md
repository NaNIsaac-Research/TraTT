---
title: Transient Formation Dynamics of Acoustic Bragg Satellites // in Dynamical X-ray Diffraction
authors: **Isaac Yong**¹, Ouyoung Kwon¹, Hyunjung Kim¹*
affiliation: ¹Center for Ultrafast Phase Transformation, Department of Physics, Sogang University, Seoul, Korea  ·  *corresponding author
footer: P2.17 · 2026 KPS Fall Meeting, Jeju, October 22, 2026 · This work was supported by the National Research Foundation of Korea grant RS-2021-NR059920.
---

<!--
Printed text source; build with python poster/build.py.
Reading order: two full-width background panels, then left and right simulation panels.
Notebook tags retain the evidence; detailed derivations stay in the notebook.
-->

@wide

## Introduction: sound makes a moving diffraction grating

**Why this matters.** Time-resolved X-ray diffraction can probe sound travelling inside a crystal. To interpret the changing signal, we need to understand how the diffraction pattern forms while the sound enters. {E0}{E7}

**Physical picture.** A crystal diffracts X-rays near its Bragg angle. A sound wave periodically displaces its atomic planes, adding a moving grating to the crystal. This produces extra diffraction peaks, called **acoustic satellites**, beside the main peak. {E0}{E7}

**Setup.** A transducer launches sound at one surface. The front moves at speed $v_s$ through thickness $L$. At each time, we calculate the diffracted intensity while scanning the X-ray angle: this is the **rocking curve**. {E0}{E62}

![Sound has reached only part of the crystal. The curve at right is the calculated diffraction pattern at that instant.](figures/poster/f0_scheme.png){E0}

@wide

## Background: what the established theory tells us

**Steady state.** Once a constant-amplitude sound wave fills the crystal, its acoustic-period-averaged diffraction pattern is stationary. During entry, only the depth $v_s t$ is vibrating. The transit time is $t_{tr}=L/v_s$. {E0}{E7}{E42}{E53}

**Why Bessel functions?** A sinusoidal displacement changes the X-ray phase. Splitting that phase modulation into diffraction orders gives Bessel weights $J_n(S)$: $n$ labels the satellite and $S=h u_0$ measures displacement amplitude ($h$: diffraction-vector component). They describe coupling; repeated scattering also determines intensity. {E0}{E7}{E42}

**Pendellösung.** In transmission (Laue geometry), the forward and diffracted beams exchange intensity with depth, repeating over a length $\Lambda_P$. Increasing the vibrating depth can therefore produce oscillations rather than continuous peak growth. {E1}{E9}

![Bessel weights for a sinusoidal displacement. Changing amplitude changes which satellite couples most strongly. These weights are not the full diffraction intensities.](figures/poster/f6_background.png){E0}{E7}{E42}

> **Our question:** how do the satellites form before the sound fills the crystal, and how does the way we launch sound change that process? {E0}{E28}{E33}

## Simulation 1: watch the satellites form

We solve the two-beam Takagi–Taupin equations for each lattice snapshot. X-rays cross much faster than sound moves. Repeating this calculation gives the time evolution of the rocking curve. {E0}{E62}

For a sudden turn-on, the vibrating depth grows as $v_s t$. Each satellite has its own time scale: $\tau_n=\Lambda_P/(v_s\left|J_n(S)\right|)$. It can rise and fall in Laue geometry, or approach saturation in reflection (Bragg geometry). {E1}{E9}{E33}

![After rescaling time, different amplitudes and satellite orders follow the same curves. Points: full simulation; lines: prediction, with no fitted parameter. $\alpha=L/\Lambda_P$, $\alpha_n=\alpha\left|J_n(S)\right|$, $\tilde t=t/t_{tr}$.](figures/poster/f1_collapse.png){E1}{E9}

> **Compared with steady state:** final peak heights do not show when each satellite forms, or whether it passes through a maximum on the way. {E1}{E9}{E33}


## What the simulations show

Bessel weights set formation times. Amplitude and rise time control overshoot: a weak final satellite can be bright during turn-on. {E1}{E9}{E28}{E67}

Calculation only: symmetric, non-absorbing, two-beam model; the simple formation law assumes well-separated satellites. {E0}{E53}{E54}

@column

## Simulation 2: where is overshoot strongest?

The **envelope** controls turn-on: amplitude rises linearly from zero to $S$ over $T_{rise}$, then stays constant. We scan amplitude and rise time for the first Laue satellite at $L/\Lambda_P=0.5$. {E67}

**Overshoot** means the transient intensity exceeds its final steady value. Colour shows $\Delta I=I_{max}-I_{steady}$, in units of incident intensity. A difference remains meaningful even when the final satellite is nearly dark. {E67}

![Map: 11,211 conditions from the independent-satellite approximation. A–C mark the traces below: lines, approximation; dots, full TT; dashed, steady state. Intensities are carrier-phase averaged at the satellite centre; $\Lambda_{ac}/\Lambda_P=0.0125$. B peaks at 1.69 times its final intensity.](figures/poster/f7_overshoot.png){E67}

> **Why the bright region?** During turn-on, the sound passes through amplitudes with stronger Bessel coupling than at its final value. The rise time controls how much of the crystal contains those amplitudes together. {E15}{E67}
