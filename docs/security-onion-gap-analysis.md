# Security Onion Gap Analysis And Closure Plan

This document compares the current SentinelMesh build against Security Onion 2.4 design patterns and analyst capabilities. It is intentionally practical: each gap should point to work we can build, validate, and improve later.

References checked:

- Security Onion Architecture: https://docs.securityonion.net/en/2.4/architecture.html
- Security Onion Ingest: https://docs.securityonion.net/en/2.4/ingest.html
- Security Onion Console: https://docs.securityonion.net/en/2.4/soc.html
- Security Onion Introduction: https://docs.securityonion.net/en/2.4/introduction.html
- Security Onion Detections: https://docs.securityonion.net/en/2.4/detections.html
- Security Onion Rules: https://docs.securityonion.net/en/2.4/rules.html

## Current Alignment

SentinelMesh already aligns with several Security Onion principles:

- One appliance image with role selection after install.
- Containerized services running inside the Ubuntu Server appliance.
- Role profiles for `standalone`, `manager`, `manager-search`, `search`, `sensor`, `receiver`, `cyber-range`, and `dev-lab`.
- Sensor-oriented components for Suricata, Zeek, Arkime, and Stenographer.
- Manager/search-oriented components for Redis, Logstash, OpenSearch, Dashboards, SOC portal, and enrollment.
- Full packet capture intended to stay local to sensors.
- Receiver profile included for future active-active ingestion and pipeline redundancy.
- Asset context, vulnerability import, risk scoring, and relationship visualization extend beyond baseline NSM.

## Gap Severity Model

- P0: Required before a believable MVP appliance.
- P1: Required before a useful SOC workflow.
- P2: Required before distributed/production use.
- P3: Enhancements that differentiate SentinelMesh after parity improves.

## Gap Matrix

| Area | Security Onion Baseline | SentinelMesh Current State | Gap | Priority |
| --- | --- | --- | --- | --- |
| Sensor ingest | Sensor forwards Zeek, Suricata, and syslog through an agent/pipeline to Logstash/search. | Suricata/Zeek containers exist. Logstash can read Suricata/Zeek-shaped JSON from sensor log volumes and index into OpenSearch. | Seeded event ingest exists; live capture and distributed forwarding are still incomplete. | P0 |
| Packet capture | Stenographer or Suricata writes full packet capture locally on sensors; SOC can pivot to PCAP. | Arkime/Stenographer are placeholders; replay script exists. | No working rolling PCAP spool or retrieval workflow. | P0 |
| Search datastore | Elasticsearch-backed search nodes receive parsed logs from Logstash. | OpenSearch exists with initial templates and MVP `sentinelmesh-events-*` Logstash output. | Mappings are not production-ready; no volume sizing or lifecycle policy. | P0 |
| SOC analyst UX | SOC includes Alerts, Dashboards, Hunt, Cases, Detections, PCAP, Grid, and pivots to external tools. | Static SOC portal scaffold plus OpenSearch Dashboards and Grafana. | No real Alerts/Hunt/Cases/PCAP/Grid workflow. | P1 |
| Detection management | Detections manages NIDS, Sigma, and YARA rules, tuning, synchronization, and playbooks. | Rule directories and `sm-update-rules` manifest workflow exist. | No rule compiler/sync engine, tuning UI, or alerting engine integration. | P1 |
| Endpoint visibility | Elastic Agent, Fleet, osquery, and endpoint logs are supported. | Sensor enrollment exists; no endpoint agent management. | No host telemetry path, osquery/live query, or Fleet-like control plane. | P2 |
| Syslog ingestion | Syslog is part of common ingest flows. | No dedicated syslog receiver config yet. | Network devices cannot send logs into the stack cleanly. | P1 |
| Receiver resilience | Receiver nodes provide load-balanced Logstash/Redis queue redundancy. | Receiver profile exists. | No enrollment output, load-balanced outputs, or search-node pull model. | P2 |
| Grid management | SOC exposes grid/node management and service health. | `sm-doctor` is local CLI only. | No centralized node inventory, heartbeat, or service status UI. | P2 |
| Case management | Cases store investigations, observables, comments, attachments, and analyst assignment. | Not implemented. | No case database or pivot flow from alerts/events. | P1 |
| Alert workflow | Alerts can be queried, grouped, acknowledged, escalated, and pivoted. | Not implemented except raw OpenSearch/Dashboards path. | No first-class alert API or analyst state. | P1 |
| Guided analysis | Playbooks guide alert investigation. | Not implemented. | No playbook model or detection-to-playbook binding. | P2 |
| File analysis/YARA | YARA and Strelka-style file analysis are part of detection management. | YARA rule directory exists conceptually. | No file extraction pipeline, scanner, verdict storage, or UI. | P2 |
| Threat intel | Security Onion supports pivots and enrichment workflows. | Asset context has planned TI/GeoIP/ASN enrichment. | No operational feed loader or enrichment cache. | P1 |
| Asset/risk context | Security Onion is detection-centric; SentinelMesh adds asset/risk context. | Asset context and relationship metrics are seeded MVP services. | Need real event ingestion, OpenSearch writes, and enrichment joins. | P1 |
| Install/update | Security Onion has mature install/update and service orchestration. | Ubuntu autoinstall/Packer scripts are started. | ISO build is not VM-proven; updates are not signed or orchestrated. | P0 |
| Security hardening | Production deployments require TLS, auth, secrets, and least privilege. | Dev credentials and basic placeholders exist. | OpenSearch/Grafana/service auth and TLS are not hardened. | P0 |
| Airgap/offline | Security Onion supports offline-style operational needs. | Image preload and signed bundles are only future work. | No offline image/rule/update bundle strategy. | P2 |
| Observability | Security Onion has service health; SentinelMesh adds Prometheus/Grafana. | Prometheus, Grafana, and relationship metrics work in dev-lab. | Need service health metrics, ingest lag, queue depth, capture loss, and disk pressure dashboards. | P1 |

