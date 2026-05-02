# Sensor Enrollment

Sensor enrollment is the manager-side workflow for joining distributed sensors to a SentinelMesh deployment.

## Current Capabilities

- `sensor-enrollment` service placeholder
- Manager-side token creation
- Sensor-side enrollment config writer

## Create Token On Manager

```bash
sudo sm-create-enrollment-token --sensor-name branch-sensor-01 --ttl-hours 24
```

The token record is stored in:

```text
/etc/sentinelmesh/enrollment/tokens.jsonl
```

## Enroll Sensor

On the sensor:

```bash
sudo sm-enroll-sensor \
  --manager-url https://manager.example.local \
  --token TOKEN_FROM_MANAGER \
  --sensor-name branch-sensor-01
```

This writes:

```text
/etc/sentinelmesh/sensor-enrollment.yml
```

## Future Work

- Validate tokens through the manager service.
- Return manager, receiver, and search pipeline settings.
- Track sensor heartbeat and health.
- Rotate enrollment tokens.
- Add mTLS or signed enrollment payloads.
