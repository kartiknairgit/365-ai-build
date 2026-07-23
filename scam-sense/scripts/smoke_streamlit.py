"""Start Streamlit as Community Cloud would and verify its health endpoint."""

from __future__ import annotations

import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
PORT = 8517
HEALTH_URL = f"http://127.0.0.1:{PORT}/_stcore/health"


def main() -> int:
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "scam-sense/app.py",
            "--server.headless=true",
            "--server.address=127.0.0.1",
            f"--server.port={PORT}",
            "--browser.gatherUsageStats=false",
        ],
        cwd=REPOSITORY_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        for _ in range(40):
            if process.poll() is not None:
                return process.returncode or 1
            try:
                with urllib.request.urlopen(HEALTH_URL, timeout=1) as response:
                    return 0 if response.read().decode().strip() == "ok" else 1
            except (urllib.error.URLError, TimeoutError):
                time.sleep(0.25)
        return 1
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


if __name__ == "__main__":
    raise SystemExit(main())
