# Flight Program Logic Table (Throttle/Launch Investigation)

## Scope
This document maps the **desired launch/throttle logic** against the **actual implemented logic** in `Flight Program R V3.0.xml`, then reviews each top-level thread for bugs/logic risks.

---

## A) Thread-by-thread review

| Thread | Entry condition | Main responsibility | Findings |
|---|---|---|---|
| GT Guidance (`Event id=0`) | waits for `fc_init_done == 1` | computes gravity-turn pitch/heading when `attowner == gravity_turn` | Logic is gated correctly by `attowner`. No direct throttle writes. |
| PEG label-only block (`Comment id=34`) | none | visual/comment-only section marker | No runtime effect. |
| K Solver (`Event id=35`) | waits for `fc_init_done == 1` | solves PEG normal axis `peg_k` asynchronously | Runs at 10 s cadence and eventually sets `peg_readyk = 1`. No throttle writes. |
| Flight Mode Controller (`Event id=53`) | starts at boot | initializes mode constants, asks user inputs, controls `fc_mode/attowner/throwner` | Sets startup mode to `countdown`. Calls `Countdown` custom instruction while in countdown. Manual override (`AG1`) forces owners to none. Uses `init` as autostage flag. |
| Autostager (`Event id=137`) | waits for init and `fc_mode >= ascent` | optional stage activation under depletion checks | **Bug:** checks `autostage` variable, but declared input flag appears to be `init`. This mismatch can disable intended behavior or read undefined state. |
| Throttle Manager (`Event id=174`) | waits for `fc_init_done == 1` | all throttle authority and throttle clamping | **Critical launch blocker:** if `fc_mode < ascent` it forces throttle input to 0 every tick. Countdown requires pilot throttle > 0.9 to arm, so launch can never arm while this thread is running. |
| Circularize (`Event id=242`) | waits for `fc_mode == circularization` | computes circularization burn windows and sets `thrcut` / `circ_active` | Generally coherent. Uses AG1 to cut circularization (`thrcut=1`). No pre-launch impact unless modes/flags are wrong. |
| PEG Guidance (`Event id=329`) | waits for init and guidance owner | computes PEG attitude commands while guidance active | Attitude-only authority; no throttle writes. |
| Countdown custom instruction (`CustomInstruction id=433`) | called by mode controller in countdown | wait for throttle >90%, allow AG1 abort/timeout, then stage and set ascent mode | Logic is self-consistent *if throttle input can actually rise above 0.9*. Currently blocked by Throttle Manager pre-ascent clamp. |

---

## B) Desired launch logic table

| Condition | Desired behavior |
|---|---|
| Startup in countdown mode | Pilot can raise throttle above 90% to arm countdown. |
| During countdown pre-arm | Autopilot should **not** override pilot throttle to zero. |
| AG1 during countdown | Abort countdown and keep vehicle safe. |
| Timeout before arming | Abort countdown and remain in countdown mode. |
| Successful T-0 | Stage activate, wait for liftoff velocity, then switch to ascent mode. |
| Ascent mode active | Throttle authority transfers to Throttle Manager (`throwner`-based formulas). |

---

## C) Actual launch logic table (as coded)

| Condition | Actual implemented behavior |
|---|---|
| `fc_mode == countdown` at startup | True (mode controller sets `fc_mode = fc_mode_countdown`). |
| Countdown waits for throttle >0.9 | True (`Input.Throttle > .9` required to break wait loop). |
| Throttle Manager while `fc_mode < ascent` | Forces `SetInput(throttle)=0` every 0.05 s. |
| Combined effect of previous two rows | Pilot cannot keep throttle >0.9 long enough (or at all), so countdown never arms. |
| AG1 behavior | Also sets throttle 0 in Throttle Manager and is used as countdown abort signal; works as abort path. |
| Launch progression | Stalls in countdown unless an external race/glitch bypasses the clamp. |

---

## D) Mismatch summary (desired vs actual)

| Area | Desired | Actual | Result |
|---|---|---|---|
| Pre-launch throttle authority | Pilot authority available for arm (>90%) | Throttle Manager zeros throttle before ascent | **Primary root cause of no-launch** |
| Autostage enable flag | use validated user input flag | thread checks `autostage` while user input stored in `init` | Secondary logic bug (autostage reliability) |

---

## E) Root-cause conclusion

The throttle-stuck-at-zero launch failure is caused by **cross-thread interaction**:
1. Mode Controller enters countdown and calls `Countdown`.
2. Countdown requires `Input.Throttle > 0.9` to arm.
3. Throttle Manager concurrently enforces `throttle = 0` whenever `fc_mode < ascent`.
4. Therefore countdown cannot arm, so ascent mode is never reached, so throttle remains locked at 0.

This is a deterministic logical deadlock between the countdown thread and throttle thread.

---

## F) Recommended fix direction (minimal)

1. In Throttle Manager, do **not** force throttle to 0 during countdown pre-arm (or gate this clamp behind an explicit abort/manual state instead of `fc_mode < ascent`).
2. Normalize autostage variable usage (`init` vs `autostage`) so one declared flag is used consistently.
3. Keep AG1 abort semantics, but separate “abort command” from “always-zero pre-ascent throttle” behavior.

