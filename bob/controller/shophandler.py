#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: eric.yang
@contact: erseyang@gmail.com
@site: http://www.lizit.net
@software: PyCharm
@file: shophandler.py
@time: 17/3/15 下午6:24
"""
import random
from bob.core.basehandler import AccessHandler
from bob.core.db import sqla_engine
from bob.model.models import TShop
from bob.model.product import ProductDao
from bob.model.shop import ShopDao
from bob.util.jsonutils import model_object_to_json, shop_list_with_data_to_dict, shop_list_to_json
import pandas as pd


class ShopAddMarkHandler(AccessHandler):
    def initialize(self):
        self.shopDao = ShopDao()

    def post(self, *args, **kwargs):
        return


class ShopListHandler(AccessHandler):
    def initialize(self):
        self.shopDao = ShopDao()

    def post(self, *args, **kwargs):
        shopName = self.get_args("shopName")
        shopArea = self.get_args("shopArea")
        shopType = self.get_args("shopType")
        shopMark = self.get_args("shopMark")
        minLevel = self.get_args("minLevel")
        maxLevel = self.get_args("maxLevel")
        page = self.get_args("page")
        pageSize = self.get_args("pageSize")
        taskId = self.get_args("taskId")
        if page is not None:
            page = int(page)
        else:
            page = 1
        if pageSize is not None:
            pageSize = int(pageSize)
        else:
            pageSize = 20
        shopList = self.shopDao.select_shop_list(page,
                                                 pageSize, shopName, shopArea, shopType, shopMark, minLevel, maxLevel, taskId)
        shopCount = self.shopDao.select_shop_list_count(shopName,
                                                        shopArea, shopType, shopMark,  minLevel, maxLevel, taskId)
        shopList = shop_list_with_data_to_dict(shopList)
        pagination = {}
        pagination["current_page"] = page
        pagination["size"] = shopCount[0]
        lastPage = (shopCount[0] + pageSize - 1) / pageSize;
        pagination["last_page"] = lastPage
        pagination["pageSize"] = pageSize
        result = {}
        result["status"] = 0
        result["message"] = "获取数据成功"
        result["shops"] = shopList
        result["pagination"] = pagination
        self.finish(result)


# #店家详情
class ShopDetailsHandler(AccessHandler):
    def initialize(self):
        self.shopDao = ShopDao()

    def post(self, *args, **kwargs):
        shopId = self.get_args("shop_id")
        shop = self.shopDao.select_shop_last_data_by_id(shopId)
        shop = model_object_to_json(shop)
        result = {}
        result["status"] = 0
        result["message"] = "获取数据成功"
        result["shop"] = shop
        self.finish(result)


# # 店家详情数据
class ShopDataHandler(AccessHandler):
    def initialize(self):
        self.productDao = ProductDao()

    def post(self, *args, **kwargs):
        shopId = self.get_args("shop_id")
        productsCount = self.productDao.get_products_count_by_shop_id(shopId)
        productSales = self.productDao.get_all_sales_by_shop_id(shopId)
        comments = self.productDao.get_comments_count_by_shop_id(shopId)
        if comments is None or comments == '':
            gc = 0
            mdc = 0
        else:
            gc = comments[0]
            mdc = comments[1]
        if productsCount is None or productsCount == '':
            productsCount = 0
        if productSales is None or productSales == '':
            productSales = 0
        else:
            productSales = productSales[0]
        result = {}
        result["status"] = 0
        result["message"] = "获取数据成功"
        result["productsCount"] = str(productsCount)
        result["productSales"] = str(productSales)
        result["gccomments"] = str(gc)
        result["mdcomments"] = str(mdc)
        self.finish(result)


##店铺服务情况
class ShopServiceHandler(AccessHandler):
    def initialize(self):
        self.shopDao = ShopDao()

    def post(self, *args, **kwargs):
        shopId = self.get_args("shop_id")
        service = self.shopDao.get_service_vary_by_shop_id(shopId)
        ##时间
        xDate = []
        ##退款
        tuikuan = []
        ##自主结算
        auto_end = []
        ##纠纷率
        dispute = []
        ##处罚率
        punish = []
        slist = list(service)
        length = slist.__len__()
        if length > 0 and length <= 1:
            slist.append(slist[0])
            xDate.append(slist[0][0])
            xDate.append(slist[0][0])
            tuikuan.append(slist[0][1])
            tuikuan.append(slist[0][1])
            auto_end.append(slist[0][2])
            auto_end.append(slist[0][2])
            dispute.append(slist[0][3])
            dispute.append(slist[0][3])
            punish.append(slist[0][4])
            punish.append(slist[0][4])
        elif length > 6:
            xDate.append(slist[length - 1][0])
            tuikuan.append(slist[length - 1][1])
            auto_end.append(slist[length - 1][2])
            dispute.append(slist[length - 1][3])
            punish.append(slist[length - 1][4])
            data_list = slist
            data_list = data_list.pop(length - 1)
            data_list = data_list.pop(0)
            data_list = random.sample(data_list, 4)
            data_list.sort()
            for index in range(len(data_list)):
                xDate.append(slist[index][0])
                tuikuan.append(slist[index][1])
                auto_end.append(slist[index][2])
                dispute.append(slist[index][3])
                punish.append(slist[index][4])
            xDate.append(slist[0][0])
            tuikuan.append(slist[0][1])
            auto_end.append(slist[0][2])
            dispute.append(slist[0][3])
            punish.append(slist[0][4])
        else:
            for index in range(len(slist)):
                xDate.append(slist[index][0])
                tuikuan.append(slist[index][1])
                auto_end.append(slist[index][2])
                dispute.append(slist[index][3])
                punish.append(slist[index][4])
        result = {}
        result["status"] = 0
        result["message"] = "获取数据成功"
        result["xDate"] = xDate
        result["tuikuan"] = tuikuan
        result["auto_end"] = auto_end
        result["dispute"] = dispute
        result["punish"] = punish
        self.finish(result)


##动态评分
class ShopScoreHandler(AccessHandler):
    def initialize(self):
        self.shopDao = ShopDao()

    def post(self, *args, **kwargs):
        shopId = self.get_args("shop_id")
        scores = self.shopDao.get_comments_vary_by_shop_id(shopId)
        xDate=[]
        ##描述
        shop_desc = []
        ##服务
        shop_service = []
        ##物流
        shop_logis = []
        slist = list(scores)
        length = slist.__len__()
        if length > 0 and length <= 1:
            slist.append(slist[0])
            xDate.append(slist[0][0])
            xDate.append(slist[0][0])
            shop_desc.append(slist[0][1])
            shop_desc.append(slist[0][1])
            shop_service.append(slist[0][2])
            shop_service.append(slist[0][2])
            shop_logis.append(slist[0][3])
            shop_logis.append(slist[0][3])
        elif length > 6:
            xDate.append(slist[length - 1][0])
            shop_desc.append(slist[length - 1][1])
            shop_service.append(slist[length - 1][2])
            shop_logis.append(slist[length - 1][3])
            data_list = slist
            data_list = data_list.pop(length - 1)
            data_list = data_list.pop(0)
            data_list = random.sample(data_list, 4)
            data_list.sort()
            for index in range(len(data_list)):
                xDate.append(slist[index][0])
                shop_desc.append(slist[index][1])
                shop_service.append(slist[index][2])
                shop_logis.append(slist[index][3])
            xDate.append(slist[0][0])
            shop_desc.append(slist[0][1])
            shop_service.append(slist[0][2])
            shop_logis.append(slist[0][3])
        else:
            for index in range(len(slist)):
                xDate.append(slist[index][0])
                shop_desc.append(slist[index][1])
                shop_service.append(slist[index][2])
                shop_logis.append(slist[index][3])
        result = {}
        result["status"] = 0
        result["message"] = "获取数据成功"
        result["xDate"] = xDate
        result["shop_desc"] = shop_desc
        result["shop_service"] = shop_service
        result["shop_logis"] = shop_logis
        self.finish(result)

class ShopProductListHandler(AccessHandler):
    def initialize(self):
        self.productDao = ProductDao()

    def post(self, *args, **kwargs):
        shopId = self.get_args("shop_id")
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
        products = self.productDao.get_products_by_shop_id(shopId, page, pageSize)
        products = shop_list_to_json(products)
        productCount = self.productDao.get_products_count_by_shop_id(shopId)
        result = {}
        result["status"] = 0
        result["message"] = "获取数据成功"
        result["products"] = products
        pagination = {}
        pagination["current_page"] = page
        pagination["size"] = productCount
        lastPage = (productCount + pageSize - 1) / pageSize;
        pagination["last_page"] = lastPage
        result["pagination"] = pagination
        pagination["pageSize"] = pageSize
        self.finish(result)

class ShopMarkHandler(AccessHandler):
    def initialize(self):
        self.shopDao = ShopDao()

    def post(self, *args, **kwargs):
        shopId = self.get_args("shop_id")
        status = self.get_args("status")

