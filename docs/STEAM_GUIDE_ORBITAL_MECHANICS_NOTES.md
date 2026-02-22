# Notes from Steam Guide: "Orbital mechanics for realistic space flight simulators"

Source reviewed: <https://steamcommunity.com/sharedfiles/filedetails/?id=2961230801>

## Scope of the source

- The guide is a practical orbital-mechanics walkthrough aimed at automation use cases (not just textbook derivations).
- It focuses on computing maneuver parameters that are directly useful in simulation scripting (especially Vizzy-style workflows).
- It uses standard two-body formulas, then calls out simulator-specific caveats (notably Juno coordinate-system details and low-warp numerical drift concerns).

## Distilled high-value takeaways

1. **Model elliptical orbits as the default; treat perfectly circular orbits as a special edge case.**
   - Many robust procedures become cleaner if you assume `0 < e < 1` and handle `e ≈ 0` explicitly with tolerances.

2. **Reference-frame discipline matters more than formula count.**
   - Build and maintain a consistent perifocal frame per orbit (`p`, `q`, `w`) and only recalculate it when the orbit changes.
   - Be explicit about game-engine coordinate conventions when mapping textbook formulas into code.

3. **Prefer maneuver decomposition into reusable primitives.**
   - The guide’s practical flow composes a rendezvous from sequential primitives:
     - adjust apsis,
     - match planes,
     - align apse lines,
     - phase timing,
     - final apsis correction.
   - This is more maintainable than one monolithic “solve everything” burn routine.

4. **Use anomaly/time conversions as first-class tools.**
   - True anomaly, eccentric anomaly, mean anomaly, and time-since-periapsis conversion functions are central plumbing for maneuver timing.
   - Reliable conversion helpers are foundational for phasing and rendezvous work.

5. **Plane matching can be formulated from orbital-plane intersection geometry.**
   - Compute the line of intersection between planes, convert candidate intersection directions to true anomalies, and evaluate burn cost at each candidate.

6. **Apse-line alignment and interception logic benefit from explicit diagnostics.**
   - Intermediate terms can reveal important topology cases (e.g., no intersection, identical orbits, already aligned apse lines).
   - Treat those conditions as explicit branches instead of relying on fragile downstream math.

7. **Burn execution accuracy is as important as burn math.**
   - The guide emphasizes that guidance quality is strongly impacted by burn-termination method and practical execution details.
   - Replan iteratively over multiple orbits when precision requirements are tight.

8. **SOI-transition prediction is computationally tricky and should use staged refinement.**
   - A practical approach is coarse sweep -> backup step -> binary-search refinement to locate the transition boundary.
   - Accuracy/speed is controlled by initial step size and refinement tolerance.

## Recommended integration into this repository

- Keep orbital toolkit architecture modular around these primitives:
  - orbit-element derivation,
  - frame transforms,
  - anomaly/time converters,
  - maneuver solvers,
  - burn execution/termination logic.
- Encode explicit tolerance policies for near-circular and near-coplanar edge cases.
- Add debug instrumentation for intermediate geometric checks (plane intersection vectors, anomaly candidates, expected intercept timing).
- Treat low-warp numerical propagation as an operational caveat and re-validate planned burns near execution.

## Caveats

- This note is a distilled conceptual summary of the linked guide, not a formal derivation.
- Any direct Vizzy/XML implementation in this repository must still be validated against repository-verified command and field usage before code edits.
