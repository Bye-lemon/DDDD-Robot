#!/usr/bin/env python2
# -*- coding: utf-8-*-

import json
from . import config
import base64
import requests
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import hashlib
import threading
import trollius
import subprocess
import os
import time
import yaml
# import markdown
import random


class GetConfigHandler(tornado.web.RequestHandler):

    def get(self):
        res = {'code': 0, 'message': 'ok', 'config': config.getText(), 'sensitivity': config.get('sensitivity', 0.5)}
        self.write(json.dumps(res))
        self.finish()


class ConfigHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('config.html', sensitivity=config.get()["snowboy"]["sensitivity"])

    def post(self):
        configStr = self.get_argument('config')
        try:
            yaml.load(configStr)
            config.dump(configStr)
            res = {'code': 0, 'message': 'ok'}
            self.write(json.dumps(res))
        except:
            res = {'code': 1, 'message': 'YAML解析失败，请检查内容'}
            self.write(json.dumps(res))
        self.finish()


settings = {
    "cookie_secret": "foobar",
    "template_path": "dingdang/client/templates",
    "static_path": "dingdang/client/static",
    "debug": False
}

application = tornado.web.Application([
    (r"/config", ConfigHandler),
    (r"/getconfig", GetConfigHandler),
], **settings)


def start_server():
    try:
        trollius.set_event_loop(trollius.new_event_loop())
        application.listen(5000)
        tornado.ioloop.IOLoop.instance().start()
    except Exception as e:
        print('服务器启动失败: {}'.format(e))


def run():
    t = threading.Thread(target=lambda: start_server())
    t.start()
