#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: eric.yang
@contact: erseyang@gmail.com
@site: http://www.lizit.net
@software: PyCharm
@file: jwtutils.py
@time: 17/3/14 下午2:52
"""
import datetime
import jwt
from jwt.exceptions import ExpiredSignatureError

# jwt加密
def jwt_encode(id, exp, serect):
    return jwt.encode({'id': id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=exp)}, serect)

# jwt验证时间是否过期 0 是在有限期间，100是过期
def valid_expired_decode(str, serect):
    try:
        jwt.decode(str, serect)
        return "0"
    except ExpiredSignatureError:
        return "100"

#获取用户ID
def check_id_decode(str, serect):
    try:
        jwt_str = jwt.decode(str, serect)
        return jwt_str.get('id')
    except Exception as e:
        return e
# str = jwt_encode(1, 10, config.serect_key)
# print str
# print valid_expired_decode(str, config.serect_key)
#
# print check_id_decode(str, config.serect_key)