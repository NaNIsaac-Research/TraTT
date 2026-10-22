# Poster session handoff (2026-10-19)

Status: **paused, awaiting user review of draft 1.** Do not continue the rewrite
until the user explicitly resumes it.

## Repository state

- Branch `main`, HEAD `892696e`. Three local commits are not on GitHub:
  `7702c07` (E67 map + audit), `cdbf8c1` (poster overshoot panel + QR),
  `892696e` (Entry 67 audit summary). The user has not approved a push.
- Uncommitted (draft 1, not approved): `poster/poster.md`, `poster/build.py`.
- Untracked and intentionally not committed: `AGENTS.md`, `HANDOFF.md` and
  `notes/tasks/` contain agent-coordination text, which the repository rules keep
  out of commits. `p.out` is a cProfile dump; the user has not decided
  whether to delete it.
- Build outputs: `poster/out/poster.pdf` (A0) and `poster/out/poster.png`
  (last built at 150 dpi). `figures/poster/poster_preview.jpg` (README) has
  **not** been refreshed for draft 1.
- Herdr: worker `tratt-worker` (pane `w2:p5`) is idle with no task. Its last
  task produced `notes/tasks/poster_facts.md`. The user told us not to rerun
  tests or calculations and not to have the worker do so.

## Goal and approved narrative

The user has given the final criterion, and their advisor agrees with it.
The poster explains what was done: background, the question, theory and
numerical method, the computed results, and the limits. It must not oversell
the results. Seven questions to answer: why sound creates satellites; the role
of the Bessel functions in steady state; why the entry transient needs its own
calculation; how the TT equations were set up and solved; what was computed;
what was observed in formation times and overshoot; scope and limits.

Approved flow: full-width Background & Question, then Theory & Numerical Method,
then Results, then Conclusion. The user cares more about the logical flow than
about the panel count.

## Figure selection (approved by user)

- Keep f0 (scheme), f6 (Bessel weights), f1 (formation collapse), f7 (overshoot map).
- f3: optional. Use a small representative trace if space allows. Draft 1
  omits it for lack of space.
- Exclude f2 (line shape) and f5 (phonon-spectrum outlook).
- f4 shows the validity of the independent-satellite approximation, **not**
  solver validation. Never put it in the checks panel. Draft 1 explains the
  validity in Result 1 text only.
- One short line for the experiment proposal below the conclusion, marked
  untested. Drop it if space runs out.

## Draft 1 layout (poster/poster.md)

- Wide **Background**: text 45 % left; f0 and f6 in one row on the right.
- Left column: **Theory and numerical method** (1 TT equations, 2 phase field
  phi = S A(t~-zeta) sin(q zeta - q t~), 3 Laue IVP, 4 Bragg Riccati
  R = Dh/D0 with R(1)=0 integrated backward, 5 RK4 with the step rule,
  6 quasi-static at 0.2 % of a period, plus a one-line procedure band). Then
  **Result 1** (sin^2/tanh^2 law, tau_n, f1, validity).
- Right column: **Result 2** (Theta_n law, overshoot definition, f7, A/B/C
  bullets, scan edge, TT agreement). Then **Numerical checks** (three tiles
  plus one line). Then **Conclusion** (3 bullets, limits, proposal line).
- The build check passes: tags, figures, footer, and minimum font size.

`poster/build.py` change: on a wide panel, several figures now sit in one row
on the right, and `SPEC["side_text"] = 0.45` sets the text share.

## Facts

Use `notes/tasks/poster_facts.md` (sources: file:line and Entry N). Corrections
already applied in draft 1:
- M1: quasi-static is 0.2 % of an acoustic period (beta = 0.012 rad), not 1.2 %.
- M2: Floquet agreement with TT is 1.6e-6 to 1.3e-5 (E42), shown as ~1e-5.
- M3: the 52 % side-peak sentence disappeared with f2.
- M4: R = 0.34-0.57 is the 5 % binned-median **steady-state population** error
  (E54). The time-resolved centre law error is ~0.9 R at S = 1.5 (E26) and
  <= 0.031 for R <= 0.05 (E19).
- f1 caption: the Bragg maximum 0.043 comes from E9 cases that are not all in f1. The
  caption says "over the notebook test cases".

## Open points flagged to the user (no decision yet)

1. Background has white space around the figure row; f0 labels are small (~7 mm on A0).
2. f3 omitted; the right column has almost no spare height.
3. The checks panel sits after Result 2. To put it right after Method,
   Result 1 must be shortened, because the left column is otherwise full.
4. README preview jpg not refreshed.

## Exact next action

Wait for the user's feedback on draft 1 (`poster/out/poster.pdf`/`.png`). Then
revise `poster/poster.md` (and `build.py` only if layout needs it), rebuild
with `.venv/Scripts/python.exe poster/build.py 150`, and inspect crops of the
render. Commit only when the user asks. Never push without approval.
