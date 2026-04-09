#!/usr/bin/env python3
"""Generate sample GTPv1-C and GTPv2-C packets and write them to a hex file.

Usage:
    python3 examples/generate_samples.py [output_file]

Output defaults to examples/sample_packets.hex
Each entry in the output file has the format:

    # <description>
    <hex string>

The hex file can be read back with gtpc.utils.hexdump.from_hex().
"""

import socket
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# GTPv1-C imports
# ---------------------------------------------------------------------------
from gtpc.v1.messages import (
    EchoRequest, EchoResponse,
    CreatePDPContextRequest, CreatePDPContextResponse,
    UpdatePDPContextRequest, UpdatePDPContextResponse,
    DeletePDPContextRequest, DeletePDPContextResponse,
    ErrorIndication,
    PDUNotificationRequest,
    SGSNContextRequest, SGSNContextResponse, SGSNContextAcknowledge,
    ForwardRelocationRequest, ForwardRelocationResponse,
    RelocationCancelRequest, RelocationCancelResponse,
    MBMSSessionStartRequest, MBMSSessionStartResponse,
    DataRecordTransferRequest,
)
from gtpc.v1.ie.tlv import EndUserAddressIE, QoSProfileIE
from gtpc.v1 import constants as V1

# ---------------------------------------------------------------------------
# GTPv2-C imports
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
    DeleteBearerCommand,
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
    UpdatePDNConnectionSetRequest,
    ModifyAccessBearersRequest, ModifyAccessBearersResponse,
    MBMSSessionStartRequest as V2MBMSSessionStartRequest,
    MBMSSessionStopRequest as V2MBMSSessionStopRequest,
    StopPagingIndication,
    TraceSessionActivation,
)
from gtpc.v2.ie.typed import (
    IMSIIE, CauseIE, RecoveryIE, APNIE, AMBRIE, EBIIE,
    IPAddressIE, MEIIE, MSISDNIE, IndicationIE, PCOIE,
    PAAIE, BearerQoSIE, FlowQoSIE, RATTypeIE, ServingNetworkIE,
    ULIIE, FTEIDIE, BearerContextIE, ChargingIDIE,
    PDNTypeIE, PTIIE, UETimeZoneIE, APNRestrictionIE,
    SelectionModeIE, FQCSIDIe, NodeTypeIE, FQDNIE, ARPIE,
)
from gtpc.v2 import constants as V2

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def ip4(addr: str) -> bytes:
    return socket.inet_pton(socket.AF_INET, addr)


def bearer_ctx(ebi: int, interface_type: int, teid: int, ipv4: str,
               qci: int = 9, pl: int = 9,
               mbr_ul: int = 128_000, mbr_dl: int = 128_000,
               gbr_ul: int = 0, gbr_dl: int = 0,
               instance: int = 0) -> BearerContextIE:
    ctx = BearerContextIE(instance=instance)
    ctx.add_ie(EBIIE(ebi))
    ctx.add_ie(FTEIDIE(interface_type, teid=teid, ipv4=ipv4))
    ctx.add_ie(BearerQoSIE(
        qci=qci, pl=pl, pci=False, pvi=False,
        mbr_ul=mbr_ul, mbr_dl=mbr_dl,
        gbr_ul=gbr_ul, gbr_dl=gbr_dl,
    ))
    return ctx


def qos_profile_bytes() -> bytes:
    """Minimal 3-byte QoS profile (Release 99 format)."""
    return bytes([0x0B, 0x92, 0x1F])


# ---------------------------------------------------------------------------
# Build all sample packets, return list of (description, bytes)
# ---------------------------------------------------------------------------

