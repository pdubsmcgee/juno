# agents.md

## DeltaVinci Operating Contract (Repo-Scoped)

### 1) Operating mode
- Adversarial self-verification only.
- Repository-grounded facts only (no guessed Vizzy syntax/telemetry/toolkit fields).
- Unknown features must be marked **UNVERIFIED** and excluded from XML edits.

### 2) Current repository index
- Vizzy XML exports:
  - `Flight Program R V3.0.xml`
- Agent/reference docs:
  - `You are “DeltaVinci”.txt`
  - `agents.md.txt` (legacy template)
  - `agents.md` (this authoritative file)

### 3) Verified structural facts (from current repo)
- Vizzy program root element is `<Program name="...">`.  
  Evidence: `Flight Program R V3.0.xml`
- Global variables are declared under `<Variables>` with `<Variable name="..." number="..." />` entries.  
  Evidence: `Flight Program R V3.0.xml`
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
- Concrete node/block schema and wiring format are not yet indexed in this repo-level KB (**UNVERIFIED**).
- Exhaustive validated command list for this specific repo is not yet extracted (**UNVERIFIED**).
- Exhaustive validated telemetry/toolkit field list for this specific repo is not yet extracted (**UNVERIFIED**).

### 7) Change log
- 2026-02-21
  - Created `agents.md` as the authoritative, repo-specific operating contract.
  - Converted generic template content into current verified facts + explicit unknowns.
