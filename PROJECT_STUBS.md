# XML Program Issue Backlog (Project Stubs)
Based on a static pass over `Flight Computer R V1.5.xml`, these project stubs target likely cleanup/quality issues.

## Stub 1 — Guidance variable namespace consolidation
- **Status:** Completed (static XML reference audit + declaration cleanup).
- **Issue:** Legacy guidance variables were declared but unreferenced, while `gt_*` variables are actively referenced.
- **Migration mapping (legacy → active equivalent):**
  - `tsv` → `gt_tsv`
  - `tev` → `gt_tev`
  - `MaxAoA` → `gt_maxaoa`
  - `pitchCmd` / `targetpitch` / `pitchmin` → `gt_pitchcmd` / `gt_pitchmin`
  - `headingCmd` / `headingtarget` / `targetinc` → `gt_headingcmd` / `targetinc_deg`
- **Actions taken:**
  - [x] Mapped each legacy variable to current equivalent (`gt_*` or renamed variable).
  - [x] Deleted legacy declarations confirmed dead by zero `variableName="..."` references.
  - [x] Added migration notes in this backlog doc for future edits.

## Stub 2 — Throttle command path completion
- **Status:** Deferred (external interface ownership unresolved from in-repo evidence).
- **Issue:** `thrcmd` and `thrcmdvalid` are declared but currently unreferenced in the instruction body.
- **Decision for now:** Keep both variables as an **externally consumed/API allowlist** pair until throttle authority ownership is explicitly specified.
- **Remaining tasks:**
  - [ ] Confirm whether throttle should be computed by this flight computer or external logic.
  - [ ] Either wire reads/writes into active instruction flow or remove declarations.
  - [ ] Add a single source-of-truth variable for throttle authority ownership.

## Stub 3 — General dead-variable debt sweep
- **Status:** Partially completed.
- **Actions taken:**
  - [x] Ran per-variable classification against static `variableName="..."` usage.
  - [x] Removed confirmed-dead variables in one audited batch (all dead candidates except throttle allowlist).
  - [x] Established allowlist policy entry for externally consumed variables: `thrcmd`, `thrcmdvalid`.

## Static classification results (current)
### Removed as dead declarations (no body references)
- `tsv`
- `tev`
- `targetAlt`
- `MaxAoA`
- `targetpitch`
- `a`
- `pitchCmd`
- `cirv`
- `burntime`
- `rp`
- `circ`
- `targetinc`
- `incerror`
- `headingtarget`
- `headingCmd`
- `pitchmin`
- `scale`
- `vhagl`
- `pitchbiasapo`
- `turn`

### Kept as external API allowlist (unreferenced internally)
- `thrcmd`
- `thrcmdvalid`
