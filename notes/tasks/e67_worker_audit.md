# E67 worker audit

Status: **closed** (2026-10-19). Run 3 accepted after correction round 1; summary in notebook Entry 67, commits 7702c07, 892696e.
Current Codex pane: `w2:p2`; worker pane: `w2:p5`; workspace: `w2`.
The worker pane was created with `--no-focus` in the TraTT directory.
Worker name: `tratt-worker`; Claude session: `bc5a531b-844a-4d66-a6d2-ab30cb9b172d`.
The user approved Claude's initial folder-trust confirmation. `agent get` then
confirmed `idle` and interactive readiness. The task was sent once through
`agent prompt`; subsequent `agent get` confirmed `working` and a visible read
showed the worker reading the task, Entry 67, and the TT solver.
The 30-second prompt wait timed out while the worker was working; this was not
a failed submission, and the prompt was not resent. While working, use visible
reads: long alternate-screen history reads require an idle agent.

Initial IPC diagnosis corrected: Herdr PID 9148 and Codex run as `isaac`,
unelevated at Medium integrity. Sandboxed tool commands run as the different
`CodexSandboxOffline` account, also Medium. The CLI's elevated-server wording
was misleading for this case. After the user enabled Ask for approval,
the approved unsandboxed `herdr agent list` succeeded. No server restart,
Windows elevation, or existing-session termination was needed.
Correction rounds used: 1 of 2.

Supervisor review of run 1: the audit completed in 26.4 s with no threshold
findings, but local TT peak refinement dropped the original grid maximum.
The reported refinement changes were negative (B: -2.0981e-6; C: -8.9696e-7;
short-rise: -4.3927e-6). Round 1 requests retaining the original peak candidate,
recomputing dependent excess/error metrics, adding a time-refinement threshold
check, and appending the corrected run to the log to preserve initial evidence.

## Objective

Independently audit the envelope-induced overshoot map used in the poster.
Determine whether its metric, sampled boundaries, and numerical checks support
the printed claims in Entry 67 and `poster/poster.md`.

## Scope

Read `AGENTS.md`, `DESIGN.md`, notebook Entries 5, 15, 28, 67,
`explore/nb/e67_overshoot_map.py`, its JSON/NPZ results, and the core TT solver.
Use the existing uncommitted working tree; do not reset, stash, or commit it.

Exclusive worker write ownership:

- `explore/nb/e67_worker_audit.py`
- `explore/nb/e67_worker_audit.json`
- `explore/nb/e67_worker_audit.log`

All existing files are read-only for this task. The supervisor owns the poster,
plotting script, original map script/results, notebook, and task records.
Do not start subagents, publish anything, or modify the physical solver.

## Acceptance criteria

1. Define the observable as first-satellite centre intensity, normalized to the
   incident intensity, averaged over carrier phase at fixed envelope time.
   Verify that it is not an angular integral or a temporal moving average.
2. Compute the depth integral directly, independently of the map script's
   antiderivative implementation. Check causality and the fully filled endpoint.
3. Check cases A/B/C plus the sampled-map maximum (S=3.8, T=4) and the short-rise,
   high-amplitude boundary (S=6, T=0.05), with alpha=0.5 and alpha_ac=40.
4. Assess TT depth resolution and carrier-phase resolution separately. Record
   differences for base versus doubled depth, and 16 versus 32 carrier phases,
   at selected times including the transient maximum and steady state.
5. Check that time sampling resolves the peak; state errors in absolute incident
   intensity units. Differences above 1e-3 require investigation and a finding,
   not a silently changed tolerance. Do not claim a global error bound from spots.
6. Verify why this thickness excludes a Pendellösung intensity maximum and why
   the map does not establish a new mechanism beyond Entry 15.

## Deliverables

A reproducible audit script, machine-readable results, and its execution log in
the three owned paths. Reply in the Herdr terminal with findings by severity,
commands executed, numerical errors, changed files, and unresolved limitations.
Do not edit the poster or notebook to resolve findings; report them to Codex.

## Validation procedure

Use `.venv/Scripts/python.exe`. Compare direct depth quadrature with the saved
map law at matched parameters and times. Recompute full TT at the selected
checks using the existing solver, verifying its Laue initial conditions and
normalization in source. Separate solver discretization, phase sampling,
time sampling, and approximation error in the JSON/log.

Keep the run to these cases, one process, and roughly five minutes maximum.
If it needs substantially longer, report the cost estimate before extending it.
Codex will inspect the implementation and log, rerun selected checks, assess
claims, and request at most two correction rounds if necessary.
