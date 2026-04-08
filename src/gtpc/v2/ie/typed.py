"""All typed GTPv2 IE subclasses with field-level encode/decode.

Mirrors Wireshark's packet-gtpv2.c dissector functions.
"""

import struct
import socket
from gtpc.v2.ie.base import IEv2
from gtpc.v2 import constants as C
from gtpc.utils import bcd, plmn


# ---------------------------------------------------------------------------
# IMSI (type 1)
# ---------------------------------------------------------------------------
class IMSIIE(IEv2):
    ie_type = C.IE_IMSI

    def __init__(self, digits: str = "", instance: int = 0):
        self.digits = digits
        self.instance = instance

    def _encode_value(self) -> bytes:
        return bcd.encode(self.digits)

    def _decode_value(self, value: bytes) -> None:
        self.digits = bcd.decode(value)

    def __repr__(self) -> str:
        return f"IMSIIE(digits={self.digits!r})"


# ---------------------------------------------------------------------------
# Cause (type 2)
# ---------------------------------------------------------------------------
class CauseIE(IEv2):
    ie_type = C.IE_CAUSE

    def __init__(self, cause: int = 0, pce: bool = False,
                 bce: bool = False, cs: bool = False, instance: int = 0):
        self.cause = cause
        self.pce = pce   # P: PDN Connection Entity
        self.bce = bce   # B: Bearer Context Entity
        self.cs = cs     # C: CS Transmission
        self.instance = instance

    def _encode_value(self) -> bytes:
        flags = (0x04 if self.pce else 0) | (0x02 if self.bce else 0) | (0x01 if self.cs else 0)
        return bytes([self.cause, flags, 0, 0])

    def _decode_value(self, value: bytes) -> None:
        self.cause = value[0] if value else 0
        flags = value[1] if len(value) > 1 else 0
        self.pce = bool(flags & 0x04)
        self.bce = bool(flags & 0x02)
        self.cs = bool(flags & 0x01)

    def __repr__(self) -> str:
        return f"CauseIE(cause={self.cause}, pce={self.pce}, bce={self.bce}, cs={self.cs})"


# ---------------------------------------------------------------------------
# Recovery (type 3)
# ---------------------------------------------------------------------------
class RecoveryIE(IEv2):
    ie_type = C.IE_RECOVERY

    def __init__(self, restart_counter: int = 0, instance: int = 0):
        self.restart_counter = restart_counter
        self.instance = instance

    def _encode_value(self) -> bytes:
        return bytes([self.restart_counter & 0xFF])

    def _decode_value(self, value: bytes) -> None:
        self.restart_counter = value[0] if value else 0

    def __repr__(self) -> str:
        return f"RecoveryIE(rc={self.restart_counter})"


# ---------------------------------------------------------------------------
# APN (type 71)
# ---------------------------------------------------------------------------
class APNIE(IEv2):
    ie_type = C.IE_APN

    def __init__(self, apn: str = "", instance: int = 0):
        self.apn = apn
        self.instance = instance

    def _encode_value(self) -> bytes:
        if not self.apn:
            return b"\x00"
        out = bytearray()
        for label in self.apn.split("."):
            enc = label.encode("ascii")
            out.append(len(enc))
            out.extend(enc)
        return bytes(out)

    def _decode_value(self, value: bytes) -> None:
        labels = []
        i = 0
        while i < len(value):
            ln = value[i]; i += 1
            if ln == 0:
                break
            labels.append(value[i:i + ln].decode("ascii", errors="replace"))
            i += ln
        self.apn = ".".join(labels)

    def __repr__(self) -> str:
        return f"APNIE(apn={self.apn!r})"


