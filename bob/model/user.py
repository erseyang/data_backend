#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: eric.yang
@contact: erseyang@gmail.com
@site: http://www.lizit.net
@software: PyCharm
@file: user.py
@time: 17/2/15 下午8:54
"""
import datetime
from sqlalchemy.ext.declarative import declarative_base
from bob.core.db import Session
from bob.model.models import TUser

class UserDao():
    def __init__(self):
        self.session = Session()
    ## 根据ID查询用户
    def get_user_by_id(self, id):
        return self.session.query(TUser).filter(TUser.id == id).first()
    ## 添加用户
    def add_user(self, user_name, mobile, password, real_name, role_id):
        user = TUser()
        user.user_name = user_name
        user.mobile = mobile
        user.password = password
        user.real_name = real_name
        user.role_id = role_id
        user.create_time = datetime.datetime.now()
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user.id
    ## 搜索列表
    def get_users_list(self, search, page, page_size):
        if search is None:
            search = ""
        return self.session.query(TUser).filter(TUser.real_name.like('%{0}%'.format(search)))\
            .offset((page - 1) * page_size).limit(page_size).all()
    ##获取所有用户数量
    def get_users_count(self, search):
        if search is None:
            search = ""
        return self.session.query(TUser).filter(TUser.real_name.like('%{0}%'.format(search))).count()
    ##通过手机查询
    def get_user_by_mobile(self, mobile):
        return self.session.query(TUser).filter(TUser.mobile == mobile).first()
    ##通过用户名查找
    def get_user_by_username(self, username):
        return self.session.query(TUser).filter(TUser.user_name == username).first()
    #更新用户密码
    def update_user_pass(self, id, newPass):
        self.session.query(TUser).filter(TUser.id == id).update({"password": newPass}, synchronize_session=False)
        self.session.commit()
    ##删除用户
    def delete_user_by_id(self, id):
        self.session.query(TUser).filter(TUser.id==id).delete()
        return

# userDao = UserDao()
# userDao.delete_user_by_id(4)




