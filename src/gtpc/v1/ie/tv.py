"""GTPv1 TV (fixed-length) Information Elements.

Each IE covers a specific type byte (0–127) and has named field access.
"""

import struct
from gtpc.v1.ie.base import IEv1
from gtpc.v1 import constants as C
from gtpc.utils import bcd, plmn


class CauseIE(IEv1):
    ie_type = C.IE_CAUSE

    def __init__(self, cause: int = 0):
        self.cause = cause

    def _encode_value(self) -> bytes:
        return bytes([self.cause])

    def _decode_value(self, value: bytes) -> None:
        self.cause = value[0] if value else 0

    def __repr__(self) -> str:
        return f"CauseIE(cause={self.cause})"


class IMSIE(IEv1):
    ie_type = C.IE_IMSI

    def __init__(self, digits: str = ""):
        self.digits = digits

    def _encode_value(self) -> bytes:
        return bcd.encode(self.digits)

    def _decode_value(self, value: bytes) -> None:
        self.digits = bcd.decode(value)

    def __repr__(self) -> str:
        return f"IMSIIE(digits={self.digits!r})"


class RAIIE(IEv1):
    """Routing Area Identity: MCC, MNC, LAC, RAC."""
    ie_type = C.IE_RAI

    def __init__(self, mcc: str = "000", mnc: str = "00",
                 lac: int = 0, rac: int = 0):
        self.mcc = mcc
        self.mnc = mnc
        self.lac = lac
        self.rac = rac

    def _encode_value(self) -> bytes:
        return plmn.encode(self.mcc, self.mnc) + struct.pack("!HB", self.lac, self.rac)

    def _decode_value(self, value: bytes) -> None:
        self.mcc, self.mnc = plmn.decode(value[:3])
        self.lac, self.rac = struct.unpack_from("!HB", value, 3)

    def __repr__(self) -> str:
        return f"RAIIE(mcc={self.mcc}, mnc={self.mnc}, lac={self.lac}, rac={self.rac})"


class TLLIIE(IEv1):
    ie_type = C.IE_TLLI

    def __init__(self, tlli: int = 0):
        self.tlli = tlli

    def _encode_value(self) -> bytes:
        return struct.pack("!I", self.tlli)

    def _decode_value(self, value: bytes) -> None:
        self.tlli = struct.unpack_from("!I", value)[0]


class PTMSIIE(IEv1):
    ie_type = C.IE_P_TMSI

    def __init__(self, ptmsi: int = 0):
        self.ptmsi = ptmsi

    def _encode_value(self) -> bytes:
        return struct.pack("!I", self.ptmsi)

    def _decode_value(self, value: bytes) -> None:
        self.ptmsi = struct.unpack_from("!I", value)[0]


class ReorderRequiredIE(IEv1):
    ie_type = C.IE_REORDER_REQUIRED

    def __init__(self, required: bool = False):
        self.required = required

    def _encode_value(self) -> bytes:
        return bytes([0xFE | (1 if self.required else 0)])

    def _decode_value(self, value: bytes) -> None:
        self.required = bool(value[0] & 0x01) if value else False


class RecoveryIE(IEv1):
    ie_type = C.IE_RECOVERY

    def __init__(self, restart_counter: int = 0):
        self.restart_counter = restart_counter

    def _encode_value(self) -> bytes:
        return bytes([self.restart_counter & 0xFF])

    def _decode_value(self, value: bytes) -> None:
        self.restart_counter = value[0] if value else 0

    def __repr__(self) -> str:
        return f"RecoveryIE(restart_counter={self.restart_counter})"


class SelectionModeIE(IEv1):
    ie_type = C.IE_SELECTION_MODE

    def __init__(self, mode: int = 0):
        self.mode = mode  # 0=subscription verified, 1/2=not verified

    def _encode_value(self) -> bytes:
        return bytes([0xFC | (self.mode & 0x03)])

    def _decode_value(self, value: bytes) -> None:
        self.mode = (value[0] & 0x03) if value else 0

    def __repr__(self) -> str:
        return f"SelectionModeIE(mode={self.mode})"


