import esp32
import st7789
import vga1_bold_16x16 as fontb16
import vga1_bold_16x32 as fontb32
import vga2_8x16 as font16
from machine import *

import battery_icon
import miio
import watchdog
import wifi_icon
from battery import *
from boot import *
from pushbutton import *
from rtime import *
from tft_buttons import *
from weather import *

TIME_OUT = 10
START_TIME = 0

DEEPSLEEP_START_TIME = 10 * 60  # sec

WATER_ON_TIME = 11 * 60  # sec
IS_WATER_ON = False
WATER_OFF_TIME = 0

MAX_TRY = 15
MAX_SLEEP = 0.25

BUTTON_LEFT = 0
BUTTON_RIGHT = 1

SINGLE_PRESS = 2
DOUBLE_PRESS = 3
LONG_PRESS = 4

wdt = watchdog.WDT(0, 20)  # 20 sec
wdt.deinit()


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


def _print(text, bg=st7789.BLACK, font=fontb32, fc=st7789.WHITE):
    tft.fill_rect(0, 33, tft.width(), tft.height() - 65, bg)
    center(text, bg, font, fc)


def __print(tt1, tt2, tt3, bg, tc=st7789.WHITE):
    tft.fill_rect(0, 33, tft.width(), tft.height() - 65, bg)
    middle(tt1, 70, bg, fontb32, tc)
    middle(tt2, tft.height() // 2 - fontb32.HEIGHT // 2, bg, fontb32, tc)
    middle(tt3, tft.height() - 100, 0x2104, fontb32, st7789.WHITE)


def center(text, bg=st7789.BLACK, font=fontb32, fc=st7789.WHITE):
    length = len(text)
    tft.text(
        font,
        text,
        (tft.width() // 2) - (length * font.WIDTH) // 2,
        tft.height() // 2 - font.HEIGHT // 2,
        fc,
        bg)


def save_file(text):
    try:
        with open('t.txt', 'w') as f:
            f.write(text)
    except OSError as exc:
        __print('Unable', 'Save', 'File', st7789.MAGENTA)
        print('Unable Save File ... ')
        # print(errno.errorcode[exc.errno])


def read_file():
    x = '0'
    try:
        with open('t.txt', 'r') as f:
            x = f.read()
    except OSError as exc:
        __print('Unable', 'Read', 'File', st7789.MAGENTA)
        print('Unable Read File ... ')
        # print(errno.errorcode[exc.errno])

    return x


def __wifi__():
    wdt.feed()
    if not wifi.is_connected():
        __print('Conn-ing', 'with', 'FreeNet', st7789.BLACK)
        connect_wifi()
        wdt.feed()
        if not wifi.is_connected():
            __print('Unable', 'Con-with', 'FreeNet', st7789.BLACK)
            return False

    wdt.feed()
    time.sleep(1)
    return True


def __alarm__():
    global START_TIME
    START_TIME = float('inf')

    wdt.init()

    tft.on()
    print('__Alarm__')

    show_info(st7789.BLUE, 'ON', 'OFF', fontb16)

    end_time = time.time() + 5
    wdt.feed()
    while True and time.time() < end_time:
        __print('Time', 'is', 'Over', st7789.GREEN, st7789.BLACK)
        time.sleep(0.2)
        __print('Time', 'is', 'Over', st7789.RED, st7789.WHITE)
        time.sleep(0.2)
        __print('Time', 'is', 'Over', st7789.BLUE, st7789.WHITE)
        time.sleep(0.2)
        __print('Time', 'is', 'Over', st7789.YELLOW, st7789.BLACK)
        time.sleep(0.2)
        __print('Time', 'is', 'Over', st7789.MAGENTA, st7789.WHITE)
        time.sleep(0.2)

    wdt.feed()
    wake___()
    START_TIME = time.time()
    wdt.feed()


def update_battery_and_wifi():
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

    BATTERY_ICON_INDEX = 0
    volt = get_volt()
    bl_str = ''
    if volt >= 4.4:
        BATTERY_ICON_INDEX = 5
        bl_str = 'Chg'
    else:
        bl = get_charge_level(volt)
        if bl > 80:
            BATTERY_ICON_INDEX = 4
        elif bl > 60:
            BATTERY_ICON_INDEX = 3
        elif bl > 40:
            BATTERY_ICON_INDEX = 2
        elif bl > 20:
            BATTERY_ICON_INDEX = 1
        else:
            BATTERY_ICON_INDEX = 0

        bl_str = str(f'{bl}%')

    # for removing previous battery level
    tft.text(fontb16, '    ', tft.width() - len(bl_str) * fontb16.WIDTH - 34, 8, st7789.WHITE, st7789.BLACK)
    tft.text(fontb16, bl_str, tft.width() - len(bl_str) * fontb16.WIDTH - 34, 8, st7789.WHITE, st7789.BLACK)
    tft.bitmap(wifi_icon, 0, 0, WIFI_ICON_INDEX)
    tft.bitmap(battery_icon, 103, 0, BATTERY_ICON_INDEX)


def show_info(bg=st7789.BLACK, lt='TEMP', rt='TIME', fo=font16):
    tft.fill(st7789.BLACK)

    update_battery_and_wifi()

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


async def wake_():
    global IS_WATER_ON

    if not IS_WATER_ON and not real_time.is_time_synced():
        if __wifi__():
            wdt.feed()

            show_info(st7789.BLUE)
            __print('Syncing', 'Real', 'Time', st7789.BLUE)

            wdt.feed()
            await real_time.init()

    if real_time.is_time_synced():
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
    else:
        show_info(st7789.MAGENTA)
        __print('Time', 'Not', 'Synced', st7789.MAGENTA)


async def _wake():
    if __wifi__():
        wdt.feed()

        show_info(st7789.BLUE)  # 0x2104
        __print('Getting', 'Weather', 'Data', st7789.BLUE)

        gc.collect()
        try:
            temp, main_desc, hd, vs, wind, desc, fl = await get_weather()
        except OSError as exc:
            __print('Unable', 'to get', 'Data', st7789.MAGENTA)
            # print(errno.errorcode[exc.errno])
            return

        if temp is None:
            __print('Unable', 'to get', 'Data', st7789.MAGENTA)
            return

        tft.fill_rect(0, 33, tft.width(), tft.height() - 65, st7789.GREEN)
        left(f'TEMP:{int(temp)}C', 36, st7789.GREEN, fontb32, st7789.BLACK)
        left(f'{main_desc.upper()}', 72, st7789.GREEN, fontb32, st7789.BLACK)
        left(f'HD:{int(hd)}%', 110, st7789.RED, fontb16)
        left(f'{vs // 1000}km | {int(wind)}m/s', 130, st7789.RED, font16)
        right(f'{desc}', 150, st7789.RED, font16)
        right(f'KHULNA, BD', 170, st7789.RED, font16)
        right(f'Feels Like:{int(fl)}C', 190, st7789.RED, font16)


def __wake():
    global IS_WATER_ON
    global WATER_OFF_TIME
    global WATER_ON_TIME
    global MAX_TRY
    global MAX_SLEEP

    if __wifi__():
        wdt.feed()

        show_info(st7789.BLUE, 'ON', 'OFF', fontb16)
        __print('Getting', 'Water', 'Status', st7789.BLUE)

        try_number = 0
        res = None

        while res is None and try_number < MAX_TRY:
            res = miio.get_status()
            try_number += 1
            wdt.feed()
            time.sleep(MAX_SLEEP)

        gc.collect()

        if res == True:
            __print('Water', 'is', 'On', st7789.GREEN, st7789.BLACK)
        elif res == False:
            __print('Water', 'is', 'Off', st7789.RED, st7789.WHITE)
        else:
            __print('Try', 'Again', 'Err', st7789.MAGENTA, st7789.WHITE)

        if IS_WATER_ON and res != False:
            tft.rect(10, 180, 113, 10, st7789.WHITE)
            tft.fill_rect(11, 181, 113 - int((((WATER_OFF_TIME - time.time()) / WATER_ON_TIME) * 102) + 11), 8,
                          st7789.BLACK)
        elif IS_WATER_ON and res == False:
            IS_WATER_ON = False
            WATER_OFF_TIME = 0
            save_file('0')


def ___wake():
    global IS_WATER_ON
    global WATER_ON_TIME
    global WATER_OFF_TIME
    global MAX_TRY
    global MAX_SLEEP

    if __wifi__():
        wdt.feed()

        show_info(st7789.BLUE, 'ON', 'OFF', fontb16)
        print('Turning on Water ... ')
        __print('Turning', 'on', 'Water', st7789.BLUE, st7789.WHITE)

        try_number = 0
        res = None
        while res is None and try_number < MAX_TRY:
            res = miio.set_power(True)
            try_number += 1
            wdt.feed()
            time.sleep(MAX_SLEEP)

        if res:
            __print('Water', 'is', 'On', st7789.GREEN, st7789.BLACK)
        else:
            __print('Try', 'Again', 'Err', st7789.MAGENTA, st7789.WHITE)
            return

        IS_WATER_ON = True
        WATER_OFF_TIME = time.time() + WATER_ON_TIME
        save_file(str(WATER_OFF_TIME))


def wake___():
    global IS_WATER_ON
    global WATER_OFF_TIME
    global MAX_SLEEP
    global MAX_TRY

    if __wifi__():
        wdt.feed()

        show_info(st7789.BLUE, 'ON', 'OFF', fontb16)
        print('Turning off Water ... ')
        __print('Turning', 'off', 'Water', st7789.BLUE, st7789.WHITE)

        try_number = 0
        res = None
        while res is None and try_number < MAX_TRY:
            res = miio.set_power()
            try_number += 1
            wdt.feed()
            time.sleep(MAX_SLEEP)

        if res:
            __print('Water', 'is', 'Off', st7789.RED, st7789.WHITE)
        else:
            __print('Try', 'Again', 'Err', st7789.MAGENTA, st7789.WHITE)
            return

        WATER_OFF_TIME = 0
        IS_WATER_ON = False
        save_file('0')


async def __wake__(btn, press_type):
    global START_TIME
    global BUTTON_LEFT
    global BUTTON_RIGHT
    global SINGLE_PRESS
    global DOUBLE_PRESS
    global LONG_PRESS

    START_TIME = float('inf')
    tft.on()

    wdt.init()
    wdt.feed()

    if press_type == SINGLE_PRESS:
        if btn == BUTTON_LEFT:
            await _wake()
        elif btn == BUTTON_RIGHT:
            await wake_()
    elif press_type == DOUBLE_PRESS:
        __wake()
    elif press_type == LONG_PRESS:
        if btn == BUTTON_LEFT:
            ___wake()
        elif btn == BUTTON_RIGHT:
            wake___()

    wdt.feed()
    gc.collect()
    START_TIME = time.time()


async def main():
    global WATER_OFF_TIME
    global IS_WATER_ON
    global WATER_ON_TIME
    global TIME_OUT
    global START_TIME
    global DEEPSLEEP_START_TIME
    global BUTTON_LEFT
    global BUTTON_RIGHT
    global SINGLE_PRESS
    global DOUBLE_PRESS
    global LONG_PRESS

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

    WATER_OFF_TIME = int(read_file())
    if WATER_OFF_TIME != 0:
        IS_WATER_ON = True

    tft.init()
    tft.fill(st7789.BLACK)
    gc.collect()

    wdt.init()
    await wake_()
    wdt.feed()

    START_TIME = time.time()
    while True:
        update_battery_and_wifi()

        if time.time() - START_TIME > TIME_OUT:
            print('Going to sleep ... ')

            wdt.deinit()
            tft.off()

            if not IS_WATER_ON:
                st = time.time()
                lightsleep(int(DEEPSLEEP_START_TIME * 1000))
                if time.time() - st >= DEEPSLEEP_START_TIME:
                    print('Going to deep sleep ... ')
                    ADC_EN.value(0)
                    tft.sleep_mode(True)
                    deepsleep(1 << 30)
            else:
                st = int(WATER_OFF_TIME - time.time()) * 1000
                lightsleep(int(st))
                if WATER_OFF_TIME - time.time() <= 0:
                    __alarm__()

            START_TIME = time.time()

        await asyncio.sleep_ms(1000)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
