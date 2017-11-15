from urllib.parse import urlparse
import time
from multiprocessing import Process
from datetime import date, datetime

import requests
import vk
import json

A = 'vk.com'

ask = 'https://api.vk.com/method/users.get?user_id={}&v=5.52'
resolve = "https://api.vk.com/method/utils.resolveScreenName?screen_name={}&v=5.52"


def get_info_by_url(url):
    global id

    if url[-1] == "/":
        url = url[:-1]
    url = url.lower()
    print("URL: {}".format(url))
    try:
        id = int(url)
    except ValueError:
        if A in url:
            nick = url[url.index(A) + len(A) + 1:]
            if 'id' == nick[:2] and nick[2:].isdigit():
                id = nick[2:]
            else:
                js = requests.get(url=resolve.format(nick))
                js = json.loads(js.text)
                id = js["object_id"]
    js = requests.get(url=ask.format(id))
    if 'error' in js:
        return ValueError
    print("parsed id={}".format(id))
    return get_info(id)


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def get_info(id):
    requests.get(url=resolve.format(1))
    # js = vk_api.users.get(user_ids=[id],
    #                       fields="bdate, city,counters,country, followers_count, has_mobile, has_photo, personal,relation,schools,sex,trending,universities")

    counters_keys = ["photos", "videos", "audios", "albums", "notes", "friends", "groups", "user_videos",
                     "followers", "pages"]
    simple_keys = ["uid", "city", "country", "has_photo", "has_mobile", "trending", "followers_count", "sex",
                   "relation", "universities", "schools", "political", "people_main", "life_main",
                   "smoking", "alcohol", "langs", "bdate", "wall_posts"]

    # init
    dict_js = {}

    for ke in counters_keys:
        dict_js[ke] = -1
    for ke in simple_keys:
        dict_js[ke] = -1

    # dict_js.update(js[0])
    dict_js["uid"] = id

    if "counters" in dict_js:
        for ke in counters_keys:
            if ke in dict_js["counters"]:
                dict_js[ke] = dict_js["counters"][ke]
        dict_js.pop('counters')

    if dict_js['universities'] != -1:
        dict_js["universities"] = len(dict_js["universities"])
    if dict_js['schools'] != -1:
        dict_js["schools"] = len(dict_js["schools"])
    if 'personal' in dict_js:
        if 'langs' in dict_js['personal']:
            dict_js["langs"] = len(dict_js['personal']["langs"])
        if 'people_main' in dict_js['personal']:
            dict_js["people_main"] = dict_js['personal']["people_main"]
        if 'life_main' in dict_js['personal']:
            dict_js["life_main"] = dict_js['personal']["life_main"]
        if 'smoking' in dict_js['personal']:
            dict_js["smoking"] = dict_js['personal']["smoking"]
        if 'alcohol' in dict_js['personal']:
            dict_js["alcohol"] = dict_js['personal']["alcohol"]
        if 'political' in dict_js['personal']:
            dict_js["political"] = dict_js['personal']["political"]
        dict_js.pop('personal')

    if 'relation_partner' in dict_js:
        dict_js.pop('relation_partner')

    # dict_js["position"] = position

    # print(dict_js)

    # js = vk_api.wall.get(owner_id=id, count=1)
    # dict_js['wall_posts'] = js[0]

    i = dict_js["bdate"]
    ages = []

    ag = 0
    if str(i) != "-1":
        l = i.split(".")
        if len(l) == 3:
            d = datetime.strptime(i, "%d.%m.%Y").date()
            ag = calculate_age(d)
        else:
            ag = -1

    dict_js["age"] = ag

    return dict_js
