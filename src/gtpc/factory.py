"""Message factory — one function per GTP-C message type with sensible defaults.

Each function returns a fully-constructed, encode-ready message object.
All parameters are optional; defaults model a realistic but minimal packet.
"""

import socket
from typing import Optional

# ---------------------------------------------------------------------------
# GTPv1-C
# ---------------------------------------------------------------------------
from gtpc.v1.messages import (
    EchoRequest, EchoResponse,
    CreatePDPContextRequest, CreatePDPContextResponse,
    UpdatePDPContextRequest, UpdatePDPContextResponse,
    DeletePDPContextRequest, DeletePDPContextResponse,
    ErrorIndication,
    PDUNotificationRequest, PDUNotificationResponse,
    PDUNotificationRejectRequest,
    SGSNContextRequest, SGSNContextResponse, SGSNContextAcknowledge,
    ForwardRelocationRequest, ForwardRelocationResponse,
    RelocationCancelRequest, RelocationCancelResponse,
    DataRecordTransferRequest, DataRecordTransferResponse,
    MBMSSessionStartRequest, MBMSSessionStartResponse,
)
from gtpc.v1.ie.tlv import EndUserAddressIE, QoSProfileIE
from gtpc.v1.messages.base import GTPv1Message
from gtpc.v1 import constants as V1

# ---------------------------------------------------------------------------
# GTPv2-C
# ---------------------------------------------------------------------------
from gtpc.v2.messages import (
    EchoRequest as V2EchoRequest,
    EchoResponse as V2EchoResponse,
    CreateSessionRequest, CreateSessionResponse,
    ModifyBearerRequest, ModifyBearerResponse,
    DeleteSessionRequest, DeleteSessionResponse,
    CreateBearerRequest, CreateBearerResponse,
    UpdateBearerRequest, UpdateBearerResponse,
    DeleteBearerRequest, DeleteBearerResponse,
    ModifyBearerCommand, ModifyBearerFailureIndication,
    DeleteBearerCommand, DeleteBearerFailureIndication,
    BearerResourceCommand,
    ReleaseAccessBearersRequest, ReleaseAccessBearersResponse,
    DownlinkDataNotification, DownlinkDataNotificationAcknowledge,
    ContextRequest, ContextResponse, ContextAcknowledge,
    ForwardRelocationRequest as V2ForwardRelocationRequest,
    ForwardRelocationResponse as V2ForwardRelocationResponse,
    ForwardRelocationCompleteNotification, ForwardRelocationCompleteAcknowledge,
    DetachNotification, DetachAcknowledge,
    SuspendNotification, SuspendAcknowledge,
    ResumeNotification, ResumeAcknowledge,
    PGWRestartNotification, PGWRestartNotificationAcknowledge,
    DeletePDNConnectionSetRequest,
    ModifyAccessBearersRequest, ModifyAccessBearersResponse,
    MBMSSessionStartRequest as V2MBMSSessionStartRequest,
    MBMSSessionStopRequest as V2MBMSSessionStopRequest,
    StopPagingIndication,
)
from gtpc.v2.ie.typed import (
    CauseIE, RecoveryIE, IMSIIE, APNIE, AMBRIE, EBIIE,
    MSISDNIE, RATTypeIE, ServingNetworkIE, ULIIE, FTEIDIE,
    BearerContextIE, BearerQoSIE, PAAIE, PDNTypeIE,
    UETimeZoneIE, APNRestrictionIE, SelectionModeIE,
    FQCSIDIe, ARPIE, MEIIE, ChargingIDIE, NodeTypeIE,
)
from gtpc.v2.messages.base import GTPv2Message
from gtpc.v2 import constants as V2


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _ip4(addr):
    return socket.inet_pton(socket.AF_INET, addr)


def _qos_bytes():
    return bytes([0x0B, 0x92, 0x1F])


def _bearer_ctx(ebi, interface_type, teid, ipv4,
                qci=9, pl=9,
                mbr_ul=128000, mbr_dl=128000,
                gbr_ul=0, gbr_dl=0,
                instance=0):
    ctx = BearerContextIE(instance=instance)
    ctx.add_ie(EBIIE(ebi))
    ctx.add_ie(FTEIDIE(interface_type, teid=teid, ipv4=ipv4))
    ctx.add_ie(BearerQoSIE(
        qci=qci, pl=pl, pci=False, pvi=False,
        mbr_ul=mbr_ul, mbr_dl=mbr_dl,
        gbr_ul=gbr_ul, gbr_dl=gbr_dl,
    ))
    return ctx


# ===========================================================================
# GTPv1-C factory functions
# ===========================================================================

def v1_echo_request(teid=0, seq_num=1, recovery=0):
    # type: (int, int, int) -> EchoRequest
    msg = EchoRequest(teid=teid, seq_num=seq_num)
    msg.set_recovery(recovery)
    return msg


def v1_echo_response(teid=0, seq_num=1, recovery=0):
    # type: (int, int, int) -> EchoResponse
    msg = EchoResponse(teid=teid, seq_num=seq_num)
    msg.set_recovery(recovery)
    return msg


