"""GTPv1-C location management messages (GTP')."""

from gtpc.v1.messages.base import GTPv1Message
from gtpc.v1.ie.tv import IMSIE, CauseIE, RecoveryIE
from gtpc.v1.ie.tlv import GSNAddressIE, MSISDNIE
from gtpc.v1 import constants as C


class SendRoutingInfoForGPRSRequest(GTPv1Message):
    msg_type = C.MSG_SEND_ROUTING_INFO_GPRS_REQ

    def set_imsi(self, digits: str) -> "SendRoutingInfoForGPRSRequest":
        self.add_ie(IMSIE(digits))
        return self


class SendRoutingInfoForGPRSResponse(GTPv1Message):
    msg_type = C.MSG_SEND_ROUTING_INFO_GPRS_RES

    def set_cause(self, cause: int) -> "SendRoutingInfoForGPRSResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_imsi(self, digits: str) -> "SendRoutingInfoForGPRSResponse":
        self.add_ie(IMSIE(digits))
        return self

    def set_msisdn(self, digits: str) -> "SendRoutingInfoForGPRSResponse":
        self.add_ie(MSISDNIE(digits))
        return self

    def set_sgsn_address(self, addr: bytes) -> "SendRoutingInfoForGPRSResponse":
        self.add_ie(GSNAddressIE(addr))
        return self

    def set_ggsn_address(self, addr: bytes) -> "SendRoutingInfoForGPRSResponse":
        self.add_ie(GSNAddressIE(addr))
        return self


class FailureReportRequest(GTPv1Message):
    msg_type = C.MSG_FAILURE_REPORT_REQ

    def set_imsi(self, digits: str) -> "FailureReportRequest":
        self.add_ie(IMSIE(digits))
        return self


class FailureReportResponse(GTPv1Message):
    msg_type = C.MSG_FAILURE_REPORT_RES

    def set_cause(self, cause: int) -> "FailureReportResponse":
        self.add_ie(CauseIE(cause))
        return self


class NoteMSGPRSPresentRequest(GTPv1Message):
    msg_type = C.MSG_NOTE_MS_GPRS_PRESENT_REQ

    def set_imsi(self, digits: str) -> "NoteMSGPRSPresentRequest":
        self.add_ie(IMSIE(digits))
        return self

    def set_sgsn_address(self, addr: bytes) -> "NoteMSGPRSPresentRequest":
        self.add_ie(GSNAddressIE(addr))
        return self


class NoteMSGPRSPresentResponse(GTPv1Message):
    msg_type = C.MSG_NOTE_MS_GPRS_PRESENT_RES

    def set_cause(self, cause: int) -> "NoteMSGPRSPresentResponse":
        self.add_ie(CauseIE(cause))
        return self
