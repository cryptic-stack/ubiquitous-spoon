# Asset Context Engine

SentinelMesh must enrich every alert, log, and network event with maximum practical context.

The asset context engine turns passive network telemetry, active vulnerability findings, and external enrichment data into a continuously updated asset memory layer.

## Service

Service name:

- `asset-context`

Container name:

- `sm-asset-context`

Profiles:

- `standalone`
- `manager`
- `manager-search`
- `cyber-range`
- `dev-lab`

The service runs near the management/search tier because it needs access to indexed event history, asset records, vulnerability records, and enrichment datasets.

## Core Principle

Every alert, log, and network event should answer:

- What asset is involved?
- What vulnerabilities exist?
- What risk level applies?
- What exposure exists?
- What history is known?

## Data Sources

Passive:

- Zeek `conn`, `dns`, `ssl`, `http`, and `files` logs
- Suricata EVE logs
- Arkime session metadata

Active:

- Optional vulnerability scanners
- Optional network scans

External:

- Threat intelligence feeds
- GeoIP databases
- ASN databases
- MAC vendor lookup

## Asset Model

The initial schema lives at:

- `schemas/asset-context.schema.json`

Canonical shape:

```json
{
  "asset_id": "uuid",
  "ip_addresses": [],
  "mac_addresses": [],
  "hostnames": [],
  "fqdn": "",
  "first_seen": "",
  "last_seen": "",
  "os_guess": "",
  "services": [],
  "open_ports": [],
  "protocols": [],
  "users_observed": [],
  "risk_score": 0,
  "criticality": "low",
  "tags": [],
  "vulnerabilities": [],
  "exposure": {
    "internet_facing": false,
    "internal_only": true
  }
}
```

## Storage

MVP storage target:

- OpenSearch index `sentinelmesh-assets`

Index templates:

- `configs/opensearch/index-templates/sentinelmesh-assets.json`
- `configs/opensearch/index-templates/sentinelmesh-events.json`

Install templates on an appliance:

```bash
sudo sm-install-index-templates
```

Future storage candidates:

- PostgreSQL for authoritative relational asset records
- OpenSearch for search and enrichment joins
- Local cache for high-volume enrichment lookups

## Enrichment Flow

```text
Zeek / Suricata / Arkime
  |
  v
collector / ingest pipeline
  |
  v
asset-context
  |
  +--> update asset record
  +--> update vulnerability state
  +--> calculate risk score
  +--> enrich events before indexing or during query
  |
  v
OpenSearch
```

## Risk Scoring MVP

Risk score should be numeric from `0` to `100`.

Initial inputs:

- Asset criticality
- Number and severity of vulnerabilities
- Internet exposure
- Sensitive service exposure
- Recent alert activity
- Threat intelligence matches
- Observed user/account context

Initial criticality mapping:

- `low`: 0-24
- `medium`: 25-49
- `high`: 50-79
- `critical`: 80-100

Current MVP implementation:

- Normalizes seed asset records.
- Generates stable asset IDs from observed identifiers when missing.
- Calculates capped risk scores from criticality, vulnerabilities, exposure, and sensitive open ports.
- Emits an explainable `risk_breakdown`.
- Loads optional seed assets from `SENTINELMESH_ASSET_SEED_PATH`.

Sample seed data:

- `services/asset-context/sample-assets.json`

## Vulnerability Awareness

Vulnerability records should track:

- Vulnerability ID, such as CVE or scanner plugin ID
- Scanner/source name
- Severity
- CVSS score where available
- First seen
- Last seen
- Status
- Affected service or port
- Evidence

Optional scanners are intentionally not hardcoded yet. The service contract should allow imports from tools such as authenticated scanners, network scanners, or future SentinelMesh-native checks.

## Vulnerability Imports

Import schema:

- `schemas/vulnerability-import.schema.json`

Sample import:

- `examples/vulnerability-import/sample-vuln-import.json`

Stage an import on the appliance:

```bash
sudo sm-import-vulnerabilities --file /path/to/findings.json
```

MVP behavior:

- Validate JSON syntax.
- Copy import into `/data/sentinelmesh/imports/vulnerabilities`.
- Leave correlation and asset merge work for the asset-context ingestion phase.

## Open Questions

- Should authoritative asset records live only in OpenSearch for MVP, or should we add PostgreSQL early?
- Should enrichment happen before indexing, after indexing, or both?
- Which scanner format should be supported first?
- Should cyber-range mode allow instructor-controlled synthetic asset and vulnerability context?
