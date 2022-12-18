import urequests as requests
from CONFIG import *
import errno


def get_weather():
    try:
        res = requests.get(TEMP_URL).json()
        temp = res.get('main').get('temp')  # C
        # tmin = res.get('main').get('temp_min')  # C
        # tmax = res.get('main').get('temp_max')  # C
        fl = res.get('main').get('feels_like')  # C
        hd = res.get('main').get('humidity')  # %
        # ps = res.get('main').get('pressure')  # hPa
        wind = res.get('wind').get('speed')  # m/s NNW
        desc = res.get('weather')[0].get('description')
        main_desc = res.get('weather')[0].get('main')
        vs = res.get('visibility')

    except OSError as exc:
        print('Unable to get Weather Data ... ')
        print(errno.errorcode[exc.errno])
        return None, None, None, None, None, None, None

    return temp, main_desc, hd, vs, wind, desc, fl
