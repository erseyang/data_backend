#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: eric.yang
@contact: erseyang@gmail.com
@site: http://www.lizit.net
@software: PyCharm
@desc:标注商家
@time: 17/3/7 下午8:04
"""
from bob.core.db import Session
from bob.model.models import TMarkShop


class MarkShopDao():
    def __init__(self):
        self.session = Session()
    ##添加标注商家
    def add_mark(self, shopId, shopName, status, area_id, shop_type):
        markshop = TMarkShop()
        markshop.shop_id = shopId
        markshop.status = status
        markshop.area_id = area_id
        markshop.shop_name = shopName
        markshop.shop_type = shop_type
        self.session.add(markshop)
        self.session.commit()
        self.session.refresh(markshop)
        return markshop.id
    ##更新状态
    def update_mark_status(self, shopId, status):
        self.session.query(TMarkShop).filter(TMarkShop.shop_id == shopId).\
            update({"status": status}, synchronize_session=False)
        self.session.commit()

