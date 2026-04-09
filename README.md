# gtpc — GTP Control Plane Packet Library

A standalone Python library for building and parsing **GTPv1-C** (3GPP TS 29.060) and **GTPv2-C** (3GPP TS 29.274) telecom packets. No external dependencies — pure Python stdlib.

Modelled after the [Wireshark EPAN dissectors](https://gitlab.com/wireshark/wireshark/-/blob/master/epan/dissectors/packet-gtp.c) (`packet-gtp.c` and `packet-gtpv2.c`), covering all standardised message types and information elements.

---

## Features

- **All message types** — every GTPv1-C and GTPv2-C message type from the 3GPP specs
- **All major IEs** — typed Information Element classes with field-level encode/decode
- **Fluent builder API** — chain `set_*()`/`add_*()` calls to build packets quickly
- **IE registry dispatch** — decoding returns typed subclasses (same model as Wireshark dissector tables)
- **Grouped IEs** — `BearerContextIE` nests child IEs for GTPv2 bearer handling
- **BCD/PLMN utilities** — IMSI, MSISDN, MEI, MCC/MNC encoding built-in
- **Hex I/O** — parse raw hex strings, print Wireshark-style hex dumps
- **Zero external deps** — only `struct`, `socket`, `dataclasses` from stdlib

---

## Installation

```bash
git clone https://github.com/you/gtp-tester
cd gtp-tester
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

---

## Quick Start

### Decode a raw packet

```python
from gtpc.utils.hexdump import from_hex
from gtpc.v1.messages import decode_message

raw = from_hex(
    "321000970000000000fe00000272020301000000f003"
    "72f230fffeff0e5d0ffc10372f000011372f00001405"
    "800002f121830010036d6d73086d796d6574656f7202"
    "696584002280c023..."
)

msg = decode_message(raw)
print(msg)
# Create PDP Context Request(teid=0x00000000, seq=254, ies=[...])

print(msg.imsi)   # '272030100000000'
print(msg.apn)    # 'mms.mymeteor.ie'
print(msg.nsapi)  # 5
```

### Hex dump

```python
from gtpc.utils.hexdump import hexdump
print(hexdump(raw))
# 0000  32 10 00 97 00 00 00 00  00 fe 00 00 02 72 02 03  2........ .r..
# 0010  ...
```

---

## GTPv1-C Examples

### Echo Request / Response

```python
from gtpc.v1.messages import EchoRequest, EchoResponse, decode_message
from gtpc.v1 import constants as C

# Build an Echo Request
req = EchoRequest(teid=0, seq_num=1)
req.set_recovery(42)
raw = req.encode()

# Decode it back
msg = decode_message(raw)
assert isinstance(msg, EchoRequest)
print(msg.get_ie(C.IE_RECOVERY).restart_counter)  # 42
```

### Create PDP Context Request (2G/3G attach)

```python
import socket
from gtpc.v1.messages import CreatePDPContextRequest, decode_message
from gtpc.v1.ie.tlv import EndUserAddressIE
from gtpc.v1 import constants as C

msg = CreatePDPContextRequest(teid=0, seq_num=100)
msg.set_imsi("272030100000000")
msg.set_rai("272", "03", lac=1234, rac=5)
msg.set_selection_mode(C.SEL_MODE_MS_OR_NET_APN_SUBSCR_VERIFIED)
msg.set_teid_data(0x372F0000)
msg.set_teid_control(0x372F0001)
msg.set_nsapi(5)
msg.set_end_user_address(
    pdp_type_org=EndUserAddressIE.PTO_IETF,
    pdp_type_num=EndUserAddressIE.PDN_IPv4,
)
msg.set_apn("internet.operator.com")
msg.set_sgsn_address_signalling(socket.inet_aton("10.0.0.1"))
msg.set_sgsn_address_user_traffic(socket.inet_aton("10.0.0.2"))
msg.set_msisdn("353871234567")
msg.set_rat_type(C.RAT_UTRAN)
msg.set_imei_sv("35492910432898")
msg.set_uli(glt=0, location=b"\x02\x72\xf2\x30\x04\xD2\x00\x05")
msg.set_ms_timezone(tz=0x40, dst=0)

raw = msg.encode()
print(f"Packet: {len(raw)} bytes")
print(f"  IMSI:  {msg.imsi}")
print(f"  APN:   {msg.apn}")
print(f"  NSAPI: {msg.nsapi}")
```

### Create PDP Context Response

```python
from gtpc.v1.messages import CreatePDPContextResponse
from gtpc.v1 import constants as C
import socket

rsp = CreatePDPContextResponse(teid=0x372F0000, seq_num=100)
rsp.set_cause(C.CAUSE_REQUEST_ACCEPTED)
rsp.set_recovery(0)
rsp.set_teid_data(0xAABBCCDD)
rsp.set_teid_control(0x11223344)
rsp.set_charging_id(0x0000CAFE)
rsp.set_end_user_address(pdp_type_org=1, pdp_type_num=0x21,
                          address=socket.inet_aton("10.20.30.40"))
rsp.set_ggsn_address_signalling(socket.inet_aton("192.168.1.1"))
rsp.set_ggsn_address_user_traffic(socket.inet_aton("192.168.1.2"))

raw = rsp.encode()
```

### Delete PDP Context

```python
from gtpc.v1.messages import DeletePDPContextRequest, DeletePDPContextResponse
from gtpc.v1 import constants as C

req = DeletePDPContextRequest(teid=0xAABBCCDD, seq_num=200)
req.set_teardown_ind(teardown=True)
req.set_nsapi(5)

rsp = DeletePDPContextResponse(teid=0xAABBCCDD, seq_num=200)
rsp.set_cause(C.CAUSE_REQUEST_ACCEPTED)
```

### SGSN Context (inter-SGSN handover)

```python
from gtpc.v1.messages import SGSNContextRequest, SGSNContextResponse
import socket

req = SGSNContextRequest(teid=0, seq_num=55)
req.set_imsi("272030100000000")
req.set_rai("272", "03", lac=1, rac=1)
req.set_teid_control(0x12345678)
req.set_sgsn_address(socket.inet_aton("10.0.1.1"))
req.set_nsapi(5)

rsp = SGSNContextResponse(teid=0x12345678, seq_num=55)
rsp.set_cause(128)  # Request Accepted
```

### Forward Relocation (UMTS handover)

```python
from gtpc.v1.messages import ForwardRelocationRequest
import socket

req = ForwardRelocationRequest(teid=0, seq_num=77)
req.set_imsi("272030100000000")
req.set_rai("272", "03", lac=100, rac=10)
req.set_teid_control(0xDEADBEEF)
req.set_sgsn_address_signalling(socket.inet_aton("10.0.2.1"))
req.set_sgsn_address_user_traffic(socket.inet_aton("10.0.2.2"))
```

---

## GTPv2-C Examples

### Echo Request / Response (S11 interface keepalive)

```python
from gtpc.v2.messages import EchoRequest, EchoResponse, decode_message

req = EchoRequest(teid=None, seq_num=1)
req.set_recovery(0)
raw = req.encode()

msg = decode_message(raw)
assert isinstance(msg, EchoRequest)
```

### Create Session Request (LTE attach / PDN connection)

```python
from gtpc.v2.messages import CreateSessionRequest, decode_message
from gtpc.v2.ie.typed import (
    ULIIE, FTEIDIE, BearerContextIE, BearerQoSIE,
    EBIIE, PAAIE,
)
from gtpc.v2 import constants as C

# --- Build a bearer context ---
bearer = BearerContextIE()
bearer.add_ie(EBIIE(ebi=5))
bearer.add_ie(FTEIDIE(
    interface_type=C.FTEID_S1U_ENODEB,
    teid=0xAABBCCDD,
    ipv4="192.168.10.50",
))
bearer.add_ie(BearerQoSIE(
    qci=9, pl=9, pci=False, pvi=False,
    mbr_ul=128_000, mbr_dl=128_000,
    gbr_ul=0,      gbr_dl=0,
))

# --- Build the Create Session Request ---
msg = CreateSessionRequest(teid=None, seq_num=42)
msg.set_imsi("272030100000000")
msg.set_msisdn("353871234567")
msg.set_mei("3549291043289800")
msg.set_rat_type(C.RAT_EUTRAN)
msg.set_serving_network(mcc="272", mnc="03")
msg.set_uli(ULIIE.with_tai_and_ecgi("272", "03", tac=0x1234, eci=0xABCDE))
msg.set_apn("internet")
msg.set_selection_mode(0)
msg.set_pdn_type(C.PDN_TYPE_IPv4)
msg.set_paa(PAAIE(C.PDN_TYPE_IPv4, "0.0.0.0"))
msg.set_ambr(uplink_kbps=100_000, downlink_kbps=200_000)
msg.set_sender_fteid(FTEIDIE(C.FTEID_S11_MME, teid=0x11111111, ipv4="10.0.0.1"))
msg.set_pgw_fteid(FTEIDIE(C.FTEID_S5S8C_PGW, teid=0x22222222, ipv4="10.0.1.1"))
msg.add_bearer_context(bearer)

raw = msg.encode()
print(f"CSR: {len(raw)} bytes, IMSI={msg.imsi}, APN={msg.apn}")

# Decode
d = decode_message(raw)
ctxs = d.bearer_contexts
print(f"Bearer EBI: {ctxs[0].get_ie(C.IE_EBI).ebi}")  # 5
```

### Create Session Response

```python
from gtpc.v2.messages import CreateSessionResponse
from gtpc.v2.ie.typed import FTEIDIE, PAAIE, BearerContextIE, EBIIE
from gtpc.v2 import constants as C

bearer = BearerContextIE()
bearer.add_ie(EBIIE(5))
bearer.add_ie(FTEIDIE(C.FTEID_S1U_SGW, teid=0x33333333, ipv4="10.0.2.1"))

rsp = CreateSessionResponse(teid=0x11111111, seq_num=42)
rsp.set_cause(C.CAUSE_REQUEST_ACCEPTED)
rsp.set_sender_fteid(FTEIDIE(C.FTEID_S11S4_SGW, teid=0x44444444, ipv4="10.0.0.2"))
rsp.set_paa(PAAIE(C.PDN_TYPE_IPv4, "100.64.0.1"))
rsp.set_ambr(100_000, 200_000)
rsp.add_bearer_context(bearer)
```

### Modify Bearer Request

```python
from gtpc.v2.messages import ModifyBearerRequest
from gtpc.v2.ie.typed import BearerContextIE, EBIIE, FTEIDIE, ULIIE
from gtpc.v2 import constants as C

ctx = BearerContextIE()
ctx.add_ie(EBIIE(5))
ctx.add_ie(FTEIDIE(C.FTEID_S1U_ENODEB, teid=0xBBBBBBBB, ipv4="192.168.10.51"))

msg = ModifyBearerRequest(teid=0x44444444, seq_num=100)
msg.set_uli(ULIIE.with_tai("272", "03", tac=0x5678))
msg.set_rat_type(C.RAT_EUTRAN)
msg.add_bearer_context(ctx)
```

### Delete Session Request

```python
from gtpc.v2.messages import DeleteSessionRequest
from gtpc.v2 import constants as C

msg = DeleteSessionRequest(teid=0x44444444, seq_num=200)
msg.set_ebi(5)
msg.set_cause(C.CAUSE_LOCAL_DETACH)
```

### Create Bearer Request (dedicated bearer, e.g. VoLTE)

```python
from gtpc.v2.messages import CreateBearerRequest
from gtpc.v2.ie.typed import BearerContextIE, EBIIE, FTEIDIE, BearerQoSIE
from gtpc.v2 import constants as C

# Dedicated bearer (EBI 6, QCI 1 for VoLTE)
bearer = BearerContextIE()
bearer.add_ie(EBIIE(ebi=6))
bearer.add_ie(FTEIDIE(C.FTEID_S5S8U_PGW, teid=0x55555555, ipv4="10.0.3.1"))
bearer.add_ie(BearerQoSIE(
    qci=1, pl=2, pci=False, pvi=False,
    mbr_ul=40_000, mbr_dl=40_000,
    gbr_ul=40_000, gbr_dl=40_000,
))

msg = CreateBearerRequest(teid=0x11111111, seq_num=300)
msg.set_linked_ebi(5)   # linked to the default bearer
msg.add_bearer_context(bearer)
```

### Downlink Data Notification (idle mode, paging trigger)

```python
from gtpc.v2.messages import DownlinkDataNotification
from gtpc.v2.ie.typed import ARPIE
from gtpc.v2 import constants as C

msg = DownlinkDataNotification(teid=0x11111111, seq_num=400)
msg.set_ebi(5)
msg.set_arp(ARPIE(pl=9, pci=False, pvi=False))
```

### Release Access Bearers (UE goes idle)

```python
from gtpc.v2.messages import ReleaseAccessBearersRequest, ReleaseAccessBearersResponse
from gtpc.v2 import constants as C

req = ReleaseAccessBearersRequest(teid=0x44444444, seq_num=500)

rsp = ReleaseAccessBearersResponse(teid=0x11111111, seq_num=500)
rsp.set_cause(C.CAUSE_REQUEST_ACCEPTED)
```

### Forward Relocation (S1/X2 handover)

```python
from gtpc.v2.messages import ForwardRelocationRequest
from gtpc.v2.ie.typed import FTEIDIE, BearerContextIE, EBIIE
from gtpc.v2 import constants as C
import socket

bearer = BearerContextIE()
bearer.add_ie(EBIIE(5))

msg = ForwardRelocationRequest(teid=0, seq_num=1)
msg.set_imsi("272030100000000")
msg.set_sender_fteid(FTEIDIE(C.FTEID_S10_MME, teid=0xCCCCCCCC, ipv4="10.1.1.1"))
msg.set_rat_type(C.RAT_EUTRAN)
msg.add_bearer_context(bearer)
```

---

## Accessing IEs

All message classes expose named property accessors for common IEs, and a generic `get_ie()` / `get_ies()` fallback for everything else.

```python
# Named accessors
msg.imsi          # str | None
msg.apn           # str | None
msg.nsapi         # int | None   (v1)
msg.teid_data     # int | None   (v1)
msg.cause         # int | None   (response messages)
msg.pdn_type      # int | None   (v2)
msg.bearer_contexts  # list[BearerContextIE]  (v2)

# Generic lookup by IE type code
ie = msg.get_ie(C.IE_RECOVERY)
ie.restart_counter   # → int

# Multiple IEs of same type
addrs = msg.get_ies(C.IE_GSN_ADDRESS)  # → list[GSNAddressIE]
for a in addrs:
    print(a.address.hex())

# GTPv2: lookup by type + instance number
fteid0 = msg.get_ie(C.IE_F_TEID, instance=0)  # sender F-TEID
fteid1 = msg.get_ie(C.IE_F_TEID, instance=1)  # PGW F-TEID
```

---

## Utilities

### BCD encoding (IMSI, MSISDN, MEI)

```python
from gtpc.utils.bcd import encode, decode

raw = encode("272030100000000")   # → b'\x72\x20\x30\x01\x00\x00\x00\xf0'
digits = decode(raw)              # → '272030100000000'
```

### PLMN encoding (MCC/MNC)

```python
from gtpc.utils.plmn import encode, decode

plmn = encode("310", "410")       # → b'\x13\xf0\x14'
mcc, mnc = decode(plmn)           # → ('310', '410')

plmn2 = encode("234", "15")       # 2-digit MNC
mcc2, mnc2 = decode(plmn2)        # → ('234', '15')
```

### Hex I/O

```python
from gtpc.utils.hexdump import from_hex, hexdump

raw = from_hex("32 10 00 97 00 00 00 00")   # spaces OK
raw = from_hex("32:10:00:97")               # colons OK
raw = from_hex("32100097")                  # plain hex OK

print(hexdump(raw))
# 0000  32 10 00 97                                        2...
```

---

## Running Tests

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[test]"
pytest tests/ -v
```

122 tests cover:
- Header encode/decode round-trips for both versions
- Every typed IE with field-level assertions
- Reference packet decoding from a real-world capture (`sample-hex.txt`)
- Build-and-decode smoke test for every message type

---

## Example Script

`examples/generate_samples.py` builds 68 sample packets across both protocol versions, writes them to `examples/sample_packets.hex`, and verifies every packet with an encode → decode → re-encode round-trip.

```bash
python3 examples/generate_samples.py [output_file]
# Wrote 68 packets to examples/sample_packets.hex
#   GTPv1-C packets : 21
#   GTPv2-C packets : 47
#   Total bytes     : 2643
# All 68 packets verified (encode → decode → re-encode round-trip OK)
```

The hex file uses a simple text format — one entry per packet:

```
# GTPv1 Create PDP Context Request
32100043000000000064000002720203...

# GTPv2 Create Session Request
480100...
```

Read a packet back with:

```python
from gtpc.utils.hexdump import from_hex
from gtpc.v1.messages import decode_message

with open("examples/sample_packets.hex") as f:
    for line in f:
        line = line.strip()
        if line.startswith("#") or not line:
            continue
        msg = decode_message(from_hex(line))
        print(msg)
```

### Packets generated

| Protocol | Count | Message types |
|----------|-------|---------------|
| GTPv1-C  | 21    | Echo Req/Res, Create/Update/Delete PDP Ctx (Req+Res), Error Indication, PDU Notification, SGSN Context (Req/Res/Ack), Forward Relocation (Req/Res), Relocation Cancel, MBMS Session Start Req/Res, Data Record Transfer |
| GTPv2-C  | 47    | Echo, Create/Modify/Delete Session, Create/Update/Delete Bearer, Bearer Resource Cmd, Modify/Delete Bearer Cmd, Release Access Bearers, Downlink Data Notification, Context (Req/Res/Ack), Forward Relocation (Req/Res/Complete/Ack), Detach/Suspend/Resume Notifications, PGW Restart, Stop Paging, Delete PDN Conn Set, Modify Access Bearers, MBMS Session Start/Stop, Trace Session Activation |

---

## Technical Reference

### GTPv1-C Header (TS 29.060 §6)

```
 0               1               2               3
 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|PT |Sp |E|S|PN|  Type  |           Length              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                     Tunnel Endpoint ID                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Sequence Number       |  N-PDU Number |Next Ext Hdr   |  (optional)
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

Two IE encoding formats:
- **TV** (type 1–127, bit 7 = 0) — fixed-length, lengths defined in `TV_LEN` dict
- **TLV** (type 128–255, bit 7 = 1) — 2-byte length field follows type byte

### GTPv2-C Header (TS 29.274 §5.1)

```
 0               1               2               3
 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|P|T|Sp |  Message Type |           Length              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                 TEID (if T=1)                                 |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Sequence Number (24 bits)           |    Spare      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

All IEs use **TLIV** encoding:

```
+---------+---------+---------+---------+----------...----------+
| Type 1B | Len  2B |Inst  1B |       Value (Len bytes)        |
+---------+---------+---------+---------+----------...----------+
```

`Instance` (low nibble of byte 3) disambiguates multiple IEs of the same type in one message (e.g., two F-TEIDs with instance 0 and 1).

### Message Type Coverage

| Version | Standard       | Messages |
|---------|----------------|----------|
| GTPv1-C | 3GPP TS 29.060 | 40+ types: path management, tunnel management (Create/Update/Delete PDP Context), location management (GTP'), mobility (SGSN Context, Forward Relocation), MBMS (types 96–121), CDR transfer |
| GTPv2-C | 3GPP TS 29.274 | 80+ types: path management, session management, bearer management, bearer resource commands, mobility/handover, notifications, forwarding tunnels, PDN connection sets, MBMS |

### IE Coverage

| Version | IEs |
|---------|-----|
| GTPv1   | Cause, IMSI, RAI, TLLI, P-TMSI, Recovery, Selection Mode, TEID Data I/II, TEID C-Plane, Teardown Ind, NSAPI, Charging Chars/ID, APN, End User Address, PCO, GSN Address, MSISDN, QoS Profile, TFT, ULI, MS Time Zone, IMEI-SV, RAT Type, Common Flags, APN Restriction, Private Extension + raw fallback for all others |
| GTPv2   | IMSI, Cause, Recovery, APN, AMBR, EBI, IP Address, MEI, MSISDN, Indication, PCO, PAA, Bearer QoS, Flow QoS, RAT Type, Serving Network, Bearer TFT, ULI (CGI/SAI/RAI/TAI/ECGI/LAI), F-TEID, Bearer Context (grouped), Charging ID/Chars, Bearer Flags, PDN Type, PTI, UE Time Zone, APN Restriction, Selection Mode, FQ-CSID, Node Type, FQDN, ARP, APCO, Private Extension + raw fallback for all others |

### Architecture

```
gtpc/
├── utils/
│   ├── bcd.py          BCD encode/decode (IMSI, MSISDN, MEI)
│   ├── plmn.py         MCC/MNC ↔ 3-byte PLMN encoding
│   └── hexdump.py      Hex string parsing and Wireshark-style dump
├── v1/
│   ├── constants.py    Message type codes, IE codes, cause values
│   ├── header.py       GTPv1Header encode/decode
│   ├── ie/
│   │   ├── base.py     IEv1 base class + decode_ies()
│   │   ├── tv.py       Typed TV IEs (fixed-length)
│   │   ├── tlv.py      Typed TLV IEs (variable-length)
│   │   └── registry.py IE type → class dispatch table
│   └── messages/
│       ├── base.py     GTPv1Message base
│       ├── path.py     Echo, Version Not Supported
│       ├── tunnel.py   Create/Update/Delete PDP Context
│       ├── notification.py  Error Indication, PDU Notification
│       ├── location.py Send Routeing Info, Failure Report
│       ├── mobility.py SGSN Context, Forward Relocation, RAN Info
│       ├── mbms.py     MBMS messages (96–121)
│       ├── cdr.py      Data Record Transfer
│       └── registry.py MSG type → class dispatch + decode_message()
└── v2/
    ├── constants.py    Message type codes, IE codes, cause values
    ├── header.py       GTPv2Header encode/decode
    ├── ie/
    │   ├── base.py     IEv2 TLIV base class + decode_ies()
    │   ├── typed.py    All typed IE subclasses
    │   └── registry.py IE type → class dispatch table
    └── messages/
        ├── base.py     GTPv2Message base
        ├── path.py     Echo, Version Not Supported
        ├── session.py  Create/Modify/Delete Session, Change Notification
        ├── bearer.py   Create/Update/Delete Bearer, Delete PDN Conn Set
        ├── commands.py Modify/Delete Bearer Cmd, Bearer Resource Cmd
        ├── mobility.py Identification, Context, Forward Relocation
        ├── notification.py Detach, Suspend, Resume, PGW Restart, etc.
        ├── forwarding.py   Forwarding tunnels, Release Access Bearers, DL Data Notif
        ├── pdn.py      Update PDN Conn Set, Modify Access Bearers
        ├── mbms.py     MBMS Session Start/Update/Stop (231–236)
        └── registry.py MSG type → class dispatch + decode_message()
```

### References

- [3GPP TS 29.060](https://www.3gpp.org/DynaReport/29060.htm) — GTP across Gn/Gp interfaces (GTPv1-C)
- [3GPP TS 29.274](https://www.3gpp.org/DynaReport/29274.htm) — GTPv2-C for EPC
- [Wireshark packet-gtp.c](https://gitlab.com/wireshark/wireshark/-/blob/master/epan/dissectors/packet-gtp.c)
- [Wireshark packet-gtpv2.c](https://gitlab.com/wireshark/wireshark/-/blob/master/epan/dissectors/packet-gtpv2.c)
