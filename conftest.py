import socket
import threading
import time
import pytest
from app.server import app


def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


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
