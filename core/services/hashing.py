import hashlib
from typing import BinaryIO

def file_sha256(fileobj: BinaryIO) -> str:
    h = hashlib.sha256()
    for chunk in iter(lambda: fileobj.read(8192), b""):
        h.update(chunk)
    try:
        fileobj.seek(0)
    except Exception:
        pass
    return h.hexdigest()