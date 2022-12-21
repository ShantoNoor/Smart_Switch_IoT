import time
import network
from CONFIG import *


class Wifi:
    def __init__(self):
        self.wifi = network.WLAN(network.STA_IF)

    def isconnected(self):
        return self.wifi.isconnected()

    def get_rssi(self):
        if not self.isconnected():
            return None
        return self.wifi.status('rssi')

    def connect(self, try_time=10):
        if not self.isconnected():
            end_time = time.time() + try_time
            print('connecting to network...')
            self.wifi.active(True)
            self.wifi.connect(SSID, PASSWORD)

            while not self.isconnected():
                if (time.time() > end_time):
                    print('Unable to connect to network ... ')
                    self.wifi.active(False)
                    return False

        print('network config:', self.wifi.ifconfig())
        return True

    def disconnect(self):
        self.wifi.disconnect()
        self.wifi.active(False)

    def status(self):
        if not self.isconnected():
            return None

        rssi = self.get_rssi()
        if (rssi > -67):
            return 'good'
        elif (rssi > -80):
            return 'okey'

        return 'poor'

    def get_ip(self):
        if not self.isconnected():
            return None
        return self.wifi.ifconfig()[0]
