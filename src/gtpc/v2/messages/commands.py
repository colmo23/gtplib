"""GTPv2-C bearer resource command messages."""

from gtpc.v2.messages.base import GTPv2Message
from gtpc.v2.ie.typed import CauseIE, EBIIE, BearerContextIE, BearerQoSIE, BearerTFTIE
from gtpc.v2 import constants as C


class ModifyBearerCommand(GTPv2Message):
    msg_type = C.MSG_MODIFY_BEARER_CMD

    def set_ambr(self, uplink_kbps: int, downlink_kbps: int) -> "ModifyBearerCommand":
        from gtpc.v2.ie.typed import AMBRIE
        self.add_ie(AMBRIE(uplink_kbps, downlink_kbps))
        return self

    def add_bearer_context(self, ctx: BearerContextIE) -> "ModifyBearerCommand":
        self.add_ie(ctx)
        return self


class ModifyBearerFailureIndication(GTPv2Message):
    msg_type = C.MSG_MODIFY_BEARER_FAIL

    def set_cause(self, cause: int) -> "ModifyBearerFailureIndication":
        self.add_ie(CauseIE(cause))
        return self

    def add_bearer_context(self, ctx: BearerContextIE) -> "ModifyBearerFailureIndication":
        self.add_ie(ctx)
        return self


class DeleteBearerCommand(GTPv2Message):
    msg_type = C.MSG_DELETE_BEARER_CMD

    def add_bearer_context(self, ctx: BearerContextIE) -> "DeleteBearerCommand":
        self.add_ie(ctx)
        return self


class DeleteBearerFailureIndication(GTPv2Message):
    msg_type = C.MSG_DELETE_BEARER_FAIL

    def set_cause(self, cause: int) -> "DeleteBearerFailureIndication":
        self.add_ie(CauseIE(cause))
        return self

    def add_bearer_context(self, ctx: BearerContextIE) -> "DeleteBearerFailureIndication":
        self.add_ie(ctx)
        return self


class BearerResourceCommand(GTPv2Message):
    msg_type = C.MSG_BEARER_RESOURCE_CMD

    def set_linked_ebi(self, ebi: int) -> "BearerResourceCommand":
        self.add_ie(EBIIE(ebi))
        return self

    def set_pti(self, pti: int) -> "BearerResourceCommand":
        from gtpc.v2.ie.typed import PTIIE
        self.add_ie(PTIIE(pti))
        return self

    def set_tad(self, data: bytes) -> "BearerResourceCommand":
        from gtpc.v2.ie.base import IEv2
        from gtpc.v2 import constants as C
        ie = IEv2.__new__(IEv2)
        ie.ie_type = C.IE_TAD
        ie.instance = 0
        ie.value = data
        self.add_ie(ie)
        return self

    def set_flow_qos(self, qos: "BearerQoSIE") -> "BearerResourceCommand":
        self.add_ie(qos)
        return self


class BearerResourceFailureIndication(GTPv2Message):
    msg_type = C.MSG_BEARER_RESOURCE_FAIL

    def set_cause(self, cause: int) -> "BearerResourceFailureIndication":
        self.add_ie(CauseIE(cause))
        return self

    def set_pti(self, pti: int) -> "BearerResourceFailureIndication":
        from gtpc.v2.ie.typed import PTIIE
        self.add_ie(PTIIE(pti))
        return self

    def set_linked_ebi(self, ebi: int) -> "BearerResourceFailureIndication":
        self.add_ie(EBIIE(ebi))
        return self


class DownlinkDataNotificationFailureIndication(GTPv2Message):
    msg_type = C.MSG_DL_DATA_NOTIF_FAIL

    def set_cause(self, cause: int) -> "DownlinkDataNotificationFailureIndication":
        self.add_ie(CauseIE(cause))
        return self


class TraceSessionActivation(GTPv2Message):
    msg_type = C.MSG_TRACE_SESSION_ACT

    def set_imsi(self, digits: str) -> "TraceSessionActivation":
        from gtpc.v2.ie.typed import IMSIIE
        self.add_ie(IMSIIE(digits))
        return self

    def set_trace_info(self, data: bytes) -> "TraceSessionActivation":
        from gtpc.v2.ie.base import IEv2
        ie = IEv2.__new__(IEv2)
        ie.ie_type = C.IE_TRACE_INFO
        ie.instance = 0
        ie.value = data
        self.add_ie(ie)
        return self


class TraceSessionDeactivation(GTPv2Message):
    msg_type = C.MSG_TRACE_SESSION_DEACT

    def set_trace_reference(self, data: bytes) -> "TraceSessionDeactivation":
        from gtpc.v2.ie.base import IEv2
        ie = IEv2.__new__(IEv2)
        ie.ie_type = C.IE_TRACE_REFERENCE
        ie.instance = 0
        ie.value = data
        self.add_ie(ie)
        return self


class StopPagingIndication(GTPv2Message):
    msg_type = C.MSG_STOP_PAGING_INDICATION

    def set_imsi(self, digits: str) -> "StopPagingIndication":
        from gtpc.v2.ie.typed import IMSIIE
        self.add_ie(IMSIIE(digits))
        return self
