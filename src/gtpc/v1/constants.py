"""GTPv1-C constants: message types and IE type codes.

Source: 3GPP TS 29.060, cross-referenced with Wireshark packet-gtp.c.
"""

# ---------------------------------------------------------------------------
# GTPv1-C Message Types
# ---------------------------------------------------------------------------

# Path management
MSG_ECHO_REQ                        = 1
MSG_ECHO_RES                        = 2
MSG_VERSION_NOT_SUPPORTED           = 3
MSG_NODE_ALIVE_REQ                  = 4
MSG_NODE_ALIVE_RES                  = 5
MSG_REDIRECT_REQ                    = 6
MSG_REDIRECT_RES                    = 7

# Tunnel management
MSG_CREATE_PDP_CTX_REQ              = 16
MSG_CREATE_PDP_CTX_RES              = 17
MSG_UPDATE_PDP_CTX_REQ              = 18
MSG_UPDATE_PDP_CTX_RES              = 19
MSG_DELETE_PDP_CTX_REQ              = 20
MSG_DELETE_PDP_CTX_RES              = 21
MSG_INIT_PDP_CTX_ACT_REQ           = 22   # MS-initiated
MSG_INIT_PDP_CTX_ACT_RES           = 23
MSG_DELETE_AA_PDP_CTX_REQ          = 24
MSG_DELETE_AA_PDP_CTX_RES          = 25
MSG_ERROR_INDICATION                = 26
MSG_PDU_NOTIFICATION_REQ           = 27
MSG_PDU_NOTIFICATION_RES           = 28
MSG_PDU_NOTIFICATION_REJECT_REQ    = 29
MSG_PDU_NOTIFICATION_REJECT_RES    = 30
MSG_SUPPORTED_EXT_HEADER_NOTIFY    = 31

# Location management (GTP')
MSG_SEND_ROUTING_INFO_GPRS_REQ     = 32
MSG_SEND_ROUTING_INFO_GPRS_RES     = 33
MSG_FAILURE_REPORT_REQ             = 34
MSG_FAILURE_REPORT_RES             = 35
MSG_NOTE_MS_GPRS_PRESENT_REQ       = 36
MSG_NOTE_MS_GPRS_PRESENT_RES       = 37

# Mobility / handover
MSG_IDENTIFICATION_REQ             = 48
MSG_IDENTIFICATION_RES             = 49
MSG_SGSN_CTX_REQ                   = 50
MSG_SGSN_CTX_RES                   = 51
MSG_SGSN_CTX_ACK                   = 52
MSG_FORWARD_RELOC_REQ              = 53
MSG_FORWARD_RELOC_RES              = 54
MSG_FORWARD_RELOC_COMPLETE         = 55
MSG_RELOC_CANCEL_REQ               = 56
MSG_RELOC_CANCEL_RES               = 57
MSG_FORWARD_SRNS_CTX               = 58
MSG_FORWARD_RELOC_COMPLETE_ACK     = 59
MSG_FORWARD_SRNS_CTX_ACK           = 60
MSG_UE_REGIST_QUERY_REQ            = 61
MSG_UE_REGIST_QUERY_RES            = 62

# RAN information relay
MSG_RAN_INFORMATION_RELAY          = 70

# MBMS (Multimedia Broadcast/Multicast Service) — types 96-121
MSG_MBMS_NOTIFICATION_REQ          = 96
MSG_MBMS_NOTIFICATION_RES          = 97
MSG_MBMS_NOTIFICATION_REJECT_REQ   = 98
MSG_MBMS_NOTIFICATION_REJECT_RES   = 99
MSG_CREATE_MBMS_CTX_REQ            = 100
MSG_CREATE_MBMS_CTX_RES            = 101
MSG_UPDATE_MBMS_CTX_REQ            = 102
MSG_UPDATE_MBMS_CTX_RES            = 103
MSG_DELETE_MBMS_CTX_REQ            = 104
MSG_DELETE_MBMS_CTX_RES            = 105
MSG_MBMS_REGIST_REQ                = 112
MSG_MBMS_REGIST_RES                = 113
MSG_MBMS_DEREGIST_REQ              = 114
MSG_MBMS_DEREGIST_RES              = 115
MSG_MBMS_SESSION_START_REQ         = 116
MSG_MBMS_SESSION_START_RES         = 117
MSG_MBMS_SESSION_STOP_REQ          = 118
MSG_MBMS_SESSION_STOP_RES          = 119
MSG_MBMS_SESSION_UPDATE_REQ        = 120
MSG_MBMS_SESSION_UPDATE_RES        = 121

