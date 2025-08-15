import os
import requests

BRIDGE_URL = os.getenv("STORACHA_BRIDGE_URL", "https://up.storacha.network/bridge")
SPACE_DID = os.getenv("STORACHA_SPACE_DID")
AUTH = os.getenv("STORACHA_AUTH")       # from bridge generate-tokens (Authorization)
SECRET = os.getenv("STORACHA_SECRET")   # from bridge generate-tokens (X-Auth-Secret)

class StorachaError(Exception):
    pass

def _headers():
    if not (AUTH and SECRET):
        raise StorachaError("Storacha bridge headers missing; set STORACHA_AUTH and STORACHA_SECRET.")
    return {
        "Authorization": AUTH,
        "X-Auth-Secret": SECRET,
        "Content-Type": "application/json",
    }

def upload_small_car(car_bytes: bytes, bag_cid: str, bafy_root_cid: str) -> str:
    """
    car_bytes: the CAR file bytes for your content
    bag_cid:   CID of the CAR itself (starts with bag...)
    bafy_root_cid: CID of the DAG root for your content (starts with bafy...)

    Returns the bafy root CID when registered.
    """
    # 1) Ask bridge to allocate storage + register upload
    tasks = {
        "tasks": [
            [
                "store/add",
                SPACE_DID,
                {
                    "link": {"/": bag_cid},
                    "size": len(car_bytes),
                },
            ],
            [
                "upload/add",
                SPACE_DID,
                {
                    "root": {"/": bafy_root_cid},
                    "shards": [{"/": bag_cid}],
                },
            ],
        ]
    }

    resp = requests.post(BRIDGE_URL, json=tasks, headers=_headers(), timeout=60)
    if resp.status_code != 200:
        raise StorachaError(f"Bridge call failed: {resp.status_code} {resp.text}")

    results = resp.json()

    # results[0] -> store/add
    store_ok = results[0]["p"]["out"]["ok"]
    status = store_ok.get("status")
    if status == "upload":
        # 2) We must PUT the CAR to S3 with the provided headers
        put_url = store_ok["url"]
        put_headers = store_ok["headers"]  # contains content-length, x-amz-checksum-sha256, etc.
        # strongly recommended by AWS to include content-type
        put_headers["content-type"] = "application/vnd.ipld.car"

        put_resp = requests.put(put_url, data=car_bytes, headers=put_headers, timeout=300)
        if put_resp.status_code not in (200, 201):
            raise StorachaError(f"CAR PUT failed: {put_resp.status_code} {put_resp.text}")

    # results[1] -> upload/add (registration)
    # If we get here without exception, upload is registered
    return