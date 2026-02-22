# agents.md

## DeltaVinci Operating Contract (Repo-Scoped)

### 1) Operating mode
- Adversarial self-verification only.
- Repository-grounded facts only (no guessed Vizzy syntax/telemetry/toolkit fields).
- Unknown features must be marked **UNVERIFIED** and excluded from XML edits.

### 2) Current repository index
- Vizzy XML exports:
  - `Flight Program R V3.0.xml`
  - `Reference.xml` (non-operational syntax reference catalog)
- Repository version marker:
  - `VERSION` (`MAJOR.REVISION`, currently `3.12`)
- Version utility:
  - `scripts/bump_version.sh`
- Agent/reference docs:
  - `You are “DeltaVinci”.txt`
  - `agents.md.txt` (legacy template)
  - `agents.md` (this authoritative file)

### 3) Verified structural facts (from current repo)
- Vizzy program root element is `<Program name="...">`.  
  Evidence: `Flight Program R V3.0.xml`, `Reference.xml`
- Global variables are declared under `<Variables>` with `<Variable name="..." number="..." />` entries.  
  Evidence: `Flight Program R V3.0.xml`, `Reference.xml`
- `Reference.xml` contains a manually assembled block catalog with broad instruction coverage, including dropdown/selector variants (for example `SetInput`, `SetTimeMode`, `LockNavSphere`, `SetCameraProperty`, `SetCraftProperty`).  
  Evidence: `Reference.xml`
- This repository currently includes one large flight-computer program with many predeclared numeric variables (guidance, PEG, circularization, staging, and control intermediates).  
  Evidence: `Flight Program R V3.0.xml`

### 4) XML editing safety rules
- Make minimal diffs only.
- Preserve existing variable names unless explicitly asked to rename.
- Preserve node/link integrity and avoid unrelated refactors.
- If a command/field cannot be verified in-repo, do not add it.
- For layout-only cleanup, use the XML “layout tidy” step: detect top-level event-entry threads (`<Instructions>` blocks beginning with `<Event ...>`), then reassign block `pos` coordinates into separated lanes with consistent spacing while preserving IDs, ordering, and all logic/link structure.

### 5) Knowledge base policy
- Maintain `vizzy_kb/` when command/telemetry verification work is requested.
- Add VERIFIED entries only when backed by explicit repo evidence.
- Include source references (file path + line/snippet identifiers) for each new KB item.

### 6) Open unknowns
- Some node/link wiring semantics across nested and custom-instruction constructs remain incompletely indexed (**PARTIALLY VERIFIED** via `Reference.xml`).
- Exhaustive validated command list for this specific repo is not yet extracted (**UNVERIFIED**).
- Exhaustive validated telemetry/toolkit field list for this specific repo is not yet extracted (**UNVERIFIED**).

### 7) Versioning protocol
- `VERSION` is the source of truth and uses `MAJOR.REVISION` (example progression: `1.1` -> `1.11` -> `1.12`).
- Every non-major change must bump by at least `+0.01` equivalent using `scripts/bump_version.sh change`.
- Use `scripts/bump_version.sh major` only for major/breaking changes.
- For release artifacts, align XML program naming/file labels with the updated version where practical.
- Every version bump should be accompanied by a `agents.md` change-log entry summarizing impact.

### 8) Change log
- 2026-02-21
  - Created `agents.md` as the authoritative, repo-specific operating contract.
  - Converted generic template content into current verified facts + explicit unknowns.
- 2026-02-22
  - Added repository versioning protocol using root `VERSION` + `scripts/bump_version.sh`.
  - Documented required version-bump linkage to change-log maintenance.
- 2026-02-22
  - Updated versioning policy to `MAJOR.REVISION` with minimum `+0.01` equivalent bump for every non-major change.
  - Updated bump helper usage to `change|major`.
  - Bumped `VERSION` to `3.12` for this repository policy update.

- 2026-02-22
  - Updated `Quadcopter Flight Program V3.xml` so `target_alt_agl` is recomputed inside the main while-loop as `Altitude.AGL + 1000`.
  - Bumped `VERSION` to `3.13` for this quadcopter altitude-target behavior update.

- 2026-02-22
  - Repaired `Quadcopter Flight Program V3.xml` control math/logic: replaced self-referential `slider1` writes with explicit throttle commands for landing/nav/altitude-hold branches.
  - Updated altitude-target policy in main loop: if `manual_override == 1` set `hold_alt_agl = Altitude.AGL`, else set `target_alt_agl = Altitude.AGL + 500`.
  - Bumped `VERSION` to `3.14` for this quadcopter control reliability and altitude-target behavior update.


