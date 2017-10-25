#!/usr/bin/env python
# encoding: utf-8
import json
from tornado.escape import json_decode
import bob
from bob.core.basehandler import BaseHandler
from bob.model.user import UserDao
from bob.util import jwtutils
from bob.util.strutils import isMobile
from bob.util.strutils import password_md5
import config

#首页
class AdminHandler(BaseHandler):
    def initialize(self):
        self.user = self.get_current_user()

    def get(self):
        self.render("admin/index.html", head_text="bob数据平台", user = self.adminUser)
# 登录接口
class LoginHandler(BaseHandler):
    def initialize(self):
        self.userDao = UserDao()

    def post(self, *args, **kwargs):
        username = self.get_args("username")
        password = self.get_args("password")
        result = {}
        if isMobile(username):
            user = self.userDao.get_user_by_mobile(username)
        else:
            user = self.userDao.get_user_by_username(username)
        if user is None:
            result["status"] = 1
            result["message"] = '无此用户'
            self.finish(result)
            return
        userPass = user.password
        password = password_md5(password)
        if password == userPass:
            result["status"] = 0
            result["message"] = "登录成功"
            result["id"] = user.id
            token = jwtutils.jwt_encode(user.id, config.one_month_seconds, config.serect_key)
            result["token"] = token
        else:
            result["status"] = 2
            result["message"] = "密码不正确"
        self.finish(result)