# Design Decisions

This file records decisions as the project evolves. Add a new entry for every meaningful design choice so future changes have context.

## Decision: Use One Universal ISO

Date: 2026-05-02

Status: Accepted

Context:

SentinelMesh must support standalone, manager, sensor, cyber range, and developer/lab deployments.

Decision:

Build one Ubuntu Server ISO and select the deployment type at first boot with `sm-setup`.

Reason:

One ISO reduces release complexity and makes field deployment simpler.

Tradeoffs:

The ISO contains files that some roles will not use.

Future Review:

Revisit if profile-specific payloads become too large for a practical ISO.

## Decision: Use Docker Compose Profiles For Install Types

Date: 2026-05-02

Status: Accepted

Context:

The same appliance needs to activate different service groups depending on role.

Decision:

Use one `compose/compose.yml` file with Compose profiles for `standalone`, `manager`, `sensor`, `cyber-range`, and `dev-lab`.

Reason:

Compose profiles match the universal ISO approach and make local testing with Docker Desktop straightforward.

Tradeoffs:

One Compose file can become large.

Future Review:

Split into documented override files if the single file becomes hard to maintain.

## Decision: Run SentinelMesh Services As Containers Inside Ubuntu Server

Date: 2026-05-02

Status: Accepted

Context:

We want to mirror Security Onion design principles as much as practical. Security Onion 2.4 uses Docker Engine and containerized services inside its installed image.

Decision:

SentinelMesh will install Ubuntu Server as the host OS, then run NSM services as Docker containers managed by SentinelMesh scripts and Compose profiles.

Reason:

This keeps the appliance modular, easier to update, and closer to the Security Onion operating model.

Tradeoffs:

Packet capture services need careful host networking, capabilities, interface handling, and storage mapping.

Future Review:

Revisit the orchestration layer if Compose becomes too limiting. Security Onion uses deeper configuration management; SentinelMesh may eventually need a controller beyond Compose.

## Decision: Add Manager, Search, And Receiver Profiles

Date: 2026-05-02

Status: Accepted

Context:

Security Onion's distributed architecture distinguishes manager, search, manager-search, sensor, and receiver responsibilities.

Decision:

SentinelMesh will keep the simple first-run choices but add advanced profiles for `manager`, `manager-search`, `search`, and `receiver`.

Reason:

This keeps the MVP approachable while preserving a path toward Security Onion-like distributed deployments.

Tradeoffs:

There are more profiles to test and document.

Future Review:

Revisit the wizard UX after the first bootable ISO test.

## Decision: Add Asset Context As A First-Class Service

Date: 2026-05-02

Status: Accepted

Context:

SentinelMesh should extend beyond detection into vulnerability awareness, asset context, and risk-based prioritization.

Decision:

Add an `asset-context` service responsible for asset inventory, vulnerability context, exposure state, and risk scoring.

Reason:

Alerts without asset context force analysts to manually reconstruct importance, exposure, and vulnerability state. A central asset context engine makes enrichment reusable across alerts, search, reporting, and cyber-range workflows.

Tradeoffs:

This adds a new stateful domain model and requires careful handling of identity resolution across IPs, MACs, hostnames, and time.

Future Review:

Decide whether OpenSearch alone is enough for MVP asset storage or whether PostgreSQL should become the authoritative asset database.

## Decision: Build On Windows, Validate In WSL And VMs

Date: 2026-05-02

Status: Accepted

Context:

The primary workstation is Windows, but the target appliance is Ubuntu Server.

Decision:

Use Windows 11, VS Code, Codex, Docker Desktop, Ubuntu WSL, PowerShell 7, Packer, and Hyper-V/QEMU for the build workflow.

Reason:

This supports the actual workstation while preserving Linux-native behavior for scripts and ISO work.

Tradeoffs:

File path and filesystem performance differ between Windows-mounted paths and WSL-native paths.

Future Review:

Prefer WSL-native clones for heavy ISO builds if Windows-mounted performance becomes an issue.
