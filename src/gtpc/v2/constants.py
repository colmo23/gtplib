"""GTPv2-C constants: message types and IE type codes.

Source: 3GPP TS 29.274, cross-referenced with Wireshark packet-gtpv2.c.
"""

# ---------------------------------------------------------------------------
# GTPv2-C Message Types
# ---------------------------------------------------------------------------

# Path management
MSG_ECHO_REQ                                    = 1
MSG_ECHO_RES                                    = 2
MSG_VERSION_NOT_SUPPORTED                       = 3

# SRVCC (Single Radio Voice Call Continuity) — types 25-30
MSG_UE_ACTIVITY_ACK                             = 25
MSG_SRVCC_PS_TO_CS_REQ                         = 25
MSG_SRVCC_PS_TO_CS_RES                         = 26
MSG_SRVCC_PS_TO_CS_COMPLETE_NOTIFY             = 27
MSG_SRVCC_PS_TO_CS_COMPLETE_ACK                = 28
MSG_SRVCC_PS_TO_CS_CANCEL_NOTIFY               = 29
MSG_SRVCC_PS_TO_CS_CANCEL_ACK                  = 30

# Session management
MSG_CREATE_SESSION_REQ                          = 32
MSG_CREATE_SESSION_RES                          = 33
MSG_MODIFY_BEARER_REQ                           = 34
MSG_MODIFY_BEARER_RES                           = 35
MSG_DELETE_SESSION_REQ                          = 36
MSG_DELETE_SESSION_RES                          = 37
MSG_CHANGE_NOTIFICATION_REQ                     = 38
MSG_CHANGE_NOTIFICATION_RES                     = 39
MSG_REMOTE_UE_REPORT_NOTIFY                    = 40
MSG_REMOTE_UE_REPORT_ACK                       = 41

# Bearer resource commands
MSG_MODIFY_BEARER_CMD                           = 64
MSG_MODIFY_BEARER_FAIL                          = 65
MSG_DELETE_BEARER_CMD                           = 66
MSG_DELETE_BEARER_FAIL                          = 67
MSG_BEARER_RESOURCE_CMD                         = 68
MSG_BEARER_RESOURCE_FAIL                        = 69
MSG_DL_DATA_NOTIF_FAIL                          = 70
MSG_TRACE_SESSION_ACT                           = 71
MSG_TRACE_SESSION_DEACT                         = 72
MSG_STOP_PAGING_INDICATION                      = 73

# Bearer management
MSG_CREATE_BEARER_REQ                           = 95
MSG_CREATE_BEARER_RES                           = 96
MSG_UPDATE_BEARER_REQ                           = 97
MSG_UPDATE_BEARER_RES                           = 98
MSG_DELETE_BEARER_REQ                           = 99
MSG_DELETE_BEARER_RES                           = 100
MSG_DELETE_PDN_CONN_SET_REQ                     = 101
MSG_DELETE_PDN_CONN_SET_RES                     = 102
MSG_PGW_DL_TRIGGER_NOTIFY                      = 103
MSG_PGW_DL_TRIGGER_ACK                         = 104

# Mobility / handover
MSG_IDENTIFICATION_REQ                          = 128
MSG_IDENTIFICATION_RES                          = 129
MSG_CONTEXT_REQ                                 = 130
MSG_CONTEXT_RES                                 = 131
MSG_CONTEXT_ACK                                 = 132
MSG_FORWARD_RELOC_REQ                           = 133
MSG_FORWARD_RELOC_RES                           = 134
MSG_FORWARD_RELOC_COMPLETE_NOTIFY              = 135
MSG_FORWARD_RELOC_COMPLETE_ACK                 = 136
MSG_FORWARD_ACCESS_CONTEXT_NOTIFY              = 137
MSG_FORWARD_ACCESS_CONTEXT_ACK                 = 138
MSG_RELOC_CANCEL_REQ                            = 139
MSG_RELOC_CANCEL_RES                            = 140
MSG_CONFIG_TRANSFER_TUNNEL                      = 141

