"""GTPv2-C session management messages."""

from gtpc.v2.messages.base import GTPv2Message
from gtpc.v2.ie.typed import (
    IMSIIE, CauseIE, RecoveryIE, APNIE, AMBRIE, EBIIE, IPAddressIE,
    MEIIE, MSISDNIE, IndicationIE, PCOIE, PAAIE, BearerQoSIE,
    RATTypeIE, ServingNetworkIE, ULIIE, FTEIDIE, BearerContextIE,
    ChargingIDIE, ChargingCharsIE, PDNTypeIE, PTIIE,
    UETimeZoneIE, APNRestrictionIE, SelectionModeIE, FQCSIDIe,
    NodeTypeIE, FQDNIE, ARPIE, APCOIE,
)
from gtpc.v2 import constants as C


class CreateSessionRequest(GTPv2Message):
    msg_type = C.MSG_CREATE_SESSION_REQ

    def set_imsi(self, digits: str) -> "CreateSessionRequest":
        self.add_ie(IMSIIE(digits))
        return self

    def set_msisdn(self, digits: str) -> "CreateSessionRequest":
        self.add_ie(MSISDNIE(digits))
        return self

    def set_mei(self, digits: str) -> "CreateSessionRequest":
        self.add_ie(MEIIE(digits))
        return self

    def set_uli(self, uli: ULIIE) -> "CreateSessionRequest":
        self.add_ie(uli)
        return self

    def set_serving_network(self, mcc: str, mnc: str) -> "CreateSessionRequest":
        self.add_ie(ServingNetworkIE(mcc, mnc))
        return self

    def set_rat_type(self, rat: int) -> "CreateSessionRequest":
        self.add_ie(RATTypeIE(rat))
        return self

    def set_indication(self, flags: int) -> "CreateSessionRequest":
        self.add_ie(IndicationIE(flags))
        return self

    def set_sender_fteid(self, fteid: FTEIDIE) -> "CreateSessionRequest":
        self.add_ie(fteid)
        return self

    def set_pgw_fteid(self, fteid: FTEIDIE) -> "CreateSessionRequest":
        fteid.instance = 1
        self.add_ie(fteid)
        return self

    def set_apn(self, apn: str) -> "CreateSessionRequest":
        self.add_ie(APNIE(apn))
        return self

    def set_selection_mode(self, mode: int) -> "CreateSessionRequest":
        self.add_ie(SelectionModeIE(mode))
        return self

    def set_pdn_type(self, pdn_type: int) -> "CreateSessionRequest":
        self.add_ie(PDNTypeIE(pdn_type))
        return self

    def set_paa(self, paa: PAAIE) -> "CreateSessionRequest":
        self.add_ie(paa)
        return self

    def set_apn_restriction(self, restriction: int) -> "CreateSessionRequest":
        self.add_ie(APNRestrictionIE(restriction))
        return self

    def set_ambr(self, uplink_kbps: int, downlink_kbps: int) -> "CreateSessionRequest":
        self.add_ie(AMBRIE(uplink_kbps, downlink_kbps))
        return self

    def set_pco(self, data: bytes) -> "CreateSessionRequest":
        self.add_ie(PCOIE(data))
        return self

    def add_bearer_context(self, ctx: BearerContextIE) -> "CreateSessionRequest":
        self.add_ie(ctx)
        return self

    def set_charging_chars(self, chars: int) -> "CreateSessionRequest":
        self.add_ie(ChargingCharsIE(chars))
        return self

    def set_recovery(self, rc: int) -> "CreateSessionRequest":
        self.add_ie(RecoveryIE(rc))
        return self

    def set_ue_timezone(self, tz_byte: int, dst: int) -> "CreateSessionRequest":
        self.add_ie(UETimeZoneIE(tz_byte, dst))
        return self

    def set_charging_id(self, cid: int) -> "CreateSessionRequest":
        self.add_ie(ChargingIDIE(cid))
        return self

    def set_mme_fq_csid(self, csid: FQCSIDIe) -> "CreateSessionRequest":
        self.add_ie(csid)
        return self

    def set_ue_local_ip(self, addr: str) -> "CreateSessionRequest":
        self.add_ie(IPAddressIE(addr))
        return self

    def set_apco(self, data: bytes) -> "CreateSessionRequest":
        self.add_ie(APCOIE(data))
        return self

    # Accessors
    @property
    def imsi(self) -> str | None:
        ie = self.get_ie(C.IE_IMSI)
        return ie.digits if ie else None

    @property
    def apn(self) -> str | None:
        ie = self.get_ie(C.IE_APN)
        return ie.apn if ie else None

    @property
    def pdn_type(self) -> int | None:
        ie = self.get_ie(C.IE_PDN_TYPE)
        return ie.pdn_type if ie else None

    @property
    def bearer_contexts(self) -> list[BearerContextIE]:
        return self.get_ies(C.IE_BEARER_CTX)


