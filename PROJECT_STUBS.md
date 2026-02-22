# Codex Task Stubs — `The Rocket Whisperer`

This backlog tracks the static review and implementation work performed against `Flight Program R V3.0.xml`.

## Resolution Summary (2026-02-21)
- [x] Task 1 — Refresh stale backlog items
- [x] Task 2 — Add startup synchronization gate
- [x] Task 3 — Add countdown timeout and abort path
- [x] Task 4 — Complete zero-delay loop audit
- [x] Task 5 — Normalize manual input typing
- [x] Task 6 — Add preflight operator summary
- [x] Task 7 — Add centralized status/fault telemetry
- [x] Task 8 — Build verified command and telemetry KB index

## Task 1 — Refresh stale backlog items (RESOLVED)
- Replaced outdated stubs with current, actionable tasks.
- Converted this file into a resolution tracker after implementation.

## Task 2 — Add startup synchronization gate (RESOLVED)
- Added global `fc_init_done` variable.
- Added `WaitUntil fc_init_done == 1` gates for non-controller `FlightStart` workers.
- Set `fc_init_done = 1` in controller after startup input normalization.

## Task 3 — Add countdown timeout and abort path (RESOLVED)
- Added countdown control variables: `countdown_timeout_s`, `countdown_elapsed_s`, `countdown_abort`.
- Replaced unbounded throttle `WaitUntil` with a guarded polling loop.
- Added AG1 abort and timeout exits with fault-code updates and logging.

## Task 4 — Complete zero-delay loop audit (RESOLVED)
- Replaced remaining `WaitSeconds` blocks using `Constant text="0"` with `0.05` loop cadence.
- Preserved the existing non-zero cadence conventions used in most control loops.

## Task 5 — Normalize manual input typing (RESOLVED)
- Updated manual mode equality check to explicit numeric compare (`manual == 1`).
- Preserved existing ownership handoff behavior for manual mode.

## Task 6 — Add preflight operator summary (RESOLVED)
- Added preflight normalization log line after input normalization.
- Summary confirms normalized launch input configuration before workers proceed.

## Task 7 — Add centralized status/fault telemetry (RESOLVED)
- Added global telemetry variables: `fc_status_code`, `fc_fault_code`.
- Initialized status/fault values at startup.
- Added mode-phase status updates in controller loop.
- Added countdown timeout/abort fault-code writes.

## Task 8 — Build verified command and telemetry KB index (RESOLVED)
- Added `vizzy_kb/verified_index.md` with in-repo extracted command/telemetry inventory.
- Included generation method and evidence references tied to repository sources.


## Task 9 — Fix autostage clamp path (RESOLVED)
- Updated preflight autostage normalization so invalid input is forced through the clamp path.
- Preserved final autostage output as explicit binary `0/1` state for downstream logic.

## Task 10 — Add repository versioning workflow (RESOLVED)
- Added semantic version source-of-truth file: `VERSION` (`3.0.1`).
- Added `scripts/bump_version.sh` to automate `major|minor|patch` version increments.
- Documented versioning procedure in `README.md`, `docs/MAINTAINER_GUIDE.md`, and `agents.md`.

## Task 11 — Incorporate reference syntax XML into docs/rules (RESOLVED)
- Reviewed `Reference.xml` as a manually assembled block/selector syntax catalog.
- Updated `README.md`, `docs/MAINTAINER_GUIDE.md`, and `vizzy_kb/verified_index.md` to treat `Reference.xml` as a first-class verification source.
- Updated `agents.md` repository contract and change log to reflect partially verified schema coverage from the reference catalog.
