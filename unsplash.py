# coding=utf-8
# __author__ = 'Mio'

import json
from time import time
from datetime import datetime
from os.path import join, abspath, exists, expanduser
from os import remove, listdir, makedirs

import requests

class Runner(object):
    def __init__(self, config_path="./config.json"):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        """
        config:
        {
            "lable": "com.my_unsplash.wallpaper.downloader",
            "wallpapers_folder": "~/Pictures/unsplash",
            "remain_picture_number": 50,
            "download_interval": 100,
            "logs_path": {
                "stdout": "",
                "stderr": ""
            },
            "proxies": {
                "http": "socks5://127.0.0.1:1081",
                "https": "socks5://127.0.0.1:1081"
            }
        }
        """
        try:
            with open(self.config_path) as f:
                config = json.load(f)
        except Exception as e:
            self.mprint("load config failed")
            self.mprint(e, level="error")
            raise e
        else:
            return config

    @property
    def wallpapers_folder(self):
        if "~" in self.config['wallpapers_folder']:
            self.config['wallpapers_folder'] = expanduser(self.config['wallpapers_folder'])
        return abspath(self.config['wallpapers_folder'])



    def remain_pics(self, num=50):
        exists_pictures = listdir(self.wallpapers_folder)
        exists_pics_count = len(exists_pictures)
        if exists_pics_count >= num:
            # delete oldest pics
            need_delete = exists_pics_count - num
            for pic in exists_pictures[:need_delete]:
                remove(join(self.wallpapers_folder, pic))

    def mprint(self, s):
        print("{}: {}".format(datetime.now(), s))

    def find_file_name(url):
        return "{}.jpeg".format(int(time()))

    def get_new(self):
        res = requests.get(self.config['download_url'], allow_redirects=False)
        file_name = self.find_file_name()
        self.mprint("downloading {}".format(res.headers['Location']))

        rst = requests.get(res.headers['Location'], proxies=self.config['proxies'])
        file_path = join(self.wallpapers_folder, file_name)
        # check folder
        if not exists(self.wallpapers_folder):
            makedirs(self.wallpapers_folder)
        with open(abspath(file_path), "wb") as f:
            for chunk in rst:
                f.write(chunk)
        self.mprint('saved {}'.format(file_path))
        self.mprint('done')

    def do_run(self):
        self.get_new()
        self.remain_pics()


if __name__ == '__main__':
    # remain_pics(REMAIN_PICS)
    # get_new(WALLPAPER_FOLDER)
    r = Runner()
    r.do_run()
