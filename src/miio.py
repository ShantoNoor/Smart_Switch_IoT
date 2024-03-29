import gc
import socket

import aes
import miio_data
from CONFIG import *
from packet_creator import *
from utils import *


def get_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", 12345))
    sock.settimeout(0.5)
    return sock


def send_and_recv_packet():
    gc.collect()

    sock = get_socket()
    try:
        sock.sendto(hex_to_byte(miio_data.HELLO_PACKET), ('192.168.0.255', 54321))
        data, addr = sock.recvfrom(100)
    except OSError as exc:
        print('Unable to Send and Receive Hello Packet ... ')
        # print(errno.errorcode[exc.errno])
        return b'', b''
    finally:
        sock.close()

    if data != b'':
        data = byte_to_hex(data)
        return data, addr

    return b'', b''


def get_status():
    data, addr = send_and_recv_packet()

    if data == b'' or addr == b'':
        return None

    gc.collect()
    packet = create_packet(data, aes.encrypt(miio_data.GET_POWER_STATUS_DATA), DEVICE_TOKEN)

    gc.collect()

    sock = get_socket()
    try:
        sock.sendto(packet, addr)
        data, addr = sock.recvfrom(100)
    except OSError as exc:
        print('Unable to Send and Receive Packet ... ')
        # print(errno.errorcode[exc.errno])
        return None
    finally:
        sock.close()

    if data != b'':
        data = byte_to_hex(data)[64:]
        data = aes.decrypt(data)
        if data == miio_data.POWER_ON_RES:
            return True
        elif data == miio_data.POWER_OFF_RES:
            return False

    print(data)
    return None


def set_power(value=False):
    data, addr = send_and_recv_packet()

    if data == b'' or addr == b'':
        return None

    PACKET_DATA = miio_data.POWER_OFF_DATA
    if value:
        PACKET_DATA = miio_data.POWER_ON_DATA

    gc.collect()
    packet = create_packet(data, aes.encrypt(PACKET_DATA), DEVICE_TOKEN)

    gc.collect()

    sock = get_socket()
    try:
        sock.sendto(packet, addr)
        data, addr = sock.recvfrom(100)
    except OSError as exc:
        print('Unable to Send and Receive Packet ... ')
        # print(errno.errorcode[exc.errno])
        return None
    finally:
        sock.close()

    if data != b'':
        data = byte_to_hex(data)[64:]
        data = aes.decrypt(data)
        if data == miio_data.OK_RES:
            return True

    print(data)
    return None
