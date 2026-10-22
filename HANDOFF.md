# TraTT handoff — 2026-10-19

Codex paused supervision at the user's request because the 5-hour usage budget
was down to 4%. Resume supervision only after the budget resets. Do not restart
Herdr or close the Claude pane.

## Live worker

- Herdr workspace `w2`; Codex pane `w2:p2`; Claude worker `tratt-worker` in `w2:p5`.
- Claude was working when this handoff was written. The final independent-finish
  instruction was accepted by `herdr agent prompt` (`agent_prompted`); completion
  has not been checked.
- Claude owns `explore/nb/e67_worker_audit.py`, `.json`, `.log`, and may write
  `notes/tasks/e67_worker_report.md`. Existing research files are read-only to it.
- Task specification: `notes/tasks/e67_worker_audit.md`. The first audit run had
  no >1e-3 numerical discrepancy, but Codex found negative values in the
  reported TT peak-refinement improvement because the old grid maximum was
  omitted. Correction round 1 was sent: retain that maximum, recompute dependent
  values, check the time-refinement threshold, and append the new log run.

## Poster and current evidence

- `poster/poster.md` presents the 11,211-condition amplitude/rise-time map.
  Source data: `explore/nb/e67_overshoot.npz` and `.json`; generated figure:
  `figures/poster/f7_overshoot.png`; research provenance: notebook Entry 67.
- Right-bottom QR was restored through `figures/poster/qr_repo.png` and
  `poster/build.py`; both the QR image and the rendered `poster/out/poster.png`
  decoded to `https://github.com/NaNIsaac/TraTT`. The poster build passed.
- Codex independently checked five direct-quadrature points against the map law
  and two Laue TT points against DOP853; the largest intensity difference was
  4.17e-8. This does not replace review of Claude's final audit.
- `poster/out/poster.pdf` and `.png` are build outputs. The checked-in preview is
  `figures/poster/poster_preview.jpg`.

## Resume steps

1. Read `notes/tasks/e67_worker_report.md`, the final audit JSON/log/script,
   and the Claude pane after the usage budget resets. Do not resubmit the task.
2. Confirm the corrected peak-refinement errors are nonnegative and dependent
   excess/error fields were recomputed; inspect the code and actual log.
3. Assess the key physical claims against Entries 5, 15, 28, and 67. State that
   the map is an approximation checked at selected TT conditions, not a full TT
   sweep or a newly discovered mechanism.
4. Run the poster build or checks only if the final audit or code changes reveal
   a concrete remaining risk. Report results to the user. Leave external actions
   such as push, PR, and publication for explicit approval.

No further Codex polling or analysis was done after the final Claude instruction.