# ---------------------------------------------------------------------------
# AMBR (type 72) — Aggregate Maximum Bit Rate
# ---------------------------------------------------------------------------
class AMBRIE(IEv2):
    ie_type = C.IE_AMBR

    def __init__(self, uplink_kbps: int = 0, downlink_kbps: int = 0, instance: int = 0):
        self.uplink_kbps = uplink_kbps
        self.downlink_kbps = downlink_kbps
        self.instance = instance

    def _encode_value(self) -> bytes:
        return struct.pack("!II", self.uplink_kbps, self.downlink_kbps)

    def _decode_value(self, value: bytes) -> None:
        if len(value) >= 8:
            self.uplink_kbps, self.downlink_kbps = struct.unpack_from("!II", value)
        else:
            self.uplink_kbps = self.downlink_kbps = 0

    def __repr__(self) -> str:
        return f"AMBRIE(ul={self.uplink_kbps}kbps, dl={self.downlink_kbps}kbps)"


# ---------------------------------------------------------------------------
# EBI (type 73) — EPS Bearer ID
# ---------------------------------------------------------------------------
class EBIIE(IEv2):
    ie_type = C.IE_EBI

    def __init__(self, ebi: int = 0, instance: int = 0):
        self.ebi = ebi
        self.instance = instance

    def _encode_value(self) -> bytes:
        return bytes([0xF0 | (self.ebi & 0x0F)])

    def _decode_value(self, value: bytes) -> None:
        self.ebi = (value[0] & 0x0F) if value else 0

    def __repr__(self) -> str:
        return f"EBIIE(ebi={self.ebi})"


# ---------------------------------------------------------------------------
# IP Address (type 74)
# ---------------------------------------------------------------------------
class IPAddressIE(IEv2):
    ie_type = C.IE_IP_ADDRESS

    def __init__(self, address: str = "0.0.0.0", instance: int = 0):
        self.address = address  # dotted-decimal or colon-hex
        self.instance = instance

    def _encode_value(self) -> bytes:
        try:
            return socket.inet_pton(socket.AF_INET, self.address)
        except OSError:
            return socket.inet_pton(socket.AF_INET6, self.address)

    def _decode_value(self, value: bytes) -> None:
        if len(value) == 4:
            self.address = socket.inet_ntop(socket.AF_INET, value)
        elif len(value) == 16:
            self.address = socket.inet_ntop(socket.AF_INET6, value)
        else:
            self.address = value.hex()

    def __repr__(self) -> str:
        return f"IPAddressIE({self.address})"


# ---------------------------------------------------------------------------
# MEI (type 75) — Mobile Equipment Identity (IMEI/IMEI-SV)
# ---------------------------------------------------------------------------
class MEIIE(IEv2):
    ie_type = C.IE_MEI

    def __init__(self, digits: str = "", instance: int = 0):
        self.digits = digits
        self.instance = instance

    def _encode_value(self) -> bytes:
        return bcd.encode(self.digits)

    def _decode_value(self, value: bytes) -> None:
        self.digits = bcd.decode(value)


# ---------------------------------------------------------------------------
# MSISDN (type 76)
# ---------------------------------------------------------------------------
class MSISDNIE(IEv2):
    ie_type = C.IE_MSISDN

    def __init__(self, digits: str = "", instance: int = 0):
        self.digits = digits
        self.instance = instance

    def _encode_value(self) -> bytes:
        return b"\x91" + bcd.encode(self.digits)

    def _decode_value(self, value: bytes) -> None:
        self.digits = bcd.decode(value[1:]) if len(value) > 1 else ""

    def __repr__(self) -> str:
        return f"MSISDNIE(digits={self.digits!r})"