## Closure Plan

### Phase A - Make The Stack Produce Real NSM Data

Goal: Turn current containers from scaffold into a believable standalone NSM.

Work:

- Configure Suricata to write EVE JSON to a mounted sensor log path.
- Configure Zeek to write protocol logs to a mounted sensor log path.
- Configure Logstash, Vector, or an agent-compatible collector to read Zeek and Suricata logs.
- Route logs through Logstash and Redis where appropriate in the standalone and manager-search profiles.
- Index normalized events into OpenSearch with stable index naming.
- Add OpenSearch index lifecycle or retention settings for hot local test data.
- Add test PCAP replay that proves alerts and protocol logs reach OpenSearch.

Progress:

- Logstash now reads Suricata EVE-style JSON from the `sentinelmesh-suricata` volume.
- Logstash now reads Zeek JSON from the `sentinelmesh-zeek` volume.
- `sm-seed-nsm-events` seeds validation records into those volumes and can verify indexing in OpenSearch.

Done when:

- `dev-lab` can replay a PCAP and produce searchable Suricata and Zeek events.
- Validation checks prove expected indexes exist and contain sample events.
- Grafana/Prometheus show ingest counters and pipeline health.

### Phase B - Finish Sensor Capture And PCAP Retrieval

Goal: Match the Security Onion principle that full packet capture stays on sensors but analysts can retrieve it.

Work:

- Replace Stenographer placeholder with working Stenographer or choose Suricata PCAP mode.
- Replace Arkime placeholder with working capture/viewer configuration.
- Define `/nsm`-style host directories for logs, packet capture, extracted files, and pcap output.
- Add retention controls based on disk percentage and reserved free space.
- Add a `pcap-api` service that can request stream/time-window PCAP from local sensor storage.
- Add SOC links from event details to PCAP retrieval.

Done when:

- Replayed traffic creates rolling packet capture.
- A flow/event can be used to retrieve matching PCAP.
- Storage limits can be configured and validated.

### Phase C - Build The Analyst SOC Core

Goal: Replace the static SOC scaffold with real operational workflows.

Work:

- Create SOC API service with auth, sessions, user settings, and role-aware access.
- Implement Alerts view backed by OpenSearch queries.
- Implement Hunt view with query builder, saved searches, and event detail pivots.
- Implement Cases with comments, observables, assignments, status, and attachments.
- Implement PCAP pivot from Alerts/Hunt.
- Embed or link Grafana/OpenSearch Dashboards for dashboards.
- Add CyberChef and ATT&CK Navigator links as external pivots.

