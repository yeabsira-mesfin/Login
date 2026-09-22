# Infrastructure Incident Runbook

## Trigger
A service check reports `critical`, repeated health checks fail, backup integrity verification fails, or an unexpected security-relevant condition is observed.

## First response
1. Record time, affected service, symptoms, and check output.
2. Confirm whether impact is isolated or widespread.
3. Preserve relevant logs and command output.
4. Escalate according to the defined ownership path rather than bypassing policy.
5. Apply only documented recovery actions for which the operator is authorized.

## Recovery verification
- Re-run the original health check.
- Confirm dependent services are functioning.
- Verify no new critical events are being generated.
- Document the recovery action and exact evidence.

## Post-incident
Record root cause when known, contributing factors, corrective action, follow-up owner, and a preventive control or monitoring improvement.
