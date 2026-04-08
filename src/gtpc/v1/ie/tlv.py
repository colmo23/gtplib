"""GTPv1 TLV (variable-length) Information Elements.

Each IE covers a specific type byte (128–255).
The wire format is: type(1B) + length(2B) + value(length bytes).
"""

import struct
from gtpc.v1.ie.base import IEv1
from gtpc.v1 import constants as C
from gtpc.utils import bcd, plmn


class EndUserAddressIE(IEv1):
    """End User Address — PDN type + IP address."""
    ie_type = C.IE_END_USER_ADDRESS

    # PDP Type Organisation values
    PTO_ETSI    = 0x00
    PTO_IETF    = 0x01

    # PDP Type Number values (IETF org)
    PDN_PPP     = 0x01
    PDN_IPv4    = 0x21
    PDN_IPv6    = 0x57
    PDN_IPv4v6  = 0x8D

    def __init__(self, pdp_type_org: int = PTO_IETF,
                 pdp_type_num: int = PDN_IPv4,
                 address: bytes = b""):
        self.pdp_type_org = pdp_type_org
        self.pdp_type_num = pdp_type_num
        self.address = address  # raw bytes (4 for IPv4, 16 for IPv6, 20 for dual)

    def _encode_value(self) -> bytes:
        return bytes([0xF0 | self.pdp_type_org, self.pdp_type_num]) + self.address

    def _decode_value(self, value: bytes) -> None:
        if len(value) >= 2:
            self.pdp_type_org = value[0] & 0x0F
            self.pdp_type_num = value[1]
            self.address = value[2:]
        else:
            self.pdp_type_org = self.PTO_IETF
            self.pdp_type_num = self.PDN_IPv4
            self.address = b""

    def __repr__(self) -> str:
        return f"EndUserAddressIE(type_org={self.pdp_type_org}, type_num=0x{self.pdp_type_num:02x}, addr={self.address.hex()})"


class APNIE(IEv1):
    """Access Point Name — label-encoded."""
    ie_type = C.IE_APN

    def __init__(self, apn: str = ""):
        self.apn = apn  # e.g. "internet.mnc001.mcc234.gprs"

    def _encode_value(self) -> bytes:
        if not self.apn:
            return b"\x00"
        out = bytearray()
        for label in self.apn.split("."):
            encoded = label.encode("ascii")
            out.append(len(encoded))
            out.extend(encoded)
        return bytes(out)

    def _decode_value(self, value: bytes) -> None:
        labels = []
        i = 0
        while i < len(value):
            ln = value[i]
            i += 1
            if ln == 0:
                break
            labels.append(value[i:i + ln].decode("ascii", errors="replace"))
            i += ln
        self.apn = ".".join(labels)

    def __repr__(self) -> str:
        return f"APNIE(apn={self.apn!r})"


class PCOIE(IEv1):
    """Protocol Configuration Options — opaque."""
    ie_type = C.IE_PCO

    def __init__(self, data: bytes = b""):
        self.data = data

    def _encode_value(self) -> bytes:
        return self.data

    def _decode_value(self, value: bytes) -> None:
        self.data = value


class GSNAddressIE(IEv1):
    """GSN Address — IPv4 (4 bytes) or IPv6 (16 bytes)."""
    ie_type = C.IE_GSN_ADDRESS

    def __init__(self, address: bytes = b"\x00\x00\x00\x00"):
        self.address = address

    def _encode_value(self) -> bytes:
        return self.address

    def _decode_value(self, value: bytes) -> None:
        self.address = value

    def __repr__(self) -> str:
        if len(self.address) == 4:
            return f"GSNAddressIE({'.'.join(str(b) for b in self.address)})"
        return f"GSNAddressIE({self.address.hex()})"


class MSISDNIE(IEv1):
    """MSISDN — BCD-encoded E.164 number."""
    ie_type = C.IE_MSISDN

    def __init__(self, digits: str = ""):
        self.digits = digits

    def _encode_value(self) -> bytes:
        # First byte is TON/NPI (0x91 = international E.164)
        return b"\x91" + bcd.encode(self.digits)

    def _decode_value(self, value: bytes) -> None:
        # Skip TON/NPI byte
        self.digits = bcd.decode(value[1:]) if len(value) > 1 else ""

    def __repr__(self) -> str:
        return f"MSISDNIE(digits={self.digits!r})"


