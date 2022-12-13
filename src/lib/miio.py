import socket
from packet_creator import *
from CONFIG import *
import time
import gc
from utils import *

HELLO_PACKET = '21310020ffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
GET_INFO_DATA = '5edc00f3fd2d5d3bec1c5ff56e78e2645fc529220e5f09e59f4d9bb58762ef5f9620fa9d2215ec0621b71075d2cd7f2d'
# GET_POWER_STATUS_DATA = 'afe0e9c5e26a2a26bbba23bd452e487e47e227086b5d55aac62949c533e0ea44782fde3e3f1d235eff60e25b31c8fa77'
GET_POWER_STATUS_DATA = 'd9bf76d83d66e70fae7a06d53f59b9a38c733add0b26b72b6615026fff9da1abc1d2d783b00e5595b89c5f8063facb74'
POWER_OFF_DATA = '6aaebcddf12b4ee2d7319208d9031fefb653297a3d2bfd56efffb0659c6b6b760e8560ffd2afd041e13ae8e8c0ad8b42'
POWER_ON_DATA = '6aaebcddf12b4ee2d7319208d9031fefb653297a3d2bfd56efffb0659c6b6b76966833b94b9e6e8059f0de76850d358e'

# POWER_OFF_RES = b'fa86de130b760f7ab8a83cdc6b6eca9cc47e5856b20940f28094db44c1f8e23a'
POWER_OFF_RES = b'97c9bbe7c213c9993a6430ed71f2d9229db5c8e11d59e4293700b9c1afb8fdd6'

POWER_ON_RES = b'3db745d2fb7d44ed7081af6ae5ee3d2797da3d285d8922ea894414f46a1d94a0'
OK_RES = b'a8855aa73e57e096623c630044f7f98ce07bbee6299249f4d67bc03fe8a5369f'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", 12345))


def send_and_recv_packet(try_time=30):
    end_time = time.time() + try_time
    sock.sendto(hex_to_byte(HELLO_PACKET), ('192.168.0.255', 54321))

    data, addr = b'', ''
    while data[16:24] != DEVICE_NAME:
        data, addr = sock.recvfrom(1024)
        data = byte_to_hex(data)

        if (time.time() > end_time):
            print('Unable to send and receive hello_packet ... ')
            return None, None

    return data, addr


def get_status():
    gc.collect()

    data, addr = send_and_recv_packet()

    print(data)
    print(addr)

    if data is not None and addr is not None:
        packet = create_packet(data, GET_POWER_STATUS_DATA, DEVICE_TOKEN)
        print(packet)
        sock.sendto(packet, addr)
        data, addr = sock.recvfrom(1024)

        if data is not None:
            print('hello')
            data = byte_to_hex(data)[64:]
            print(data)
            print(addr)
            print(POWER_OFF_RES)
            print(POWER_ON_RES)

            if (data == POWER_ON_RES):
                return True
            elif (data == POWER_OFF_RES):
                return False

    return None


def power_on():
    gc.collect()

    data, addr = send_and_recv_packet()

    if data is not None and addr is not None:
        packet = create_packet(data, POWER_ON_DATA, DEVICE_TOKEN)

        sock.sendto(packet, addr)
        data, addr = sock.recvfrom(1024)

        data = byte_to_hex(data)[64:]

        if data is not None and data == OK_RES:
            return True
        else:
            return False

    return None


def power_off():
    gc.collect()

    data, addr = send_and_recv_packet()

    if data is not None and addr is not None:
        packet = create_packet(data, POWER_OFF_DATA, DEVICE_TOKEN)

        sock.sendto(packet, addr)
        data, addr = sock.recvfrom(1024)

        data = byte_to_hex(data)[64:]

        if data is not None and data == OK_RES:
            return True
        else:
            return False

    return None