class TEIDDataIIE(IEv1):
    """TEID Data I (4 bytes)."""
    ie_type = C.IE_TEID_DATA_1

    def __init__(self, teid: int = 0):
        self.teid = teid

    def _encode_value(self) -> bytes:
        return struct.pack("!I", self.teid)

    def _decode_value(self, value: bytes) -> None:
        self.teid = struct.unpack_from("!I", value)[0]

    def __repr__(self) -> str:
        return f"TEIDDataIIE(teid=0x{self.teid:08x})"


class TEIDCPlaneIE(IEv1):
    """TEID Control Plane (4 bytes)."""
    ie_type = C.IE_TEID_C_PLANE

    def __init__(self, teid: int = 0):
        self.teid = teid

    def _encode_value(self) -> bytes:
        return struct.pack("!I", self.teid)

    def _decode_value(self, value: bytes) -> None:
        self.teid = struct.unpack_from("!I", value)[0]

    def __repr__(self) -> str:
        return f"TEIDCPlaneIE(teid=0x{self.teid:08x})"


class TEIDDataIIIE(IEv1):
    """TEID Data II (5 bytes: 1-byte NSAPI + 4-byte TEID)."""
    ie_type = C.IE_TEID_DATA_2

    def __init__(self, nsapi: int = 0, teid: int = 0):
        self.nsapi = nsapi
        self.teid = teid

    def _encode_value(self) -> bytes:
        return bytes([self.nsapi & 0x0F]) + struct.pack("!I", self.teid)

    def _decode_value(self, value: bytes) -> None:
        self.nsapi = value[0] & 0x0F
        self.teid = struct.unpack_from("!I", value, 1)[0]


class TeardownIndIE(IEv1):
    ie_type = C.IE_TEARDOWN_IND

    def __init__(self, teardown: bool = False):
        self.teardown = teardown

    def _encode_value(self) -> bytes:
        return bytes([0xFE | (1 if self.teardown else 0)])

    def _decode_value(self, value: bytes) -> None:
        self.teardown = bool(value[0] & 0x01) if value else False


class NSAPIIE(IEv1):
    ie_type = C.IE_NSAPI

    def __init__(self, nsapi: int = 0):
        self.nsapi = nsapi

    def _encode_value(self) -> bytes:
        return bytes([0xF0 | (self.nsapi & 0x0F)])

    def _decode_value(self, value: bytes) -> None:
        self.nsapi = (value[0] & 0x0F) if value else 0

    def __repr__(self) -> str:
        return f"NSAPIIE(nsapi={self.nsapi})"


class ChargingCharsIE(IEv1):
    ie_type = C.IE_CHARGING_CHARS

    def __init__(self, chars: int = 0):
        self.chars = chars

    def _encode_value(self) -> bytes:
        return struct.pack("!H", self.chars)

    def _decode_value(self, value: bytes) -> None:
        self.chars = struct.unpack_from("!H", value)[0] if len(value) >= 2 else 0


class TraceReferenceIE(IEv1):
    ie_type = C.IE_TRACE_REFERENCE

    def __init__(self, ref: int = 0):
        self.ref = ref

    def _encode_value(self) -> bytes:
        return struct.pack("!H", self.ref)

    def _decode_value(self, value: bytes) -> None:
        self.ref = struct.unpack_from("!H", value)[0] if len(value) >= 2 else 0


class TraceTypeIE(IEv1):
    ie_type = C.IE_TRACE_TYPE

    def __init__(self, trace_type: int = 0):
        self.trace_type = trace_type

    def _encode_value(self) -> bytes:
        return struct.pack("!H", self.trace_type)

    def _decode_value(self, value: bytes) -> None:
        self.trace_type = struct.unpack_from("!H", value)[0] if len(value) >= 2 else 0


class ChargingIDIE(IEv1):
    ie_type = C.IE_CHARGING_ID

    def __init__(self, charging_id: int = 0):
        self.charging_id = charging_id

    def _encode_value(self) -> bytes:
        return struct.pack("!I", self.charging_id)

    def _decode_value(self, value: bytes) -> None:
        self.charging_id = struct.unpack_from("!I", value)[0] if len(value) >= 4 else 0

    def __repr__(self) -> str:
        return f"ChargingIDIE(id=0x{self.charging_id:08x})"
