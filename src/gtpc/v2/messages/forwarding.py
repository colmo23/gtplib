"""GTPv2-C forwarding tunnel and access bearer messages."""

from gtpc.v2.messages.base import GTPv2Message
from gtpc.v2.ie.typed import CauseIE, EBIIE, FTEIDIE, RecoveryIE, IMSIIE
from gtpc.v2 import constants as C


class CreateForwardingTunnelRequest(GTPv2Message):
    msg_type = C.MSG_CREATE_FORWARDING_TUNNEL_REQ

    def set_s103pdf(self, data: bytes) -> "CreateForwardingTunnelRequest":
        from gtpc.v2.ie.base import IEv2
        ie = IEv2.__new__(IEv2)
        ie.ie_type = C.IE_S103PDF; ie.instance = 0; ie.value = data
        self.add_ie(ie)
        return self


class CreateForwardingTunnelResponse(GTPv2Message):
    msg_type = C.MSG_CREATE_FORWARDING_TUNNEL_RES

    def set_cause(self, cause: int) -> "CreateForwardingTunnelResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_s1udf(self, data: bytes) -> "CreateForwardingTunnelResponse":
        from gtpc.v2.ie.base import IEv2
        ie = IEv2.__new__(IEv2)
        ie.ie_type = C.IE_S1UDF; ie.instance = 0; ie.value = data
        self.add_ie(ie)
        return self


class CreateIndirectDataForwardingTunnelRequest(GTPv2Message):
    msg_type = C.MSG_CREATE_INDIRECT_DATA_FWD_TUNNEL_REQ

    def set_imsi(self, digits: str) -> "CreateIndirectDataForwardingTunnelRequest":
        self.add_ie(IMSIIE(digits))
        return self

    def set_sender_fteid(self, fteid: FTEIDIE) -> "CreateIndirectDataForwardingTunnelRequest":
        self.add_ie(fteid)
        return self

    def add_bearer_context(self, ctx) -> "CreateIndirectDataForwardingTunnelRequest":
        self.add_ie(ctx)
        return self


class CreateIndirectDataForwardingTunnelResponse(GTPv2Message):
    msg_type = C.MSG_CREATE_INDIRECT_DATA_FWD_TUNNEL_RES

    def set_cause(self, cause: int) -> "CreateIndirectDataForwardingTunnelResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_recovery(self, rc: int) -> "CreateIndirectDataForwardingTunnelResponse":
        self.add_ie(RecoveryIE(rc))
        return self

    def add_bearer_context(self, ctx) -> "CreateIndirectDataForwardingTunnelResponse":
        self.add_ie(ctx)
        return self


class DeleteIndirectDataForwardingTunnelRequest(GTPv2Message):
    msg_type = C.MSG_DELETE_INDIRECT_DATA_FWD_TUNNEL_REQ


class DeleteIndirectDataForwardingTunnelResponse(GTPv2Message):
    msg_type = C.MSG_DELETE_INDIRECT_DATA_FWD_TUNNEL_RES

    def set_cause(self, cause: int) -> "DeleteIndirectDataForwardingTunnelResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_recovery(self, rc: int) -> "DeleteIndirectDataForwardingTunnelResponse":
        self.add_ie(RecoveryIE(rc))
        return self


class ReleaseAccessBearersRequest(GTPv2Message):
    msg_type = C.MSG_RELEASE_ACCESS_BEARERS_REQ

    def add_ebi(self, ebi: int) -> "ReleaseAccessBearersRequest":
        self.add_ie(EBIIE(ebi))
        return self

    def set_node_type(self, node_type: int) -> "ReleaseAccessBearersRequest":
        from gtpc.v2.ie.typed import NodeTypeIE
        self.add_ie(NodeTypeIE(node_type))
        return self


class ReleaseAccessBearersResponse(GTPv2Message):
    msg_type = C.MSG_RELEASE_ACCESS_BEARERS_RES

    def set_cause(self, cause: int) -> "ReleaseAccessBearersResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_recovery(self, rc: int) -> "ReleaseAccessBearersResponse":
        self.add_ie(RecoveryIE(rc))
        return self

    @property
    def cause(self) -> int | None:
        ie = self.get_ie(C.IE_CAUSE)
        return ie.cause if ie else None


class DownlinkDataNotification(GTPv2Message):
    msg_type = C.MSG_DL_DATA_NOTIFY

    def set_cause(self, cause: int) -> "DownlinkDataNotification":
        self.add_ie(CauseIE(cause))
        return self

    def set_ebi(self, ebi: int) -> "DownlinkDataNotification":
        self.add_ie(EBIIE(ebi))
        return self

    def set_arp(self, arp) -> "DownlinkDataNotification":
        self.add_ie(arp)
        return self

    def set_pgw_fteid(self, fteid: FTEIDIE) -> "DownlinkDataNotification":
        self.add_ie(fteid)
        return self


class DownlinkDataNotificationAcknowledge(GTPv2Message):
    msg_type = C.MSG_DL_DATA_NOTIFY_ACK

    def set_cause(self, cause: int) -> "DownlinkDataNotificationAcknowledge":
        self.add_ie(CauseIE(cause))
        return self

    def set_recovery(self, rc: int) -> "DownlinkDataNotificationAcknowledge":
        self.add_ie(RecoveryIE(rc))
        return self
