#!/usr/bin/python
# coding=utf8
from __future__ import print_function

import os
import json
import logging
from shutil import copy
from plistlib import writePlist


class Installer(object):
    def __init__(self, config_path):
        self.config_path = config_path
        self.label = None
        self.plist_file_name = None

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
            self.label = config['label']
            self.plist_file_name = config['label'] + ".plist"
            return config

    def mprint(self, log, level="info"):
        print("\n", "*" * 10, log, "*" * 10, "\n")
        if level == "info":
            logging.info(log)
        elif level == "error":
            logging.error(log)
        else:
            logging.warn(log)

    def install_pip(self):
        os.system("python ./get-pip.py")
        os.system("which pip")

    def install_requests(self):
        os.system("pip install -U 'requests[socks]'")

    def generate_plist(self):
        out_path = os.path.abspath(self.config['logs_path']['stdout'])
        err_path = os.path.abspath(self.config['logs_path']['stderr'])
        for p in (out_path, err_path):
            if not os.path.exists(p):
                os.makedirs(p)
        plist_content = {
            'Label': self.label,
            'Program': os.path.abspath('./unsplash.py'),
            'StandardOutPath': out_path,
            'StandardErrorPath': err_path,
            'StartInterval': self.config['download_interval']
        }
        writePlist(plist_content, self.plist_file_name)
        copy(self.plist_file_name, os.path.expanduser("~/Library/LaunchAgents/"))

    def start_lanchctl(self):
        final_plist_path = os.path.expanduser("~/Library/LaunchAgents/{}".format(self.plist_file_name))
        os.system("launchctl unload {}".format(final_plist_path))
        os.system("launchctl load {}".format(final_plist_path))
        os.system("launchctl start {}".format(final_plist_path))
        os.system("launchctl list|grep {}".format(self.config['label']))

    def do_install(self):
        self.install_pip()
        self.install_requests()
        self.generate_plist()
        self.start_lanchctl()


if __name__ == '__main__':
    # config_path from cmd args
    _config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    i = Installer(_config_path)
    i.do_install()
