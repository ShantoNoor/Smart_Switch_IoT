import binascii

from ucryptolib import aes

import CONFIG
import md5

key = md5.digest(binascii.unhexlify(CONFIG.DEVICE_TOKEN))  # -> hex
iv = md5.digest(binascii.unhexlify(key + CONFIG.DEVICE_TOKEN))  # -> hex

key = binascii.unhexlify(key)  # -> bytes
iv = binascii.unhexlify(iv)  # -> bytes

MODE_CBC = 2


def encrypt(byte_str):  # byte_str -> hex(str)
    cipher = aes(key, MODE_CBC, iv)

    # print("Using AES{}-CBC cipher".format(len(key * 8)))

    # AES works in 16-bytes blocks, PKCS#7 padding
    block_size = 16
    padding_length = block_size - len(byte_str) % block_size
    padding = bytes([padding_length] * padding_length)
    padded_plaintext = byte_str + padding

    encrypted = cipher.encrypt(padded_plaintext)
    return binascii.hexlify(encrypted).decode()


def decrypt(byte):  # str(hex) -> byte_str
    decipher = aes(key, MODE_CBC, iv)
    decrypted = decipher.decrypt(binascii.unhexlify(byte))

    # Get the padding length from the last byte of the decrypted message
    padding_length = decrypted[-1]

    # Remove the padding bytes from the decrypted message
    decrypted = decrypted[:-padding_length]

    return decrypted