class QoSProfileIE(IEv1):
    """Quality of Service Profile — opaque byte blob."""
    ie_type = C.IE_QOS_PROFILE

    def __init__(self, data: bytes = b""):
        self.data = data

    def _encode_value(self) -> bytes:
        return self.data

    def _decode_value(self, value: bytes) -> None:
        self.data = value

    def __repr__(self) -> str:
        return f"QoSProfileIE({self.data.hex()})"


class TrafficFlowTemplateIE(IEv1):
    ie_type = C.IE_TRAFFIC_FLOW_TEMPLATE

    def __init__(self, data: bytes = b""):
        self.data = data

    def _encode_value(self) -> bytes:
        return self.data

    def _decode_value(self, value: bytes) -> None:
        self.data = value


class UserLocationInfoIE(IEv1):
    """User Location Information.

    Encoding (TS 29.060 §7.7.51):
      Byte 0: Geographic Location Type
        0 = CGI, 1 = SAI, 2 = RAI
      Bytes 1-n: location data
    """
    ie_type = C.IE_USER_LOCATION_INFO

    GLT_CGI = 0
    GLT_SAI = 1
    GLT_RAI = 2

    def __init__(self, glt: int = GLT_CGI, location: bytes = b""):
        self.glt = glt
        self.location = location

    def _encode_value(self) -> bytes:
        return bytes([self.glt]) + self.location

    def _decode_value(self, value: bytes) -> None:
        self.glt = value[0] if value else 0
        self.location = value[1:]


class MSTimeZoneIE(IEv1):
    """MS Time Zone (TS 29.060 §7.7.52)."""
    ie_type = C.IE_MS_TIME_ZONE

    def __init__(self, tz_byte: int = 0, dst: int = 0):
        self.tz_byte = tz_byte
        self.dst = dst

    def _encode_value(self) -> bytes:
        return bytes([self.tz_byte, self.dst & 0x03])

    def _decode_value(self, value: bytes) -> None:
        self.tz_byte = value[0] if len(value) > 0 else 0
        self.dst = (value[1] & 0x03) if len(value) > 1 else 0


class IMEISVIe(IEv1):
    """IMEI(SV) — BCD encoded."""
    ie_type = C.IE_IMEI_SV

    def __init__(self, digits: str = ""):
        self.digits = digits

    def _encode_value(self) -> bytes:
        return bcd.encode(self.digits)

    def _decode_value(self, value: bytes) -> None:
        self.digits = bcd.decode(value)


class RATTypeIE(IEv1):
    ie_type = C.IE_RAT_TYPE

    def __init__(self, rat: int = C.RAT_UTRAN):
        self.rat = rat

    def _encode_value(self) -> bytes:
        return bytes([self.rat])

    def _decode_value(self, value: bytes) -> None:
        self.rat = value[0] if value else 0

    def __repr__(self) -> str:
        return f"RATTypeIE(rat={self.rat})"


class CommonFlagsIE(IEv1):
    ie_type = C.IE_COMMON_FLAGS

    def __init__(self, flags: int = 0):
        self.flags = flags

    def _encode_value(self) -> bytes:
        return bytes([self.flags])

    def _decode_value(self, value: bytes) -> None:
        self.flags = value[0] if value else 0


class APNRestrictionIE(IEv1):
    ie_type = C.IE_APN_RESTRICTION

    def __init__(self, restriction: int = 0):
        self.restriction = restriction

    def _encode_value(self) -> bytes:
        return bytes([self.restriction])

    def _decode_value(self, value: bytes) -> None:
        self.restriction = value[0] if value else 0


class PrivateExtensionIE(IEv1):
    ie_type = C.IE_PRIVATE_EXT

    def __init__(self, enterprise_id: int = 0, value: bytes = b""):
        self.enterprise_id = enterprise_id
        self.ext_value = value

    def _encode_value(self) -> bytes:
        return struct.pack("!H", self.enterprise_id) + self.ext_value

    def _decode_value(self, value: bytes) -> None:
        if len(value) >= 2:
            self.enterprise_id = struct.unpack_from("!H", value)[0]
            self.ext_value = value[2:]
        else:
            self.enterprise_id = 0
            self.ext_value = b""

    def __repr__(self) -> str:
        return f"PrivateExtensionIE(enterprise={self.enterprise_id}, val={self.ext_value.hex()})"
