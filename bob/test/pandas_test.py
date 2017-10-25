#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: eric.yang
@contact: erseyang@gmail.com
@site: http://www.lizit.net
@software: PyCharm
@file: pandas_test.py
@time: 17/4/7 上午11:59
"""
import datetime
import json
import random
from sqlalchemy import create_engine
import pandas as pd
from pandas import concat
import numpy as np

db_conn = 'mysql://bob:bobspider@114.55.151.132:3306/bob_spider?charset=utf8'
db = create_engine(db_conn, convert_unicode=True, encoding='utf-8', echo=True, pool_size=100)

# sql = 'select * from t_shop as ts where ts.task_id = 50'
sql = 'select tp.product_id, DATE_FORMAT(tp.create_time, "%%Y%%m%%d") as date_frame from t_product as tp where tp.task_id = 50 limit 10'
#
sql_new = 'select tp.current_price, tp.original_price, DATE_FORMAT(tp.create_time, "%%Y%%m%%d") as date_frame ' \
          'from t_product as tp where tp.product_id = 45353762204 group by date_frame order by tp.create_time desc'
# result = pd.read_sql_query(sql, db, index_col='product_id')
result = pd.read_sql_query(sql_new, db)
# result = pd.read_sql_query(sql, db)

# print result


length = result['date_frame'].__len__()
# print length
if length > 0 and length <= 1:
    result1 = result
    result = pd.concat([result, result1], ignore_index=True)
    # result.loc[1] = {"current_price": result['current_price'], "original_price":
    # result['original_price'], "date_frame": result['date_frame']}
# if length > 1 and length <= 6:

# print result['original_price'].to_json()

def date_add_days(start, range):
    format = "%Y%m%d";
    ss = strtodatetime(start, format)
    end = ss + datetime.timedelta(days=range)
    return end

def datediff(maxDate, minDate):
    format = "%Y%m%d";
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


print datediff('20170421', '20170403')

# ages = [20, 22,25,27,21,23,37,31,61,45,41,32]
#
# bins = [18, 25, 35, 60, 100]
#
# cats = pd.cut(ages, bins)
# #
# print cats.to_json()

# bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
# cats = pd.cut(df['yanzhi'], bins)

#prop_rates = pd.DataFrame(data = [1000, 5000, 12000, 20000, 28000], index=['Rural','Semiurban','Urban'],columns=['rates'])

# print prop_rates.cut(prop_rates['data'])
# s = pd.Series([1,3,5,np.nan,6,8])
# print s
#
# dates = pd.date_range('20160101',periods=6)
# print dates
#
# df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
#
# print df.tail(3)
#
# dd = pd.date_range(start='20170403',  periods=7)
# print dd
# dates = pd.Series();
df3 = pd.DataFrame({"current_price": pd.Series(1,index=list(range(7)),dtype='float32'),
                    "original_price": pd.Series(1,index=list(range(7)),dtype='float32'),
                    "create_time": pd.date_range(start='20170403',  periods=7)})
# df2 = pd.DataFrame({ 'A' : 1.,
#                      'B' : pd.Timestamp('20160102'),
#                      'C' : pd.Series(1,index=list(range(4)),dtype='float32'),
#                      'D' : np.array([3]*4,dtype='int32'),
#                      'E' : pd.Categorical(["test","train","test","train"]),
#                      'F' : 'foo' })
# print df3['create_time']
#
# ll = df3['create_time'].__len__()
# print ll
#
# print df3['create_time'][ll - 1]
#
# print pd.cut(df3['create_time'], 6, precision=2)

list = []
list.append(("123", "345", "20170421"))
list.append(("123", "345", "20170425"))
list.append(("123", "345", "20170435"))
list.append(7)
list.append(8)
list.append(14)
print list
list.pop(3)
print list
list2 = random.sample(list, 3)
print list2
list2.sort()
print list2
print json.dumps(list)
