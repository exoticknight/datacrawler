# -*- coding: utf-8 -*-

# latitude and longtitude

from utils.database_config import CONFIG

import MySQLdb
import urllib
import requests

con = MySQLdb.connect(**CONFIG)
items = []

def get_latandlon(x):
    print(x[1]),
    payload = {
        'address': u'杭州' + x[1],
        'language': 'zh-cn'
    }
    r = requests.get(u'http://ditu.google.cn/maps/api/geocode/json', params=payload, timeout=5)
    print(r.status_code)
    print(url)
    res = r.json()
    if res['status'] == 'OK':
        datum = res['results'][0]
        return (True, {
            'id': x[0],
            'lat': datum['geometry']['location']['lat'],
            'lng': datum['geometry']['location']['lng'],
            'district': datum['address_components'][1]['long_name'],
            'city': datum['address_components'][2]['long_name'],
            'province': datum['address_components'][3]['long_name'],
            })
    else:
        return (False,)

# lookup scenes
with con:
    c = con.cursor()
    c.execute("""SELECT * FROM `scenelist` WHERE `lat` IS NULL""")
    for row in c.fetchall():
        items.append((row[0], row[1]))  # name is in column 2


print(items)
# request lat & lng
# values = [(site[1]['lat'], site[1]['lng'], site[1]['district'], site[1]['provice'], site[1]['id']) for site in [get_latandlon(x) for x in items] if site[0]]


# update scenes
# with con:
#     c = con.cursor()
#     c.executemany(
#     """UPDATE `scenelist` SET `lat`=%s,`lng`=%s,`district`=%s,'provice'=%s WHERE `id`=%s""",
#     values)