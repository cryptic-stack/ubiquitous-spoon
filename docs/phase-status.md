# Phase Status

This document tracks build progress against the SentinelMesh implementation phases.

## Phase 0 - Windows Development Environment

Status: In Progress

Done:

- Windows build environment documentation exists.
- PowerShell prerequisite checker exists.
- Docker-backed Linux validation exists for Windows.

Remaining:

- Install or verify PowerShell 7.
- Install or verify HashiCorp Packer.
- Install or verify Ubuntu WSL distro.
- Choose first-class VM test target: Hyper-V, QEMU, or VMware.

## Phase 1 - Repo Skeleton And Docs

Status: Mostly Complete

Done:

- Repository structure exists.
- Core documentation exists.
- Design decisions are recorded.
- Validation documentation exists.
- GitHub Actions validation workflow exists.
- Security Onion gap analysis and closure plan exists.

Remaining:

- Commit and push initial scaffold.
- Keep docs current as implementation continues.
- Convert the highest-priority Security Onion gaps into implementation issues.

## Phase 2 - Compose Profile Stack

Status: In Progress

Done:

- One main Compose file exists.
- Profiles exist for `standalone`, `manager`, `manager-search`, `search`, `sensor`, `receiver`, `cyber-range`, and `dev-lab`.
- Compose validation passes for all profiles.
- `smbridge` network and `sm-*` container names are defined.
- Initial services include Suricata, Zeek, Vector, Redis, Logstash, OpenSearch, Dashboards, SOC placeholder, range placeholder, and asset context.
- Arkime and Stenographer placeholder containers exist.
- SOC portal static scaffold exists.
- Prometheus, Grafana, and connection metrics services exist.
- Logstash has an MVP file ingest path from Suricata and Zeek log volumes into OpenSearch.

Remaining:

- Replace static SOC portal scaffold with real application/API.
- Replace Arkime and Stenographer placeholders with final images/configuration.
- Decide final collector model: Vector, Elastic Agent, or hybrid.
- Add live traffic and PCAP replay validation for the Logstash ingest path.
- Add service healthchecks to Compose.

## Phase 3 - Ubuntu Server Autoinstall

Status: Started

Done:

- Autoinstall `user-data` and `meta-data` exist.
- YAML validation passes.
- Autoinstall copies SentinelMesh payload from ISO to `/opt/sentinelmesh/source`.
- Autoinstall runs the Ansible host-prep playbook during late commands.

Remaining:

- Replace placeholder password hash.
- Add ISO remastering workflow.
- Test in VM.

## Phase 4 - Packer Templates

Status: Started

Done:

- Initial Packer template exists.
- Packer validation test exists and skips cleanly when Packer is not installed.

Remaining:

- Install Packer locally.
- Validate template with real Ubuntu ISO path.
- Decide QEMU, Hyper-V, or VMware builder strategy.

## Phase 5 - Universal ISO Build Script

Status: In Progress

Done:

- ISO build script exists.
- Script validates required arguments.
- Script checks required remastering tools.
- Script injects NoCloud autoinstall data.
- Script copies SentinelMesh repo payload into the ISO.
- Script patches GRUB boot config.
- Script rebuilds ISO with `xorriso`.

Remaining:

- Add checksum documentation.
- Add artifact naming convention.
- Boot-test generated ISO in VM.
- QEMU ISO smoke-test script exists.

## Phase 6 - First Boot Wizard

Status: In Progress

Done:

- `sm-setup` exists.
- Profile selection works at script level.
- Config file output exists.
- Secrets generation exists.
- Profile deployment exists.
- Index-template installation is wired for profiles with OpenSearch.
- `sm-doctor` performs baseline and profile-aware checks.
- `sm-configure-network` records network intent and writes a netplan preview.
- `sm-configure-storage` creates directories and records storage intent.

Remaining:

- Improve network interface detection and validation.
- Add optional netplan apply workflow.
- Improve admin/TLS setup.

## Phase 7 - Asset Context And Risk

Status: Started

Done:

- `asset-context` service exists.
- Asset schema exists.
- Sample seed assets exist.
- MVP deterministic asset IDs exist.
- MVP explainable risk scoring exists.
- OpenSearch index templates exist for assets and enriched events.
- Tests validate risk scoring and schema parsing.
- Vulnerability import schema and staging command exist.
- Event indexes can receive MVP Suricata and Zeek-shaped records through Logstash.

Remaining:

- Write assets to OpenSearch.
- Consume live Zeek and Suricata events.
- Merge staged vulnerability scanner output into asset context records.
- Enrich events before indexing or at query time.
- Add UI/API surface for asset context.

## Phase 8 - Sensor Functionality

Status: Started

Done:

- Arkime and Stenographer placeholder containers exist.
- PCAP replay script exists.
- Offline PCAP processing script exists for Suricata and Zeek.

Remaining:

- Make always-on Suricata produce EVE logs from monitored interfaces.
- Make always-on Zeek produce logs from monitored interfaces.
- Replace Arkime placeholder with working capture/viewer configuration.
- Replace Stenographer placeholder with working packet spool configuration.
- Forward sensor logs to manager.

## Phase 9 - Manager Functionality

Status: Started

Done:

- OpenSearch and Dashboards services exist.
- Redis and Logstash services exist.
- Index template scaffolding exists.
- Sensor enrollment service placeholder exists.
- Manager-side enrollment token script exists.
- Sensor-side enrollment config script exists.
- Prometheus and Grafana observability stack exists.
- Relationship metrics and dashboard provisioning exist.
- `sm-seed-nsm-events` can seed Suricata and Zeek-shaped validation events into the ingest path.
- `sm-process-pcap` can process PCAPs through Suricata and Zeek into the Logstash ingest path.

Remaining:

- Extend real ingest pipelines from seeded validation to live sensor output.
- Add dashboard saved objects.
- Validate enrollment tokens through the manager service.
- Add rule management placeholder.

## Phase 10 - Cyber Range Mode

Status: Started

Done:

- Cyber-range profile exists.
- Range engine Python scenario discovery service exists.
- Asset-context seed data supports future scenario context.
- `sm-replay-pcap` exists for PCAP replay once `tcpreplay` is installed.
- Scenario schema exists.
- Initial `vpn-ransomware` scenario exists.
- `sm-range-inject` creates scenario injection markers.

Remaining:

- Add synthetic event generation from scenario timelines.
- Add scenario injection format.
- Add CTFd webhook placeholders.

## Phase 11 - Health, Backup, Upgrade

Status: Started

Done:

- `sm-doctor` exists.
- `sm-backup` creates configuration backup archives.
- `sm-restore` restores backup archives with explicit confirmation.
- `sm-update-rules` creates local rule update manifests.

Remaining:

- Add packet capture backup/export strategy.
- Add OpenSearch snapshot strategy.
- Add signed remote rule feed updates.
- Add upgrade notes.