---

## G) Implemented fixes (post-analysis)

The following XML fixes were applied to align implementation with the desired logic above:

1. **Countdown throttle deadlock removed**
   - In Throttle Manager, the pre-ascent zero-throttle branch was narrowed from `fc_mode < ascent` to `fc_mode == none`, so countdown no longer gets blanket-throttled to zero.
   - Additional `throwner_none`/fallback zero-throttle branches were gated so they do not fire in `countdown` mode.

2. **Autostage flag consistency fixed**
   - Autostager now checks `init` (the same flag populated by user input normalization), replacing inconsistent `autostage` usage.


3. **Circularization thread conflict fixes**
   - AG1 abort in Circularize outer loop now sets `thrcut=1` (cut thrust) instead of `0`.
   - Circularize inner-loop attitude-owner mismatch now relinquishes with `thrcut=0` instead of forcing a global throttle cut.
   - Throttle Manager circularization branch now holds throttle at zero until the craft is within 1 km of apoapsis altitude (`Altitude.AGL >= Orbit.Apoapsis - 1000`), reducing premature/negative-Δv throttle behavior.

These changes preserve AG1 abort behavior while allowing pilot throttle authority during countdown arming.

---

## H) Quadcopter activation-group logic table (comprehensive)

### Initialization policy at FlightStart

| Variable / command | Init value | Reason |
|---|---:|---|
| `auto_enabled` | `0` | Start in non-auto state. |
| `manual_override` | `0` | Manual should not be latched at boot. |
| `landing_armed` | `1` | Craft starts landed; landing mode is initially armed/safe. |
| `nav_enabled` | `0` | Navigation guidance should be off until takeoff/hold is engaged. |
| `ag1_takeoff_hold_cmd` / `ag2_land_cmd` / `ag3_manual_cmd` / `ag4_nav_cmd` | `0` | Command mirrors initialize false and are refreshed every control tick from AG1..AG4. |

### Command-priority and transition table

| Priority | Input condition | State updates | Notes |
|---:|---|---|---|
| 1 | `AG3` active (`ag3_manual_cmd = 1`) | `manual_override=1`, `auto_enabled=0`, `nav_enabled=0` | Manual is dominant when active. |
| 2 | `AG1` active (`ag1_takeoff_hold_cmd = 1`) | `manual_override=0`, `auto_enabled=1`, `landing_armed=0`, `nav_enabled=0`, capture `home_pos`, set `hold_alt_agl=target_alt_agl` | Explicitly clears manual when switching to takeoff/hover. |
| 3 | `AG4` active and `auto_enabled=1` | `nav_enabled=1` | Enables horizontal nav only when auto is already enabled. |
| 4 | `AG2` active and `auto_enabled=1` | `landing_armed=1`, `nav_enabled=0` | Landing request cancels nav and arms descent. |

### Mode-behavior table

| Mode flags | Vertical command | Attitude command | Horizontal command |
|---|---|---|---|
| `auto_enabled=0` (manual) | No auto throttle writes expected from mode logic branch | Pilot/manual | Pilot/manual |
| `auto_enabled=1`, `landing_armed=1` | Descent throttle schedule by altitude bands | `pitch=90` | none |
| `auto_enabled=1`, `landing_armed=0`, `nav_enabled=1` | Cruise/hold throttle | `pitch=90`, heading-to-target | drive toward target |
| `auto_enabled=1`, `landing_armed=0`, `nav_enabled=0` | Altitude hold throttle (`0.60` up / `0.45` maintain) | `pitch=90` | hold |

### Threading/refactor table

| Thread | Loop rate | Responsibility |
|---|---|---|
| Control-logic planner (`Event id=0`, `While id=12`) | `0.05 s` | Computes command outputs (`throttle_cmd`, `pitch_cmd`, `nav_heading_cmd`, `heading_hold_enabled`) from state vars (`auto_enabled`, `landing_armed`, `nav_enabled`, `manual_override`). |
| Throttle actuator (`Event id=344`, `While id=345`) | `0.05 s` | Applies `throttle_cmd` to `slider1` only when `manual_override=0`. |
| Navigation actuator (`Event id=349`, `While id=350`) | `0.05 s` | Applies `pitch_cmd` continuously; applies heading hold from `nav_heading_cmd` when `heading_hold_enabled=1` and `manual_override=0`. |
| Activation/state manager (`Event id=300`, `While id=301`) | `0.05 s` | Reads AG1..AG4, updates command mirrors, applies transition priority/state updates. |
| Prop-pitch optimizer (`Event id=173`, `While id=174`) | `0.1 s` | Independent variable-pitch optimization and fail-safe reset behavior. |

### Input-handling answer (manual -> takeoff/hover)

Yes — with the refactor, switching from manual (`AG3`) to takeoff+hover (`AG1`) explicitly writes `manual_override=0` in the activation/state-manager thread before enabling auto flight state. This makes the handoff deterministic and avoids stale manual-mode ownership.
