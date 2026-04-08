"""GTPv1 IE base class.

Two IE encoding formats (TS 29.060 §7.7):
  TV  (type-value):  bit 7 of type byte = 0, fixed-length per TV_LEN dict
  TLV (type-length-value): bit 7 of type byte = 1, 2-byte length field follows
"""

import struct
from gtpc.v1 import constants as C


class IEv1:
    """Generic GTPv1 Information Element.

    Subclass and override `ie_type`, `_encode_value()`, `_decode_value()`.
    """

    ie_type: int = 0

    def __init__(self, value: bytes = b""):
        self.value = value

    # ------------------------------------------------------------------
    # Encoding
    # ------------------------------------------------------------------

    @property
    def is_tlv(self) -> bool:
        return self.ie_type >= 128

    def encode(self) -> bytes:
        val = self._encode_value()
        if self.is_tlv:
            return struct.pack("!BH", self.ie_type, len(val)) + val
        else:
            return bytes([self.ie_type]) + val

    def _encode_value(self) -> bytes:
        return self.value

    # ------------------------------------------------------------------
    # Decoding
    # ------------------------------------------------------------------

    @classmethod
    def decode(cls, buf: bytes) -> "IEv1":
        ie_type = buf[0]
        if ie_type >= 128:
            length = struct.unpack_from("!H", buf, 1)[0]
            value = buf[3:3 + length]
        else:
            length = C.TV_LEN.get(ie_type, 0)
            value = buf[1:1 + length]
        obj = cls.__new__(cls)
        obj.ie_type = ie_type
        obj.value = value
        obj._decode_value(value)
        return obj

    def _decode_value(self, value: bytes) -> None:
        pass

    def wire_len(self) -> int:
        val_len = len(self._encode_value())
        return (3 + val_len) if self.is_tlv else (1 + val_len)

    def __bytes__(self) -> bytes:
        return self.encode()

    def __repr__(self) -> str:
        name = C.IE_TYPE_NAMES.get(self.ie_type, f"IE-{self.ie_type}")
        return f"{name}({self.value.hex()})"


def decode_ies(buf: bytes) -> list[IEv1]:
    """Decode all IEs from a buffer, returning a list of IEv1 instances."""
    from gtpc.v1.ie.registry import IE_REGISTRY

    ies: list[IEv1] = []
    offset = 0
    while offset < len(buf):
        ie_type = buf[offset]
        if ie_type >= 128:
            if offset + 3 > len(buf):
                break
            length = struct.unpack_from("!H", buf, offset + 1)[0]
            end = offset + 3 + length
        else:
            length = C.TV_LEN.get(ie_type, 0)
            end = offset + 1 + length

        if end > len(buf):
            break

        ie_buf = buf[offset:end]
        klass = IE_REGISTRY.get(ie_type, IEv1)
        ie = klass.decode(ie_buf)
        ies.append(ie)
        offset = end
    return ies