def v1_create_pdp_context_request(
        teid=0, seq_num=1,
        imsi="272030100000000",
        mcc="272", mnc="03", lac=1234, rac=5,
        teid_data=0x11111111, teid_control=0x11111112,
        nsapi=5,
        apn="internet",
        sgsn_addr_sig="10.0.0.1", sgsn_addr_data="10.0.0.2",
        msisdn="353871234567",
        rat_type=None,
):
    # type: (int, int, str, str, str, int, int, int, int, int, str, str, str, str, Optional[int]) -> CreatePDPContextRequest
    if rat_type is None:
        rat_type = V1.RAT_UTRAN
    msg = CreatePDPContextRequest(teid=teid, seq_num=seq_num)
    msg.set_imsi(imsi)
    msg.set_rai(mcc, mnc, lac=lac, rac=rac)
    msg.set_recovery(0)
    msg.set_selection_mode(V1.SEL_MODE_MS_OR_NET_APN_SUBSCR_VERIFIED)
    msg.set_teid_data(teid_data)
    msg.set_teid_control(teid_control)
    msg.set_nsapi(nsapi)
    msg.set_charging_chars(0x0800)
    msg.set_end_user_address(
        pdp_type_org=EndUserAddressIE.PTO_IETF,
        pdp_type_num=EndUserAddressIE.PDN_IPv4,
    )
    msg.set_apn(apn)
    msg.set_sgsn_address_signalling(_ip4(sgsn_addr_sig))
    msg.set_sgsn_address_user_traffic(_ip4(sgsn_addr_data))
    msg.set_msisdn(msisdn)
    msg.set_qos_profile(QoSProfileIE(_qos_bytes()).encode()[3:])
    msg.set_rat_type(rat_type)
    return msg


def v1_create_pdp_context_response(
        teid=0, seq_num=1,
        cause=None,
        teid_data=0xAAAAAAAA, teid_control=0xBBBBBBBB,
        ggsn_addr_sig="192.168.1.1", ggsn_addr_data="192.168.1.2",
        allocated_ip="100.64.0.1",
):
    # type: (int, int, Optional[int], int, int, str, str, str) -> CreatePDPContextResponse
    if cause is None:
        cause = V1.CAUSE_REQUEST_ACCEPTED
    msg = CreatePDPContextResponse(teid=teid, seq_num=seq_num)
    msg.set_cause(cause)
    if cause == V1.CAUSE_REQUEST_ACCEPTED:
        msg.set_recovery(0)
        msg.set_teid_data(teid_data)
        msg.set_teid_control(teid_control)
        msg.set_charging_id(0x0000CAFE)
        msg.set_end_user_address(
            pdp_type_org=EndUserAddressIE.PTO_IETF,
            pdp_type_num=EndUserAddressIE.PDN_IPv4,
            address=_ip4(allocated_ip),
        )
        msg.set_ggsn_address_signalling(_ip4(ggsn_addr_sig))
        msg.set_ggsn_address_user_traffic(_ip4(ggsn_addr_data))
        msg.set_qos_profile(QoSProfileIE(_qos_bytes()).encode()[3:])
    return msg


def v1_update_pdp_context_request(
        teid=0xAAAAAAAA, seq_num=1,
        teid_data=0x22222222, teid_control=0x22222223,
        nsapi=5,
        sgsn_addr_sig="10.0.1.1", sgsn_addr_data="10.0.1.2",
        rat_type=None,
):
    # type: (int, int, int, int, int, str, str, Optional[int]) -> UpdatePDPContextRequest
    if rat_type is None:
        rat_type = V1.RAT_UTRAN
    msg = UpdatePDPContextRequest(teid=teid, seq_num=seq_num)
    msg.set_teid_data(teid_data)
    msg.set_teid_control(teid_control)
    msg.set_nsapi(nsapi)
    msg.set_sgsn_address_signalling(_ip4(sgsn_addr_sig))
    msg.set_sgsn_address_user_traffic(_ip4(sgsn_addr_data))
    msg.set_qos_profile(QoSProfileIE(_qos_bytes()).encode()[3:])
    msg.set_rat_type(rat_type)
    return msg


def v1_update_pdp_context_response(
        teid=0, seq_num=1,
        cause=None,
        teid_data=0xAAAAAAAA, teid_control=0xBBBBBBBB,
        ggsn_addr_sig="192.168.1.1", ggsn_addr_data="192.168.1.2",
):
    # type: (int, int, Optional[int], int, int, str, str) -> UpdatePDPContextResponse
    if cause is None:
        cause = V1.CAUSE_REQUEST_ACCEPTED
    msg = UpdatePDPContextResponse(teid=teid, seq_num=seq_num)
    msg.set_cause(cause)
    if cause == V1.CAUSE_REQUEST_ACCEPTED:
        msg.set_recovery(0)
        msg.set_teid_data(teid_data)
        msg.set_teid_control(teid_control)
        msg.set_charging_id(0x0000CAFE)
        msg.set_qos_profile(QoSProfileIE(_qos_bytes()).encode()[3:])
        msg.set_ggsn_address_signalling(_ip4(ggsn_addr_sig))
        msg.set_ggsn_address_user_traffic(_ip4(ggsn_addr_data))
    return msg


def v1_delete_pdp_context_request(
        teid=0xAAAAAAAA, seq_num=1,
        nsapi=5, teardown=True,
):
    # type: (int, int, int, bool) -> DeletePDPContextRequest
    msg = DeletePDPContextRequest(teid=teid, seq_num=seq_num)
    msg.set_teardown_ind(teardown)
    msg.set_nsapi(nsapi)
    return msg


