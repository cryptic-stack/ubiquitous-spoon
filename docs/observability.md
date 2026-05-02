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
- `sentinelmesh_soc_relationship_observed_count`

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

The SOC overview dashboard is provisioned from:

- `configs/grafana/dashboards/sentinelmesh-soc-overview.json`

It mirrors the Security Onion Dashboards pattern as closely as Prometheus and Grafana allow:

- Basic metrics for indexed events, alerts, and highest asset risk
- Timeline for current indexed event and alert counts
- Group metrics for `event.module`, `event_type`, `source.ip`, `destination.ip`, and destination port
- Event table sourced from the SOC JSON API
- Relationship context table sourced from the SOC JSON API

Security Onion's Dashboards page is still more interactive for ad hoc OQL, recursive groupby, row expansion, and context menus. SentinelMesh keeps those analyst pivots in the SOC portal while Grafana provides durable wallboard-style visualizations and trend panels.

## Event-Derived Relationship Context

The SOC portal exposes relationship data derived from indexed events:

- `GET /api/relationships?q=<hunt query>&size=250`
- `GET /graph/soc/assets?q=<hunt query>&size=250`

The payload includes:

- `nodes`: source and destination assets or IPs with risk context when known
- `edges`: Grafana-friendly source-to-target relationship records
- `relationships`: table-oriented rows with source asset, destination asset, destination IP, port, protocol, event count, highest risk, and last seen

The SOC Prometheus scrape also emits `sentinelmesh_soc_relationship_observed_count` so Grafana can show top observed communication pairs from the same OpenSearch-backed event stream used by Hunt.

## Hunt Grouping

The SOC portal exposes dashboard-style grouped Hunt pivots:

- `GET /api/groupby?q=<hunt query>&field=source.ip&size=10`

Allowed fields are constrained to common operator pivots: `source.ip`, `destination.ip`, `destination.port`, `event.module`, `event.dataset`, `event_type`, and `protocol`. Each bucket includes a `pivot_query` value that the SOC UI can immediately run as a filtered Hunt. Operator-facing aliases such as `destination.port` are translated to the current backend field names when the query runs.

## Design Boundary

Prometheus is the time-series metrics store. It is not the authoritative relationship database.

OpenSearch remains the event/search datastore, while `asset-context` remains the asset memory and risk context service.
