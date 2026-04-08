"""Message type → class registry and top-level decode for GTPv1-C."""

from gtpc.v1.messages.base import GTPv1Message
from gtpc.v1.header import GTPv1Header
from gtpc.v1.ie.base import decode_ies
from gtpc.v1 import constants as C

# Import all message classes
from gtpc.v1.messages.path import EchoRequest, EchoResponse, VersionNotSupported
from gtpc.v1.messages.tunnel import (
    CreatePDPContextRequest, CreatePDPContextResponse,
    UpdatePDPContextRequest, UpdatePDPContextResponse,
    DeletePDPContextRequest, DeletePDPContextResponse,
    InitiatePDPContextActivationRequest, InitiatePDPContextActivationResponse,
)
from gtpc.v1.messages.notification import (
    ErrorIndication,
    PDUNotificationRequest, PDUNotificationResponse,
    PDUNotificationRejectRequest, PDUNotificationRejectResponse,
    SupportedExtensionHeadersNotification,
)
from gtpc.v1.messages.location import (
    SendRoutingInfoForGPRSRequest, SendRoutingInfoForGPRSResponse,
    FailureReportRequest, FailureReportResponse,
    NoteMSGPRSPresentRequest, NoteMSGPRSPresentResponse,
)
from gtpc.v1.messages.mobility import (
    IdentificationRequest, IdentificationResponse,
    SGSNContextRequest, SGSNContextResponse, SGSNContextAcknowledge,
    ForwardRelocationRequest, ForwardRelocationResponse,
    ForwardRelocationComplete, ForwardRelocationCompleteAcknowledge,
    RelocationCancelRequest, RelocationCancelResponse,
    ForwardSRNSContext, ForwardSRNSContextAcknowledge,
    UERegistrationQueryRequest, UERegistrationQueryResponse,
    RANInformationRelay,
)
from gtpc.v1.messages.mbms import (
    MBMSNotificationRequest, MBMSNotificationResponse,
    MBMSNotificationRejectRequest, MBMSNotificationRejectResponse,
    CreateMBMSContextRequest, CreateMBMSContextResponse,
    UpdateMBMSContextRequest, UpdateMBMSContextResponse,
    DeleteMBMSContextRequest, DeleteMBMSContextResponse,
    MBMSRegistrationRequest, MBMSRegistrationResponse,
    MBMSDeRegistrationRequest, MBMSDeRegistrationResponse,
    MBMSSessionStartRequest, MBMSSessionStartResponse,
    MBMSSessionStopRequest, MBMSSessionStopResponse,
    MBMSSessionUpdateRequest, MBMSSessionUpdateResponse,
)
from gtpc.v1.messages.cdr import DataRecordTransferRequest, DataRecordTransferResponse

