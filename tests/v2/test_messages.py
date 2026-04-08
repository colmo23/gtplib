"""Tests for GTPv2-C message encode/decode."""

import pytest
from gtpc.v2.messages import (
    decode_message,
    EchoRequest, EchoResponse,
    CreateSessionRequest, CreateSessionResponse,
    ModifyBearerRequest, ModifyBearerResponse,
    DeleteSessionRequest, DeleteSessionResponse,
    ChangeNotificationRequest, ChangeNotificationResponse,
    CreateBearerRequest, CreateBearerResponse,
    UpdateBearerRequest, UpdateBearerResponse,
    DeleteBearerRequest, DeleteBearerResponse,
    ModifyBearerCommand, ModifyBearerFailureIndication,
    DeleteBearerCommand, DeleteBearerFailureIndication,
    BearerResourceCommand, BearerResourceFailureIndication,
    ForwardRelocationRequest, ForwardRelocationResponse,
    ContextRequest, ContextResponse, ContextAcknowledge,
    ReleaseAccessBearersRequest, ReleaseAccessBearersResponse,
    DownlinkDataNotification, DownlinkDataNotificationAcknowledge,
    DetachNotification, DetachAcknowledge,
    SuspendNotification, SuspendAcknowledge,
    ResumeNotification, ResumeAcknowledge,
    PGWRestartNotification,
    MBMSSessionStartRequest, MBMSSessionStartResponse,
    MBMSSessionStopRequest, MBMSSessionStopResponse,
    DeletePDNConnectionSetRequest, DeletePDNConnectionSetResponse,
    UpdatePDNConnectionSetRequest, UpdatePDNConnectionSetResponse,
    ModifyAccessBearersRequest, ModifyAccessBearersResponse,
)
from gtpc.v2.ie.typed import (
    IMSIIE, CauseIE, RecoveryIE, APNIE, AMBRIE, EBIIE,
    MSISDNIE, PAAIE, BearerQoSIE, RATTypeIE, ServingNetworkIE,
    ULIIE, FTEIDIE, BearerContextIE, PDNTypeIE,
)
from gtpc.v2 import constants as C


def smoke(klass, teid=None, seq_num=1, setup=None):
    """Build, encode, decode, check type."""
    msg = klass(teid=teid, seq_num=seq_num)
    if setup:
        setup(msg)
    raw = msg.encode()
    d = decode_message(raw)
    assert isinstance(d, klass), f"Expected {klass.__name__}, got {type(d).__name__}"
    return d


# ---------------------------------------------------------------------------
# Echo
# ---------------------------------------------------------------------------

def test_echo_request():
    d = smoke(EchoRequest)
    assert isinstance(d, EchoRequest)


def test_echo_response():
    def s(m): m.set_recovery(99)
    d = smoke(EchoResponse, setup=s)
    assert d.recovery == 99


# ---------------------------------------------------------------------------
# Create Session
# ---------------------------------------------------------------------------

def _make_bearer_ctx(ebi=5):
    ctx = BearerContextIE()
    ctx.add_ie(EBIIE(ebi))
    ctx.add_ie(FTEIDIE(C.FTEID_S1U_ENODEB, teid=0xAABB, ipv4="1.2.3.4"))
    ctx.add_ie(BearerQoSIE(qci=9, pl=9))
    return ctx


