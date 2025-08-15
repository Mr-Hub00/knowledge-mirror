import os, re, subprocess, threading, time

_SPACE_DID = os.environ.get("STORACHA_SPACE_DID", "").strip()
_BRIDGE_URL = os.environ.get("STORACHA_BRIDGE_URL", "https://up.storacha.network/bridge").strip()
_CAPS = [c.strip() for c in os.environ.get("STORACHA_CAN", "store/add,upload/add,upload/list").split(",") if c.strip()]
_TTL = int(os.environ.get("STORACHA_TOKEN_TTL_SECS", "21600"))  # 6h
_REFRESH_BUFFER = 300  # refresh 5 min early

_lock = threading.RLock()
_cache = {"auth": None, "secret": None, "exp": 0}

_AUTH_RE = re.compile(r"Authorization header:\s*([^\r\n]+)", re.S)
_SECR_RE = re.compile(r"X-Auth-Secret header:\s*([^\r\n]+)", re.S)

def _now() -> int:
    return int(time.time())

def _mint():
    if not _SPACE_DID:
        raise RuntimeError("STORACHA_SPACE_DID missing")

    exp = _now() + _TTL
    cmd = ["storacha", "bridge", "generate-tokens", _SPACE_DID, "--expiration", str(exp)]
    for c in _CAPS:
        cmd.extend(["--can", c])

    out = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)

    m_auth = _AUTH_RE.search(out)
    m_secr = _SECR_RE.search(out)
    if not (m_auth and m_secr):
        raise RuntimeError(f"Could not parse tokens from CLI output:\n{out}")

    auth = m_auth.group(1).strip()
    secr = m_secr.group(1).strip()

    if not re.match(r'^[A-Za-z0-9\-_\.]+$', auth):
        raise RuntimeError("Authorization token contains invalid characters")
    if not re.match(r'^[A-Za-z0-9\-_]+$', secr):
        raise RuntimeError("Secret token contains invalid characters")

    _cache.update({"auth": auth, "secret": secr, "exp": exp})

def get_headers():
    """Return fresh headers; auto‑refreshes if near expiry."""
    with _lock:
        if _now() >= (_cache["exp"] - _REFRESH_BUFFER):
            _mint()
        return {"Authorization": _cache["auth"], "X-Auth-Secret": _cache["secret"]}, _BRIDGE_URL