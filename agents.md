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
  - `VERSION` (semantic version, currently `3.0.2`)
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
- Semantic version source of truth is the repo-root `VERSION` file.
- Use `scripts/bump_version.sh {patch|minor|major}` when behavior/docs change.
- For release artifacts, align XML program naming/file labels with the updated semantic version where practical.
- Every version bump should be accompanied by a `agents.md` change-log entry summarizing impact.

### 8) Change log
- 2026-02-21
  - Created `agents.md` as the authoritative, repo-specific operating contract.
  - Converted generic template content into current verified facts + explicit unknowns.
- 2026-02-22
  - Added repository versioning protocol using root `VERSION` + `scripts/bump_version.sh`.
  - Documented required version-bump linkage to change-log maintenance.

- 2026-02-22
  - Added `Reference.xml` as an explicit repository syntax source for block/tag/selector verification.
  - Updated verification posture to treat broad block schema coverage as partially verified in-repo.