def test_create_session_request_full():
    msg = CreateSessionRequest(teid=None, seq_num=1)
    msg.set_imsi("272030100000000")
    msg.set_msisdn("353800000000")
    msg.set_rat_type(C.RAT_EUTRAN)
    msg.set_serving_network("272", "03")
    msg.set_apn("internet")
    msg.set_pdn_type(C.PDN_TYPE_IPv4)
    msg.set_paa(PAAIE(C.PDN_TYPE_IPv4, "0.0.0.0"))
    msg.set_ambr(100000, 200000)
    msg.set_selection_mode(0)
    msg.set_sender_fteid(FTEIDIE(C.FTEID_S11_MME, teid=0x1234, ipv4="10.0.0.1"))
    msg.add_bearer_context(_make_bearer_ctx())
    raw = msg.encode()
    d = decode_message(raw)
    assert isinstance(d, CreateSessionRequest)
    assert d.imsi == "272030100000000"
    assert d.apn == "internet"
    assert d.pdn_type == C.PDN_TYPE_IPv4
    ctxs = d.bearer_contexts
    assert len(ctxs) == 1
    assert ctxs[0].get_ie(C.IE_EBI).ebi == 5


def test_create_session_response():
    msg = CreateSessionResponse(teid=0x1234, seq_num=1)
    msg.set_cause(C.CAUSE_REQUEST_ACCEPTED)
    msg.set_sender_fteid(FTEIDIE(C.FTEID_S11S4_SGW, teid=0xABCD, ipv4="5.6.7.8"))
    msg.set_paa(PAAIE(C.PDN_TYPE_IPv4, "192.168.1.100"))
    msg.add_bearer_context(_make_bearer_ctx())
    raw = msg.encode()
    d = decode_message(raw)
    assert isinstance(d, CreateSessionResponse)
    assert d.cause == C.CAUSE_REQUEST_ACCEPTED


# ---------------------------------------------------------------------------
# Modify Bearer
# ---------------------------------------------------------------------------

def test_modify_bearer_request():
    msg = ModifyBearerRequest(teid=0x5678, seq_num=2)
    ctx = BearerContextIE()
    ctx.add_ie(EBIIE(5))
    ctx.add_ie(FTEIDIE(C.FTEID_S1U_ENODEB, teid=0xBBCC, ipv4="3.3.3.3"))
    msg.add_bearer_context(ctx)
    raw = msg.encode()
    d = decode_message(raw)
    assert isinstance(d, ModifyBearerRequest)


def test_modify_bearer_response():
    def s(m): m.set_cause(C.CAUSE_REQUEST_ACCEPTED)
    d = smoke(ModifyBearerResponse, teid=0x1234, setup=s)
    assert d.cause == C.CAUSE_REQUEST_ACCEPTED


# ---------------------------------------------------------------------------
# Delete Session
# ---------------------------------------------------------------------------

def test_delete_session_request():
    msg = DeleteSessionRequest(teid=0xABCD, seq_num=3)
    msg.set_ebi(5)
    raw = msg.encode()
    d = decode_message(raw)
    assert isinstance(d, DeleteSessionRequest)


def test_delete_session_response():
    def s(m): m.set_cause(C.CAUSE_REQUEST_ACCEPTED)
    d = smoke(DeleteSessionResponse, teid=0xABCD, setup=s)
    assert d.cause == C.CAUSE_REQUEST_ACCEPTED


# ---------------------------------------------------------------------------
# Create / Update / Delete Bearer
# ---------------------------------------------------------------------------

def test_create_bearer_request():
    msg = CreateBearerRequest(teid=0x1234, seq_num=4)
    msg.set_linked_ebi(5)
    msg.add_bearer_context(_make_bearer_ctx(ebi=6))
    raw = msg.encode()
    d = decode_message(raw)
    assert isinstance(d, CreateBearerRequest)


def test_delete_bearer_request():
    msg = DeleteBearerRequest(teid=0x1234, seq_num=5)
    msg.add_ebi(5)
    raw = msg.encode()
    d = decode_message(raw)
    assert isinstance(d, DeleteBearerRequest)


# ---------------------------------------------------------------------------
# Mobility
# ---------------------------------------------------------------------------

def test_context_request():
    msg = ContextRequest(teid=0, seq_num=10)
    msg.set_imsi("123456789012345")
    msg.set_rat_type(C.RAT_EUTRAN)
    raw = msg.encode()
    d = decode_message(raw)
    assert isinstance(d, ContextRequest)


