"""Tests for GTPv1-C message encode/decode.

The reference packet is the sample Create PDP Context Request from sample-hex.txt.
"""

import pytest
import socket
from tests.conftest import SAMPLE_V1_CREATE_PDP_CTX_HEX
from gtpc.utils.hexdump import from_hex
from gtpc.v1.messages import (
    decode_message,
    CreatePDPContextRequest, CreatePDPContextResponse,
    UpdatePDPContextRequest, UpdatePDPContextResponse,
    DeletePDPContextRequest, DeletePDPContextResponse,
    EchoRequest, EchoResponse,
    ErrorIndication,
    SGSNContextRequest, SGSNContextResponse,
    ForwardRelocationRequest, ForwardRelocationResponse,
    MBMSSessionStartRequest, MBMSSessionStartResponse,
    DataRecordTransferRequest, DataRecordTransferResponse,
)
from gtpc.v1 import constants as C
from gtpc.v1.ie.tv import IMSIE, NSAPIIE, RecoveryIE, TEIDDataIIE, TEIDCPlaneIE
from gtpc.v1.ie.tlv import APNIE, GSNAddressIE


# ---------------------------------------------------------------------------
# Reference packet (sample-hex.txt)
# ---------------------------------------------------------------------------

class TestSamplePacketDecode:
    def setup_method(self):
        raw = from_hex(SAMPLE_V1_CREATE_PDP_CTX_HEX)
        self.msg = decode_message(raw)
        self.raw = raw

    def test_message_type(self):
        assert isinstance(self.msg, CreatePDPContextRequest)

    def test_teid(self):
        assert self.msg.header.teid == 0

    def test_seq_num(self):
        assert self.msg.header.seq_num == 254

    def test_imsi(self):
        assert self.msg.imsi == "272030100000000"

    def test_nsapi(self):
        assert self.msg.nsapi == 5

    def test_apn(self):
        assert self.msg.apn == "mms.mymeteor.ie"

    def test_teid_data(self):
        assert self.msg.teid_data == 0x372F0000

    def test_teid_control(self):
        assert self.msg.teid_control == 0x372F0000

    def test_gsn_addresses(self):
        addrs = self.msg.get_ies(C.IE_GSN_ADDRESS)
        assert len(addrs) == 2

    def test_num_ies(self):
        assert len(self.msg.ies) == 16


# ---------------------------------------------------------------------------
# Round-trip: encode then decode → same bytes
# ---------------------------------------------------------------------------

def test_echo_request_roundtrip():
    msg = EchoRequest(teid=0, seq_num=1)
    msg.set_recovery(42)
    raw = msg.encode()
    decoded = decode_message(raw)
    assert isinstance(decoded, EchoRequest)
    assert decoded.header.seq_num == 1
    rc = decoded.get_ie(C.IE_RECOVERY)
    assert rc.restart_counter == 42


def test_create_pdp_ctx_req_build_and_decode():
    msg = CreatePDPContextRequest(teid=0, seq_num=100)
    msg.set_imsi("272030100000000")
    msg.set_nsapi(5)
    msg.set_teid_data(0xAABBCCDD)
    msg.set_teid_control(0x11223344)
    msg.set_apn("internet")
    msg.set_selection_mode(0)
    msg.set_sgsn_address_signalling(socket.inet_pton(socket.AF_INET, "1.2.3.4"))
    raw = msg.encode()
    d = decode_message(raw)
    assert isinstance(d, CreatePDPContextRequest)
    assert d.imsi == "272030100000000"
    assert d.nsapi == 5
    assert d.teid_data == 0xAABBCCDD
    assert d.apn == "internet"


def test_create_pdp_ctx_res_cause():
    msg = CreatePDPContextResponse(teid=0x12345678, seq_num=10)
    msg.set_cause(C.CAUSE_REQUEST_ACCEPTED)
    msg.set_teid_data(0xABCD)
    msg.set_teid_control(0xEF01)
    raw = msg.encode()
    d = decode_message(raw)
    assert isinstance(d, CreatePDPContextResponse)
    assert d.cause == C.CAUSE_REQUEST_ACCEPTED


def test_delete_pdp_ctx_req():
    msg = DeletePDPContextRequest(teid=0x1234, seq_num=5)
    msg.set_nsapi(5)
    msg.set_teardown_ind(True)
    raw = msg.encode()
    d = decode_message(raw)
    assert isinstance(d, DeletePDPContextRequest)


def test_update_pdp_ctx_req():
    msg = UpdatePDPContextRequest(teid=0, seq_num=20)
    msg.set_teid_data(0x1111)
    msg.set_teid_control(0x2222)
    msg.set_nsapi(5)
    msg.set_sgsn_address_signalling(socket.inet_pton(socket.AF_INET, "10.0.0.1"))
    raw = msg.encode()
    d = decode_message(raw)
    assert isinstance(d, UpdatePDPContextRequest)


def test_error_indication():
    msg = ErrorIndication(teid=0, seq_num=1)
    msg.set_teid_data(0xCAFE)
    msg.set_gsn_address(socket.inet_pton(socket.AF_INET, "5.6.7.8"))
    raw = msg.encode()
    d = decode_message(raw)
    assert isinstance(d, ErrorIndication)


def test_sgsn_context_request():
    msg = SGSNContextRequest(teid=0, seq_num=77)
    msg.set_imsi("123456789012345")
    msg.set_nsapi(5)
    raw = msg.encode()
    d = decode_message(raw)
    assert isinstance(d, SGSNContextRequest)


def test_mbms_session_start_request():
    msg = MBMSSessionStartRequest(teid=0, seq_num=1)
    msg.set_recovery(0)
    raw = msg.encode()
    d = decode_message(raw)
    assert isinstance(d, MBMSSessionStartRequest)


# One test per remaining message type (smoke: encode + decode)
@pytest.mark.parametrize("klass,kwargs", [
    (EchoResponse,          dict(teid=0, seq_num=1)),
    (CreatePDPContextResponse, dict(teid=0, seq_num=1)),
    (UpdatePDPContextResponse, dict(teid=0, seq_num=1)),
    (DeletePDPContextResponse, dict(teid=0, seq_num=1)),
    (SGSNContextResponse,   dict(teid=0, seq_num=1)),
    (SGSNContextRequest,    dict(teid=0, seq_num=1)),
    (ForwardRelocationRequest, dict(teid=0, seq_num=1)),
    (ForwardRelocationResponse, dict(teid=0, seq_num=1)),
    (DataRecordTransferRequest, dict(teid=0, seq_num=1)),
    (DataRecordTransferResponse, dict(teid=0, seq_num=1)),
])
def test_message_smoke(klass, kwargs):
    msg = klass(**kwargs)
    raw = msg.encode()
    d = decode_message(raw)
    assert isinstance(d, klass)
