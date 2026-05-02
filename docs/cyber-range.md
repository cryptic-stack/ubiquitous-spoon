# Cyber Range Mode

Cyber range mode turns SentinelMesh into a training and validation node.

## Current Capabilities

- `cyber-range` Compose profile
- `sm-range-engine` service
- Scenario JSON format
- Scenario injection marker command
- PCAP replay command
- Asset-context seed support

## Scenario Files

Scenario files live under:

- `scenarios/range/`

The initial scenario is:

- `scenarios/range/vpn-ransomware.json`

Schema:

- `schemas/range-scenario.schema.json`

## Range Engine

The range engine currently discovers scenario files and emits periodic status.

Future behavior:

- Emit synthetic logs.
- Coordinate PCAP replay.
- Send scoring hooks to CTFd.
- Write scenario timeline markers into OpenSearch.

## Inject A Scenario Marker

On the appliance:

```bash
sudo sm-range-inject --scenario vpn-ransomware
```

This creates a marker under:

```text
/data/sentinelmesh/range/injections
```

## Replay PCAP

```bash
sudo sm-replay-pcap --pcap /data/range/attack.pcap --interface eth1
```

PCAP replay requires `tcpreplay`, installed by the base Ansible role.