def test_forward_relocation_request():
    msg = ForwardRelocationRequest(teid=0, seq_num=11)
    msg.set_imsi("987654321098765")
    raw = msg.encode()
    d = decode_message(raw)
    assert isinstance(d, ForwardRelocationRequest)


# ---------------------------------------------------------------------------
# Access bearers / downlink
# ---------------------------------------------------------------------------

def test_release_access_bearers():
    msg = ReleaseAccessBearersRequest(teid=0x1234, seq_num=20)
    msg.add_ebi(5)
    raw = msg.encode()
    d = decode_message(raw)
    assert isinstance(d, ReleaseAccessBearersRequest)


def test_downlink_data_notification():
    msg = DownlinkDataNotification(teid=0x1234, seq_num=21)
    msg.set_ebi(5)
    raw = msg.encode()
    d = decode_message(raw)
    assert isinstance(d, DownlinkDataNotification)


# ---------------------------------------------------------------------------
# Notifications
# ---------------------------------------------------------------------------

def test_detach_notification():
    d = smoke(DetachNotification, teid=0x1234)
    assert isinstance(d, DetachNotification)


def test_suspend_resume():
    d = smoke(SuspendNotification, teid=0x1234)
    assert isinstance(d, SuspendNotification)
    d = smoke(ResumeNotification, teid=0x1234)
    assert isinstance(d, ResumeNotification)


def test_pgw_restart_notification():
    msg = PGWRestartNotification(teid=None, seq_num=1)
    msg.set_pgw_s5s8_ip("1.2.3.4")
    msg.set_sgw_s11s4_ip("5.6.7.8")
    raw = msg.encode()
    d = decode_message(raw)
    assert isinstance(d, PGWRestartNotification)


# ---------------------------------------------------------------------------
# MBMS
# ---------------------------------------------------------------------------

def test_mbms_session_start():
    msg = MBMSSessionStartRequest(teid=None, seq_num=1)
    msg.set_tmgi(b"\x00\x01\x02\x03\x04\x05")
    raw = msg.encode()
    d = decode_message(raw)
    assert isinstance(d, MBMSSessionStartRequest)


def test_mbms_session_stop():
    msg = MBMSSessionStopRequest(teid=None, seq_num=1)
    msg.set_tmgi(b"\x00\x01\x02\x03\x04\x05")
    raw = msg.encode()
    d = decode_message(raw)
    assert isinstance(d, MBMSSessionStopRequest)


# ---------------------------------------------------------------------------
# Smoke tests for remaining message types
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("klass", [
    EchoResponse,
    ModifyBearerResponse,
    DeleteSessionResponse,
    CreateBearerResponse,
    UpdateBearerRequest,
    UpdateBearerResponse,
    DeleteBearerResponse,
    ModifyBearerCommand,
    ModifyBearerFailureIndication,
    DeleteBearerCommand,
    DeleteBearerFailureIndication,
    BearerResourceFailureIndication,
    ContextResponse,
    ContextAcknowledge,
    ForwardRelocationResponse,
    DetachAcknowledge,
    SuspendAcknowledge,
    ResumeAcknowledge,
    DownlinkDataNotificationAcknowledge,
    ReleaseAccessBearersResponse,
    DeletePDNConnectionSetRequest,
    DeletePDNConnectionSetResponse,
    UpdatePDNConnectionSetRequest,
    UpdatePDNConnectionSetResponse,
    ModifyAccessBearersRequest,
    ModifyAccessBearersResponse,
    MBMSSessionStartResponse,
    MBMSSessionStopResponse,
    ChangeNotificationRequest,
    ChangeNotificationResponse,
])
def test_message_smoke(klass):
    msg = klass(teid=None, seq_num=1)
    raw = msg.encode()
    d = decode_message(raw)
    assert isinstance(d, klass), f"Expected {klass.__name__}, got {type(d).__name__}"
