"""GTPv1-C header encode/decode.

Wire format (3GPP TS 29.060 §6):

  Byte 0: flags
    bits 7-5  version = 0b001
    bit  4    PT  (Protocol Type, 1 = GTP)
    bit  3    spare = 0
    bit  2    E   (Extension Header present)
    bit  1    S   (Sequence Number present)
    bit  0    PN  (N-PDU Number present)
  Byte 1: Message Type
  Bytes 2-3: Length (payload, not including first 8 bytes)
  Bytes 4-7: TEID (Tunnel Endpoint Identifier)

  If any of E, S, PN is set (bytes 8-11 always present):
    Bytes 8-9:  Sequence Number
    Byte  10:   N-PDU Number
    Byte  11:   Next Extension Header Type
"""

import struct
from dataclasses import dataclass, field


@dataclass
class GTPv1Header:
    msg_type: int = 0
    teid: int = 0
    seq_num: int | None = None   # None → S flag = 0 (and 8-11 omitted)
    npdu: int = 0
    next_ext_hdr: int = 0
    e_flag: bool = False
    # version and PT are fixed at 1 and 1 respectively
    VERSION = 1
    PT = 1

    # Derived flag helpers
    @property
    def s_flag(self) -> bool:
        return self.seq_num is not None

    @property
    def _flags_byte(self) -> int:
        flags = (self.VERSION << 5) | (self.PT << 4)
        if self.e_flag:
            flags |= 0x04
        if self.s_flag:
            flags |= 0x02
        if self.npdu:
            flags |= 0x01
        return flags

    def encode(self, payload_len: int) -> bytes:
        """Return the encoded header bytes (8 or 12 bytes)."""
        hdr = struct.pack("!BBHI",
                          self._flags_byte,
                          self.msg_type,
                          payload_len,
                          self.teid)
        if self.s_flag or self.e_flag or self.npdu:
            sn = self.seq_num if self.seq_num is not None else 0
            hdr += struct.pack("!HBB", sn, self.npdu, self.next_ext_hdr)
        return hdr

    @classmethod
    def decode(cls, buf: bytes) -> tuple["GTPv1Header", int]:
        """Decode header from buf, return (header, offset_after_header)."""
        if len(buf) < 8:
            raise ValueError(f"Buffer too short for GTPv1 header: {len(buf)}")
        flags, msg_type, length, teid = struct.unpack_from("!BBHI", buf, 0)
        version = (flags >> 5) & 0x7
        if version != 1:
            raise ValueError(f"Not a GTPv1 packet (version={version})")
        e_flag = bool(flags & 0x04)
        s_flag = bool(flags & 0x02)
        pn_flag = bool(flags & 0x01)

        offset = 8
        seq_num = None
        npdu = 0
        next_ext_hdr = 0

        if e_flag or s_flag or pn_flag:
            if len(buf) < 12:
                raise ValueError("Buffer too short for GTPv1 extended header")
            seq_num, npdu, next_ext_hdr = struct.unpack_from("!HBB", buf, 8)
            offset = 12

        hdr = cls(
            msg_type=msg_type,
            teid=teid,
            seq_num=seq_num if s_flag else None,
            npdu=npdu,
            next_ext_hdr=next_ext_hdr,
            e_flag=e_flag,
        )
        return hdr, offset

    @property
    def wire_length(self) -> int:
        """Header size on the wire in bytes."""
        return 12 if (self.s_flag or self.e_flag or self.npdu) else 8

    def __repr__(self) -> str:
        return (
            f"GTPv1Header(type={self.msg_type}, teid=0x{self.teid:08x}, "
            f"seq={self.seq_num}, npdu={self.npdu})"
        )
