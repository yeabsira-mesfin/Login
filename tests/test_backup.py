import sys
from pathlib import Path
SRC_DIR = Path(__file__).resolve().parents[1] / 'src'
sys.path.insert(0, str(SRC_DIR))
from backup_verify import backup_and_verify

def test_backup_integrity(tmp_path):
    src = tmp_path / 'source.txt'
    src.write_text('important infrastructure record')
    result = backup_and_verify(src, tmp_path / 'backup')
    assert result['integrity_verified'] is True
    assert result['source_sha256'] == result['backup_sha256']
