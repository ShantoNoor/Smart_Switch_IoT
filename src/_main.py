import esp32
import st7789
import tft_config
from machine import *
from pushbutton import *
from tft_buttons import *
import uasyncio as asyncio
import vga1_bold_16x16 as font

import miio
from CONFIG import *
from wifi import *
from rtime import *
import gc

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

# real_time = RTime()
# real_time.show_time()
# gc.collect()

def center(text, bg = st7789.RED):
    length = len(text)
    tft.text(
        font,
        text,
        (tft.width() // 2) - (length * font.WIDTH) // 2,
        tft.height() // 2 - font.HEIGHT,
        st7789.WHITE,
        bg)


def _print(text, bg = st7789.RED):
    tft.fill(bg)
    center(text, bg)


def __sleep__():
    print('Going to sleep ... ')
    tft.fill(0)
    tft.off()
    lightsleep()


def _wake(btn):
    if (btn == BUTTON_LEFT):
        _print('S: L')
        print('S: L')

    elif (btn == BUTTON_RIGHT):
        _print('S: R')
        print('S: R')


def __wake(btn):
    _print('Status', st7789.BLUE)
    res = miio.get_status()
    gc.collect()

    if res == True:
        _print('ON', st7789.GREEN)
    elif res == False:
        _print('OFF')
    else:
        _print('Err', st7789.MAGENTA)


def ___wake(btn):
    if (btn == BUTTON_LEFT):
        _print('L: L')
        print('L: L')

    elif (btn == BUTTON_RIGHT):
        _print('L: R')
        print('L: R')


def __wake__(btn, press_type):
    tft.on()
    t1.deinit()

    if press_type == SINGLE_PRESS:
        _wake(btn)
    elif press_type == DOUBLE_PRESS:
        __wake(btn)
        gc.collect()
    elif press_type == LONG_PRESS:
        ___wake(btn)

    t1.init(mode=Timer.ONE_SHOT, period=TIME_OUT, callback=lambda x: __sleep__())


buttons = Buttons()
esp32.wake_on_ext0(buttons.left)
esp32.wake_on_ext1((buttons.right,))

left_button = Pushbutton(buttons.left, True)
right_button = Pushbutton(buttons.right, True)

left_button.release_func(__wake__, (BUTTON_LEFT, SINGLE_PRESS))
right_button.release_func(__wake__, (BUTTON_RIGHT,SINGLE_PRESS))

left_button.double_func(__wake__, (BUTTON_LEFT, DOUBLE_PRESS))
right_button.double_func(__wake__, (BUTTON_RIGHT, DOUBLE_PRESS))

left_button.long_func(__wake__, (BUTTON_LEFT, LONG_PRESS))
right_button.long_func(__wake__, (BUTTON_RIGHT, LONG_PRESS))

_wake(BUTTON_LEFT)
t1.init(mode=Timer.ONE_SHOT, period=TIME_OUT, callback=lambda x: __sleep__())

loop = asyncio.get_event_loop()
loop.run_forever()