# MS Info Change
MSG_MS_INFO_CHANGE_NOTIFY_REQ      = 128
MSG_MS_INFO_CHANGE_NOTIFY_RES      = 129

# CDR transfer
MSG_DATA_RECORD_TRANSFER_REQ       = 240
MSG_DATA_RECORD_TRANSFER_RES       = 241

# End marker / G-PDU
MSG_END_MARKER                      = 254
MSG_G_PDU                           = 255

# Human-readable message type names (mirrors Wireshark val_to_str)
MSG_TYPE_NAMES: dict[int, str] = {
    MSG_ECHO_REQ:                       "Echo Request",
    MSG_ECHO_RES:                       "Echo Response",
    MSG_VERSION_NOT_SUPPORTED:          "Version Not Supported",
    MSG_NODE_ALIVE_REQ:                 "Node Alive Request",
    MSG_NODE_ALIVE_RES:                 "Node Alive Response",
    MSG_REDIRECT_REQ:                   "Redirect Request",
    MSG_REDIRECT_RES:                   "Redirect Response",
    MSG_CREATE_PDP_CTX_REQ:            "Create PDP Context Request",
    MSG_CREATE_PDP_CTX_RES:            "Create PDP Context Response",
    MSG_UPDATE_PDP_CTX_REQ:            "Update PDP Context Request",
    MSG_UPDATE_PDP_CTX_RES:            "Update PDP Context Response",
    MSG_DELETE_PDP_CTX_REQ:            "Delete PDP Context Request",
    MSG_DELETE_PDP_CTX_RES:            "Delete PDP Context Response",
    MSG_INIT_PDP_CTX_ACT_REQ:          "Initiate PDP Context Activation Request",
    MSG_INIT_PDP_CTX_ACT_RES:          "Initiate PDP Context Activation Response",
    MSG_DELETE_AA_PDP_CTX_REQ:         "Delete AA PDP Context Request",
    MSG_DELETE_AA_PDP_CTX_RES:         "Delete AA PDP Context Response",
    MSG_ERROR_INDICATION:               "Error Indication",
    MSG_PDU_NOTIFICATION_REQ:          "PDU Notification Request",
    MSG_PDU_NOTIFICATION_RES:          "PDU Notification Response",
    MSG_PDU_NOTIFICATION_REJECT_REQ:   "PDU Notification Reject Request",
    MSG_PDU_NOTIFICATION_REJECT_RES:   "PDU Notification Reject Response",
    MSG_SUPPORTED_EXT_HEADER_NOTIFY:   "Supported Extension Headers Notification",
    MSG_SEND_ROUTING_INFO_GPRS_REQ:    "Send Routeing Information for GPRS Request",
    MSG_SEND_ROUTING_INFO_GPRS_RES:    "Send Routeing Information for GPRS Response",
    MSG_FAILURE_REPORT_REQ:            "Failure Report Request",
    MSG_FAILURE_REPORT_RES:            "Failure Report Response",
    MSG_NOTE_MS_GPRS_PRESENT_REQ:      "Note MS GPRS Present Request",
    MSG_NOTE_MS_GPRS_PRESENT_RES:      "Note MS GPRS Present Response",
    MSG_IDENTIFICATION_REQ:            "Identification Request",
    MSG_IDENTIFICATION_RES:            "Identification Response",
    MSG_SGSN_CTX_REQ:                  "SGSN Context Request",
    MSG_SGSN_CTX_RES:                  "SGSN Context Response",
    MSG_SGSN_CTX_ACK:                  "SGSN Context Acknowledge",
    MSG_FORWARD_RELOC_REQ:             "Forward Relocation Request",
    MSG_FORWARD_RELOC_RES:             "Forward Relocation Response",
    MSG_FORWARD_RELOC_COMPLETE:        "Forward Relocation Complete",
    MSG_RELOC_CANCEL_REQ:              "Relocation Cancel Request",
    MSG_RELOC_CANCEL_RES:              "Relocation Cancel Response",
    MSG_FORWARD_SRNS_CTX:              "Forward SRNS Context",
    MSG_FORWARD_RELOC_COMPLETE_ACK:    "Forward Relocation Complete Acknowledge",
    MSG_FORWARD_SRNS_CTX_ACK:          "Forward SRNS Context Acknowledge",
    MSG_UE_REGIST_QUERY_REQ:           "UE Registration Query Request",
    MSG_UE_REGIST_QUERY_RES:           "UE Registration Query Response",
    MSG_RAN_INFORMATION_RELAY:         "RAN Information Relay",
    MSG_MBMS_NOTIFICATION_REQ:         "MBMS Notification Request",
    MSG_MBMS_NOTIFICATION_RES:         "MBMS Notification Response",
    MSG_MBMS_NOTIFICATION_REJECT_REQ:  "MBMS Notification Reject Request",
    MSG_MBMS_NOTIFICATION_REJECT_RES:  "MBMS Notification Reject Response",
    MSG_CREATE_MBMS_CTX_REQ:           "Create MBMS Context Request",
    MSG_CREATE_MBMS_CTX_RES:           "Create MBMS Context Response",
    MSG_UPDATE_MBMS_CTX_REQ:           "Update MBMS Context Request",
    MSG_UPDATE_MBMS_CTX_RES:           "Update MBMS Context Response",
    MSG_DELETE_MBMS_CTX_REQ:           "Delete MBMS Context Request",
    MSG_DELETE_MBMS_CTX_RES:           "Delete MBMS Context Response",
    MSG_MBMS_REGIST_REQ:               "MBMS Registration Request",
    MSG_MBMS_REGIST_RES:               "MBMS Registration Response",
    MSG_MBMS_DEREGIST_REQ:             "MBMS De-Registration Request",
    MSG_MBMS_DEREGIST_RES:             "MBMS De-Registration Response",
    MSG_MBMS_SESSION_START_REQ:        "MBMS Session Start Request",
    MSG_MBMS_SESSION_START_RES:        "MBMS Session Start Response",
    MSG_MBMS_SESSION_STOP_REQ:         "MBMS Session Stop Request",
    MSG_MBMS_SESSION_STOP_RES:         "MBMS Session Stop Response",
    MSG_MBMS_SESSION_UPDATE_REQ:       "MBMS Session Update Request",
    MSG_MBMS_SESSION_UPDATE_RES:       "MBMS Session Update Response",
    MSG_MS_INFO_CHANGE_NOTIFY_REQ:     "MS Info Change Notification Request",
    MSG_MS_INFO_CHANGE_NOTIFY_RES:     "MS Info Change Notification Response",
    MSG_DATA_RECORD_TRANSFER_REQ:      "Data Record Transfer Request",
    MSG_DATA_RECORD_TRANSFER_RES:      "Data Record Transfer Response",
    MSG_END_MARKER:                     "End Marker",
    MSG_G_PDU:                          "G-PDU",
}

