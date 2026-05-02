# Service Map

Update this file whenever a service is added, removed, or changed.

## Suricata

Profiles:

- standalone
- sensor
- cyber-range

Purpose:

Network IDS and protocol alerting.

Inputs:

- Monitoring interface
- Rule files

Outputs:

- EVE JSON
- Alerts
- Protocol metadata

Data path:

- Docker volume `sentinelmesh-suricata`
- Future host path `/data/sentinelmesh/suricata`

Logs:

- `/var/log/sentinelmesh/suricata`

Health checks:

- Container running
- EVE file being written
- Interface exists
- Offline PCAP processing through `sm-process-pcap` produces EVE records

## Zeek

Profiles:

- standalone
- sensor
- cyber-range

Purpose:

Network protocol metadata and connection logging.

Inputs:

- Monitoring interface

Outputs:

- Zeek logs
- Connection metadata
- DNS, HTTP, TLS, and file metadata

Data path:

- Docker volume `sentinelmesh-zeek`
- Future host path `/data/sentinelmesh/zeek`

Logs:

- `/var/log/sentinelmesh/zeek`

Health checks:

- Container running
- `conn.log` being written
- Offline PCAP processing through `sm-process-pcap` produces JSON log records

## Arkime

Profiles:

- standalone
- sensor
- cyber-range

Purpose:

Indexed packet/session search and packet investigation.

Inputs:

- Monitoring interface
- Packet/session metadata

Outputs:

- Arkime session metadata
- Packet investigation UI in a future phase

Data path:

- Docker volume `sentinelmesh-arkime`
- Future host path `/data/arkime`

Logs:

- Docker logs for `sm-arkime`

Health checks:

- Container running
- Capture process active after final image/config is selected

Current state:

- Placeholder container until final Arkime image and configuration are selected.

## Stenographer

Profiles:

- standalone
- sensor
- cyber-range

Purpose:

Rolling full packet capture buffer local to sensor nodes.

Inputs:

- Monitoring interface

Outputs:

- Local PCAP ring buffer

Data path:

- Docker volume `sentinelmesh-pcap`
- Future host path `/data/pcap`

Logs:

- Docker logs for `sm-stenographer`

Health checks:

- Container running
- Packet spool is being written after final image/config is selected

Current state:

- Placeholder container until final Stenographer image and configuration are selected.

## Vector

Profiles:

- standalone
- manager
- sensor
- cyber-range
- dev-lab

Purpose:

Collect and forward logs between local services and search backends.

Inputs:

- Suricata logs
- Zeek logs
- Application logs

Outputs:

- Future OpenSearch indexes
- Future manager forwarding endpoint

Data path:

- `/data/sentinelmesh/vector`

Logs:

- `/var/log/sentinelmesh/vector`

Health checks:

- Container running
- Config validates
- Output endpoint reachable when configured

Design note:

Vector is currently a lightweight MVP collector placeholder. The first working ingest path uses Logstash file inputs against the sensor log volumes so that seeded and replay-derived NSM events can reach OpenSearch quickly. Vector may be replaced or supplemented by Elastic Agent-compatible collection to more closely mirror Security Onion.

## Redis

Profiles:

- standalone
- manager
- receiver
- dev-lab

Purpose:

Queue events between ingest and indexing stages.

Inputs:

- Collector or Logstash-style ingest pipeline

Outputs:

- Logstash-style indexing pipeline

Data path:

- Docker volume `sentinelmesh-redis`

Logs:

- Docker logs for `sm-redis`

Health checks:

- Container running
- Redis ping succeeds

## Logstash

Profiles:

- standalone
- manager
- receiver
- search
- dev-lab

Purpose:

Ingest, parse, and forward events.

Inputs:

- Redis queue
- Suricata EVE JSON from `sentinelmesh-suricata`
- Zeek JSON logs from `sentinelmesh-zeek`
- Future Beats/Elastic Agent compatible endpoints

Outputs:

- OpenSearch
- stdout during early MVP validation

Data path:

- `/opt/sentinelmesh/configs/logstash`

Logs:

- Docker logs for `sm-logstash`

Health checks:

- Container running
- Pipeline config loads
- Output endpoint reachable when configured
- Seeded Suricata and Zeek events can be found in `sentinelmesh-events-*`

Current state:

- Reads `/logs/suricata/eve.json`.
- Reads `/logs/zeek/current/*.json`.
- Reads Redis list `sentinelmesh-events`.
- Writes `sentinelmesh-events-YYYY.MM.dd` indexes in OpenSearch.

## OpenSearch

Profiles:

- standalone
- manager
- dev-lab

Purpose:

Search and analytics datastore.

Inputs:

