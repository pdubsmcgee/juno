# Codex Task Stubs — `The Rocket Whisperer`

This backlog is a repository-grounded static review of `Flight Computer R V1.5.xml` and is intended to be directly actionable in Codex.

## Task Stub 1 — Refresh stale backlog items
- **Problem:** Existing stubs include historical issues that no longer match the current XML state, which can cause wasted effort and confusion.
- **Suggested improvement:** Keep this backlog synchronized with the actual program state and remove/mark completed items.
- **Codex starter stub:**
  - [ ] Re-verify each task against the latest XML before keeping it in backlog.
  - [ ] Remove or mark completed items with date and short evidence note.
  - [ ] Add source line references for all active tasks.
  - [ ] Keep only unresolved, reproducible issues/features.

## Task Stub 2 — Add startup synchronization gate
- **Problem:** Multiple `FlightStart` instruction trees run concurrently and can read shared state before initialization is complete.
- **Suggested improvement:** Introduce an explicit startup barrier variable and gate dependent workers.
- **Codex starter stub:**
  - [ ] Add global variable `fc_init_done` defaulting to `0`.
  - [ ] Set `fc_init_done = 1` after startup constants and input normalization complete.
  - [ ] Insert `WaitUntil` checks in dependent `FlightStart` loops.
  - [ ] Verify no worker consumes shared mode/owner state before gate opens.

## Task Stub 3 — Add countdown timeout and abort path
- **Problem:** Countdown arming waits for throttle threshold and may block indefinitely if the condition is never met.
- **Suggested improvement:** Add bounded wait behavior with explicit abort/timeout outcomes.
- **Codex starter stub:**
  - [ ] Add countdown timeout variable and elapsed-time check.
  - [ ] Add abort condition (manual override/cancel flag).
  - [ ] Log the terminal path (`armed`, `timeout`, or `abort`).
  - [ ] Ensure controller mode transitions are deterministic after each path.

## Task Stub 4 — Complete zero-delay loop audit
- **Problem:** Remaining `WaitSeconds` nodes with `Constant text="0"` can still cause aggressive polling.
- **Suggested improvement:** Classify each zero-wait loop as latency-critical or safe-to-throttle and document intent.
- **Codex starter stub:**
  - [ ] Enumerate current `WaitSeconds 0` locations and map loop purpose.
  - [ ] Keep zero only in latency-critical loops with comment rationale.
  - [ ] Replace safe loops with small non-zero tick (e.g., `0.02`–`0.05`).
  - [ ] Flight-test behavior equivalence after cadence changes.

## Task Stub 5 — Normalize manual input typing
- **Problem:** `manual` control uses activation-group output and boolean equality checks, which mixes numeric/boolean semantics.
- **Suggested improvement:** Normalize to explicit `0/1` state and use one comparison style consistently.
- **Codex starter stub:**
  - [ ] Normalize activation group output to strict numeric `manual` state.
  - [ ] Update manual-mode comparisons to one consistent convention.
  - [ ] Verify ownership handoff logic is unchanged in manual mode.
  - [ ] Add one inline comment documenting manual-state semantics.

## Task Stub 6 — Add preflight operator summary
- **Problem:** Inputs are validated/clamped, but there is no single summary confirming final launch parameters.
- **Suggested improvement:** Emit a concise preflight summary to improve operator confidence and traceability.
- **Codex starter stub:**
  - [ ] Add one display/log summary after input normalization.
  - [ ] Include normalized altitude, inclination, and autostage status.
  - [ ] Include initial mode/owner state in summary.
  - [ ] Ensure summary is emitted once per flight start.

## Task Stub 7 — Add centralized status/fault telemetry
- **Problem:** Multi-loop control flow lacks centralized status/fault code variables for rapid diagnostics.
- **Suggested improvement:** Introduce explicit status and fault channels.
- **Codex starter stub:**
  - [ ] Add global variables `fc_status_code` and `fc_fault_code`.
  - [ ] Set status code at major mode/owner transitions.
  - [ ] Set fault code on timeout/abort/error paths.
  - [ ] Document code map in a nearby comment block.

## Task Stub 8 — Build verified command and telemetry KB index
- **Problem:** Repository KB still marks exhaustive validated command/telemetry extraction as open.
- **Suggested improvement:** Build a local verified-only index from this XML and related repo docs.
- **Codex starter stub:**
  - [ ] Extract command node types and telemetry properties used in XML.
  - [ ] Record each entry in `vizzy_kb/` with source references.
  - [ ] Separate VERIFIED entries from UNVERIFIED hypotheses.
  - [ ] Add a short coverage summary (counts + known gaps).
