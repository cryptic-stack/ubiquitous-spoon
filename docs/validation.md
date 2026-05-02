# Validation

SentinelMesh validation is designed to work from both Windows and Linux.

## Windows-Friendly Validation

Run from the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ./scripts/windows/run-validation.ps1
```

This performs:

- PowerShell parse checks
- Docker Compose profile validation for all profiles
- Docker-backed Bash syntax checks
- Docker-backed Python syntax checks
- SOC portal API helper unit tests
- Docker-backed JSON parsing for schemas, OpenSearch templates, and examples
- Docker-backed YAML parsing for Prometheus and Grafana provisioning
- Docker-backed autoinstall YAML validation
- Optional live ingest proof with `sm-seed-nsm-events` against a running Compose stack

Use this when Ubuntu WSL is not ready yet but Docker Desktop is working.

## Linux Or WSL Validation

Run:

```bash
./tests/run-all.sh
```

This performs:

- Bash syntax checks
- Python syntax checks
- JSON parsing for schemas, OpenSearch templates, and examples
- YAML parsing for Prometheus and Grafana provisioning
- Autoinstall YAML validation
- Ansible syntax check when Ansible is installed
- Docker Compose profile validation

## Individual Checks

```bash
./tests/test-scripts.sh
./tests/test-autoinstall.sh
./tests/test-ansible.sh
./tests/test-compose.sh
```

## Live Ingest Check

With a profile containing `logstash` and `opensearch` running, seed validation events:

```bash
sudo sm-seed-nsm-events --opensearch-url http://localhost:9200
```

From the repository root on a Windows development host, the same script can be run through a Linux shell with Docker Desktop available. It writes one Suricata EVE-style event and one Zeek JSON event into the SentinelMesh Docker log volumes, then waits for those records to appear in `sentinelmesh-events-*`.

To validate with a PCAP instead of synthetic JSON:

```bash
sudo sm-process-pcap --pcap /data/range/example.pcap
```

Then query OpenSearch for Suricata and Zeek records in `sentinelmesh-events-*`.

## CI Validation

GitHub Actions runs:

- Bash syntax checks
- Autoinstall YAML validation
- Ansible syntax check
- Docker Compose profile validation
- PowerShell parser checks

The workflow lives at:

- `.github/workflows/validate.yml`

## Current Local Tooling Notes

This workstation can validate Docker Compose through Docker Desktop.

For full native validation, finish installing:

- PowerShell 7
- HashiCorp Packer
- Ubuntu WSL distro
- Python YAML support inside WSL