# ---------------------------------------------------------------------------
# GTPv1 Next Extension Header types
# ---------------------------------------------------------------------------
EXT_HDR_NO_MORE                     = 0x00
EXT_HDR_MBMS_SUPPORT_IND            = 0x01
EXT_HDR_MS_INFO_CHANGE_SUPPORT      = 0x02
EXT_HDR_PDCP_PDU_NUMBER             = 0xC0
EXT_HDR_SUSPEND_REQUEST             = 0xC1
EXT_HDR_SUSPEND_RESPONSE            = 0xC2

# ---------------------------------------------------------------------------
# GTPv1 TV IE types (bit 7 = 0, fixed length per TV_LEN)
# ---------------------------------------------------------------------------
IE_RESERVED                 = 0
IE_CAUSE                    = 1
IE_IMSI                     = 2
IE_RAI                      = 3
IE_TLLI                     = 4
IE_P_TMSI                   = 5
IE_REORDER_REQUIRED         = 8
IE_AUTH_TRIPLET             = 9
IE_MAP_CAUSE                = 11
IE_P_TMSI_SIG               = 12
IE_MS_VALIDATED             = 13
IE_RECOVERY                 = 14
IE_SELECTION_MODE           = 15
IE_TEID_DATA_1              = 16
IE_TEID_C_PLANE             = 17
IE_TEID_DATA_2              = 18
IE_TEARDOWN_IND             = 19
IE_NSAPI                    = 20
IE_RANAP_CAUSE              = 21
IE_RAB_CTX                  = 22
IE_RADIO_PRIORITY_SMS       = 23
IE_RADIO_PRIORITY           = 24
IE_PACKET_FLOW_ID           = 25
IE_CHARGING_CHARS           = 26
IE_TRACE_REFERENCE          = 27
IE_TRACE_TYPE               = 28
IE_MS_NOT_REACHABLE_REASON  = 29
IE_PACKET_TRANSFER_CMD      = 126   # GTP' Packet Transfer Command (TV, 1 byte)
IE_CHARGING_ID              = 127   # last TV IE

