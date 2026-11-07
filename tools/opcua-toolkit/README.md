# Siemens OPC UA Read-only Toolkit

Windows toolkit for the simulated Siemens S7-1500 OPC UA server used by the Warehouse MES project.

## One-click start

1. Download and extract this folder (or the ZIP package).
2. Double-click **START.bat**.
3. The launcher installs the isolated Python environment, creates or retains the MES client certificate, exports the PLC server certificate, opens the certificate file in Explorer, and guides you through the TIA Portal trust step.
4. After you have imported the public client certificate into TIA Portal, added it to the CPU's OPC UA Trusted clients list, and compiled/loaded the configuration to PLCSIM if needed, return to the window and press ENTER.
5. The toolkit tests the secure connection and automatically writes the discovered node tree to plc_nodes.txt.

The installer creates a local Python environment, installs dependencies, and creates config.json from config.example.json. Default endpoint: opc.tcp://192.168.0.1:4840.

## Why TIA Portal still needs confirmation

Siemens documents importing a client certificate into TIA Portal's global Certificate Manager, adding it to the CPU's Trusted clients list, compiling, and loading the configuration. The toolkit automates certificate generation, export, file opening, connection testing, and browsing. It does not silently change a TIA Portal project or download a PLC configuration. Those engineering/security changes remain an explicit operator action.

## Security

- The supplied OPC UA scripts are read-only. They do not call OPC UA Write, Call, or PLC control methods.
- Import only certificates/mes-client.der. Never import, upload, email, or commit certificates/mes-client-key.pem.
- The exported PLC server certificate comes from the endpoint itself. Verify its SHA256 fingerprint through a trusted engineering route before relying on it.
- The client certificate is generated for the Windows hostname. If the PC hostname changes, regenerate the certificate and re-import the new public certificate.
- Do not disable certificate validation or switch to an unsecured endpoint to work around errors.

## Manual menu

Run run-toolkit.ps1 to use the individual tools:
1. Generate MES client certificate
2. Export PLC server certificate
3. Test secure OPC UA connection
4. Browse PLC nodes
5. Open toolkit folder

## Files

- START.bat: double-click launcher.
- install.ps1: isolated environment installation.
- first-run.ps1: first-run workflow and TIA trust handoff.
- run-toolkit.ps1: interactive menu.
- Python scripts: certificate generation/export, secure connection test, read-only browse.
- setup-log.txt: installation and first-run log.
