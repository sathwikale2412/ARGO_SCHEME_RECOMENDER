"""Supabase PostgREST access for the ARGO API.

The original project read from a committed SQLite file, which cannot survive a
serverless deployment (the filesystem is ephemeral and the file ships read-only).
The tables mirror backend/models.py one-for-one so the query logic stays familiar.
"""

import os

import requests

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY", "")


class NotConfigured(RuntimeError):
    pass


def is_configured():
    return bool(SUPABASE_URL and SUPABASE_ANON_KEY)


def _headers():
    return {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _require_config():
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise NotConfigured(
            "SUPABASE_URL / SUPABASE_ANON_KEY are not set on this deployment. "
            "Add them in Vercel and redeploy."
        )


def fetch_schemes():
    _require_config()
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/schemes?select=*",
        headers=_headers(),
        timeout=15,
    )
    response.raise_for_status()
    return response.json()
