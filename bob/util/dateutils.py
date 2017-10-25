#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: eric.yang
@contact: erseyang@gmail.com
@site: http://www.lizit.net
@software: PyCharm
@file: dateutils.py
@time: 17/4/28 下午9:37
"""
import datetime


def str2date(str):
    return datetime.datetime.strptime(str, "%Y%m%d").date()

def diffDate(start, end):
    return (end - start).days

# start = str2date("20170203")
# end = str2date("20170208")
# print(diffDate(start, end))
# list = ['1', '2', '3']
# for value in list:
#     if value == '3':
#         list.remove(value)
# print list

