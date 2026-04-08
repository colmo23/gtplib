"""Message type → class registry and top-level decode for GTPv2-C."""

from gtpc.v2.messages.base import GTPv2Message
from gtpc.v2.header import GTPv2Header
from gtpc.v2.ie.base import decode_ies
from gtpc.v2 import constants as C

from gtpc.v2.messages.path import EchoRequest, EchoResponse, VersionNotSupported
from gtpc.v2.messages.session import (
    CreateSessionRequest, CreateSessionResponse,
    ModifyBearerRequest, ModifyBearerResponse,
    DeleteSessionRequest, DeleteSessionResponse,
    ChangeNotificationRequest, ChangeNotificationResponse,
    RemoteUEReportNotification, RemoteUEReportAcknowledge,
)
from gtpc.v2.messages.bearer import (
    CreateBearerRequest, CreateBearerResponse,
    UpdateBearerRequest, UpdateBearerResponse,
    DeleteBearerRequest, DeleteBearerResponse,
    DeletePDNConnectionSetRequest, DeletePDNConnectionSetResponse,
    PGWDownlinkTriggeringNotification, PGWDownlinkTriggeringAcknowledge,
)
from gtpc.v2.messages.commands import (
    ModifyBearerCommand, ModifyBearerFailureIndication,
    DeleteBearerCommand, DeleteBearerFailureIndication,
    BearerResourceCommand, BearerResourceFailureIndication,
    DownlinkDataNotificationFailureIndication,
    TraceSessionActivation, TraceSessionDeactivation,
    StopPagingIndication,
)
from gtpc.v2.messages.mobility import (
    IdentificationRequest, IdentificationResponse,
    ContextRequest, ContextResponse, ContextAcknowledge,
    ForwardRelocationRequest, ForwardRelocationResponse,
    ForwardRelocationCompleteNotification, ForwardRelocationCompleteAcknowledge,
    ForwardAccessContextNotification, ForwardAccessContextAcknowledge,
    RelocationCancelRequest, RelocationCancelResponse,
    ConfigurationTransferTunnel,
)
from gtpc.v2.messages.notification import (
    DetachNotification, DetachAcknowledge,
    CSPagingIndication, RANInformationRelay,
    AlertMMENotification, AlertMMEAcknowledge,
    UEActivityNotification, UEActivityAcknowledge,
    ISRStatusIndication,
    UERegistrationQueryRequest, UERegistrationQueryResponse,
    SuspendNotification, SuspendAcknowledge,
    ResumeNotification, ResumeAcknowledge,
    PGWRestartNotification, PGWRestartNotificationAcknowledge,
)
from gtpc.v2.messages.forwarding import (
    CreateForwardingTunnelRequest, CreateForwardingTunnelResponse,
    CreateIndirectDataForwardingTunnelRequest,
    CreateIndirectDataForwardingTunnelResponse,
    DeleteIndirectDataForwardingTunnelRequest,
    DeleteIndirectDataForwardingTunnelResponse,
    ReleaseAccessBearersRequest, ReleaseAccessBearersResponse,
    DownlinkDataNotification, DownlinkDataNotificationAcknowledge,
)
from gtpc.v2.messages.pdn import (
    UpdatePDNConnectionSetRequest, UpdatePDNConnectionSetResponse,
    ModifyAccessBearersRequest, ModifyAccessBearersResponse,
)
from gtpc.v2.messages.mbms import (
    MBMSSessionStartRequest, MBMSSessionStartResponse,
    MBMSSessionUpdateRequest, MBMSSessionUpdateResponse,
    MBMSSessionStopRequest, MBMSSessionStopResponse,
)

