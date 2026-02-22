# Notes from Steam Guide: "Introduction to Vizzy and Launch Automation"

Source reviewed: <https://steamcommunity.com/sharedfiles/filedetails/?id=3247360849>

## Why this guide is useful

- It presents a full launch autopilot build in incremental steps rather than a single "finished" script dump.
- It targets newer Vizzy users while still introducing patterns that scale to more advanced scripts.
- The practical focus (launch-to-orbit with staging + inclination targeting) aligns with flight-computer work in this repository.

## Distilled implementation takeaways

1. **Build automation as staged capability slices.**
   - Add one behavior at a time (for example: ascent pitch logic, then staging, then circularization, then inclination handling).
   - Validate each slice in flight before layering additional behavior.

2. **Use explicit mission phases/state gates.**
   - Segment ascent behavior into stage/phase-specific logic instead of one monolithic control formula.
   - Gate actions by clear conditions (altitude bands, engine state, apoapsis/periapsis targets, etc.).

3. **Separate craft-agnostic guidance from craft-specific tuning.**
   - Keep reusable logic (orbit-targeting flow) distinct from vehicle-specific constants (roll schedule, gains, throttle heuristics).
   - This reduces rework when migrating autopilot logic to a new launcher.

4. **Treat roll control as an independent concern.**
   - Running roll behavior in its own thread can simplify the primary pitch/heading guidance path.
   - Roll targets are highly craft-dependent and should be tuned separately from generic launch logic.

5. **Multithreading is a core Vizzy scaling tool.**
   - Split long-running or logically distinct responsibilities across concurrent event/while threads.
   - Use waits and thread pacing deliberately so one loop does not monopolize instruction budget.

6. **Design for observability while tuning.**
   - Include operator-facing status output/logging to expose current phase and key guidance values.
   - Better visibility shortens PID/heuristic tuning cycles and helps isolate bad transitions.

7. **Use fUNK selectively, not everywhere.**
   - fUNK can compress complex expressions and dynamic access patterns into one block.
   - Prefer normal Vizzy blocks for readability unless fUNK provides a clear practical advantage.

8. **Expect and manage runtime limits.**
   - Large scripts may hit practical performance limits; organization and thread pacing matter.
   - Keep control loops simple, bounded, and robust to frame-rate/instruction-budget variation.

## Repository-aligned reuse guidance

- The guide includes image-heavy examples and author-specific craft assumptions; adapt concepts, not literal numeric values.
- For this repository, keep using the documented state-machine/event-thread architecture and explicit state transitions when integrating ideas.
- Any command/field used in XML edits must still be validated against local repository evidence (`Reference.xml` and existing verified patterns).
