#!/usr/bin/env python3
"""Annotated examples of decoding GTPv1-C and GTPv2-C packets.

Run this script to see the decoded output for each example:
    python3 examples/decode_examples.py
"""

import socket
from gtpc.utils.hexdump import from_hex, hexdump

# ===========================================================================
# GTPv1-C — Create PDP Context Request (real-world capture)
# ===========================================================================

print("=" * 60)
print("GTPv1-C — Create PDP Context Request (real-world capture)")
print("=" * 60)

RAW_V1_CREATE_PDP = from_hex(
    "321000970000000000fe00000272020301000000f00372f230fffeff0e5d0ffc10372f000011"
    "372f00001405800002f121830010036d6d73086d796d6574656f7202696584002280c0230b01"
    "00000b026d790377617080211001000010810600000000830600000000850004d481410d8500"
    "04d48141178600079153830000000087000c0223621f9396585874fbffff970001029a000853"
    "89011058985321"
)

from gtpc.v1.messages import decode_message as v1_decode
from gtpc.v1 import constants as V1

msg = v1_decode(RAW_V1_CREATE_PDP)
print(f"Type   : {type(msg).__name__}")
print(f"TEID   : 0x{msg.header.teid:08x}")
print(f"Seq    : {msg.header.seq_num}")
print(f"IMSI   : {msg.imsi}")
print(f"APN    : {msg.apn}")
print(f"NSAPI  : {msg.nsapi}")
print(f"TEID Data I  : 0x{msg.teid_data:08x}")
print(f"TEID C-Plane : 0x{msg.teid_control:08x}")
print(f"IEs ({len(msg.ies)} total):")
for ie in msg.ies:
    print(f"  {ie!r}")

print()

# ===========================================================================
# GTPv1-C — Echo Request / Response
# ===========================================================================

print("=" * 60)
print("GTPv1-C — Echo Request / Response")
print("=" * 60)

from gtpc.v1.messages import EchoRequest, EchoResponse

# Decode a raw Echo Request
raw_echo_req = from_hex("3201000600000000000100000e2a")
echo_req = v1_decode(raw_echo_req)
print(f"Echo Request  : seq={echo_req.header.seq_num}")
recovery_ie = echo_req.get_ie(V1.IE_RECOVERY)
if recovery_ie:
    print(f"  Recovery    : restart_counter={recovery_ie.restart_counter}")

# Build an Echo Response to it
echo_res = EchoResponse(teid=0, seq_num=echo_req.header.seq_num)
echo_res.set_recovery(0)
print(f"Echo Response : {echo_res.encode().hex()}")
print()

# ===========================================================================
# GTPv1-C — Delete PDP Context Request
# ===========================================================================

print("=" * 60)
print("GTPv1-C — Delete PDP Context Request")
print("=" * 60)

raw_del = from_hex("32140008aabbccdd012c000013ff14f5")
del_msg = v1_decode(raw_del)
print(f"Type       : {type(del_msg).__name__}")
print(f"TEID       : 0x{del_msg.header.teid:08x}")
teardown_ie = del_msg.get_ie(V1.IE_TEARDOWN_IND)
nsapi_ie    = del_msg.get_ie(V1.IE_NSAPI)
print(f"Teardown   : {teardown_ie.teardown if teardown_ie else 'n/a'}")
print(f"NSAPI      : {nsapi_ie.nsapi if nsapi_ie else 'n/a'}")
print()

# ===========================================================================
# GTPv1-C — GSN Address IEs (two addresses in one message)
# ===========================================================================

print("=" * 60)
print("GTPv1-C — Multiple GSN Address IEs")
print("=" * 60)

addrs = v1_decode(RAW_V1_CREATE_PDP).get_ies(V1.IE_GSN_ADDRESS)
for i, a in enumerate(addrs):
    ip = socket.inet_ntoa(a.address)
    print(f"  GSN Address[{i}] : {ip}")
print()

# ===========================================================================
# GTPv2-C — Create Session Request (LTE attach)
# ===========================================================================

print("=" * 60)
print("GTPv2-C — Create Session Request (LTE attach)")
print("=" * 60)

from gtpc.v2.messages import decode_message as v2_decode
from gtpc.v2 import constants as V2
from gtpc.v2.ie.typed import ULIIE, FTEIDIE, BearerContextIE, BearerQoSIE, EBIIE, PAAIE

# Build one so we have a known packet to decode
from gtpc.v2.messages import CreateSessionRequest

csr = CreateSessionRequest(teid=None, seq_num=42)
csr.set_imsi("272030100000000")
csr.set_msisdn("353871234567")
csr.set_rat_type(V2.RAT_EUTRAN)
csr.set_serving_network(mcc="272", mnc="03")
csr.set_uli(ULIIE.with_tai_and_ecgi("272", "03", tac=0x1234, eci=0xABCDE))
csr.set_apn("internet.operator.com")
csr.set_pdn_type(V2.PDN_TYPE_IPv4)
csr.set_paa(PAAIE(V2.PDN_TYPE_IPv4, "0.0.0.0"))
csr.set_ambr(uplink_kbps=100_000, downlink_kbps=200_000)
csr.set_sender_fteid(FTEIDIE(V2.FTEID_S11_MME, teid=0x11111111, ipv4="10.0.0.1"))
csr.set_pgw_fteid(FTEIDIE(V2.FTEID_S5S8C_PGW, teid=0x22222222, ipv4="10.0.1.1"))

