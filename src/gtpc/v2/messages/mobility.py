"""GTPv2-C mobility / handover messages."""

from gtpc.v2.messages.base import GTPv2Message
from gtpc.v2.ie.typed import (
    IMSIIE, CauseIE, RecoveryIE, FTEIDIE, BearerContextIE,
    RATTypeIE, ServingNetworkIE, ULIIE, MEIIE,
)
from gtpc.v2 import constants as C


class IdentificationRequest(GTPv2Message):
    msg_type = C.MSG_IDENTIFICATION_REQ

    def set_guti(self, data: bytes) -> "IdentificationRequest":
        from gtpc.v2.ie.base import IEv2
        ie = IEv2.__new__(IEv2)
        ie.ie_type = C.IE_GUTI; ie.instance = 0; ie.value = data
        self.add_ie(ie)
        return self

    def set_rai(self, data: bytes) -> "IdentificationRequest":
        from gtpc.v2.ie.base import IEv2
        ie = IEv2.__new__(IEv2)
        ie.ie_type = C.IE_P_TMSI; ie.instance = 0; ie.value = data
        self.add_ie(ie)
        return self

    def set_ptmsi(self, data: bytes) -> "IdentificationRequest":
        from gtpc.v2.ie.base import IEv2
        ie = IEv2.__new__(IEv2)
        ie.ie_type = C.IE_P_TMSI; ie.instance = 0; ie.value = data
        self.add_ie(ie)
        return self

    def set_sender_fteid(self, fteid: FTEIDIE) -> "IdentificationRequest":
        self.add_ie(fteid)
        return self


class IdentificationResponse(GTPv2Message):
    msg_type = C.MSG_IDENTIFICATION_RES

    def set_cause(self, cause: int) -> "IdentificationResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_imsi(self, digits: str) -> "IdentificationResponse":
        self.add_ie(IMSIIE(digits))
        return self

    def set_mei(self, digits: str) -> "IdentificationResponse":
        self.add_ie(MEIIE(digits))
        return self


class ContextRequest(GTPv2Message):
    msg_type = C.MSG_CONTEXT_REQ

    def set_imsi(self, digits: str) -> "ContextRequest":
        self.add_ie(IMSIIE(digits))
        return self

    def set_rai(self, data: bytes) -> "ContextRequest":
        from gtpc.v2.ie.base import IEv2
        ie = IEv2.__new__(IEv2)
        ie.ie_type = C.IE_P_TMSI; ie.instance = 0; ie.value = data
        self.add_ie(ie)
        return self

    def set_rat_type(self, rat: int) -> "ContextRequest":
        self.add_ie(RATTypeIE(rat))
        return self

    def set_serving_network(self, mcc: str, mnc: str) -> "ContextRequest":
        self.add_ie(ServingNetworkIE(mcc, mnc))
        return self

    def set_sender_fteid(self, fteid: FTEIDIE) -> "ContextRequest":
        self.add_ie(fteid)
        return self


class ContextResponse(GTPv2Message):
    msg_type = C.MSG_CONTEXT_RES

    def set_cause(self, cause: int) -> "ContextResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_imsi(self, digits: str) -> "ContextResponse":
        self.add_ie(IMSIIE(digits))
        return self

    def set_sender_fteid(self, fteid: FTEIDIE) -> "ContextResponse":
        self.add_ie(fteid)
        return self

    def add_bearer_context(self, ctx: BearerContextIE) -> "ContextResponse":
        self.add_ie(ctx)
        return self


class ContextAcknowledge(GTPv2Message):
    msg_type = C.MSG_CONTEXT_ACK

    def set_cause(self, cause: int) -> "ContextAcknowledge":
        self.add_ie(CauseIE(cause))
        return self


class ForwardRelocationRequest(GTPv2Message):
    msg_type = C.MSG_FORWARD_RELOC_REQ

    def set_imsi(self, digits: str) -> "ForwardRelocationRequest":
        self.add_ie(IMSIIE(digits))
        return self

    def set_sender_fteid(self, fteid: FTEIDIE) -> "ForwardRelocationRequest":
        self.add_ie(fteid)
        return self

    def set_rat_type(self, rat: int) -> "ForwardRelocationRequest":
        self.add_ie(RATTypeIE(rat))
        return self

    def add_bearer_context(self, ctx: BearerContextIE) -> "ForwardRelocationRequest":
        self.add_ie(ctx)
        return self


class ForwardRelocationResponse(GTPv2Message):
    msg_type = C.MSG_FORWARD_RELOC_RES

    def set_cause(self, cause: int) -> "ForwardRelocationResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_sender_fteid(self, fteid: FTEIDIE) -> "ForwardRelocationResponse":
        self.add_ie(fteid)
        return self

    def add_bearer_context(self, ctx: BearerContextIE) -> "ForwardRelocationResponse":
        self.add_ie(ctx)
        return self


class ForwardRelocationCompleteNotification(GTPv2Message):
    msg_type = C.MSG_FORWARD_RELOC_COMPLETE_NOTIFY


class ForwardRelocationCompleteAcknowledge(GTPv2Message):
    msg_type = C.MSG_FORWARD_RELOC_COMPLETE_ACK

    def set_cause(self, cause: int) -> "ForwardRelocationCompleteAcknowledge":
        self.add_ie(CauseIE(cause))
        return self


class ForwardAccessContextNotification(GTPv2Message):
    msg_type = C.MSG_FORWARD_ACCESS_CONTEXT_NOTIFY

    def set_f_container(self, data: bytes) -> "ForwardAccessContextNotification":
        from gtpc.v2.ie.base import IEv2
        ie = IEv2.__new__(IEv2)
        ie.ie_type = C.IE_F_CONTAINER; ie.instance = 0; ie.value = data
        self.add_ie(ie)
        return self


class ForwardAccessContextAcknowledge(GTPv2Message):
    msg_type = C.MSG_FORWARD_ACCESS_CONTEXT_ACK

    def set_cause(self, cause: int) -> "ForwardAccessContextAcknowledge":
        self.add_ie(CauseIE(cause))
        return self


class RelocationCancelRequest(GTPv2Message):
    msg_type = C.MSG_RELOC_CANCEL_REQ

    def set_imsi(self, digits: str) -> "RelocationCancelRequest":
        self.add_ie(IMSIIE(digits))
        return self

    def set_mei(self, digits: str) -> "RelocationCancelRequest":
        self.add_ie(MEIIE(digits))
        return self


class RelocationCancelResponse(GTPv2Message):
    msg_type = C.MSG_RELOC_CANCEL_RES

    def set_cause(self, cause: int) -> "RelocationCancelResponse":
        self.add_ie(CauseIE(cause))
        return self


class ConfigurationTransferTunnel(GTPv2Message):
    msg_type = C.MSG_CONFIG_TRANSFER_TUNNEL

    def set_f_container(self, data: bytes) -> "ConfigurationTransferTunnel":
        from gtpc.v2.ie.base import IEv2
        ie = IEv2.__new__(IEv2)
        ie.ie_type = C.IE_F_CONTAINER; ie.instance = 0; ie.value = data
        self.add_ie(ie)
        return self
