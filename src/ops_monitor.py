from __future__ import annotations
import argparse, json, logging, socket, time
from dataclasses import dataclass, asdict
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

@dataclass
class CheckResult:
    name: str
    target: str
    status: str
    latency_ms: float | None
    detail: str


def check_http(name: str, url: str, timeout: float = 3.0) -> CheckResult:
    start = time.perf_counter()
    try:
        with urlopen(url, timeout=timeout) as response:
            latency = (time.perf_counter() - start) * 1000
            status = 'healthy' if 200 <= response.status < 400 else 'degraded'
            return CheckResult(name, url, status, round(latency, 2), f'HTTP {response.status}')
    except (URLError, HTTPError, TimeoutError) as exc:
        return CheckResult(name, url, 'critical', None, str(exc))


def check_tcp(name: str, host: str, port: int, timeout: float = 3.0) -> CheckResult:
    start = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            latency = (time.perf_counter() - start) * 1000
            return CheckResult(name, f'{host}:{port}', 'healthy', round(latency, 2), 'TCP connect succeeded')
    except OSError as exc:
        return CheckResult(name, f'{host}:{port}', 'critical', None, str(exc))


def load_config(path: str) -> dict:
    return json.loads(Path(path).read_text())


def run_checks(config: dict) -> list[CheckResult]:
    results = []
    for service in config.get('services', []):
        if service['type'] == 'http':
            results.append(check_http(service['name'], service['url']))
        elif service['type'] == 'tcp':
            results.append(check_tcp(service['name'], service['host'], int(service['port'])))
    return results


def write_incidents(results: list[CheckResult], path: str) -> int:
    critical = [r for r in results if r.status == 'critical']
    if not critical:
        return 0
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('a') as f:
        for r in critical:
            event = {
                'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                'severity': 'HIGH',
                'service': r.name,
                'target': r.target,
                'detail': r.detail,
                'action': 'Escalate to infrastructure on-call and attach check evidence.'
            }
            f.write(json.dumps(event) + '\n')
    return len(critical)


def main() -> int:
    parser = argparse.ArgumentParser(description='Infrastructure health and incident check runner')
    parser.add_argument('--config', default='config/services.json')
    parser.add_argument('--incident-log', default='artifacts/incidents.jsonl')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')
    results = run_checks(load_config(args.config))
    for result in results:
        logging.info(json.dumps(asdict(result)))
    incident_count = write_incidents(results, args.incident_log)
    logging.info('critical_incidents=%s', incident_count)
    return 2 if incident_count else 0

if __name__ == '__main__':
    raise SystemExit(main())
