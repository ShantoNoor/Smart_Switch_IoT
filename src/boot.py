import gc

from machine import Pin

import rtime
import tft_config
import wifi as WiFi

gc.enable()

tft = tft_config.config(0)
wifi = WiFi.Wifi()
real_time = rtime.RTime()


def connect_wifi():
    try:
        wifi.connect()
    except OSError as exc:
        print('Unable to connect to wifi ... ')
        # print(errno.errorcode[exc.errno])
        # reset()


if __name__ == '__main__':
    gc.collect()
    tft.init()
    tft.png('boot.png', 0, 0)

    gc.collect()
    connect_wifi()

    gc.collect()
    real_time.init()

    # Enable ADC for getting battery voltage
    gc.collect()
    ADC_EN = Pin(14, Pin.OUT)
    ADC_EN.value(1)
