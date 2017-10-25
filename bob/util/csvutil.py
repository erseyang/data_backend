#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: eric.yang
@contact: erseyang@gmail.com
@site: http://www.lizit.net
@software: PyCharm
@desc: csv导出
@time: 17/2/23 上午11:37
"""
import xlwt
from bob.core.db import Session, sqla_engine


# def xls(sql='select ts.shop_name, ts.shop_url, ts.shop_boss_tb, ts.shop_level, tp.product_url, tp.product_name, tp.product_sales_count, tp.`original_price` from t_shop as ts, t_product as tp where ts.shop_id = tp.shop_id and ts.task_id = 3 order by tp.`product_sales_count` desc'):
#     result = sqla_engine.execute(sql)
#
#     print(result)

sql = "this is a bad"
sql += ", yeah, oh good"

print sql