# Fixed lengths for TV IEs (bytes after the type byte)
TV_LEN: dict[int, int] = {
    IE_RESERVED:                0,
    IE_CAUSE:                   1,
    IE_IMSI:                    8,
    IE_RAI:                     6,
    IE_TLLI:                    4,
    IE_P_TMSI:                  4,
    IE_REORDER_REQUIRED:        1,
    IE_AUTH_TRIPLET:            28,
    IE_MAP_CAUSE:               1,
    IE_P_TMSI_SIG:              3,
    IE_MS_VALIDATED:            1,
    IE_RECOVERY:                1,
    IE_SELECTION_MODE:          1,
    IE_TEID_DATA_1:             4,
    IE_TEID_C_PLANE:            4,
    IE_TEID_DATA_2:             5,
    IE_TEARDOWN_IND:            1,
    IE_NSAPI:                   1,
    IE_RANAP_CAUSE:             1,
    IE_RAB_CTX:                 9,
    IE_RADIO_PRIORITY_SMS:      1,
    IE_RADIO_PRIORITY:          1,
    IE_PACKET_FLOW_ID:          2,
    IE_CHARGING_CHARS:          2,
    IE_TRACE_REFERENCE:         2,
    IE_TRACE_TYPE:              2,
    IE_MS_NOT_REACHABLE_REASON: 1,
    IE_PACKET_TRANSFER_CMD:     1,
    IE_CHARGING_ID:             4,
}

# ---------------------------------------------------------------------------
# GTPv1 TLV IE types (bit 7 = 1, preceded by 2-byte length)
# ---------------------------------------------------------------------------
IE_END_USER_ADDRESS         = 128
IE_MM_CTX                   = 129
IE_PDP_CTX                  = 130
IE_APN                      = 131
IE_PCO                      = 132
IE_GSN_ADDRESS              = 133
IE_MSISDN                   = 134
IE_QOS_PROFILE              = 135
IE_AUTH_QUINTUPLET          = 136
IE_TRAFFIC_FLOW_TEMPLATE    = 137
IE_TARGET_ID                = 138
IE_UTRAN_TRANSPARENT_CONT   = 139
IE_RAB_SETUP_INFO           = 140
IE_EXT_HEADER_TYPE_LIST     = 141
IE_TRIGGER_ID               = 143
IE_OMC_ID                   = 144
IE_RAN_TRANSPARENT_CONT     = 145
IE_PDP_CTX_PRIORITIZATION   = 146
IE_ADDITIONAL_RA_INFO       = 147
IE_SGSN_NUMBER              = 148
IE_COMMON_FLAGS             = 149
IE_APN_RESTRICTION          = 150
IE_RAT_TYPE                 = 151
IE_USER_LOCATION_INFO       = 152
IE_MS_TIME_ZONE             = 153
IE_IMEI_SV                  = 154
IE_CAMEL_CHARGING_INFO_CONT = 155
IE_MBMS_UE_CTX              = 156
IE_TMGI                     = 157
IE_RIM_ROUTING_ADDRESS      = 158
IE_MBMS_PROTOCOL_CONFIG     = 159
IE_MBMS_SERVICE_AREA        = 160
IE_SRC_RNC_PDCP_CTX_INFO    = 161
IE_ADDITIONAL_TRACE_INFO    = 162
IE_HOP_COUNTER              = 163
IE_SEL_PLMN_ID              = 164
IE_MBMS_SESSION_ID          = 165
IE_MBMS_2G_3G_IND           = 166
IE_ENHANCED_NSAPI           = 167
IE_MBMS_SESSION_DURATION    = 168
IE_MBMS_TIME_TO_DATA_XFER   = 169
IE_LHN_ID                   = 170
IE_MBMS_SESSION_REPETITION_NUM = 171
IE_MBMS_TIME_TO_DATA_XFER2  = 172
IE_BSS_CONTAINER            = 173
IE_CELL_ID                  = 174
IE_PDU_NUMBERS              = 175
IE_BSSGP_CAUSE              = 176
IE_REQ_MBMS_BEARER_CAP      = 177
IE_RIM_ROUTING_ADDR_DISC    = 178
IE_LIST_OF_SETUPS           = 179
IE_PS_HANDOVER_XID_PARAMS   = 180
IE_MS_INFO_CHANGE_REP_ACTION = 181
IE_DIRECT_TUNNEL_FLAGS      = 182
IE_CORRELATION_ID           = 183
IE_BEARER_CONTROL_MODE      = 184
IE_MBMS_FLOW_ID             = 185
IE_MBMS_IP_MCAST_DIST       = 186
IE_MBMS_DIST_ACK            = 187
IE_RELIABLE_INTER_RAT_HO_INFO = 188
IE_RFSP_INDEX               = 189
IE_FQDN                     = 190
IE_EVOLVED_ALLOCATION_RETENTION_1 = 191
IE_EVOLVED_ALLOCATION_RETENTION_2 = 192
IE_EXTENDED_COMMON_FLAGS    = 193
IE_UCI                      = 194
IE_CSG_INFO_REP_ACTION      = 195
IE_CSG_ID                   = 196
IE_CMI                      = 197
IE_APCO                     = 198
IE_UE_NETWORK_CAPABILITY    = 199
IE_UE_AMBR                  = 200
IE_APN_AMBR_WITH_NSAPI      = 201
IE_GGSN_BACK_OFF_TIME       = 202
IE_SIG_PRIO_INDICATION      = 203
IE_SIG_PRIO_INDICATION_NSAPI = 204
IE_HIGHER_BITRATES_THAN_16M_FLAG = 205
IE_MAX_MBR_APN_AMBR         = 206
IE_ADDITIONAL_MM_CTX_SRVCC  = 207
IE_ADDITIONAL_FLAGS_SRVCC   = 208
IE_STN_SR                   = 209
IE_SRC_TGT_TRANS_CON        = 210
IE_TGT_SRC_TRANS_CON        = 211
IE_MM_CON_EUTRAN_SRVCC      = 212
IE_MM_CON_UTRAN_SRVCC       = 213
IE_SRVCC_CAUSE              = 214
IE_TGT_RNC_ID               = 215
IE_TGT_GLOBAL_CELL_ID       = 216
IE_TEID_C_SRVCC             = 217
IE_SV_FLAGS                 = 218
IE_SAI_SRVCC                = 219
IE_LHN_ID_W_NSAPI           = 220
IE_CN_OPERATOR_SEL_ENT      = 221
IE_UE_USAGE_TYPE            = 222
IE_EXTENDED_COMMON_FLAGS_2  = 223
IE_NODE_IDENTIFIER          = 224
IE_CIOT_OPT_SUPPORT_IND     = 225
IE_SCEF_PDN_CONNECTION      = 226
IE_IOV_UPDATES_COUNTER      = 227
IE_MAPPED_UE_USAGE_TYPE     = 228
IE_UP_FUNCTION_SEL_IND_FLAGS = 229
IE_PRIVATE_EXT              = 255

