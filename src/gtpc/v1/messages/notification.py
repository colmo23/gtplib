"""GTPv1-C notification/error messages."""

from gtpc.v1.messages.base import GTPv1Message
from gtpc.v1.ie.tv import (
    IMSIE, TEIDDataIIE, TEIDCPlaneIE, NSAPIIE, CauseIE,
)
from gtpc.v1.ie.tlv import (
    EndUserAddressIE, APNIE, GSNAddressIE,
)
from gtpc.v1.ie.base import IEv1
from gtpc.v1 import constants as C


class ErrorIndication(GTPv1Message):
    msg_type = C.MSG_ERROR_INDICATION

    def set_teid_data(self, teid: int) -> "ErrorIndication":
        self.add_ie(TEIDDataIIE(teid))
        return self

    def set_gsn_address(self, addr: bytes) -> "ErrorIndication":
        self.add_ie(GSNAddressIE(addr))
        return self


class PDUNotificationRequest(GTPv1Message):
    msg_type = C.MSG_PDU_NOTIFICATION_REQ

    def set_imsi(self, digits: str) -> "PDUNotificationRequest":
        self.add_ie(IMSIE(digits))
        return self

    def set_teid_control(self, teid: int) -> "PDUNotificationRequest":
        self.add_ie(TEIDCPlaneIE(teid))
        return self

    def set_end_user_address(self, pdp_type_org: int, pdp_type_num: int,
                              address: bytes = b"") -> "PDUNotificationRequest":
        self.add_ie(EndUserAddressIE(pdp_type_org, pdp_type_num, address))
        return self

    def set_apn(self, apn: str) -> "PDUNotificationRequest":
        self.add_ie(APNIE(apn))
        return self

    def set_ggsn_address(self, addr: bytes) -> "PDUNotificationRequest":
        self.add_ie(GSNAddressIE(addr))
        return self


class PDUNotificationResponse(GTPv1Message):
    msg_type = C.MSG_PDU_NOTIFICATION_RES

    def set_cause(self, cause: int) -> "PDUNotificationResponse":
        self.add_ie(CauseIE(cause))
        return self

    @property
    def cause(self) -> int | None:
        ie = self.get_ie(C.IE_CAUSE)
        return ie.cause if ie else None


class PDUNotificationRejectRequest(GTPv1Message):
    msg_type = C.MSG_PDU_NOTIFICATION_REJECT_REQ

    def set_cause(self, cause: int) -> "PDUNotificationRejectRequest":
        self.add_ie(CauseIE(cause))
        return self

    def set_teid_control(self, teid: int) -> "PDUNotificationRejectRequest":
        self.add_ie(TEIDCPlaneIE(teid))
        return self

    def set_end_user_address(self, pdp_type_org: int, pdp_type_num: int,
                              address: bytes = b"") -> "PDUNotificationRejectRequest":
        self.add_ie(EndUserAddressIE(pdp_type_org, pdp_type_num, address))
        return self

    def set_apn(self, apn: str) -> "PDUNotificationRejectRequest":
        self.add_ie(APNIE(apn))
        return self


class PDUNotificationRejectResponse(GTPv1Message):
    msg_type = C.MSG_PDU_NOTIFICATION_REJECT_RES

    def set_cause(self, cause: int) -> "PDUNotificationRejectResponse":
        self.add_ie(CauseIE(cause))
        return self


class SupportedExtensionHeadersNotification(GTPv1Message):
    msg_type = C.MSG_SUPPORTED_EXT_HEADER_NOTIFY

    def set_ext_header_list(self, header_types: list[int]) -> "SupportedExtensionHeadersNotification":
        # IE 141: Extension Header Type List — TLV with raw list of type bytes
        ie = IEv1.__new__(IEv1)
        ie.ie_type = C.IE_EXT_HEADER_TYPE_LIST
        ie.value = bytes(header_types)
        self.add_ie(ie)
        return self
