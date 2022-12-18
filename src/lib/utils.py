import binascii

def hex_to_byte(hex: str) -> bytes:
    return binascii.unhexlify(hex)


def byte_to_hex(bytes: bytes) -> str:
    return binascii.hexlify(bytes)

