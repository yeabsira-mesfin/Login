# Infrastructure Operations Toolkit

A Python operations toolkit focused on the daily work behind reliable hosting: service health checks, evidence-rich incident escalation, backup creation, and backup integrity verification.

The project treats operations as more than "is the server up?". A useful operator workflow should capture evidence, distinguish healthy and unhealthy states, follow a documented response path, and verify that recovery mechanisms actually work.

## Portfolio demo

`mock-app/` contains an interactive Windows-style **Infrastructure Operations Desk**. It presents service health, simulated incidents, backup verification, and runbook-driven recovery in a format that can be shown directly in a portfolio.

```bash
python -m http.server 8000 --directory mock-app
# open http://localhost:8000
```

The dashboard is a presentation simulation. The Python utilities in `src/` perform the actual checks and integrity verification implemented by the project.

## Components

### Service monitor

`src/ops_monitor.py` performs HTTP and TCP checks, records latency, assigns health status, and writes structured JSON Lines evidence when a critical condition is detected.

### Backup verifier

`src/backup_verify.py` creates a backup copy and compares SHA-256 hashes between the source and destination. A copy is not reported as verified until the hashes match.

### Incident runbook

`docs/incident-runbook.md` defines a lightweight operational response: capture evidence, scope impact, escalate appropriately, recover through documented actions, and verify restoration.

## Run the demo workflow

```bash
chmod +x scripts/demo.sh
./scripts/demo.sh
```

Edit `config/services.json` to point the monitor at services in your own local lab.

## Test

```bash
python -m pip install pytest
pytest -q
```

## CIA connection

- **Confidentiality:** use controlled procedures and escalation instead of unauthorized intervention.
- **Integrity:** backup copies are verified with SHA-256 hashes.
- **Availability:** HTTP and TCP checks identify unreachable services and preserve evidence for escalation and recovery.

## Repository layout

```text
src/                   Monitoring and backup verification tools
config/                Service-check configuration
docs/                  Incident response runbook
scripts/               Demonstration workflow
mock-app/               Interactive portfolio presentation
tests/                  Automated tests
.github/workflows/      CI pipeline
```

## Skills demonstrated

`Python` `Linux Operations` `Monitoring` `Incident Escalation` `Structured Logging` `HTTP/TCP Troubleshooting` `SHA-256` `Backup Verification` `Runbooks` `Testing` `CI/CD`

## Why I built it

Reliable hosting depends on operational discipline after infrastructure is provisioned. This project demonstrates how I approach detection, evidence collection, escalation, and integrity checks in a small environment that can be tested and explained end to end.
