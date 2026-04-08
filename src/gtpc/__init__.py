"""GTP Control Plane packet builder and parser.

Supports GTPv1-C (3GPP TS 29.060) and GTPv2-C (3GPP TS 29.274).
Modelled after Wireshark's EPAN dissectors (packet-gtp.c, packet-gtpv2.c).
"""
from gtpc.v1.messages import decode_message as decode_v1
from gtpc.v2.messages import decode_message as decode_v2

__all__ = ["decode_v1", "decode_v2"]
