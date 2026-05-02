# Next Steps

This is the next practical build plan after the SOC portal, Grafana embedding, grouped Hunt pivots, event-derived relationships, and seeded OpenSearch ingest work.

## Immediate Priority

Focus next on making the appliance produce and preserve real NSM evidence.

The current SOC workflow is useful enough to validate operator ideas, but it still depends mostly on seeded and offline-processed events. The highest-value next work is always-on sensor capture, reliable ingest, and PCAP retrieval.

## Sprint 1 - Real Sensor Data Path

Goal: prove the stack can capture traffic, parse it, index it, and display it without manual seed scripts.

Tasks:

- Configure Suricata to write EVE JSON from the selected monitor interface into the shared sensor log path.
- Configure Zeek to write JSON logs from the selected monitor interface into the shared sensor log path.
- Normalize sensor log directories under a predictable host path such as `/nsm/sensor/logs`.
- Decide whether Vector stays in the live collector path, Logstash reads files directly, or both are used by role.
- Add Compose health checks for Suricata, Zeek, Logstash, OpenSearch, SOC, Prometheus, and Grafana.
- Add ingest counters for events read, events indexed, parser errors, and event lag.

Acceptance checks:

- Bring up `dev-lab` or `standalone`.
- Replay a PCAP or generate local test traffic.
- Confirm Suricata and Zeek produce logs.
- Confirm OpenSearch receives Suricata alerts/flows and Zeek protocol records.
- Confirm SOC Overview, Hunt, Relationships, and embedded Grafana graphs update from those events.

## Sprint 2 - PCAP Evidence And Pivoting

Goal: let an analyst move from alert or hunt result to packet evidence.

Tasks:

- Choose the first PCAP implementation: Stenographer, Suricata PCAP mode, or both staged behind one API.
- Replace the Stenographer placeholder with a working capture container or documented Suricata PCAP mode.
- Define storage paths for rolling PCAP, extracted PCAP, and exported evidence.
- Add retention controls based on max disk usage and reserved free space.
- Add a `pcap-api` service with time/IP/port/protocol lookup parameters.
- Wire SOC event pivots to call the PCAP API instead of only showing command placeholders.

Acceptance checks:

- Replayed or live traffic creates rolling packet capture.
- A SOC event can request matching packet evidence.
- PCAP retrieval respects storage limits and returns a bounded artifact.

## Sprint 3 - Asset Context From Events

Goal: move asset context from seed files toward continuous passive discovery.

Tasks:

- Have `asset-context` consume Zeek conn, DNS, SSL, HTTP, and Suricata EVE records.
- Write normalized asset records to `sentinelmesh-assets`.
- Add merge logic for IPs, hostnames, MACs, services, users, and timestamps.
- Enrich events with asset ID, criticality, exposure, vulnerability count, and risk score.
- Add SOC asset detail view with observed services, related alerts, vulnerabilities, and relationships.

Acceptance checks:

- New event data creates or updates asset records.
- Alerts and Hunt rows show resolved asset context where available.
- Relationship views prefer asset names but preserve raw IPs.

## Sprint 4 - Operator Workflow State

Goal: move from read-only dashboards to analyst work.

Tasks:

- Add authentication for SOC local access.
- Add persistent alert state: new, acknowledged, escalated, closed, false positive.
- Add basic case records with title, status, owner, observables, notes, and linked events.
- Add pivots from Alerts/Hunt/Relationships into a case.
- Add saved Hunt queries and saved dashboard filters.

Acceptance checks:

- An analyst can acknowledge an alert, create a case, attach events, add notes, and return later.
- Case and alert state survive container restarts.

## Sprint 5 - Detection Lifecycle

Goal: start closing the Security Onion Detections gap.

Tasks:

- Define detection metadata for Suricata rules, Sigma rules, and future YARA content.
- Track rule source, version, enabled state, tuning notes, and test status.
- Add rule import and sync workflow around `sm-update-rules`.
- Add detection detail page in SOC with related events and suggested pivots.
- Decide Sigma execution path: ElastAlert 2, OpenSearch Alerting, or a SentinelMesh-native alert engine.

Acceptance checks:

- A rule can be imported, tracked, disabled/enabled, and linked to generated alerts.

## Engineering Notes

- Keep mirroring Security Onion's operator flow: Alerts, Dashboards, Hunt, Cases, Detections, PCAP, Grid, and pivots.
- Keep Grafana for charts and wallboards, but keep analyst action in the SOC portal.
- Keep Prometheus for time-series metrics only; OpenSearch remains the event/search datastore.
- Keep asset context as a first-class enrichment layer rather than a dashboard-only feature.
- Document every interface as it appears so future tweaks are easy.
