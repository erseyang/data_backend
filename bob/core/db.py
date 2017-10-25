#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: eric.yang
@contact: erseyang@gmail.com
@site: http://www.lizit.net
@desc:用于对数据库的处理
@time: 17/2/15 下午8:54
"""
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
sqla_engine = create_engine('mysql://bob:bobspider@114.55.151.132:3306/bob_spider?charset=utf8',convert_unicode=True, encoding='utf-8', echo=False, pool_size = 100)
# sqla_engine = create_engine('mysql://root:CP2016_@new@120.132.51.138:3506/bob?charset=utf8',convert_unicode=True, encoding='utf-8', echo=False, pool_size = 100)
##redis连接池
Base = declarative_base()

Session = sessionmaker(bind=sqla_engine)