# Notifications
MSG_DETACH_NOTIFY                               = 149
MSG_DETACH_ACK                                  = 150
MSG_CS_PAGING_INDICATION                        = 151
MSG_RAN_INFO_RELAY                              = 152
MSG_ALERT_MME_NOTIFY                            = 153
MSG_ALERT_MME_ACK                               = 154
MSG_UE_ACTIVITY_NOTIFY                          = 155
MSG_UE_ACTIVITY_ACK                             = 156
MSG_ISR_STATUS_INDICATION                       = 157
MSG_UE_REGIST_QUERY_REQ                         = 158
MSG_UE_REGIST_QUERY_RES                         = 159

# Forwarding tunnels
MSG_CREATE_FORWARDING_TUNNEL_REQ               = 160
MSG_CREATE_FORWARDING_TUNNEL_RES               = 161
MSG_SUSPEND_NOTIFY                              = 162
MSG_SUSPEND_ACK                                 = 163
MSG_RESUME_NOTIFY                               = 164
MSG_RESUME_ACK                                  = 165
MSG_CREATE_INDIRECT_DATA_FWD_TUNNEL_REQ        = 166
MSG_CREATE_INDIRECT_DATA_FWD_TUNNEL_RES        = 167
MSG_DELETE_INDIRECT_DATA_FWD_TUNNEL_REQ        = 168
MSG_DELETE_INDIRECT_DATA_FWD_TUNNEL_RES        = 169
MSG_RELEASE_ACCESS_BEARERS_REQ                 = 170
MSG_RELEASE_ACCESS_BEARERS_RES                 = 171

# Downlink data / PGW restart
MSG_DL_DATA_NOTIFY                              = 176
MSG_DL_DATA_NOTIFY_ACK                          = 177
MSG_PGW_RESTART_NOTIFY                          = 179
MSG_PGW_RESTART_ACK                             = 180

# PDN connection set
MSG_UPDATE_PDN_CONN_SET_REQ                     = 200
MSG_UPDATE_PDN_CONN_SET_RES                     = 201

# Modify access bearers
MSG_MODIFY_ACCESS_BEARERS_REQ                   = 211
MSG_MODIFY_ACCESS_BEARERS_RES                   = 212

# MBMS
MSG_MBMS_SESSION_START_REQ                      = 231
MSG_MBMS_SESSION_START_RES                      = 232
MSG_MBMS_SESSION_UPDATE_REQ                     = 233
MSG_MBMS_SESSION_UPDATE_RES                     = 234
MSG_MBMS_SESSION_STOP_REQ                       = 235
MSG_MBMS_SESSION_STOP_RES                       = 236

