# Poster session prep — P2.17, KPS Fall 2026, Jeju, 22 October

Every answer below carries the entry in `lab_notebook.md` that backs it. If a question has no
entry, the honest answer is "not checked" — say that, and write the question down.

Rule for the session: **concede the known part first, then say what is added.** Every strong
question here has a real prior-art or validity component. Conceding it costs nothing and makes
the rest credible.

---

## 1. The opening

**10 seconds.** "A sound wave in a crystal adds satellite peaks to the X-ray rocking curve; the
steady state is known. We simulated how the satellites grow while the sound is still entering the
crystal. In our runs each satellite grows at its own rate."

**30 seconds (Korean, for a first approach).** "음파가 결정 안으로 들어가는 동안 X선 위성 피크가
어떻게 자라는지 시뮬레이션했습니다. 계산해 보니 음파가 지나간 부분이 '그 깊이만큼 두께의
결정'처럼 행동했습니다. 차수 n의 결합이 α|J_n(S)|로 줄어들어서 차수마다 자라는 속도가 다르고,
음향 세기 S를 바꾸면 순서도 바뀝니다. 맞춘 변수는 없습니다. 아직 실험과 비교하지는 않았습니다."

**60 seconds, pointing at panel 2.** "Behind the front, satellite *n* behaves like a plain crystal
of thickness v_s t whose coupling is reduced to α_n = α|J_n(S)|. So the Laue centre intensity is
sin²(πα_n t) and Bragg is tanh²(πα_n t). Four different (S, α, n) fall on these curves without a
fitted parameter. The transit time only limits how long the growth lasts; the growth rate is set
by t_tr/α_n, i.e. by the satellite's own extinction length." {E1}{E9}{E33}

---

## 1b. Basics — easy questions that are easy to get wrong

Answer in this order: definition, physical picture, assumptions, what is measured, limits.
**[F]** marks a computed or looked-up fact with its entry; **[I]** marks interpretation. Say
which one you are giving.

### Q. "What is S?"

- **Definition.** S = h·u₀: the largest phase the lattice displacement adds to the diffracted
  wave. h = 2π/d along the reflection, u₀ the displacement amplitude. It is the modulation index
  of the phase grating e^{iφ}.
- **Picture.** e^{iS sin(…)} = Σₙ Jₙ(S) e^{in(…)} is an exact identity, so S decides how the
  coupling is shared among the orders. S is a phase, not a strain.
- **Assumptions.** Only the part of u along h counts. In symmetric Laue h lies in the surface,
  so the wave travelling into the depth must be shear, polarised along h; a longitudinal wave
  gives h·u = 0. One sinusoid, uniform amplitude behind the front.
- **Measured.** Not directly. In strain terms S = ε₀Λ_ac/d with ε₀ = Ku₀ [F E20]: Si 440,
  30 keV, 0.6 GHz, S = 1.5 is ε₀ = 1.5×10⁻⁵. In an experiment, from τ₂/τ₁ = |J₁/J₂| [F E13].
- **Limits.** The same S at a different frequency is a different strain. The expansion holds at
  any S; the independent-channel picture needs R = Λ_ac/Λ_P ≲ 0.34–0.57 [F E53, E54].

### Q. "What is ν?"

- **Definition.** On this sheet (§6b) ν is the satellite amplitude that first-order theory, linear
  in S, predicts [F E65]. **Not a frequency**; the acoustic frequency is f. (Entry 57 uses ν for a
  frequency in one line. Do not mix them.)
- **Picture.** Roughly the coupling the satellite accumulates over the strained depth the X-rays
  see, ~π|J₁(S)|·ℓ/Λ_P [I, order estimate, E65]. Small ν: a weak, kinematic satellite, and the
  Fourier-weight spectroscopy of the Outlook works. ν ~ 1: the satellite has become its own
  dynamical reflection, which is the rest of the poster.
- **Assumptions.** First-order perturbation of TT. Si 400, symmetric Bragg.
- **Measured.** Not measured; it is a predicted amplitude. What it controls is computed: the
  error of the linear estimator grows as ν², ≲ 4 % for ν ≲ 0.2 [F E65].
- **Limits.** Chalise et al.'s ν ≈ 0.03 is an order estimate, not a TT run of their packet [E65].

### Q. "Extinction length or Pendellösung length — which is your Λ_P?"

