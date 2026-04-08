"""GTPv2-C notification / status messages."""

from gtpc.v2.messages.base import GTPv2Message
from gtpc.v2.ie.typed import CauseIE, IMSIIE, FTEIDIE, RecoveryIE
from gtpc.v2 import constants as C


class DetachNotification(GTPv2Message):
    msg_type = C.MSG_DETACH_NOTIFY

    def set_detach_type(self, detach_type: int) -> "DetachNotification":
        from gtpc.v2.ie.base import IEv2
        ie = IEv2.__new__(IEv2)
        ie.ie_type = C.IE_DETACH_TYPE; ie.instance = 0
        ie.value = bytes([detach_type])
        self.add_ie(ie)
        return self


class DetachAcknowledge(GTPv2Message):
    msg_type = C.MSG_DETACH_ACK

    def set_cause(self, cause: int) -> "DetachAcknowledge":
        self.add_ie(CauseIE(cause))
        return self


class CSPagingIndication(GTPv2Message):
    msg_type = C.MSG_CS_PAGING_INDICATION

    def set_imsi(self, digits: str) -> "CSPagingIndication":
        self.add_ie(IMSIIE(digits))
        return self


class RANInformationRelay(GTPv2Message):
    msg_type = C.MSG_RAN_INFO_RELAY

    def set_rim_routing_address(self, data: bytes) -> "RANInformationRelay":
        from gtpc.v2.ie.base import IEv2
        ie = IEv2.__new__(IEv2)
        ie.ie_type = 164; ie.instance = 0; ie.value = data  # RIM routing addr placeholder
        self.add_ie(ie)
        return self


class AlertMMENotification(GTPv2Message):
    msg_type = C.MSG_ALERT_MME_NOTIFY


class AlertMMEAcknowledge(GTPv2Message):
    msg_type = C.MSG_ALERT_MME_ACK

    def set_cause(self, cause: int) -> "AlertMMEAcknowledge":
        self.add_ie(CauseIE(cause))
        return self


class UEActivityNotification(GTPv2Message):
    msg_type = C.MSG_UE_ACTIVITY_NOTIFY


class UEActivityAcknowledge(GTPv2Message):
    msg_type = C.MSG_UE_ACTIVITY_ACK

    def set_cause(self, cause: int) -> "UEActivityAcknowledge":
        self.add_ie(CauseIE(cause))
        return self


class ISRStatusIndication(GTPv2Message):
    msg_type = C.MSG_ISR_STATUS_INDICATION

    def set_isr_status(self, data: bytes) -> "ISRStatusIndication":
        from gtpc.v2.ie.base import IEv2
        ie = IEv2.__new__(IEv2)
        ie.ie_type = C.IE_SERVICE_INDICATOR; ie.instance = 0; ie.value = data
        self.add_ie(ie)
        return self


class UERegistrationQueryRequest(GTPv2Message):
    msg_type = C.MSG_UE_REGIST_QUERY_REQ

    def set_imsi(self, digits: str) -> "UERegistrationQueryRequest":
        self.add_ie(IMSIIE(digits))
        return self


class UERegistrationQueryResponse(GTPv2Message):
    msg_type = C.MSG_UE_REGIST_QUERY_RES

    def set_cause(self, cause: int) -> "UERegistrationQueryResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_imsi(self, digits: str) -> "UERegistrationQueryResponse":
        self.add_ie(IMSIIE(digits))
        return self


class SuspendNotification(GTPv2Message):
    msg_type = C.MSG_SUSPEND_NOTIFY

    def set_imsi(self, digits: str) -> "SuspendNotification":
        self.add_ie(IMSIIE(digits))
        return self


class SuspendAcknowledge(GTPv2Message):
    msg_type = C.MSG_SUSPEND_ACK

    def set_cause(self, cause: int) -> "SuspendAcknowledge":
        self.add_ie(CauseIE(cause))
        return self


class ResumeNotification(GTPv2Message):
    msg_type = C.MSG_RESUME_NOTIFY

    def set_imsi(self, digits: str) -> "ResumeNotification":
        self.add_ie(IMSIIE(digits))
        return self


class ResumeAcknowledge(GTPv2Message):
    msg_type = C.MSG_RESUME_ACK

    def set_cause(self, cause: int) -> "ResumeAcknowledge":
        self.add_ie(CauseIE(cause))
        return self


class PGWRestartNotification(GTPv2Message):
    msg_type = C.MSG_PGW_RESTART_NOTIFY

    def set_pgw_s5s8_ip(self, addr: str) -> "PGWRestartNotification":
        from gtpc.v2.ie.typed import IPAddressIE
        self.add_ie(IPAddressIE(addr))
        return self

    def set_sgw_s11s4_ip(self, addr: str) -> "PGWRestartNotification":
        from gtpc.v2.ie.typed import IPAddressIE
        ie = IPAddressIE(addr)
        ie.instance = 1
        self.add_ie(ie)
        return self

    def set_cause(self, cause: int) -> "PGWRestartNotification":
        self.add_ie(CauseIE(cause))
        return self


class PGWRestartNotificationAcknowledge(GTPv2Message):
    msg_type = C.MSG_PGW_RESTART_ACK

    def set_cause(self, cause: int) -> "PGWRestartNotificationAcknowledge":
        self.add_ie(CauseIE(cause))
        return self
