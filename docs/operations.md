# Operations

This document covers operator workflows that are not tied to the initial installer.

## Health Check

```bash
sudo sm-doctor
```

`sm-doctor` performs baseline host checks and profile-aware container checks.

## Backups

```bash
sudo sm-backup
```

The MVP backup includes:

- `/etc/sentinelmesh`
- `/opt/sentinelmesh/profiles`
- `/opt/sentinelmesh/compose`
- `/opt/sentinelmesh/configs`

The MVP backup excludes:

- Packet captures
- OpenSearch data
- Docker volumes

## Restore

```bash
sudo sm-restore --archive /data/sentinelmesh/backups/sentinelmesh-backup-TIMESTAMP.tar.gz --yes
```

Restore can overwrite existing configuration. Run `sm-doctor` after restore.

## Rule Updates

```bash
sudo sm-update-rules
```

The MVP rule update workflow creates a local manifest. Future versions will fetch, verify, test, and deploy rule content.

## Ingest Validation

To seed Suricata and Zeek-shaped events into a running local stack:

```bash
sudo sm-seed-nsm-events --opensearch-url http://localhost:9200
```

This writes validation records into the sensor log volumes and verifies that Logstash indexes them into `sentinelmesh-events-*`.

To process an actual PCAP through the containerized engines and feed the same ingest path:

```bash
sudo sm-process-pcap --pcap /data/range/example.pcap
```

This runs Suricata and Zeek in offline mode, appends their JSON output to the sensor log volumes, and lets Logstash index the records.
