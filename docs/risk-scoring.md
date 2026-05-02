# Risk Scoring

SentinelMesh risk scoring prioritizes alerts and investigations based on asset context, vulnerability state, exposure, and recent behavior.

## Score Range

Risk score:

- Minimum: `0`
- Maximum: `100`

Criticality:

- `low`: 0-24
- `medium`: 25-49
- `high`: 50-79
- `critical`: 80-100

## MVP Formula

Initial formula:

```text
risk_score =
  asset_criticality_weight
  + vulnerability_weight
  + exposure_weight
  + alert_activity_weight
  + threat_intel_weight
  + user_context_weight
```

The score must be capped at `100`.

## Initial Weights

Asset criticality:

- low: 5
- medium: 15
- high: 25
- critical: 35

Vulnerability severity:

- low vulnerability: +2
- medium vulnerability: +5
- high vulnerability: +10
- critical vulnerability: +20

Exposure:

- internal only: +0
- internet facing: +20
- sensitive service exposed: +10

Recent alert activity:

- low: +5
- medium: +10
- high: +20

Threat intelligence:

- weak match: +5
- medium confidence match: +10
- high confidence match: +20

User context:

- privileged user observed: +10
- service account observed: +5
- unknown user on sensitive service: +10

## Design Rule

Risk scoring must be explainable.

Every calculated score should eventually include a breakdown showing why the score was assigned.