def v1_delete_pdp_context_response(teid=0, seq_num=1, cause=None):
    # type: (int, int, Optional[int]) -> DeletePDPContextResponse
    if cause is None:
        cause = V1.CAUSE_REQUEST_ACCEPTED
    msg = DeletePDPContextResponse(teid=teid, seq_num=seq_num)
    msg.set_cause(cause)
    return msg


def v1_error_indication(
        teid=0, seq_num=1,
        teid_data=0xDEADBEEF,
        gsn_addr="10.0.0.99",
):
    # type: (int, int, int, str) -> ErrorIndication
    msg = ErrorIndication(teid=teid, seq_num=seq_num)
    msg.set_teid_data(teid_data)
    msg.set_gsn_address(_ip4(gsn_addr))
    return msg


def v1_pdu_notification_request(
        teid=0, seq_num=1,
        imsi="272030100000000",
        teid_control=0x11111112,
        apn="internet",
        ggsn_addr="192.168.1.1",
):
    # type: (int, int, str, int, str, str) -> PDUNotificationRequest
    msg = PDUNotificationRequest(teid=teid, seq_num=seq_num)
    msg.set_imsi(imsi)
    msg.set_teid_control(teid_control)
    msg.set_end_user_address(
        pdp_type_org=EndUserAddressIE.PTO_IETF,
        pdp_type_num=EndUserAddressIE.PDN_IPv4,
    )
    msg.set_apn(apn)
    msg.set_ggsn_address(_ip4(ggsn_addr))
    return msg


def v1_pdu_notification_response(teid=0, seq_num=1, cause=None):
    # type: (int, int, Optional[int]) -> PDUNotificationResponse
    if cause is None:
        cause = V1.CAUSE_REQUEST_ACCEPTED
    msg = PDUNotificationResponse(teid=teid, seq_num=seq_num)
    msg.set_cause(cause)
    return msg


def v1_sgsn_context_request(
        teid=0, seq_num=1,
        imsi="272030100000000",
        mcc="272", mnc="03", lac=1234, rac=5,
        teid_control=0x11111112,
        sgsn_addr="10.0.2.1",
        nsapi=5,
):
    # type: (int, int, str, str, str, int, int, int, str, int) -> SGSNContextRequest
    msg = SGSNContextRequest(teid=teid, seq_num=seq_num)
    msg.set_imsi(imsi)
    msg.set_rai(mcc, mnc, lac=lac, rac=rac)
    msg.set_teid_control(teid_control)
    msg.set_sgsn_address(_ip4(sgsn_addr))
    msg.set_nsapi(nsapi)
    return msg


def v1_sgsn_context_response(
        teid=0, seq_num=1,
        cause=None,
        teid_control=0x87654321,
        sgsn_addr="10.0.3.1",
):
    # type: (int, int, Optional[int], int, str) -> SGSNContextResponse
    if cause is None:
        cause = V1.CAUSE_REQUEST_ACCEPTED
    msg = SGSNContextResponse(teid=teid, seq_num=seq_num)
    msg.set_cause(cause)
    if cause == V1.CAUSE_REQUEST_ACCEPTED:
        msg.set_teid_control(teid_control)
        msg.set_sgsn_address(_ip4(sgsn_addr))
    return msg


def v1_sgsn_context_acknowledge(teid=0, seq_num=1, cause=None):
    # type: (int, int, Optional[int]) -> SGSNContextAcknowledge
    if cause is None:
        cause = V1.CAUSE_REQUEST_ACCEPTED
    msg = SGSNContextAcknowledge(teid=teid, seq_num=seq_num)
    msg.set_cause(cause)
    return msg


def v1_forward_relocation_request(
        teid=0, seq_num=1,
        imsi="272030100000000",
        mcc="272", mnc="03", lac=2000, rac=10,
        teid_control=0xABCDABCD,
        sgsn_addr_sig="10.0.4.1", sgsn_addr_data="10.0.4.2",
):
    # type: (int, int, str, str, str, int, int, int, str, str) -> ForwardRelocationRequest
    msg = ForwardRelocationRequest(teid=teid, seq_num=seq_num)
    msg.set_imsi(imsi)
    msg.set_rai(mcc, mnc, lac=lac, rac=rac)
    msg.set_teid_control(teid_control)
    msg.set_sgsn_address_signalling(_ip4(sgsn_addr_sig))
    msg.set_sgsn_address_user_traffic(_ip4(sgsn_addr_data))
    return msg


def v1_forward_relocation_response(
        teid=0, seq_num=1,
        cause=None,
        teid_control=0xDCBCDCBC,
        sgsn_addr_sig="10.0.5.1",
):
    # type: (int, int, Optional[int], int, str) -> ForwardRelocationResponse
    if cause is None:
        cause = V1.CAUSE_REQUEST_ACCEPTED
    msg = ForwardRelocationResponse(teid=teid, seq_num=seq_num)
    msg.set_cause(cause)
    if cause == V1.CAUSE_REQUEST_ACCEPTED:
        msg.set_teid_control(teid_control)
        msg.set_sgsn_address_signalling(_ip4(sgsn_addr_sig))
    return msg


def v1_relocation_cancel_request(
        teid=0, seq_num=1,
        imsi="272030100000000",
):
    # type: (int, int, str) -> RelocationCancelRequest
    msg = RelocationCancelRequest(teid=teid, seq_num=seq_num)
    msg.set_imsi(imsi)
    return msg


