import os
import json
import typing as t
import requests
from django.conf import settings
from core.services import storacha

class StorachaError(Exception):
    pass

def enabled() -> bool:
    return bool(
        getattr(settings, "STORACHA_ENABLED", False)
        and getattr(settings, "STORACHA_ENDPOINT", "")
        and getattr(settings, "STORACHA_API_KEY", "")
    )

def upload_file(fileobj: t.BinaryIO, filename: str) -> str:
    if not enabled():
        # Only warn if user expects real uploads
        if getattr(settings, "STORACHA_ENABLED", False):
            print("[storacha] falling back to mock CID: Storacha not enabled or misconfigured")
        raise StorachaError("Storacha not enabled or misconfigured")
    try:
        fileobj.seek(0)
    except Exception:
        pass
    headers = {"Authorization": f"Bearer {settings.STORACHA_API_KEY}"}
    files = {"file": (filename, fileobj)}
    try:
        resp = requests.post(
            settings.STORACHA_ENDPOINT,
            headers=headers,
            files=files,
            timeout=60,
        )
    except requests.RequestException as e:
        raise StorachaError(f"Network error: {e}") from e
    if not (200 <= resp.status_code < 300):
        raise StorachaError(f"HTTP {resp.status_code}: {resp.text[:200]}")
    try:
        data = resp.json()
    except json.JSONDecodeError:
        raise StorachaError("Non-JSON response from Storacha")
    cid = data.get("cid") or (data.get("data") or {}).get("cid") or (data.get("result") or {}).get("cid")
    if not cid:
        raise StorachaError(f"CID not found in response: {data}")
    return cid