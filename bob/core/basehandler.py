#!/usr/bin/env python
# encoding: utf-8
import functools
import json
import logging
import tornado
import tornado.web
from bob.model.user import UserDao
from bob.util import jwtutils
import config


# 允许发起请求的host列表
HOST_ACCEPT_LIST = ["127.0.0.1:8091"]
class BaseHandler(tornado.web.RequestHandler):
    url_pattern = None

    def data_received(self, chunk):
        pass

    def options(self):
        # no body
        self.set_default_headers()
        # self.set_status(204)
        self.finish()

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        # self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS')
        self.set_header('Cache-Control', 'no-cache')
        self.set_header('If-Modified-Since', '0')

    def get_args(self, key, default=None, type=None):
        if type == list:
            if default is None: default = []
            return self.get_arguments(key, default)
        value = self.get_argument(key, default)
        if value and type:
            try:
                value = type(value)
            except ValueError:
                value = default
        return value

    def to_json(self, status, msg, object):
        value = {"status": status, "msg": msg, "object": object}
        return json.dumps(value)

    def get_user_by_id(self, id):
        self.userDao = UserDao()
        return self.userDao.get_user_by_id(id)

class AccessHandler(BaseHandler):
    def prepare(self):
        # 获取请求头，并对请求头做做处理
        # if (config.debug):
        #     logging.info("prepare")
        headers = self.request.headers
        # if (config.debug):
        #     logging.info(headers)
        if not self.ckeck_access_token(headers):
            # 不通过则返回禁止信息
            result = {}
            result["status"] = 1000
            result["message"] = "请登录"
            self.finish(result)
        else:
            return

    def get_current_user(self):
        access_token = self.request.headers['Authorization']
        id = jwtutils.check_id_decode(access_token, config.serect_key)
        user = self.get_user_by_id(id)
        return user

    def ckeck_access_token(self, headers):
        # 判断host是否合法
        if "Host" in headers and headers["Host"] in HOST_ACCEPT_LIST:
            user_host = headers["Host"]
        else:
            # return False
            logging.info('Host:' + headers["Host"])
        # 判断token
        if 'Authorization' in headers:
            access_token = headers['Authorization']
            logging.info(access_token)
            if jwtutils.valid_expired_decode(access_token, config.serect_key) == "100":
                return False
            id = jwtutils.check_id_decode(access_token, config.serect_key)
            user = self.get_user_by_id(id)
            if user is None:
                return False
        else:
            return False
        # 执行到最后还不返回True就说明token错误
        return True

def authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        header = self.request.headers(config.header_key)
        id = jwtutils.check_id_decode(header)
        user = self.get_current_user(id)
        if user is None:
            if self.request.method in ("GET", "HEAD", "POST"):
                result = {}
                result["status"] = 1001
                result["message"] = "请登录"
                self.finish(result)
                return
            raise tornado.HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper