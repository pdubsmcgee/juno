# Steam Guide Notes: Orbital Toolkit Inaccuracies and Mitigations

Source reviewed: Steam guide `id=3039843312` (“A Vizzy toolkit for orbital mechanics”).

## Why this matters
The guide reports that **Juno uses numerical integration at low warp (1x/2x)** and an analytical/on-rails model at higher warp.
That means guidance logic based on ideal orbital math can diverge from game-reported state while the craft remains at 1x/2x for long periods.

## Main in-game inaccuracies called out in the guide

1. **Drift at 1x due to numerical integration**
   - In a 100 km × 102 km test orbit, long-duration 1x simulation produced measurable divergence between calculated and game-reported state.
   - Reported example scale after ~2h7m: about **2.2 km position error** and **~2.60 m/s velocity error**.

2. **Orbit-element instability that should be constant in pure 2-body flight**
   - The guide highlights visible drift in elements like **Argument of Periapsis** during numerical integration (example rate around **0.01°/s**).
   - In an ideal two-body model, most orbital parameters should stay constant while only true anomaly/time-to-apse evolve.

3. **Timing race around physics ticks**
   - Even “immediate” sampling can show tiny mismatches if a physics tick occurs between timestamp capture and telemetry read.

## Practical compensation strategy (recommended by guide)

1. **After each burn, switch to higher warp (e.g., 10x) quickly**
   - Purpose: minimize time spent in low-warp numerical integration where drift accumulates.

2. **Return to 1x only when needed for burn execution/attitude setup**
   - Plan and execute burns at 1x, then go back to high warp for coast phases.

3. **Compute/refresh post-burn orbit after entering high warp**
   - Keeps calculations synchronized to the same model the game is using in coast.

4. **If staying at 1x for long periods is unavoidable, continuously replan**
   - Inferior to high-warp coast, but can reduce stale-maneuver errors by repeatedly recalculating near execution time.

## What this could affect in this repository

These notes are most relevant to any routines that:
- Compute future orbit intersections/rendezvous or patched-conic transitions.
- Depend on stable orbital elements over long coast intervals.
- Assume “calculated state == game state” while idling at 1x/2x.

Potential symptoms if unmitigated:
- Slightly mistimed burns.
- Small phase/apse alignment misses.
- SOI-transition predictions that are close but offset when dropping from warp early and waiting at 1x.

## Suggested operational guardrails for our Vizzy workflows

- Treat low-warp coasting as a **drift-prone mode**.
- Prefer a “**burn at 1x, coast at >=10x, re-check before next burn**” cadence.
- Recalculate targeting data after any extended 1x/2x period.
- Keep tolerances in maneuver logic realistic for low-warp operation.

## Additional caveats from the same guide

- Complex maneuver stack code may still contain implementation bugs independent of the math.
- Perfectly circular orbits (`e = 0`) are a known edge case in the referenced toolkit.
- Large Vizzy programs may be editor-slow (especially on mobile), even if runtime is acceptable.
