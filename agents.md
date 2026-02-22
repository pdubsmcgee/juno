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
