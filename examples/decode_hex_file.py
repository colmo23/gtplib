#!/usr/bin/env python3
"""Decode a GTP-C hex file and print each packet with all its IEs.

Usage:
    python3 examples/decode_hex_file.py [hex_file] [-v | --verbose]

hex_file defaults to examples/sample_packets.hex

Each non-blank, non-comment line in the file is treated as a hex-encoded
GTPv1-C or GTPv2-C packet.  The version is detected automatically from
the flags byte (bits 7-5):
  - 001 → GTPv1-C (port 2123)
  - 010 → GTPv2-C (port 2123)

Output per packet:
  [n]  GTPvX-C  <MessageName>  teid=0x...  seq=<n>  (<N> IEs)
    IE[0]  <TypeName>  <decoded fields>
    IE[1]  ...
    ...

-v / --verbose additionally prints a Wireshark-style hex dump of the raw bytes.
"""

import socket
import sys
from pathlib import Path

from gtpc.utils.hexdump import from_hex, hexdump
import gtpc.v1.messages as v1_msgs
import gtpc.v2.messages as v2_msgs
from gtpc.v1 import constants as V1
from gtpc.v2 import constants as V2
from gtpc.v2.ie.typed import BearerContextIE as V2BearerContextIE


# ---------------------------------------------------------------------------
# Version detection / dispatch
# ---------------------------------------------------------------------------

def _version(raw: bytes) -> int:
    return (raw[0] >> 5) & 0x7


def _decode(raw: bytes):
    ver = _version(raw)
    if ver == 1:
        return v1_msgs.decode_message(raw)
    elif ver == 2:
        return v2_msgs.decode_message(raw)
    raise ValueError(f"Unknown GTP version {ver} (flags byte 0x{raw[0]:02x})")


# ---------------------------------------------------------------------------
# IE formatting
# ---------------------------------------------------------------------------

def _ie_type_name(ie, ver: int) -> str:
    """Return a human-readable IE type name."""
    names = V1.IE_TYPE_NAMES if ver == 1 else V2.IE_TYPE_NAMES
    return names.get(ie.ie_type, f"IE-{ie.ie_type}")


def _fmt_addr(v) -> str:
    """Format an address value: bytes→dotted-decimal/colon-hex, str passthrough."""
    if isinstance(v, bytes):
        if len(v) == 4:
            return socket.inet_ntoa(v)
        if len(v) == 16:
            return socket.inet_ntop(socket.AF_INET6, v)
        return v.hex()
    return str(v)


def _ie_fields(ie) -> str:
    """Extract interesting decoded fields from an IE as a string."""
    # Named attributes to probe, in priority order.
    # Each entry: (attr_name, format_fn)
    PROBES = [
        ("digits",          lambda v: f"digits={v!r}"),
        ("apn",             lambda v: f"apn={v!r}"),
        ("restart_counter", lambda v: f"restart_counter={v}"),
        ("cause",           lambda v: f"cause=0x{v:02x}({v})"),
        ("teid",            lambda v: f"teid=0x{v:08x}"),
        ("nsapi",           lambda v: f"nsapi={v}"),
        ("ebi",             lambda v: f"ebi={v}"),
        ("rat",             lambda v: f"rat={v}"),
        ("mode",            lambda v: f"mode={v}"),
        ("uplink_kbps",     lambda v: f"ul={v}kbps"),
        ("downlink_kbps",   lambda v: f"dl={v}kbps"),
        ("qci",             lambda v: f"qci={v}"),
        ("pl",              lambda v: f"pl={v}"),
        ("mbr_ul",          lambda v: f"mbr_ul={v}"),
        ("mbr_dl",          lambda v: f"mbr_dl={v}"),
        ("gbr_ul",          lambda v: f"gbr_ul={v}"),
        ("gbr_dl",          lambda v: f"gbr_dl={v}"),
        ("address",         lambda v: f"addr={_fmt_addr(v)}"),
        ("ipv4",            lambda v: f"ipv4={v}"),
        ("ipv6",            lambda v: f"ipv6={v}"),
        ("interface_type",  lambda v: f"iface={v}"),
        ("pdn_type",        lambda v: f"pdn_type={v}"),
        ("mcc",             lambda v: f"mcc={v}"),
        ("mnc",             lambda v: f"mnc={v}"),
        ("lac",             lambda v: f"lac={v}"),
        ("rac",             lambda v: f"rac={v}"),
        ("tac",             lambda v: f"tac=0x{v:04x}"),
        ("eci",             lambda v: f"eci=0x{v:06x}"),
        ("teardown",        lambda v: f"teardown={v}"),
        ("cmd",             lambda v: f"cmd={v}"),
        ("rat_type",        lambda v: f"rat_type={v}"),
        ("node_type",       lambda v: f"node_type={v}"),
    ]

    parts = []
    seen = set()
    for attr, fmt in PROBES:
        if attr in seen:
            continue
        val = getattr(ie, attr, None)
        if val is not None and val != b"":
            parts.append(fmt(val))
            seen.add(attr)

    # Fall back to raw value bytes for unknown IEs (no named attrs decoded)
    if not parts:
        raw_val = getattr(ie, "value", b"")
        if raw_val:
            parts.append(f"value={raw_val.hex()}")

    return "  ".join(parts)


