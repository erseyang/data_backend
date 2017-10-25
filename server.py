#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: eric.yang
@contact: erseyang@gmail.com
@site: http://www.lizit.net
@file: server.py
@time: 17/2/12 下午2:47
"""
import tornado
import tornado.httpserver
from tornado.options import define, options
from bob import Application

define("port", default=8095, help="run on the given port", type=int)
if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

