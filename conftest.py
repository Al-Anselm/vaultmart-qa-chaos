import os
import sys
import socket
import threading
import time
import pytest
from app.server import app


def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """
    On Windows machines with Smart App Control (SAC) enabled, the unsigned
    open-source Chromium binary downloaded by Playwright can be blocked.
    Using the pre-installed, Microsoft-signed 'msedge' channel bypasses SAC!
    """
    if sys.platform == "win32":
        edge_paths = [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        ]
        if any(os.path.exists(p) for p in edge_paths):
            return {
                **browser_type_launch_args,
                "channel": "msedge",
            }
    return browser_type_launch_args


@pytest.fixture(scope="session", autouse=True)
def ensure_vaultmart_server():
    """
    Automatically ensures http://localhost:8000 is running before Playwright tests start.
    If the student already started it via 'docker compose up -d' or 'python app/server.py',
    this fixture detects port 8000 is active and uses it directly.
    Otherwise, it launches the Flask app in a background daemon thread automatically!
    """
    if not is_port_in_use(8000):
        print("\n[INFO] Port 8000 not active — auto-starting VaultMart server in background thread...")
        server_thread = threading.Thread(
            target=lambda: app.run(host="127.0.0.1", port=8000, debug=False, use_reloader=False),
            daemon=True,
        )
        server_thread.start()
        for _ in range(20):
            if is_port_in_use(8000):
                break
            time.sleep(0.2)
    yield
