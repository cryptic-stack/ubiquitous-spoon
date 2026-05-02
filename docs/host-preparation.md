# Host Preparation

Host preparation is handled by Ansible after Ubuntu Server is installed.

## Role Order

`ansible/site.yml` applies roles in this order:

1. `base`
2. `hardening`
3. `docker`
4. `sentinelmesh-files`
5. `firstboot`

## Base Role

Installs baseline packages and creates these directories:

- `/opt/sentinelmesh`
- `/opt/sentinelmesh/bin`
- `/etc/sentinelmesh`
- `/etc/sentinelmesh/secrets`
- `/var/log/sentinelmesh`
- `/data/sentinelmesh`
- `/data/pcap`

## Hardening Role

Initial hardening is intentionally conservative:

- Enables nftables.
- Disables SSH password authentication.
- Disables SSH root login.

This role will grow as the appliance model matures.

## Docker Role

Installs Docker Engine and the Docker Compose plugin from the Docker Ubuntu apt repository.

Docker Desktop remains a development-only tool on Windows. The appliance runtime uses Linux-native Docker Engine.

## SentinelMesh Files Role

Copies repo assets into `/opt/sentinelmesh` and links the main commands into `/usr/local/bin`.

## Firstboot Role

Installs `sentinelmesh-firstboot.service`.

The service and `/etc/profile.d/sentinelmesh-firstboot.sh` print setup reminders until `/etc/sentinelmesh/profile` exists.

## Local Syntax Check

Run:

```bash
./tests/test-ansible.sh
```

If Ansible is not installed, the test skips cleanly. CI installs Ansible and runs the full syntax check.
