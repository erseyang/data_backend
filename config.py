#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: eric.yang
@contact: erseyang@gmail.com
@site: http://www.lizit.net
@file: config.py
@time: 17/2/12 下午3:19
"""
import os

cookie_name = "admin_user"

debug = True

serect_key = "34jdn+m===mdnlvmndkMNdl"

header_key = "bob_data"

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates')
STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')

#一天的秒数
one_day_seconds = 24 * 60 * 60
#一周的秒数
one_week_seconds = one_day_seconds * 7
# 一月秒数
one_month_seconds = one_day_seconds * 30
# 一年秒数
one_year_seconds = one_day_seconds * 365