# ---------------------------------------------------------------------------
# Indication (type 77) — 64-bit flags bitmap
# ---------------------------------------------------------------------------
class IndicationIE(IEv2):
    ie_type = C.IE_INDICATION

    def __init__(self, flags: int = 0, instance: int = 0):
        self.flags = flags  # raw bitmask (up to 8 bytes)
        self.instance = instance

    def _encode_value(self) -> bytes:
        # Encode only as many bytes as needed
        n = max(1, (self.flags.bit_length() + 7) // 8)
        return self.flags.to_bytes(n, "big")

    def _decode_value(self, value: bytes) -> None:
        self.flags = int.from_bytes(value, "big") if value else 0


# ---------------------------------------------------------------------------
# PCO (type 78)
# ---------------------------------------------------------------------------
class PCOIE(IEv2):
    ie_type = C.IE_PCO

    def __init__(self, data: bytes = b"", instance: int = 0):
        self.data = data
        self.instance = instance

    def _encode_value(self) -> bytes:
        return self.data

    def _decode_value(self, value: bytes) -> None:
        self.data = value


# ---------------------------------------------------------------------------
# PAA (type 79) — PDN Address Allocation
# ---------------------------------------------------------------------------
class PAAIE(IEv2):
    ie_type = C.IE_PAA

    def __init__(self, pdn_type: int = C.PDN_TYPE_IPv4,
                 address: str = "0.0.0.0", instance: int = 0):
        self.pdn_type = pdn_type
        self.address = address
        self.instance = instance

    def _encode_value(self) -> bytes:
        b = bytes([self.pdn_type & 0x07])
        if self.pdn_type == C.PDN_TYPE_IPv4:
            b += socket.inet_pton(socket.AF_INET, self.address)
        elif self.pdn_type == C.PDN_TYPE_IPv6:
            b += bytes([0])  # PDN prefix length
            b += socket.inet_pton(socket.AF_INET6, self.address)
        elif self.pdn_type == C.PDN_TYPE_IPv4v6:
            b += bytes([0])  # IPv6 prefix length
            b += socket.inet_pton(socket.AF_INET6, "::") # placeholder
            b += socket.inet_pton(socket.AF_INET, self.address)
        return b

    def _decode_value(self, value: bytes) -> None:
        self.pdn_type = value[0] & 0x07 if value else C.PDN_TYPE_IPv4
        if self.pdn_type == C.PDN_TYPE_IPv4 and len(value) >= 5:
            self.address = socket.inet_ntop(socket.AF_INET, value[1:5])
        elif self.pdn_type == C.PDN_TYPE_IPv6 and len(value) >= 18:
            self.address = socket.inet_ntop(socket.AF_INET6, value[2:18])
        elif self.pdn_type == C.PDN_TYPE_IPv4v6 and len(value) >= 22:
            self.address = socket.inet_ntop(socket.AF_INET, value[18:22])
        else:
            self.address = "0.0.0.0"

    def __repr__(self) -> str:
        return f"PAAIE(type={self.pdn_type}, addr={self.address})"


# ---------------------------------------------------------------------------
# Bearer QoS (type 80)
# ---------------------------------------------------------------------------
class BearerQoSIE(IEv2):
    ie_type = C.IE_BEARER_QOS

    def __init__(self, pci: bool = False, pl: int = 0, pvi: bool = False,
                 qci: int = 0, mbr_ul: int = 0, mbr_dl: int = 0,
                 gbr_ul: int = 0, gbr_dl: int = 0, instance: int = 0):
        self.pci = pci
        self.pl = pl      # Priority Level (4 bits)
        self.pvi = pvi
        self.qci = qci    # QoS Class Identifier
        self.mbr_ul = mbr_ul
        self.mbr_dl = mbr_dl
        self.gbr_ul = gbr_ul
        self.gbr_dl = gbr_dl
        self.instance = instance

    def _encode_value(self) -> bytes:
        arp_byte = ((1 if self.pci else 0) << 6) | ((self.pl & 0x0F) << 2) | (1 if self.pvi else 0)
        # MBR/GBR are 5 bytes each (40 bits)
        def pack5(v: int) -> bytes:
            return v.to_bytes(5, "big")
        return (bytes([arp_byte, self.qci]) +
                pack5(self.mbr_ul) + pack5(self.mbr_dl) +
                pack5(self.gbr_ul) + pack5(self.gbr_dl))

    def _decode_value(self, value: bytes) -> None:
        if len(value) < 22:
            return
        arp = value[0]
        self.pci = bool(arp & 0x40)
        self.pl = (arp >> 2) & 0x0F
        self.pvi = bool(arp & 0x01)
        self.qci = value[1]
        self.mbr_ul = int.from_bytes(value[2:7], "big")
        self.mbr_dl = int.from_bytes(value[7:12], "big")
        self.gbr_ul = int.from_bytes(value[12:17], "big")
        self.gbr_dl = int.from_bytes(value[17:22], "big")

    def __repr__(self) -> str:
        return f"BearerQoSIE(qci={self.qci}, pl={self.pl}, mbr_ul={self.mbr_ul}, mbr_dl={self.mbr_dl})"


# ---------------------------------------------------------------------------
# Flow QoS (type 81)
# ---------------------------------------------------------------------------
class FlowQoSIE(IEv2):
    ie_type = C.IE_FLOW_QOS

    def __init__(self, qci: int = 0, mbr_ul: int = 0, mbr_dl: int = 0,
                 gbr_ul: int = 0, gbr_dl: int = 0, instance: int = 0):
        self.qci = qci
        self.mbr_ul = mbr_ul
        self.mbr_dl = mbr_dl
        self.gbr_ul = gbr_ul
        self.gbr_dl = gbr_dl
        self.instance = instance

    def _encode_value(self) -> bytes:
        def pack5(v: int) -> bytes:
            return v.to_bytes(5, "big")
        return (bytes([self.qci]) +
                pack5(self.mbr_ul) + pack5(self.mbr_dl) +
                pack5(self.gbr_ul) + pack5(self.gbr_dl))

    def _decode_value(self, value: bytes) -> None:
        if len(value) < 21:
            return
        self.qci = value[0]
        self.mbr_ul = int.from_bytes(value[1:6], "big")
        self.mbr_dl = int.from_bytes(value[6:11], "big")
        self.gbr_ul = int.from_bytes(value[11:16], "big")
        self.gbr_dl = int.from_bytes(value[16:21], "big")


# ---------------------------------------------------------------------------
# RAT Type (type 82)
# ---------------------------------------------------------------------------
class RATTypeIE(IEv2):
    ie_type = C.IE_RAT_TYPE

    def __init__(self, rat: int = C.RAT_EUTRAN, instance: int = 0):
        self.rat = rat
        self.instance = instance

    def _encode_value(self) -> bytes:
        return bytes([self.rat])

    def _decode_value(self, value: bytes) -> None:
        self.rat = value[0] if value else 0

    def __repr__(self) -> str:
        return f"RATTypeIE(rat={self.rat})"


# ---------------------------------------------------------------------------
# Serving Network (type 83)
# ---------------------------------------------------------------------------
class ServingNetworkIE(IEv2):
    ie_type = C.IE_SERVING_NET

    def __init__(self, mcc: str = "000", mnc: str = "00", instance: int = 0):
        self.mcc = mcc
        self.mnc = mnc
        self.instance = instance

    def _encode_value(self) -> bytes:
        return plmn.encode(self.mcc, self.mnc)

    def _decode_value(self, value: bytes) -> None:
        self.mcc, self.mnc = plmn.decode(value[:3]) if len(value) >= 3 else ("000", "00")

    def __repr__(self) -> str:
        return f"ServingNetworkIE(mcc={self.mcc}, mnc={self.mnc})"


# ---------------------------------------------------------------------------
# Bearer TFT (type 84) — opaque
# ---------------------------------------------------------------------------
class BearerTFTIE(IEv2):
    ie_type = C.IE_BEARER_TFT

    def __init__(self, data: bytes = b"", instance: int = 0):
        self.data = data
        self.instance = instance

    def _encode_value(self) -> bytes:
        return self.data

    def _decode_value(self, value: bytes) -> None:
        self.data = value


# ---------------------------------------------------------------------------
# ULI (type 86) — User Location Information
# ---------------------------------------------------------------------------
class ULIIE(IEv2):
    ie_type = C.IE_ULI

    # Flags
    CGI_PRESENT  = 0x01
    SAI_PRESENT  = 0x02
    RAI_PRESENT  = 0x04
    TAI_PRESENT  = 0x08
    ECGI_PRESENT = 0x10
    LAI_PRESENT  = 0x20

    def __init__(self, flags: int = 0, cgi: bytes = b"",
                 sai: bytes = b"", rai: bytes = b"",
                 tai: bytes = b"", ecgi: bytes = b"",
                 lai: bytes = b"", instance: int = 0):
        self.flags = flags
        self.cgi = cgi    # 7 bytes: PLMN(3) + LAC(2) + CI(2)
        self.sai = sai    # 7 bytes: PLMN(3) + LAC(2) + SAC(2)
        self.rai = rai    # 7 bytes: PLMN(3) + LAC(2) + RAC(2)
        self.tai = tai    # 5 bytes: PLMN(3) + TAC(2)
        self.ecgi = ecgi  # 7 bytes: PLMN(3) + ECI(4)
        self.lai = lai    # 5 bytes: PLMN(3) + LAC(2)
        self.instance = instance

    def _encode_value(self) -> bytes:
        out = bytes([self.flags])
        if self.flags & self.CGI_PRESENT:
            out += self.cgi
        if self.flags & self.SAI_PRESENT:
            out += self.sai
        if self.flags & self.RAI_PRESENT:
            out += self.rai
        if self.flags & self.TAI_PRESENT:
            out += self.tai
        if self.flags & self.ECGI_PRESENT:
            out += self.ecgi
        if self.flags & self.LAI_PRESENT:
            out += self.lai
        return out

    def _decode_value(self, value: bytes) -> None:
        if not value:
            return
        self.flags = value[0]
        offset = 1
        if self.flags & self.CGI_PRESENT:
            self.cgi = value[offset:offset + 7]; offset += 7
        if self.flags & self.SAI_PRESENT:
            self.sai = value[offset:offset + 7]; offset += 7
        if self.flags & self.RAI_PRESENT:
            self.rai = value[offset:offset + 7]; offset += 7
        if self.flags & self.TAI_PRESENT:
            self.tai = value[offset:offset + 5]; offset += 5
        if self.flags & self.ECGI_PRESENT:
            self.ecgi = value[offset:offset + 7]; offset += 7
        if self.flags & self.LAI_PRESENT:
            self.lai = value[offset:offset + 5]; offset += 5

    @classmethod
    def with_tai(cls, mcc: str, mnc: str, tac: int, instance: int = 0) -> "ULIIE":
        tai = plmn.encode(mcc, mnc) + struct.pack("!H", tac)
        return cls(flags=cls.TAI_PRESENT, tai=tai, instance=instance)

    @classmethod
    def with_ecgi(cls, mcc: str, mnc: str, eci: int, instance: int = 0) -> "ULIIE":
        ecgi = plmn.encode(mcc, mnc) + struct.pack("!I", eci & 0x0FFFFFFF)
        return cls(flags=cls.ECGI_PRESENT, ecgi=ecgi, instance=instance)

    @classmethod
    def with_tai_and_ecgi(cls, mcc: str, mnc: str, tac: int,
                           eci: int, instance: int = 0) -> "ULIIE":
        tai = plmn.encode(mcc, mnc) + struct.pack("!H", tac)
        ecgi = plmn.encode(mcc, mnc) + struct.pack("!I", eci & 0x0FFFFFFF)
        return cls(flags=cls.TAI_PRESENT | cls.ECGI_PRESENT,
                   tai=tai, ecgi=ecgi, instance=instance)


# ---------------------------------------------------------------------------
# F-TEID (type 87) — Fully Qualified Tunnel Endpoint Identifier
# ---------------------------------------------------------------------------
class FTEIDIE(IEv2):
    ie_type = C.IE_F_TEID

    def __init__(self, interface_type: int = 0, teid: int = 0,
                 ipv4: str | None = None, ipv6: str | None = None,
                 instance: int = 0):
        self.interface_type = interface_type
        self.teid = teid
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.instance = instance

    def _encode_value(self) -> bytes:
        flags = self.interface_type & 0x3F
        if self.ipv4:
            flags |= 0x80
        if self.ipv6:
            flags |= 0x40
        out = bytes([flags]) + struct.pack("!I", self.teid)
        if self.ipv4:
            out += socket.inet_pton(socket.AF_INET, self.ipv4)
        if self.ipv6:
            out += socket.inet_pton(socket.AF_INET6, self.ipv6)
        return out

    def _decode_value(self, value: bytes) -> None:
        if not value:
            return
        flags = value[0]
        self.interface_type = flags & 0x3F
        has_ipv4 = bool(flags & 0x80)
        has_ipv6 = bool(flags & 0x40)
        self.teid = struct.unpack_from("!I", value, 1)[0]
        offset = 5
        if has_ipv4:
            self.ipv4 = socket.inet_ntop(socket.AF_INET, value[offset:offset + 4])
            offset += 4
        else:
            self.ipv4 = None
        if has_ipv6:
            self.ipv6 = socket.inet_ntop(socket.AF_INET6, value[offset:offset + 16])
        else:
            self.ipv6 = None

    def __repr__(self) -> str:
        return (f"FTEIDIE(if_type={self.interface_type}, teid=0x{self.teid:08x}, "
                f"ipv4={self.ipv4}, ipv6={self.ipv6})")


# ---------------------------------------------------------------------------
# Bearer Context (type 93) — grouped IE
# ---------------------------------------------------------------------------
class BearerContextIE(IEv2):
    ie_type = C.IE_BEARER_CTX

    def __init__(self, ies: list | None = None, instance: int = 0):
        self.grouped_ies: list[IEv2] = ies or []
        self.instance = instance

    def _encode_value(self) -> bytes:
        return b"".join(ie.encode() for ie in self.grouped_ies)

    def _decode_value(self, value: bytes) -> None:
        from gtpc.v2.ie.base import decode_ies
        self.grouped_ies = decode_ies(value)

    def add_ie(self, ie: "IEv2") -> "BearerContextIE":
        self.grouped_ies.append(ie)
        return self

    def get_ie(self, ie_type: int, instance: int = 0) -> "IEv2 | None":
        for ie in self.grouped_ies:
            if ie.ie_type == ie_type and ie.instance == instance:
                return ie
        return None

    def __repr__(self) -> str:
        return f"BearerContextIE(inst={self.instance}, ies={self.grouped_ies!r})"


# ---------------------------------------------------------------------------
# Charging ID (type 94)
# ---------------------------------------------------------------------------
class ChargingIDIE(IEv2):
    ie_type = C.IE_CHARGING_ID

    def __init__(self, charging_id: int = 0, instance: int = 0):
        self.charging_id = charging_id
        self.instance = instance

    def _encode_value(self) -> bytes:
        return struct.pack("!I", self.charging_id)

    def _decode_value(self, value: bytes) -> None:
        self.charging_id = struct.unpack_from("!I", value)[0] if len(value) >= 4 else 0


# ---------------------------------------------------------------------------
# Charging Characteristics (type 95)
# ---------------------------------------------------------------------------
class ChargingCharsIE(IEv2):
    ie_type = C.IE_CHARGING_CHARS

    def __init__(self, chars: int = 0, instance: int = 0):
        self.chars = chars
        self.instance = instance

    def _encode_value(self) -> bytes:
        return struct.pack("!H", self.chars)

    def _decode_value(self, value: bytes) -> None:
        self.chars = struct.unpack_from("!H", value)[0] if len(value) >= 2 else 0


# ---------------------------------------------------------------------------
# Bearer Flags (type 97)
# ---------------------------------------------------------------------------
class BearerFlagsIE(IEv2):
    ie_type = C.IE_BEARER_FLAGS

    def __init__(self, flags: int = 0, instance: int = 0):
        self.flags = flags
        self.instance = instance

    def _encode_value(self) -> bytes:
        return bytes([self.flags & 0xFF])

    def _decode_value(self, value: bytes) -> None:
        self.flags = value[0] if value else 0


# ---------------------------------------------------------------------------
# PDN Type (type 99)
# ---------------------------------------------------------------------------
class PDNTypeIE(IEv2):
    ie_type = C.IE_PDN_TYPE

    def __init__(self, pdn_type: int = C.PDN_TYPE_IPv4, instance: int = 0):
        self.pdn_type = pdn_type
        self.instance = instance

    def _encode_value(self) -> bytes:
        return bytes([0xF8 | (self.pdn_type & 0x07)])

    def _decode_value(self, value: bytes) -> None:
        self.pdn_type = (value[0] & 0x07) if value else C.PDN_TYPE_IPv4

    def __repr__(self) -> str:
        return f"PDNTypeIE(type={self.pdn_type})"


# ---------------------------------------------------------------------------
# PTI (type 100) — Procedure Transaction ID
# ---------------------------------------------------------------------------
class PTIIE(IEv2):
    ie_type = C.IE_PTI

    def __init__(self, pti: int = 0, instance: int = 0):
        self.pti = pti
        self.instance = instance

    def _encode_value(self) -> bytes:
        return bytes([self.pti & 0xFF])

    def _decode_value(self, value: bytes) -> None:
        self.pti = value[0] if value else 0


# ---------------------------------------------------------------------------
# UE Time Zone (type 114)
# ---------------------------------------------------------------------------
class UETimeZoneIE(IEv2):
    ie_type = C.IE_UE_TIME_ZONE

    def __init__(self, tz_byte: int = 0, dst: int = 0, instance: int = 0):
        self.tz_byte = tz_byte
        self.dst = dst
        self.instance = instance

    def _encode_value(self) -> bytes:
        return bytes([self.tz_byte, self.dst & 0x03])

    def _decode_value(self, value: bytes) -> None:
        self.tz_byte = value[0] if len(value) > 0 else 0
        self.dst = (value[1] & 0x03) if len(value) > 1 else 0


# ---------------------------------------------------------------------------
# APN Restriction (type 127)
# ---------------------------------------------------------------------------
class APNRestrictionIE(IEv2):
    ie_type = C.IE_APN_RESTRICTION

    def __init__(self, restriction: int = 0, instance: int = 0):
        self.restriction = restriction
        self.instance = instance

    def _encode_value(self) -> bytes:
        return bytes([self.restriction & 0xFF])

    def _decode_value(self, value: bytes) -> None:
        self.restriction = value[0] if value else 0


# ---------------------------------------------------------------------------
# Selection Mode (type 128)
# ---------------------------------------------------------------------------
class SelectionModeIE(IEv2):
    ie_type = C.IE_SEL_MODE

    def __init__(self, mode: int = 0, instance: int = 0):
        self.mode = mode
        self.instance = instance

    def _encode_value(self) -> bytes:
        return bytes([0xFC | (self.mode & 0x03)])

    def _decode_value(self, value: bytes) -> None:
        self.mode = (value[0] & 0x03) if value else 0


# ---------------------------------------------------------------------------
# FQ-CSID (type 132)
# ---------------------------------------------------------------------------
class FQCSIDIe(IEv2):
    ie_type = C.IE_FQ_CSID

    def __init__(self, node_id: bytes = b"\x00\x00\x00\x00",
                 csids: list[int] | None = None, instance: int = 0):
        self.node_id = node_id   # 4 bytes IPv4 or 16 bytes IPv6
        self.csids = csids or []
        self.instance = instance

    def _encode_value(self) -> bytes:
        node_id_type = 0 if len(self.node_id) == 4 else 1
        header = bytes([(node_id_type << 4) | (len(self.csids) & 0x0F)])
        csid_bytes = b"".join(struct.pack("!H", c) for c in self.csids)
        return header + self.node_id + csid_bytes

    def _decode_value(self, value: bytes) -> None:
        if not value:
            return
        node_id_type = (value[0] >> 4) & 0x0F
        num_csids = value[0] & 0x0F
        if node_id_type == 0:
            self.node_id = value[1:5]
            offset = 5
        else:
            self.node_id = value[1:17]
            offset = 17
        self.csids = []
        for _ in range(num_csids):
            if offset + 2 <= len(value):
                self.csids.append(struct.unpack_from("!H", value, offset)[0])
                offset += 2


# ---------------------------------------------------------------------------
# Node Type (type 135)
# ---------------------------------------------------------------------------
class NodeTypeIE(IEv2):
    ie_type = C.IE_NODE_TYPE

    def __init__(self, node_type: int = C.NODE_TYPE_MME, instance: int = 0):
        self.node_type = node_type
        self.instance = instance

    def _encode_value(self) -> bytes:
        return bytes([self.node_type & 0xFF])

    def _decode_value(self, value: bytes) -> None:
        self.node_type = value[0] if value else 0


# ---------------------------------------------------------------------------
# FQDN (type 136)
# ---------------------------------------------------------------------------
class FQDNIE(IEv2):
    ie_type = C.IE_FQDN

    def __init__(self, fqdn: str = "", instance: int = 0):
        self.fqdn = fqdn
        self.instance = instance

    def _encode_value(self) -> bytes:
        out = bytearray()
        for label in self.fqdn.rstrip(".").split("."):
            enc = label.encode("ascii")
            out.append(len(enc))
            out.extend(enc)
        out.append(0)
        return bytes(out)

    def _decode_value(self, value: bytes) -> None:
        labels, i = [], 0
        while i < len(value):
            ln = value[i]; i += 1
            if ln == 0:
                break
            labels.append(value[i:i + ln].decode("ascii", errors="replace"))
            i += ln
        self.fqdn = ".".join(labels)

    def __repr__(self) -> str:
        return f"FQDNIE(fqdn={self.fqdn!r})"


# ---------------------------------------------------------------------------
# ARP (type 155) — Allocation/Retention Priority
# ---------------------------------------------------------------------------
class ARPIE(IEv2):
    ie_type = C.IE_ARP

    def __init__(self, pl: int = 0, pci: bool = False, pvi: bool = False,
                 instance: int = 0):
        self.pl = pl    # Priority Level (4 bits, 1-15)
        self.pci = pci  # Pre-emption Capability
        self.pvi = pvi  # Pre-emption Vulnerability
        self.instance = instance

    def _encode_value(self) -> bytes:
        b = ((self.pl & 0x0F) << 2) | ((1 if self.pci else 0) << 1) | (1 if self.pvi else 0)
        return bytes([b])

    def _decode_value(self, value: bytes) -> None:
        if not value:
            return
        self.pl = (value[0] >> 2) & 0x0F
        self.pci = bool(value[0] & 0x02)
        self.pvi = bool(value[0] & 0x01)

    def __repr__(self) -> str:
        return f"ARPIE(pl={self.pl}, pci={self.pci}, pvi={self.pvi})"


# ---------------------------------------------------------------------------
# APCO (type 163) — Additional Protocol Config Options (opaque)
# ---------------------------------------------------------------------------
class APCOIE(IEv2):
    ie_type = C.IE_APCO

    def __init__(self, data: bytes = b"", instance: int = 0):
        self.data = data
        self.instance = instance

    def _encode_value(self) -> bytes:
        return self.data

    def _decode_value(self, value: bytes) -> None:
        self.data = value


# ---------------------------------------------------------------------------
# Private Extension (type 255)
# ---------------------------------------------------------------------------
class PrivateExtIE(IEv2):
    ie_type = C.IE_PRIVATE_EXT

    def __init__(self, enterprise_id: int = 0, value: bytes = b"", instance: int = 0):
        self.enterprise_id = enterprise_id
        self.ext_value = value
        self.instance = instance

    def _encode_value(self) -> bytes:
        return struct.pack("!H", self.enterprise_id) + self.ext_value

    def _decode_value(self, value: bytes) -> None:
        if len(value) >= 2:
            self.enterprise_id = struct.unpack_from("!H", value)[0]
            self.ext_value = value[2:]
        else:
            self.enterprise_id = 0
            self.ext_value = b""
