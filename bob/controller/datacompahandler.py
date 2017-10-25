#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: eric.yang
@contact: erseyang@gmail.com
@site: http://www.lizit.net
@software: PyCharm
@file: datacompahandler.py
@time: 17/4/28 下午5:24
"""
from bob.core.basehandler import AccessHandler
from bob.model.product import ProductDao
from bob.util import dateutils


class DataCompa(AccessHandler):
    def initialize(self):
        self.productDao = ProductDao()

    def post(self, *args, **kwargs):
        taskId = self.get_args("task_id")
        page = self.get_args("page")
        if page is None or page == '' or page == 'undefined':
            page = 1
        else:
            page = int(page)
        pageSize = self.get_args("pageSize")
        if pageSize is None or pageSize == '' or pageSize == 'undefined':
            pageSize = 20
        else:
            pageSize = int(pageSize)
        product_date = self.productDao.get_data_date_by_task_id(taskId)
        for value in product_date:
            if value == '00000000':
                product_date.remove(value)
        minDate = product_date[0][0]
        length = len(product_date)
        maxDate = product_date[length - 1][0]
        result = {}
        check_list = []
        days = dateutils.diffDate(dateutils.str2date(minDate), dateutils.str2date(maxDate))
        #只是当前的参数，可修改。
        if days > 10:
            products_start = self.productDao.get_data_by_date_with_taskid(minDate, taskId, page, pageSize)
            count = self.productDao.get_all_count_by_date_with_taskid(minDate, taskId)
            pagination = {}
            lastPage = count / pageSize + 1
            pagination.setdefault("size", pageSize)
            pagination.setdefault("current_page", page)
            pagination.setdefault("last_page", lastPage)
            product_end = self.productDao.get_data_by_date_with_taskid(maxDate, taskId, page, pageSize)
            product_all = self.productDao.get_all_data_by_date_with_taskid(maxDate, taskId)
            for index, product in products_start:
                p_end = product_end[index]
                check_list["product_id"] = product.product_id
                check_list["product_name"] = product.product_name
                check_list["product_url"] = product.product_url
                if p_end.product_id == product.product_id:
                    ##状态没变化
                    check_list["state"] = "0"
                else:
                    for p_all in product_all:
                        if product.product_id == p_all.product_id:
                            ##位置有变化
                            check_list["state"] = "1"
                            continue
                        ##没有找到
                        check_list["state"] = "2"
            result["status"] = 0
            result["message"] = "测试成功"
            result["start_date"] = minDate
            result["end_date"] = maxDate
            result["product_check"] = check_list
            result["pagination"] = pagination
        else:
            result["status"] = 1
            result["message"] = "没有可测试数据"
        self.finish(result)

class DataEndCompa(AccessHandler):
    def initialize(self):
        self.productDao = ProductDao()
    def post(self, *args, **kwargs):
        taskId = self.get_args("task_id")
        page = self.get_args("page")
        if page is None or page == '' or page == 'undefined':
            page = 1
        else:
            page = int(page)
        pageSize = self.get_args("pageSize")
        if pageSize is None or pageSize == '' or pageSize == 'undefined':
            pageSize = 20
        else:
            pageSize = int(pageSize)
        product_date = self.productDao.get_data_date_by_task_id(taskId)
        for value in product_date:
            if value == '00000000':
                product_date.remove(value)
        minDate = product_date[0][0]
        length = len(product_date)
        maxDate = product_date[length - 1][0]
        result = {}
        check_end_list = []
        days = dateutils.diffDate(dateutils.str2date(minDate), dateutils.str2date(maxDate))
        #只是当前的参数，可修改。
        if days > 10:
            count = self.productDao.get_all_count_by_date_with_taskid(minDate, taskId)
            pagination = {}
            lastPage = count / pageSize + 1
            pagination.setdefault("size", pageSize)
            pagination.setdefault("current_page", page)
            pagination.setdefault("last_page", lastPage)
            product_end = self.productDao.get_data_by_date_with_taskid(maxDate, taskId, page, pageSize)
            product_end_all = self.productDao.get_all_data_by_date_with_taskid(minDate, taskId)
            for index, product in product_end:
                check_end_list["product_id"] = product.product_id
                check_end_list["product_name"] = product.product_name
                check_end_list["product_url"] = product.product_url
                for p_all in product_end_all:
                    if product.product_id == p_all.product_id:
                        continue
                    check_end_list["state"] = "2"
            result["status"] = 0
            result["message"] = "测试成功"
            result["start_date"] = minDate
            result["end_date"] = maxDate
            result["product_check_end"] = check_end_list
            result["pagination"] = pagination
        else:
            result["status"] = 1
            result["message"] = "没有可测试数据"
        self.finish(result)

