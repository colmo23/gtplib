"""Tests for GTPv1 IE encode/decode."""

import pytest
from gtpc.v1.ie.base import decode_ies
from gtpc.v1.ie.tv import (
    CauseIE, IMSIE, RAIIE, RecoveryIE, SelectionModeIE,
    TEIDDataIIE, TEIDCPlaneIE, NSAPIIE, ChargingIDIE,
)
from gtpc.v1.ie.tlv import APNIE, GSNAddressIE, MSISDNIE, EndUserAddressIE


def round_trip(ie):
    encoded = ie.encode()
    klass = type(ie)
    decoded = klass.decode(encoded)
    return decoded


def test_cause_ie():
    ie = CauseIE(128)
    d = round_trip(ie)
    assert d.cause == 128


def test_imsi_ie():
    ie = IMSIE("272030100000000")
    d = round_trip(ie)
    assert d.digits == "272030100000000"


def test_rai_ie():
    ie = RAIIE("272", "03", 65534, 255)
    d = round_trip(ie)
    assert d.mcc == "272"
    assert d.mnc == "03"
    assert d.lac == 65534
    assert d.rac == 255


def test_recovery_ie():
    ie = RecoveryIE(93)
    d = round_trip(ie)
    assert d.restart_counter == 93


def test_selection_mode_ie():
    ie = SelectionModeIE(0)
    d = round_trip(ie)
    assert d.mode == 0


def test_teid_data_ie():
    ie = TEIDDataIIE(0x372F0000)
    d = round_trip(ie)
    assert d.teid == 0x372F0000


def test_nsapi_ie():
    ie = NSAPIIE(5)
    d = round_trip(ie)
    assert d.nsapi == 5


def test_charging_id_ie():
    ie = ChargingIDIE(0xDEADBEEF)
    d = round_trip(ie)
    assert d.charging_id == 0xDEADBEEF


def test_apn_ie():
    ie = APNIE("mms.mymeteor.ie")
    d = round_trip(ie)
    assert d.apn == "mms.mymeteor.ie"


def test_gsn_address_ipv4():
    import socket
    addr = socket.inet_pton(socket.AF_INET, "212.129.65.13")
    ie = GSNAddressIE(addr)
    d = round_trip(ie)
    assert d.address == addr


def test_msisdn_ie():
    ie = MSISDNIE("353800000000")
    d = round_trip(ie)
    assert d.digits == "353800000000"


def test_end_user_address_ipv4():
    import socket
    addr = socket.inet_pton(socket.AF_INET, "10.0.0.1")
    ie = EndUserAddressIE(
        pdp_type_org=EndUserAddressIE.PTO_IETF,
        pdp_type_num=EndUserAddressIE.PDN_IPv4,
        address=addr,
    )
    d = round_trip(ie)
    assert d.pdp_type_num == EndUserAddressIE.PDN_IPv4
    assert d.address == addr


def test_decode_ies_multiple():
    from gtpc.v1.ie.tv import IMSIE, NSAPIIE
    ies = [IMSIE("272030100000000"), NSAPIIE(5), RecoveryIE(10)]
    buf = b"".join(ie.encode() for ie in ies)
    decoded = decode_ies(buf)
    assert len(decoded) == 3
    assert decoded[0].ie_type == 2  # IMSI
    assert decoded[1].ie_type == 20  # NSAPI
    assert decoded[2].ie_type == 14  # Recovery
