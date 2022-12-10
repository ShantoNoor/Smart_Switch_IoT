import time, ntptime

class mTime:
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
        ntptime.settime()
    
    def get_time(self):
        temp_time = time.localtime(time.time() + Time.UTC_OFFSET)
        
        year = temp_time[0]
        month = temp_time[1]
        date = temp_time[2]
        hour = temp_time[3]
        minute = temp_time[4]
        second = temp_time[5]
        day = temp_time[6]
        am_pm = 'am'
        
        if hour > 12:
            hour -= 12
            am_pm = 'pm'
        
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
        print(f'{t[Time.HOUR]}:{t[Time.MINUTE]}:{t[Time.SECOND]}-{t[Time.AM_PM]} | {t[Time.DAY]}-{t[Time.DATE]}-{t[Time.MONTH]}-{t[Time.YEAR]}')
    