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

TIME_OUT = 5000
BUTTON_LEFT = 0
BUTTON_RIGHT = 1

tft = tft_config.config(0)
tft.init()
t1 = Timer(0)

wifi = Wifi()
wifi.connect()

# real_time = RTime()
# real_time.show_time()

print('here')

def center(text, bg = st7789.RED):
    length = len(text)
    tft.text(
        font,
        text,
        (tft.width() // 2) - (length * font.WIDTH) // 2,
        tft.height() // 2 - font.HEIGHT,
        st7789.WHITE,
        bg)

print('here1')

def _print(text, bg = st7789.RED):
    tft.fill(bg)
    center(text, bg)

print('here2')

def __sleep__():
    print('Going to sleep ... ')
    tft.off()
    lightsleep()

print('here3')

def __wake__():
    tft.on()
    t1.deinit()
    t1.init(mode=Timer.ONE_SHOT, period=TIME_OUT, callback=lambda x: __sleep__())

print('here4')

def _wake(btn):
    __wake__()
    if(btn == BUTTON_LEFT):
        _print('S: L')
        print('S: L')
        
    elif(btn == BUTTON_RIGHT):
        _print('S: R')
        print('S: R')

print('here5')

def __wake(btn):
    gc.collect()

    tft.on()
    t1.deinit()

    res = miio.get_status()

    if res == True:
        _print('ON', st7789.GREEN)
    elif res == False:
        _print('OFF')
    else:
        _print('Err', st7789.YELLOW)

    t1.init(mode=Timer.ONE_SHOT, period=TIME_OUT, callback=lambda x: __sleep__())

print('here6')

def ___wake(btn):
    __wake__()
    if(btn == BUTTON_LEFT):
        _print('L: L')
        print('L: L')
        
    elif(btn == BUTTON_RIGHT):
        _print('L: R')
        print('L: R')

print('here7')

buttons = Buttons()
esp32.wake_on_ext0(buttons.left)
esp32.wake_on_ext1((buttons.right,))
print('here8')

left_button = Pushbutton(buttons.left, True)
right_button = Pushbutton(buttons.right, True)
print('here9')

left_button.release_func(_wake, (BUTTON_LEFT, ))
right_button.release_func(_wake, (BUTTON_RIGHT,))
print('here10')

left_button.double_func(__wake, (BUTTON_LEFT,))
right_button.double_func(__wake, (BUTTON_RIGHT,))
print('here11')

left_button.long_func(___wake, (BUTTON_LEFT,))
right_button.long_func(___wake, (BUTTON_RIGHT,))
print('here12')

t1.init(mode=Timer.ONE_SHOT, period=TIME_OUT, callback=lambda x: __sleep__())
_print('RUNNING')
print('here13')

loop = asyncio.get_event_loop()
loop.run_forever()
print('here14')

