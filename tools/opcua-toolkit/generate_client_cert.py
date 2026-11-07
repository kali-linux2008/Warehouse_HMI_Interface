import asyncio
import json
import socket
from pathlib import Path
from asyncua import Client

ROOT = Path(__file__).resolve().parent
CERT_DIR = ROOT / "certificates"
CONFIG = ROOT / "config.json"

def endpoint():
    if CONFIG.exists():
        return json.loads(CONFIG.read_text(encoding="utf-8"))["endpoint"]
    return "opc.tcp://192.168.0.1:4840"

async def main():
    CERT_DIR.mkdir(exist_ok=True)
    key = CERT_DIR / "mes-client-key.pem"
    cert = CERT_DIR / "mes-client.der"
    hostname = socket.gethostname()

    if key.exists() or cert.exists():
        answer = input(
            "A client certificate already exists. Replace it? "
            "This requires re-importing the new .der in TIA Portal (y/N): "
        )
        if answer.strip().lower() != "y":
            print("Cancelled; existing certificate retained.")
            return

    client = Client(endpoint(), timeout=10)
    client.application_uri = f"urn:{hostname}:WarehouseMES:OPCUAClient"

    await client.setup_self_signed_certificate(
        key,
        cert,
        subject_attrs={
            "countryName": "NL",
            "organizationName": "Warehouse MES",
            "commonName": f"Warehouse MES on {hostname}",
        },
        host_name=hostname,
    )

    print("Client certificate generated locally.")
    print(f"Public certificate: {cert}")
    print(f"PRIVATE KEY (keep secret): {key}")
    print("Import only the .der public certificate into TIA Portal Trusted clients.")
    print("Do not upload, email, or commit the private key.")

if __name__ == "__main__":
    asyncio.run(main())
