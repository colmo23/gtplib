"""GTPv2Message base class — wraps header + IE list."""

from __future__ import annotations
from typing import TypeVar, Type

from gtpc.v2.header import GTPv2Header
from gtpc.v2.ie.base import IEv2, decode_ies
from gtpc.v2 import constants as C

Self = TypeVar("Self", bound="GTPv2Message")


class GTPv2Message:
    """Base for all GTPv2-C messages.

    Subclasses set `msg_type` at the class level.
    """
    msg_type: int = 0

    def __init__(self, teid: int | None = None, seq_num: int = 0):
        self.header = GTPv2Header(
            msg_type=self.__class__.msg_type,
            teid=teid,
            seq_num=seq_num,
        )
        self.ies: list[IEv2] = []

    # ------------------------------------------------------------------
    # IE access helpers
    # ------------------------------------------------------------------

    def add_ie(self, ie: IEv2) -> "GTPv2Message":
        self.ies.append(ie)
        return self

    def get_ie(self, ie_type: int, instance: int = 0) -> IEv2 | None:
        for ie in self.ies:
            if ie.ie_type == ie_type and ie.instance == instance:
                return ie
        return None

    def get_ies(self, ie_type: int) -> list[IEv2]:
        return [ie for ie in self.ies if ie.ie_type == ie_type]

    # ------------------------------------------------------------------
    # Encode / decode
    # ------------------------------------------------------------------

    def encode(self) -> bytes:
        payload = b"".join(ie.encode() for ie in self.ies)
        return self.header.encode(len(payload)) + payload

    @classmethod
    def decode(cls: Type[Self], buf: bytes) -> Self:
        hdr, offset = GTPv2Header.decode(buf)
        body = buf[offset:]
        obj = cls.__new__(cls)
        obj.header = hdr
        obj.ies = decode_ies(body)
        return obj

    # ------------------------------------------------------------------
    # Repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        name = C.MSG_TYPE_NAMES.get(self.msg_type, f"GTPv2-msg-{self.msg_type}")
        return (
            f"{name}("
            f"teid={self.header.teid!r}, "
            f"seq={self.header.seq_num}, "
            f"ies={self.ies!r})"
        )
