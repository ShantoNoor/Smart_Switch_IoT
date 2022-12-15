import network, time
from CONFIG import *
import wifi_logo
import gc

class Wifi:
    def __init__(self):
        self.wifi = network.WLAN(network.STA_IF)

    def isconnected(self):
        return self.wifi.isconnected()

    def get_rssi(self):
        if not self.isconnected():
            return None
        return self.wifi.status('rssi')

    def connect(self, tft, try_time=10):
        if not self.isconnected():
            end_time = time.time() + try_time
            print('connecting to network...')
            self.wifi.active(True)
            self.wifi.connect(SSID, PASSWORD)

            while not self.isconnected():
                for i in range(4):
                    tft.bitmap(wifi_logo, 17, 70, i)
                    time.sleep(0.25)

                tft.fill(0)
                gc.collect()

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
            return '0%'

        rssi = self.get_rssi()
        if (rssi > -67):
            return '90%'
        elif (rssi > -80):
            return '50%'

        return '10%'

    def get_ip(self):
        if not self.isconnected():
            return None
        return self.wifi.ifconfig()[0]