MSG_REGISTRY: dict[int, type[GTPv2Message]] = {
    C.MSG_ECHO_REQ:                                 EchoRequest,
    C.MSG_ECHO_RES:                                 EchoResponse,
    C.MSG_VERSION_NOT_SUPPORTED:                    VersionNotSupported,
    C.MSG_CREATE_SESSION_REQ:                       CreateSessionRequest,
    C.MSG_CREATE_SESSION_RES:                       CreateSessionResponse,
    C.MSG_MODIFY_BEARER_REQ:                        ModifyBearerRequest,
    C.MSG_MODIFY_BEARER_RES:                        ModifyBearerResponse,
    C.MSG_DELETE_SESSION_REQ:                       DeleteSessionRequest,
    C.MSG_DELETE_SESSION_RES:                       DeleteSessionResponse,
    C.MSG_CHANGE_NOTIFICATION_REQ:                  ChangeNotificationRequest,
    C.MSG_CHANGE_NOTIFICATION_RES:                  ChangeNotificationResponse,
    C.MSG_REMOTE_UE_REPORT_NOTIFY:                 RemoteUEReportNotification,
    C.MSG_REMOTE_UE_REPORT_ACK:                    RemoteUEReportAcknowledge,
    C.MSG_MODIFY_BEARER_CMD:                        ModifyBearerCommand,
    C.MSG_MODIFY_BEARER_FAIL:                       ModifyBearerFailureIndication,
    C.MSG_DELETE_BEARER_CMD:                        DeleteBearerCommand,
    C.MSG_DELETE_BEARER_FAIL:                       DeleteBearerFailureIndication,
    C.MSG_BEARER_RESOURCE_CMD:                      BearerResourceCommand,
    C.MSG_BEARER_RESOURCE_FAIL:                     BearerResourceFailureIndication,
    C.MSG_DL_DATA_NOTIF_FAIL:                       DownlinkDataNotificationFailureIndication,
    C.MSG_TRACE_SESSION_ACT:                        TraceSessionActivation,
    C.MSG_TRACE_SESSION_DEACT:                      TraceSessionDeactivation,
    C.MSG_STOP_PAGING_INDICATION:                   StopPagingIndication,
    C.MSG_CREATE_BEARER_REQ:                        CreateBearerRequest,
    C.MSG_CREATE_BEARER_RES:                        CreateBearerResponse,
    C.MSG_UPDATE_BEARER_REQ:                        UpdateBearerRequest,
    C.MSG_UPDATE_BEARER_RES:                        UpdateBearerResponse,
    C.MSG_DELETE_BEARER_REQ:                        DeleteBearerRequest,
    C.MSG_DELETE_BEARER_RES:                        DeleteBearerResponse,
    C.MSG_DELETE_PDN_CONN_SET_REQ:                  DeletePDNConnectionSetRequest,
    C.MSG_DELETE_PDN_CONN_SET_RES:                  DeletePDNConnectionSetResponse,
    C.MSG_PGW_DL_TRIGGER_NOTIFY:                   PGWDownlinkTriggeringNotification,
    C.MSG_PGW_DL_TRIGGER_ACK:                      PGWDownlinkTriggeringAcknowledge,
    C.MSG_IDENTIFICATION_REQ:                       IdentificationRequest,
    C.MSG_IDENTIFICATION_RES:                       IdentificationResponse,
    C.MSG_CONTEXT_REQ:                              ContextRequest,
    C.MSG_CONTEXT_RES:                              ContextResponse,
    C.MSG_CONTEXT_ACK:                              ContextAcknowledge,
    C.MSG_FORWARD_RELOC_REQ:                        ForwardRelocationRequest,
    C.MSG_FORWARD_RELOC_RES:                        ForwardRelocationResponse,
    C.MSG_FORWARD_RELOC_COMPLETE_NOTIFY:            ForwardRelocationCompleteNotification,
    C.MSG_FORWARD_RELOC_COMPLETE_ACK:               ForwardRelocationCompleteAcknowledge,
    C.MSG_FORWARD_ACCESS_CONTEXT_NOTIFY:            ForwardAccessContextNotification,
    C.MSG_FORWARD_ACCESS_CONTEXT_ACK:               ForwardAccessContextAcknowledge,
    C.MSG_RELOC_CANCEL_REQ:                         RelocationCancelRequest,
    C.MSG_RELOC_CANCEL_RES:                         RelocationCancelResponse,
    C.MSG_CONFIG_TRANSFER_TUNNEL:                   ConfigurationTransferTunnel,
    C.MSG_DETACH_NOTIFY:                            DetachNotification,
    C.MSG_DETACH_ACK:                               DetachAcknowledge,
    C.MSG_CS_PAGING_INDICATION:                     CSPagingIndication,
    C.MSG_RAN_INFO_RELAY:                           RANInformationRelay,
    C.MSG_ALERT_MME_NOTIFY:                         AlertMMENotification,
    C.MSG_ALERT_MME_ACK:                            AlertMMEAcknowledge,
    C.MSG_UE_ACTIVITY_NOTIFY:                       UEActivityNotification,
    C.MSG_UE_ACTIVITY_ACK:                          UEActivityAcknowledge,
    C.MSG_ISR_STATUS_INDICATION:                    ISRStatusIndication,
    C.MSG_UE_REGIST_QUERY_REQ:                      UERegistrationQueryRequest,
    C.MSG_UE_REGIST_QUERY_RES:                      UERegistrationQueryResponse,
    C.MSG_CREATE_FORWARDING_TUNNEL_REQ:             CreateForwardingTunnelRequest,
    C.MSG_CREATE_FORWARDING_TUNNEL_RES:             CreateForwardingTunnelResponse,
    C.MSG_SUSPEND_NOTIFY:                           SuspendNotification,
    C.MSG_SUSPEND_ACK:                              SuspendAcknowledge,
    C.MSG_RESUME_NOTIFY:                            ResumeNotification,
    C.MSG_RESUME_ACK:                               ResumeAcknowledge,
    C.MSG_CREATE_INDIRECT_DATA_FWD_TUNNEL_REQ:      CreateIndirectDataForwardingTunnelRequest,
    C.MSG_CREATE_INDIRECT_DATA_FWD_TUNNEL_RES:      CreateIndirectDataForwardingTunnelResponse,
    C.MSG_DELETE_INDIRECT_DATA_FWD_TUNNEL_REQ:      DeleteIndirectDataForwardingTunnelRequest,
    C.MSG_DELETE_INDIRECT_DATA_FWD_TUNNEL_RES:      DeleteIndirectDataForwardingTunnelResponse,
    C.MSG_RELEASE_ACCESS_BEARERS_REQ:               ReleaseAccessBearersRequest,
    C.MSG_RELEASE_ACCESS_BEARERS_RES:               ReleaseAccessBearersResponse,
    C.MSG_DL_DATA_NOTIFY:                           DownlinkDataNotification,
    C.MSG_DL_DATA_NOTIFY_ACK:                       DownlinkDataNotificationAcknowledge,
    C.MSG_PGW_RESTART_NOTIFY:                       PGWRestartNotification,
    C.MSG_PGW_RESTART_ACK:                          PGWRestartNotificationAcknowledge,
    C.MSG_UPDATE_PDN_CONN_SET_REQ:                  UpdatePDNConnectionSetRequest,
    C.MSG_UPDATE_PDN_CONN_SET_RES:                  UpdatePDNConnectionSetResponse,
    C.MSG_MODIFY_ACCESS_BEARERS_REQ:                ModifyAccessBearersRequest,
    C.MSG_MODIFY_ACCESS_BEARERS_RES:                ModifyAccessBearersResponse,
    C.MSG_MBMS_SESSION_START_REQ:                   MBMSSessionStartRequest,
    C.MSG_MBMS_SESSION_START_RES:                   MBMSSessionStartResponse,
    C.MSG_MBMS_SESSION_UPDATE_REQ:                  MBMSSessionUpdateRequest,
    C.MSG_MBMS_SESSION_UPDATE_RES:                  MBMSSessionUpdateResponse,
    C.MSG_MBMS_SESSION_STOP_REQ:                    MBMSSessionStopRequest,
    C.MSG_MBMS_SESSION_STOP_RES:                    MBMSSessionStopResponse,
}


def decode_message(buf: bytes) -> GTPv2Message:
    """Decode a GTPv2-C packet from raw bytes.

    Returns the most specific message class, falling back to GTPv2Message.
    """
    if len(buf) < 8:
        raise ValueError(f"Buffer too short for GTPv2 header: {len(buf)} bytes")
    hdr, offset = GTPv2Header.decode(buf)
    body = buf[offset:]
    klass = MSG_REGISTRY.get(hdr.msg_type, GTPv2Message)
    obj = klass.__new__(klass)
    obj.header = hdr
    obj.ies = decode_ies(body)
    return obj
