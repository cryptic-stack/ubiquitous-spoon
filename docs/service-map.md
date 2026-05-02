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

- `/data/sentinelmesh/suricata`

Logs:

- `/var/log/sentinelmesh/suricata`

Health checks:

- Container running
- EVE file being written
- Interface exists

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

- `/data/sentinelmesh/zeek`

Logs:

- `/var/log/sentinelmesh/zeek`

Health checks:

- Container running
- `conn.log` being written

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

- OpenSearch indexes
- Manager forwarding endpoint

Data path:

- `/data/sentinelmesh/vector`

Logs:

- `/var/log/sentinelmesh/vector`

Health checks:

- Container running
- Config validates
- Output endpoint reachable when configured

Design note:

Vector is currently a lightweight MVP collector. It may be replaced or supplemented by Elastic Agent-compatible collection to more closely mirror Security Onion.

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