def build_samples() -> list[tuple[str, bytes]]:
    samples: list[tuple[str, bytes]] = []

    def add(desc: str, raw: bytes) -> None:
        samples.append((desc, raw))

    # ===================================================================
    # GTPv1-C
    # ===================================================================

    # --- Path management ------------------------------------------------

    echo_req = EchoRequest(teid=0, seq_num=1)
    echo_req.set_recovery(42)
    add("GTPv1 Echo Request", echo_req.encode())

    echo_res = EchoResponse(teid=0, seq_num=1)
    echo_res.set_recovery(42)
    add("GTPv1 Echo Response", echo_res.encode())

    # --- Create PDP Context (2G/3G attach) ------------------------------

    create_pdp_req = CreatePDPContextRequest(teid=0, seq_num=100)
    create_pdp_req.set_imsi("272030100000000")
    create_pdp_req.set_rai("272", "03", lac=1234, rac=5)
    create_pdp_req.set_recovery(0)
    create_pdp_req.set_selection_mode(V1.SEL_MODE_MS_OR_NET_APN_SUBSCR_VERIFIED)
    create_pdp_req.set_teid_data(0x372F0001)
    create_pdp_req.set_teid_control(0x372F0002)
    create_pdp_req.set_nsapi(5)
    create_pdp_req.set_charging_chars(0x0800)
    create_pdp_req.set_end_user_address(
        pdp_type_org=EndUserAddressIE.PTO_IETF,
        pdp_type_num=EndUserAddressIE.PDN_IPv4,
    )
    create_pdp_req.set_apn("internet.operator.com")
    create_pdp_req.set_sgsn_address_signalling(ip4("10.0.0.1"))
    create_pdp_req.set_sgsn_address_user_traffic(ip4("10.0.0.2"))
    create_pdp_req.set_msisdn("353871234567")
    create_pdp_req.set_qos_profile(QoSProfileIE(qos_profile_bytes()).encode()[3:])
    create_pdp_req.set_rat_type(V1.RAT_UTRAN)
    create_pdp_req.set_imei_sv("3549291043289800")
    create_pdp_req.set_ms_timezone(tz=0x40, dst=0)
    add("GTPv1 Create PDP Context Request", create_pdp_req.encode())

    create_pdp_res = CreatePDPContextResponse(teid=0x372F0002, seq_num=100)
    create_pdp_res.set_cause(V1.CAUSE_REQUEST_ACCEPTED)
    create_pdp_res.set_recovery(0)
    create_pdp_res.set_teid_data(0xAABBCCDD)
    create_pdp_res.set_teid_control(0x11223344)
    create_pdp_res.set_charging_id(0x0000CAFE)
    create_pdp_res.set_end_user_address(
        pdp_type_org=EndUserAddressIE.PTO_IETF,
        pdp_type_num=EndUserAddressIE.PDN_IPv4,
        address=ip4("100.64.0.1"),
    )
    create_pdp_res.set_ggsn_address_signalling(ip4("192.168.1.1"))
    create_pdp_res.set_ggsn_address_user_traffic(ip4("192.168.1.2"))
    create_pdp_res.set_qos_profile(QoSProfileIE(qos_profile_bytes()).encode()[3:])
    add("GTPv1 Create PDP Context Response (accepted)", create_pdp_res.encode())

    create_pdp_res_rej = CreatePDPContextResponse(teid=0, seq_num=101)
    create_pdp_res_rej.set_cause(V1.CAUSE_NO_RESOURCES)
    add("GTPv1 Create PDP Context Response (rejected)", create_pdp_res_rej.encode())

    # --- Update PDP Context (handover / QoS change) ---------------------

    update_pdp_req = UpdatePDPContextRequest(teid=0xAABBCCDD, seq_num=200)
    update_pdp_req.set_teid_data(0x55667788)
    update_pdp_req.set_teid_control(0x99AABBCC)
    update_pdp_req.set_nsapi(5)
    update_pdp_req.set_sgsn_address_signalling(ip4("10.0.1.1"))
    update_pdp_req.set_sgsn_address_user_traffic(ip4("10.0.1.2"))
    update_pdp_req.set_qos_profile(QoSProfileIE(qos_profile_bytes()).encode()[3:])
    update_pdp_req.set_rat_type(V1.RAT_GERAN)
    add("GTPv1 Update PDP Context Request", update_pdp_req.encode())

    update_pdp_res = UpdatePDPContextResponse(teid=0x55667788, seq_num=200)
    update_pdp_res.set_cause(V1.CAUSE_REQUEST_ACCEPTED)
    update_pdp_res.set_recovery(0)
    update_pdp_res.set_teid_data(0xAABBCCDD)
    update_pdp_res.set_teid_control(0x11223344)
    update_pdp_res.set_charging_id(0x0000CAFE)
    update_pdp_res.set_qos_profile(QoSProfileIE(qos_profile_bytes()).encode()[3:])
    update_pdp_res.set_ggsn_address_signalling(ip4("192.168.1.1"))
    update_pdp_res.set_ggsn_address_user_traffic(ip4("192.168.1.2"))
    add("GTPv1 Update PDP Context Response", update_pdp_res.encode())

    # --- Delete PDP Context (detach / PDP deactivation) ----------------

    delete_pdp_req = DeletePDPContextRequest(teid=0xAABBCCDD, seq_num=300)
    delete_pdp_req.set_teardown_ind(teardown=True)
    delete_pdp_req.set_nsapi(5)
    add("GTPv1 Delete PDP Context Request (teardown)", delete_pdp_req.encode())

    delete_pdp_res = DeletePDPContextResponse(teid=0x11223344, seq_num=300)
    delete_pdp_res.set_cause(V1.CAUSE_REQUEST_ACCEPTED)
    add("GTPv1 Delete PDP Context Response", delete_pdp_res.encode())

    # --- Error Indication -----------------------------------------------

    err_ind = ErrorIndication(teid=0, seq_num=1)
    err_ind.set_teid_data(0xDEADBEEF)
    err_ind.set_gsn_address(ip4("10.0.0.99"))
    add("GTPv1 Error Indication", err_ind.encode())

    # --- PDU Notification (GGSN-initiated) ------------------------------

    pdu_notif = PDUNotificationRequest(teid=0, seq_num=50)
    pdu_notif.set_imsi("272030100000000")
    pdu_notif.set_teid_control(0x372F0002)
    pdu_notif.set_end_user_address(
        pdp_type_org=EndUserAddressIE.PTO_IETF,
        pdp_type_num=EndUserAddressIE.PDN_IPv4,
    )
    pdu_notif.set_apn("internet.operator.com")
    pdu_notif.set_ggsn_address(ip4("192.168.1.1"))
    add("GTPv1 PDU Notification Request", pdu_notif.encode())

    # --- SGSN Context (inter-SGSN RAU) ---------------------------------

    sgsn_ctx_req = SGSNContextRequest(teid=0, seq_num=400)
    sgsn_ctx_req.set_imsi("272030100000000")
    sgsn_ctx_req.set_rai("272", "03", lac=1234, rac=5)
    sgsn_ctx_req.set_teid_control(0x12345678)
    sgsn_ctx_req.set_sgsn_address(ip4("10.0.2.1"))
    sgsn_ctx_req.set_nsapi(5)
    add("GTPv1 SGSN Context Request", sgsn_ctx_req.encode())

    sgsn_ctx_res = SGSNContextResponse(teid=0x12345678, seq_num=400)
    sgsn_ctx_res.set_cause(V1.CAUSE_REQUEST_ACCEPTED)
    sgsn_ctx_res.set_teid_control(0x87654321)
    sgsn_ctx_res.set_sgsn_address(ip4("10.0.3.1"))
    add("GTPv1 SGSN Context Response", sgsn_ctx_res.encode())

    sgsn_ctx_ack = SGSNContextAcknowledge(teid=0x87654321, seq_num=400)
    sgsn_ctx_ack.set_cause(V1.CAUSE_REQUEST_ACCEPTED)
    add("GTPv1 SGSN Context Acknowledge", sgsn_ctx_ack.encode())

    # --- Forward Relocation (SRNS relocation) --------------------------

    fwd_reloc_req = ForwardRelocationRequest(teid=0, seq_num=500)
    fwd_reloc_req.set_imsi("272030100000000")
    fwd_reloc_req.set_rai("272", "03", lac=2000, rac=10)
    fwd_reloc_req.set_teid_control(0xABCDABCD)
    fwd_reloc_req.set_sgsn_address_signalling(ip4("10.0.4.1"))
    fwd_reloc_req.set_sgsn_address_user_traffic(ip4("10.0.4.2"))
    add("GTPv1 Forward Relocation Request", fwd_reloc_req.encode())

    fwd_reloc_res = ForwardRelocationResponse(teid=0xABCDABCD, seq_num=500)
    fwd_reloc_res.set_cause(V1.CAUSE_REQUEST_ACCEPTED)
    fwd_reloc_res.set_teid_control(0xDCBCDCBC)
    fwd_reloc_res.set_sgsn_address_signalling(ip4("10.0.5.1"))
    add("GTPv1 Forward Relocation Response", fwd_reloc_res.encode())

    reloc_cancel_req = RelocationCancelRequest(teid=0, seq_num=501)
    reloc_cancel_req.set_imsi("272030100000000")
    add("GTPv1 Relocation Cancel Request", reloc_cancel_req.encode())

    reloc_cancel_res = RelocationCancelResponse(teid=0, seq_num=501)
    reloc_cancel_res.set_cause(V1.CAUSE_REQUEST_ACCEPTED)
    add("GTPv1 Relocation Cancel Response", reloc_cancel_res.encode())

    # --- MBMS ----------------------------------------------------------

    mbms_start_req = MBMSSessionStartRequest(teid=0, seq_num=600)
    mbms_start_req.set_recovery(0)
    mbms_start_req.set_tmgi(b"\x00\x00\x01\x02\xf2\x30")
    mbms_start_req.set_mbms_session_id(b"\x01")
    mbms_start_req.set_mbms_service_area(b"\x00\x01\x00\x01")
    add("GTPv1 MBMS Session Start Request", mbms_start_req.encode())

    mbms_start_res = MBMSSessionStartResponse(teid=0, seq_num=600)
    mbms_start_res.set_cause(V1.CAUSE_REQUEST_ACCEPTED)
    mbms_start_res.set_recovery(0)
    add("GTPv1 MBMS Session Start Response", mbms_start_res.encode())

    # --- Data Record Transfer (GTP' / CDR) ----------------------------

    cdr_req = DataRecordTransferRequest(teid=0, seq_num=700)
    cdr_req.set_packet_transfer_command(1)  # 1 = Send Data Record Packet
    cdr_req.set_data_record_packet(b"\x00\x01" + b"\xFF" * 32)
    add("GTPv1 Data Record Transfer Request", cdr_req.encode())

    # ===================================================================
    # GTPv2-C
    # ===================================================================

    # --- Path management ------------------------------------------------

    v2_echo_req = V2EchoRequest(teid=None, seq_num=1)
    v2_echo_req.set_recovery(0)
    add("GTPv2 Echo Request", v2_echo_req.encode())

    v2_echo_res = V2EchoResponse(teid=None, seq_num=1)
    v2_echo_res.set_recovery(0)
    add("GTPv2 Echo Response", v2_echo_res.encode())

    # --- Create Session Request (LTE initial attach, default bearer) ----

    csr = CreateSessionRequest(teid=None, seq_num=42)
    csr.set_imsi("272030100000000")
    csr.set_msisdn("353871234567")
    csr.set_mei("3549291043289800")
    csr.set_rat_type(V2.RAT_EUTRAN)
    csr.set_serving_network("272", "03")
    csr.set_uli(ULIIE.with_tai_and_ecgi("272", "03", tac=0x1234, eci=0xABCDE))
    csr.set_apn("internet.operator.com")
    csr.set_selection_mode(0)
    csr.set_pdn_type(V2.PDN_TYPE_IPv4)
    csr.set_paa(PAAIE(V2.PDN_TYPE_IPv4, "0.0.0.0"))
    csr.set_apn_restriction(0)
    csr.set_ambr(100_000, 200_000)
    csr.set_recovery(0)
    csr.set_charging_chars(0x0800)
    csr.set_ue_timezone(tz_byte=0x40, dst=0)
    csr.set_sender_fteid(FTEIDIE(V2.FTEID_S11_MME, teid=0x11111111, ipv4="10.0.0.1"))
    csr.set_pgw_fteid(FTEIDIE(V2.FTEID_S5S8C_PGW, teid=0x22222222, ipv4="10.0.1.1"))
    csr.add_bearer_context(bearer_ctx(
        ebi=5, interface_type=V2.FTEID_S1U_ENODEB,
        teid=0xAAAA1111, ipv4="192.168.10.10",
    ))
    add("GTPv2 Create Session Request (IPv4, LTE attach)", csr.encode())

    # --- Create Session Request (IPv4v6 dual-stack) ---------------------

    csr_dual = CreateSessionRequest(teid=None, seq_num=43)
    csr_dual.set_imsi("272030100000001")
    csr_dual.set_rat_type(V2.RAT_EUTRAN)
    csr_dual.set_serving_network("272", "03")
    csr_dual.set_uli(ULIIE.with_tai("272", "03", tac=0x5678))
    csr_dual.set_apn("ims")
    csr_dual.set_pdn_type(V2.PDN_TYPE_IPv4v6)
    csr_dual.set_paa(PAAIE(V2.PDN_TYPE_IPv4, "0.0.0.0"))
    csr_dual.set_ambr(40_000, 40_000)
    csr_dual.set_sender_fteid(FTEIDIE(V2.FTEID_S11_MME, teid=0x11111112, ipv4="10.0.0.1"))
    csr_dual.add_bearer_context(bearer_ctx(
        ebi=6, interface_type=V2.FTEID_S1U_ENODEB,
        teid=0xAAAA2222, ipv4="192.168.10.11",
        qci=5, pl=1,  # IMS signalling bearer
    ))
    add("GTPv2 Create Session Request (IPv4v6, IMS)", csr_dual.encode())

    # --- Create Session Response ----------------------------------------

    css = CreateSessionResponse(teid=0x11111111, seq_num=42)
    css.set_cause(V2.CAUSE_REQUEST_ACCEPTED)
    css.set_recovery(0)
    css.set_sender_fteid(FTEIDIE(V2.FTEID_S11S4_SGW, teid=0x33333333, ipv4="10.0.2.1"))
    css.set_pgw_fteid(FTEIDIE(V2.FTEID_S5S8C_PGW, teid=0x44444444, ipv4="10.0.1.1"))
    css.set_paa(PAAIE(V2.PDN_TYPE_IPv4, "100.64.0.1"))
    css.set_apn_restriction(0)
    css.set_ambr(100_000, 200_000)
    css.set_charging_id(0xCAFEBABE)
    css.add_bearer_context(bearer_ctx(
        ebi=5, interface_type=V2.FTEID_S1U_SGW,
        teid=0x55556666, ipv4="10.0.3.1",
    ))
    add("GTPv2 Create Session Response (accepted)", css.encode())

    css_rej = CreateSessionResponse(teid=0x11111111, seq_num=43)
    css_rej.set_cause(V2.CAUSE_ALL_DYNAMIC_ADDR_OCCUPIED)
    add("GTPv2 Create Session Response (rejected)", css_rej.encode())

    # --- Modify Bearer Request (eNodeB relocation / TAU with S1) --------

    mbr = ModifyBearerRequest(teid=0x33333333, seq_num=100)
    mbr.set_uli(ULIIE.with_tai_and_ecgi("272", "03", tac=0xAAAA, eci=0x12345))
    mbr.set_rat_type(V2.RAT_EUTRAN)
    mbr.set_recovery(0)
    ctx = BearerContextIE()
    ctx.add_ie(EBIIE(5))
    ctx.add_ie(FTEIDIE(V2.FTEID_S1U_ENODEB, teid=0xBBBBBBBB, ipv4="192.168.10.20"))
    mbr.add_bearer_context(ctx)
    add("GTPv2 Modify Bearer Request", mbr.encode())

    mbr_res = ModifyBearerResponse(teid=0x11111111, seq_num=100)
    mbr_res.set_cause(V2.CAUSE_REQUEST_ACCEPTED)
    mbr_res.set_recovery(0)
    ctx2 = BearerContextIE()
    ctx2.add_ie(EBIIE(5))
    ctx2.add_ie(CauseIE(V2.CAUSE_REQUEST_ACCEPTED))
    mbr_res.add_bearer_context(ctx2)
    add("GTPv2 Modify Bearer Response", mbr_res.encode())

    # --- Delete Session Request (UE detach) -----------------------------

    dsr = DeleteSessionRequest(teid=0x33333333, seq_num=200)
    dsr.set_ebi(5)
    dsr.set_cause(V2.CAUSE_LOCAL_DETACH)
    dsr.set_uli(ULIIE.with_tai("272", "03", tac=0x1234))
    dsr.set_ue_timezone(tz_byte=0x40, dst=0)
    add("GTPv2 Delete Session Request (local detach)", dsr.encode())

    dsr_network = DeleteSessionRequest(teid=0x33333333, seq_num=201)
    dsr_network.set_ebi(5)
    dsr_network.set_cause(V2.CAUSE_ISR_DEACTIVATION)
    add("GTPv2 Delete Session Request (ISR deactivation)", dsr_network.encode())

    dsr_res = DeleteSessionResponse(teid=0x11111111, seq_num=200)
    dsr_res.set_cause(V2.CAUSE_REQUEST_ACCEPTED)
    dsr_res.set_recovery(0)
    add("GTPv2 Delete Session Response", dsr_res.encode())

    # --- Create Bearer Request (dedicated bearer — VoLTE QCI-1) --------

    cbr = CreateBearerRequest(teid=0x11111111, seq_num=300)
    cbr.set_linked_ebi(5)
    cbr.set_pti(1)
    cbr.add_bearer_context(bearer_ctx(
        ebi=7, interface_type=V2.FTEID_S5S8U_PGW,
        teid=0x77777777, ipv4="10.0.4.1",
        qci=1, pl=2,
        mbr_ul=40_000, mbr_dl=40_000,
        gbr_ul=40_000, gbr_dl=40_000,
    ))
    add("GTPv2 Create Bearer Request (VoLTE QCI-1)", cbr.encode())

    cbr_res = CreateBearerResponse(teid=0x44444444, seq_num=300)
    cbr_res.set_cause(V2.CAUSE_REQUEST_ACCEPTED)
    cbr_res.set_recovery(0)
    ctx3 = BearerContextIE()
    ctx3.add_ie(EBIIE(7))
    ctx3.add_ie(CauseIE(V2.CAUSE_REQUEST_ACCEPTED))
    ctx3.add_ie(FTEIDIE(V2.FTEID_S1U_ENODEB, teid=0xCCCCCCCC, ipv4="192.168.10.30"))
    ctx3.add_ie(FTEIDIE(V2.FTEID_S1U_SGW, teid=0xDDDDDDDD, ipv4="10.0.3.1", instance=1))
    cbr_res.add_bearer_context(ctx3)
    add("GTPv2 Create Bearer Response (accepted)", cbr_res.encode())

    # --- Update Bearer Request (QoS change) ----------------------------

    ubr = UpdateBearerRequest(teid=0x11111111, seq_num=400)
    ubr.set_pco(b"\x80\x00\x00")
    ubr.set_ambr(150_000, 300_000)
    ctx4 = BearerContextIE()
    ctx4.add_ie(EBIIE(5))
    ctx4.add_ie(BearerQoSIE(qci=9, pl=8, mbr_ul=150_000, mbr_dl=300_000))
    ubr.add_bearer_context(ctx4)
    add("GTPv2 Update Bearer Request (QoS change)", ubr.encode())

    ubr_res = UpdateBearerResponse(teid=0x44444444, seq_num=400)
    ubr_res.set_cause(V2.CAUSE_REQUEST_ACCEPTED)
    ctx5 = BearerContextIE()
    ctx5.add_ie(EBIIE(5))
    ctx5.add_ie(CauseIE(V2.CAUSE_REQUEST_ACCEPTED))
    ubr_res.add_bearer_context(ctx5)
    add("GTPv2 Update Bearer Response", ubr_res.encode())

    # --- Delete Bearer Request (PGW-initiated deactivation) ------------

    dbr = DeleteBearerRequest(teid=0x11111111, seq_num=500)
    dbr.add_ebi(7)   # delete the VoLTE dedicated bearer
    add("GTPv2 Delete Bearer Request", dbr.encode())

    dbr_res = DeleteBearerResponse(teid=0x44444444, seq_num=500)
    dbr_res.set_cause(V2.CAUSE_REQUEST_ACCEPTED)
    ctx6 = BearerContextIE()
    ctx6.add_ie(EBIIE(7))
    ctx6.add_ie(CauseIE(V2.CAUSE_REQUEST_ACCEPTED))
    dbr_res.add_bearer_context(ctx6)
    add("GTPv2 Delete Bearer Response", dbr_res.encode())

    # --- Bearer Resource Command (UE-requested bearer modification) ----

    brc = BearerResourceCommand(teid=0x33333333, seq_num=600)
    brc.set_linked_ebi(5)
    brc.set_pti(2)
    add("GTPv2 Bearer Resource Command", brc.encode())

    # --- Modify Bearer Command / Failure Indication --------------------

    mbc = ModifyBearerCommand(teid=0x33333333, seq_num=700)
    mbc.set_ambr(50_000, 100_000)
    ctx7 = BearerContextIE()
    ctx7.add_ie(EBIIE(5))
    ctx7.add_ie(BearerQoSIE(qci=9, pl=9, mbr_ul=50_000, mbr_dl=100_000))
    mbc.add_bearer_context(ctx7)
    add("GTPv2 Modify Bearer Command", mbc.encode())

    mbfi = ModifyBearerFailureIndication(teid=0x11111111, seq_num=700)
    mbfi.set_cause(V2.CAUSE_NO_RESOURCES)
    add("GTPv2 Modify Bearer Failure Indication", mbfi.encode())

    # --- Delete Bearer Command -----------------------------------------

    dbc = DeleteBearerCommand(teid=0x33333333, seq_num=800)
    ctx8 = BearerContextIE()
    ctx8.add_ie(EBIIE(7))
    dbc.add_bearer_context(ctx8)
    add("GTPv2 Delete Bearer Command", dbc.encode())

    # --- Release Access Bearers (UE goes to ECM-IDLE) -----------------

    rab_req = ReleaseAccessBearersRequest(teid=0x33333333, seq_num=900)
    rab_req.add_ebi(5)
    rab_req.set_node_type(V2.NODE_TYPE_MME)
    add("GTPv2 Release Access Bearers Request", rab_req.encode())

    rab_res = ReleaseAccessBearersResponse(teid=0x11111111, seq_num=900)
    rab_res.set_cause(V2.CAUSE_REQUEST_ACCEPTED)
    rab_res.set_recovery(0)
    add("GTPv2 Release Access Bearers Response", rab_res.encode())

    # --- Downlink Data Notification (paging trigger) ------------------

    ddn = DownlinkDataNotification(teid=0x11111111, seq_num=1000)
    ddn.set_ebi(5)
    ddn.set_cause(V2.CAUSE_REQUEST_ACCEPTED)
    ddn.set_arp(ARPIE(pl=9, pci=False, pvi=False))
    add("GTPv2 Downlink Data Notification", ddn.encode())

    ddn_ack = DownlinkDataNotificationAcknowledge(teid=0x33333333, seq_num=1000)
    ddn_ack.set_cause(V2.CAUSE_REQUEST_ACCEPTED)
    add("GTPv2 Downlink Data Notification Acknowledge", ddn_ack.encode())

    # --- Mobility: Context Request / Response / Acknowledge -----------

    ctx_req = ContextRequest(teid=0, seq_num=1100)
    ctx_req.set_imsi("272030100000000")
    ctx_req.set_rat_type(V2.RAT_EUTRAN)
    ctx_req.set_serving_network("272", "03")
    ctx_req.set_sender_fteid(FTEIDIE(V2.FTEID_S10_MME, teid=0xEEEEEEEE, ipv4="10.1.0.1"))
    add("GTPv2 Context Request", ctx_req.encode())

    ctx_res = ContextResponse(teid=0xEEEEEEEE, seq_num=1100)
    ctx_res.set_cause(V2.CAUSE_REQUEST_ACCEPTED)
    ctx_res.set_imsi("272030100000000")
    ctx_res.set_sender_fteid(FTEIDIE(V2.FTEID_S10_MME, teid=0xFFFFFFFF, ipv4="10.1.1.1"))
    add("GTPv2 Context Response", ctx_res.encode())

    ctx_ack = ContextAcknowledge(teid=0xFFFFFFFF, seq_num=1100)
    ctx_ack.set_cause(V2.CAUSE_REQUEST_ACCEPTED)
    add("GTPv2 Context Acknowledge", ctx_ack.encode())

    # --- Forward Relocation (S10 inter-MME handover) ------------------

    fwd_req = V2ForwardRelocationRequest(teid=0, seq_num=1200)
    fwd_req.set_imsi("272030100000000")
    fwd_req.set_sender_fteid(FTEIDIE(V2.FTEID_S10_MME, teid=0xAAAAAAAA, ipv4="10.1.0.1"))
    fwd_req.set_rat_type(V2.RAT_EUTRAN)
    fwd_req.add_bearer_context(bearer_ctx(
        ebi=5, interface_type=V2.FTEID_S1U_SGW,
        teid=0x55556666, ipv4="10.0.3.1",
    ))
    add("GTPv2 Forward Relocation Request", fwd_req.encode())

    fwd_res = V2ForwardRelocationResponse(teid=0xAAAAAAAA, seq_num=1200)
    fwd_res.set_cause(V2.CAUSE_REQUEST_ACCEPTED)
    fwd_res.set_sender_fteid(FTEIDIE(V2.FTEID_S10_MME, teid=0xBBBBBBBB, ipv4="10.1.1.1"))
    add("GTPv2 Forward Relocation Response", fwd_res.encode())

    fwd_cn = ForwardRelocationCompleteNotification(teid=0xAAAAAAAA, seq_num=1201)
    add("GTPv2 Forward Relocation Complete Notification", fwd_cn.encode())

    fwd_ca = ForwardRelocationCompleteAcknowledge(teid=0xBBBBBBBB, seq_num=1201)
    fwd_ca.set_cause(V2.CAUSE_REQUEST_ACCEPTED)
    add("GTPv2 Forward Relocation Complete Acknowledge", fwd_ca.encode())

    # --- Detach (MME-initiated) ----------------------------------------

    detach_n = DetachNotification(teid=0x33333333, seq_num=1300)
    add("GTPv2 Detach Notification", detach_n.encode())

    detach_a = DetachAcknowledge(teid=0x11111111, seq_num=1300)
    detach_a.set_cause(V2.CAUSE_REQUEST_ACCEPTED)
    add("GTPv2 Detach Acknowledge", detach_a.encode())

    # --- Suspend / Resume (CSFB / SRVCC) --------------------------------

    suspend_n = SuspendNotification(teid=0x33333333, seq_num=1400)
    suspend_n.set_imsi("272030100000000")
    add("GTPv2 Suspend Notification", suspend_n.encode())

    suspend_a = SuspendAcknowledge(teid=0x11111111, seq_num=1400)
    suspend_a.set_cause(V2.CAUSE_REQUEST_ACCEPTED)
    add("GTPv2 Suspend Acknowledge", suspend_a.encode())

    resume_n = ResumeNotification(teid=0x33333333, seq_num=1500)
    resume_n.set_imsi("272030100000000")
    add("GTPv2 Resume Notification", resume_n.encode())

    resume_a = ResumeAcknowledge(teid=0x11111111, seq_num=1500)
    resume_a.set_cause(V2.CAUSE_REQUEST_ACCEPTED)
    add("GTPv2 Resume Acknowledge", resume_a.encode())

    # --- PGW Restart Notification (S11 interface) ----------------------

    pgw_rn = PGWRestartNotification(teid=None, seq_num=1600)
    pgw_rn.set_pgw_s5s8_ip("10.0.1.1")
    pgw_rn.set_sgw_s11s4_ip("10.0.2.1")
    add("GTPv2 PGW Restart Notification", pgw_rn.encode())

    pgw_ra = PGWRestartNotificationAcknowledge(teid=None, seq_num=1600)
    pgw_ra.set_cause(V2.CAUSE_REQUEST_ACCEPTED)
    add("GTPv2 PGW Restart Notification Acknowledge", pgw_ra.encode())

    # --- Stop Paging Indication -----------------------------------------

    stop_paging = StopPagingIndication(teid=None, seq_num=1700)
    stop_paging.set_imsi("272030100000000")
    add("GTPv2 Stop Paging Indication", stop_paging.encode())

    # --- Delete PDN Connection Set (S11 interface) ----------------------

    del_pdn = DeletePDNConnectionSetRequest(teid=None, seq_num=1800)
    del_pdn.set_mme_fq_csid(FQCSIDIe(
        node_id=ip4("10.0.0.1"), csids=[0x1234], instance=0
    ))
    add("GTPv2 Delete PDN Connection Set Request", del_pdn.encode())

    # --- Modify Access Bearers (SGW-initiated) -------------------------

    mab_req = ModifyAccessBearersRequest(teid=0x33333333, seq_num=1900)
    mab_req.set_sender_fteid(FTEIDIE(V2.FTEID_S11S4_SGW, teid=0x33333333, ipv4="10.0.2.1"))
    ctx9 = BearerContextIE()
    ctx9.add_ie(EBIIE(5))
    ctx9.add_ie(FTEIDIE(V2.FTEID_S1U_SGW, teid=0x55556666, ipv4="10.0.3.1"))
    mab_req.add_bearer_context_to_modify(ctx9)
    add("GTPv2 Modify Access Bearers Request", mab_req.encode())

    mab_res = ModifyAccessBearersResponse(teid=0x11111111, seq_num=1900)
    mab_res.set_cause(V2.CAUSE_REQUEST_ACCEPTED)
    mab_res.set_recovery(0)
    add("GTPv2 Modify Access Bearers Response", mab_res.encode())

    # --- MBMS Session Start / Stop ------------------------------------

    mbms_req = V2MBMSSessionStartRequest(teid=None, seq_num=2000)
    mbms_req.set_sender_fteid(FTEIDIE(V2.FTEID_SM_MBMS_GW, teid=0x0A0A0A0A, ipv4="10.10.10.1"))
    mbms_req.set_tmgi(b"\x00\x00\x01\x02\xf2\x30")
    mbms_req.set_mbms_session_id(b"\x01")
    mbms_req.set_mbms_service_area(b"\x00\x01\x00\x01")
    mbms_req.set_ambr(10_000, 10_000)
    add("GTPv2 MBMS Session Start Request", mbms_req.encode())

    mbms_stop = V2MBMSSessionStopRequest(teid=None, seq_num=2100)
    mbms_stop.set_tmgi(b"\x00\x00\x01\x02\xf2\x30")
    mbms_stop.set_mbms_flow_id(b"\x00\x01")
    add("GTPv2 MBMS Session Stop Request", mbms_stop.encode())

    # --- Trace Session Activation (O&M) --------------------------------

    trace_act = TraceSessionActivation(teid=0x33333333, seq_num=9999)
    trace_act.set_imsi("272030100000000")
    trace_act.set_trace_info(b"\x02\x72\x03" + b"\xff\xff" + b"\x00\x00\x00\x00" + b"\x01")
    add("GTPv2 Trace Session Activation", trace_act.encode())

    return samples


