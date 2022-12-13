import esp32
import st7789
import tft_config
from machine import *
from pushbutton import *
from tft_buttons import *
import uasyncio as asyncio
import vga1_bold_16x16 as font

TIME_OUT = 5000
BUTTON_LEFT = 0
BUTTON_RIGHT = 1

tft = tft_config.config(0)
tft.init()
t1 = Timer(0)

def center(text):
    length = len(text)
    tft.text(
        font,
        text,
        (tft.width() // 2) - (length * font.WIDTH) // 2,
        tft.height() // 2 - font.HEIGHT,
        st7789.WHITE,
        st7789.RED)
    
def _print(text):
    tft.fill(st7789.RED)
    center(text)

def __sleep__():
    print('Going to sleep ... ')
    tft.off()
    pressed = False
    lightsleep()

def __wake__():
    tft.on()
    t1.deinit()
    t1.init(mode=Timer.ONE_SHOT, period=TIME_OUT, callback=lambda x: __sleep__())
    
async def _wake(btn):
    __wake__()
    if(btn == BUTTON_LEFT):
        _print('S: L')
        print('S: L')
        
    if(btn == BUTTON_RIGHT):
        _print('S: R')
        print('S: R')
        
async def __wake(btn):
    __wake__()
    if(btn == BUTTON_LEFT):
        _print('D: L')
        print('D: L')
        
    if(btn == BUTTON_RIGHT):
        _print('D: R')
        print('D: R')
    
async def ___wake(btn):
    __wake__()
    if(btn == BUTTON_LEFT):
        _print('L: L')
        print('L: L')
        
    if(btn == BUTTON_RIGHT):
        _print('L: R')
        print('L: R')
    
buttons = Buttons()
esp32.wake_on_ext0(buttons.left)
esp32.wake_on_ext1((buttons.right,))

left_button = Pushbutton(buttons.left, True)
right_button = Pushbutton(buttons.right, True)

left_button.release_func(_wake, (BUTTON_LEFT, ))
right_button.release_func(_wake, (BUTTON_RIGHT,))

left_button.double_func(__wake, (BUTTON_LEFT,))
right_button.double_func(__wake, (BUTTON_RIGHT,))

left_button.long_func(___wake, (BUTTON_LEFT,))
right_button.long_func(___wake, (BUTTON_RIGHT,))

loop = asyncio.get_event_loop()
loop.run_forever()

t1.init(mode=Timer.ONE_SHOT, period=TIME_OUT, callback=lambda x: __sleep__())
_print('RUNNING')
