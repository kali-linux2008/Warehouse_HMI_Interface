# OPC UA discovery snapshot — 2026-11-07

This is a summary of the user's successful read-only browse of the simulated PLC using Python `asyncua` 2.1.0 over OPC UA SecureChannel.

## Connection result

- Endpoint: `opc.tcp://192.168.0.1:4840`
- Security policy: `Basic256Sha256`
- Security mode: `SignAndEncrypt`
- Session: successful
- NamespaceArray:
  - `http://opcfoundation.org/UA/`
  - `urn:SIMATIC.S7-1500.OPC-UA.Application:PLC_1`
  - `http://opcfoundation.org/UA/DI/`
  - `http://www.siemens.com/simatic-s7-opcua`
- Browse result: 268 nodes visited in the first scan.

## Important device identity discrepancy

The OPC UA DeviceSet metadata returned:
- Model: `CPU 1516-3 PN/DP`
- Order number: `6ES7 516-3AP03-0AB0`
- Engineering revision: `V20.0.0.0`
- Software revision: `V04.00.00`

The project was previously described as an S7-1515-2 PN. Confirm that the PLCSIM instance and intended CPU are the same before using these node IDs or mapping tags.

## Discovered data areas

### `DB_Tracking`

Observed variables/structures:
- `Onderweg`
- `ST01`, `ST02`, `ST03`
- `Robot1`, `Robot2`
- `Pallet_Robot_1`, `Pallet_Robot_2`
- `Onderweg_Aantal`
- `Lid_Verwacht`
- `Doel`
- `Status_Robot_1`, `Status_Robot_2`
- `Naar_Magazijn`
- `Naar_Magazijn_Aantal`
- `Magazijn_Ingang`

### `DB_HMI`

Observed variables include:
- Mode/alarm: `Modus`, `Alarm_Woord`, `Alarm_Aantal`, `Alarm_Nr`, `Alarm_Ernst`
- Storage: `Vak_Status`, `K1_Kolom`, `K1_Laag`, `K1_Kant`, `K1_Status`, corresponding `K2_*`, `Bezetting_K1`, `Bezetting_K2`
- Throughput/age: `Inslag_Uur`, `Uitslag_Uur`, `Oudste_Vak`, `Oudste_Uren`
- Machine states: `Invoer_Status`, `Uitvoer_Status`, `K1_*`, `K2_*`
- HMI commands exist, including `Cmd_Start`, `Cmd_Stop`, `Cmd_Reset`, `Cmd_Hand`, crane and fork commands.

**Do not write to these HMI command tags from the MES.** They are machine-control interfaces and are not a substitute for a dedicated MES handshake.

### Inputs

Examples observed:
- `S1_SE01_Base`, `S1_SE02_Lid`, `S1_SE03_AtStop`
- `S1_PU01_Front`, `S1_PU01_Back`
- `S3_SE01_Palletaankomst`, `S3_SE03_Robot_1`, `S3_SE04_Robot_2`, `S3_SE02_Buffer`
- `S4_RO04_Detected`, `S5_RO04_Detected`
- `S6_SE01_Magazijn_Ingang`

### Outputs

Examples observed:
- `S1_EM01_Emit`, `S1_EM02_Emit`, `S1_PU01_Push`
- `S1_CV01_Run` through `S1_CV04_Run`
- `S1_ST01_UP` through `S1_ST03_UP`
- `S3_ST01_UP` through `S3_ST03_UP`
- `S3_CV01_Run` through `S3_CV03_Run`
- Robot axis/gripper outputs under `S4_*` and `S5_*`

## Next engineering steps

1. Export the complete current `plc_nodes.txt` from the PC and review all node IDs, types, access levels and structure encodings.
2. Confirm the simulated CPU identity.
3. Design a dedicated `DB_MES` in TIA Portal for order transfer, acknowledgement, cancellation, heartbeat and status.
4. Implement PLC-side handshake logic with validation, duplicate protection, bounds checking and safe state handling.
5. Test with a dedicated simulation scenario before enabling any OPC UA writes.