def _print_ie(ie, ver: int, prefix: str = "  ") -> None:
    """Print one IE with its decoded fields; recurse into grouped IEs."""
    if isinstance(ie, V2BearerContextIE):
        instance = getattr(ie, "instance", 0)
        print(f"{prefix}BearerContext (instance={instance})  [{len(ie.grouped_ies)} IEs]")
        for child in ie.grouped_ies:
            _print_ie(child, ver, prefix=prefix + "  ")
        return

    type_name = _ie_type_name(ie, ver)
    fields = _ie_fields(ie)
    line = f"{prefix}{type_name}"
    if fields:
        line += f"  {fields}"
    print(line)


# ---------------------------------------------------------------------------
# Packet printing
# ---------------------------------------------------------------------------

def _print_packet(packet_num: int, raw: bytes, msg, description: str) -> None:
    ver = _version(raw)
    ver_str = f"GTPv{ver}-C"
    name = type(msg).__name__
    teid = msg.header.teid
    seq = msg.header.seq_num
    n_ies = len(msg.ies)

    teid_str = f"0x{teid:08x}" if teid is not None else "none"
    seq_str = str(seq) if seq is not None else "-"

    header_line = (
        f"[{packet_num:3d}]  {ver_str}  {name:<45s}"
        f"  teid={teid_str:<10}  seq={seq_str:>5}  ({n_ies} IEs)"
    )
    if description:
        header_line += f"  # {description}"
    print(header_line)

    for ie in msg.ies:
        _print_ie(ie, ver)


# ---------------------------------------------------------------------------
# Main decode loop
# ---------------------------------------------------------------------------

def decode_file(path: Path, *, verbose: bool = False) -> None:
    lines = path.read_text().splitlines()

    description = ""
    packet_num = 0
    errors = 0

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            if stripped.startswith("# ") and not stripped.startswith("# GTP-C sample"):
                description = stripped[2:]
            continue

        packet_num += 1
        try:
            raw = from_hex(stripped)
            msg = _decode(raw)
        except Exception as exc:
            print(f"[{packet_num:3d}]  ERROR  {description!r}: {exc}")
            errors += 1
            description = ""
            continue

        _print_packet(packet_num, raw, msg, description)
        description = ""

        if verbose:
            print()
            print(hexdump(raw))

        print()

    print(f"Decoded {packet_num} packet(s), {errors} error(s).")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    args = sys.argv[1:]

    verbose = "--verbose" in args or "-v" in args
    args = [a for a in args if a not in ("--verbose", "-v")]

    path = Path(args[0]) if args else Path(__file__).parent / "sample_packets.hex"

    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)

    print(f"Decoding {path} …\n")
    decode_file(path, verbose=verbose)


if __name__ == "__main__":
    main()
