#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: eric.yang
@contact: erseyang@gmail.com
@site: http://www.lizit.net
@file: route.py
@time: 17/2/12 下午3:58
"""
from bob.controller.datacompahandler import DataCompa, DataEndCompa
from bob.controller.excelhandler import ShopExportHandler, ProductExportHandler
from bob.controller.indexhandler import IndexDataHandler
from bob.controller.producthandler import ProductListHandler, ProductDetailsHandler, ProductPriceHandler, \
    ProductCommentsHandler, ProductSalesHandler, ProductPopularHandler
from bob.controller.shophandler import ShopListHandler, ShopDetailsHandler, ShopDataHandler, ShopServiceHandler, \
    ShopScoreHandler, ShopProductListHandler
from bob.controller.taskhandler import TaskAddHandler, TaskListHandler, TaskDetailsHandler, TaskDataHandler, \
     TaskPriceHandler, TaskRankHandler, TaskShopLevelHandler, TaskShopAreaHandler, TaskIsOpenHandler, TaskUpdateHandler
from bob.controller.userhandler import UserAddHandler, UserListHandler, UserUpdatePassword, UserDeleteHandler
from bob.core.adminhandler import LoginHandler

urls = [
    (r"/user/add", UserAddHandler, dict()),
    (r"/user/list", UserListHandler, dict()),
    (r"/user/updatePass", UserUpdatePassword, dict()),
    (r"/user/delete", UserDeleteHandler, dict()),
    (r"/login", LoginHandler, dict()),
    (r"/index_data", IndexDataHandler, dict()),
    (r"/task/add", TaskAddHandler, dict()),
    (r"/task/update", TaskUpdateHandler, dict()),
    (r"/task/open_close", TaskIsOpenHandler, dict()),
    (r"/task/list", TaskListHandler, dict()),
    (r"/task/details", TaskDetailsHandler, dict()),
    (r"/task/data", TaskDataHandler, dict()),
    (r"/task/rank", TaskRankHandler, dict()),
    (r"/task/price", TaskPriceHandler, dict()),
    (r"/task/shopLevel", TaskShopLevelHandler, dict()),
    (r"/task/shopArea", TaskShopAreaHandler, dict()),
    (r"/shop/list", ShopListHandler, dict()),
    (r"/shop/details", ShopDetailsHandler, dict()),
    (r"/shop/data", ShopDataHandler, dict()),
    (r"/shop/service", ShopServiceHandler, dict()),
    (r"/shop/score", ShopScoreHandler, dict()),
    (r"/shop/export", ShopExportHandler, dict()),
    (r"/shop/productList", ShopProductListHandler, dict()),
    (r"/product/list", ProductListHandler, dict()),
    (r"/product/details", ProductDetailsHandler, dict()),
    (r"/product/comment", ProductCommentsHandler, dict()),
    (r"/product/price", ProductPriceHandler, dict()),
    (r"/product/sales", ProductSalesHandler, dict()),
    (r"/product/popular", ProductPopularHandler, dict()),
    (r"/product/export", ProductExportHandler, dict()),
    (r"/comparison", DataCompa, dict()),
    (r"/comparison_end", DataEndCompa, dict()),
]


