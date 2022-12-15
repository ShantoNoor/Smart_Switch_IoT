import esp32
import st7789
import tft_config
from machine import *
from pushbutton import *
from tft_buttons import *
import uasyncio as asyncio
import vga1_bold_16x16 as font
import vga1_bold_16x32 as fontb

import miio
from CONFIG import *
from wifi import *
from rtime import *
import gc

import wifi_icon
import battery_icon

gc.enable()

TIME_OUT = 5000

BUTTON_LEFT = 0
BUTTON_RIGHT = 1

SINGLE_PRESS = 2
DOUBLE_PRESS = 3
LONG_PRESS = 4

tft = tft_config.config(0)
tft.init()
tft.on()

t1 = Timer(0)

wifi = Wifi()
wifi.connect(tft)
gc.collect()

time.sleep(1)

real_time = RTime()
real_time.show_time()
gc.collect()


def middle(text, height, bg=st7789.BLACK, font=fontb):
    length = len(text)
    tft.text(
        font,
        text,
        (tft.width() // 2) - (length * font.WIDTH) // 2,
        height,
        st7789.WHITE,
        bg)


def left(text, height, bg=st7789.BLACK, font=fontb):
    length = len(text)
    tft.text(
        font,
        text,
        0,
        height,
        st7789.WHITE,
        bg)


def right(text, height, bg=st7789.BLACK, font=fontb):
    length = len(text)
    tft.text(
        font,
        text,
        tft.width() - length * font.WIDTH,
        height,
        st7789.WHITE,
        bg)


def center(text, bg=st7789.BLACK, font=fontb):
    length = len(text)
    tft.text(
        font,
        text,
        (tft.width() // 2) - (length * font.WIDTH) // 2,
        tft.height() // 2 - font.HEIGHT,
        st7789.WHITE,
        bg)


def _print(text, bg=st7789.BLACK):
    tft.fill(bg)
    center(text, bg)


def __sleep__():
    print('Going to sleep ... ')
    tft.fill(0)
    tft.off()
    lightsleep()


def show_info():
    tft.bitmap(wifi_icon, 0, 0, 3)
    tft.bitmap(battery_icon, 103, 0, 5)
    tft.hline(0, 32, 135, st7789.WHITE)

    tft.hline(0, 240-32, 135, st7789.WHITE)
    tft.vline(135//2, 240-32, 32, st7789.WHITE)
    left('ON', 240-32, font=font)
    right('OFF', 240 - 32, font=font)


def wake_():
    tft.fill(st7789.BLACK)

    show_info()

    rt = real_time.get_time()

    hour = rt[RTime.HOUR]
    minuie = rt[RTime.MINUTE]
    am_pm = rt[RTime.AM_PM]

    if hour < 10:
        hour = f'0{hour}'

    if minuie < 10:
        minuie = f'0{minuie}'

    middle(f'{hour}:{minuie}{am_pm}', 40)


def _wake():
    _print('S: L')
    print('S: L')


def __wake():
    _print('Status', st7789.BLUE)
    res = miio.get_status()
    gc.collect()

    if res == True:
        _print('ON', st7789.GREEN)
    elif res == False:
        _print('OFF')
    else:
        _print('Err', st7789.MAGENTA)


def ___wake():
    _print('L: L')
    print('L: L')


def wake___():
    _print('L: R')
    print('L: R')


def __wake__(btn, press_type):
    tft.on()
    t1.deinit()

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


