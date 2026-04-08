"""IE type → class registry for GTPv1 (mirrors Wireshark dissector tables)."""

from gtpc.v1.ie.base import IEv1
from gtpc.v1.ie.tv import (
    CauseIE, IMSIE, RAIIE, TLLIIE, PTMSIIE, ReorderRequiredIE,
    RecoveryIE, SelectionModeIE, TEIDDataIIE, TEIDCPlaneIE, TEIDDataIIIE,
    TeardownIndIE, NSAPIIE, ChargingCharsIE, TraceReferenceIE,
    TraceTypeIE, ChargingIDIE,
)
from gtpc.v1.ie.tlv import (
    EndUserAddressIE, APNIE, PCOIE, GSNAddressIE, MSISDNIE,
    QoSProfileIE, TrafficFlowTemplateIE, UserLocationInfoIE,
    MSTimeZoneIE, IMEISVIe, RATTypeIE, CommonFlagsIE,
    APNRestrictionIE, PrivateExtensionIE,
)
from gtpc.v1 import constants as C

IE_REGISTRY: dict[int, type[IEv1]] = {
    C.IE_CAUSE:                 CauseIE,
    C.IE_IMSI:                  IMSIE,
    C.IE_RAI:                   RAIIE,
    C.IE_TLLI:                  TLLIIE,
    C.IE_P_TMSI:                PTMSIIE,
    C.IE_REORDER_REQUIRED:      ReorderRequiredIE,
    C.IE_RECOVERY:              RecoveryIE,
    C.IE_SELECTION_MODE:        SelectionModeIE,
    C.IE_TEID_DATA_1:           TEIDDataIIE,
    C.IE_TEID_C_PLANE:          TEIDCPlaneIE,
    C.IE_TEID_DATA_2:           TEIDDataIIIE,
    C.IE_TEARDOWN_IND:          TeardownIndIE,
    C.IE_NSAPI:                 NSAPIIE,
    C.IE_CHARGING_CHARS:        ChargingCharsIE,
    C.IE_TRACE_REFERENCE:       TraceReferenceIE,
    C.IE_TRACE_TYPE:            TraceTypeIE,
    C.IE_CHARGING_ID:           ChargingIDIE,
    C.IE_END_USER_ADDRESS:      EndUserAddressIE,
    C.IE_APN:                   APNIE,
    C.IE_PCO:                   PCOIE,
    C.IE_GSN_ADDRESS:           GSNAddressIE,
    C.IE_MSISDN:                MSISDNIE,
    C.IE_QOS_PROFILE:           QoSProfileIE,
    C.IE_TRAFFIC_FLOW_TEMPLATE: TrafficFlowTemplateIE,
    C.IE_USER_LOCATION_INFO:    UserLocationInfoIE,
    C.IE_MS_TIME_ZONE:          MSTimeZoneIE,
    C.IE_IMEI_SV:               IMEISVIe,
    C.IE_RAT_TYPE:              RATTypeIE,
    C.IE_COMMON_FLAGS:          CommonFlagsIE,
    C.IE_APN_RESTRICTION:       APNRestrictionIE,
    C.IE_PRIVATE_EXT:           PrivateExtensionIE,
}
