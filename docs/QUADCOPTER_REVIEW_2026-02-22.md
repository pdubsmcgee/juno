# Quadcopter Flight Program V3 — QA Review (2026-02-22)

## Scope
Static logic review of `Quadcopter Flight Program V3.xml` focused on mode transitions, control authority, navigation convergence, and landing behavior.

## Findings

### 1) Nav mode can drive past target because throttle is unconditional inside nav branch
In the nav branch (`If id="46"`), distance gating is used for heading updates (`If id="53"`), but throttle is set to `0.55` unconditionally afterward (`SetInput id="68"`).

**Impact:** once the craft reaches tolerance, heading updates stop but forward thrust persists, causing drift/overshoot and potential orbiting around the target.

**Recommended fix (minimal):**
- Keep `pitch=90` command.
- Gate throttle by the same distance check:
  - `distance_to_target > target_tolerance_m` -> throttle `0.55`
  - else -> set throttle near hover value (or zero and clear `nav_enabled`).

### 2) Nav completion state is not latched
`nav_enabled` is set when AG4 is pressed, but there is no explicit "arrived" transition that clears nav state on target capture.

**Impact:** controller remains in navigation mode indefinitely unless pilot changes mode, even after arriving.

**Recommended fix (minimal):**
- When `distance_to_target <= target_tolerance_m`, set:
  - `nav_enabled = 0`
  - `hold_alt_agl = Altitude.AGL` (capture current hover altitude)
- Optional: display a short "Target reached" message.

### 3) Landing flare is altitude-only with no sink-rate check
Landing logic now uses stepped throttle bands (`0.35`, `0.30`, `0.25`, `0.18`, then `0`). This is safer than hard cutoff, but the final shutdown still depends only on altitude thresholds.

**Impact:** on heavier or faster-descending craft, touchdown can still be hard because throttle cuts without considering current descent rate.

**Recommended improvement:**
- Add sink-rate check before final motor cut (if a verified vertical-speed property is available in this repo).
- If no verified sink-rate property is available, keep current approach but expose the throttle thresholds as tunables near program start for easier per-craft calibration.

## Validation notes
- XML remains well-formed after review (no program edits in this change).