MSG_TYPE_NAMES: dict[int, str] = {
    MSG_ECHO_REQ:                           "Echo Request",
    MSG_ECHO_RES:                           "Echo Response",
    MSG_VERSION_NOT_SUPPORTED:              "Version Not Supported",
    MSG_SRVCC_PS_TO_CS_REQ:                "SRVCC PS to CS Request",
    MSG_SRVCC_PS_TO_CS_RES:                "SRVCC PS to CS Response",
    MSG_SRVCC_PS_TO_CS_COMPLETE_NOTIFY:    "SRVCC PS to CS Complete Notification",
    MSG_SRVCC_PS_TO_CS_COMPLETE_ACK:       "SRVCC PS to CS Complete Acknowledge",
    MSG_SRVCC_PS_TO_CS_CANCEL_NOTIFY:      "SRVCC PS to CS Cancel Notification",
    MSG_SRVCC_PS_TO_CS_CANCEL_ACK:         "SRVCC PS to CS Cancel Acknowledge",
    MSG_CREATE_SESSION_REQ:                 "Create Session Request",
    MSG_CREATE_SESSION_RES:                 "Create Session Response",
    MSG_MODIFY_BEARER_REQ:                  "Modify Bearer Request",
    MSG_MODIFY_BEARER_RES:                  "Modify Bearer Response",
    MSG_DELETE_SESSION_REQ:                 "Delete Session Request",
    MSG_DELETE_SESSION_RES:                 "Delete Session Response",
    MSG_CHANGE_NOTIFICATION_REQ:            "Change Notification Request",
    MSG_CHANGE_NOTIFICATION_RES:            "Change Notification Response",
    MSG_REMOTE_UE_REPORT_NOTIFY:           "Remote UE Report Notification",
    MSG_REMOTE_UE_REPORT_ACK:              "Remote UE Report Acknowledge",
    MSG_MODIFY_BEARER_CMD:                  "Modify Bearer Command",
    MSG_MODIFY_BEARER_FAIL:                 "Modify Bearer Failure Indication",
    MSG_DELETE_BEARER_CMD:                  "Delete Bearer Command",
    MSG_DELETE_BEARER_FAIL:                 "Delete Bearer Failure Indication",
    MSG_BEARER_RESOURCE_CMD:                "Bearer Resource Command",
    MSG_BEARER_RESOURCE_FAIL:               "Bearer Resource Failure Indication",
    MSG_DL_DATA_NOTIF_FAIL:                 "Downlink Data Notification Failure Indication",
    MSG_TRACE_SESSION_ACT:                  "Trace Session Activation",
    MSG_TRACE_SESSION_DEACT:                "Trace Session Deactivation",
    MSG_STOP_PAGING_INDICATION:             "Stop Paging Indication",
    MSG_CREATE_BEARER_REQ:                  "Create Bearer Request",
    MSG_CREATE_BEARER_RES:                  "Create Bearer Response",
    MSG_UPDATE_BEARER_REQ:                  "Update Bearer Request",
    MSG_UPDATE_BEARER_RES:                  "Update Bearer Response",
    MSG_DELETE_BEARER_REQ:                  "Delete Bearer Request",
    MSG_DELETE_BEARER_RES:                  "Delete Bearer Response",
    MSG_DELETE_PDN_CONN_SET_REQ:            "Delete PDN Connection Set Request",
    MSG_DELETE_PDN_CONN_SET_RES:            "Delete PDN Connection Set Response",
    MSG_PGW_DL_TRIGGER_NOTIFY:             "PGW Downlink Triggering Notification",
    MSG_PGW_DL_TRIGGER_ACK:                "PGW Downlink Triggering Acknowledge",
    MSG_IDENTIFICATION_REQ:                 "Identification Request",
    MSG_IDENTIFICATION_RES:                 "Identification Response",
    MSG_CONTEXT_REQ:                        "Context Request",
    MSG_CONTEXT_RES:                        "Context Response",
    MSG_CONTEXT_ACK:                        "Context Acknowledge",
    MSG_FORWARD_RELOC_REQ:                  "Forward Relocation Request",
    MSG_FORWARD_RELOC_RES:                  "Forward Relocation Response",
    MSG_FORWARD_RELOC_COMPLETE_NOTIFY:      "Forward Relocation Complete Notification",
    MSG_FORWARD_RELOC_COMPLETE_ACK:         "Forward Relocation Complete Acknowledge",
    MSG_FORWARD_ACCESS_CONTEXT_NOTIFY:      "Forward Access Context Notification",
    MSG_FORWARD_ACCESS_CONTEXT_ACK:         "Forward Access Context Acknowledge",
    MSG_RELOC_CANCEL_REQ:                   "Relocation Cancel Request",
    MSG_RELOC_CANCEL_RES:                   "Relocation Cancel Response",
    MSG_CONFIG_TRANSFER_TUNNEL:             "Configuration Transfer Tunnel",
    MSG_DETACH_NOTIFY:                      "Detach Notification",
    MSG_DETACH_ACK:                         "Detach Acknowledge",
    MSG_CS_PAGING_INDICATION:               "CS Paging Indication",
    MSG_RAN_INFO_RELAY:                     "RAN Information Relay",
    MSG_ALERT_MME_NOTIFY:                   "Alert MME Notification",
    MSG_ALERT_MME_ACK:                      "Alert MME Acknowledge",
    MSG_UE_ACTIVITY_NOTIFY:                 "UE Activity Notification",
    MSG_UE_ACTIVITY_ACK:                    "UE Activity Acknowledge",
    MSG_ISR_STATUS_INDICATION:              "ISR Status Indication",
    MSG_UE_REGIST_QUERY_REQ:                "UE Registration Query Request",
    MSG_UE_REGIST_QUERY_RES:                "UE Registration Query Response",
    MSG_CREATE_FORWARDING_TUNNEL_REQ:       "Create Forwarding Tunnel Request",
    MSG_CREATE_FORWARDING_TUNNEL_RES:       "Create Forwarding Tunnel Response",
    MSG_SUSPEND_NOTIFY:                     "Suspend Notification",
    MSG_SUSPEND_ACK:                        "Suspend Acknowledge",
    MSG_RESUME_NOTIFY:                      "Resume Notification",
    MSG_RESUME_ACK:                         "Resume Acknowledge",
    MSG_CREATE_INDIRECT_DATA_FWD_TUNNEL_REQ: "Create Indirect Data Forwarding Tunnel Request",
    MSG_CREATE_INDIRECT_DATA_FWD_TUNNEL_RES: "Create Indirect Data Forwarding Tunnel Response",
    MSG_DELETE_INDIRECT_DATA_FWD_TUNNEL_REQ: "Delete Indirect Data Forwarding Tunnel Request",
    MSG_DELETE_INDIRECT_DATA_FWD_TUNNEL_RES: "Delete Indirect Data Forwarding Tunnel Response",
    MSG_RELEASE_ACCESS_BEARERS_REQ:         "Release Access Bearers Request",
    MSG_RELEASE_ACCESS_BEARERS_RES:         "Release Access Bearers Response",
    MSG_DL_DATA_NOTIFY:                     "Downlink Data Notification",
    MSG_DL_DATA_NOTIFY_ACK:                 "Downlink Data Notification Acknowledge",
    MSG_PGW_RESTART_NOTIFY:                 "PGW Restart Notification",
    MSG_PGW_RESTART_ACK:                    "PGW Restart Notification Acknowledge",
    MSG_UPDATE_PDN_CONN_SET_REQ:            "Update PDN Connection Set Request",
    MSG_UPDATE_PDN_CONN_SET_RES:            "Update PDN Connection Set Response",
    MSG_MODIFY_ACCESS_BEARERS_REQ:          "Modify Access Bearers Request",
    MSG_MODIFY_ACCESS_BEARERS_RES:          "Modify Access Bearers Response",
    MSG_MBMS_SESSION_START_REQ:             "MBMS Session Start Request",
    MSG_MBMS_SESSION_START_RES:             "MBMS Session Start Response",
    MSG_MBMS_SESSION_UPDATE_REQ:            "MBMS Session Update Request",
    MSG_MBMS_SESSION_UPDATE_RES:            "MBMS Session Update Response",
    MSG_MBMS_SESSION_STOP_REQ:              "MBMS Session Stop Request",
    MSG_MBMS_SESSION_STOP_RES:              "MBMS Session Stop Response",
}

