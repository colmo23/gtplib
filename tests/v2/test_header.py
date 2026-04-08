"""Tests for GTPv2-C header encode/decode."""

import pytest
from gtpc.v2.header import GTPv2Header
from gtpc.v2 import constants as C


def test_header_no_teid():
    hdr = GTPv2Header(msg_type=C.MSG_ECHO_REQ, teid=None, seq_num=0)
    raw = hdr.encode(0)
    assert len(raw) == 8
    assert (raw[0] >> 5) & 0x7 == 2       # version = 2
    assert not (raw[0] & 0x08)            # T flag = 0


def test_header_with_teid():
    hdr = GTPv2Header(msg_type=C.MSG_CREATE_SESSION_REQ, teid=0xDEADBEEF, seq_num=42)
    raw = hdr.encode(0)
    assert len(raw) == 12
    assert raw[0] & 0x08                  # T flag = 1
    import struct
    assert struct.unpack_from("!I", raw, 4)[0] == 0xDEADBEEF


def test_header_roundtrip_with_teid():
    hdr = GTPv2Header(msg_type=C.MSG_CREATE_SESSION_REQ, teid=0x12345678, seq_num=999)
    raw = hdr.encode(50)
    decoded, offset = GTPv2Header.decode(raw)
    assert decoded.msg_type == C.MSG_CREATE_SESSION_REQ
    assert decoded.teid == 0x12345678
    assert decoded.seq_num == 999
    assert offset == 12


def test_header_roundtrip_no_teid():
    hdr = GTPv2Header(msg_type=C.MSG_ECHO_REQ, teid=None, seq_num=1)
    raw = hdr.encode(0)
    decoded, offset = GTPv2Header.decode(raw)
    assert decoded.teid is None
    assert decoded.seq_num == 1
    assert offset == 8


def test_header_wrong_version_raises():
    from gtpc.v1.header import GTPv1Header
    v1hdr = GTPv1Header(msg_type=1, teid=0, seq_num=1)
    raw = v1hdr.encode(0)
    with pytest.raises(ValueError, match="Not a GTPv2"):
        GTPv2Header.decode(raw)
