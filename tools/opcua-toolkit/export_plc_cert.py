import asyncio
import hashlib
import json
from pathlib import Path
from asyncua import Client

ROOT = Path(__file__).resolve().parent
CERT_DIR = ROOT / "certificates"
CONFIG = ROOT / "config.json"

def load_config():
    return json.loads(CONFIG.read_text(encoding="utf-8"))

async def main():
    cfg = load_config()
    client = Client(cfg["endpoint"], timeout=15)
    print(f"Discovering OPC UA endpoint: {cfg['endpoint']}", flush=True)
    endpoints = await client.connect_and_get_server_endpoints()

    secure = next(
        (ep for ep in endpoints
         if ep.SecurityMode.value == 3
         and ep.SecurityPolicyUri.endswith("Basic256Sha256")),
        None,
    )
    if secure is None:
        raise RuntimeError("No Basic256Sha256 SignAndEncrypt endpoint was advertised.")

    certificate = secure.ServerCertificate
    if not certificate:
        raise RuntimeError("Server did not provide an application certificate.")

    CERT_DIR.mkdir(exist_ok=True)
    path = CERT_DIR / "plc-server.der"
    path.write_bytes(certificate)
    fingerprint = hashlib.sha256(certificate).hexdigest().upper()

    print("PLC server certificate exported.")
    print(f"File: {path}")
    print(f"Bytes: {len(certificate)}")
    print(f"SHA256: {fingerprint}")
    print("IMPORTANT: independently verify this fingerprint before trusting this certificate.")

if __name__ == "__main__":
    asyncio.run(main())
