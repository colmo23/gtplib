"""GTPv1-C tunnel management messages (Create/Update/Delete PDP Context)."""

from gtpc.v1.messages.base import GTPv1Message
from gtpc.v1.ie.tv import (
    IMSIE, RAIIE, RecoveryIE, SelectionModeIE,
    TEIDDataIIE, TEIDCPlaneIE, NSAPIIE, ChargingCharsIE, ChargingIDIE,
    TeardownIndIE, TEIDDataIIIE, CauseIE,
)
from gtpc.v1.ie.tlv import (
    EndUserAddressIE, APNIE, PCOIE, GSNAddressIE, MSISDNIE,
    QoSProfileIE, TrafficFlowTemplateIE, UserLocationInfoIE,
    MSTimeZoneIE, IMEISVIe, RATTypeIE, CommonFlagsIE, APNRestrictionIE,
)
from gtpc.v1 import constants as C


class CreatePDPContextRequest(GTPv1Message):
    msg_type = C.MSG_CREATE_PDP_CTX_REQ

    def set_imsi(self, digits: str) -> "CreatePDPContextRequest":
        self.add_ie(IMSIE(digits))
        return self

    def set_rai(self, mcc: str, mnc: str, lac: int, rac: int) -> "CreatePDPContextRequest":
        self.add_ie(RAIIE(mcc, mnc, lac, rac))
        return self

    def set_recovery(self, rc: int) -> "CreatePDPContextRequest":
        self.add_ie(RecoveryIE(rc))
        return self

    def set_selection_mode(self, mode: int) -> "CreatePDPContextRequest":
        self.add_ie(SelectionModeIE(mode))
        return self

    def set_teid_data(self, teid: int) -> "CreatePDPContextRequest":
        self.add_ie(TEIDDataIIE(teid))
        return self

    def set_teid_control(self, teid: int) -> "CreatePDPContextRequest":
        self.add_ie(TEIDCPlaneIE(teid))
        return self

    def set_nsapi(self, nsapi: int) -> "CreatePDPContextRequest":
        self.add_ie(NSAPIIE(nsapi))
        return self

    def set_charging_chars(self, chars: int) -> "CreatePDPContextRequest":
        self.add_ie(ChargingCharsIE(chars))
        return self

    def set_end_user_address(self, pdp_type_org: int, pdp_type_num: int,
                              address: bytes = b"") -> "CreatePDPContextRequest":
        self.add_ie(EndUserAddressIE(pdp_type_org, pdp_type_num, address))
        return self

    def set_apn(self, apn: str) -> "CreatePDPContextRequest":
        self.add_ie(APNIE(apn))
        return self

    def set_pco(self, data: bytes) -> "CreatePDPContextRequest":
        self.add_ie(PCOIE(data))
        return self

    def set_sgsn_address_signalling(self, addr: bytes) -> "CreatePDPContextRequest":
        self.add_ie(GSNAddressIE(addr))
        return self

    def set_sgsn_address_user_traffic(self, addr: bytes) -> "CreatePDPContextRequest":
        self.add_ie(GSNAddressIE(addr))
        return self

    def set_msisdn(self, digits: str) -> "CreatePDPContextRequest":
        self.add_ie(MSISDNIE(digits))
        return self

    def set_qos_profile(self, data: bytes) -> "CreatePDPContextRequest":
        self.add_ie(QoSProfileIE(data))
        return self

    def set_rat_type(self, rat: int) -> "CreatePDPContextRequest":
        self.add_ie(RATTypeIE(rat))
        return self

    def set_uli(self, glt: int, location: bytes) -> "CreatePDPContextRequest":
        self.add_ie(UserLocationInfoIE(glt, location))
        return self

    def set_ms_timezone(self, tz: int, dst: int) -> "CreatePDPContextRequest":
        self.add_ie(MSTimeZoneIE(tz, dst))
        return self

    def set_imei_sv(self, digits: str) -> "CreatePDPContextRequest":
        self.add_ie(IMEISVIe(digits))
        return self

    def set_common_flags(self, flags: int) -> "CreatePDPContextRequest":
        self.add_ie(CommonFlagsIE(flags))
        return self

    def set_apn_restriction(self, restriction: int) -> "CreatePDPContextRequest":
        self.add_ie(APNRestrictionIE(restriction))
        return self

    # Property accessors
    @property
    def imsi(self) -> str | None:
        ie = self.get_ie(C.IE_IMSI)
        return ie.digits if ie else None

    @property
    def apn(self) -> str | None:
        ie = self.get_ie(C.IE_APN)
        return ie.apn if ie else None

    @property
    def nsapi(self) -> int | None:
        ie = self.get_ie(C.IE_NSAPI)
        return ie.nsapi if ie else None

    @property
    def teid_data(self) -> int | None:
        ie = self.get_ie(C.IE_TEID_DATA_1)
        return ie.teid if ie else None

    @property
    def teid_control(self) -> int | None:
        ie = self.get_ie(C.IE_TEID_C_PLANE)
        return ie.teid if ie else None


