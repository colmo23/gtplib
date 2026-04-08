"""Hex string parsing and Wireshark-style hex dump."""


def from_hex(s: str) -> bytes:
    """Parse a hex string (with optional spaces/colons) into bytes.

    >>> from_hex("32 10 00 97").hex()
    '32100097'
    >>> from_hex("32:10:00:97").hex()
    '32100097'
    """
    s = s.strip().replace(":", "").replace(" ", "").replace("\n", "")
    return bytes.fromhex(s)


def hexdump(data: bytes, width: int = 16) -> str:
    """Return a Wireshark-style hex dump string.

    Example output:
        0000  32 10 00 97 00 00 00 00  00 fe 00 00 02 72 02 03  2........ .r..
    """
    lines = []
    for offset in range(0, len(data), width):
        chunk = data[offset:offset + width]
        hex_part = " ".join(f"{b:02x}" for b in chunk)
        # Insert extra space in middle for readability
        if len(chunk) > 8:
            mid = 8 * 3 - 1  # position after 8 bytes
            hex_part = hex_part[:mid] + "  " + hex_part[mid:]
        ascii_part = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        lines.append(f"{offset:04x}  {hex_part:<{width * 3 + 1}}  {ascii_part}")
    return "\n".join(lines)