# ---------------------------------------------------------------------------
# GTPv2 IE Type codes (from Wireshark packet-gtpv2.c)
# ---------------------------------------------------------------------------
IE_RESERVED                     = 0
IE_IMSI                         = 1
IE_CAUSE                        = 2
IE_RECOVERY                     = 3
# SRVCC (51-62)
IE_STN_SR                       = 51
IE_SRC_TGT_TRANS_CON            = 52
IE_TGT_SRC_TRANS_CON            = 53
IE_MM_CON_EUTRAN_SRVCC          = 54
IE_MM_CON_UTRAN_SRVCC           = 55
IE_SRVCC_CAUSE                  = 56
IE_TGT_RNC_ID                   = 57
IE_TGT_GLOBAL_CELL_ID           = 58
IE_TEID_C                       = 59
IE_SV_FLAGS                     = 60
IE_SAI                          = 61
IE_MM_CTX_FOR_CS_TO_PS_SRVCC    = 62
# Main IEs
IE_APN                          = 71
IE_AMBR                         = 72
IE_EBI                          = 73
IE_IP_ADDRESS                   = 74
IE_MEI                          = 75
IE_MSISDN                       = 76
IE_INDICATION                   = 77
IE_PCO                          = 78
IE_PAA                          = 79
IE_BEARER_QOS                   = 80
IE_FLOW_QOS                     = 81
IE_RAT_TYPE                     = 82
IE_SERVING_NET                  = 83
IE_BEARER_TFT                   = 84
IE_TAD                          = 85
IE_ULI                          = 86
IE_F_TEID                       = 87
IE_TMSI                         = 88
IE_GLOBAL_CN_ID                 = 89
IE_S103PDF                      = 90
IE_S1UDF                        = 91
IE_DEL_VAL                      = 92
IE_BEARER_CTX                   = 93
IE_CHARGING_ID                  = 94
IE_CHARGING_CHARS               = 95
IE_TRACE_INFO                   = 96
IE_BEARER_FLAGS                 = 97
IE_PDN_TYPE                     = 99
IE_PTI                          = 100
IE_DRX_PARAM                    = 101
IE_UE_NET_CAPABILITY            = 102
IE_MM_CTX_GSM_T                 = 103
IE_MM_CTX_UMTS_CQ               = 104
IE_MM_CTX_GSM_CQ                = 105
IE_MM_CTX_UMTS_Q                = 106
IE_MM_CTX_EPS_QQ                = 107
IE_MM_CTX_UMTS_QQ               = 108
IE_PDN_CONNECTION               = 109
IE_PDN_NUMBERS                  = 110
IE_P_TMSI                       = 111
IE_P_TMSI_SIG                   = 112
IE_HOP_COUNTER                  = 113
IE_UE_TIME_ZONE                 = 114
IE_TRACE_REFERENCE              = 115
IE_COMPLETE_REQ_MSG             = 116
IE_GUTI                         = 117
IE_F_CONTAINER                  = 118
IE_F_CAUSE                      = 119
IE_SEL_PLMN_ID                  = 120
IE_TARGET_ID                    = 121
IE_PKT_FLOW_ID                  = 123
IE_RAB_CONTEXT                  = 124
IE_S_RNC_PDCP_CTX_INFO          = 125
IE_UDP_S_PORT_NR                = 126
IE_APN_RESTRICTION              = 127
IE_SEL_MODE                     = 128
IE_SOURCE_IDENT                 = 129
IE_BEARER_CONTROL_MODE          = 130
IE_CNG_REP_ACT                  = 131
IE_FQ_CSID                      = 132
IE_CHANNEL_NEEDED               = 133
IE_EMLPP_PRI                    = 134
IE_NODE_TYPE                    = 135
IE_FQDN                         = 136
IE_TI                           = 137
IE_MBMS_SESSION_DURATION        = 138
IE_MBMS_SERVICE_AREA            = 139
IE_MBMS_SESSION_ID              = 140
IE_MBMS_FLOW_ID                 = 141
IE_MBMS_IP_MC_DIST              = 142
IE_MBMS_DIST_ACK                = 143
IE_RFSP_INDEX                   = 144
IE_UCI                          = 145
IE_CSG_INFO_REP_ACTION          = 146
IE_CSG_ID                       = 147
IE_CMI                          = 148
IE_SERVICE_INDICATOR            = 149
IE_DETACH_TYPE                  = 150
IE_LDN                          = 151
IE_NODE_FEATURES                = 152
IE_MBMS_TIME_TO_DATA_XFER       = 153
IE_THROTTLING                   = 154
IE_ARP                          = 155
IE_EPC_TIMER                    = 156
IE_SIG_PRIO_IND                 = 157
IE_TMGI                         = 158
IE_ADD_MM_CONT_FOR_SRVCC        = 159
IE_ADD_FLAGS_FOR_SRVCC          = 160
IE_MMBR                         = 161
IE_MDT_CONFIG                   = 162
IE_APCO                         = 163
IE_ABS_MBMS_DATA_TF_TIME        = 164
IE_HENB_INFO_REPORT             = 165
IE_IP4CP                        = 166
IE_CHANGE_TO_REPORT_FLAGS       = 167
IE_ACTION_INDICATION            = 168
IE_TWAN_IDENTIFIER              = 169
IE_ULI_TIMESTAMP                = 170
IE_MBMS_FLAGS                   = 171
IE_RAN_NAS_CAUSE                = 172
IE_CN_OP_SEL_ENT                = 173
IE_TRUST_WLAN_MODE_IND          = 174
IE_NODE_NUMBER                  = 175
IE_NODE_IDENTIFIER              = 176
IE_PRES_REP_AREA_ACT            = 177
IE_PRES_REP_AREA_INF            = 178
IE_TWAN_ID_TS                   = 179
IE_OVERLOAD_CONTROL_INF         = 180
IE_LOAD_CONTROL_INF             = 181
IE_METRIC                       = 182
IE_SEQ_NO                       = 183
IE_APN_AND_REL_CAP              = 184
IE_WLAN_OFFLOADABILITY_IND      = 185
IE_PAGING_AND_SERVICE_INF       = 186
IE_INTEGER_NUMBER               = 187
IE_MILLISECOND_TS               = 188
IE_MONITOR_EVENT_INFO           = 189
IE_REMOTE_UE_CTX                = 191
IE_EPCO                         = 197
IE_SERVING_PLMN_RATE_CONTROL    = 198
IE_COUNTER                      = 199
IE_MAP_USAGE                    = 200
IE_PRIVATE_EXT                  = 255

