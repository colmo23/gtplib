"""BCD (Binary Coded Decimal) encoding/decoding.

Used for IMSI, MSISDN, MEI fields in GTP packets.
Each byte encodes two decimal digits, low nibble first.
Unused trailing nibbles are set to 0xF (filler).
"""


def encode(digits: str) -> bytes:
    """Encode a digit string to BCD bytes (low nibble first, 0xF filler).

    >>> encode("123456789012345").hex()
    '214365870921436f'
    """
    if len(digits) % 2:
        digits += "F"
    out = bytearray()
    for i in range(0, len(digits), 2):
        lo = int(digits[i], 16)
        hi = int(digits[i + 1], 16)
        out.append((hi << 4) | lo)
    return bytes(out)


def decode(data: bytes, strip_filler: bool = True) -> str:
    """Decode BCD bytes to a digit string.

    >>> decode(bytes.fromhex("214365870921436f"))
    '123456789012345'
    """
    digits = []
    for b in data:
        lo = b & 0x0F
        hi = (b >> 4) & 0x0F
        digits.append(format(lo, "X"))
        digits.append(format(hi, "X"))
    s = "".join(digits)
    if strip_filler:
        s = s.rstrip("F").rstrip("f")
    return s
