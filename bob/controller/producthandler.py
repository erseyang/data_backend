#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: eric.yang
@contact: erseyang@gmail.com
@site: http://www.lizit.net
@desc: 商品数据
@file: producthandler.py
@time: 17/4/6 上午10:26
"""
import random
from bob.core.basehandler import AccessHandler
from bob.core.db import sqla_engine
from bob.model.product import ProductDao
from bob.util.datautils import create_time_range, md_rate_fun
from bob.util.jsonutils import product_list_to_dict, product_with_shop_to_dict
from pandas import *


class ProductListHandler(AccessHandler):
    def initialize(self):
        self.productDao = ProductDao()

    def post(self, *args, **kwargs):
        taskId = self.get_args("task_id")
        productName = self.get_args("product_name")
        minPrice = self.get_args("min_price")
        maxPrice = self.get_args("max_price")
        minComments = self.get_args("min_comments")
        maxComments = self.get_args("max_comments")
        minSales = self.get_args("min_sales")
        maxSales = self.get_args("max_sales")
        shopName = self.get_args("shop_name")
        shopArea = self.get_args("shop_area")
        shopType = self.get_args("shop_type")
        page = self.get_args("page")
        pageSize = self.get_args("pageSize")
        if productName is None or productName == 'null':
            productName = ''
        if minPrice is None or minPrice == 'null':
            minPrice = ''
        if maxPrice is None or maxPrice == 'null':
            maxPrice = ''
        if minComments is None or minComments == 'null':
            minComments = ''
        if maxComments is None or maxComments == 'null':
            maxComments = ''
        if minSales is None or minSales == 'null':
            minSales = ''
        if maxSales is None or maxSales == 'null':
            maxSales = ''
        if shopName is None or shopName == 'null':
            shopName = ''
        if shopArea is None or shopArea == 'null':
            shopArea = ''
        if shopType is None or shopType == 'null':
            shopType = ''
        if page is None or page == '':
            page = 1
        else:
            page = int(page)
        if pageSize is None or pageSize == '':
            pageSize = 20
        else:
            pageSize = int(pageSize)
        results = self.productDao.get_product_list_and_shop(
            taskId, productName, minPrice, maxPrice, minComments,
            maxComments, minSales, maxSales, shopName, shopArea, shopType, page, pageSize)
        results = product_list_to_dict(results)
        productCount = self.productDao.get_product_count_and_shop(taskId, productName, minPrice, maxPrice, minComments,
            maxComments, minSales, maxSales, shopName, shopArea, shopType)
        pagination = {}
        if productCount is None or productCount == '':
            pagination["current_page"] = page
            pagination["size"] = 0
            lastPage = 0;
            pagination["last_page"] = lastPage
            pagination["pageSize"] = pageSize
        else:
            pagination["current_page"] = page
            pagination["size"] = productCount[0]
            lastPage = (productCount[0] + pageSize - 1) / pageSize;
            pagination["last_page"] = lastPage
            pagination["pageSize"] = pageSize
        result = {}
        result["status"] = 0
        result["message"] = "获取数据成功"
        result["products"] = results
        result["pagination"] = pagination
        self.finish(result)

##商品详情
class ProductDetailsHandler(AccessHandler):
    def initialize(self):
        self.productDao = ProductDao()

    def post(self, *args, **kwargs):
        productId = self.get_args("product_id")
        product = self.productDao.get_product_by_id(productId)
        product = product_with_shop_to_dict(product)
        result = {}
        result["status"] = 0
        result["message"] = "获取数据成功"
        result["product"] = product
        self.finish(result)

##价格变化
class ProductPriceHandler(AccessHandler):
    def initialize(self):
        self.productDao = ProductDao()

    def post(self, *args, **kwargs):
        productId = self.get_args("product_id")
        prices = self.productDao.get_price_by_product_id(productId)
        plist = list(prices)
        xDate = []
        current_price = []
        original_price = []
        length = plist.__len__()
        if length > 0 and length <= 1:
            plist.append(plist[0])
            xDate.append(plist[0][2])
            xDate.append(plist[0][2])
            current_price.append(plist[0][0])
            current_price.append(plist[0][0])
            original_price.append(plist[0][1])
            original_price.append(plist[0][1])
        elif length > 6:
            minDate = plist[length - 1][2]
            maxDate = plist[0][2]
            xDate.append(minDate)
            current_price.append(plist[length - 1][0])
            original_price.append(plist[length - 1][1])
            data_list = plist
            data_list = data_list.pop(length - 1)
            data_list = data_list.pop(0)
            data_list = random.sample(data_list, 4)
            data_list.sort()
            for index in range(len(data_list)):
                xDate.append(data_list[index][2])
                current_price.append(data_list[index][0])
                original_price.append(data_list[index][1])
            original_price.append(plist[0][1])
            current_price.append(plist[0][0])
            xDate.append(maxDate)
        else:
            for index in range(len(plist)):
                xDate.append(plist[index][2])
                current_price.append(plist[index][0])
                original_price.append(plist[index][1])
        result = {}
        result["status"] = 0
        result["message"] = "获取数据成功"
        result["xDate"] = xDate
        result["current_price"] = current_price
        result["original_price"] = original_price
        self.finish(result)

##评论变化
class ProductCommentsHandler(AccessHandler):
    def initialize(self):
        self.productDao = ProductDao()

    def post(self, *args, **kwargs):
        productId = self.get_args("product_id")
        commnets = self.productDao.get_comments_by_product_id(productId)
        clist = list(commnets)
        ##中差评
        md = []
        ##总的评论
        product_comments = []
        ##比例
        md_rate = []
        xDate = []
        length = clist.__len__()
        if length > 0 and length <= 1:
            clist.append(clist[0])
            xDate.append(clist[0][2])
            xDate.append(clist[0][2])
            md.append(clist[0][1])
            md.append(clist[0][1])
            product_comments.append(clist[0][0])
            product_comments.append(clist[0][0])
            md_rate.append(md_rate_fun(clist[0][0], clist[0][1]))
            md_rate.append(md_rate_fun(clist[0][0], clist[0][1]))
        elif length > 6:
            xDate.append(clist[length - 1][2])
            md.append(clist[length - 1][1])
            product_comments.append(clist[length - 1][0])
            md_rate.append(md_rate_fun(clist[length - 1][0], clist[length - 1][1]))
            data_list = clist
            data_list = data_list.pop(length - 1)
            data_list = data_list.pop(0)
            data_list = random.sample(data_list, 4)
            data_list.sort()
            for index in range(len(data_list)):
                xDate.append(data_list[index][2])
                product_comments.append(data_list[index][0])
                md.append(data_list[index][1])
                md_rate.append(md_rate_fun(data_list[index][0], data_list[index][1]))
            xDate.append(clist[0][2])
            md.append(clist[0][1])
            product_comments.append(clist[0][0])
            md_rate.append(md_rate_fun(clist[0][0], clist[0][1]))
        else:
            for index in range(len(clist)):
                xDate.append(clist[index][2])
                md.append(clist[index][1])
                product_comments.append(clist[index][0])
                md_rate.append(md_rate_fun(clist[index][0], clist[index][1]))
        result = {}
        result["status"] = 0
        result["message"] = "获取数据成功"
        result["xDate"] = xDate
        result["product_comments"] = product_comments
        result["md"] = md
        result["md_rate"] = md_rate
        self.finish(result)

##销量变化
class ProductSalesHandler(AccessHandler):
    def initialize(self):
        self.productDao = ProductDao()

    def post(self, *args, **kwargs):
        productId = self.get_args("product_id")
        sales = self.productDao.get_sales_by_product_id(productId)
        slist = list(sales)
        xDate = []
        sales_list = []
        length = slist.__len__()
        if length > 0 and length <= 1:
            xDate.append(slist[0][1])
            xDate.append(slist[0][1])
            sales_list.append(slist[0][0])
            sales_list.append(slist[0][0])
        elif length > 6:
            xDate.append(slist[length - 1][1])
            sales_list.append(slist[length - 1][0])
            data_list = slist
            data_list = data_list.pop(length - 1)
            data_list = data_list.pop(0)
            data_list = random.sample(data_list, 4)
            data_list.sort()
            for index in range(len(data_list)):
                xDate.append(slist[index][1])
                sales_list.append(slist[index][0])
            xDate.append(slist[0][1])
            sales_list.append(slist[0][0])
        else:
            for index in range(len(slist)):
                xDate.append(slist[index][1])
                sales_list.append(slist[index][0])
        result = {}
        result["status"] = 0
        result["message"] = "获取数据成功"
        result["xDate"] = xDate
        result["sales"] = sales_list
        self.finish(result)

##人气变化
class ProductPopularHandler(AccessHandler):
    def initialize(self):
        self.productDao = ProductDao()

    def post(self, *args, **kwargs):
        productId = self.get_args("product_id")
        populars = self.productDao.get_popular_by_product_id(productId)
        plist = list(populars)
        xDate = []
        populars_list = []
        length = plist.__len__()
        if length > 0 and length <= 1:
            xDate.append(plist[0][1])
            xDate.append(plist[0][1])
            populars_list.append(plist[0][0])
            populars_list.append(plist[0][0])
        elif length > 6:
            xDate.append(plist[length - 1][1])
            populars_list.append(plist[length - 1][0])
            data_list = plist
            data_list = data_list.pop(length - 1)
            data_list = data_list.pop(0)
            data_list = random.sample(data_list, 4)
            data_list.sort()
            for index in range(len(data_list)):
                xDate.append(plist[index][1])
                populars_list.append(plist[index][0])
            xDate.append(plist[0][1])
            populars_list.append(plist[0][0])
        else:
            for index in range(len(plist)):
                xDate.append(plist[index][1])
                populars_list.append(plist[index][0])
        result = {}
        result["status"] = 0
        result["message"] = "获取数据成功"
        result["xDate"] = xDate
        result["populars"] = populars_list
        self.finish(result)