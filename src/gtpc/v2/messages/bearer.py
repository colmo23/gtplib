"""GTPv2-C bearer management messages."""

from gtpc.v2.messages.base import GTPv2Message
from gtpc.v2.ie.typed import (
    CauseIE, EBIIE, PCOIE, BearerContextIE, FTEIDIE,
    BearerQoSIE, AMBRIE, FQCSIDIe, RecoveryIE,
)
from gtpc.v2 import constants as C


class CreateBearerRequest(GTPv2Message):
    msg_type = C.MSG_CREATE_BEARER_REQ

    def set_pti(self, pti: int) -> "CreateBearerRequest":
        from gtpc.v2.ie.typed import PTIIE
        self.add_ie(PTIIE(pti))
        return self

    def set_linked_ebi(self, ebi: int) -> "CreateBearerRequest":
        self.add_ie(EBIIE(ebi))
        return self

    def set_pco(self, data: bytes) -> "CreateBearerRequest":
        self.add_ie(PCOIE(data))
        return self

    def add_bearer_context(self, ctx: BearerContextIE) -> "CreateBearerRequest":
        self.add_ie(ctx)
        return self

    def set_pgw_fq_csid(self, csid: FQCSIDIe) -> "CreateBearerRequest":
        self.add_ie(csid)
        return self

    def set_ambr(self, uplink_kbps: int, downlink_kbps: int) -> "CreateBearerRequest":
        self.add_ie(AMBRIE(uplink_kbps, downlink_kbps))
        return self


class CreateBearerResponse(GTPv2Message):
    msg_type = C.MSG_CREATE_BEARER_RES

    def set_cause(self, cause: int) -> "CreateBearerResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_recovery(self, rc: int) -> "CreateBearerResponse":
        self.add_ie(RecoveryIE(rc))
        return self

    def add_bearer_context(self, ctx: BearerContextIE) -> "CreateBearerResponse":
        self.add_ie(ctx)
        return self

    def set_pco(self, data: bytes) -> "CreateBearerResponse":
        self.add_ie(PCOIE(data))
        return self

    @property
    def cause(self) -> int | None:
        ie = self.get_ie(C.IE_CAUSE)
        return ie.cause if ie else None


class UpdateBearerRequest(GTPv2Message):
    msg_type = C.MSG_UPDATE_BEARER_REQ

    def set_pco(self, data: bytes) -> "UpdateBearerRequest":
        self.add_ie(PCOIE(data))
        return self

    def add_bearer_context(self, ctx: BearerContextIE) -> "UpdateBearerRequest":
        self.add_ie(ctx)
        return self

    def set_ambr(self, uplink_kbps: int, downlink_kbps: int) -> "UpdateBearerRequest":
        self.add_ie(AMBRIE(uplink_kbps, downlink_kbps))
        return self

    def set_pgw_fq_csid(self, csid: FQCSIDIe) -> "UpdateBearerRequest":
        self.add_ie(csid)
        return self


class UpdateBearerResponse(GTPv2Message):
    msg_type = C.MSG_UPDATE_BEARER_RES

    def set_cause(self, cause: int) -> "UpdateBearerResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_recovery(self, rc: int) -> "UpdateBearerResponse":
        self.add_ie(RecoveryIE(rc))
        return self

    def add_bearer_context(self, ctx: BearerContextIE) -> "UpdateBearerResponse":
        self.add_ie(ctx)
        return self

    def set_pco(self, data: bytes) -> "UpdateBearerResponse":
        self.add_ie(PCOIE(data))
        return self

    @property
    def cause(self) -> int | None:
        ie = self.get_ie(C.IE_CAUSE)
        return ie.cause if ie else None


class DeleteBearerRequest(GTPv2Message):
    msg_type = C.MSG_DELETE_BEARER_REQ

    def set_linked_ebi(self, ebi: int) -> "DeleteBearerRequest":
        self.add_ie(EBIIE(ebi))
        return self

    def add_ebi(self, ebi: int) -> "DeleteBearerRequest":
        self.add_ie(EBIIE(ebi))
        return self

    def add_bearer_context(self, ctx: BearerContextIE) -> "DeleteBearerRequest":
        self.add_ie(ctx)
        return self

    def set_pco(self, data: bytes) -> "DeleteBearerRequest":
        self.add_ie(PCOIE(data))
        return self


class DeleteBearerResponse(GTPv2Message):
    msg_type = C.MSG_DELETE_BEARER_RES

    def set_cause(self, cause: int) -> "DeleteBearerResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_recovery(self, rc: int) -> "DeleteBearerResponse":
        self.add_ie(RecoveryIE(rc))
        return self

    def add_bearer_context(self, ctx: BearerContextIE) -> "DeleteBearerResponse":
        self.add_ie(ctx)
        return self

    def set_pco(self, data: bytes) -> "DeleteBearerResponse":
        self.add_ie(PCOIE(data))
        return self

    @property
    def cause(self) -> int | None:
        ie = self.get_ie(C.IE_CAUSE)
        return ie.cause if ie else None


class DeletePDNConnectionSetRequest(GTPv2Message):
    msg_type = C.MSG_DELETE_PDN_CONN_SET_REQ

    def set_mme_fq_csid(self, csid: FQCSIDIe) -> "DeletePDNConnectionSetRequest":
        self.add_ie(csid)
        return self

    def set_sgw_fq_csid(self, csid: FQCSIDIe) -> "DeletePDNConnectionSetRequest":
        csid.instance = 1
        self.add_ie(csid)
        return self


class DeletePDNConnectionSetResponse(GTPv2Message):
    msg_type = C.MSG_DELETE_PDN_CONN_SET_RES

    def set_cause(self, cause: int) -> "DeletePDNConnectionSetResponse":
        self.add_ie(CauseIE(cause))
        return self

    @property
    def cause(self) -> int | None:
        ie = self.get_ie(C.IE_CAUSE)
        return ie.cause if ie else None


class PGWDownlinkTriggeringNotification(GTPv2Message):
    msg_type = C.MSG_PGW_DL_TRIGGER_NOTIFY

    def set_imsi(self, digits: str) -> "PGWDownlinkTriggeringNotification":
        from gtpc.v2.ie.typed import IMSIIE
        self.add_ie(IMSIIE(digits))
        return self

    def set_mme_fteid(self, fteid: FTEIDIE) -> "PGWDownlinkTriggeringNotification":
        self.add_ie(fteid)
        return self


class PGWDownlinkTriggeringAcknowledge(GTPv2Message):
    msg_type = C.MSG_PGW_DL_TRIGGER_ACK

    def set_cause(self, cause: int) -> "PGWDownlinkTriggeringAcknowledge":
        self.add_ie(CauseIE(cause))
        return self

    def set_imsi(self, digits: str) -> "PGWDownlinkTriggeringAcknowledge":
        from gtpc.v2.ie.typed import IMSIIE
        self.add_ie(IMSIIE(digits))
        return self
