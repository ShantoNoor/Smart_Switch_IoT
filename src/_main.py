import esp32
import st7789
import tft_config
from machine import *
from pushbutton import *
from tft_buttons import *
import uasyncio as asyncio
import vga2_8x16 as font16
import vga1_bold_16x16 as fontb16
import vga1_bold_16x32 as fontb32

import miio
from CONFIG import *
from wifi import *
from rtime import *
import gc

import wifi_icon
import battery_icon
from weather import *

gc.enable()

TIME_OUT = 10000

BUTTON_LEFT = 0
BUTTON_RIGHT = 1

SINGLE_PRESS = 2
DOUBLE_PRESS = 3
LONG_PRESS = 4

tft = tft_config.config(0)
tft.init()

t1 = Timer(0)
wifi = Wifi()


def left(text, height, bg=st7789.BLACK, font=font16, tc=st7789.WHITE):
    tft.text(
        font,
        text,
        0,
        height,
        tc,
        bg)


def right(text, height, bg=st7789.BLACK, font=font16, tc=st7789.WHITE):
    length = len(text)
    tft.text(
        font,
        text,
        tft.width() - length * font.WIDTH,
        height,
        tc,
        bg)


def middle(text, height, bg=st7789.BLACK, font=fontb32, tc=st7789.WHITE):
    length = len(text)
    tft.text(
        font,
        text,
        (tft.width() // 2) - (length * font.WIDTH) // 2,
        height,
        tc,
        bg)


def center(text, bg=st7789.BLACK, font=fontb32, fc=st7789.WHITE):
    length = len(text)
    tft.text(
        font,
        text,
        (tft.width() // 2) - (length * font.WIDTH) // 2,
        tft.height() // 2 - font.HEIGHT // 2,
        fc,
        bg)


def connect_wifi():
    middle('Conn..to', 20, font=fontb16)
    middle(SSID, 60)
    wifi.connect(tft)


connect_wifi()
gc.collect()

time.sleep(1)

real_time = RTime()
real_time.show_time()
gc.collect()


def _print(text, bg=st7789.BLACK, font=fontb32, fc=st7789.WHITE):
    tft.fill_rect(0, 33, tft.width(), tft.height() - 65, bg)
    center(text, bg, font, fc)


def __print(tt1, tt2, tt3, bg, tc=st7789.WHITE):
    tft.fill_rect(0, 33, tft.width(), tft.height() - 65, bg)
    middle(tt1, 70, bg, fontb32, tc)
    middle(tt2, tft.height() // 2 - fontb32.HEIGHT // 2, bg, fontb32, tc)
    middle(f' {tt3} ', tft.height() - 100, 0x2104, fontb32, st7789.WHITE)


def __sleep__():
    print('Going to sleep ... ')
    tft.fill(0)
    tft.off()
    lightsleep()


def show_info(bg=st7789.BLACK, lt='TEMP', rt='TIME', fo=font16):
    tft.fill(st7789.BLACK)

    WIFI_ICON_INDEX = 0
    WIFI_STATUS = wifi.status()

    if WIFI_STATUS is None:
        WIFI_ICON_INDEX = 4
    elif WIFI_STATUS == 'good':
        WIFI_ICON_INDEX = 3
    elif WIFI_STATUS == 'okey':
        WIFI_ICON_INDEX = 2
    elif WIFI_STATUS == 'poor':
        WIFI_ICON_INDEX = 1

    tft.bitmap(wifi_icon, 0, 0, WIFI_ICON_INDEX)
    tft.bitmap(battery_icon, 103, 0, 5)

    tft.fill_rect(0, tft.height() - 32, tft.width() // 2, 32, st7789.GREEN)
    tft.fill_rect(tft.width() // 2, tft.height() - 32, tft.width() // 2, 32, st7789.RED)

    tft.hline(0, 32, 135, st7789.WHITE)
    tft.hline(0, 240 - 32, 135, st7789.WHITE)
    tft.vline(135 // 2, 240 - 32, 32, st7789.WHITE)

    tft.text(fo, lt,
             (tft.width() // 4) - (len(lt) * fo.WIDTH) // 2,
             tft.height() - 3 * fo.HEIGHT // 2,
             st7789.BLACK, st7789.GREEN)

    tft.text(fo, rt,
             (tft.width() // 4) * 3 - (len(rt) * fo.WIDTH) // 2,
             tft.height() - 3 * fo.HEIGHT // 2,
             st7789.WHITE, st7789.RED)

    tft.fill_rect(0, 33, tft.width(), tft.height() - 65, bg)


def wake_():
    show_info(st7789.RED)

    rt = real_time.get_time()

    hour = rt[RTime.HOUR]
    minuie = rt[RTime.MINUTE]
    am_pm = rt[RTime.AM_PM]

    if hour < 10:
        hour = f'0{hour}'

    if minuie < 10:
        minuie = f'0{minuie}'

    middle(f'{hour}:{minuie}{am_pm}', 40, bg=st7789.RED)
    middle(f' {rt[RTime.DATE]}/{rt[RTime.MONTH]} ', 90, bg=st7789.BLUE)
    middle(f' {rt[RTime.YEAR]} ', 122, bg=st7789.BLUE)
    middle(f' {rt[RTime.DAY]} ', 166, bg=0x2104)


def _wake():
    show_info(0x2104)
    __print('Getting', 'Weather', 'Data', st7789.BLUE)

    temp, main_desc, hd, vs, wind, desc, fl = get_weather()
    if temp is None:
        __print('Unable', 'to get', 'Data', st7789.MAGENTA)
        return

    tft.fill_rect(0, 33, tft.width(), tft.height() - 65, 0x2104)
    left(f'TEMP:{int(temp)}C', 36, st7789.GREEN, fontb32, st7789.BLACK)
    left(f'{main_desc.upper()}', 72, st7789.GREEN, fontb32, st7789.BLACK)
    left(f'HD:{int(hd)}%', 110, st7789.RED, fontb16)
    left(f'{vs // 1000}km | {int(wind)}m/s', 130, st7789.RED, font16)
    right(f'{desc}', 150, st7789.RED, font16)
    right(f'KHULNA, BD', 170, st7789.RED, font16)
    right(f'Feels Like:{int(fl)}C', 190, st7789.RED, font16)


def __wake():
    show_info(st7789.BLUE, 'ON', 'OFF', fontb16)
    __print('Getting', 'Water', 'Status', st7789.BLUE)
    res = miio.get_status()
    gc.collect()

    if res == True:
        __print('Water', 'is', 'On', st7789.GREEN, st7789.BLACK)
    elif res == False:
        __print('Water', 'is', 'Off', st7789.RED, st7789.WHITE)
    else:
        __print('Try', 'Again', 'Err', st7789.MAGENTA, st7789.WHITE)


def ___wake():
    show_info(st7789.BLUE, 'ON', 'OFF', fontb16)
    _print('L: L')
    print('L: L')


def wake___():
    show_info(st7789.BLUE, 'ON', 'OFF', fontb16)
    _print('L: R')
    print('L: R')


def __wake__(btn, press_type):
    tft.on()
    t1.deinit()

    if not wifi.isconnected() and btn != BUTTON_RIGHT and press_type != SINGLE_PRESS:
        connect_wifi()

    if press_type == SINGLE_PRESS:
        if (btn == BUTTON_LEFT):
            _wake()
        elif (btn == BUTTON_RIGHT):
            wake_()
    elif press_type == DOUBLE_PRESS:
        __wake()
    elif press_type == LONG_PRESS:
        if (btn == BUTTON_LEFT):
            ___wake()
        elif (btn == BUTTON_RIGHT):
            wake___()

    gc.collect()
    t1.init(mode=Timer.ONE_SHOT, period=TIME_OUT, callback=lambda x: __sleep__())


buttons = Buttons()
esp32.wake_on_ext0(buttons.left)
esp32.wake_on_ext1((buttons.right,))

left_button = Pushbutton(buttons.left, True)
right_button = Pushbutton(buttons.right, True)

left_button.release_func(__wake__, (BUTTON_LEFT, SINGLE_PRESS))
right_button.release_func(__wake__, (BUTTON_RIGHT, SINGLE_PRESS))

left_button.double_func(__wake__, (BUTTON_LEFT, DOUBLE_PRESS))
right_button.double_func(__wake__, (BUTTON_RIGHT, DOUBLE_PRESS))

left_button.long_func(__wake__, (BUTTON_LEFT, LONG_PRESS))
right_button.long_func(__wake__, (BUTTON_RIGHT, LONG_PRESS))

wake_()
t1.init(mode=Timer.ONE_SHOT, period=TIME_OUT, callback=lambda x: __sleep__())

loop = asyncio.get_event_loop()
loop.run_forever()
