import uasyncio as asyncio
import urequests as requests

from CONFIG import *


async def get_weather_data():
    res = None
    try:
        res = requests.get(TEMP_URL).json()
    except asyncio.TimeoutError as exc:
        print('Unable to get Weather Data [TIMEOUT] ... ')
        # print(errno.errorcode[exc.errno])
        return None
    except OSError as exc:
        print('Unable to get Weather Data ... ')
        # print(errno.errorcode[exc.errno])
        return None

    return res


async def get_weather():
    res = None
    try:
        res = await asyncio.wait_for(get_weather_data(), 5)
    except asyncio.TimeoutError as exc:
        print('Unable to get Weather Info [TIMEOUT] ... ')
        # print(errno.errorcode[exc.errno])
        return None, None, None, None, None, None, None
    except OSError as exc:
        print('Unable to get Weather Info ... ')
        # print(errno.errorcode[exc.errno])
        return None, None, None, None, None, None, None

    if res == None:
        return None, None, None, None, None, None, None

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

    return temp, main_desc, hd, vs, wind, desc, fl
