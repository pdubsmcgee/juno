# Verified Vizzy Index (Repo-Extracted)

Generated from `Flight Program R V3.0.xml` and `Reference.xml` using local extraction.
Only repository-observed commands/properties are listed (no external assumptions).

## Flight program command/node tags observed (top 25 by frequency)

- `SetVariable`: 242
- `Comparison`: 105
- `If`: 84
- `BinaryOp`: 82
- `VectorOp`: 43
- `CraftProperty`: 41
- `WaitSeconds`: 38
- `ElseIf`: 14
- `LogFlight`: 14
- `Comment`: 11
- `WaitUntil`: 11
- `MathFunction`: 11
- `While`: 10
- `Event`: 7
- `LockNavSphere`: 7
- `DisplayMessage`: 7
- `BoolOp`: 6
- `SetInput`: 6
- `Break`: 6
- `Not`: 5
- `ActivationGroup`: 5
- `SetTargetHeading`: 4
- `Planet`: 4
- `SetCraftProperty`: 4
- `UserInput`: 3

## Reference syntax catalog coverage (`Reference.xml`)

- `Instructions` groups: 48
- Unique instruction tags represented: 30
- High-coverage selector families included:
  - `SetInput` (13 variants)
  - `SetTimeMode` (14 variants)
  - `LockNavSphere` (7 variants)
  - `SetCameraProperty` (7 variants)
  - `SetCraftProperty` (6 variants)

## CraftProperty fields observed in flight program

- `Altitude.AGL`: 2
- `Fuel.FuelInStage`: 1
- `Input.Throttle`: 2
- `Nav.AngleOfAttack`: 3
- `Nav.East`: 3
- `Nav.North`: 1
- `Nav.Position`: 5
- `Orbit.Apoapsis`: 4
- `Orbit.Periapsis`: 1
- `Performance.CurrentEngineThrust`: 2
- `Performance.Mass`: 2
- `Performance.MaxActiveEngineThrust`: 3
- `Vel.Gravity`: 5
- `Vel.OrbitVelocity`: 4
- `Vel.SurfaceVelocity`: 3

## Source
- `Flight Program R V3.0.xml`
- `Reference.xml`
- `agents.md` (verification policy context)
