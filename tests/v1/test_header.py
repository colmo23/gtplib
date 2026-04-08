"""Tests for GTPv1-C header encode/decode."""

import pytest
from gtpc.v1.header import GTPv1Header
from gtpc.v1 import constants as C


def test_header_encode_no_seq():
    hdr = GTPv1Header(msg_type=C.MSG_ECHO_REQ, teid=0)
    raw = hdr.encode(0)
    assert len(raw) == 8
    assert raw[0] == 0x20 | 0x10  # version=1, PT=1, no flags
    assert raw[1] == C.MSG_ECHO_REQ
    assert raw[2:4] == b"\x00\x00"
    assert raw[4:8] == b"\x00\x00\x00\x00"


def test_header_encode_with_seq():
    hdr = GTPv1Header(msg_type=C.MSG_ECHO_REQ, teid=0xABCD1234, seq_num=255)
    raw = hdr.encode(0)
    assert len(raw) == 12
    assert raw[0] & 0x02  # S flag
    assert raw[8:10] == b"\x00\xff"  # seq_num = 255
    assert raw[10] == 0   # npdu
    assert raw[11] == 0   # next ext hdr


def test_header_roundtrip():
    hdr = GTPv1Header(
        msg_type=C.MSG_CREATE_PDP_CTX_REQ,
        teid=0x372F0000,
        seq_num=254,
    )
    raw = hdr.encode(100)
    decoded, offset = GTPv1Header.decode(raw)
    assert decoded.msg_type == C.MSG_CREATE_PDP_CTX_REQ
    assert decoded.teid == 0x372F0000
    assert decoded.seq_num == 254
    assert offset == 12


def test_header_wrong_version_raises():
    # Craft a GTPv2 packet and try to decode as v1
    from gtpc.v2.header import GTPv2Header
    v2hdr = GTPv2Header(msg_type=1, teid=None, seq_num=1)
    raw = v2hdr.encode(0)
    with pytest.raises(ValueError, match="Not a GTPv1"):
        GTPv1Header.decode(raw)