IE_TYPE_NAMES: dict[int, str] = {
    IE_IMSI:                    "IMSI",
    IE_CAUSE:                   "Cause",
    IE_RECOVERY:                "Recovery",
    IE_APN:                     "Access Point Name",
    IE_AMBR:                    "Aggregate Maximum Bit Rate",
    IE_EBI:                     "EPS Bearer ID",
    IE_IP_ADDRESS:              "IP Address",
    IE_MEI:                     "MEI",
    IE_MSISDN:                  "MSISDN",
    IE_INDICATION:              "Indication",
    IE_PCO:                     "PCO",
    IE_PAA:                     "PDN Address Allocation",
    IE_BEARER_QOS:              "Bearer QoS",
    IE_FLOW_QOS:                "Flow QoS",
    IE_RAT_TYPE:                "RAT Type",
    IE_SERVING_NET:             "Serving Network",
    IE_BEARER_TFT:              "Bearer TFT",
    IE_ULI:                     "User Location Information",
    IE_F_TEID:                  "Fully Qualified TEID",
    IE_BEARER_CTX:              "Bearer Context",
    IE_CHARGING_ID:             "Charging ID",
    IE_CHARGING_CHARS:          "Charging Characteristics",
    IE_BEARER_FLAGS:            "Bearer Flags",
    IE_PDN_TYPE:                "PDN Type",
    IE_PTI:                     "Procedure Transaction ID",
    IE_UE_TIME_ZONE:            "UE Time Zone",
    IE_APN_RESTRICTION:         "APN Restriction",
    IE_SEL_MODE:                "Selection Mode",
    IE_BEARER_CONTROL_MODE:     "Bearer Control Mode",
    IE_FQ_CSID:                 "FQ-CSID",
    IE_NODE_TYPE:               "Node Type",
    IE_FQDN:                    "FQDN",
    IE_TI:                      "Transaction Identifier",
    IE_ARP:                     "ARP",
    IE_PRIVATE_EXT:             "Private Extension",
}