Done when:

- An analyst can move from alert to hunt to PCAP to case without leaving the SentinelMesh workflow.
- Case records persist and can link back to source events.

### Phase D - Detection Engineering And Rule Lifecycle

Goal: Move from static rule directories to controlled detection operations.

Work:

- Define detection metadata schema for NIDS, Sigma, and YARA.
- Implement rule package import with source, version, signature, and checksum tracking.
- Implement Suricata rule sync, disable/enable, threshold, and suppress workflows.
- Add Sigma-to-alert-engine path, initially via ElastAlert 2 or an OpenSearch-compatible alternative.
- Add YARA scanner strategy for files extracted by Zeek/Suricata or a Strelka-like service.
- Add detection notes, tuning history, and test status.
- Add guided analysis/playbook model tied to detections.

Done when:

- Rule changes are reproducible, auditable, and testable.
- A tuned detection can generate alerts and show its playbook.

### Phase E - Distributed Grid And Enrollment

Goal: Make multi-node deployments behave like a managed grid rather than independent Compose stacks.

Work:

- Extend `sensor-enrollment` into a real manager API.
- Return manager, receiver, search, TLS, and collector output settings during enrollment.
- Add node identity, heartbeat, role, version, and service status records.
- Implement receiver outputs and load-balanced failover behavior.
- Implement search-node Redis pull configuration for manager/receiver queues.
- Add Grid UI for nodes, service health, ingest lag, packet loss, and disk usage.

Done when:

- A sensor can enroll, receive pipeline settings, ship events, and appear in Grid.
- A receiver can be added and used as an alternate ingest target.

### Phase F - Endpoint And Third-Party Log Visibility

Goal: Close the host visibility and syslog gap.

Work:

- Add syslog receiver service and parsing pipeline.
- Add Windows Event Log/Sysmon ingestion path.
- Decide endpoint strategy: Elastic Agent compatibility, FleetDM/osquery, Velociraptor, Wazuh, or hybrid.
- Add endpoint enrollment and policy model separate from network sensors if needed.
- Normalize host events into OpenSearch with ECS-like or SentinelMesh-native fields.

Done when:

- Windows endpoint logs and network-device syslog can be searched and correlated with network events.
- Asset context links host telemetry to observed network identity.

### Phase G - Production Hardening, Updates, And Offline Operation

Goal: Turn the lab stack into an appliance users can trust.

Work:

- Enable TLS and authentication for OpenSearch, Grafana, SOC, enrollment, and inter-node APIs.
- Replace dev passwords with first-boot secret generation and rotation.
- Add signed container image and rule bundle verification.
- Add backup/restore for config, cases, detections, Grafana, OpenSearch snapshots, and enrollment state.
- Add upgrade orchestration with preflight checks and rollback notes.
- Add airgap bundle creation for images, rules, dashboards, and vulnerability feeds.
- Add VM smoke tests for ISO boot and profile deployment.

Done when:

- A fresh ISO can install, configure a profile, pass `sm-doctor`, ingest sample data, and survive backup/restore.
- Updates can be applied with signatures and documented rollback.

## Recommended Next Sprint

The next sprint should focus on P0 ingest and packet evidence:

1. Make Suricata write EVE logs from live or replay traffic.
2. Make Zeek write logs from live or replay traffic.
3. Mount sensor logs consistently under a host data path.
4. Configure Vector/Logstash to ingest those logs into OpenSearch.
5. Add a PCAP replay validation test that asserts events reach OpenSearch.
6. Add Prometheus metrics for ingest count, parser errors, queue depth, and event lag.

This is the highest-leverage gap because SOC, asset context, risk scoring, dashboards, and relationship views all become more useful once real events flow through the system.

## Open Design Decisions

- Should SentinelMesh keep Vector as the collector, switch to Elastic Agent compatibility, or support both?
- Should Sigma alerting use ElastAlert 2 for parity, OpenSearch Alerting for native integration, or a SentinelMesh alert engine?
- Should full packet capture standardize on Stenographer first, Suricata PCAP first, or both?
- Should case management use OpenSearch only for MVP or add PostgreSQL for authoritative workflow state?
- Should endpoint visibility prioritize Elastic Agent compatibility, osquery/FleetDM, Velociraptor, Wazuh, or a staged hybrid?