- 2026-02-22
  - Updated `Quadcopter Flight Program V3.xml` to add a dedicated FlightStart/while loop that continuously tunes variable-pitch prop angle for thrust using `Vel.VerticalSurfaceVelocity`, starting at 50 degrees and clamped to 0-90.
  - Bumped `VERSION` to `3.15` for this quadcopter variable-pitch control enhancement.

- 2026-02-22
  - Refined `Quadcopter Flight Program V3.xml` variable-pitch thread to optimize against `Performance.CurrentEngineThrust` instead of vertical speed.
  - Added fail-safe/default behavior in variable-pitch control: force 50° when landing is armed, when thrust is near zero, or when `Input.Throttle` stays at zero for more than 2 seconds.
  - Bumped `VERSION` to `3.16` for this quadcopter variable-pitch thrust-control refinement.

- 2026-02-22
  - Refactored `Quadcopter Flight Program V3.xml` into clearer thread separation by introducing a dedicated activation/state-manager FlightStart loop (AG1/AG2/AG3/AG4 command decoding + mode transitions), while keeping flight-control and prop-pitch logic in their own loops.
  - Updated quadcopter startup state so all activation-driven state flags initialize false except `landing_armed=1` to reflect landed-safe startup.
  - Added explicit manual-to-takeoff handoff behavior: AG1 transition writes `manual_override=0` before enabling auto hold/takeoff state.
  - Expanded `logic-table.md` with a comprehensive quadcopter activation/mode/thread logic table and transition priorities.
  - Bumped `VERSION` to `3.17` for this quadcopter state-machine/thread refactor update.

- 2026-02-22
  - Updated `scripts/bump_version.sh` to automatically sync version-tagged XML `<Program name="...">` labels to the newly bumped `VERSION` value.
  - Auto-updated `Flight Program R V3.0.xml` and `Quadcopter Flight Program V3.xml` program names to `V3.18` during the version bump.
  - Bumped `VERSION` to `3.18` for XML program-version tracking automation.

- 2026-02-22
  - Added targeted thread comments to `Quadcopter Flight Program V3.xml` to document throttle-output, heading-output, activation-state, and prop-pitch loops.
  - Added operator-facing startup and target-reached flight log entries in `Quadcopter Flight Program V3.xml` while preserving existing display messages.
  - Bumped `VERSION` to `3.19` for quadcopter comments + telemetry visibility updates.

- 2026-02-22
  - Hardened all `Quadcopter Flight Program V3.xml` runtime threads by adding defensive command bounds and state-guard logic.
  - Added throttle-thread clamp protection to constrain `throttle_cmd` into [0,1] before applying `slider1` output.
  - Added pitch/heading-thread clamp and normalization protection to keep `pitch_cmd` in [0,90] and `nav_heading_cmd` in [0,360] before heading outputs.
  - Added activation-state thread safety enforcement (`thread_safe_mode`) so manual override always clears auto/nav/heading-hold states.
  - Bumped `VERSION` to `3.20` for this quadcopter thread-hardening update.

- 2026-02-22
  - Updated `Quadcopter Flight Program V3.xml` navigation pitch behavior to use heading-gated, staged tilt control: forward tilt only after heading alignment, reverse tilt for deceleration near target, and neutral 90° pitch at final settle.
  - Added `nav_heading_error_deg` computation using `Nav.CraftHeading` to gate translational tilt until heading error is small and wrapped into [0,180].
  - Bumped `VERSION` to `3.21` for controlled navigation-tilt and braking behavior integration.

- 2026-02-22
  - Standardized a repo-wide Vizzy state-machine scaffold in `Flight Program R V3.0.xml`, `gpttest.xml`, and `Quadcopter Flight Program V3.xml` using shared state variables (`ProgramState`, `RequestedState`, `StateChangePending`, `*Active`) and `STATE_*` Broadcast/Receive entrypoints.
  - Added `docs/VIZZY_STATE_MACHINE_PATTERN.md` documenting required architecture and per-program state maps/triggers.
  - Extended `logic-table.md` with state-standardization notes and quadcopter compatibility mapping to legacy mode flags.
  - Bumped `VERSION` to `3.22` for the repo-wide state-machine standardization pass.

