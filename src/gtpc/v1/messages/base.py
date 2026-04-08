"""GTPv1Message base class — wraps header + IE list."""

from __future__ import annotations
from typing import TYPE_CHECKING, TypeVar, Type

from gtpc.v1.header import GTPv1Header
from gtpc.v1.ie.base import IEv1, decode_ies
from gtpc.v1 import constants as C

Self = TypeVar("Self", bound="GTPv1Message")


class GTPv1Message:
    """Base for all GTPv1-C messages.

    Subclasses set `msg_type` at the class level.
    """
    msg_type: int = 0

    def __init__(self, teid: int = 0, seq_num: int | None = None):
        self.header = GTPv1Header(
            msg_type=self.__class__.msg_type,
            teid=teid,
            seq_num=seq_num,
        )
        self.ies: list[IEv1] = []

    # ------------------------------------------------------------------
    # IE access helpers
    # ------------------------------------------------------------------

    def add_ie(self, ie: IEv1) -> "GTPv1Message":
        """Append an IE; returns self for chaining."""
        self.ies.append(ie)
        return self

    def get_ie(self, ie_type: int) -> IEv1 | None:
        """Return first IE of the given type, or None."""
        for ie in self.ies:
            if ie.ie_type == ie_type:
                return ie
        return None

    def get_ies(self, ie_type: int) -> list[IEv1]:
        """Return all IEs of the given type."""
        return [ie for ie in self.ies if ie.ie_type == ie_type]

    # ------------------------------------------------------------------
    # Encode / decode
    # ------------------------------------------------------------------

    def encode(self) -> bytes:
        """Encode the full GTPv1-C packet to bytes."""
        payload = b"".join(ie.encode() for ie in self.ies)
        # The 4-byte seqnum/npdu/next_ext block is included when S flag is set
        extra = b""
        if self.header.s_flag or self.header.e_flag or self.header.npdu:
            sn = self.header.seq_num if self.header.seq_num is not None else 0
            import struct
            extra = struct.pack("!HBB", sn, self.header.npdu, self.header.next_ext_hdr)
        body = extra + payload
        return self.header.encode(len(body)) + payload

    @classmethod
    def decode(cls: Type[Self], buf: bytes) -> Self:
        """Decode from raw bytes into a message of this class."""
        hdr, offset = GTPv1Header.decode(buf)
        body = buf[offset:]
        obj = cls.__new__(cls)
        obj.header = hdr
        obj.ies = decode_ies(body)
        return obj

    # ------------------------------------------------------------------
    # Repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        name = C.MSG_TYPE_NAMES.get(self.msg_type, f"GTPv1-msg-{self.msg_type}")
        return (
            f"{name}("
            f"teid=0x{self.header.teid:08x}, "
            f"seq={self.header.seq_num}, "
            f"ies={self.ies!r})"
        )
