from __future__ import annotations
import argparse, hashlib, json, shutil, time
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def backup_and_verify(source: Path, backup_dir: Path) -> dict:
    backup_dir.mkdir(parents=True, exist_ok=True)
    destination = backup_dir / source.name
    shutil.copy2(source, destination)
    source_hash = sha256(source)
    backup_hash = sha256(destination)
    return {
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'source': str(source),
        'backup': str(destination),
        'source_sha256': source_hash,
        'backup_sha256': backup_hash,
        'integrity_verified': source_hash == backup_hash,
    }


def main() -> int:
    p = argparse.ArgumentParser(description='Create a file backup and verify integrity with SHA-256')
    p.add_argument('source')
    p.add_argument('--backup-dir', default='artifacts/backups')
    args = p.parse_args()
    result = backup_and_verify(Path(args.source), Path(args.backup_dir))
    print(json.dumps(result, indent=2))
    return 0 if result['integrity_verified'] else 3

if __name__ == '__main__':
    raise SystemExit(main())