- 2026-02-22
  - Fixed `Quadcopter Flight Program V3.xml` activation-command handling by wiring AG1/AG2/AG3/AG4 transitions to broadcast `STATE_*` messages and update `RequestedState`/`StateChangePending`, so program state modules now change with activation inputs.
  - Updated state receive behavior for `STATE_STANDBY` and `STATE_ORBIT` to keep mode flags (`manual_override`, `auto_enabled`, `nav_enabled`, `landing_armed`) synchronized with active program mode.
  - Auto-updated `Flight Program R V3.0.xml` and `Quadcopter Flight Program V3.xml` program names to `V3.23` during version bump.
  - Bumped `VERSION` to `3.23` for activation-state-to-mode synchronization repair.

- 2026-02-22
  - Reworked `Quadcopter Flight Program V3.xml` state-thread interactions by introducing a dedicated state-transition dispatcher FlightStart loop that emits `STATE_*` craft broadcasts only when `StateChangePending == 1` and keyed by `RequestedState`.
  - Updated AG1/AG2/AG3/AG4 activation-state manager thread to request states via `RequestedState`/`StateChangePending` without direct inline broadcast calls, so transitions are routed through one broadcast owner thread.
  - Auto-updated `Flight Program R V3.0.xml` and `Quadcopter Flight Program V3.xml` program names to `V3.24` during version bump.
  - Bumped `VERSION` to `3.24` for state-thread broadcast-dispatch reliability hardening.

- 2026-02-22
  - Updated `Quadcopter Flight Program V3.xml` altitude-control variable model to use `target_alt_agl` (startup user-set offset), `auto_alt_agl` (`Altitude.AGL + target_alt_agl` in auto/nav), and `hover_alt_agl`/`hover_alt_target` capture for hover hold behavior.
  - Replaced stepped hover/nav throttle setpoints in `Quadcopter Flight Program V3.xml` with a damped altitude controller using altitude error and `Vel.VerticalSurfaceVelocity` to reduce pogoing while preserving output clamping via the slider-output thread.
  - Kept Slider2 fully program-driven for prop-pitch optimization and retained existing state-message filtering/broadcast architecture.
  - Auto-updated `Flight Program R V3.0.xml` and `Quadcopter Flight Program V3.xml` program names to `V3.25` during version bump.
  - Bumped `VERSION` to `3.25` for quadcopter altitude-control and startup-target refactor.

- 2026-02-22
  - Added `scripts/vizzy_layout_tidy.py` to perform XML layout-only tidying by detecting event-entry threads and assigning lane-based block coordinates with consistent spacing and reduced overlap while preserving logic/IDs/connections.
  - Ran layout tidy across `Flight Program R V3.0.xml`, `Quadcopter Flight Program V3.xml`, `gpttest.xml`, and `Reference.xml` to produce cleaner Vizzy canvas organization.
  - Auto-updated `Flight Program R V3.0.xml` and `Quadcopter Flight Program V3.xml` program names to `V3.26` during version bump.
  - Bumped `VERSION` to `3.26` for XML layout tidying automation and repo-wide layout cleanup pass.

- 2026-02-22
  - Added `docs/STEAM_GUIDE_VECTORS_AND_PIDS_NOTES.md` summarizing practical vector/PID control lessons from the reviewed Steam guide (`id=2944674093`) for local documentation reuse.
  - Auto-updated `Flight Program R V3.0.xml` and `Quadcopter Flight Program V3.xml` program names to `V3.27` during version bump.
  - Bumped `VERSION` to `3.27` for this documentation/research-notes update.

- 2026-02-22
  - Added `docs/STEAM_GUIDE_ORBITAL_TOOLKIT_INACCURACY_NOTES.md` summarizing the reviewed Steam guide (`id=3039843312`) with a focus on low-warp numerical-integration drift and practical mitigation workflow for maneuver planning.
  - Auto-updated `Flight Program R V3.0.xml` and `Quadcopter Flight Program V3.xml` program names to `V3.28` during version bump.
  - Bumped `VERSION` to `3.28` for this Steam-guide inaccuracy documentation update.

- 2026-02-22
  - Added `docs/STEAM_GUIDE_MFD_HUD_NOTES.md` distilling Steam guide `id=2954199325` into practical MFD HUD build/programming notes (transparent panel setup, widget hierarchy workflow, coordinate/update model, and target-node caveats).
  - Auto-updated `Flight Program R V3.0.xml` and `Quadcopter Flight Program V3.xml` program names to `V3.29` during version bump.
  - Bumped `VERSION` to `3.29` for this MFD HUD documentation update.
