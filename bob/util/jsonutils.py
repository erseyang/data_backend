#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: eric.yang
@contact: erseyang@gmail.com
@site: http://www.lizit.net
@software: PyCharm
@desc:list转json对象
@time: 17/3/15 下午3:56
"""
#对user对象进行转换
import datetime
from decimal import Decimal
from sqlalchemy.ext.declarative import DeclarativeMeta
import types
from bob.model.models import TShop

NumberTypes = (types.IntType, types.LongType, types.FloatType, types.ComplexType)
def user_to_json(result):
    user_list = []
    for obj in result:
        d = dict()
        if isinstance(obj.__class__, DeclarativeMeta):
           for column in obj.__table__.columns:
               value = getattr(obj, column.name)
               if isinstance(value, NumberTypes):
                   d[column.name] = str(value)
               elif isinstance(value, datetime.datetime):
                   d[column.name] = str(datetime.datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S'))
               else:
                   if value:
                      d[column.name] = str(value.encode('utf-8'))
                   else:
                      d[column.name] = ''
        user_list.append(d)
    return user_list
def type_list_to_json(result):
    type_list = []
    for obj in result:
        d = dict()
        if isinstance(obj.__class__, DeclarativeMeta):
           for column in obj.__table__.columns:
               value = getattr(obj, column.name)
               if isinstance(value, NumberTypes):
                   d[column.name] = str(value)
               elif isinstance(value, datetime.datetime):
                   d[column.name] = str(datetime.datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S'))
               else:
                   if value:
                      d[column.name] = str(value.encode('utf-8'))
                   else:
                      d[column.name] = ''
        type_list.append(d)
    return type_list
#列表转为json
def task_list_to_json(result):
    task_list = []
    for obj in result:
        d = dict()
        if isinstance(obj.__class__, DeclarativeMeta):
           for column in obj.__table__.columns:
               value = getattr(obj, column.name)
               if isinstance(value, NumberTypes):
                   d[column.name] = str(value)
               elif isinstance(value, datetime.datetime):
                   d[column.name] = str(datetime.datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S'))
               else:
                   if value:
                      d[column.name] = str(value.encode('utf-8'))
                   else:
                      d[column.name] = ''
        task_list.append(d)
    return task_list
#对象转为json
def model_object_to_json(object):
    d = dict()
    if isinstance(object.__class__, DeclarativeMeta):
        for column in object.__table__.columns:
               value = getattr(object, column.name)
               if isinstance(value, NumberTypes):
                   d[column.name] = str(value)
               elif isinstance(value, datetime.datetime):
                   d[column.name] = str(datetime.datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S'))
               else:
                   if value:
                      d[column.name] = str(value.encode('utf-8'))
                   else:
                      d[column.name] = ''
    return d

def shop_list_to_json(object):
    shop_list = []
    for result in object:
        d = dict()
        if isinstance(result.__class__, DeclarativeMeta):
           for column in result.__table__.columns:
               value = getattr(result, column.name)
               if isinstance(value, NumberTypes):
                   d[column.name] = str(value)
               elif isinstance(value, datetime.datetime):
                   d[column.name] = str(datetime.datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S'))
               else:
                   if value:
                      d[column.name] = str(value.encode('utf-8'))
                   else:
                      d[column.name] = ''
        shop_list.append(d)
    return shop_list

def shop_list_with_data_to_dict(object):
    shop_list = []
    for result in object:
        d = dict()
        result = list(result)
        for index, value in enumerate(result):
            for i, v in enumerate(TShop.__table__.columns):
                if i == index:
                    key = v.name
                else:
                    if index <= 36:
                        continue
                    elif index == 37:
                        continue
                    elif index == 38:
                        key = "sales"
                    elif index == 39:
                        key = "gc"
                    elif index == 40:
                        key = "mc"
                    elif index == 41:
                        key = "bc"
            if isinstance(value, NumberTypes):
                d[key] = str(value)
            elif isinstance(value, Decimal):
                d[key] = int(Decimal(value))
            elif isinstance(value, datetime.datetime):
                d[key] = str(datetime.datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S'))
            else:
                if value:
                    d[key] = str(value.encode('utf-8'))
                else:
                    d[key] = ''
        shop_list.append(d)
    return shop_list

def model_list_to_json(object, model):
    model_list = []
    for result in object:
        d = dict()
        result = list(result)
        for index, value in enumerate(result):
            for i, v in enumerate(model.__table__.columns):
                if i == index:
                    key = v.name
                else:
                    continue
            if isinstance(value, NumberTypes):
                d[key] = str(value)
            elif isinstance(value, datetime.datetime):
                d[key] = str(datetime.datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S'))
            else:
                if value:
                    d[key] = str(value.encode('utf-8'))
                else:
                    d[key] = ''
        model_list.append(d)
    return model_list
##产品详情
def product_with_shop_to_dict(object):
    d = dict()
    keys = ["product_id", "product_url", "product_name", "current_price", "original_price", "product_sales_count", "good_comments",
            "mid_comments", "bad_comments", "product_collections", "shop_name", "shop_url", "shop_boss_tb", "shop_area",
            "shop_level", "shop_time", "shop_desc_count", "shop_service_count","shop_logis_count", "month_tuikuan_value",
            "month_dispute_value", "month_punish_value"]
    for index, value in enumerate(object):
        key = keys[index]
        if isinstance(value, NumberTypes):
            d[key] = str(value)
        elif isinstance(value, datetime.datetime):
            d[key] = str(datetime.datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S'))
        else:
            if value:
                d[key] = str(value.encode('utf-8'))
            else:
                d[key] = ''
    return d
##对商品的转化
def product_list_to_dict(object):
    product_shop_list = []
    keys = ["product_id", "product_name", "product_sales_count", "current_price",
            "product_comments", "good_comments", "mid_comments", "bad_comments", "product_url",
            "shop_id", "shop_name", "shop_level", "shop_area", "shop_url"]
    for result in object:
        d = dict()
        result = list(result)
        for index, value in enumerate(result):
            key = keys[index]
            if isinstance(value, NumberTypes):
                d[key] = str(value)
            elif isinstance(value, datetime.datetime):
                d[key] = str(datetime.datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S'))
            else:
                if value:
                    d[key] = str(value.encode('utf-8'))
                else:
                    d[key] = ''
        product_shop_list.append(d)
    return product_shop_list
##个案处理
def list_to_json(object):
    list = []
    for result in object:
        d = dict(result)
        list.append(d)
    return list

