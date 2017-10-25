#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: eric.yang
@contact: erseyang@gmail.com
@site: http://www.lizit.net
@software: PyCharm
@desc:任务操作接口
@time: 17/3/15 下午4:57
"""
import logging
import datetime
import random
from sqlalchemy import text
from bob.core.basehandler import AccessHandler
from bob.core.db import sqla_engine, Session
from bob.model.product import ProductDao
from bob.model.shop import ShopDao
from bob.model.task import TaskDao, TaskTypeDao
from bob.util.datautils import price_space_data, sum_sales, create_random_price
from bob.util.jsonutils import task_list_to_json, model_object_to_json, list_to_json, type_list_to_json
import pandas as pd


class TaskAddHandler(AccessHandler):
    def initialize(self):
        self.taskDao = TaskDao()
        self.taskTypeDao = TaskTypeDao()

    def post(self, *args, **kwargs):
        taskName = self.get_args("taskName")
        taskKey = self.get_args("key")
        taskType = self.get_args("type")
        taskNum = self.get_args("taskNum")
        startTime = self.get_args("startTime")
        taskComment = self.get_args("is_comment")
        if taskComment is None or taskComment == '':
            taskComment = 0
        url = self.get_args("url")
        if startTime is None or startTime == '':
            startTime = datetime.datetime.now()
        if taskNum is None or taskNum == '' or taskNum == '0':
            taskNum = 100
        types = self.get_args("shopType")
        user = self.get_current_user()
        taskId = self.taskDao.add_task(taskName, taskKey, taskType, taskNum,
                                       startTime, user.id, url, 0, taskComment)
        self.taskDao.update_task_id(taskId, taskId)
        self.taskTypeDao.add_type(taskId, types.split(","))
        result = {}
        result["status"] = 0
        result["message"] = "添加成功"
        self.finish(result)


# 提交关键字查询
class TaskListHandler(AccessHandler):
    def initialize(self):
        self.taskDao = TaskDao()
        self.taskTypeDao = TaskTypeDao()

    def post(self, *args, **kwargs):
        page = self.get_args("page")
        pageSize = self.get_args("pageSize")
        search = self.get_args("key")
        status = self.get_args("status")
        if page is None or page == '':
            page = 1
        else:
            page = int(page)
        if pageSize is None or pageSize == '':
            pageSize = 20
        else:
            pageSize = int(pageSize)
        if search is None:
            search = ''
        result = {}
        tasks = self.taskDao.get_task_list(search, page, pageSize, status)
        count = self.taskDao.get_task_count(search, status)
        lastPage = count / pageSize + 1
        pagination = {}
        pagination.setdefault("size", count)
        pagination.setdefault("current_page", page)
        pagination.setdefault("last_page", lastPage)
        pagination["pageSize"] = pageSize
        tasks = task_list_to_json(tasks)
        for task in tasks:
            id = task["id"]
            child_task = self.taskDao.get_child_task_list(id, 0)
            task["childs"] = task_list_to_json(child_task)
            taskTypes = self.taskTypeDao.get_task_type(task["task_id"])
            task["task_types"] = type_list_to_json(taskTypes)
        result["status"] = 0
        result["message"] = "获取数据成功"
        result["tasks"] = tasks
        result["pagination"] = pagination
        self.finish(result)


# 更新任务，就是添加新的子任务
class TaskUpdateHandler(AccessHandler):
    def initialize(self):
        self.taskDao = TaskDao()
        self.taskTypeDao = TaskTypeDao()

    def post(self, *args, **kwargs):
        taskId = self.get_args("task_id")
        task = self.taskDao.get_task_details(taskId)
        user = self.get_current_user()
        task = model_object_to_json(task)
        task_id = self.taskDao.add_task(task["task_name"], task["task_key"], task["task_type"],
                                        task["task_num"], '', user.id, url=task["task_url"], parentId=task["id"])
        taskType = self.taskTypeDao.get_task_type(taskId)
        taskType = type_list_to_json(taskType)
        types = []
        for type in taskType:
            types.append(type["task_type"])
        self.taskDao.update_task_id(task_id, task_id)
        self.taskTypeDao.add_type(task_id, types)
        result = {}
        result["status"] = 0
        result["message"] = "更新成功"
        self.finish(result)


#查找任务详情
class TaskDetailsHandler(AccessHandler):
    def initialize(self):
        self.taskDao = TaskDao()
        self.taskTypeDao = TaskTypeDao()

    def post(self, *args, **kwargs):
        taskId = self.get_args("task_id")
        task = self.taskDao.get_task_details(taskId)
        task = model_object_to_json(task)
        taskType = self.taskTypeDao.get_task_type(taskId)
        taskType = type_list_to_json(taskType)
        task["task_types"] = taskType
        result = {}
        result["task"] = task
        result["status"] = 0
        result["message"] = "获取成功"
        self.finish(result)


##关闭任务或者重新任务
class TaskIsOpenHandler(AccessHandler):
    def initialize(self):
        self.taskDao = TaskDao()

    def post(self, *args, **kwargs):
        taskId = self.get_args("task_id")
        is_open = self.get_args("is_open")
        self.taskDao.close_or_open_task(taskId, is_open)
        result = {}
        result["status"] = 0
        result["message"] = "更新成功"
        self.finish(result)


##任务数据接口
class TaskDataHandler(AccessHandler):
    def initialize(self):
        self.taskDao = TaskDao()
        self.shopDao = ShopDao()
        self.productDao = ProductDao()

    def post(self, *args, **kwargs):
        taskId = self.get_args("task_id")
        shopCount = self.shopDao.select_all_shop_by_task_id(taskId)
        productCount = self.productDao.get_all_products_by_taskid(taskId)
        productSales = self.productDao.get_sales_count_by_taskid(taskId)
        productMidPrice = self.productDao.get_mid_price_by_taskid(taskId)
        result = {}
        result["status"] = 0
        result["message"] = "更新成功"
        result["shopCount"] = shopCount
        result["productCount"] = productCount
        result["sales"] = productSales
        result["midPrice"] = productMidPrice
        self.finish(result)


##任务等级接口
class TaskRankHandler(AccessHandler):
    def initialize(self):
        self.taskDao = TaskDao()
        self.shopDao = ShopDao()
        self.productDao = ProductDao()

    def post(self, *args, **kwargs):
        taskId = self.get_args("task_id")
        salesRank = self.shopDao.get_sales_ranking_by_task_id(taskId)
        salesRank = list_to_json(salesRank)
        commentsRank = self.shopDao.get_comments_by_task_id(taskId)
        commentsRank = list_to_json(commentsRank)
        levelRank = self.shopDao.get_shop_level_by_task_id(taskId)
        levelRank = list_to_json(levelRank)
        result = {}
        result["status"] = 0
        result["message"] = "更新成功"
        result["sales"] = salesRank
        result["comment"] = commentsRank
        result["level"] = levelRank
        self.finish(result)

##价格空间分布
class TaskPriceHandler(AccessHandler):
    def initialize(self):
        self.taskDao = TaskDao()

    def post(self, *args, **kwargs):
        taskId = self.get_args("task_id")
        prices = self.taskDao.get_price_range_by_task_id(taskId)
        prices = price_space_data(prices)
        plist = list(prices)
        price_list_sum = []
        price_list = []
        length = plist.__len__()
        if length > 0 and length <= 1:
            price_list.append(plist[0][0])
            price_list.append(plist[0][0])
            price_list_sum.append(plist[0][1])
            price_list_sum.append(plist[0][1])
        elif length > 10:
            min = plist[length - 1][0]
            max = plist[0][0]
            price_list = create_random_price(max, min)
            price_list_sum = sum_sales(price_list, plist)
        else:
            price_list_sum = sorted(plist, key=lambda tup: float(tup[1]), reverse=True)
            price_list = sorted(plist, key=lambda tup: float(tup[0]), reverse=True)
        result = {}
        result["status"] = 0
        result["message"] = "更新成功"
        result["product_sales_count"] = price_list_sum
        result["price_value"] = price_list
        self.finish(result)


##商户等级分布
class TaskShopLevelHandler(AccessHandler):
    # def initialize(self):
    #     self.taskDao = TaskDao()

    def post(self, *args, **kwargs):
        taskId = self.get_args("task_id")
        df = pd.read_sql_query(
            'select (CASE WHEN shop_level>=4 and shop_level<=250 then 1 WHEN shop_level>=251 and shop_level<=10000 then 2 '
            'WHEN shop_level>=10001 and shop_level<=500000 then 3 WHEN shop_level>=5000001 and shop_level<=10000000 '
            'then 4 WHEN shop_level>=100000001 then 5 ELSE 0 END) as star, count(id) as shop_count from t_shop '
            'where shop_type = 1 and task_id = ' + taskId + ' group by star;', sqla_engine)
        res = df.to_json()
        self.finish(res)


##商户区域分布
class TaskShopAreaHandler(AccessHandler):
    def post(self, *args, **kwargs):
        taskId = self.get_args("task_id")
        province_dic = [
            u'河北', u'山西', u'吉林', u'辽宁', u'黑龙江', u'陕西', u'甘肃', u'青海', u'山东', u'福建', u'浙江', u'台湾', u'河南', u'湖北', u'湖南',
            u'江西', u'江苏', u'安徽',
            u'广东', u'海南', u'四川', u'贵州', u'云南', u'北京', u'上海', u'天津', u'重庆', u'内蒙古', u'新疆', u'宁夏', u'广西', u'西藏', u'香港',
            u'澳门'
        ]
        result = {}
        for province in province_dic:
            query = text(
                u"select count(DISTINCT shop_id) from t_shop where task_id = " + taskId + " and  shop_area like '%" + province + "%';")
            count = Session().execute(query).scalar()
            result[province] = count
        self.finish(result)
