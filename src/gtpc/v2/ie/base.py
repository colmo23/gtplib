"""GTPv2 IE base class — TLIV encoding.

Wire format (TS 29.274 §8.1):
  Byte 0:    IE Type
  Bytes 1-2: Length (value bytes only, excluding type/length/instance)
  Byte 3:    Spare (bits 7-4) + Instance (bits 3-0)
  Bytes 4-n: Value
"""

import struct
from gtpc.v2 import constants as C


class IEv2:
    """Generic GTPv2 Information Element.

    Subclass and override `ie_type`, `_encode_value()`, `_decode_value()`.
    """
    ie_type: int = 0

    def __init__(self, value: bytes = b"", instance: int = 0):
        self.value = value
        self.instance = instance

    # ------------------------------------------------------------------
    # Encoding
    # ------------------------------------------------------------------

    def encode(self) -> bytes:
        val = self._encode_value()
        return struct.pack("!BHB", self.ie_type, len(val), self.instance & 0x0F) + val

    def _encode_value(self) -> bytes:
        return self.value

    # ------------------------------------------------------------------
    # Decoding
    # ------------------------------------------------------------------

    @classmethod
    def decode(cls, buf: bytes) -> "IEv2":
        if len(buf) < 4:
            raise ValueError("IE buffer too short")
        ie_type, length, instance = struct.unpack_from("!BHB", buf, 0)
        value = buf[4:4 + length]
        obj = cls.__new__(cls)
        obj.ie_type = ie_type
        obj.instance = instance & 0x0F
        obj.value = value
        obj._decode_value(value)
        return obj

    def _decode_value(self, value: bytes) -> None:
        pass

    def wire_len(self) -> int:
        return 4 + len(self._encode_value())

    def __bytes__(self) -> bytes:
        return self.encode()

    def __repr__(self) -> str:
        name = C.IE_TYPE_NAMES.get(self.ie_type, f"IE-{self.ie_type}")
        return f"{name}(inst={self.instance}, {self.value.hex()})"


def decode_ies(buf: bytes) -> list[IEv2]:
    """Decode all IEs from a GTPv2 payload buffer."""
    from gtpc.v2.ie.registry import IE_REGISTRY

    ies: list[IEv2] = []
    offset = 0
    while offset + 4 <= len(buf):
        ie_type, length, instance = struct.unpack_from("!BHB", buf, offset)
        end = offset + 4 + length
        if end > len(buf):
            break
        ie_buf = buf[offset:end]
        klass = IE_REGISTRY.get(ie_type, IEv2)
        ie = klass.decode(ie_buf)
        ies.append(ie)
        offset = end
    return ies
