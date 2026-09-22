#!/usr/bin/env bash
set -u
mkdir -p artifacts
printf 'demo-data\n' > artifacts/sample.txt
python src/backup_verify.py artifacts/sample.txt
python src/ops_monitor.py --config config/services.json || true
printf '\nArtifacts created under ./artifacts\n'
