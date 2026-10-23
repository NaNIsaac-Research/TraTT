# Equations

The model TraTT solves, written out from the solver (`src/tratt/core.py`, `src/tratt/drive.py`).
The assumptions behind it and the analytic limits the tests assert are in
[DESIGN.md](../DESIGN.md); this page is the same model in one place, with the equations typeset.

## Variables

Everything is dimensionless.

| symbol | meaning | in the code |
|---|---|---|
| $\zeta = z/L \in [0, 1]$ | depth in units of the crystal thickness $L$ | `zeta` |
| $\tilde t = t / t_\mathrm{tr}$, $t_\mathrm{tr} = L / v_s$ | time in units of the acoustic transit time | `t` |
| $\alpha = L / \Lambda_P$ | thickness in Pendellösung lengths | `alpha` |
| $\eta$ | deviation parameter (wavevector mismatch from the Bragg condition) multiplied by $L$ | `eta` |
| $S = h \cdot u_0$ | acoustic modulation strength | `Drive.S` |
| $\alpha_\mathrm{ac} = L / \Lambda_\mathrm{ac}$ | thickness in acoustic wavelengths | `Drive.alpha_ac` |
| $q = w = 2\pi\alpha_\mathrm{ac}$ | acoustic phase across the slab, and per transit | `Drive.q`, `Drive.w` |

The README's $R = \Lambda_\mathrm{ac} / \Lambda_P$ is $\alpha / \alpha_\mathrm{ac}$.

The forward susceptibility $\chi_0$ does not appear in the equations below. In Laue geometry it
enters both beams with the same coefficient and is removed by a common phase substitution. In
Bragg geometry it enters the two beams with opposite signs, so no common phase removes it: its
real part is absorbed into $\eta$ and its imaginary part is the absorption $\kappa$ (below). In
both, $\eta = 0$ is the refraction-corrected Bragg angle.

## Laue geometry

Both beams travel into the crystal. With $D_0(0) = 1$ and $D_h(0) = 0$ at the entrance face, the
two-beam Takagi–Taupin equations are integrated to the exit face by fixed-step RK4:

$$
\frac{dD_0}{d\zeta} = i\pi\alpha\, e^{+i\varphi(\zeta;\tilde t)}\, D_h, \qquad
\frac{dD_h}{d\zeta} = i\pi\alpha\, e^{-i\varphi(\zeta;\tilde t)}\, D_0 + i\eta\, D_h .
$$

The diffracted intensity is $I = |D_h(1)|^2$ (`rocking(..., geometry="laue")`). A complex
$\alpha$ adds the anomalous (Borrmann) part of absorption.

## Bragg geometry

The diffracted beam travels back to the entrance face, so the boundary conditions sit on opposite
faces ($D_0(0) = 1$, $D_h(1) = 0$). The solver integrates the ratio $R = D_h / D_0$ backward from
$R(1) = 0$, which turns the two-point problem into an initial-value problem:

$$
\frac{dR}{d\zeta} = -i\pi\alpha\, e^{-i\varphi} - i\eta\, R - i\pi\alpha\, e^{+i\varphi}\, R^2 .
$$

The reflectivity is $I = |R(0)|^2$ (`rocking(..., geometry="bragg")`). Normal absorption, which does
not gauge out in this geometry, enters as $\eta \to \eta + i\kappa$ (`solve_bragg(..., kappa=)`).

## The acoustic drive

The sound wave enters at the surface at $\tilde t = 0$. The lattice is frozen at each time (the
X-rays cross the crystal much faster than one acoustic period), and the phase it imposes is

$$
\varphi(\zeta; \tilde t) = S\, A(\tilde t - \zeta)\, \sin(q\zeta - w\tilde t) .
$$

$A$ is a causal envelope of the retarded time $s = \tilde t - \zeta$: a step ($A = 0$ for
$s < 0$, $1$ after) or, with `Drive(rise=r)`, the smoothstep $3x^2 - 2x^3$ with
$x = \min(\max(s/r, 0), 1)$. $A(s < 0) = 0$ is the wavefront: at time $\tilde t$ only the depth
$\zeta < \tilde t$ is vibrating. For a non-dispersive wave $\Omega = K v_s$, so $w = q$, and the
phase is a function of the retarded time alone, $\varphi = -S\, A(s) \sin(qs)$.

## Satellite channels

The channel positions and weights come from the kinematic limit (weak diffraction,
$\alpha \ll 1$), where the Laue amplitude is a single integral over depth,

$$
D_h(1) = i\pi\alpha \int_0^1 e^{-i\varphi(\zeta)}\, e^{i\eta(1 - \zeta)}\, d\zeta .
$$

Where the crystal is filled ($A = 1$; with the step envelope, everywhere once $\tilde t \ge 1$),
the phase factor expands in Bessel functions,

$$
e^{-i\varphi} = \sum_n (-1)^n J_n(S)\, e^{in(q\zeta - q\tilde t)},
$$

and term $n$ of the integral peaks at $\eta_n = nq$ (`Drive.eta_channel(n)`): satellite $n$ has
amplitude $(-1)^n J_n(S)$ and intensity proportional to $J_n(S)^2$. The positions are analytic;
nothing is fitted. For integer $\alpha_\mathrm{ac}$ the response of one channel vanishes at the
centres of the others. Outside the kinematic limit the intensity ratios no longer follow
$J_n(S)^2$; the full equations above give them.

## Limits the tests assert

- Laue, real $\alpha$, no sound, $\eta = 0$: $|D_h(1)|^2 = \sin^2(\pi\alpha)$.
- Laue, real $\alpha$ and $\eta$, with or without sound: $|D_0|^2 + |D_h|^2 = 1$ at the exit face.
- Bragg, real $\alpha$, with sound: $|R|^2 \le 1$.
- Bragg, no sound, $\alpha = 4$: $|R|^2 > 0.99$ for $|\eta| \le 0.6 \cdot 2\pi\alpha$ and
  $|R|^2 < 0.5$ for $|\eta| \ge 1.6 \cdot 2\pi\alpha$, the total-reflection plateau of a thick
  crystal, whose edge at $|\eta| = 2\pi\alpha$ is soft at this thickness.
- Step envelope, $\tilde t \ge 1$: $\varphi$ has its final form, so $I(\eta, \tilde t)$ is
  periodic in $\tilde t$ with period $2\pi/w$.

## What the model leaves out

Two beams only, symmetric geometry, a plane monochromatic X-ray wave, a fixed polarization factor,
and a sound wave that acts only as a displacement of the lattice (no change of $\chi_h$, no
vibrational Debye–Waller factor). Absorption is off unless $\alpha$ is made complex (Laue) or
$\kappa > 0$ (Bragg). The full list, with what each assumption discards, is in
[DESIGN.md](../DESIGN.md).