class CreatePDPContextResponse(GTPv1Message):
    msg_type = C.MSG_CREATE_PDP_CTX_RES

    def set_cause(self, cause: int) -> "CreatePDPContextResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_recovery(self, rc: int) -> "CreatePDPContextResponse":
        self.add_ie(RecoveryIE(rc))
        return self

    def set_teid_data(self, teid: int) -> "CreatePDPContextResponse":
        self.add_ie(TEIDDataIIE(teid))
        return self

    def set_teid_control(self, teid: int) -> "CreatePDPContextResponse":
        self.add_ie(TEIDCPlaneIE(teid))
        return self

    def set_charging_id(self, cid: int) -> "CreatePDPContextResponse":
        self.add_ie(ChargingIDIE(cid))
        return self

    def set_end_user_address(self, pdp_type_org: int, pdp_type_num: int,
                              address: bytes) -> "CreatePDPContextResponse":
        self.add_ie(EndUserAddressIE(pdp_type_org, pdp_type_num, address))
        return self

    def set_pco(self, data: bytes) -> "CreatePDPContextResponse":
        self.add_ie(PCOIE(data))
        return self

    def set_ggsn_address_signalling(self, addr: bytes) -> "CreatePDPContextResponse":
        self.add_ie(GSNAddressIE(addr))
        return self

    def set_ggsn_address_user_traffic(self, addr: bytes) -> "CreatePDPContextResponse":
        self.add_ie(GSNAddressIE(addr))
        return self

    def set_qos_profile(self, data: bytes) -> "CreatePDPContextResponse":
        self.add_ie(QoSProfileIE(data))
        return self

    def set_apn_restriction(self, restriction: int) -> "CreatePDPContextResponse":
        self.add_ie(APNRestrictionIE(restriction))
        return self

    @property
    def cause(self) -> int | None:
        ie = self.get_ie(C.IE_CAUSE)
        return ie.cause if ie else None


class UpdatePDPContextRequest(GTPv1Message):
    msg_type = C.MSG_UPDATE_PDP_CTX_REQ

    def set_imsi(self, digits: str) -> "UpdatePDPContextRequest":
        self.add_ie(IMSIE(digits))
        return self

    def set_rai(self, mcc: str, mnc: str, lac: int, rac: int) -> "UpdatePDPContextRequest":
        self.add_ie(RAIIE(mcc, mnc, lac, rac))
        return self

    def set_recovery(self, rc: int) -> "UpdatePDPContextRequest":
        self.add_ie(RecoveryIE(rc))
        return self

    def set_teid_data(self, teid: int) -> "UpdatePDPContextRequest":
        self.add_ie(TEIDDataIIE(teid))
        return self

    def set_teid_control(self, teid: int) -> "UpdatePDPContextRequest":
        self.add_ie(TEIDCPlaneIE(teid))
        return self

    def set_nsapi(self, nsapi: int) -> "UpdatePDPContextRequest":
        self.add_ie(NSAPIIE(nsapi))
        return self

    def set_sgsn_address_signalling(self, addr: bytes) -> "UpdatePDPContextRequest":
        self.add_ie(GSNAddressIE(addr))
        return self

    def set_sgsn_address_user_traffic(self, addr: bytes) -> "UpdatePDPContextRequest":
        self.add_ie(GSNAddressIE(addr))
        return self

    def set_qos_profile(self, data: bytes) -> "UpdatePDPContextRequest":
        self.add_ie(QoSProfileIE(data))
        return self

    def set_tft(self, data: bytes) -> "UpdatePDPContextRequest":
        self.add_ie(TrafficFlowTemplateIE(data))
        return self

    def set_rat_type(self, rat: int) -> "UpdatePDPContextRequest":
        self.add_ie(RATTypeIE(rat))
        return self

    def set_uli(self, glt: int, location: bytes) -> "UpdatePDPContextRequest":
        self.add_ie(UserLocationInfoIE(glt, location))
        return self

    def set_ms_timezone(self, tz: int, dst: int) -> "UpdatePDPContextRequest":
        self.add_ie(MSTimeZoneIE(tz, dst))
        return self


