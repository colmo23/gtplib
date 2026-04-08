"""Tests for GTPv2 IE encode/decode."""

import pytest
import socket
from gtpc.v2.ie.base import decode_ies
from gtpc.v2.ie.typed import (
    IMSIIE, CauseIE, RecoveryIE, APNIE, AMBRIE, EBIIE,
    IPAddressIE, MEIIE, MSISDNIE, PAAIE, BearerQoSIE,
    RATTypeIE, ServingNetworkIE, ULIIE, FTEIDIE, BearerContextIE,
    ChargingIDIE, PDNTypeIE, PTIIE, UETimeZoneIE, PrivateExtIE, ARPIE,
)
from gtpc.v2 import constants as C


def rt(ie):
    """Round-trip: encode then decode with the same class."""
    klass = type(ie)
    return klass.decode(ie.encode())


def test_imsi():
    d = rt(IMSIIE("272030100000000"))
    assert d.digits == "272030100000000"


def test_cause():
    d = rt(CauseIE(C.CAUSE_REQUEST_ACCEPTED, pce=True))
    assert d.cause == C.CAUSE_REQUEST_ACCEPTED
    assert d.pce is True


def test_recovery():
    d = rt(RecoveryIE(77))
    assert d.restart_counter == 77


def test_apn():
    d = rt(APNIE("internet.operator.com"))
    assert d.apn == "internet.operator.com"


def test_ambr():
    d = rt(AMBRIE(100000, 200000))
    assert d.uplink_kbps == 100000
    assert d.downlink_kbps == 200000


def test_ebi():
    d = rt(EBIIE(5))
    assert d.ebi == 5


def test_ip_address_v4():
    d = rt(IPAddressIE("10.1.2.3"))
    assert d.address == "10.1.2.3"


def test_ip_address_v6():
    d = rt(IPAddressIE("2001:db8::1"))
    assert d.address == "2001:db8::1"


def test_msisdn():
    d = rt(MSISDNIE("353800000000"))
    assert d.digits == "353800000000"


def test_paa_ipv4():
    d = rt(PAAIE(C.PDN_TYPE_IPv4, "192.168.1.1"))
    assert d.pdn_type == C.PDN_TYPE_IPv4
    assert d.address == "192.168.1.1"


def test_bearer_qos():
    ie = BearerQoSIE(qci=9, pl=9, mbr_ul=128000, mbr_dl=128000)
    d = rt(ie)
    assert d.qci == 9
    assert d.pl == 9
    assert d.mbr_ul == 128000


def test_rat_type():
    d = rt(RATTypeIE(C.RAT_EUTRAN))
    assert d.rat == C.RAT_EUTRAN


def test_serving_network():
    d = rt(ServingNetworkIE("310", "410"))
    assert d.mcc == "310"
    assert d.mnc == "410"


def test_uli_tai():
    ie = ULIIE.with_tai("310", "410", 0x1234)
    d = rt(ie)
    assert d.flags & ULIIE.TAI_PRESENT
    assert d.tai is not None and len(d.tai) == 5


def test_uli_ecgi():
    ie = ULIIE.with_ecgi("310", "410", 0xABCDE)
    d = rt(ie)
    assert d.flags & ULIIE.ECGI_PRESENT


def test_fteid_ipv4():
    ie = FTEIDIE(C.FTEID_S11_MME, teid=0xCAFEBABE, ipv4="1.2.3.4")
    d = rt(ie)
    assert d.teid == 0xCAFEBABE
    assert d.ipv4 == "1.2.3.4"
    assert d.interface_type == C.FTEID_S11_MME


def test_bearer_context_grouped():
    ctx = BearerContextIE()
    ctx.add_ie(EBIIE(5))
    ctx.add_ie(FTEIDIE(C.FTEID_S1U_SGW, teid=0x1111, ipv4="10.0.0.1"))
    ctx.add_ie(BearerQoSIE(qci=9, pl=9))
    d = BearerContextIE.decode(ctx.encode())
    assert len(d.grouped_ies) == 3
    ebi = d.get_ie(C.IE_EBI)
    assert ebi.ebi == 5


def test_pdn_type():
    d = rt(PDNTypeIE(C.PDN_TYPE_IPv4v6))
    assert d.pdn_type == C.PDN_TYPE_IPv4v6


def test_ue_timezone():
    d = rt(UETimeZoneIE(tz_byte=0x40, dst=1))
    assert d.tz_byte == 0x40
    assert d.dst == 1


def test_arp():
    d = rt(ARPIE(pl=9, pci=True, pvi=False))
    assert d.pl == 9
    assert d.pci is True
    assert d.pvi is False


def test_private_ext():
    d = rt(PrivateExtIE(enterprise_id=9999, value=b"\xDE\xAD"))
    assert d.enterprise_id == 9999
    assert d.ext_value == b"\xDE\xAD"


def test_decode_ies_multiple():
    ies = [IMSIIE("123456789"), EBIIE(5), RecoveryIE(1)]
    buf = b"".join(ie.encode() for ie in ies)
    decoded = decode_ies(buf)
    assert len(decoded) == 3
    assert decoded[0].ie_type == C.IE_IMSI
    assert decoded[2].ie_type == C.IE_RECOVERY


def test_instance_field():
    ie1 = FTEIDIE(0, teid=0x1111, ipv4="1.1.1.1", instance=0)
    ie2 = FTEIDIE(1, teid=0x2222, ipv4="2.2.2.2", instance=1)
    buf = ie1.encode() + ie2.encode()
    decoded = decode_ies(buf)
    assert decoded[0].instance == 0
    assert decoded[1].instance == 1