# Cause values (TS 29.274 Table 8.4-1)
CAUSE_LOCAL_DETACH                  = 2
CAUSE_COMPLETE_DETACH               = 3
CAUSE_RAT_CHANGED_3GPP_TO_WLAN     = 4
CAUSE_ISR_DEACTIVATION              = 5
CAUSE_ERROR_IND_FROM_RNC_ENODEB    = 6
CAUSE_IMSI_DETACH_ONLY              = 7
CAUSE_REACTIVATION_REQUESTED        = 8
CAUSE_PDN_RECONNECTION_TO_THIS_APN_DISALLOWED = 9
CAUSE_ACCESS_CHANGED_FROM_NON_3GPP = 10
CAUSE_REQUEST_ACCEPTED              = 16
CAUSE_REQUEST_ACCEPTED_PARTIALLY    = 17
CAUSE_NEW_PDN_TYPE_DUE_NETWORK      = 18
CAUSE_NEW_PDN_TYPE_DUE_SINGLE_ADDR = 19
CAUSE_CONTEXT_NOT_FOUND             = 64
CAUSE_INVALID_MSG_FORMAT            = 65
CAUSE_VERSION_NOT_SUPPORTED         = 66
CAUSE_INVALID_LENGTH                = 67
CAUSE_SERVICE_NOT_SUPPORTED         = 68
CAUSE_MANDATORY_IE_INCORRECT        = 69
CAUSE_MANDATORY_IE_MISSING          = 70
CAUSE_OPTIONAL_IE_INCORRECT         = 71
CAUSE_SYSTEM_FAILURE                = 72
CAUSE_NO_RESOURCES                  = 73
CAUSE_SEMANTIC_ERROR_TFT            = 74
CAUSE_SYNTACTIC_ERROR_TFT           = 75
CAUSE_SEMANTIC_ERROR_PACKET_FILTER  = 76
CAUSE_SYNTACTIC_ERROR_PACKET_FILTER = 77
CAUSE_MISSING_UNKNOWN_APN           = 78
CAUSE_GRE_KEY_NOT_FOUND             = 79
CAUSE_RELOCATION_FAILURE            = 80
CAUSE_DENIED_IN_RAT                 = 81
CAUSE_PREFERRED_PDN_TYPE_NOT_SUPPORTED = 82
CAUSE_ALL_DYNAMIC_ADDR_OCCUPIED     = 83
CAUSE_UE_CONTEXT_WITHOUT_TFT_ACTIVATED = 84
CAUSE_PROTOCOL_TYPE_NOT_SUPPORTED   = 85
CAUSE_UE_NOT_RESPONDING             = 86
CAUSE_UE_REFUSES                    = 87
CAUSE_SERVICE_DENIED                = 88
CAUSE_UNABLE_TO_PAGE_UE             = 89
CAUSE_NO_MEMORY                     = 90
CAUSE_USER_AUTH_FAILED              = 91
CAUSE_APN_ACCESS_DENIED             = 92
CAUSE_REQUEST_REJECTED              = 93
CAUSE_P_TMSI_SIG_MISMATCH           = 94
CAUSE_IMSI_IMEI_NOT_KNOWN           = 95
CAUSE_SEMANTIC_ERROR_HDR_FLAGS      = 96
CAUSE_SYNTACTIC_ERROR_HDR_FLAGS     = 97
CAUSE_SEMANTIC_ERRORS_IN_TAD        = 98
CAUSE_SYNTACTIC_ERRORS_IN_TAD       = 99
CAUSE_MUTUALLY_EXCLUSIVE_TADS       = 100
CAUSE_REMOTE_PEER_NOT_RESPONDING    = 101
CAUSE_COLLISION_WITH_NW_INIT_REQ    = 102
CAUSE_UNABLE_TO_PAGE_UE_DUE_SUSPENSION = 103
CAUSE_COND_IE_MISSING               = 104
CAUSE_APN_RESTRICTION_INCOMPATIBLE  = 105
CAUSE_INVALID_OVERALL_LEN_OF_TRIGGER_PKT = 106
CAUSE_DATA_FORWARDING_NOT_SUPPORTED = 107
CAUSE_INVALID_REPLY_FROM_REMOTE_PEER = 108
CAUSE_FALLBACK_TO_GTPV1             = 109
CAUSE_INVALID_PEER                  = 110
CAUSE_TEMPORARILY_REJECTED          = 111
CAUSE_MODIFICATIONS_NOT_LIMITED_TO_S1_U = 112
CAUSE_REQUEST_REJECTED_FOR_PMIPv6   = 113
CAUSE_APN_CONGESTION                = 114
CAUSE_BEARER_HANDLING_NOT_SUPPORTED = 115
CAUSE_UE_ALREADY_RE_ATTACHED        = 116
CAUSE_MULTIPLE_PDN_CONN_SAME_APN_NOT_ALLOWED = 117

