import md5
from utils import *


def create_packet(recv_data, payload, TOKEN):
    packet_payload = hex_to_byte(payload)

    packet_length = hex(len(packet_payload) + 32)[2:]
    while len(packet_length) != 4:
        packet_length = '0' + packet_length

    packet_head = hex_to_byte(recv_data[:4] + packet_length + recv_data[8:32] + TOKEN)

    packet = bytearray(packet_head + packet_payload)

    packet_checksum = hex_to_byte(md5.digest(packet))

    for i in range(0, 16):
        packet[i + 16] = packet_checksum[i]

    return packet