MSG_REGISTRY: dict[int, type[GTPv1Message]] = {
    C.MSG_ECHO_REQ:                         EchoRequest,
    C.MSG_ECHO_RES:                         EchoResponse,
    C.MSG_VERSION_NOT_SUPPORTED:            VersionNotSupported,
    C.MSG_CREATE_PDP_CTX_REQ:              CreatePDPContextRequest,
    C.MSG_CREATE_PDP_CTX_RES:              CreatePDPContextResponse,
    C.MSG_UPDATE_PDP_CTX_REQ:              UpdatePDPContextRequest,
    C.MSG_UPDATE_PDP_CTX_RES:              UpdatePDPContextResponse,
    C.MSG_DELETE_PDP_CTX_REQ:              DeletePDPContextRequest,
    C.MSG_DELETE_PDP_CTX_RES:              DeletePDPContextResponse,
    C.MSG_INIT_PDP_CTX_ACT_REQ:            InitiatePDPContextActivationRequest,
    C.MSG_INIT_PDP_CTX_ACT_RES:            InitiatePDPContextActivationResponse,
    C.MSG_ERROR_INDICATION:                 ErrorIndication,
    C.MSG_PDU_NOTIFICATION_REQ:            PDUNotificationRequest,
    C.MSG_PDU_NOTIFICATION_RES:            PDUNotificationResponse,
    C.MSG_PDU_NOTIFICATION_REJECT_REQ:     PDUNotificationRejectRequest,
    C.MSG_PDU_NOTIFICATION_REJECT_RES:     PDUNotificationRejectResponse,
    C.MSG_SUPPORTED_EXT_HEADER_NOTIFY:     SupportedExtensionHeadersNotification,
    C.MSG_SEND_ROUTING_INFO_GPRS_REQ:      SendRoutingInfoForGPRSRequest,
    C.MSG_SEND_ROUTING_INFO_GPRS_RES:      SendRoutingInfoForGPRSResponse,
    C.MSG_FAILURE_REPORT_REQ:              FailureReportRequest,
    C.MSG_FAILURE_REPORT_RES:              FailureReportResponse,
    C.MSG_NOTE_MS_GPRS_PRESENT_REQ:        NoteMSGPRSPresentRequest,
    C.MSG_NOTE_MS_GPRS_PRESENT_RES:        NoteMSGPRSPresentResponse,
    C.MSG_IDENTIFICATION_REQ:              IdentificationRequest,
    C.MSG_IDENTIFICATION_RES:              IdentificationResponse,
    C.MSG_SGSN_CTX_REQ:                    SGSNContextRequest,
    C.MSG_SGSN_CTX_RES:                    SGSNContextResponse,
    C.MSG_SGSN_CTX_ACK:                    SGSNContextAcknowledge,
    C.MSG_FORWARD_RELOC_REQ:               ForwardRelocationRequest,
    C.MSG_FORWARD_RELOC_RES:               ForwardRelocationResponse,
    C.MSG_FORWARD_RELOC_COMPLETE:          ForwardRelocationComplete,
    C.MSG_FORWARD_RELOC_COMPLETE_ACK:      ForwardRelocationCompleteAcknowledge,
    C.MSG_RELOC_CANCEL_REQ:                RelocationCancelRequest,
    C.MSG_RELOC_CANCEL_RES:                RelocationCancelResponse,
    C.MSG_FORWARD_SRNS_CTX:                ForwardSRNSContext,
    C.MSG_FORWARD_SRNS_CTX_ACK:            ForwardSRNSContextAcknowledge,
    C.MSG_UE_REGIST_QUERY_REQ:             UERegistrationQueryRequest,
    C.MSG_UE_REGIST_QUERY_RES:             UERegistrationQueryResponse,
    C.MSG_RAN_INFORMATION_RELAY:           RANInformationRelay,
    C.MSG_MBMS_NOTIFICATION_REQ:           MBMSNotificationRequest,
    C.MSG_MBMS_NOTIFICATION_RES:           MBMSNotificationResponse,
    C.MSG_MBMS_NOTIFICATION_REJECT_REQ:    MBMSNotificationRejectRequest,
    C.MSG_MBMS_NOTIFICATION_REJECT_RES:    MBMSNotificationRejectResponse,
    C.MSG_CREATE_MBMS_CTX_REQ:             CreateMBMSContextRequest,
    C.MSG_CREATE_MBMS_CTX_RES:             CreateMBMSContextResponse,
    C.MSG_UPDATE_MBMS_CTX_REQ:             UpdateMBMSContextRequest,
    C.MSG_UPDATE_MBMS_CTX_RES:             UpdateMBMSContextResponse,
    C.MSG_DELETE_MBMS_CTX_REQ:             DeleteMBMSContextRequest,
    C.MSG_DELETE_MBMS_CTX_RES:             DeleteMBMSContextResponse,
    C.MSG_MBMS_REGIST_REQ:                 MBMSRegistrationRequest,
    C.MSG_MBMS_REGIST_RES:                 MBMSRegistrationResponse,
    C.MSG_MBMS_DEREGIST_REQ:               MBMSDeRegistrationRequest,
    C.MSG_MBMS_DEREGIST_RES:               MBMSDeRegistrationResponse,
    C.MSG_MBMS_SESSION_START_REQ:          MBMSSessionStartRequest,
    C.MSG_MBMS_SESSION_START_RES:          MBMSSessionStartResponse,
    C.MSG_MBMS_SESSION_STOP_REQ:           MBMSSessionStopRequest,
    C.MSG_MBMS_SESSION_STOP_RES:           MBMSSessionStopResponse,
    C.MSG_MBMS_SESSION_UPDATE_REQ:         MBMSSessionUpdateRequest,
    C.MSG_MBMS_SESSION_UPDATE_RES:         MBMSSessionUpdateResponse,
    C.MSG_DATA_RECORD_TRANSFER_REQ:        DataRecordTransferRequest,
    C.MSG_DATA_RECORD_TRANSFER_RES:        DataRecordTransferResponse,
}


def decode_message(buf: bytes) -> GTPv1Message:
    """Decode a GTPv1-C packet from raw bytes.

    Returns the most specific message class available, falling back to
    GTPv1Message for unknown types.
    """
    if len(buf) < 8:
        raise ValueError(f"Buffer too short for GTPv1 header: {len(buf)} bytes")
    hdr, offset = GTPv1Header.decode(buf)
    body = buf[offset:]
    klass = MSG_REGISTRY.get(hdr.msg_type, GTPv1Message)
    obj = klass.__new__(klass)
    obj.header = hdr
    obj.ies = decode_ies(body)
    return obj
