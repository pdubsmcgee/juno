# XML Program Issue Backlog (Project Stubs)
Based on a static pass over `Flight Computer R V1.5.xml`, these project stubs target likely cleanup/quality issues.
## Stub 1 — Guidance variable namespace consolidation
- **Issue:** Legacy guidance variables are still declared but appear unreferenced, while `gt_*` variables are actively referenced.
- **Evidence (declared legacy):** `tsv`, `tev`, `targetAlt`, `MaxAoA`, `targetpitch`, `pitchCmd`, `targetinc`, `headingtarget`, `headingCmd`.
- **Evidence (active replacements):** `gt_tsv`, `gt_tev`, `gt_maxaoa`, `gt_pitchcmd`, `targetinc_deg`.
- **Stub tasks:**
  - [ ] Map each legacy variable to current equivalent (`gt_*` or renamed variable).
  - [ ] Delete legacy declarations that are confirmed dead.
  - [ ] Add migration notes in comments/doc for future edits.

## Stub 2 — Throttle command path completion
- **Issue:** `thrcmd` and `thrcmdvalid` are declared but currently appear unreferenced, suggesting an incomplete throttle authority handoff path.
- **Stub tasks:**
  - [ ] Confirm whether throttle should be computed by this flight computer or external logic.
  - [ ] Either wire reads/writes into active instruction flow or remove declarations.
  - [ ] Add a single source-of-truth variable for throttle authority ownership.

## Stub 3 — General dead-variable debt sweep
- **Issue:** 22 declared globals currently have no `variableName="..."` usage in the program body.
- **Stub tasks:**
  - [ ] Run per-variable classification: **remove**, **keep for external API**, or **wire into flow**.
  - [ ] Remove confirmed-dead variables in small batches with regression checks.
  - [ ] Keep an “externally consumed variables” allowlist to avoid accidental deletion.

## Candidate unused variables (static detection)
- `tsv` (declared line 27)
- `tev` (declared line 28)
- `targetAlt` (declared line 29)
- `MaxAoA` (declared line 30)
- `targetpitch` (declared line 32)
- `a` (declared line 34)
- `pitchCmd` (declared line 35)
- `cirv` (declared line 36)
- `burntime` (declared line 39)
- `rp` (declared line 41)
- `circ` (declared line 42)
- `targetinc` (declared line 46)
- `incerror` (declared line 47)
- `headingtarget` (declared line 48)
- `headingCmd` (declared line 49)
- `pitchmin` (declared line 51)
- `scale` (declared line 52)
- `vhagl` (declared line 54)
- `pitchbiasapo` (declared line 56)
- `turn` (declared line 57)
- `thrcmd` (declared line 115)
- `thrcmdvalid` (declared line 116)
