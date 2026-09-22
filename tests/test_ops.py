import sys
from pathlib import Path
SRC_DIR = Path(__file__).resolve().parents[1] / 'src'
sys.path.insert(0, str(SRC_DIR))
from ops_monitor import check_tcp

def test_closed_tcp_port_returns_critical():
    result = check_tcp('closed', '127.0.0.1', 9, timeout=0.2)
    assert result.status == 'critical'
