# Siemens OPC UA Read-only Toolkit

Windows toolkit for the simulated Siemens S7-1500 OPC UA server used by the Warehouse MES project.

## What it does

- Creates an isolated Python virtual environment.
- Installs `asyncua` into that environment.
- Generates a local MES application certificate and private key.
- Exports the PLC server certificate from the configured OPC UA endpoint.
- Tests a secure `Basic256Sha256 + SignAndEncrypt` connection.
- Browses OPC UA Objects and saves the discovered node tree to `plc_nodes.txt`.

**Safety:** the supplied scripts are read-only. They do not call OPC UA Write, Call, or PLC control methods. Do not add write operations to this toolkit without a separately reviewed PLC/MES handshake and machine-safety design.

## Requirements

- Windows 10/11
- Python 3.10 or newer available as the Windows `py` launcher
- Network access to the PLC/PLCSIM OPC UA endpoint
- TIA Portal configuration that enables OPC UA and trusts the MES client certificate

Default endpoint: `opc.tcp://192.168.0.1:4840`. Change it in `config.json` if your PLCSIM network uses another address.

## Install

1. Download this folder (or the ZIP package) to your Windows PC.
2. Open PowerShell in the extracted `opcua-toolkit` folder.
3. Run:

   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1
   ```

The installer creates `.venv`, installs dependencies, creates `certificates\` and writes a local `config.json`. It does not change TIA Portal or PLC settings.

## First-time setup

1. Run `powershell -NoProfile -ExecutionPolicy Bypass -File .\run-toolkit.ps1`.
2. Choose **1 - Generate MES client certificate**.
3. Import `certificates\mes-client.der` into the TIA Portal certificate manager and add it to the CPU's trusted OPC UA clients. Keep `mes-client-key.pem` private; never import or upload it.
4. Download/load the hardware configuration to PLCSIM if needed.
5. Choose **2 - Export PLC server certificate**. Verify that the PLC identity and certificate fingerprint are expected before relying on it.
6. Choose **3 - Test secure connection**.
7. Choose **4 - Browse PLC nodes**. Output is saved as `plc_nodes.txt`.

The TIA Portal certificate trust steps remain a manual engineering task and are not automated by this installer.

## Files

- `install.ps1`: local environment setup only.
- `run-toolkit.ps1`: interactive menu.
- `generate_client_cert.py`: creates a client certificate/key locally.
- `export_plc_cert.py`: exports the server certificate advertised by the endpoint.
- `secure_test.py`: verifies secure session and reads the namespace array.
- `browse_plc.py`: browses Objects and reads visible variables.
- `config.json`: generated locally; endpoint configuration.
- `certificates\`: generated locally; never commit private keys or certificates.

## Security notes

- The exported server certificate is obtained from the endpoint; this alone is not independent proof of PLC identity. Verify its fingerprint against a trusted engineering source before trusting it.
- Client and server application certificates are separate from OPC UA user authentication (Anonymous in the current endpoint discovery).
- A hostname warning means the client certificate's DNS names do not match the local hostname. Regenerate the client certificate on the target PC and re-import the new public certificate into TIA Portal.
- Do not disable certificate validation or switch to an unsecured endpoint to work around errors.
- The current test CPU identity observed in the user's session reported model **CPU 1516-3 PN/DP**, order number **6ES7 516-3AP03-0AB0**. Confirm the intended simulated CPU before using the node list.