class UpdatePDPContextResponse(GTPv1Message):
    msg_type = C.MSG_UPDATE_PDP_CTX_RES

    def set_cause(self, cause: int) -> "UpdatePDPContextResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_recovery(self, rc: int) -> "UpdatePDPContextResponse":
        self.add_ie(RecoveryIE(rc))
        return self

    def set_teid_data(self, teid: int) -> "UpdatePDPContextResponse":
        self.add_ie(TEIDDataIIE(teid))
        return self

    def set_teid_control(self, teid: int) -> "UpdatePDPContextResponse":
        self.add_ie(TEIDCPlaneIE(teid))
        return self

    def set_charging_id(self, cid: int) -> "UpdatePDPContextResponse":
        self.add_ie(ChargingIDIE(cid))
        return self

    def set_qos_profile(self, data: bytes) -> "UpdatePDPContextResponse":
        self.add_ie(QoSProfileIE(data))
        return self

    def set_ggsn_address_signalling(self, addr: bytes) -> "UpdatePDPContextResponse":
        self.add_ie(GSNAddressIE(addr))
        return self

    def set_ggsn_address_user_traffic(self, addr: bytes) -> "UpdatePDPContextResponse":
        self.add_ie(GSNAddressIE(addr))
        return self

    @property
    def cause(self) -> int | None:
        ie = self.get_ie(C.IE_CAUSE)
        return ie.cause if ie else None


class DeletePDPContextRequest(GTPv1Message):
    msg_type = C.MSG_DELETE_PDP_CTX_REQ

    def set_teardown_ind(self, teardown: bool) -> "DeletePDPContextRequest":
        self.add_ie(TeardownIndIE(teardown))
        return self

    def set_nsapi(self, nsapi: int) -> "DeletePDPContextRequest":
        self.add_ie(NSAPIIE(nsapi))
        return self

    def set_pco(self, data: bytes) -> "DeletePDPContextRequest":
        self.add_ie(PCOIE(data))
        return self

    def set_uli(self, glt: int, location: bytes) -> "DeletePDPContextRequest":
        self.add_ie(UserLocationInfoIE(glt, location))
        return self

    def set_ms_timezone(self, tz: int, dst: int) -> "DeletePDPContextRequest":
        self.add_ie(MSTimeZoneIE(tz, dst))
        return self


class DeletePDPContextResponse(GTPv1Message):
    msg_type = C.MSG_DELETE_PDP_CTX_RES

    def set_cause(self, cause: int) -> "DeletePDPContextResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_pco(self, data: bytes) -> "DeletePDPContextResponse":
        self.add_ie(PCOIE(data))
        return self

    @property
    def cause(self) -> int | None:
        ie = self.get_ie(C.IE_CAUSE)
        return ie.cause if ie else None


class InitiatePDPContextActivationRequest(GTPv1Message):
    msg_type = C.MSG_INIT_PDP_CTX_ACT_REQ

    def set_nsapi(self, nsapi: int) -> "InitiatePDPContextActivationRequest":
        self.add_ie(NSAPIIE(nsapi))
        return self

    def set_pco(self, data: bytes) -> "InitiatePDPContextActivationRequest":
        self.add_ie(PCOIE(data))
        return self

    def set_qos_profile(self, data: bytes) -> "InitiatePDPContextActivationRequest":
        self.add_ie(QoSProfileIE(data))
        return self

    def set_tft(self, data: bytes) -> "InitiatePDPContextActivationRequest":
        self.add_ie(TrafficFlowTemplateIE(data))
        return self


class InitiatePDPContextActivationResponse(GTPv1Message):
    msg_type = C.MSG_INIT_PDP_CTX_ACT_RES

    def set_cause(self, cause: int) -> "InitiatePDPContextActivationResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_pco(self, data: bytes) -> "InitiatePDPContextActivationResponse":
        self.add_ie(PCOIE(data))
        return self
