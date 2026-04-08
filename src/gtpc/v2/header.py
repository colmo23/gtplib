"""GTPv2-C header encode/decode.

Wire format (3GPP TS 29.274 §5.1):

  Byte 0: flags
    bits 7-5  version = 0b010
    bit  4    P flag (Piggybacking)
    bit  3    T flag (TEID present)
    bits 2-0  spare = 0
  Byte 1: Message Type
  Bytes 2-3: Message Length (octets after byte 3, i.e. excludes first 4 bytes)

  If T flag = 1:
    Bytes 4-7: TEID (32-bit)
    Bytes 8-10: Sequence Number (24-bit)
    Byte  11:  Spare
  If T flag = 0:
    Bytes 4-6: Sequence Number (24-bit)
    Byte  7:   Spare
"""

import struct
from dataclasses import dataclass


@dataclass
class GTPv2Header:
    msg_type: int = 0
    teid: int | None = None      # None → T flag = 0
    seq_num: int = 0
    p_flag: bool = False
    VERSION = 2

    @property
    def t_flag(self) -> bool:
        return self.teid is not None

    @property
    def _flags_byte(self) -> int:
        flags = (self.VERSION << 5)
        if self.p_flag:
            flags |= 0x10
        if self.t_flag:
            flags |= 0x08
        return flags

    def encode(self, payload_len: int) -> bytes:
        """Return encoded header bytes (8 or 12 bytes)."""
        # Length = bytes after first 4 (includes TEID if present, seq, spare, payload)
        if self.t_flag:
            length = 4 + 4 + payload_len  # teid(4) + seq(3) + spare(1) + payload
            hdr = struct.pack("!BBH", self._flags_byte, self.msg_type, length)
            hdr += struct.pack("!I", self.teid)
            hdr += struct.pack("!I", (self.seq_num << 8) & 0xFFFFFF00)
        else:
            length = 4 + payload_len  # seq(3) + spare(1) + payload
            hdr = struct.pack("!BBH", self._flags_byte, self.msg_type, length)
            hdr += struct.pack("!I", (self.seq_num << 8) & 0xFFFFFF00)
        return hdr

    @classmethod
    def decode(cls, buf: bytes) -> tuple["GTPv2Header", int]:
        """Decode header, return (header, offset_after_header)."""
        if len(buf) < 8:
            raise ValueError(f"Buffer too short for GTPv2 header: {len(buf)}")
        flags, msg_type, length = struct.unpack_from("!BBH", buf, 0)
        version = (flags >> 5) & 0x7
        if version != 2:
            raise ValueError(f"Not a GTPv2 packet (version={version})")
        p_flag = bool(flags & 0x10)
        t_flag = bool(flags & 0x08)

        if t_flag:
            if len(buf) < 12:
                raise ValueError("Buffer too short for GTPv2 header with TEID")
            teid = struct.unpack_from("!I", buf, 4)[0]
            seq_num = (struct.unpack_from("!I", buf, 8)[0] >> 8) & 0xFFFFFF
            offset = 12
        else:
            teid = None
            seq_num = (struct.unpack_from("!I", buf, 4)[0] >> 8) & 0xFFFFFF
            offset = 8

        hdr = cls(msg_type=msg_type, teid=teid, seq_num=seq_num, p_flag=p_flag)
        return hdr, offset

    @property
    def wire_length(self) -> int:
        return 12 if self.t_flag else 8

    def __repr__(self) -> str:
        return (
            f"GTPv2Header(type={self.msg_type}, teid=0x{self.teid or 0:08x}, "
            f"seq={self.seq_num})"
        )
