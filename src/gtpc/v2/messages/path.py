"""GTPv2-C path management messages."""

from gtpc.v2.messages.base import GTPv2Message
from gtpc.v2.ie.typed import RecoveryIE
from gtpc.v2 import constants as C


class EchoRequest(GTPv2Message):
    msg_type = C.MSG_ECHO_REQ

    def set_recovery(self, restart_counter: int) -> "EchoRequest":
        self.add_ie(RecoveryIE(restart_counter))
        return self


class EchoResponse(GTPv2Message):
    msg_type = C.MSG_ECHO_RES

    def set_recovery(self, restart_counter: int) -> "EchoResponse":
        self.add_ie(RecoveryIE(restart_counter))
        return self

    @property
    def recovery(self) -> int | None:
        ie = self.get_ie(C.IE_RECOVERY)
        return ie.restart_counter if ie else None


class VersionNotSupported(GTPv2Message):
    msg_type = C.MSG_VERSION_NOT_SUPPORTED