bearer = BearerContextIE()
bearer.add_ie(EBIIE(ebi=5))
bearer.add_ie(FTEIDIE(V2.FTEID_S1U_ENODEB, teid=0xAABBCCDD, ipv4="192.168.10.50"))
bearer.add_ie(BearerQoSIE(
    qci=9, pl=9, pci=False, pvi=False,
    mbr_ul=128_000, mbr_dl=128_000, gbr_ul=0, gbr_dl=0,
))
csr.add_bearer_context(bearer)

raw_csr = csr.encode()

# Now decode it
msg = v2_decode(raw_csr)
print(f"Type          : {type(msg).__name__}")
print(f"TEID          : {msg.header.teid}")        # None → T flag not set
print(f"Seq           : {msg.header.seq_num}")
print(f"IMSI          : {msg.imsi}")
print(f"APN           : {msg.apn}")

rat_ie = msg.get_ie(V2.IE_RAT_TYPE)
print(f"RAT type      : {rat_ie.rat if rat_ie else 'n/a'}")

ambr_ie = msg.get_ie(V2.IE_AMBR)
if ambr_ie:
    print(f"AMBR UL/DL    : {ambr_ie.uplink_kbps} / {ambr_ie.downlink_kbps} kbps")

# F-TEID: sender (instance 0) and PGW (instance 1)
sender_fteid = msg.get_ie(V2.IE_F_TEID, instance=0)
pgw_fteid    = msg.get_ie(V2.IE_F_TEID, instance=1)
if sender_fteid:
    print(f"Sender F-TEID : teid=0x{sender_fteid.teid:08x}  ip={sender_fteid.ipv4}")
if pgw_fteid:
    print(f"PGW F-TEID    : teid=0x{pgw_fteid.teid:08x}  ip={pgw_fteid.ipv4}")

# Bearer contexts (grouped IEs)
contexts = msg.bearer_contexts
for i, bc in enumerate(contexts):
    ebi_ie  = bc.get_ie(V2.IE_EBI)
    qos_ie  = bc.get_ie(V2.IE_BEARER_QOS)
    ft_ie   = bc.get_ie(V2.IE_F_TEID)
    print(f"Bearer[{i}]:")
    print(f"  EBI          : {ebi_ie.ebi if ebi_ie else 'n/a'}")
    if ft_ie:
        print(f"  F-TEID       : teid=0x{ft_ie.teid:08x}  ip={ft_ie.ipv4}")
    if qos_ie:
        print(f"  QCI          : {qos_ie.qci}")
        print(f"  MBR UL/DL    : {qos_ie.mbr_ul} / {qos_ie.mbr_dl} bps")

print()

# ===========================================================================
# GTPv2-C — Hex dump of a packet
# ===========================================================================

print("=" * 60)
print("GTPv2-C — Hex dump")
print("=" * 60)

from gtpc.v2.messages import EchoRequest as V2EchoRequest

echo = V2EchoRequest(teid=None, seq_num=1)
echo.set_recovery(0)
raw = echo.encode()
print(hexdump(raw))

# ===========================================================================
# GTPv2-C — Decoding a Create Session Response
# ===========================================================================

print("=" * 60)
print("GTPv2-C — Create Session Response")
print("=" * 60)

from gtpc.v2.messages import CreateSessionResponse

rsp = CreateSessionResponse(teid=0x11111111, seq_num=42)
rsp.set_cause(V2.CAUSE_REQUEST_ACCEPTED)
rsp.set_sender_fteid(FTEIDIE(V2.FTEID_S11S4_SGW, teid=0x44444444, ipv4="10.0.0.2"))
rsp.set_paa(PAAIE(V2.PDN_TYPE_IPv4, "100.64.0.1"))
rsp.set_ambr(100_000, 200_000)

brsp = BearerContextIE()
brsp.add_ie(EBIIE(5))
brsp.add_ie(FTEIDIE(V2.FTEID_S1U_SGW, teid=0x33333333, ipv4="10.0.2.1"))
rsp.add_bearer_context(brsp)

decoded_rsp = v2_decode(rsp.encode())
print(f"Type          : {type(decoded_rsp).__name__}")
cause_ie = decoded_rsp.get_ie(V2.IE_CAUSE)
print(f"Cause         : {cause_ie.cause if cause_ie else 'n/a'}")
paa_ie = decoded_rsp.get_ie(V2.IE_PAA)
if paa_ie:
    print(f"PAA           : {paa_ie.address}")

print()
print("Done.")
