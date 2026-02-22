# The Rocket Whisperer (Juno: New Origins Vizzy Program)

`The Rocket Whisperer` is a Vizzy flight-computer program export for **Juno: New Origins**, stored as XML in this repository.

## Repository purpose

This repo is focused on:

- Maintaining the primary Vizzy program export (`Flight Program R V3.0.xml`).
- Capturing verified command/telemetry references under `vizzy_kb/`.
- Tracking implementation and safety updates in markdown docs.

## Repository layout

- `Flight Program R V3.0.xml` — Main Vizzy program export (`<Program name="Flight Program R V3.22">`). The project title remains “The Rocket Whisperer”.
- `USER_MANUAL.md` — Full operator manual for using the flight computer.
- `PROJECT_STUBS.md` — Resolution tracker describing recent implemented tasks.
- `vizzy_kb/verified_index.md` — Repo-extracted tag/property inventory.
- `vizzy_kb/vizzy_commands_web_research.md` — Supplemental external research notes.
- `agents.md` — Repo-scoped operating and verification contract.
- `VERSION` — Repository version used for release/process tracking (`MAJOR.REVISION`).
- `scripts/bump_version.sh` — Helper to bump `VERSION` (`change|major`).
- `gpttest.xml` — Alternate complete Vizzy flight-control program profile (`<Program name="gpttest">`).
- `Reference.xml` — Comprehensive syntax reference program containing manually placed instruction blocks, dropdown variants, and representative custom-instruction patterns for future program construction.
- `docs/VIZZY_STATE_MACHINE_PATTERN.md` — Standardized Broadcast/Receive state-machine architecture and per-program state maps.
- `docs/STEAM_GUIDE_ADVANCED_DATA_STRUCTURES_NOTES.md` — Distilled notes from the Steam guide on dynamic-variable and pseudo-struct patterns in Vizzy.

## What the program does (high level)

The flight computer runs a mode-driven launch and ascent flow with:

- Preflight user input collection (target altitude, inclination, autostage).
- Input normalization and startup synchronization (`fc_init_done` gate).
- Autostage clamp fix: invalid autostage input is explicitly normalized to `1` before final `0/1` clamp logic.
- Countdown arming with timeout and abort handling.
- Gravity-turn and PEG guidance worker loops.
- Circularization ownership transitions.
- Centralized status/fault code variables for telemetry (`fc_status_code`, `fc_fault_code`).

## Quick start

1. Import either `Flight Program R V3.0.xml` or `gpttest.xml` into a craft's Vizzy program in Juno: New Origins.
2. Start flight; respond to the three startup prompts:
   - Target altitude (m AGL)
   - Target inclination (deg)
   - Autostage enabled (1/0)
3. Throttle above 90% to arm countdown and continue to launch.
4. Use AG1 as manual override / abort input where applicable.

For full operation details, see [USER_MANUAL.md](USER_MANUAL.md).

## Versioning workflow

This repo now tracks a `MAJOR.REVISION` version in `VERSION` (currently `3.22`).

When making changes:

1. Run `scripts/bump_version.sh change` for all normal updates (minimum `+0.01` equivalent), or `major` for major/breaking updates.
2. If needed for a release artifact, align the Vizzy program label/file naming with the new version.
3. Record a short summary in `agents.md` change log and `PROJECT_STUBS.md`.

## Verification posture

This repository follows a strict repo-grounded verification policy. If an instruction/field is not evidenced in the repository, it should be treated as **UNVERIFIED** and excluded from flight-program modifications.

## Reference workflow (`Reference.xml`)

`Reference.xml` is now the primary in-repo syntax catalog when drafting or validating new Vizzy logic patterns. It is intentionally non-operational and exists to show concrete XML shapes for:

- Instruction block tag names and wrapper structure.
- Dropdown/enum variants expressed as repeated attributes (for example: input channels, time modes, nav-sphere indicators, camera/craft property selectors).
- Representative custom instruction wiring patterns and argument ordering.

When adding or changing XML logic in executable programs, prefer syntax that already appears in `Reference.xml` (or the target flight program) to stay within verified repository evidence.
