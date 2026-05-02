# Developer Notes

Use this file as the working notebook for implementation details, rough edges, test findings, and follow-up tasks.

## 2026-05-02

- Project scaffold created in `cryptic-stack/ubiquitous-spoon`.
- Initial build direction captured from the `Context` file.
- Windows build workflow is treated as a first-class requirement.
- Target appliance OS confirmed as Ubuntu Server 24.04 LTS.
- Local repository initialized from `https://github.com/cryptic-stack/ubiquitous-spoon.git`.
- Docker Compose profile rendering passed for `standalone`, `manager`, `sensor`, `cyber-range`, and `dev-lab` from Windows Docker.
- Bash syntax checks could not run because this workstation is not currently exposing a usable `/bin/bash` through WSL.
- Autoinstall YAML parse check could not run because Python YAML support is not installed in the current Windows Python environment.
- PowerShell helper check could not run through `pwsh` because PowerShell 7 is not installed or not on PATH in this shell.
- Running the PowerShell helper directly was blocked by the current PowerShell execution policy.
- Added GitHub Actions validation workflow for Bash syntax, autoinstall YAML, Compose profiles, and PowerShell parsing.
- Docker-based Linux validation passed for Bash syntax and autoinstall YAML because local WSL Bash is not currently available.
- Adjusted Ansible file installation so only `sm-*` appliance commands are copied into `/opt/sentinelmesh/bin`.
- Added firstboot login reminder because a oneshot systemd unit alone is easy for operators to miss.
- Added `tests/test-ansible.sh`; it skips locally if Ansible is unavailable but runs fully in CI.
- Docker-based Ansible syntax check passed after adding explicit local inventory handling.
- Added `tests/run-all.sh` for Linux/WSL validation and `scripts/windows/run-validation.ps1` for Windows-friendly validation.
- Updated Compose validation helpers so they skip cleanly when Docker is absent and validate all profiles by default on Windows.
- Confirmed from Security Onion 2.4 docs that their ISO includes Docker Engine and Docker images.
- Updated SentinelMesh to explicitly run services as containers inside Ubuntu Server and to use a named bridge network.
- Added advanced profiles for manager/search/receiver patterns to stay closer to Security Onion distributed architecture.
- Removed hard local Redis dependency from Logstash so `search` profiles can point at manager or receiver queues later.
- Added asset context engine as a first-class service near the manager/search tier.
- Asset context MVP is a placeholder process with schema and docs; enrichment implementation is still future work.
- Added validation for the new Python service placeholder and JSON schema files.
- Added OpenSearch and Dashboards to the cyber-range profile so asset context has local storage in training scenarios.
- Implemented deterministic asset IDs, seed asset loading, and capped risk scoring in `asset-context`.
- Added OpenSearch index template scaffolding for assets and enriched events.
- Added profile-aware container checks to `sm-doctor`.
- Added an idempotent index-template installer with OpenSearch readiness retries.
- Added `docs/phase-status.md` to keep implementation progress visible between build sessions.
- Fixed Ansible packaging for service code and schemas used by Compose mounts.
- Added sensor placeholders for Arkime and Stenographer while final images/configs are evaluated.
- Added PCAP replay script for cyber-range and sensor validation workflows.
- Replaced range-engine placeholder with a Python service that discovers scenario JSON files.
- Added initial range scenario format and injection marker workflow.
- Added first sensor enrollment scaffolding for distributed deployments.
- Replaced backup, restore, and rule update placeholders with safe MVP operator workflows.
- Implemented first ISO remaster workflow; still needs real Ubuntu ISO and VM boot testing.
- Wired ISO payload installation into Ubuntu autoinstall late commands.
- Added QEMU smoke-test workflow and Packer validation hook.
- Replaced network and storage placeholders with safe configuration writers that do not apply risky network changes automatically.
- Added vulnerability import staging as the next step toward continuous vulnerability awareness.
- Replaced the basic SOC portal placeholder with a static dashboard scaffold.
- Added Prometheus and Grafana as the default observability stack.
- Added seeded asset relationship metrics and Grafana relationship dashboard provisioning.

## Open Questions

- Which VM target should be the first-class ISO test path: Hyper-V, QEMU, or VMware Workstation?
- Should OpenSearch run with security enabled in the first MVP, or should dev-lab start with a simplified local-only mode?
- Which SOC portal framework should be used for the first placeholder implementation?