# RAT Type values (TS 29.274 §8.17)
RAT_UTRAN                   = 1
RAT_GERAN                   = 2
RAT_WLAN                    = 3
RAT_GAN                     = 4
RAT_HSPA_EVOLUTION          = 5
RAT_EUTRAN                  = 6
RAT_VIRTUAL                 = 7
RAT_EUTRAN_NB_IOT           = 8
RAT_LTE_M                   = 9
RAT_NR                      = 10

# PDN Type values
PDN_TYPE_IPv4               = 1
PDN_TYPE_IPv6               = 2
PDN_TYPE_IPv4v6             = 3
PDN_TYPE_NON_IP             = 4

# F-TEID Interface Types (TS 29.274 Table 8.22-1)
FTEID_S1U_ENODEB            = 0
FTEID_S1U_SGW               = 1
FTEID_S12_RNC               = 2
FTEID_S12_SGW               = 3
FTEID_S5S8U_SGW             = 4
FTEID_S5S8U_PGW             = 5
FTEID_S5S8C_SGW             = 6
FTEID_S5S8C_PGW             = 7
FTEID_S5S8_PMIPv6_SGW       = 8
FTEID_S5S8_PMIPv6_PGW       = 9
FTEID_S11_MME               = 10
FTEID_S11S4_SGW             = 11
FTEID_S10_MME               = 12
FTEID_S3_MME                = 13
FTEID_S3_SGSN               = 14
FTEID_S4U_SGSN              = 15
FTEID_S4U_SGW               = 16
FTEID_S4C_SGSN              = 17
FTEID_S16_SGSN              = 18
FTEID_ENODEB_FOR_X2         = 19
FTEID_ENODEB_GTP_U_FOR_X2   = 20
FTEID_TARGET_ENODEB         = 21
FTEID_SGW_GTP_U_FOR_DL_DATA_FWD = 22
FTEID_SGW_GTP_U_FOR_UL_DATA_FWD = 23
FTEID_RNC_GTP_U             = 24
FTEID_SGSN_GTP_U            = 25
FTEID_SGW_GTP_U_FOR_UL_DATA_FWD2 = 26
FTEID_SM_MBMS_GW            = 27
FTEID_SN_MBMS_GW            = 28
FTEID_SM_MME                = 29
FTEID_SN_SGSN               = 30
FTEID_SGW_GTP_U_FOR_UL      = 31

# Node Type values
NODE_TYPE_MME               = 0
NODE_TYPE_SGSN              = 1