class CreateSessionResponse(GTPv2Message):
    msg_type = C.MSG_CREATE_SESSION_RES

    def set_cause(self, cause: int) -> "CreateSessionResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_recovery(self, rc: int) -> "CreateSessionResponse":
        self.add_ie(RecoveryIE(rc))
        return self

    def set_sender_fteid(self, fteid: FTEIDIE) -> "CreateSessionResponse":
        self.add_ie(fteid)
        return self

    def set_pgw_fteid(self, fteid: FTEIDIE) -> "CreateSessionResponse":
        fteid.instance = 1
        self.add_ie(fteid)
        return self

    def set_paa(self, paa: PAAIE) -> "CreateSessionResponse":
        self.add_ie(paa)
        return self

    def set_apn_restriction(self, restriction: int) -> "CreateSessionResponse":
        self.add_ie(APNRestrictionIE(restriction))
        return self

    def set_ambr(self, uplink_kbps: int, downlink_kbps: int) -> "CreateSessionResponse":
        self.add_ie(AMBRIE(uplink_kbps, downlink_kbps))
        return self

    def set_pco(self, data: bytes) -> "CreateSessionResponse":
        self.add_ie(PCOIE(data))
        return self

    def add_bearer_context(self, ctx: BearerContextIE) -> "CreateSessionResponse":
        self.add_ie(ctx)
        return self

    def set_charging_id(self, cid: int) -> "CreateSessionResponse":
        self.add_ie(ChargingIDIE(cid))
        return self

    def set_fq_csid(self, csid: FQCSIDIe) -> "CreateSessionResponse":
        self.add_ie(csid)
        return self

    @property
    def cause(self) -> int | None:
        ie = self.get_ie(C.IE_CAUSE)
        return ie.cause if ie else None


class ModifyBearerRequest(GTPv2Message):
    msg_type = C.MSG_MODIFY_BEARER_REQ

    def set_indication(self, flags: int) -> "ModifyBearerRequest":
        self.add_ie(IndicationIE(flags))
        return self

    def set_rat_type(self, rat: int) -> "ModifyBearerRequest":
        self.add_ie(RATTypeIE(rat))
        return self

    def set_uli(self, uli: ULIIE) -> "ModifyBearerRequest":
        self.add_ie(uli)
        return self

    def set_serving_network(self, mcc: str, mnc: str) -> "ModifyBearerRequest":
        self.add_ie(ServingNetworkIE(mcc, mnc))
        return self

    def set_recovery(self, rc: int) -> "ModifyBearerRequest":
        self.add_ie(RecoveryIE(rc))
        return self

    def add_bearer_context(self, ctx: BearerContextIE) -> "ModifyBearerRequest":
        self.add_ie(ctx)
        return self

    def set_ue_timezone(self, tz_byte: int, dst: int) -> "ModifyBearerRequest":
        self.add_ie(UETimeZoneIE(tz_byte, dst))
        return self

    def set_sender_fteid(self, fteid: FTEIDIE) -> "ModifyBearerRequest":
        self.add_ie(fteid)
        return self


