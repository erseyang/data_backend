#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: eric.yang
@contact: erseyang@gmail.com
@site: http://www.lizit.net
@software: PyCharm
@file: __init__.py.py
@time: 17/2/12 下午2:32
"""
import tornado
from tornado.web import url
from bob.core.helpers import setting_from_object
from bob.core.route import urls
import config


class Application(tornado.web.Application):
    def __init__(self):
        settings = setting_from_object(config)
        handlers = urls
        settings.update(dict(
            autoescape = None
        ))
        tornado.web.Application.__init__(self, handlers, **settings)

