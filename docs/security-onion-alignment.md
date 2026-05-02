# Security Onion Alignment

SentinelMesh should mirror Security Onion design principles where practical while leaving room for our own portal, cyber range mode, and future detection engineering workflow.

## Confirmed Security Onion Principles

Security Onion 2.4 uses Docker inside the installed image. Their documentation states that the ISO includes Docker Engine and Docker images, and that containers use a common Docker bridge network with aliases for service-to-service communication.

Security Onion also uses role-based node architecture:

- Standalone
- Manager
- Search
- Manager Search
- Sensor
- Receiver
- Heavy node patterns for special cases

For sensors, Security Onion forwards Suricata and Zeek logs through Elastic Agent toward Logstash on the manager. Full packet capture remains on the sensor.

## SentinelMesh Decisions

SentinelMesh will use Docker containers inside Ubuntu Server.

The target appliance model is:

- Ubuntu Server 24.04 LTS host
- Docker Engine on the host
- SentinelMesh-managed containers
- Common Docker bridge network named `smbridge`
- Predictable container names using `sm-*`
- Role selection through `sm-setup`

## Where We Match Security Onion

We will mirror these patterns:

- One installed server image with role selection.
- Docker Engine included in the target appliance.
- Containerized services rather than host-installed application sprawl.
- Named bridge network for container-to-container traffic.
- Sensor nodes run Suricata, Zeek, and packet capture services.
- Manager and receiver nodes handle ingestion services.
- Search nodes handle datastore services.
- Full packet capture stays local to the sensor.
- Central docs and health checks are treated as product features.

## Where We Intentionally Differ

Security Onion uses Elastic Stack components. SentinelMesh currently uses OpenSearch for the first open-source-friendly MVP.

This is an intentional early decision, but the pipeline should still follow the same shape:

```text
Sensor logs
  |
  v
Agent or collector
  |
  v
Logstash or compatible ingest processor
  |
  v
Redis queue where applicable
  |
  v
Search datastore
```

Current SentinelMesh MVP placeholders:

- `vector` is present as a lightweight collector while we decide whether to use Elastic Agent, OpenSearch Data Prepper, or another compatible collector.
- `logstash` and `redis` are now included to keep the pipeline shape close to Security Onion.
- `opensearch` is currently the search datastore.

## Profiles

SentinelMesh profiles:

- `standalone`
- `manager`
- `manager-search`
- `search`
- `sensor`
- `receiver`
- `cyber-range`
- `dev-lab`

The original user-facing five choices remain, but advanced choices are available:

- Manager / Search Node maps to `manager-search`.
- Dedicated Manager Node maps to `manager`.
- Dedicated Search Node maps to `search`.
- Receiver Node maps to `receiver`.

## Future Work

Evaluate:

- Whether to replace or supplement Vector with Elastic Agent-compatible collection.
- Whether to include a local container registry on manager nodes.
- Whether to sign and verify SentinelMesh container images before update.
- Whether to preload all required images into the ISO or provide airgap bundles.
- Whether OpenSearch remains the default datastore or Elasticsearch compatibility becomes a supported option.

Detailed parity gaps and closure phases are tracked in `docs/security-onion-gap-analysis.md`.
