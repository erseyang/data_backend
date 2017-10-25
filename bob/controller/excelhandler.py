#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: eric.yang
@contact: erseyang@gmail.com
@site: http://www.lizit.net
@desc: 生成 excel文件
@file: excelhandler.py
@time: 17/4/18 下午9:21
"""
import StringIO
import datetime
import xlwt
from bob.core.basehandler import AccessHandler, BaseHandler
from bob.model.product import ProductDao
from bob.model.shop import ShopDao


class ShopExportHandler(BaseHandler):
    def initialize(self):
        self.shopDao = ShopDao()

    def get(self, *args, **kwargs):
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
        pageSize = page * pageSize
        page = 1
        shopList = self.shopDao.select_shop_list_all(shopName, shopArea, shopType, shopMark, minLevel, maxLevel, taskId)
        workbook = xlwt.Workbook(encoding = 'utf-8')
        font = xlwt.Font()
        font.name = 'SimSu'
        sheet = workbook.add_sheet('导出数据')
        sheet.write(0, 0, '店铺名')
        sheet.write(0, 1, '店铺url')
        sheet.write(0, 2, '淘宝号')
        sheet.write(0, 3, '所在地')
        sheet.write(0, 4, '淘宝分数')
        # sheet.write(0, 5, '好评')
        # sheet.write(0, 6, '中差评')
        # sheet.write(0, 6, '销量')
        row = 1
        for shop_data in shopList:
            midc = 0
            bc = 0
            sheet.write(row, 0, shop_data.shop_name)
            sheet.write(row, 1, shop_data.shop_url)
            sheet.write(row, 2, shop_data.shop_boss_tb)
            sheet.write(row, 3, shop_data.shop_area)
            sheet.write(row, 4, shop_data.shop_level)
            # sheet.write(row, 5, shop_data.good_comments)
            # sheet.write(row, 6, mb)
            # sheet.write(row, 6, shop_data.product_sales_count)
            row += 1
        self.set_header('Content-Type', 'application/x-xls')
        filename = datetime.datetime.now().strftime("%Y-%m-%d") + ".xls"
        self.set_header('Content-Disposition', 'attachment; filename='+ filename +'')
        sio = StringIO.StringIO()
        workbook.save(sio)
        self.write(sio.getvalue())
        self.finish()

class ProductExportHandler(BaseHandler):
    def initialize(self):
        self.productDao = ProductDao()

    def get(self, *args, **kwargs):
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
        if taskId is None or taskId == 'null':
            taskId = ''
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
        if page is not None:
            page = int(page)
        else:
            page = 1
        if pageSize is not None:
            pageSize = int(pageSize)
        else:
            pageSize = 20
        pageSize = page * pageSize
        results = self.productDao.get_product_list_and_shop_all(
            taskId, productName, minPrice, maxPrice, minComments,
            maxComments, minSales, maxSales, shopName, shopArea, shopType)
        workbook = xlwt.Workbook(encoding = 'utf-8')
        font = xlwt.Font()
        font.name = 'SimSu'
        sheet = workbook.add_sheet('导出产品数据')
        sheet.write(0, 0, '淘宝旺旺')
        sheet.write(0, 1, '产品名')
        sheet.write(0, 2, '产品链接')
        sheet.write(0, 3, '店铺名称')
        sheet.write(0, 4, '店铺链接')
        sheet.write(0, 5, '价格')
        sheet.write(0, 6, '销量')
        sheet.write(0, 7, '库存')
        sheet.write(0, 8, '所在地')
        row = 1
        for data in results:
            sheet.write(row, 0, data.shop_boss_tb)
            sheet.write(row, 1, data.product_name)
            sheet.write(row, 2, data.product_url)
            sheet.write(row, 3, data.shop_name)
            sheet.write(row, 4, data.shop_url)
            sheet.write(row, 5, data.current_price)
            sheet.write(row, 6, data.product_sales_count)
            sheet.write(row, 7, data.product_stock)
            sheet.write(row, 8, data.shop_area)
            row += 1
        self.set_header('Content-Type', 'application/x-xls')
        filename = datetime.datetime.now().strftime("%Y-%m-%d") + ".xls"
        self.set_header('Content-Disposition', 'attachment; filename='+ filename +'')
        sio = StringIO.StringIO()
        workbook.save(sio)
        self.write(sio.getvalue())
        self.finish()