import os
import threading
import time
import subprocess
import shlex

# --- your real refresh code should live inside these two functions ---

def refresh_now() -> bool:
    """
    Generate/refresh STORACHA_SECRET and STORACHA_AUTH and export them to env.
    Return True on success, False on failure.
    """
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
    return True

def start_token_refresher(interval_seconds: int = 50 * 60) -> None:
    """
    Starts a background thread that calls refresh_now() periodically.
    """
    def loop():
        while True:
            try:
                refresh_now()
            except Exception as e:
                # Optional: log/print e
                pass
            time.sleep(interval_seconds)

    t = threading.Thread(target=loop, name="storacha-token-refresher", daemon=True)
    t.start()