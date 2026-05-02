# First Boot Wizard

The first boot wizard is `sm-setup`.

## Purpose

`sm-setup` turns the universal installed base into a selected SentinelMesh role.

## Required Questions

1. Select install type.
2. Set hostname.
3. Select management interface.
4. Select monitoring interface.
5. Configure DHCP or static IP.
6. Configure storage paths.
7. Configure admin account.
8. Configure TLS mode.
9. Configure update and rule feeds.
10. Deploy selected profile.
11. Run health checks.

## Required Outputs

- `/etc/sentinelmesh/profile`
- `/etc/sentinelmesh/sentinelmesh.yml`
- Generated secrets in `/etc/sentinelmesh/secrets/`
- Deployment logs in `/var/log/sentinelmesh/`

## Profile Choices

The wizard must support:

1. Standalone NSM
2. Manager / Search Node
3. Sensor Node
4. Cyber Range Node
5. Developer / Lab Node
6. Dedicated Manager Node
7. Dedicated Search Node
8. Receiver Node

## Script Design

`sm-setup` should orchestrate smaller scripts:

- `sm-detect-hardware`
- `sm-configure-network`
- `sm-configure-storage`
- `sm-generate-secrets`
- `sm-deploy-profile`
- `sm-doctor`

Current network behavior:

- Records network intent in `/etc/sentinelmesh/network.yml`.
- Writes a netplan preview to `/etc/sentinelmesh/netplan-preview.yaml`.
- Does not apply netplan automatically yet.

Current storage behavior:

- Creates selected storage directories.
- Records storage intent in `/etc/sentinelmesh/storage.yml`.
