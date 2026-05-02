# Install Types

SentinelMesh presents these install types during first boot.

## Standalone NSM

Runs sensor, packet capture, search, dashboards, and portal services on one host.

Use for:

- Small business monitoring
- Labs
- Demos
- Single-server deployments

## Manager / Search Node

Runs central search, dashboards, portal, ingestion queue, reporting, and sensor management services.

Use for:

- Distributed sensor deployments
- Multi-site environments
- Central SOC operations

This maps to the `manager-search` profile.

## Dedicated Manager Node

Runs central management, SOC portal, dashboards, enrollment, Redis, and Logstash-style ingestion services.

Use for:

- Distributed deployments with separate search nodes
- Larger lab or production designs

This maps to the `manager` profile.

## Dedicated Search Node

Runs search and indexing services.

Use for:

- Distributed deployments
- Scaling storage and query load separately from management

This maps to the `search` profile.

## Receiver Node

Runs ingestion and queue services to reduce manager load and provide pipeline redundancy.

Use for:

- Larger distributed deployments
- Environments that need ingestion fan-in before search nodes

This maps to the `receiver` profile.

## Sensor Node

Runs packet capture, protocol metadata, IDS, and forwarding services.

Use for:

- SPAN/TAP monitoring
- Remote branch networks
- Dedicated packet capture nodes

Full packet capture should remain local to the sensor, following the Security Onion model.

## Cyber Range Node

Runs monitoring plus training helpers.

Use for:

- Blue-team labs
- CTFs
- Attack replay
- Student scoring integrations

## Developer / Lab Node

Runs a lightweight local stack for development and test work.

Use for:

- Local Docker Desktop testing
- API development
- Demo data
- Fast iteration
