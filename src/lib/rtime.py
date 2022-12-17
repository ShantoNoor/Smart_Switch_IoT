import time, ntptime
from machine import RTC
import errno


class RTime:
    UTC_OFFSET = 6 * 60 * 60

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

        try:
            ntptime.settime()
        except OSError as exc:
            print('Unable to Set Time from Online ... ')
            print(errno.errorcode[exc.errno])

        real_time = time.localtime(time.time() + RTime.UTC_OFFSET)
        year = real_time[0]
        month = real_time[1]
        date = real_time[2]
        hour = real_time[3]
        minute = real_time[4]
        second = real_time[5]

        self.rtc.init((year, month, date, 0, hour, minute, second, 0))

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

        if hour > 12:
            hour -= 12
            am_pm = 'pm'
        elif hour == 0:
            hour = 12

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

        return (date, month, year, hour, minute, second, am_pm, day)

    def show_time(self):
        t = self.get_time()
        print(
            f'{t[RTime.HOUR]}:{t[RTime.MINUTE]}:{t[RTime.SECOND]}-{t[RTime.AM_PM]} | {t[RTime.DAY]}-{t[RTime.DATE]}-{t[RTime.MONTH]}-{t[RTime.YEAR]}')

