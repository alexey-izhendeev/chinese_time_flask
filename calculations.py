import geocoder
import ephem
import datetime


g = geocoder.ip('me')  # detects latitude and longitude with ip. Just for fast debugging here. On site it's used frontend coordinates
now_time = datetime.datetime.now()  # ordinary time at user's location, didn't work (showed server time). Now it's used JS time on site.


def solartime(observer, sun=ephem.Sun()):  # returns an astronomic time
    sun.compute(observer)
    # sidereal time == ra (right ascension) is the highest point (noon)
    hour_angle = observer.sidereal_time() - sun.ra
    return ephem.hours(hour_angle + ephem.hours('12:00')).norm  # norm for 24h



me = ephem.Observer()
me.lat = str(g.latlng[0])  # position latitude
me.long = str(g.latlng[1])  # position longitude


def positioner(lat, long):  # returns user's position and astronomic time
    iam = ephem.Observer()
    iam.lat = str(lat)  # position latitude
    iam.long = str(long)  # position longitude
    return f'Your position is {lat} latitude, {long} longitude. ' \
           f'The astronomic time of this position is {solartime(iam)}'


def find_hours(ephem_time):  # returns only hours (as a string) from ephem astronomic time
    str_hour = ''
    for i in str(ephem_time):
        if i == ':':
            break
        else:
            str_hour += i
    return str_hour


def solar_to_chinese(solartime):  # returns a description of an hour
    hour = int(find_hours(solartime))
    for i in chinese_time:
        if hour in i:
            return f'Now it is {chinese_time[i][0]} ({chinese_time[i][3]}) hour (earthly branch). \n' \
                   f'The direction of the earthly branch is {chinese_time[i][4]}. \n' \
                   f'Now it is active {chinese_time[i][2]} meridian.' \
                   f'The animal of the hour is {chinese_time[i][1]}. ' \
                   f'This chinese hour lasts {i[0]} and {i[1]} astronomic hours.'


chinese_time = {  # a description of an hour
           (23, 0): ['子', 'rat', 'gallbladder', 'zi', '0° (north)', 'water'],
           (1, 2): ['丑', 'ox', 'liver', 'chou', '30°', 'earth'],
           (3, 4): ['寅', 'tiger', 'lung', 'yin', '60°', 'tree'],
           (5, 6): ['卯', 'rabbit', 'large intestine', 'mao', '90° (east)', 'tree'],
           (7, 8): ['辰', 'dragon', 'stomach', 'chen', '120°', 'earth'],
           (9, 10): ['巳', 'snake', 'spleen', 'si', '150°', 'fire'],
           (11, 12): ['午', 'horse', 'heart', 'wu', '180° (south)', 'fire'],
           (13, 14): ['未', 'goat', 'small intestine', 'wei', '210°', 'earth'],
           (15, 16): ['申', 'monkey', 'urinary bladder', 'shen', '240°', 'metal'],
           (17, 18): ['酉', 'rooster', 'kidney', 'you', '270° (west)', 'metal'],
           (19, 20): ['戌', 'dog', 'pericardium', 'xu', '300°', 'earth'],
           (21, 22): ['亥', 'pig', 'triple burner', 'hai', '330°', 'water'],
           }

# print(solar_to_chinese(solartime(me)))
# print(positioner(g.latlng[0], g.latlng[1]))
# print(positioner(56.511079699999996, 85.0236888))
# print(solartime(me))
# print(me)