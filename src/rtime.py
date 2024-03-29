import gc
import time

from machine import RTC

import ntp_time


class RTime:
    UTC_OFFSET = 6

    YEAR = 2
    MONTH = 1
    DATE = 0
    HOUR = 3
    MINUTE = 4
    SECOND = 5
    DAY = 7
    AM_PM = 6

    def __init__(self):
        self.rtc = RTC()
        self.TIME_SYNCED = False

    async def init(self):
        if not self.TIME_SYNCED:
            gc.collect()

            tm = await ntp_time.time(RTime.UTC_OFFSET)
            if tm == 0:
                print('Unable to Set Time from Online ... ')
            else:
                real_time = time.localtime(tm)
                year = real_time[0]
                month = real_time[1]
                date = real_time[2]
                hour = real_time[3]
                minute = real_time[4]
                second = real_time[5]

                self.rtc.init((year, month, date, 0, hour, minute, second, 0))
                self.TIME_SYNCED = True

    def get_time(self):
        real_time = self.rtc.datetime()

        year = real_time[0]
        month = real_time[1]
        date = real_time[2]
        day = real_time[3]
        hour = real_time[4]
        minute = real_time[5]
        second = real_time[6]
        am_pm = 'am'

        if hour > 11:
            am_pm = 'pm'
            if hour > 12:
                hour -= 12

        if day == 0:
            day = 'Mon'
        elif day == 1:
            day = 'Tue'
        elif day == 2:
            day = 'Wed'
        elif day == 3:
            day = 'Thu'
        elif day == 4:
            day = 'Fri'
        elif day == 5:
            day = 'Sat'
        elif day == 6:
            day = 'Sun'

        return date, month, year, hour, minute, second, am_pm, day

    def is_time_synced(self):
        return self.TIME_SYNCED

    def show_time(self):
        t = self.get_time()
        print(
            f'{t[RTime.HOUR]}:{t[RTime.MINUTE]}:{t[RTime.SECOND]}-{t[RTime.AM_PM]} | {t[RTime.DAY]}-{t[RTime.DATE]}-{t[RTime.MONTH]}-{t[RTime.YEAR]}')
