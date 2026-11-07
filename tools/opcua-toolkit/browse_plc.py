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

    client = Client(CONFIG["endpoint"], timeout=20)
    await client.set_security(
        SecurityPolicyBasic256Sha256,
        certificate=str(cert),
        private_key=str(key),
        server_certificate=str(server_cert),
        mode=ua.MessageSecurityMode.SignAndEncrypt,
    )

    max_nodes = int(CONFIG.get("browse_max_nodes", 1500))
    max_depth = int(CONFIG.get("browse_max_depth", 8))
    output = []
    visited = set()
    count = 0

    async def browse(node, depth=0):
        nonlocal count
        if count >= max_nodes or depth > max_depth:
            return
        node_id = node.nodeid.to_string()
        if node_id in visited:
            return
        visited.add(node_id)
        count += 1

        try:
            browse_name = await node.read_browse_name()
            node_class = await node.read_node_class()
            line = "  " * depth + f"{browse_name.Name} | {node_id} | {node_class.name}"

            if node_class == ua.NodeClass.Variable:
                try:
                    value = await node.read_value()
                    value_text = repr(value).replace("\\n", " ")
                    if len(value_text) > 180:
                        value_text = value_text[:177] + "..."
                    line += f" | Value: {value_text}"
                except Exception as exc:
                    line += f" | Read error: {type(exc).__name__}: {exc}"

            output.append(line)
            print(line, flush=True)

            # Browse Objects and Variables with children (e.g. structured values).
            if node_class in (ua.NodeClass.Object, ua.NodeClass.Variable):
                try:
                    children = await node.get_children()
                except Exception:
                    children = []
                for child in children:
                    await browse(child, depth + 1)
        except Exception as exc:
            line = f"{node_id} | Browse error: {type(exc).__name__}: {exc}"
            output.append(line)
            print(line, flush=True)

    connected = False
    try:
        print(f"Connecting: {CONFIG['endpoint']}", flush=True)
        await client.connect()
        connected = True
        print("Connected securely. NamespaceArray:", await client.get_namespace_array(), flush=True)
        print("\nOPC UA Objects tree (read-only):", flush=True)
        await browse(client.nodes.objects)

        output_path = ROOT / CONFIG.get("output_file", "plc_nodes.txt")
        output_path.write_text("\n".join(output) + "\n", encoding="utf-8")
        print(f"\nFinished: {count} nodes visited.", flush=True)
        print(f"Saved: {output_path}", flush=True)
        print("No PLC values were written.", flush=True)
    finally:
        if connected:
            await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