def v1_relocation_cancel_response(teid=0, seq_num=1, cause=None):
    # type: (int, int, Optional[int]) -> RelocationCancelResponse
    if cause is None:
        cause = V1.CAUSE_REQUEST_ACCEPTED
    msg = RelocationCancelResponse(teid=teid, seq_num=seq_num)
    msg.set_cause(cause)
    return msg


def v1_data_record_transfer_request(
        teid=0, seq_num=1,
        command=1,
        record_data=None,
):
    # type: (int, int, int, Optional[bytes]) -> DataRecordTransferRequest
    if record_data is None:
        record_data = b"\x00\x01" + b"\xff" * 32
    msg = DataRecordTransferRequest(teid=teid, seq_num=seq_num)
    msg.set_packet_transfer_command(command)
    msg.set_data_record_packet(record_data)
    return msg


def v1_data_record_transfer_response(teid=0, seq_num=1, cause=None):
    # type: (int, int, Optional[int]) -> DataRecordTransferResponse
    if cause is None:
        cause = V1.CAUSE_REQUEST_ACCEPTED
    msg = DataRecordTransferResponse(teid=teid, seq_num=seq_num)
    msg.set_cause(cause)
    return msg


def v1_mbms_session_start_request(
        teid=0, seq_num=1,
        tmgi=b"\x00\x00\x01\x02\xf2\x30",
        session_id=b"\x01",
        service_area=b"\x00\x01\x00\x01",
):
    # type: (int, int, bytes, bytes, bytes) -> MBMSSessionStartRequest
    msg = MBMSSessionStartRequest(teid=teid, seq_num=seq_num)
    msg.set_recovery(0)
    msg.set_tmgi(tmgi)
    msg.set_mbms_session_id(session_id)
    msg.set_mbms_service_area(service_area)
    return msg


def v1_mbms_session_start_response(teid=0, seq_num=1, cause=None):
    # type: (int, int, Optional[int]) -> MBMSSessionStartResponse
    if cause is None:
        cause = V1.CAUSE_REQUEST_ACCEPTED
    msg = MBMSSessionStartResponse(teid=teid, seq_num=seq_num)
    msg.set_cause(cause)
    msg.set_recovery(0)
    return msg


# ===========================================================================
# GTPv2-C factory functions
# ===========================================================================

def v2_echo_request(seq_num=1, recovery=0):
    # type: (int, int) -> V2EchoRequest
    msg = V2EchoRequest(teid=None, seq_num=seq_num)
    msg.set_recovery(recovery)
    return msg


def v2_echo_response(seq_num=1, recovery=0):
    # type: (int, int) -> V2EchoResponse
    msg = V2EchoResponse(teid=None, seq_num=seq_num)
    msg.set_recovery(recovery)
    return msg


def v2_create_session_request(
        seq_num=1,
        imsi="272030100000000",
        msisdn="353871234567",
        mcc="272", mnc="03", tac=0x1234,
        apn="internet",
        pdn_type=None,
        ambr_ul=100000, ambr_dl=200000,
        mme_teid=0x11111111, mme_addr="10.0.0.1",
        pgw_teid=0x22222222, pgw_addr="10.0.1.1",
        ebi=5, enb_teid=0xAAAA1111, enb_addr="192.168.10.10",
        rat_type=None,
):
    # type: (int, str, str, str, str, int, str, Optional[int], int, int, int, str, int, str, int, int, str, Optional[int]) -> CreateSessionRequest
    if pdn_type is None:
        pdn_type = V2.PDN_TYPE_IPv4
    if rat_type is None:
        rat_type = V2.RAT_EUTRAN
    msg = CreateSessionRequest(teid=None, seq_num=seq_num)
    msg.set_imsi(imsi)
    msg.set_msisdn(msisdn)
    msg.set_rat_type(rat_type)
    msg.set_serving_network(mcc, mnc)
    msg.set_uli(ULIIE.with_tai(mcc, mnc, tac=tac))
    msg.set_apn(apn)
    msg.set_selection_mode(0)
    msg.set_pdn_type(pdn_type)
    msg.set_paa(PAAIE(pdn_type, "0.0.0.0"))
    msg.set_apn_restriction(0)
    msg.set_ambr(ambr_ul, ambr_dl)
    msg.set_recovery(0)
    msg.set_sender_fteid(FTEIDIE(V2.FTEID_S11_MME, teid=mme_teid, ipv4=mme_addr))
    msg.set_pgw_fteid(FTEIDIE(V2.FTEID_S5S8C_PGW, teid=pgw_teid, ipv4=pgw_addr))
    msg.add_bearer_context(_bearer_ctx(
        ebi=ebi,
        interface_type=V2.FTEID_S1U_ENODEB,
        teid=enb_teid,
        ipv4=enb_addr,
    ))
    return msg


