# Vizzy State Machine Pattern (Repository Standard)

## Canonical variables
- `ProgramState` (int enum): `0=Standby, 1=Ascent, 2=Orbit, 3=Landing, 4=Hover`.
- `RequestedState` (int enum request channel).
- `StateChangePending` (bool/int).
- Per-state gates: `StandbyActive`, `AscentActive`, `OrbitActive`, `LandingActive`, `HoverActive`.

## Canonical messages
State transitions are requested/announced with craft-scope broadcast messages:
- `STATE_STANDBY`
- `STATE_ASCENT`
- `STATE_ORBIT`
- `STATE_LANDING`
- `STATE_HOVER`

## Required wiring pattern
1. **State manager owns state**:
   - Initialize all state variables at `FlightStart`.
   - Request a default startup state (`STATE_STANDBY`).
2. **Receive entrypoints per state**:
   - One `ReceiveMessage` event per `STATE_*`.
   - On receipt: clear all `*Active` flags, then set exactly one active flag and set `ProgramState`.
3. **Controller loops are state-gated**:
   - Long-running control loops must check the relevant `*Active` gate (or equivalent state variable) to avoid post-transition output contention.
4. **Activation groups request state only**:
   - AG toggles should request transition (typically via broadcast), not directly fight controller outputs.

## Program state maps

### `Quadcopter Flight Program V3.xml`
| State | Message | Trigger source | Primary effect |
|---|---|---|---|
| Standby | `STATE_STANDBY` | startup default / explicit request | clears auto/nav output ownership |
| Ascent | `STATE_ASCENT` | AG1 takeoff/hold request path | enables auto and clears landing/manual latch |
| Orbit | `STATE_ORBIT` | reserved for transit/cruise mode | marks cruise/orbit active for shared pattern consistency |
| Landing | `STATE_LANDING` | AG2 landing request path | arms landing and drops nav ownership |
| Hover | `STATE_HOVER` | AG4/nav-hold request path | enables auto hover-like hold path |

### `Flight Program R V3.0.xml`
| State | Message | Trigger source | Mapping note |
|---|---|---|---|
| Standby | `STATE_STANDBY` | startup default | maps to pre-countdown safe state |
| Ascent | `STATE_ASCENT` | launch progression | aligns with existing ascent guidance ownership |
| Orbit | `STATE_ORBIT` | circularization completion path | aligns with on-orbit operations |
| Landing | `STATE_LANDING` | fallback/manual abort extension | reserved for future RTLS/landing module |
| Hover | `STATE_HOVER` | N/A (non-VTOL) | included as standard enum slot |

### `gpttest.xml`
Uses the same message/variable pattern as `Flight Program R V3.0.xml` for parity test coverage and migration rehearsal.

## Notes
- Existing tuning math/constants were preserved.
- This refactor standardizes state ownership channels and receive entrypoints first, while keeping existing control computations intact.
