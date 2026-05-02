# Architecture

SentinelMesh NSM is designed as a universal Ubuntu Server appliance image for network security monitoring, threat intelligence, case work, reporting, and cyber range operation.

## Target Operating System

The target OS is Ubuntu Server 24.04 LTS.

Ubuntu Desktop is intentionally excluded from the target image to keep the appliance smaller, simpler, easier to harden, and better aligned with server deployment patterns.

## Build And Runtime Split

The development workstation is Windows-based:

- VS Code is the primary editor.
- Codex is used for implementation and refactoring.
- Docker Desktop with the WSL 2 backend is used for local Compose testing.
- Ubuntu WSL runs Linux-native build and validation scripts.
- Packer is used for repeatable image automation and VM validation where practical.

The runtime appliance is Linux-based:

- Ubuntu Server 24.04 LTS
- Docker Engine
- Docker Compose plugin
- SentinelMesh-managed Docker containers
- Common container bridge network named `smbridge`
- systemd services
- SentinelMesh scripts under `/opt/sentinelmesh/bin`
- Persistent configuration under `/etc/sentinelmesh`
- Logs under `/var/log/sentinelmesh`

## Universal ISO Flow

```text
SentinelMesh-NSM.iso
  |
  v
Ubuntu Server autoinstall
  |
  v
Base host preparation
  |
  v
First boot prompt
  |
  v
sudo sm-setup
  |
  v
Selected Docker Compose profile
```

The ISO must not fork into separate role-specific images. Role selection is deferred to first boot so the same artifact can be reused in labs, production sensors, manager nodes, and cyber ranges.

## Install Profiles

Standalone NSM:

- Suricata
- Zeek
- Arkime
- Stenographer
- Vector
- Logstash
- Redis
- OpenSearch
- OpenSearch Dashboards
- SOC portal
- Asset context engine

Manager / Search Node:

- OpenSearch
- OpenSearch Dashboards
- SOC portal
- Logstash
- Redis
- Threat intelligence
- Rule management
- Sensor enrollment placeholder
- Asset context engine

Dedicated Manager Node:

- SOC portal
- Dashboards
- Logstash
- Redis
- Sensor enrollment placeholder
- Search cluster coordination

Dedicated Search Node:

- OpenSearch
- Logstash

Receiver Node:

- Logstash
- Redis
- Pipeline redundancy placeholder

Sensor Node:

- Suricata
- Zeek
- Arkime capture
- Stenographer
- Vector
- Local spool queue
- Health reporter

Cyber Range Node:

- Suricata
- Zeek
- Arkime
- Vector
- OpenSearch
- OpenSearch Dashboards
- Asset context engine
- PCAP replay
- Synthetic event generation
- CTFd integration placeholders

Developer / Lab Node:

- Lightweight OpenSearch
- Dashboards
- SOC portal placeholder
- Range engine placeholder
- Sample data hooks
- Asset context engine

## Persistent Paths

- `/etc/sentinelmesh/sentinelmesh.yml`: main appliance configuration
- `/etc/sentinelmesh/profile`: selected install profile
- `/etc/sentinelmesh/secrets/`: generated secrets
- `/opt/sentinelmesh/`: installed application files
- `/data/sentinelmesh/`: application data
- `/data/pcap/`: packet capture data
- `/var/log/sentinelmesh/`: script and service logs

## Security Onion-Inspired Principles

SentinelMesh intentionally uses Docker containers inside the Ubuntu Server appliance. This mirrors Security Onion's current pattern of shipping Docker Engine and running services as containers.

See:

- `docs/security-onion-alignment.md`
