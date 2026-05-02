# Observability And Relationship Visualization

SentinelMesh uses Prometheus and Grafana for local observability, operational metrics, and asset relationship visualization.

## Services

- `connection-metrics`: SentinelMesh metrics and relationship graph endpoint
- `prometheus`: Metrics collection and query engine
- `grafana`: Dashboard and relationship visualization UI

## Local URLs

- Grafana: `http://localhost:3000`
- Prometheus: `http://localhost:9090`
- Connection metrics: `http://localhost:9105/metrics` when the port is exposed for local development

Inside the Compose network:

- `http://connection-metrics:9105/metrics`
- `http://connection-metrics:9105/graph/assets`

## Metrics

The first Prometheus metrics are:

- `sentinelmesh_connection_observed_total`
- `sentinelmesh_asset_risk_score`
- `sentinelmesh_asset_vulnerability_count`
- `sentinelmesh_relationship_weight`

The MVP metrics are seeded from sample asset and connection data. Future versions will consume Zeek, Suricata, Arkime, and OpenSearch data.

## Grafana Dashboard

The default dashboard is provisioned from:

- `configs/grafana/dashboards/sentinelmesh-relationships.json`

It includes:

- Observed connection count
- Top asset relationships
- Asset risk scores
- Vulnerability counts by asset
- Asset connection table
- Relationship edge feed from `/graph/assets`

## Design Boundary

Prometheus is the time-series metrics store. It is not the authoritative relationship database.

OpenSearch remains the event/search datastore, while `asset-context` remains the asset memory and risk context service.
