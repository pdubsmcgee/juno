# Notes from Steam Guide: "Vectors and PIDs in Vizzy"

Source reviewed: <https://steamcommunity.com/sharedfiles/filedetails/?id=2944674093>

## Why this guide is useful

- The author frames the guide as a refresher for people who already learned vector math, then shows how to apply that math in practical Vizzy control scripts.
- The guide's worked examples focus on a powered "hopper" problem (hovering and controlled short-range landing), which is a compact sandbox for vector-control techniques.

## Key vector takeaways for Vizzy work

1. **Treat error as a vector whenever possible.**
   - The difference between current-state and target-state vectors is a natural control error signal.
   - Error magnitude tells "how far off" the system is; error direction tells "which way to push".

2. **Use vector operations intentionally.**
   - Vector + vector / vector - vector for combining state and target signals.
   - Vector scaled by scalar for control gain adjustments.
   - Unary operations (`X`, `Y`, `Z`, `Length`, `Norm`) for extracting components or normalized direction.

3. **Coordinate systems matter.**
   - Reframing axes (custom axis definitions) can simplify guidance logic.
   - The guide repeatedly converts between coordinate frames to make heading/pitch commands more intuitive.

4. **Heading/pitch can be derived from vector geometry.**
   - Horizontal projection and spherical-angle concepts are used to generate heading-like values.
   - Pitch targets can be mapped from horizontal/vertical error behavior, including nonlinear or unit-mixed mappings when they improve control behavior.

## Key PID/control takeaways

1. **Start simple, then iterate.**
   - The guide begins with proportional-style corrections and refines from there.
   - Practical tuning and repeated test flights are treated as mandatory, not optional.

2. **Single-loop vertical control has limits.**
   - A basic velocity-only loop may not converge cleanly to zero error (or may leave residual error / oscillation).
   - Adding additional terms/state context (integral/derivative-like behavior, altitude coupling, etc.) improves stability.

3. **Gain scaling can be vectorized.**
   - Per-axis gain vectors allow different response strength per axis rather than one global gain.

4. **Clamping/physical limits are expected in practice.**
   - Requested throttle/attitude commands may exceed feasible bounds during transients; practical scripts rely on bounded outputs and tuning.

5. **Control priorities should be explicit.**
   - In landing contexts, scripts may intentionally prioritize certain objectives (for example, lateral velocity shaping vs vertical-rate safety) and then add guard conditions for edge cases.

## Practical implementation patterns worth reusing

- Build intermediate debug displays/logs to inspect vector components and error magnitudes while tuning.
- Separate target-generation logic from actuator-command logic so each can be tuned independently.
- Use staged workflows: stabilize hover first, then add landing target logic, then add dynamic target redesignation.
- Expect floating-point edge cases and include tolerance checks instead of strict equality checks when comparing small errors.

## Caveats for reuse in this repository

- The Steam guide includes many image-based code snippets. Re-implementation in this repo should still follow local verification rules (`Reference.xml`, existing program patterns, and repository-tested command forms).
- Treat this file as conceptual guidance; command/attribute syntax must be validated against this repository before XML edits.