# Human-readable IE type names (mirrors Wireshark)
IE_TYPE_NAMES: dict[int, str] = {
    IE_CAUSE:                   "Cause",
    IE_IMSI:                    "IMSI",
    IE_RAI:                     "Routing Area Identity",
    IE_TLLI:                    "TLLI",
    IE_P_TMSI:                  "P-TMSI",
    IE_REORDER_REQUIRED:        "Reorder Required",
    IE_AUTH_TRIPLET:            "Authentication Triplet",
    IE_MAP_CAUSE:               "MAP Cause",
    IE_P_TMSI_SIG:              "P-TMSI Signature",
    IE_MS_VALIDATED:            "MS Validated",
    IE_RECOVERY:                "Recovery",
    IE_SELECTION_MODE:          "Selection Mode",
    IE_TEID_DATA_1:             "TEID Data I",
    IE_TEID_C_PLANE:            "TEID Control Plane",
    IE_TEID_DATA_2:             "TEID Data II",
    IE_TEARDOWN_IND:            "Teardown Ind",
    IE_NSAPI:                   "NSAPI",
    IE_RANAP_CAUSE:             "RANAP Cause",
    IE_RAB_CTX:                 "RAB Context",
    IE_RADIO_PRIORITY_SMS:      "Radio Priority SMS",
    IE_RADIO_PRIORITY:          "Radio Priority",
    IE_PACKET_FLOW_ID:          "Packet Flow ID",
    IE_CHARGING_CHARS:          "Charging Characteristics",
    IE_TRACE_REFERENCE:         "Trace Reference",
    IE_TRACE_TYPE:              "Trace Type",
    IE_MS_NOT_REACHABLE_REASON: "MS Not Reachable Reason",
    IE_CHARGING_ID:             "Charging ID",
    IE_END_USER_ADDRESS:        "End User Address",
    IE_MM_CTX:                  "MM Context",
    IE_PDP_CTX:                 "PDP Context",
    IE_APN:                     "Access Point Name",
    IE_PCO:                     "Protocol Configuration Options",
    IE_GSN_ADDRESS:             "GSN Address",
    IE_MSISDN:                  "MSISDN",
    IE_QOS_PROFILE:             "QoS Profile",
    IE_AUTH_QUINTUPLET:         "Authentication Quintuplet",
    IE_TRAFFIC_FLOW_TEMPLATE:   "Traffic Flow Template",
    IE_TARGET_ID:               "Target Identification",
    IE_RAT_TYPE:                "RAT Type",
    IE_USER_LOCATION_INFO:      "User Location Information",
    IE_MS_TIME_ZONE:            "MS Time Zone",
    IE_IMEI_SV:                 "IMEI(SV)",
    IE_PRIVATE_EXT:             "Private Extension",
}

