"""GTPv1-C MBMS (Multimedia Broadcast/Multicast Service) messages (types 96-121)."""

from gtpc.v1.messages.base import GTPv1Message
from gtpc.v1.ie.tv import IMSIE, CauseIE, NSAPIIE
from gtpc.v1.ie.tlv import GSNAddressIE
from gtpc.v1.ie.base import IEv1
from gtpc.v1 import constants as C


def _raw_ie(ie_type: int, data: bytes) -> IEv1:
    ie = IEv1.__new__(IEv1)
    ie.ie_type = ie_type
    ie.value = data
    return ie


class MBMSNotificationRequest(GTPv1Message):
    msg_type = C.MSG_MBMS_NOTIFICATION_REQ

    def set_imsi(self, digits: str) -> "MBMSNotificationRequest":
        self.add_ie(IMSIE(digits))
        return self

    def set_nsapi(self, nsapi: int) -> "MBMSNotificationRequest":
        self.add_ie(NSAPIIE(nsapi))
        return self

    def set_end_user_address(self, data: bytes) -> "MBMSNotificationRequest":
        self.add_ie(_raw_ie(C.IE_END_USER_ADDRESS, data))
        return self

    def set_apn(self, data: bytes) -> "MBMSNotificationRequest":
        self.add_ie(_raw_ie(C.IE_APN, data))
        return self

    def set_ggsn_address(self, addr: bytes) -> "MBMSNotificationRequest":
        self.add_ie(GSNAddressIE(addr))
        return self


class MBMSNotificationResponse(GTPv1Message):
    msg_type = C.MSG_MBMS_NOTIFICATION_RES

    def set_cause(self, cause: int) -> "MBMSNotificationResponse":
        self.add_ie(CauseIE(cause))
        return self


class MBMSNotificationRejectRequest(GTPv1Message):
    msg_type = C.MSG_MBMS_NOTIFICATION_REJECT_REQ

    def set_cause(self, cause: int) -> "MBMSNotificationRejectRequest":
        self.add_ie(CauseIE(cause))
        return self

    def set_teid_control(self, data: bytes) -> "MBMSNotificationRejectRequest":
        self.add_ie(_raw_ie(C.IE_TEID_C_PLANE, data))
        return self


class MBMSNotificationRejectResponse(GTPv1Message):
    msg_type = C.MSG_MBMS_NOTIFICATION_REJECT_RES

    def set_cause(self, cause: int) -> "MBMSNotificationRejectResponse":
        self.add_ie(CauseIE(cause))
        return self


class CreateMBMSContextRequest(GTPv1Message):
    msg_type = C.MSG_CREATE_MBMS_CTX_REQ

    def set_imsi(self, digits: str) -> "CreateMBMSContextRequest":
        self.add_ie(IMSIE(digits))
        return self

    def set_rai(self, data: bytes) -> "CreateMBMSContextRequest":
        self.add_ie(_raw_ie(C.IE_RAI, data))
        return self

    def set_recovery(self, rc: int) -> "CreateMBMSContextRequest":
        from gtpc.v1.ie.tv import RecoveryIE
        self.add_ie(RecoveryIE(rc))
        return self

    def set_end_user_address(self, data: bytes) -> "CreateMBMSContextRequest":
        self.add_ie(_raw_ie(C.IE_END_USER_ADDRESS, data))
        return self

    def set_apn(self, data: bytes) -> "CreateMBMSContextRequest":
        self.add_ie(_raw_ie(C.IE_APN, data))
        return self

    def set_sgsn_address(self, addr: bytes) -> "CreateMBMSContextRequest":
        self.add_ie(GSNAddressIE(addr))
        return self

    def set_msisdn(self, data: bytes) -> "CreateMBMSContextRequest":
        self.add_ie(_raw_ie(C.IE_MSISDN, data))
        return self


class CreateMBMSContextResponse(GTPv1Message):
    msg_type = C.MSG_CREATE_MBMS_CTX_RES

    def set_cause(self, cause: int) -> "CreateMBMSContextResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_recovery(self, rc: int) -> "CreateMBMSContextResponse":
        from gtpc.v1.ie.tv import RecoveryIE
        self.add_ie(RecoveryIE(rc))
        return self

    def set_teid_control(self, data: bytes) -> "CreateMBMSContextResponse":
        self.add_ie(_raw_ie(C.IE_TEID_C_PLANE, data))
        return self

    def set_charging_id(self, data: bytes) -> "CreateMBMSContextResponse":
        self.add_ie(_raw_ie(C.IE_CHARGING_ID, data))
        return self

    def set_ggsn_address(self, addr: bytes) -> "CreateMBMSContextResponse":
        self.add_ie(GSNAddressIE(addr))
        return self


class UpdateMBMSContextRequest(GTPv1Message):
    msg_type = C.MSG_UPDATE_MBMS_CTX_REQ

    def set_imsi(self, digits: str) -> "UpdateMBMSContextRequest":
        self.add_ie(IMSIE(digits))
        return self

    def set_sgsn_address(self, addr: bytes) -> "UpdateMBMSContextRequest":
        self.add_ie(GSNAddressIE(addr))
        return self


class UpdateMBMSContextResponse(GTPv1Message):
    msg_type = C.MSG_UPDATE_MBMS_CTX_RES

    def set_cause(self, cause: int) -> "UpdateMBMSContextResponse":
        self.add_ie(CauseIE(cause))
        return self


class DeleteMBMSContextRequest(GTPv1Message):
    msg_type = C.MSG_DELETE_MBMS_CTX_REQ

    def set_imsi(self, digits: str) -> "DeleteMBMSContextRequest":
        self.add_ie(IMSIE(digits))
        return self

    def set_nsapi(self, nsapi: int) -> "DeleteMBMSContextRequest":
        self.add_ie(NSAPIIE(nsapi))
        return self


