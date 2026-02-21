# Codex Task Stubs — `The Rocket Whisperer`

This backlog is a repository-grounded static review of `Flight Computer R V1.5.xml` and is intended to be directly actionable in Codex.

## Task Stub 1 — Resolve unowned throttle command outputs
- **Problem:** `thrcmd` and `thrcmdvalid` are declared in `<Variables>` but have no `variableName="..."` references in `<Instructions>`.
- **Suggested improvement:** Either wire these variables into the active throttle control flow, or remove them and document that throttle output is internal-only.
- **Codex starter stub:**
  - [ ] Confirm throttle ownership contract (`throwner`/`thrcut` vs external consumer).
  - [ ] If external API is intended, add a dedicated comment block marking `thrcmd`/`thrcmdvalid` as interface outputs.
  - [ ] If not intended, remove both declarations and rerun static usage check.
  - [ ] Validate no new unreferenced declarations remain.

## Task Stub 2 — Replace mode/owner magic numbers with named constants
- **Problem:** Mode and ownership values are hard-coded as numeric literals across the controller logic (`fc_mode` values like `1..4`, and owner fields like `0..3`).
- **Suggested improvement:** Introduce explicit constants (or documented variable aliases) for each mode and owner state to reduce ambiguity and editing mistakes.
- **Codex starter stub:**
  - [ ] Inventory all literals used for `fc_mode`, `attowner`, and `throwner` comparisons/assignments.
  - [ ] Define a naming scheme (e.g., `MODE_ASCENT`, `OWNER_GT`) and apply consistently.
  - [ ] Update assignments/comparisons to use named constants/aliases.
  - [ ] Run XML sanity pass to ensure no node/link breakage.

## Task Stub 3 — Audit busy-loop cadence (`WaitSeconds 0`)
- **Problem:** The file contains many `WaitSeconds` blocks with `Constant text="0"` inside `While true` loops, which can create aggressive update loops.
- **Suggested improvement:** Standardize a minimal scheduler tick (where safe) and reserve zero-wait loops only for latency-critical sections.
- **Codex starter stub:**
  - [ ] Enumerate all `WaitSeconds 0` locations and map each to its loop purpose.
  - [ ] Classify each as latency-critical or safe-to-throttle.
  - [ ] Replace safe cases with a small non-zero cadence.
  - [ ] Flight-test behavior equivalence after cadence changes.

## Task Stub 4 — Normalize operator prompts and inline docs
- **Problem:** User prompts and labels are inconsistent (`"Target Alt?"`, `"Target inc?"`, `"Autostage??  1 or 0"`), and some control intent is encoded only in numeric values.
- **Suggested improvement:** Standardize operator-facing text and add concise comments near control handoff logic.
- **Codex starter stub:**
  - [ ] Rewrite `UserInput` prompt strings for consistent style/units.
  - [ ] Add comments describing mode transitions and owner handoffs.
  - [ ] Add one comment block documenting accepted input ranges.
  - [ ] Re-export and diff-check XML for minimal structural changes.
