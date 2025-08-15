import hmac
import time
import hashlib
import secrets
from django.conf import settings

def make_share_token(stamp_id: int, now: int | None = None) -> str:
    now = now or int(time.time())
    msg = f"{stamp_id}:{now}".encode()
    sig = hmac.new(settings.SECRET_KEY.encode(), msg, hashlib.sha256).hexdigest()[:32]
    return f"{now}.{sig}"

def verify_share_token(stamp_id: int, token: str) -> bool:
    try:
        ts_str, sig = token.split(".", 1)
        ts = int(ts_str)
    except Exception:
        return False

    ttl = getattr(settings, "SHARELINK_TTL_SECONDS", 3600)
    if int(time.time()) - ts > ttl:
        return False

    msg = f"{stamp_id}:{ts}".encode()
    expected = hmac.new(settings.SECRET_KEY.encode(), msg, hashlib.sha256).hexdigest()[:32]
    return hmac.compare_digest(expected, sig)

def random_share_token(n_bytes: int = 24) -> str:
    return secrets.token_urlsafe(n_bytes)