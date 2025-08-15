import os
import threading
import time
import subprocess
import shlex
from storacha_tokens import start_token_refresher, refresh_now

_REFRESH_INTERVAL = int(os.environ.get("STORACHA_TTL", "14400")) - 300  # 5 min before expiry
_REF_STARTED = False
_LOCK = threading.Lock()

def refresh_now():
    space_did = os.environ["STORACHA_SPACE_DID"]
    ttl       = int(os.environ.get("STORACHA_TTL", "14400"))   # 4h default
    caps      = os.environ.get("STORACHA_CAPABILITIES", "store/add,upload/add,upload/list")
    exp       = str(int(time.time()) + ttl)

    cmd = f'storacha bridge generate-tokens {shlex.quote(space_did)} ' \
          + ' '.join(f'--can {shlex.quote(c)}' for c in caps.split(',')) \
          + f' --expiration {exp}'

    out = subprocess.check_output(cmd, shell=True, text=True)

    import re
    secret = re.search(r"X-Auth-Secret header:\s*([^\r\n]+)", out).group(1).strip()
    auth   = re.search(r"Authorization header:\s*([^\r\n]+)", out).group(1).strip()

    if "..." in secret or "..." in auth:
        raise RuntimeError("Truncated header detected")
    if not secret or not auth:
        raise RuntimeError("Failed to parse tokens")

    os.environ["STORACHA_SECRET"] = secret
    os.environ["STORACHA_AUTH"]   = auth

def start_token_refresher():
    global _REF_STARTED
    with _LOCK:
        if _REF_STARTED:
            return
        _REF_STARTED = True

    def loop():
        try:
            refresh_now()
        except Exception as e:
            time.sleep(30)
        while True:
            ttl = int(os.environ.get("STORACHA_TTL", "14400"))
            safety = min(600, max(300, ttl // 10))
            sleep_s = max(900, ttl - safety)
            time.sleep(sleep_s)
            try:
                refresh_now()
            except Exception:
                time.sleep(60)

    t = threading.Thread(target=loop, name="storacha-token-refresher", daemon=True)
    t.start()