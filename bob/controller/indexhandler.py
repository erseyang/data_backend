#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: eric.yang
@contact: erseyang@gmail.com
@site: http://www.lizit.net
@software: PyCharm
@file: indexhandler.py
@time: 17/3/28 下午3:55
"""
from bob.core.basehandler import AccessHandler
from bob.model.markshop import MarkShopDao
from bob.model.product import ProductDao
from bob.model.shop import ShopDao
from bob.model.task import TaskDao


class IndexDataHandler(AccessHandler):
    def initialize(self):
        self.productDao = ProductDao()
        self.shopDao = ShopDao()
        self.taskDao = TaskDao()

    def post(self):
        productData = self.productDao.get_all_product()
        shopData = self.shopDao.select_all_shop_count()
        taskData = self.taskDao.get_all_task_count()
        result = {}
        result["status"] = 0
        result["message"] = "获取数据成功"
        result["productData"] = productData
        result["shopData"] = shopData
        result["taskData"] = taskData
        self.finish(result)

class IndexMarkHandler(AccessHandler):
    def initialize(self):
        self.markShopDao = MarkShopDao()

    def post(self, *args, **kwargs):
        page = self.get_args("page")
        pageSize = self.get_args("pageSize")
        if page is None or page == '':
            page = 1
        else:
            page = int(page)
        if pageSize is None or pageSize == '':
            pageSize = 20
        else:
            pageSize = int(pageSize)