class ModifyBearerResponse(GTPv2Message):
    msg_type = C.MSG_MODIFY_BEARER_RES

    def set_cause(self, cause: int) -> "ModifyBearerResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_recovery(self, rc: int) -> "ModifyBearerResponse":
        self.add_ie(RecoveryIE(rc))
        return self

    def add_bearer_context(self, ctx: BearerContextIE) -> "ModifyBearerResponse":
        self.add_ie(ctx)
        return self

    def set_pco(self, data: bytes) -> "ModifyBearerResponse":
        self.add_ie(PCOIE(data))
        return self

    @property
    def cause(self) -> int | None:
        ie = self.get_ie(C.IE_CAUSE)
        return ie.cause if ie else None


class DeleteSessionRequest(GTPv2Message):
    msg_type = C.MSG_DELETE_SESSION_REQ

    def set_cause(self, cause: int) -> "DeleteSessionRequest":
        self.add_ie(CauseIE(cause))
        return self

    def set_indication(self, flags: int) -> "DeleteSessionRequest":
        self.add_ie(IndicationIE(flags))
        return self

    def set_ebi(self, ebi: int) -> "DeleteSessionRequest":
        self.add_ie(EBIIE(ebi))
        return self

    def set_uli(self, uli: ULIIE) -> "DeleteSessionRequest":
        self.add_ie(uli)
        return self

    def set_ue_timezone(self, tz_byte: int, dst: int) -> "DeleteSessionRequest":
        self.add_ie(UETimeZoneIE(tz_byte, dst))
        return self

    def set_pco(self, data: bytes) -> "DeleteSessionRequest":
        self.add_ie(PCOIE(data))
        return self


class DeleteSessionResponse(GTPv2Message):
    msg_type = C.MSG_DELETE_SESSION_RES

    def set_cause(self, cause: int) -> "DeleteSessionResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_recovery(self, rc: int) -> "DeleteSessionResponse":
        self.add_ie(RecoveryIE(rc))
        return self

    def set_pco(self, data: bytes) -> "DeleteSessionResponse":
        self.add_ie(PCOIE(data))
        return self

    @property
    def cause(self) -> int | None:
        ie = self.get_ie(C.IE_CAUSE)
        return ie.cause if ie else None


class ChangeNotificationRequest(GTPv2Message):
    msg_type = C.MSG_CHANGE_NOTIFICATION_REQ

    def set_imsi(self, digits: str) -> "ChangeNotificationRequest":
        self.add_ie(IMSIIE(digits))
        return self

    def set_rat_type(self, rat: int) -> "ChangeNotificationRequest":
        self.add_ie(RATTypeIE(rat))
        return self

    def set_indication(self, flags: int) -> "ChangeNotificationRequest":
        self.add_ie(IndicationIE(flags))
        return self

    def set_uli(self, uli: ULIIE) -> "ChangeNotificationRequest":
        self.add_ie(uli)
        return self

    def set_mei(self, digits: str) -> "ChangeNotificationRequest":
        self.add_ie(MEIIE(digits))
        return self


class ChangeNotificationResponse(GTPv2Message):
    msg_type = C.MSG_CHANGE_NOTIFICATION_RES

    def set_cause(self, cause: int) -> "ChangeNotificationResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_imsi(self, digits: str) -> "ChangeNotificationResponse":
        self.add_ie(IMSIIE(digits))
        return self


class RemoteUEReportNotification(GTPv2Message):
    msg_type = C.MSG_REMOTE_UE_REPORT_NOTIFY


class RemoteUEReportAcknowledge(GTPv2Message):
    msg_type = C.MSG_REMOTE_UE_REPORT_ACK

    def set_cause(self, cause: int) -> "RemoteUEReportAcknowledge":
        self.add_ie(CauseIE(cause))
        return self