- Vector events
- SOC portal data

Outputs:

- Search API
- Dashboards data source

Data path:

- `/data/sentinelmesh/opensearch`

Logs:

- `/var/log/sentinelmesh/opensearch`

Health checks:

- Container running
- Cluster health endpoint reachable
- SentinelMesh index templates installed

## SOC Portal

Profiles:

- standalone
- manager
- manager-search
- cyber-range
- dev-lab

Purpose:

Operator dashboard and workflow entry point. The MVP mirrors the Security Onion analyst navigation pattern with Alerts, Dashboards, Hunt, Cases, Detections, PCAP, Grid, and Assets.

Inputs:

- Browser requests
- OpenSearch event queries
- Seed asset context

Outputs:

- SOC web UI
- Same-origin `/api/overview`, `/api/events`, `/api/groupby`, `/api/assets`, `/api/relationships`, `/graph/soc/assets`, and `/api/health` JSON
- Prometheus metrics at `/metrics` for dashboard rollups

Data path:

- Static UI: `/portal`
- API service: `services/soc-portal`

Logs:

- Docker logs for `sm-soc`

Health checks:

- Container running
- HTTP endpoint returns OK
- `/api/health` returns OK
- `/api/overview` can summarize event and asset context
- `/api/groupby` can summarize Hunt results by approved fields for dashboard-style pivots
- `/api/relationships` can summarize source-to-destination communication from indexed events
- Prometheus can scrape `/metrics`

## Asset Context

Profiles:

- standalone
- manager
- manager-search
- cyber-range
- dev-lab

Purpose:

Maintain continuously updated asset inventory, vulnerability context, exposure state, and risk scores.

Inputs:

- Zeek logs
- Suricata EVE logs
- Arkime session metadata
- Vulnerability scanner imports
- Network scan imports
- Threat intelligence
- GeoIP and ASN databases
- MAC vendor data

Outputs:

- Asset records
- Event enrichment fields
- Risk scores
- Vulnerability summaries
- Exposure context

Data path:

- OpenSearch index `sentinelmesh-assets`
- Future local cache or database

Logs:

- Docker logs for `sm-asset-context`

Health checks:

- Container running
- Can reach OpenSearch when applicable
- Asset schema is valid
- Enrichment backlog is draining
- Seed asset file loads when configured
- Risk scoring tests pass in CI
- Asset and event index templates exist

## Connection Metrics

Profiles:

- standalone
- manager
- manager-search
- cyber-range
- dev-lab

Purpose:

Expose SentinelMesh asset connection and risk metrics for Prometheus and relationship graph JSON for Grafana.

Inputs:

- Seed asset data
- Seed connection data
- Future Zeek, Suricata, Arkime, and OpenSearch-derived relationships

Outputs:

- Prometheus `/metrics`
- Relationship graph JSON at `/graph/assets`

Data path:

- `services/connection-metrics`

Logs:

- Docker logs for `sm-connection-metrics`

Health checks:

- Container running
- `/health` returns OK
- Prometheus can scrape `/metrics`

## Prometheus

Profiles:

- standalone
- manager
- manager-search
- cyber-range
- dev-lab

Purpose:

Store time-series metrics for SentinelMesh observability and relationship charts.

Inputs:

- `connection-metrics`
- Future SentinelMesh exporters

Outputs:

- Prometheus query API
- Grafana datasource

Data path:

- Docker volume `sentinelmesh-prometheus`

Logs:

- Docker logs for `sm-prometheus`

Health checks:

- Container running
- Target `connection-metrics` is healthy

## Grafana

Profiles:

- standalone
- manager
- manager-search
- cyber-range
- dev-lab

Purpose:

Visualize SentinelMesh metrics, asset relationships, risk scores, and operational dashboards.

Inputs:

- Prometheus datasource
- Connection metrics JSON datasource

Outputs:

- Grafana web UI
- Provisioned SentinelMesh relationship dashboard
- Embedded SOC portal dashboard frames for local operator workflows

Data path:

- Docker volume `sentinelmesh-grafana`

Logs:

- Docker logs for `sm-grafana`

Health checks:

- Container running
- Grafana HTTP endpoint returns OK
- Provisioned dashboard is available
- Embedded dashboards render in the SOC portal

## Firstboot Reminder

Profiles:

- all base installs before profile selection

Purpose:

Prompt the operator to run `sudo sm-setup` after installation.

Inputs:

- Presence or absence of `/etc/sentinelmesh/profile`

Outputs:

- Console and journal reminder

Data path:

- none

Logs:

- systemd journal

Health checks:

- `systemctl status sentinelmesh-firstboot.service`
- `/etc/sentinelmesh/profile` exists after setup
