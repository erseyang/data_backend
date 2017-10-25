#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: eric.yang
@contact: erseyang@gmail.com
@site: http://www.lizit.net
@file: utils.py
@time: 17/2/15 下午9:12
"""
import hashlib
import uuid
import time
import datetime
import re
import jwt

def jwt_encode(payload, key):
    return jwt.encode(payload, key, algorithm='HS256')

def jwt_decode(jwt, key):
    try:
        return jwt.decode(jwt, key)
    except:
        return None
##md5加密
def md5(str):
    return hashlib.md5(str.encode('utf-8')).hexdigest()

##sha1加密
def sha1(str):
    return hashlib.sha1(str.encode('utf-8')).hexdigest()

def timestamp():
    return int(time.time())

def datetime_no_format():
    return datetime.datetime.now()

def datetime_my():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

##格式化年月
def format_ym(indate):
    return indate.strftime('%m-%d')


##生成uuid
def getuuid():
    return str(uuid.uuid1())

##判断是否是手机号码
def is_tel(str):
    p = re.compile(r'(1)([3,7]\d|4[5,7]|5[0-3,5-9]|8[0,2,3,6-9])\D*(\d{4})\D*(\d{4})$')
    match = p.match(str)
    if match:
        return True
    else:
        return False
##判断是否是邮箱
def is_email(str):
    p = re.compile(r'\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*')
    match = p.match(str)
    if match:
        return True
    else:
        return False