# Cause values (TS 29.060 Table 37)
CAUSE_REQUEST_IMSI                  = 0
CAUSE_REQUEST_IMEI                  = 1
CAUSE_REQUEST_IMSI_IMEI             = 2
CAUSE_NO_IDENTITY_NEEDED            = 3
CAUSE_MS_REFUSES                    = 4
CAUSE_MS_NOT_GPRS_RESPONDING        = 5
CAUSE_REQUEST_ACCEPTED              = 128
CAUSE_NEW_PDP_TYPE_DUE_TO_NETWORK   = 129
CAUSE_NEW_PDP_TYPE_DUE_TO_MS       = 130
CAUSE_NO_RESOURCES                  = 192
CAUSE_SERVICE_NOT_SUPPORTED         = 193
CAUSE_MANDATORY_IE_INCORRECT        = 194
CAUSE_MANDATORY_IE_MISSING          = 195
CAUSE_OPTIONAL_IE_INCORRECT         = 196
CAUSE_SYSTEM_FAILURE                = 197
CAUSE_ROAMING_RESTRICTION           = 198
CAUSE_P_TMSI_SIG_MISMATCH           = 199
CAUSE_GPRS_CONNECTION_SUSPENDED     = 200
CAUSE_AUTH_FAILURE                  = 201
CAUSE_USER_AUTH_FAILURE             = 202
CAUSE_CONTEXT_NOT_FOUND             = 203
CAUSE_ALL_PDP_DYNAMIC_ADDRESSES_OCCUPIED = 204
CAUSE_NO_MEMORY                     = 205
CAUSE_REALLOCATION_FAILURE          = 206
CAUSE_UNKNOWN_MANDATORY_EXT_HEADER  = 207
CAUSE_SEMANTIC_ERROR_TFT            = 208
CAUSE_SYNTACTIC_ERROR_TFT           = 209
CAUSE_SEMANTIC_ERROR_IN_PACKET_FILTER = 210
CAUSE_SYNTACTIC_ERROR_IN_PACKET_FILTER = 211
CAUSE_MISSING_OR_UNKNOWN_APN        = 212
CAUSE_UNKNOWN_PDP_ADDRESS_OR_TYPE   = 213
CAUSE_PDP_CONTEXT_WITHOUT_TFT_ALREADY_ACTIVATED = 214
CAUSE_APN_ACCESS_DENIED             = 215
CAUSE_APN_RESTRICTION_MISMATCH      = 216
CAUSE_MS_MBMS_CAPABILITY_INSUFFICIENT = 217
CAUSE_INVALID_CORRELATION_ID        = 218
CAUSE_MBMS_BEARER_CONTEXT_SUPERSEDED = 219
CAUSE_SELECTIVE_PAGING_INDICATION   = 220
CAUSE_INVALID_MESSAGE_FORMAT        = 221
CAUSE_M_TMSI_NOT_KNOWN              = 222
CAUSE_IMSI_IMEI_NOT_KNOWN           = 223

# RAT Type values (TS 29.060 §7.7.50)
RAT_UTRAN                           = 1
RAT_GERAN                           = 2
RAT_WLAN                            = 3
RAT_GAN                             = 4
RAT_HSPA_EVOLUTION                  = 5

# Selection Mode values
SEL_MODE_MS_OR_NET_APN_SUBSCR_VERIFIED = 0
SEL_MODE_MS_APN_SUBSCR_NOT_VERIFIED    = 1
SEL_MODE_NET_APN_SUBSCR_NOT_VERIFIED   = 2
