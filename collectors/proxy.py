"""Shared proxy configuration for all collectors."""
import os
import re
import random
import string
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root regardless of where collector is invoked from
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Format: host:port:username:password
PROXY_CONFIG = os.getenv("PROXY_CONFIG", "")


def get_proxy() -> str | None:
    """Return a proxy URL with a fresh random session ID."""
    if not PROXY_CONFIG:
        return None
    session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    parts = PROXY_CONFIG.split(':')
    if len(parts) != 4:
        return None
    host, port, username, password = parts
    if "session-" in username:
        username = re.sub(r'session-[a-zA-Z0-9]+', f'session-{session_id}', username)
    return f"http://{username}:{password}@{host}:{port}"


def apply_proxy(proxy_str: str | None):
    """Set proxy environment variables for yfinance."""
    if proxy_str:
        for key in ('HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy'):
            os.environ[key] = proxy_str
    else:
        for key in ('HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy'):
            os.environ.pop(key, None)
