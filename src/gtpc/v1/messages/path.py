"""GTPv1-C path management messages (Echo, Version Not Supported)."""

from gtpc.v1.messages.base import GTPv1Message
from gtpc.v1.ie.tv import RecoveryIE
from gtpc.v1 import constants as C


class EchoRequest(GTPv1Message):
    msg_type = C.MSG_ECHO_REQ

    def set_recovery(self, restart_counter: int) -> "EchoRequest":
        self.add_ie(RecoveryIE(restart_counter))
        return self


class EchoResponse(GTPv1Message):
    msg_type = C.MSG_ECHO_RES

    def set_recovery(self, restart_counter: int) -> "EchoResponse":
        self.add_ie(RecoveryIE(restart_counter))
        return self

    @property
    def recovery(self) -> int | None:
        ie = self.get_ie(C.IE_RECOVERY)
        return ie.restart_counter if ie else None


class VersionNotSupported(GTPv1Message):
    msg_type = C.MSG_VERSION_NOT_SUPPORTED