class DeleteMBMSContextResponse(GTPv1Message):
    msg_type = C.MSG_DELETE_MBMS_CTX_RES

    def set_cause(self, cause: int) -> "DeleteMBMSContextResponse":
        self.add_ie(CauseIE(cause))
        return self


class MBMSRegistrationRequest(GTPv1Message):
    msg_type = C.MSG_MBMS_REGIST_REQ

    def set_end_user_address(self, data: bytes) -> "MBMSRegistrationRequest":
        self.add_ie(_raw_ie(C.IE_END_USER_ADDRESS, data))
        return self

    def set_apn(self, data: bytes) -> "MBMSRegistrationRequest":
        self.add_ie(_raw_ie(C.IE_APN, data))
        return self

    def set_sgsn_address(self, addr: bytes) -> "MBMSRegistrationRequest":
        self.add_ie(GSNAddressIE(addr))
        return self


class MBMSRegistrationResponse(GTPv1Message):
    msg_type = C.MSG_MBMS_REGIST_RES

    def set_cause(self, cause: int) -> "MBMSRegistrationResponse":
        self.add_ie(CauseIE(cause))
        return self


class MBMSDeRegistrationRequest(GTPv1Message):
    msg_type = C.MSG_MBMS_DEREGIST_REQ

    def set_end_user_address(self, data: bytes) -> "MBMSDeRegistrationRequest":
        self.add_ie(_raw_ie(C.IE_END_USER_ADDRESS, data))
        return self

    def set_apn(self, data: bytes) -> "MBMSDeRegistrationRequest":
        self.add_ie(_raw_ie(C.IE_APN, data))
        return self


class MBMSDeRegistrationResponse(GTPv1Message):
    msg_type = C.MSG_MBMS_DEREGIST_RES

    def set_cause(self, cause: int) -> "MBMSDeRegistrationResponse":
        self.add_ie(CauseIE(cause))
        return self


class MBMSSessionStartRequest(GTPv1Message):
    msg_type = C.MSG_MBMS_SESSION_START_REQ

    def set_recovery(self, rc: int) -> "MBMSSessionStartRequest":
        from gtpc.v1.ie.tv import RecoveryIE
        self.add_ie(RecoveryIE(rc))
        return self

    def set_end_user_address(self, data: bytes) -> "MBMSSessionStartRequest":
        self.add_ie(_raw_ie(C.IE_END_USER_ADDRESS, data))
        return self

    def set_apn(self, data: bytes) -> "MBMSSessionStartRequest":
        self.add_ie(_raw_ie(C.IE_APN, data))
        return self

    def set_ggsn_address(self, addr: bytes) -> "MBMSSessionStartRequest":
        self.add_ie(GSNAddressIE(addr))
        return self

    def set_tmgi(self, data: bytes) -> "MBMSSessionStartRequest":
        self.add_ie(_raw_ie(C.IE_TMGI, data))
        return self

    def set_mbms_session_id(self, data: bytes) -> "MBMSSessionStartRequest":
        self.add_ie(_raw_ie(C.IE_MBMS_SESSION_ID, data))
        return self

    def set_mbms_service_area(self, data: bytes) -> "MBMSSessionStartRequest":
        self.add_ie(_raw_ie(C.IE_MBMS_SERVICE_AREA, data))
        return self


class MBMSSessionStartResponse(GTPv1Message):
    msg_type = C.MSG_MBMS_SESSION_START_RES

    def set_cause(self, cause: int) -> "MBMSSessionStartResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_recovery(self, rc: int) -> "MBMSSessionStartResponse":
        from gtpc.v1.ie.tv import RecoveryIE
        self.add_ie(RecoveryIE(rc))
        return self

    def set_sgsn_address(self, addr: bytes) -> "MBMSSessionStartResponse":
        self.add_ie(GSNAddressIE(addr))
        return self


class MBMSSessionStopRequest(GTPv1Message):
    msg_type = C.MSG_MBMS_SESSION_STOP_REQ

    def set_end_user_address(self, data: bytes) -> "MBMSSessionStopRequest":
        self.add_ie(_raw_ie(C.IE_END_USER_ADDRESS, data))
        return self

    def set_apn(self, data: bytes) -> "MBMSSessionStopRequest":
        self.add_ie(_raw_ie(C.IE_APN, data))
        return self


class MBMSSessionStopResponse(GTPv1Message):
    msg_type = C.MSG_MBMS_SESSION_STOP_RES

    def set_cause(self, cause: int) -> "MBMSSessionStopResponse":
        self.add_ie(CauseIE(cause))
        return self


class MBMSSessionUpdateRequest(GTPv1Message):
    msg_type = C.MSG_MBMS_SESSION_UPDATE_REQ

    def set_end_user_address(self, data: bytes) -> "MBMSSessionUpdateRequest":
        self.add_ie(_raw_ie(C.IE_END_USER_ADDRESS, data))
        return self

    def set_apn(self, data: bytes) -> "MBMSSessionUpdateRequest":
        self.add_ie(_raw_ie(C.IE_APN, data))
        return self

    def set_tmgi(self, data: bytes) -> "MBMSSessionUpdateRequest":
        self.add_ie(_raw_ie(C.IE_TMGI, data))
        return self

    def set_sgsn_address(self, addr: bytes) -> "MBMSSessionUpdateRequest":
        self.add_ie(GSNAddressIE(addr))
        return self


class MBMSSessionUpdateResponse(GTPv1Message):
    msg_type = C.MSG_MBMS_SESSION_UPDATE_RES

    def set_cause(self, cause: int) -> "MBMSSessionUpdateResponse":
        self.add_ie(CauseIE(cause))
        return self
