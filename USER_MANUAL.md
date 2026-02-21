# User Manual — The Rocket Whisperer

This manual describes how to operate the `The Rocket Whisperer` Vizzy flight computer from this repository.

---

## 1) Overview

`The Rocket Whisperer` is a mode-based ascent automation program with coordinated worker loops (countdown, gravity turn, PEG guidance, and circularization support). It includes startup synchronization and fault/status telemetry variables.

Core operator-visible behavior:

- Prompts for mission inputs at flight start.
- Normalizes out-of-range startup values.
- Waits for throttle arm before countdown/launch.
- Can abort countdown via AG1 or timeout.
- Transitions through internal flight phases.

---

## 2) Before you fly

### Requirements

- Juno: New Origins craft with Vizzy support.
- Program imported from `Flight Computer R V1.5.xml`.

### Program identity

The XML root defines:

- Program name: `The Rocket Whisperer`

### Safety expectations

- This program is automation-heavy; review your craft's staging, thrust-to-weight ratio, and aerodynamic stability before use.
- Manual mode / AG1 interaction is integrated into controller logic; be prepared to intervene.

---

## 3) Startup sequence

At `FlightStart`, the controller initializes mode constants/owners, status/fault codes, and asks for three inputs:

1. `Target altitude (m AGL). Enter 10000 to 500000.`
2. `Target inclination (deg). Enter 0 to 180.`
3. `Autostage enabled? Enter 1=yes, 0=no.`

### Input normalization

The program clamps/normalizes startup values and logs preflight status:

- Altitude is clamped to `10000..500000` meters.
- Inclination is clamped to `0..180` degrees.
- Autostage is normalized to `0` or `1`.

After normalization, initialization completes by setting `fc_init_done = 1`, allowing dependent workers to proceed.

---

## 4) Operator controls

### Throttle arming for launch

The countdown instruction displays:

- `Set Throttle>90% to arm countdown (timeout 30s, AG1 abort).`

Launch does not proceed until throttle input exceeds `0.9`.

### AG1 behavior

AG1 is read in multiple places:

- During countdown, AG1 can trigger abort.
- In controller loop logic, AG1 is also used for manual ownership behavior.

Treat AG1 as a high-impact operator control.

---

## 5) Flight phases and internal state

The controller defines mode and ownership states.

### `fc_mode` states

- `0` = none
- `1` = countdown
- `2` = ascent
- `3` = circularization
- `4` = done

### `attowner` states

- `0` = none/manual
- `1` = gravity turn
- `2` = guidance
- `3` = circularization

### `throwner` states

- `0` = none/manual
- `1` = gravity turn
- `2` = guidance
- `3` = circularization

### Telemetry codes

- `fc_status_code` tracks high-level active mode phase (initialized and updated by controller).
- `fc_fault_code` tracks fault/abort conditions (for example, countdown timeout/abort).

---

## 6) Countdown and abort logic

Countdown behavior is implemented as a custom instruction (`Countdown`) and includes explicit abort conditions.

### Countdown path

If throttle is armed before timeout/abort:

1. Fault is cleared (`fc_fault_code = 0`).
2. Audible/visual countdown (`3`, `2`, `1`, `Blastoff!!!!`).
3. Stage activation.
4. Wait until surface velocity exceeds threshold (`gt_tsv`).
5. Transition to ascent mode and gravity-turn start message.

### Abort/fault path

Countdown sets `countdown_abort = 1` and exits when either occurs:

- **Timeout** (`countdown_elapsed_s >= countdown_timeout_s`) with fault code `100`.
- **AG1 abort** during countdown with fault code `101`.

On abort/timeout, the program logs that it remains in countdown mode.

---

## 7) Guidance architecture (operator-facing summary)

Multiple `FlightStart` workers run in parallel and gate on `fc_init_done == 1` before active operation. This prevents early startup races.

Operator-relevant modules include:

- Gravity-turn guidance loop.
- PEG guidance loop (displays and logs initialization once ownership transitions to guidance).
- Circularization ownership logic.

Loop cadences are generally non-zero (notably `0.05s` in many polling loops).

---

## 8) Troubleshooting

### No launch after program starts

- Verify throttle is above 90% to arm countdown.
- Check AG1 state; AG1 can trigger countdown abort behavior.

### Program seems stuck in countdown

- Inspect whether timeout/abort occurred.
- If available in your display/log workflow, inspect `fc_fault_code`:
  - `100`: countdown timeout
  - `101`: AG1 abort during countdown

### Unexpected mission targets

- Startup values are normalized. If you entered values out of range, the program clamps them and logs the normalization.

---

## 9) Known limits and verification boundaries

- This manual is derived from repository-visible XML and docs.
- Features not evidenced in this repo are intentionally excluded.
- The supplemental web-research notes under `vizzy_kb/` are informative but should not override in-repo evidence when editing mission-critical logic.

---

## 10) File references

Primary sources in this repository:

- `Flight Computer R V1.5.xml`
- `PROJECT_STUBS.md`
- `vizzy_kb/verified_index.md`
- `agents.md`
