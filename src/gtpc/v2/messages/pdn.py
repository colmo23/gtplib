"""GTPv2-C PDN connection set and access bearer messages."""

from gtpc.v2.messages.base import GTPv2Message
from gtpc.v2.ie.typed import CauseIE, RecoveryIE, BearerContextIE, FQCSIDIe, FTEIDIE
from gtpc.v2 import constants as C


class UpdatePDNConnectionSetRequest(GTPv2Message):
    msg_type = C.MSG_UPDATE_PDN_CONN_SET_REQ

    def set_mme_fq_csid(self, csid: FQCSIDIe) -> "UpdatePDNConnectionSetRequest":
        self.add_ie(csid)
        return self

    def set_sgw_fq_csid(self, csid: FQCSIDIe) -> "UpdatePDNConnectionSetRequest":
        csid.instance = 1
        self.add_ie(csid)
        return self


class UpdatePDNConnectionSetResponse(GTPv2Message):
    msg_type = C.MSG_UPDATE_PDN_CONN_SET_RES

    def set_cause(self, cause: int) -> "UpdatePDNConnectionSetResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_pgw_fq_csid(self, csid: FQCSIDIe) -> "UpdatePDNConnectionSetResponse":
        self.add_ie(csid)
        return self

    @property
    def cause(self) -> int | None:
        ie = self.get_ie(C.IE_CAUSE)
        return ie.cause if ie else None


class ModifyAccessBearersRequest(GTPv2Message):
    msg_type = C.MSG_MODIFY_ACCESS_BEARERS_REQ

    def set_sender_fteid(self, fteid: FTEIDIE) -> "ModifyAccessBearersRequest":
        self.add_ie(fteid)
        return self

    def add_bearer_context_to_modify(self, ctx: BearerContextIE) -> "ModifyAccessBearersRequest":
        self.add_ie(ctx)
        return self

    def add_bearer_context_to_remove(self, ctx: BearerContextIE) -> "ModifyAccessBearersRequest":
        ctx.instance = 1
        self.add_ie(ctx)
        return self


class ModifyAccessBearersResponse(GTPv2Message):
    msg_type = C.MSG_MODIFY_ACCESS_BEARERS_RES

    def set_cause(self, cause: int) -> "ModifyAccessBearersResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_recovery(self, rc: int) -> "ModifyAccessBearersResponse":
        self.add_ie(RecoveryIE(rc))
        return self

    def add_bearer_context(self, ctx: BearerContextIE) -> "ModifyAccessBearersResponse":
        self.add_ie(ctx)
        return self

    @property
    def cause(self) -> int | None:
        ie = self.get_ie(C.IE_CAUSE)
        return ie.cause if ie else None
