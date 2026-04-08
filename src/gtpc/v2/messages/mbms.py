"""GTPv2-C MBMS session messages (types 231-236)."""

from gtpc.v2.messages.base import GTPv2Message
from gtpc.v2.ie.typed import CauseIE, FTEIDIE, AMBRIE
from gtpc.v2.ie.base import IEv2
from gtpc.v2 import constants as C


def _raw_ie(ie_type: int, data: bytes, instance: int = 0) -> IEv2:
    ie = IEv2.__new__(IEv2)
    ie.ie_type = ie_type
    ie.instance = instance
    ie.value = data
    return ie


class MBMSSessionStartRequest(GTPv2Message):
    msg_type = C.MSG_MBMS_SESSION_START_REQ

    def set_sender_fteid(self, fteid: FTEIDIE) -> "MBMSSessionStartRequest":
        self.add_ie(fteid)
        return self

    def set_tmgi(self, data: bytes) -> "MBMSSessionStartRequest":
        self.add_ie(_raw_ie(C.IE_TMGI, data))
        return self

    def set_mbms_session_duration(self, data: bytes) -> "MBMSSessionStartRequest":
        self.add_ie(_raw_ie(C.IE_MBMS_SESSION_DURATION, data))
        return self

    def set_mbms_service_area(self, data: bytes) -> "MBMSSessionStartRequest":
        self.add_ie(_raw_ie(C.IE_MBMS_SERVICE_AREA, data))
        return self

    def set_mbms_ip_multicast_distribution(self, data: bytes) -> "MBMSSessionStartRequest":
        self.add_ie(_raw_ie(C.IE_MBMS_IP_MC_DIST, data))
        return self

    def set_ambr(self, uplink_kbps: int, downlink_kbps: int) -> "MBMSSessionStartRequest":
        self.add_ie(AMBRIE(uplink_kbps, downlink_kbps))
        return self

    def set_mbms_session_id(self, data: bytes) -> "MBMSSessionStartRequest":
        self.add_ie(_raw_ie(C.IE_MBMS_SESSION_ID, data))
        return self


class MBMSSessionStartResponse(GTPv2Message):
    msg_type = C.MSG_MBMS_SESSION_START_RES

    def set_cause(self, cause: int) -> "MBMSSessionStartResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_sender_fteid(self, fteid: FTEIDIE) -> "MBMSSessionStartResponse":
        self.add_ie(fteid)
        return self

    def set_mbms_distribution_acknowledge(self, data: bytes) -> "MBMSSessionStartResponse":
        self.add_ie(_raw_ie(C.IE_MBMS_DIST_ACK, data))
        return self

    @property
    def cause(self) -> int | None:
        ie = self.get_ie(C.IE_CAUSE)
        return ie.cause if ie else None


class MBMSSessionUpdateRequest(GTPv2Message):
    msg_type = C.MSG_MBMS_SESSION_UPDATE_REQ

    def set_sender_fteid(self, fteid: FTEIDIE) -> "MBMSSessionUpdateRequest":
        self.add_ie(fteid)
        return self

    def set_tmgi(self, data: bytes) -> "MBMSSessionUpdateRequest":
        self.add_ie(_raw_ie(C.IE_TMGI, data))
        return self

    def set_mbms_session_duration(self, data: bytes) -> "MBMSSessionUpdateRequest":
        self.add_ie(_raw_ie(C.IE_MBMS_SESSION_DURATION, data))
        return self

    def set_mbms_service_area(self, data: bytes) -> "MBMSSessionUpdateRequest":
        self.add_ie(_raw_ie(C.IE_MBMS_SERVICE_AREA, data))
        return self

    def set_ambr(self, uplink_kbps: int, downlink_kbps: int) -> "MBMSSessionUpdateRequest":
        self.add_ie(AMBRIE(uplink_kbps, downlink_kbps))
        return self


class MBMSSessionUpdateResponse(GTPv2Message):
    msg_type = C.MSG_MBMS_SESSION_UPDATE_RES

    def set_cause(self, cause: int) -> "MBMSSessionUpdateResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_sender_fteid(self, fteid: FTEIDIE) -> "MBMSSessionUpdateResponse":
        self.add_ie(fteid)
        return self

    @property
    def cause(self) -> int | None:
        ie = self.get_ie(C.IE_CAUSE)
        return ie.cause if ie else None


class MBMSSessionStopRequest(GTPv2Message):
    msg_type = C.MSG_MBMS_SESSION_STOP_REQ

    def set_tmgi(self, data: bytes) -> "MBMSSessionStopRequest":
        self.add_ie(_raw_ie(C.IE_TMGI, data))
        return self

    def set_mbms_flow_id(self, data: bytes) -> "MBMSSessionStopRequest":
        self.add_ie(_raw_ie(C.IE_MBMS_FLOW_ID, data))
        return self


class MBMSSessionStopResponse(GTPv2Message):
    msg_type = C.MSG_MBMS_SESSION_STOP_RES

    def set_cause(self, cause: int) -> "MBMSSessionStopResponse":
        self.add_ie(CauseIE(cause))
        return self

    @property
    def cause(self) -> int | None:
        ie = self.get_ie(C.IE_CAUSE)
        return ie.cause if ie else None