def v2_create_session_response(
        teid=0x11111111, seq_num=1,
        cause=None,
        sgw_teid=0x33333333, sgw_addr="10.0.2.1",
        pgw_teid=0x44444444, pgw_addr="10.0.1.1",
        allocated_ip="100.64.0.1",
        ambr_ul=100000, ambr_dl=200000,
        ebi=5, sgw_u_teid=0x55556666, sgw_u_addr="10.0.3.1",
):
    # type: (int, int, Optional[int], int, str, int, str, str, int, int, int, int, str) -> CreateSessionResponse
    if cause is None:
        cause = V2.CAUSE_REQUEST_ACCEPTED
    msg = CreateSessionResponse(teid=teid, seq_num=seq_num)
    msg.set_cause(cause)
    if cause == V2.CAUSE_REQUEST_ACCEPTED:
        msg.set_recovery(0)
        msg.set_sender_fteid(FTEIDIE(V2.FTEID_S11S4_SGW, teid=sgw_teid, ipv4=sgw_addr))
        msg.set_pgw_fteid(FTEIDIE(V2.FTEID_S5S8C_PGW, teid=pgw_teid, ipv4=pgw_addr))
        msg.set_paa(PAAIE(V2.PDN_TYPE_IPv4, allocated_ip))
        msg.set_apn_restriction(0)
        msg.set_ambr(ambr_ul, ambr_dl)
        msg.set_charging_id(0x0000CAFE)
        msg.add_bearer_context(_bearer_ctx(
            ebi=ebi,
            interface_type=V2.FTEID_S1U_SGW,
            teid=sgw_u_teid,
            ipv4=sgw_u_addr,
        ))
    return msg


def v2_modify_bearer_request(
        teid=0x33333333, seq_num=1,
        mcc="272", mnc="03", tac=0xAAAA,
        ebi=5, enb_teid=0xBBBBBBBB, enb_addr="192.168.10.20",
        rat_type=None,
):
    # type: (int, int, str, str, int, int, int, str, Optional[int]) -> ModifyBearerRequest
    if rat_type is None:
        rat_type = V2.RAT_EUTRAN
    msg = ModifyBearerRequest(teid=teid, seq_num=seq_num)
    msg.set_uli(ULIIE.with_tai(mcc, mnc, tac=tac))
    msg.set_rat_type(rat_type)
    msg.set_recovery(0)
    ctx = BearerContextIE()
    ctx.add_ie(EBIIE(ebi))
    ctx.add_ie(FTEIDIE(V2.FTEID_S1U_ENODEB, teid=enb_teid, ipv4=enb_addr))
    msg.add_bearer_context(ctx)
    return msg


def v2_modify_bearer_response(teid=0x11111111, seq_num=1, cause=None, ebi=5):
    # type: (int, int, Optional[int], int) -> ModifyBearerResponse
    if cause is None:
        cause = V2.CAUSE_REQUEST_ACCEPTED
    msg = ModifyBearerResponse(teid=teid, seq_num=seq_num)
    msg.set_cause(cause)
    msg.set_recovery(0)
    ctx = BearerContextIE()
    ctx.add_ie(EBIIE(ebi))
    ctx.add_ie(CauseIE(cause))
    msg.add_bearer_context(ctx)
    return msg


def v2_delete_session_request(
        teid=0x33333333, seq_num=1,
        ebi=5,
        cause=None,
        mcc="272", mnc="03", tac=0x1234,
):
    # type: (int, int, int, Optional[int], str, str, int) -> DeleteSessionRequest
    if cause is None:
        cause = V2.CAUSE_LOCAL_DETACH
    msg = DeleteSessionRequest(teid=teid, seq_num=seq_num)
    msg.set_ebi(ebi)
    msg.set_cause(cause)
    msg.set_uli(ULIIE.with_tai(mcc, mnc, tac=tac))
    return msg


def v2_delete_session_response(teid=0x11111111, seq_num=1, cause=None):
    # type: (int, int, Optional[int]) -> DeleteSessionResponse
    if cause is None:
        cause = V2.CAUSE_REQUEST_ACCEPTED
    msg = DeleteSessionResponse(teid=teid, seq_num=seq_num)
    msg.set_cause(cause)
    msg.set_recovery(0)
    return msg


def v2_create_bearer_request(
        teid=0x11111111, seq_num=1,
        linked_ebi=5, pti=1,
        ebi=7,
        interface_type=None,
        pgw_u_teid=0x77777777, pgw_u_addr="10.0.4.1",
        qci=1, pl=2,
        mbr_ul=40000, mbr_dl=40000,
        gbr_ul=40000, gbr_dl=40000,
):
    # type: (int, int, int, int, int, Optional[int], int, str, int, int, int, int, int, int) -> CreateBearerRequest
    if interface_type is None:
        interface_type = V2.FTEID_S5S8U_PGW
    msg = CreateBearerRequest(teid=teid, seq_num=seq_num)
    msg.set_linked_ebi(linked_ebi)
    msg.set_pti(pti)
    msg.add_bearer_context(_bearer_ctx(
        ebi=ebi,
        interface_type=interface_type,
        teid=pgw_u_teid,
        ipv4=pgw_u_addr,
        qci=qci, pl=pl,
        mbr_ul=mbr_ul, mbr_dl=mbr_dl,
        gbr_ul=gbr_ul, gbr_dl=gbr_dl,
    ))
    return msg