# ---------------------------------------------------------------------------
# Write hex file
# ---------------------------------------------------------------------------

def write_hex_file(samples: list[tuple[str, bytes]], path: Path) -> None:
    lines = ["# GTP-C sample packets — generated by examples/generate_samples.py",
             f"# {len(samples)} packets total",
             ""]
    for desc, raw in samples:
        lines.append(f"# {desc}")
        lines.append(raw.hex())
        lines.append("")
    path.write_text("\n".join(lines))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "sample_packets.hex"
    out.parent.mkdir(parents=True, exist_ok=True)

    print("Building packets...")
    samples = build_samples()

    write_hex_file(samples, out)
    print(f"Wrote {len(samples)} packets to {out}")

    # Print a summary table
    v1_count = sum(1 for d, _ in samples if d.startswith("GTPv1"))
    v2_count = sum(1 for d, _ in samples if d.startswith("GTPv2"))
    total_bytes = sum(len(r) for _, r in samples)

    print()
    print(f"  GTPv1-C packets : {v1_count}")
    print(f"  GTPv2-C packets : {v2_count}")
    print(f"  Total bytes     : {total_bytes}")
    print()

    # Verify every packet round-trips cleanly
    from gtpc.v1.messages import decode_message as v1_decode
    from gtpc.v2.messages import decode_message as v2_decode

    errors = 0
    for desc, raw in samples:
        try:
            if desc.startswith("GTPv1"):
                msg = v1_decode(raw)
            else:
                msg = v2_decode(raw)
            reenc = msg.encode()
            if reenc != raw:
                print(f"  [MISMATCH] {desc}")
                print(f"    original : {raw.hex()}")
                print(f"    re-encode: {reenc.hex()}")
                errors += 1
        except Exception as e:
            print(f"  [ERROR] {desc}: {e}")
            errors += 1

    if errors == 0:
        print(f"All {len(samples)} packets verified (encode → decode → re-encode round-trip OK)")
    else:
        print(f"{errors} packet(s) failed verification")


if __name__ == "__main__":
    main()
