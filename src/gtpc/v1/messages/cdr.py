"""GTPv1-C CDR transfer messages (Data Record Transfer)."""

from gtpc.v1.messages.base import GTPv1Message
from gtpc.v1.ie.tv import CauseIE
from gtpc.v1.ie.base import IEv1
from gtpc.v1 import constants as C


class DataRecordTransferRequest(GTPv1Message):
    msg_type = C.MSG_DATA_RECORD_TRANSFER_REQ

    def set_packet_transfer_command(self, cmd: int) -> "DataRecordTransferRequest":
        # Packet Transfer Command is a TV IE (type = 126, 1 byte value)
        ie = IEv1.__new__(IEv1)
        ie.ie_type = 126  # GTP' specific
        ie.value = bytes([cmd])
        self.add_ie(ie)
        return self

    def set_data_record_packet(self, data: bytes) -> "DataRecordTransferRequest":
        ie = IEv1.__new__(IEv1)
        ie.ie_type = 252  # Data Record Packet TLV
        ie.value = data
        self.add_ie(ie)
        return self


class DataRecordTransferResponse(GTPv1Message):
    msg_type = C.MSG_DATA_RECORD_TRANSFER_RES

    def set_cause(self, cause: int) -> "DataRecordTransferResponse":
        self.add_ie(CauseIE(cause))
        return self

    def set_requests_responded(self, seq_nums: list[int]) -> "DataRecordTransferResponse":
        import struct
        data = b"".join(struct.pack("!H", s) for s in seq_nums)
        ie = IEv1.__new__(IEv1)
        ie.ie_type = 253  # Requests Responded TLV
        ie.value = data
        self.add_ie(ie)
        return self