def v2_create_bearer_response(
        teid=0x44444444, seq_num=1,
        cause=None,
        ebi=7, enb_teid=0xCCCCCCCC, enb_addr="192.168.10.30",
):
    # type: (int, int, Optional[int], int, int, str) -> CreateBearerResponse
    if cause is None:
        cause = V2.CAUSE_REQUEST_ACCEPTED
    msg = CreateBearerResponse(teid=teid, seq_num=seq_num)
    msg.set_cause(cause)
    msg.set_recovery(0)
    ctx = BearerContextIE()
    ctx.add_ie(EBIIE(ebi))
    ctx.add_ie(CauseIE(cause))
    ctx.add_ie(FTEIDIE(V2.FTEID_S1U_ENODEB, teid=enb_teid, ipv4=enb_addr))
    msg.add_bearer_context(ctx)
    return msg


def v2_update_bearer_request(
        teid=0x11111111, seq_num=1,
        ebi=5,
        qci=9, pl=8,
        ambr_ul=150000, ambr_dl=300000,
):
    # type: (int, int, int, int, int, int, int) -> UpdateBearerRequest
    msg = UpdateBearerRequest(teid=teid, seq_num=seq_num)
    msg.set_ambr(ambr_ul, ambr_dl)
    ctx = BearerContextIE()
    ctx.add_ie(EBIIE(ebi))
    ctx.add_ie(BearerQoSIE(qci=qci, pl=pl, mbr_ul=ambr_ul, mbr_dl=ambr_dl))
    msg.add_bearer_context(ctx)
    return msg


def v2_update_bearer_response(teid=0x44444444, seq_num=1, cause=None, ebi=5):
    # type: (int, int, Optional[int], int) -> UpdateBearerResponse
    if cause is None:
        cause = V2.CAUSE_REQUEST_ACCEPTED
    msg = UpdateBearerResponse(teid=teid, seq_num=seq_num)
    msg.set_cause(cause)
    ctx = BearerContextIE()
    ctx.add_ie(EBIIE(ebi))
    ctx.add_ie(CauseIE(cause))
    msg.add_bearer_context(ctx)
    return msg


def v2_delete_bearer_request(teid=0x11111111, seq_num=1, ebi=7):
    # type: (int, int, int) -> DeleteBearerRequest
    msg = DeleteBearerRequest(teid=teid, seq_num=seq_num)
    msg.add_ebi(ebi)
    return msg


def v2_delete_bearer_response(teid=0x44444444, seq_num=1, cause=None, ebi=7):
    # type: (int, int, Optional[int], int) -> DeleteBearerResponse
    if cause is None:
        cause = V2.CAUSE_REQUEST_ACCEPTED
    msg = DeleteBearerResponse(teid=teid, seq_num=seq_num)
    msg.set_cause(cause)
    ctx = BearerContextIE()
    ctx.add_ie(EBIIE(ebi))
    ctx.add_ie(CauseIE(cause))
    msg.add_bearer_context(ctx)
    return msg


def v2_modify_bearer_command(
        teid=0x33333333, seq_num=1,
        ebi=5,
        ambr_ul=50000, ambr_dl=100000,
):
    # type: (int, int, int, int, int) -> ModifyBearerCommand
    msg = ModifyBearerCommand(teid=teid, seq_num=seq_num)
    msg.set_ambr(ambr_ul, ambr_dl)
    ctx = BearerContextIE()
    ctx.add_ie(EBIIE(ebi))
    ctx.add_ie(BearerQoSIE(qci=9, pl=9, mbr_ul=ambr_ul, mbr_dl=ambr_dl))
    msg.add_bearer_context(ctx)
    return msg


def v2_modify_bearer_failure_indication(teid=0x11111111, seq_num=1, cause=None):
    # type: (int, int, Optional[int]) -> ModifyBearerFailureIndication
    if cause is None:
        cause = V2.CAUSE_NO_RESOURCES
    msg = ModifyBearerFailureIndication(teid=teid, seq_num=seq_num)
    msg.set_cause(cause)
    return msg


def v2_delete_bearer_command(teid=0x33333333, seq_num=1, ebi=7):
    # type: (int, int, int) -> DeleteBearerCommand
    msg = DeleteBearerCommand(teid=teid, seq_num=seq_num)
    ctx = BearerContextIE()
    ctx.add_ie(EBIIE(ebi))
    msg.add_bearer_context(ctx)
    return msg


def v2_bearer_resource_command(
        teid=0x33333333, seq_num=1,
        linked_ebi=5, pti=2,
):
    # type: (int, int, int, int) -> BearerResourceCommand
    msg = BearerResourceCommand(teid=teid, seq_num=seq_num)
    msg.set_linked_ebi(linked_ebi)
    msg.set_pti(pti)
    return msg


def v2_release_access_bearers_request(
        teid=0x33333333, seq_num=1,
        ebi=5,
        node_type=None,
):
    # type: (int, int, int, Optional[int]) -> ReleaseAccessBearersRequest
    if node_type is None:
        node_type = V2.NODE_TYPE_MME
    msg = ReleaseAccessBearersRequest(teid=teid, seq_num=seq_num)
    msg.add_ebi(ebi)
    msg.set_node_type(node_type)
    return msg


def v2_release_access_bearers_response(teid=0x11111111, seq_num=1, cause=None):
    # type: (int, int, Optional[int]) -> ReleaseAccessBearersResponse
    if cause is None:
        cause = V2.CAUSE_REQUEST_ACCEPTED
    msg = ReleaseAccessBearersResponse(teid=teid, seq_num=seq_num)
    msg.set_cause(cause)
    msg.set_recovery(0)
    return msg


