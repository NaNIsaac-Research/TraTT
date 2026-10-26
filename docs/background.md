# Background

The physics behind TraTT, the question it works on and the numbers it reduces to. The results are in the [README](../README.md#results).

## Background

**X-ray diffraction from a crystal.** An X-ray beam hitting a crystal is reflected strongly only
near one angle, the Bragg angle, where the reflections from successive atomic planes add up in
phase. Scanning the crystal angle through that point and recording the reflected intensity gives
the *rocking curve* I(η), where η is the (dimensionless) angular offset from the Bragg angle.

**Dynamical diffraction.** In a thin or imperfect crystal each X-ray is scattered at most once
(kinematic theory). In a thick, perfect crystal such as a silicon wafer the diffracted beam is
scattered back into the forward direction, and the two beams trade intensity back and forth as
they go deeper. The depth for one full exchange is the *Pendellösung length* Λ<sub>P</sub>,
typically 15–100 µm in silicon. The **Takagi–Taupin (TT) equations** describe this: two coupled
differential equations, along the depth, for the amplitude of the forward beam D<sub>0</sub> and
of the diffracted beam D<sub>h</sub>. They also allow the lattice to be locally displaced, which
is what a sound wave does.

**Two geometries.** In *Laue* (transmission) geometry the diffracted beam leaves through the back
surface, and the whole thickness contributes. In *Bragg* (reflection) geometry it leaves through
the front surface, and mainly the top ~Λ<sub>P</sub> contributes.

**Acoustic satellites.** A sound wave (here a GHz acoustic wave of wavelength Λ<sub>ac</sub>)
shifts the atomic planes periodically. For the X-rays this is a periodic phase modulation, so the
rocking curve gains extra peaks, *satellites*, on both sides of the main peak, spaced by the
acoustic wave vector. Satellite n carries the weight J<sub>n</sub>(S), a Bessel function of the
modulation strength S = h·u<sub>0</sub> (reciprocal lattice vector times displacement amplitude).
This steady state, with the whole crystal already vibrating, has been known for decades.

## The question

The sound wave is launched at one surface at t = 0 and travels at speed v<sub>s</sub>. At time t
only the depth v<sub>s</sub>t is vibrating; the rest of the crystal is still undisturbed. After
the transit time t<sub>tr</sub> = L/v<sub>s</sub> (L = crystal thickness) the wave fills the
crystal and the known steady state applies. **How do the satellites grow during
0 < t < t<sub>tr</sub>?** That is the question this repository works on.

## What the code computes

For each time t the solver freezes the displacement profile (sound present down to depth
v<sub>s</sub>t, nothing below), solves the TT equations through the crystal for every η, and
stores the rocking curve. Stacking these gives a map I(η, t). Every result in the README is an analysis of
such maps.

Freezing the lattice is safe here: the X-rays cross the crystal in about 1 ps, while one acoustic
period is about 500 ps, so one crossing takes about 0.2 % of a period even in the least
favourable proposed case (Si 440, 30 keV, 2 GHz, L = 296 µm; notebook Entry 62).

The problem reduces to a few dimensionless numbers:

| symbol | meaning |
|---|---|
| α = L/Λ<sub>P</sub> | crystal thickness in units of the Pendellösung length |
| S = h·u<sub>0</sub> | strength of the acoustic modulation |
| R = Λ<sub>ac</sub>/Λ<sub>P</sub> | acoustic wavelength in units of the Pendellösung length |
| t̃ = t/t<sub>tr</sub> | time in units of the transit time (t̃ = 1: the sound reaches the back surface) |

Main simplifications: two beams only, symmetric geometry, a plane monochromatic X-ray wave, no
absorption (an optional uniform absorption exists for Bragg geometry), and the sound acts only as
a displacement of the lattice. Details in [DESIGN.md](../DESIGN.md).

A realistic case (notebook Entry 20): the Si 440 reflection at 17–30 keV, a crystal 150–300 µm
thick, a 1–2 GHz shear wave with strain ~2–3×10⁻⁵. The transit time is then 20–50 ns, long
compared with a synchrotron X-ray pulse (~100 ps), so the growth could in principle be resolved.

