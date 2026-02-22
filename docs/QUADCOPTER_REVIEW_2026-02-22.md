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

### 3) Landing flare is altitude-only with no sink-rate check — ✅ Closed
Landing branch now keeps low throttle in the touchdown zone until both conditions are true:
- `Altitude.AGL < 1` (touchdown zone)
- `Vel.VerticalSurfaceVelocity` is within a safe band (`-0.6 < v < 0.6`), i.e., low absolute vertical speed.

Only then does logic set `throttle_cmd = 0`, clear `landing_armed`, clear `auto_enabled/nav_enabled`, and emit a touchdown confirmation display/log message.

**Closure impact:** final motor shutdown is now gated by both altitude and sink-rate evidence, reducing hard-cut risk during high descent rates.

## Validation notes
- XML remains well-formed after the landing-branch sink-rate gate update.
