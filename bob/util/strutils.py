#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: eric.yang
@contact: erseyang@gmail.com
@site: http://www.lizit.net
@software: PyCharm
@desc:一些string数据处理
@time: 17/3/14 上午11:50
"""
import re
import hashlib

#手机号码加密
def isMobile(str):
    p2=re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
    phonematch=p2.match(str)
    if phonematch:
        return True
    return False

##md5加密
def password_md5(str):
    return hashlib.md5(str).hexdigest()