- **Definition.** Λ_P is the intensity Pendellösung period in symmetric Laue at the Bragg angle:
  I = sin²(πL/Λ_P), Λ_P = λ cos θ_B/|χ_h| (σ). It is what X0h lists as the Laue extinction
  length (Si 220, 8 keV: 15.21 µm by hand against 15.203 reported) [F E20]. α = L/Λ_P.
- **Picture.** Laue: the depth over which energy swings from D₀ to D_h and back. Bragg, from the
  same TT equations: at η = 0 in a thick crystal the field decays as e^{−πz/Λ_P}, so the
  amplitude 1/e depth is Λ_P/π [I, follows from the poster's equations].
- **Assumptions.** Two beams, symmetric, σ polarisation, no absorption.
- **Measured.** Λ_P from Pendellösung fringes against thickness or energy; the poster uses X0h
  values [F E20].
- **Limits.** Books differ by factors of π and 2 between Pendellösung distance, extinction
  distance and extinction depth. Always say "intensity period, I = sin²(πL/Λ_P)" first. For
  satellite n the length is Λ_P/|Jₙ(S)|; that steady-state form is prior art (Polikarpov) [E29].

### Q. "What is the 'filled depth' v_s·t?"

- **Definition.** How far the acoustic front has travelled since it entered: z = v_s·t, i.e.
  ζ = t̃ = t/t_tr with t_tr = L/v_s. Behind the front the lattice is modulated; ahead, A = 0.
- **Picture.** A modulated layer of thickness v_s·t on top of a perfect crystal. For a step onset
  with the channels independent, satellite n sees a uniform crystal of that thickness with
  coupling α|Jₙ(S)|: sin²(πα_n t̃) in Laue, tanh² in Bragg [F E1, E9].
- **Assumptions (all in the model).** The sound enters at the X-ray entrance face as a plane
  front parallel to the surface. No dispersion, no attenuation, and no wave reflected back from
  the far face. Quasi-static: the X-ray transit is 0.2 % of an acoustic period [F E62].
- **Measured.** Time, not depth. v_s·t follows from the timing with a known v_s (shear
  5846 m/s from a textbook c₄₄, not measured) [F E20]. The observable is Iₙ(t).
- **Limits.** After t_tr the crystal is full. A real crystal then gets an acoustic echo from the
  far face, which the model does not have. A gradual front replaces the step law by Θₙ [E28].

### Q. "Isn't the satellite intensity just |Jₙ(S)|²?" (why Jₙ is not the time-resolved intensity)

- **Definition.** Jₙ(S) is a Fourier coefficient of e^{iφ}: the amplitude with which channel n
  couples D₀ and D_h in the filled crystal. It is a coupling, not an intensity.
- **Picture.** For weak coupling, sin²(πα_n t̃) ≈ (πα|Jₙ|t̃)² ∝ |Jₙ|²: the familiar
  Bessel-squared ladder is the kinematic limit of the poster's own formula [I, algebra]. In the
  dynamical regime the intensity oscillates (Laue) or saturates (Bragg), and Jₙ sets the rate:
  τₙ = Λ_P/(v_s|Jₙ(S)|) [F E6].
- **Assumptions.** Step onset, independent channels.
- **Measured.** Iₙ(t) at η = nq. Jₙ enters through the periods, hence τ₂/τ₁ = |J₁/J₂| [F E13].
- **Limits.** A larger |Jₙ| can give a dimmer satellite at a given time (sin² past its maximum);
  formation order at S = 3 is n = 2, 1, 3 [F E1]. At a Bessel zero the slow clock stops [F E53].
  With a finite ramp Θₙ replaces Jₙ, and the overshoot can be large even where the final |Jₙ|
  is small [F E67].

### Q. "Laue or Bragg — what differs?"

- **Definition.** Laue: the diffracted beam leaves through the far face; both beams travel
  forward, so it is an initial-value problem integrated from the entrance. Bragg: the diffracted
  beam leaves through the entrance face; a two-point boundary problem, solved as a Riccati
  equation for R = D_h/D₀ integrated backward from the far face.
- **Picture.** Laue: energy swings through the whole thickness, sin². Bragg: total reflection
  builds within about Λ_P/π of the surface, tanh², and saturates.
- **Assumptions.** Symmetric reflections, no absorption, σ.
- **Measured.** Laue: the diffracted beam behind the crystal, so the crystal must transmit
  (Si 440 at 17–30 keV: 0.78–0.92) [F E20]. Bragg: the reflectivity.
- **Limits / what changes for formation.** Bragg formation ends at ≈ 0.95 t_tr/α_n, capped at
  t_tr; the first guess 1/α was wrong [F E9]. The ramp law Θₙ holds equally in both (error
  ≤ 0.03) [F E28]. Polarisation of the sound: symmetric Laue needs shear (above); in symmetric
  Bragg h is along the normal, so a longitudinal wave works [I].

### Q. "And the phase wall — is that new?"

**No, and say so first.** The acoustic phase wall is the stacking-fault contrast of Authier &
Simon (1968), satellite by satellite, with fault phase δ = n·dφ. Manukyan (2014) eq. 11 is the
same amplitude at η = 0. For n = 1, 2 the 1968 formula reproduces our TT integrals within
1–3 % [F E56]. The "new mechanism" claim was withdrawn in Entry 56.

What differs, as fact and not as a novelty claim: δ depends on n (a crystallographic fault has
one δ for all satellites), and position and phase are set by the drive. Whether that enables a
new measurement is not shown [E56]. It is not on the poster; do not raise it.

---

## 2. Prior art — the questions that decide whether you are taken seriously

### Q. "Pendellösung in the time domain is not new. DeCamp did this in 2001."

**Concede, precisely.** Yes — DeCamp, Reis & Bucksbaum, *Nature* **413**, 825 (2001), read in
full: Ge (001), 280 µm, asymmetric 202 Laue at 10 keV, a **single short strain pulse** acting as
a moving interface between two perfect crystals, switching the **main** reflection. Their own
statement is that the pulse must travel about a quarter of a Pendellösung depth. {E21}

**Then.** "No satellites, no periodic drive, no Bessel functions in that work. Our n = 0 law is
the CW-grating version of their picture and we cite it on the poster. The satellite results sit
outside it: every order n, both geometries, one law." {E21}{E7}

### Q. "The satellite extinction length ~ Λ/|J_n| is in the ultrasonic-superlattice literature."

**Concede fully.** Correct — Polikarpov, *phys. stat. sol. (b)* **143** (1987) and **149** (1988),
read in full; Iolin & Entin; Zolotoyabko and co-workers. That is the steady-state ingredient and
we attribute it. {E29}{E50}{E7}

**Then.** "What we add is the transient: the time-domain collapse onto the static thickness
curves, formation ordered by the Bessel ladder, the accumulated-coupling law for a finite ramp,
and the path memory." {E21}

### Q. "Zolotoyabko already did stroboscopic X-ray diffraction from SAWs."

Standing SAW at 0.58 GHz in LiNbO₃, satellites modulated at 2f — a phase-locked **periodic steady
state**, not a formation transient. Different object. {E21}

### Q. "Why not do this with a surface acoustic wave? That is how everyone does it."

Expect this one. Say the geometry first, then the number. {E63}

**Geometry.** "A SAW's wavevector lies *in* the surface and its amplitude decays into the depth.
Ours is a bulk wave travelling *into* the depth, uniform behind the front. So what grows with time
is different: for us the modulated depth, for a SAW the modulated lateral extent. Our solver is
one-dimensional in depth and cannot represent an in-plane wavevector at all — which is why that
literature talks about sagittal diffraction."

**The number that settles it.** "A Rayleigh wave's skin is 0.30–0.41 Λ_ac, so the fraction of the
extinction depth it modulates is 0.30–0.41 R — independent of frequency and material. Resolving
the channels needs R ≤ 0.34–0.57, so the modulated fraction is capped at 10–17 %. A SAW cannot
fill the extinction depth and keep its satellites resolved: resolving wants a short acoustic
wavelength, filling wants a long one."

**The physical point, if they push.** "The skin depth is set by the frequency and does not grow.
Once the surface wavefront has passed a point, the profile under it is static. **A SAW has no
depth-filling transient** — that is the whole mechanism here. A SAW does have a transient, the
lateral filling of the X-ray footprint, ~20 ns for a 100 µm footprint. Same order as our t_tr,
but it is an inhomogeneously illuminated surface, not a depth-graded crystal."

**What does carry over.** "The accumulated-coupling law is a statement about the depth *profile*,
not about the front. I checked it on a static exponential skin: it holds to ≤ 1.1×10⁻² absolute
for skins thinner than 0.1 L, which is the whole SAW regime. And a skin of depth d reads like a
filled depth of 1.0–3.1 d depending on S — above S ≈ 1.8 the decaying tail sweeps through the
maximum of J₁, so depth where the amplitude has *fallen* couples more strongly than the surface."

**Close by naming your own geometry.** "So the experiment this predicts is a bulk wave from a
transducer, launched along the depth, and shear-polarised — in symmetric Laue a longitudinal wave
along the normal gives h·u = 0." {E6}{E20}

Never say a SAW experiment is uninteresting. It measures a different quantity.

### Q. "What about Sondhauss & Wark's time-dependent dynamical diffraction theory?"

**Read in full (Acta Cryst. A59, 7–13). It is the Outlook panel's comparison, so point at it.** {E64}

**Concede.** "Their Sec. 4 is the first-order perturbative solution of TT for a phonon. The
linearisation is theirs, and so is the idea of fitting mode contents with a linear solution.
I don't claim either."

**Then, with the figure.** "Their solution uses a plane-wave ansatz with constant perfect-crystal
amplitudes. They themselves say it is unsafe when the satellite is within about one rocking-curve
width of the main peak (their Fig. 4). I evaluated their eq. 29 in our variables. Against full TT
it is 2 % off at 20 Darwin half-widths, 22 % at 5, a factor 3 at 1 and a factor 8 at 0.5. Keeping
the Bloch-wave depth dependence turns it into our closed form, which holds to 1 % everywhere,
inside the Darwin plateau included. That regime is exactly where a Fourier-weight spectrum is
biased." {E64}

### Q. "What is new in the Outlook panel, then?"

"Three things, none of them in the 2003 paper or in Chalise et al. 2026:
1. The Fourier weight of R(t) used as the spectral estimator, written as the strain spectrum times
   a crystal transfer function H(ω).
2. H collapses on one curve in phonon frequency over the Darwin half-width, and depends strongly on
   absorption, κ/2πα = χ_i0/|χ_h|.
3. A first-order form that is valid inside the Darwin width, where the plane-wave one fails."
{E59}{E64}

If they ask for a real crystal, see the Si 400 numbers in §6b. {E65}

### Q. "So what is actually yours?"

Say exactly these five, nothing more: {E21}

1. transient formation of satellites behind a travelling front;
2. the time-domain collapse onto the static thickness curves, no fit parameter;
3. formation order set by the Bessel ladder and reorderable with S;
4. the accumulated-coupling law Θ_n for a finite ramp;
5. the period-ratio calibration of S.

Add: "The search was web-level, not a database search. I would like to know if you have seen any
of these." — turn it into an ask.

---

## 3. The model — the sharpest technical question

### Q. "Where is the time derivative of the X-ray field? This is not time-dependent diffraction."

**Correct, and it is deliberate.** The deformation is frozen at each instant and the two-beam
Takagi–Taupin system is solved in depth. The number: in the poster's window the X-ray crosses the
crystal in 0.99 ps, which is **0.2 % of a 500 ps acoustic period**; β = 2πfL/c ≤ 1.2×10⁻² over
Si 440, 17–30 keV, L = 163–296 µm, 0.6–2 GHz. The lattice is static while the field is inside.
{E62}

**What it does not cover, said before they say it.** The crystal's own field settling time — the
Shvyd'ko–Lindberg regime — is a separate question, and this model does not address it. Any
dependence on v_s beyond t_tr is outside these maps by construction. {E21}{E62}

### Q. "Are these Floquet sidebands / Stokes and anti-Stokes?"

"The channels sit at η = nq in the rocking variable. There is no photon-energy axis in this
calculation, so I don't label them Stokes / anti-Stokes — that needs the frequency-resolved
treatment." Do not improvise past this. {E0}

### Q. "Absorption?"

Simulated, not estimated: `core.solve_laue` takes a complex α. The oscillation contrast goes as
1/cosh(μLκ|J_n|t). Si 220 at 8 keV with L = 100 µm gives μL ≈ 1.4 and contrast ≈ 0.78 at t = t_tr.
The recommended window is better — Si 440 at 17–30 keV has α″/α′ < 0.4 % and contrast ≈ 1.00.
Design rule: keep μLκ|J_n| ≲ 1. {E11}{E20}

### Q. "How well does the law hold, and where does it break?"

Panel 4 is that map, and the limit is **R = Λ_ac/Λ_P**, not α: {E26}{E53}{E54}{E25}

- accuracy ≈ 0.9 R, independent of how many turns the clock makes — f tunes accuracy, L and S
  tune the clock;
- with the exact acoustic-phase average, channels stay independent to better than 5 % up to
  R = 0.34–0.57 depending on S;
- the law fails when |J_n| α_ac ≲ 0.5 — at a Bessel zero the slow clock stops and only an
  acoustic-period ripple ~ (α/α_ac)² is left;
- near R ~ 1 a Bessel-dark order reappears through a third-order coupling πα(R/2)²C_n(S), with a
  renormalised zero. {E45}{E52}

### Q. "Is it a special-point artefact — integer α_ac, nice α?"

Checked on random conditions, not a grid. {E19}

### Q. "How is the solver verified?"

54 tests. Analytic limits to 10⁻⁹ (whole rocking curve against the closed form, Bragg tanh²(πα),
RK4 fourth-order convergence measured at 3.98–4.00). An independent exact Floquet solver agrees to
3×10⁻⁷; unitarity holds to 3×10⁻⁷. {E0}{E42}

---

## 4. Numbers a visitor may challenge

| They ask | Answer | Entry |
|---|---|---|
| Why 0.95 t_tr/α_n? | 99 % formation of tanh², 0.953/α_n, capped at t_tr — it cannot exceed the transit | E9 |
| Why does S reorder the channels? | t\* / t_tr = 1/(2α\|J_n(S)\|); at S = 3 that is n = 2, then 1, then 3 | E1 |
| The dark point — is the satellite gone? | Centre drops to 0.1–0.2 %, but ~52 % of the integrated satellite is still there, in two side lobes; lobes collapse as (η−nq)t = G(α_n t) | E23 |
| Centre vs integrated intensity? | Same period, different phase and damping: the integral leads by ~1/8 period and damps as J₀ | E23 |
| Is the transient-only satellite just a slow amplitude sweep? | See §5 — concede most of it | E34 |
| 1–3 % on the phase walls? | That 1–3 % is the agreement with the 1968 plane-wave stacking-fault formula, δ = n·dφ (Authier & Simon; Manukyan 2014): known physics, not ours (§1b) | E56 |

---

## 5. The one claim to state carefully

**"Transient-only satellite: an order forbidden at the final amplitude is the brightest during
formation."** The honest framing is already written down — use it verbatim. {E34}

- For a **slow** ramp (T ≫ t_tr) this is the steady Bessel ladder sampled on the way to a zero.
  Any amplitude sweep shows n = 1 at intermediate S. Say this first.
- What the transient adds: (i) the t_tr memory — the satellite reports the drive t_tr/2 late and
  smoothed; (ii) the fast-ramp regime T ≲ t_tr, where it is a flash set by the ramp profile
  *inside* the crystal; (iii) a step onset gives **exactly zero** at all times, so the peak is a
  signature of the amplitude gradient inside the crystal, not of the final state.
- Robustness: > 30:1 transient-to-final contrast survives a 5 % error in S and 10 % acoustic loss
  across the crystal.

---

## 6. Experiment — for the person who might actually do it

Verified X-ray constants from X0h; c44 and the transducer are still estimates. {E20}

| | Si 440, 17.48 keV | Si 440, 30 keV |
|---|---|---|
| Λ_P | 54.3 µm | 98.8 µm |
| L = 3Λ_P | 163 µm | 296 µm |
| t_tr | 27.9 ns | 50.7 ns |
| τ₁ | 16.7 ns | 30.3 ns |
| f_min (r = 0.1) | 1.1 GHz | 0.6 GHz |
| strain | 2.7×10⁻⁵ | 1.5×10⁻⁵ |
| transmission | 0.78 | 0.92 |

Points to make: tens of ns is comfortable against ~100 ps storage-ring bunches; higher energy and
higher order improve **every** axis at once (lower frequency, lower strain, less absorption).

**"How do I know S in the experiment?"** From the ratio of the two temporal periods,
τ₂/τ₁ = |J₁/J₂| — independent of gain and of thickness, ~1 % recovered in a simulated measurement
with 3 % noise. The design rule is α|J₂(S)| ≥ 0.5; the S = 1 case failed at +9.4 % precisely
because α₂ = 0.35 and the n = 2 trace never completed half an oscillation. {E13}

### 6b. The Outlook in a real crystal: Si 400, symmetric Bragg (Chalise et al.'s case) {E65}

| | 8 keV | 17.48 keV |
|---|---|---|
| f_D = v_L/Λ (one Darwin half-width) | 0.74 GHz | 0.73 GHz |
| absorption g = χ_i0/\|χ_h\| | 0.046 | 0.010 |
| crystal factor H at 20 GHz | 0.93 | 0.48 |
| H(20 GHz)/H(100 GHz) | 0.93 | **0.51** |

- "At 17 keV a peak-normalised Fourier-weight spectrum under-reads 20 GHz by a factor 2, even
  after the kinematic correction. The cause is weak absorption: the tail extinction competes with
  absorption out to tens of Darwin widths."
- **If asked whether this explains their Fig. 2.** "Same sign, same order of magnitude. Their
  energy and normalisation are not stated, so I don't claim a quantitative match."
- **Linearity limit, if asked.** "The estimator is linear only while the satellite's own amplitude
  ν ≲ 0.2. A few-cycle packet is far below that (ν ≈ 0.03). A long GHz train is far above it, and
  that is exactly where the satellite forms dynamically — the rest of the poster."

---

## 7. Negative results — volunteer these, they buy credibility

- The satellite **peak shift** is kinematic interference, not a dynamical shift. {E3}
- The transient **±n asymmetry** is a first-acoustic-wavelength effect ∝ 1/α_ac, not dynamical.
  {E8}
- Same strain **up vs down** a pulse: mostly a negative result for the whole rocking curve. {E36}
- **Chirped** acoustic waves give a Landau–Zener plateau, no focusing. {E38}
- The session-1 conclusion "no additional timescale" was **wrong** — t_tr/α_n is one. Saying this
  out loud is a strength. {E12}

---

## 8. Do not say

| Never | Say instead |
|---|---|
| "time-dependent Takagi–Taupin" | "Takagi–Taupin with a travelling deformation, solved at each instant" |
| "Stokes / anti-Stokes", "Floquet sidebands" (energy sense) | "channels at η = nq"; no photon-energy axis here |
| "we derived the first-order solution" | "the linearisation is Sondhauss & Wark 2003; ours keeps the Bloch-wave depth dependence and holds inside the Darwin width" |
| "temporal Pendellösung is new" | "the organising principle, from DeCamp 2001, extended to every order" |
| "satellite extinction length ~ Λ/\|J_n\| is ours" | "that is the steady-state ingredient, from Polikarpov and the superlattice literature" |
| "the phase wall is a new mechanism" | "that is the 1968 stacking-fault contrast with δ = n·dφ; withdrawn in Entry 56" |
| "the satellite intensity is Jₙ(S)²" | "Jₙ is the coupling; Jₙ² is only the kinematic limit of sin²(πα_n t̃)" |
| ν for a frequency | f for the acoustic frequency; ν here is the linear satellite amplitude |
| "S is the strain" | "S = h·u₀ is a phase; strain = S·d/Λ_ac" |
| any number not on this sheet | "I don't have that checked — can I take your email?" |

---

## 9. Pocket card

```
S            h u0 (a phase);  strain = S d / Lambda_ac;  S = 1.5 <-> 1.5e-5 at Si 440, 30 keV, 0.6 GHz
Lambda_P     intensity period, Laue I = sin^2(pi L / Lambda_P) = X0h "extinction length"
             Bragg amplitude depth Lambda_P / pi;  satellite n: Lambda_P / |J_n|  (prior art)
filled depth v_s t;  model: no echo from the far face, quasi-static (transit 0.2 % of a period)
J_n          coupling, not intensity;  J_n^2 only in the kinematic limit
phase wall   Authier & Simon 1968 stacking fault, delta = n dphi -> NOT new (E56)
clock        t_tr / alpha_n,   alpha_n = alpha |J_n(S)|
Laue         sin^2(pi alpha_n t)        Bragg  tanh^2(pi alpha_n t)
order        t*/t_tr = 1 / (2 alpha |J_n(S)|)      S = 3 -> n = 2, 1, 3
dark point   centre 0.1-0.2 %, integral still 52 %
validity     R = Lambda_ac / Lambda_P <= 0.34-0.57;  accuracy ~ 0.9 R
verified     1e-9 analytic, 3e-7 Floquet, 54 tests
experiment   Si 440, 17-30 keV, 1-2 GHz, tau_1 = 17-30 ns, strain ~3e-5
calibrate S  tau_2 / tau_1 = |J_1 / J_2|,  needs alpha |J_2| >= 0.5
concede      DeCamp 2001 (main line, pulse);  Polikarpov / Entin / Zolotoyabko (steady state)
```
