import asyncio
import json
from pathlib import Path
from asyncua import Client, ua
from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256

ROOT = Path(__file__).resolve().parent
CERT_DIR = ROOT / "certificates"
CONFIG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))

async def main():
    cert = CERT_DIR / "mes-client.der"
    key = CERT_DIR / "mes-client-key.pem"
    server_cert = CERT_DIR / "plc-server.der"

    for path in (cert, key, server_cert):
        if not path.is_file():
            raise FileNotFoundError(f"Required certificate file missing: {path}")

    client = Client(CONFIG["endpoint"], timeout=15)
    await client.set_security(
        SecurityPolicyBasic256Sha256,
        certificate=str(cert),
        private_key=str(key),
        server_certificate=str(server_cert),
        mode=ua.MessageSecurityMode.SignAndEncrypt,
    )

    connected = False
    try:
        print("[1] Connecting with Basic256Sha256 + SignAndEncrypt...", flush=True)
        await asyncio.wait_for(client.connect(), timeout=25)
        connected = True
        print("[2] SECURE CONNECTION SUCCESSFUL", flush=True)
        namespaces = await asyncio.wait_for(client.get_namespace_array(), timeout=10)
        print("[3] NamespaceArray:", namespaces, flush=True)
        print("[4] Read-only test complete; no PLC values were written.", flush=True)
    finally:
        if connected:
            await client.disconnect()
            print("[5] Disconnected.", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
