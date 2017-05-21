# coding=utf-8
# __author__ = 'Mio'
from os.path import join
from os import remove, listdir
from time import time
from datetime import datetime

import requests

WALLPAPER_FOLDER = "/Users/mio/Pictures/wallpaper/unsplash"
REMAIN_PICS = 50


def remain_pics(num=50):
    exists_pictures = listdir(WALLPAPER_FOLDER)
    exists_pics_count = len(exists_pictures)
    if exists_pics_count >= num:
        # delete oldest pics
        need_delete = exists_pics_count - num
        for pic in exists_pictures[:need_delete]:
            remove(join(WALLPAPER_FOLDER, pic))

def mprint(s):
    print("{}: {}".format(datetime.now(), s))


def get_new(folder_path):
    url = "https://source.unsplash.com/random/2560x1600"
    # request.urlretrieve(url, filename="{}.jpeg".format(join(folder_path, str(int(time()) * 6))))
    file_path = "{}.jpeg".format(join(folder_path, str(int(time()))))
    res = requests.get(url, allow_redirects=False)
    mprint(res.headers['Location'])
    proxies = {
        "http": "http://127.0.0.1:1087",
        "https": "http://127.0.0.1:1087",
    }
    rst = requests.get(res.headers['Location'], proxies=proxies)
    with open(file_path, "wb") as f:
        for chunk in rst:
            f.write(chunk)
    mprint('done')


if __name__ == '__main__':
    remain_pics(REMAIN_PICS)
    get_new(WALLPAPER_FOLDER)
