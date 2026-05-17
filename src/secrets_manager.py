#!/usr/bin/env python3
"""
ZEUS OPS Secrets Manager
Secure credential loader for all Sierra portfolio data fetchers.

Reads from sierra-secrets.json (workspace root) or environment variables.
Never hardcode keys in source code.

Usage:
    from secrets_manager import get_secret
    
    census_key = get_secret("census_api_key")
    usaspending_key = get_secret("usaspending_api_key")  # None if not set
"""

import json
import os
from pathlib import Path

SECRETS_PATH = Path(__file__).parent.parent.parent / "sierra-secrets.json"


def load_secrets() -> dict:
    """Load secrets from sierra-secrets.json."""
    if not SECRETS_PATH.exists():
        return {}
    try:
        with open(SECRETS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def get_secret(key: str, default=None):
    """
    Get a secret by key.
    Priority: 1) Environment variable, 2) sierra-secrets.json, 3) default
    """
    # 1. Environment variable (highest priority)
    env_val = os.environ.get(key.upper())
    if env_val:
        return env_val
    
    # 2. secrets.json
    secrets = load_secrets()
    if key in secrets and secrets[key] and not secrets[key].startswith("PASTE_"):
        return secrets[key]
    
    # 3. Default fallback
    return default


def require_secret(key: str) -> str:
    """
    Get a secret or raise an error with setup instructions.
    Use for keys that MUST be present for the fetcher to work.
    """
    val = get_secret(key)
    if not val:
        raise RuntimeError(
            f"Missing required secret: '{key}'\n"
            f"Add it to: {SECRETS_PATH}\n"
            f"Or set environment variable: {key.upper()}=your_key_here"
        )
    return val


def list_secrets() -> list[str]:
    """List all available secret keys (values hidden)."""
    secrets = load_secrets()
    return list(secrets.keys())


if __name__ == "__main__":
    print("=== ZEUS OPS Secrets Manager ===")
    print(f"Secrets file: {SECRETS_PATH}")
    keys = list_secrets()
    print(f"\nAvailable keys ({len(keys)}):")
    for k in keys:
        val = get_secret(k)
        status = "✅ Set" if val else "❌ Missing / Placeholder"
        print(f"  {k}: {status}")