def v2_downlink_data_notification(
        teid=0x11111111, seq_num=1,
        ebi=5,
        cause=None,
        arp_pl=9,
):
    # type: (int, int, int, Optional[int], int) -> DownlinkDataNotification
    if cause is None:
        cause = V2.CAUSE_REQUEST_ACCEPTED
    msg = DownlinkDataNotification(teid=teid, seq_num=seq_num)
    msg.set_ebi(ebi)
    msg.set_cause(cause)
    msg.set_arp(ARPIE(pl=arp_pl, pci=False, pvi=False))
    return msg


def v2_downlink_data_notification_ack(teid=0x33333333, seq_num=1, cause=None):
    # type: (int, int, Optional[int]) -> DownlinkDataNotificationAcknowledge
    if cause is None:
        cause = V2.CAUSE_REQUEST_ACCEPTED
    msg = DownlinkDataNotificationAcknowledge(teid=teid, seq_num=seq_num)
    msg.set_cause(cause)
    return msg


def v2_context_request(
        teid=0, seq_num=1,
        imsi="272030100000000",
        mcc="272", mnc="03",
        mme_teid=0xEEEEEEEE, mme_addr="10.1.0.1",
        rat_type=None,
):
    # type: (int, int, str, str, str, int, str, Optional[int]) -> ContextRequest
    if rat_type is None:
        rat_type = V2.RAT_EUTRAN
    msg = ContextRequest(teid=teid, seq_num=seq_num)
    msg.set_imsi(imsi)
    msg.set_rat_type(rat_type)
    msg.set_serving_network(mcc, mnc)
    msg.set_sender_fteid(FTEIDIE(V2.FTEID_S10_MME, teid=mme_teid, ipv4=mme_addr))
    return msg


def v2_context_response(
        teid=0xEEEEEEEE, seq_num=1,
        cause=None,
        imsi="272030100000000",
        mme_teid=0xFFFFFFFF, mme_addr="10.1.1.1",
):
    # type: (int, int, Optional[int], str, int, str) -> ContextResponse
    if cause is None:
        cause = V2.CAUSE_REQUEST_ACCEPTED
    msg = ContextResponse(teid=teid, seq_num=seq_num)
    msg.set_cause(cause)
    if cause == V2.CAUSE_REQUEST_ACCEPTED:
        msg.set_imsi(imsi)
        msg.set_sender_fteid(FTEIDIE(V2.FTEID_S10_MME, teid=mme_teid, ipv4=mme_addr))
    return msg


def v2_context_acknowledge(teid=0xFFFFFFFF, seq_num=1, cause=None):
    # type: (int, int, Optional[int]) -> ContextAcknowledge
    if cause is None:
        cause = V2.CAUSE_REQUEST_ACCEPTED
    msg = ContextAcknowledge(teid=teid, seq_num=seq_num)
    msg.set_cause(cause)
    return msg


def v2_forward_relocation_request(
        teid=0, seq_num=1,
        imsi="272030100000000",
        mme_teid=0xAAAAAAAA, mme_addr="10.1.0.1",
        ebi=5, sgw_u_teid=0x55556666, sgw_u_addr="10.0.3.1",
        rat_type=None,
):
    # type: (int, int, str, int, str, int, int, str, Optional[int]) -> V2ForwardRelocationRequest
    if rat_type is None:
        rat_type = V2.RAT_EUTRAN
    msg = V2ForwardRelocationRequest(teid=teid, seq_num=seq_num)
    msg.set_imsi(imsi)
    msg.set_sender_fteid(FTEIDIE(V2.FTEID_S10_MME, teid=mme_teid, ipv4=mme_addr))
    msg.set_rat_type(rat_type)
    msg.add_bearer_context(_bearer_ctx(
        ebi=ebi,
        interface_type=V2.FTEID_S1U_SGW,
        teid=sgw_u_teid,
        ipv4=sgw_u_addr,
    ))
    return msg


def v2_forward_relocation_response(
        teid=0xAAAAAAAA, seq_num=1,
        cause=None,
        mme_teid=0xBBBBBBBB, mme_addr="10.1.1.1",
):
    # type: (int, int, Optional[int], int, str) -> V2ForwardRelocationResponse
    if cause is None:
        cause = V2.CAUSE_REQUEST_ACCEPTED
    msg = V2ForwardRelocationResponse(teid=teid, seq_num=seq_num)
    msg.set_cause(cause)
    if cause == V2.CAUSE_REQUEST_ACCEPTED:
        msg.set_sender_fteid(FTEIDIE(V2.FTEID_S10_MME, teid=mme_teid, ipv4=mme_addr))
    return msg


def v2_detach_notification(teid=0x33333333, seq_num=1):
    # type: (int, int) -> DetachNotification
    return DetachNotification(teid=teid, seq_num=seq_num)


def v2_detach_acknowledge(teid=0x11111111, seq_num=1, cause=None):
    # type: (int, int, Optional[int]) -> DetachAcknowledge
    if cause is None:
        cause = V2.CAUSE_REQUEST_ACCEPTED
    msg = DetachAcknowledge(teid=teid, seq_num=seq_num)
    msg.set_cause(cause)
    return msg


def v2_suspend_notification(
        teid=0x33333333, seq_num=1,
        imsi="272030100000000",
):
    # type: (int, int, str) -> SuspendNotification
    msg = SuspendNotification(teid=teid, seq_num=seq_num)
    msg.set_imsi(imsi)
    return msg


