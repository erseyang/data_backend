#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: eric.yang
@contact: erseyang@gmail.com
@site: http://www.lizit.net
@software: PyCharm
@file: userhandler.py
@time: 17/3/14 下午5:53
"""
import json
from bob.core.basehandler import BaseHandler, AccessHandler
from bob.model.user import UserDao
from bob.util import strutils
from bob.util.jsonutils import user_to_json
from bob.util.strutils import password_md5


class UserAddHandler(AccessHandler):
    def initialize(self):
        self.userDao = UserDao()

    def post(self, *args, **kwargs):
        username = self.get_args("user_name")
        mobile = self.get_args("mobile")
        password = self.get_args("password")
        real_name = self.get_args("real_name")
        role_id = self.get_args('role_id')
        password = strutils.password_md5(password)
        self.userDao.add_user(username, mobile, password, real_name, role_id)
        result = {}
        result["status"] = 0
        result["message"] = "添加成功"
        self.finish(result)

class UserListHandler(AccessHandler):
    def initialize(self):
        self.userDao = UserDao()

    def post(self, *args, **kwargs):
        page = self.get_args("page")
        if page is None:
            page = 1
        else:
            page = int(page)
        pageSize = self.get_args("pageSize")
        if pageSize is None:
            pageSize = 20
        else:
            pageSize = int(pageSize)
        key = self.get_args("key")
        users = self.userDao.get_users_list(key, page, pageSize)
        count = self.userDao.get_users_count(key)
        users = user_to_json(users)
        lastPage = count / pageSize + 1
        pagination = {}
        pagination.setdefault("size", count)
        pagination.setdefault("current_page", page)
        pagination.setdefault("last_page", lastPage)
        pagination["pageSize"] = pageSize
        result = {}
        result["status"] = 0
        result["message"] = "数据获取成功"
        result["users"] = users
        result["pagination"] = pagination
        self.finish(json.dumps(result))

class UserUpdatePassword(AccessHandler):
    def initialize(self):
        self.userDao = UserDao()

    def post(self, *args, **kwargs):
        user = self.get_current_user()
        oldPass = self.get_args("oldPass")
        newPass = self.get_args("newPass")
        userPass = password_md5(oldPass)
        result = {}
        if user.password != userPass:
            result["status"] = 1
            result["message"] = "原密码错误"
        else:
            userPass = password_md5(newPass)
            self.userDao.update_user_pass(user.id, userPass)
            result["status"] = 0
            result["message"] = "更新成功"
        self.finish(result)

class UserDeleteHandler(AccessHandler):
    def initialize(self):
        self.userDao = UserDao()

    def post(self, *args, **kwargs):
        id = self.get_args('id')
        self.userDao.delete_user_by_id(id)
        result = {}
        result["status"] = 0
        result["message"] = "更新成功"
        self.finish(result)