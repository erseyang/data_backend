#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: eric.yang
@contact: erseyang@gmail.com
@desc:数据处理
@software: PyCharm
@file: datautils.py
@time: 17/4/11 下午5:10
"""
import datetime

#计算两个日期区间
import random
import string
import numpy as np


def datediff(maxDate, minDate):
    format = "%Y%m%d"
    bd = strtodatetime(minDate, format)
    ed = strtodatetime(maxDate, format)
    oneday = datetime.timedelta(days=1)
    count = 0
    while bd != ed:
        ed = ed - oneday
        count += 1
    return count

# 将字符串转换成datetime类型
def strtodatetime(datestr, format):
    return datetime.datetime.strptime(datestr, format)

##生成六个时间节点
def create_time_range(maxDate, minDate):
    count = datediff(maxDate, minDate)
    date_range = count / 6 + 1
    date_list = []
    date_list.append(minDate)
    date_list.append(date_add_days(minDate, date_range))
    date_list.append(date_add_days(minDate, date_range * 2))
    date_list.append(date_add_days(minDate, date_range * 3))
    date_list.append(date_add_days(minDate, date_range * 4))
    date_list.append(maxDate)
    return date_list

def date_add_days(start, days):
    format = "%Y%m%d"
    start_format = strtodatetime(start, format)
    return (start_format + datetime.timedelta(days=days))

def md_rate_fun(all, md):
    if all is None or all == '':
        return 0
    return md * 100 / all

def price_space_data(params):
    new_list = params
    print params
    del_value = []
    for i , el in enumerate(new_list, 0):
        if el[0] == '' or el[0] is None:
            del_value.append(new_list[i])
            continue
        if string.find(el[0], u'¥') != -1:
            price = string.replace(el[0], u'¥', '',1)
            price = str_to_float(price)
            tp = list(new_list[i])
            tp[0] = price
            new_list[i] = tuple(tp)
            continue
        if string.find(el[0], u'-') != -1:
            price1 = float(string.split(el[0], u'-')[0])
            price2 = float(string.split(el[0], u'-')[1])
            price = (price1 + price2) /2
            tp = list(new_list[i])
            tp[0] = price
            new_list[i] = tuple(tp)
            continue
        price = str_to_float(el[0])
        tp = list(new_list[i])
        tp[0] = price
        new_list[i] = tuple(tp)
    for i, value in enumerate(del_value, 0):
        new_list.remove(value)
    return sorted(new_list, key=lambda tup: float(tup[0]), reverse=True)

def str_to_float(value):
    if isinstance(value, float):
        return float(value)
    return value
##生成价格区间数
def create_random_price(max, min):
    if isinstance(max, basestring):
        max = float(max)
    if isinstance(min, basestring):
        min = float(min)
    return_value = []
    internal = int((max + min) / 10) + 1
    return_value.append(min)
    i = 1
    while i < 9:
        value = min + i * internal
        return_value.append(value)
        i += 1
    return_value.append(max)
    return return_value

##统计价格数据
def sum_sales(params, params1):
    sum_list = []
    sum_1 = 0
    sum_2 = 0
    sum_3 = 0
    sum_4 = 0
    sum_5 = 0
    sum_6 = 0
    params.sort()
    print params1
    for i , el in enumerate(params1, 0):
        value = el[0]
        counts = el[1]
        if counts is None:
            counts = 0
        if isinstance(value, basestring):
            value = float(value)
        if value >= params[0] and value < params[1]:
            sum_1 += counts
        elif value > params[1] and value <= params[2]:
            sum_2 += counts
        elif value > params[2] and value <= params[3]:
            sum_3 += counts
        elif value > params[3] and value <= params[4]:
            sum_4 += counts
        elif value > params[4] and value <= params[5]:
            sum_5 += counts
        else:
            sum_6 += counts
    sum_list.append(sum_1)
    sum_list.append(sum_2)
    sum_list.append(sum_3)
    sum_list.append(sum_4)
    sum_list.append(sum_5)
    sum_list.append(sum_6)
    return sum_list
# params = [(u'0.6-1.6', 23L), (u'', 11L), (u'', 23L), (u'0.15-0.2', 4L),
#         (u'', 4L), (u'1-2', 3L), (u'¥1.5', 0L), (u'0.25-0.8', 0L), (u'0.5-1', 0L), ('3.4', 26), ('10.8', 79)]
#
# params_1 = price_space_data(params)

# print params_1
#
# param_price = [10.8, 3.4, 0.525, 1.1, 1.5, 0.175]
#
# param_price.sort()
#
# print param_price
#
# print sum_sales(param_price, params_1)



# s_list = [1, 5, 7, 9, 18, 2, (0, 3), "123"]
# del_value = [5, 2, "123"]
# for i, value in enumerate(del_value, 0):
#       print value
#       s_list.remove(value)
# s_list.remove(18)
# print s_list
# print string.find(ss, '@')
# print string.find(ss, u'¥')
#
# data_test = [20, 15, 40, 32, 50, 1000, 25, 3000]
#
# data_test.sort()
#
# print data_test
#
# data = create_random_price(3990.00, 70.00)
# print data
#
# print(data_test.append(data))

# print data_test.men()