def v2_suspend_acknowledge(teid=0x11111111, seq_num=1, cause=None):
    # type: (int, int, Optional[int]) -> SuspendAcknowledge
    if cause is None:
        cause = V2.CAUSE_REQUEST_ACCEPTED
    msg = SuspendAcknowledge(teid=teid, seq_num=seq_num)
    msg.set_cause(cause)
    return msg


def v2_resume_notification(
        teid=0x33333333, seq_num=1,
        imsi="272030100000000",
):
    # type: (int, int, str) -> ResumeNotification
    msg = ResumeNotification(teid=teid, seq_num=seq_num)
    msg.set_imsi(imsi)
    return msg


def v2_resume_acknowledge(teid=0x11111111, seq_num=1, cause=None):
    # type: (int, int, Optional[int]) -> ResumeAcknowledge
    if cause is None:
        cause = V2.CAUSE_REQUEST_ACCEPTED
    msg = ResumeAcknowledge(teid=teid, seq_num=seq_num)
    msg.set_cause(cause)
    return msg


def v2_pgw_restart_notification(
        seq_num=1,
        pgw_ip="10.0.1.1",
        sgw_ip="10.0.2.1",
):
    # type: (int, str, str) -> PGWRestartNotification
    msg = PGWRestartNotification(teid=None, seq_num=seq_num)
    msg.set_pgw_s5s8_ip(pgw_ip)
    msg.set_sgw_s11s4_ip(sgw_ip)
    return msg


def v2_pgw_restart_notification_ack(seq_num=1, cause=None):
    # type: (int, Optional[int]) -> PGWRestartNotificationAcknowledge
    if cause is None:
        cause = V2.CAUSE_REQUEST_ACCEPTED
    msg = PGWRestartNotificationAcknowledge(teid=None, seq_num=seq_num)
    msg.set_cause(cause)
    return msg


def v2_stop_paging_indication(
        seq_num=1,
        imsi="272030100000000",
):
    # type: (int, str) -> StopPagingIndication
    msg = StopPagingIndication(teid=None, seq_num=seq_num)
    msg.set_imsi(imsi)
    return msg


def v2_delete_pdn_connection_set_request(
        seq_num=1,
        mme_ip="10.0.0.1",
        csids=None,
):
    # type: (int, str, Optional[list]) -> DeletePDNConnectionSetRequest
    if csids is None:
        csids = [0x1234]
    msg = DeletePDNConnectionSetRequest(teid=None, seq_num=seq_num)
    msg.set_mme_fq_csid(FQCSIDIe(node_id=_ip4(mme_ip), csids=csids))
    return msg


def v2_modify_access_bearers_request(
        teid=0x33333333, seq_num=1,
        sgw_teid=0x33333333, sgw_addr="10.0.2.1",
        ebi=5, sgw_u_teid=0x55556666, sgw_u_addr="10.0.3.1",
):
    # type: (int, int, int, str, int, int, str) -> ModifyAccessBearersRequest
    msg = ModifyAccessBearersRequest(teid=teid, seq_num=seq_num)
    msg.set_sender_fteid(FTEIDIE(V2.FTEID_S11S4_SGW, teid=sgw_teid, ipv4=sgw_addr))
    ctx = BearerContextIE()
    ctx.add_ie(EBIIE(ebi))
    ctx.add_ie(FTEIDIE(V2.FTEID_S1U_SGW, teid=sgw_u_teid, ipv4=sgw_u_addr))
    msg.add_bearer_context_to_modify(ctx)
    return msg


def v2_modify_access_bearers_response(teid=0x11111111, seq_num=1, cause=None):
    # type: (int, int, Optional[int]) -> ModifyAccessBearersResponse
    if cause is None:
        cause = V2.CAUSE_REQUEST_ACCEPTED
    msg = ModifyAccessBearersResponse(teid=teid, seq_num=seq_num)
    msg.set_cause(cause)
    msg.set_recovery(0)
    return msg


def v2_mbms_session_start_request(
        seq_num=1,
        tmgi=b"\x00\x00\x01\x02\xf2\x30",
        session_id=b"\x01",
        service_area=b"\x00\x01\x00\x01",
        ambr_ul=10000, ambr_dl=10000,
        fteid_teid=0x0A0A0A0A, fteid_addr="10.10.10.1",
):
    # type: (int, bytes, bytes, bytes, int, int, int, str) -> V2MBMSSessionStartRequest
    msg = V2MBMSSessionStartRequest(teid=None, seq_num=seq_num)
    msg.set_sender_fteid(FTEIDIE(V2.FTEID_SM_MBMS_GW, teid=fteid_teid, ipv4=fteid_addr))
    msg.set_tmgi(tmgi)
    msg.set_mbms_session_id(session_id)
    msg.set_mbms_service_area(service_area)
    msg.set_ambr(ambr_ul, ambr_dl)
    return msg


def v2_mbms_session_stop_request(
        seq_num=1,
        tmgi=b"\x00\x00\x01\x02\xf2\x30",
        flow_id=b"\x00\x01",
):
    # type: (int, bytes, bytes) -> V2MBMSSessionStopRequest
    msg = V2MBMSSessionStopRequest(teid=None, seq_num=seq_num)
    msg.set_tmgi(tmgi)
    msg.set_mbms_flow_id(flow_id)
    return msg
