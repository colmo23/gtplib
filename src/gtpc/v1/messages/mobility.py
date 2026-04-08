"""GTPv1-C mobility / handover messages."""

from gtpc.v1.messages.base import GTPv1Message
from gtpc.v1.ie.tv import (
    IMSIE, RAIIE, CauseIE, RecoveryIE, TEIDDataIIE, TEIDCPlaneIE,
    NSAPIIE, PTMSIIE,
)
from gtpc.v1.ie.tlv import (
    GSNAddressIE, MSISDNIE, QoSProfileIE, PCOIE,
    UserLocationInfoIE, MSTimeZoneIE, RATTypeIE,
)
from gtpc.v1.ie.base import IEv1
from gtpc.v1 import constants as C


class IdentificationRequest(GTPv1Message):
    msg_type = C.MSG_IDENTIFICATION_REQ

    def set_rai(self, mcc: str, mnc: str, lac: int, rac: int) -> "IdentificationRequest":
        self.add_ie(RAIIE(mcc, mnc, lac, rac))
        return self

    def set_ptmsi(self, ptmsi: int) -> "IdentificationRequest":
        self.add_ie(PTMSIIE(ptmsi))
        return self


class IdentificationResponse(GTPv1Message):
    msg_type = C.MSG_IDENTIFICATION_RES

    def set_cause(self, cause: int) -> "IdentificationResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_imsi(self, digits: str) -> "IdentificationResponse":
        self.add_ie(IMSIE(digits))
        return self


class SGSNContextRequest(GTPv1Message):
    msg_type = C.MSG_SGSN_CTX_REQ

    def set_imsi(self, digits: str) -> "SGSNContextRequest":
        self.add_ie(IMSIE(digits))
        return self

    def set_rai(self, mcc: str, mnc: str, lac: int, rac: int) -> "SGSNContextRequest":
        self.add_ie(RAIIE(mcc, mnc, lac, rac))
        return self

    def set_teid_control(self, teid: int) -> "SGSNContextRequest":
        self.add_ie(TEIDCPlaneIE(teid))
        return self

    def set_sgsn_address(self, addr: bytes) -> "SGSNContextRequest":
        self.add_ie(GSNAddressIE(addr))
        return self

    def set_nsapi(self, nsapi: int) -> "SGSNContextRequest":
        self.add_ie(NSAPIIE(nsapi))
        return self


class SGSNContextResponse(GTPv1Message):
    msg_type = C.MSG_SGSN_CTX_RES

    def set_cause(self, cause: int) -> "SGSNContextResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_imsi(self, digits: str) -> "SGSNContextResponse":
        self.add_ie(IMSIE(digits))
        return self

    def set_teid_control(self, teid: int) -> "SGSNContextResponse":
        self.add_ie(TEIDCPlaneIE(teid))
        return self

    def set_sgsn_address(self, addr: bytes) -> "SGSNContextResponse":
        self.add_ie(GSNAddressIE(addr))
        return self


class SGSNContextAcknowledge(GTPv1Message):
    msg_type = C.MSG_SGSN_CTX_ACK

    def set_cause(self, cause: int) -> "SGSNContextAcknowledge":
        self.add_ie(CauseIE(cause))
        return self


class ForwardRelocationRequest(GTPv1Message):
    msg_type = C.MSG_FORWARD_RELOC_REQ

    def set_imsi(self, digits: str) -> "ForwardRelocationRequest":
        self.add_ie(IMSIE(digits))
        return self

    def set_teid_control(self, teid: int) -> "ForwardRelocationRequest":
        self.add_ie(TEIDCPlaneIE(teid))
        return self

    def set_rai(self, mcc: str, mnc: str, lac: int, rac: int) -> "ForwardRelocationRequest":
        self.add_ie(RAIIE(mcc, mnc, lac, rac))
        return self

    def set_sgsn_address_signalling(self, addr: bytes) -> "ForwardRelocationRequest":
        self.add_ie(GSNAddressIE(addr))
        return self

    def set_sgsn_address_user_traffic(self, addr: bytes) -> "ForwardRelocationRequest":
        self.add_ie(GSNAddressIE(addr))
        return self


class ForwardRelocationResponse(GTPv1Message):
    msg_type = C.MSG_FORWARD_RELOC_RES

    def set_cause(self, cause: int) -> "ForwardRelocationResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_teid_control(self, teid: int) -> "ForwardRelocationResponse":
        self.add_ie(TEIDCPlaneIE(teid))
        return self

    def set_sgsn_address_signalling(self, addr: bytes) -> "ForwardRelocationResponse":
        self.add_ie(GSNAddressIE(addr))
        return self


class ForwardRelocationComplete(GTPv1Message):
    msg_type = C.MSG_FORWARD_RELOC_COMPLETE


class ForwardRelocationCompleteAcknowledge(GTPv1Message):
    msg_type = C.MSG_FORWARD_RELOC_COMPLETE_ACK

    def set_cause(self, cause: int) -> "ForwardRelocationCompleteAcknowledge":
        self.add_ie(CauseIE(cause))
        return self


class RelocationCancelRequest(GTPv1Message):
    msg_type = C.MSG_RELOC_CANCEL_REQ

    def set_imsi(self, digits: str) -> "RelocationCancelRequest":
        self.add_ie(IMSIE(digits))
        return self


class RelocationCancelResponse(GTPv1Message):
    msg_type = C.MSG_RELOC_CANCEL_RES

    def set_cause(self, cause: int) -> "RelocationCancelResponse":
        self.add_ie(CauseIE(cause))
        return self


class ForwardSRNSContext(GTPv1Message):
    msg_type = C.MSG_FORWARD_SRNS_CTX

    def set_rab_context(self, data: bytes) -> "ForwardSRNSContext":
        ie = IEv1.__new__(IEv1)
        ie.ie_type = C.IE_RAB_CTX
        ie.value = data
        self.add_ie(ie)
        return self


class ForwardSRNSContextAcknowledge(GTPv1Message):
    msg_type = C.MSG_FORWARD_SRNS_CTX_ACK

    def set_cause(self, cause: int) -> "ForwardSRNSContextAcknowledge":
        self.add_ie(CauseIE(cause))
        return self


class UERegistrationQueryRequest(GTPv1Message):
    msg_type = C.MSG_UE_REGIST_QUERY_REQ

    def set_imsi(self, digits: str) -> "UERegistrationQueryRequest":
        self.add_ie(IMSIE(digits))
        return self


class UERegistrationQueryResponse(GTPv1Message):
    msg_type = C.MSG_UE_REGIST_QUERY_RES

    def set_cause(self, cause: int) -> "UERegistrationQueryResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_imsi(self, digits: str) -> "UERegistrationQueryResponse":
        self.add_ie(IMSIE(digits))
        return self


class RANInformationRelay(GTPv1Message):
    msg_type = C.MSG_RAN_INFORMATION_RELAY

    def set_rim_routing_address(self, data: bytes) -> "RANInformationRelay":
        ie = IEv1.__new__(IEv1)
        ie.ie_type = C.IE_RIM_ROUTING_ADDRESS
        ie.value = data
        self.add_ie(ie)
        return self
