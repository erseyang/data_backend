#!/usr/bin/env python
# encoding: utf-8
"""
@version: 1.0
@author: eric.yang
@contact: erseyang@gmail.com
@site: http://www.lizit.net
@software: PyCharm
@file: product.py
@time: 17/3/6 下午5:47
"""
from sqlalchemy import func, text
from bob.core.db import Session
from bob.model.models import TProduct

"""
首页
产品搜索:
1.产品关键字
2.价格范围
3.卖家信用
4.爬虫任务
产品信息管理搜索:
1.爬虫
2.商品名关键字
3.评论数区间
4.商品标注
5.售价区间
6.月销量
7.店铺名
8.店铺所在地关键字
9.卖家信用区间
10.店铺标注
11.店铺类型 天猫 淘宝 阿里巴巴中文 阿里巴巴英文
"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class ProductDao():
    def __init__(self):
        self.session = Session()

    # #获取所有的商品数量
    def get_all_product(self):
        return self.session.query(TProduct).distinct(TProduct.product_id).count()

    # #任务ID查询商品总数
    def get_all_products_by_taskid(self, taskId):
        return self.session.query(TProduct.product_id).filter(TProduct.task_id == taskId). \
            distinct().count()

    ##总的销量
    def get_sales_count_by_taskid(self, taskId):
        sql_text = text('select sum(product_sales_count) from t_product where ' \
                        'task_id = :taskId and status = 0')
        args = {"taskId": taskId}
        sales = self.session.execute(sql_text, args).first()[0]
        return int(sales)

    ##均价
    def get_mid_price_by_taskid(self, taskId):
        sql_text = text('select AVG(current_price) from t_product where task_id = :taskId and status = 0'
                        '')
        args = {"taskId": taskId}
        price = self.session.execute(sql_text, args).first()
        print price
        return "%.2f" % price[0]

    ##商店商品总数
    def get_products_count_by_shop_id(self, shopId):
        return self.session.query(TProduct.product_id).filter(TProduct.shop_id == shopId).distinct().count()

    ##总销量
    def get_all_sales_by_shop_id(self, shopId):
        sql_text = ('select sum(product_sales_count) from t_product where shop_id = :shopId and status = 0'
                    'group by `product_id` order by create_time desc')
        args = {"shopId": shopId}
        return self.session.execute(sql_text, args).first()

    ##评论数
    def get_comments_count_by_shop_id(self, shopId):
        sql_text = 'select sum(good_comments) as gc, sum(mid_comments + bad_comments) as mdc from t_product ' \
                   'where shop_id = :shopId group by `product_id` order by create_time desc '
        args = {"shopId": shopId}
        return self.session.execute(sql_text, args).first()

    ##查询该shop下所有的商品信息
    def get_products_by_shop_id(self, shopId, page, pageSize):
        return self.session.query(TProduct).group_by(TProduct.product_id). \
            filter(TProduct.shop_id == shopId).order_by(TProduct.create_time.desc()) \
            .offset((page - 1) * pageSize).limit(pageSize)

    ## 查询该shop下的所有商品
    def get_products_count_by_shop_id(self, shopId):
        return self.session.query(TProduct).group_by(TProduct.product_id).filter(TProduct.shop_id == shopId).count()

    ## 搜索商品信息
    def get_product_list_and_shop(self, taskId, productName, minPrice, maxPrice,
                                  minComments, maxComments, minSales, maxSales,
                                  shopName, shopArea, shopType, page, pageSize):
        sql_text = "select tp.product_id, tp.product_name, tp.product_sales_count," \
                   "tp.current_price, tp.product_comments, tp.good_comments, tp.mid_comments, tp.bad_comments," \
                   "tp.product_url, ts.shop_id, ts.shop_name, ts.shop_level, ts.shop_area, ts.shop_url " \
                   "from t_product as tp left join t_shop as ts on tp.shop_id = ts.shop_id where 1 = 1 and tp.shop_id <> '' and tp.status = 0"
        if taskId is not None and taskId != "":
            sql_text += " and tp.task_id=" + taskId
        if productName is not None and productName != "":
            sql_text += " and tp.product_name like '%" + productName + "%'"
        if minPrice is not None and minPrice != "":
            sql_text += " and tp.current_price >=" + str(minPrice)
        if maxPrice is not None and maxPrice != "":
            sql_text += " and tp.current_price <=" + str(maxPrice)
        if minComments is not None and minComments != "":
            sql_text += " and tp.product_comments >=" + str(minComments)
        if maxComments is not None and maxComments != "":
            sql_text += " and tp.product_comments <=" + str(maxComments)
        if minSales is not None and minSales != "":
            sql_text += " and tp.product_sales_count >=" + str(minSales)
        if maxSales is not None and maxSales != "":
            sql_text += " and tp.product_sales_count <=" + str(maxSales)
        if shopName is not None and shopName != "":
            sql_text += " and ts.shop_name like '%" + shopName + "%'"
        if shopArea is not None and shopArea != "":
            sql_text += " and ts.shop_area like '%" + shopArea + "%'"
        if shopType is not None and shopType != "":
            sql_text += " and ts.shop_type =" + shopType
        sql_text += " group by tp.product_id order by tp.create_time desc "
        sql_text += " limit " + str((page - 1) * pageSize) + ", " + str(pageSize)
        return self.session.execute(sql_text).fetchall()

    def get_product_list_and_shop_all(self, taskId, productName, minPrice, maxPrice,
                                  minComments, maxComments, minSales, maxSales,
                                  shopName, shopArea, shopType):
        sql_text = "select tp.product_id, tp.product_name, tp.product_sales_count," \
                   "tp.current_price, tp.product_stock," \
                   "tp.product_url, ts.shop_boss_tb, ts.shop_id, ts.shop_name, ts.shop_level, ts.shop_area, ts.shop_url " \
                   "from t_product as tp left join t_shop as ts on tp.shop_id = ts.shop_id where 1 = 1 and tp.shop_id <> '' and tp.status = 0"
        if taskId is not None and taskId != "":
            sql_text += " and tp.task_id=" + taskId
        if productName is not None and productName != "":
            sql_text += " and tp.product_name like '%" + productName + "%'"
        if minPrice is not None and minPrice != "":
            sql_text += " and tp.current_price >=" + str(minPrice)
        if maxPrice is not None and maxPrice != "":
            sql_text += " and tp.current_price <=" + str(maxPrice)
        if minComments is not None and minComments != "":
            sql_text += " and tp.product_comments >=" + str(minComments)
        if maxComments is not None and maxComments != "":
            sql_text += " and tp.product_comments <=" + str(maxComments)
        if minSales is not None and minSales != "":
            sql_text += " and tp.product_sales_count >=" + str(minSales)
        if maxSales is not None and maxSales != "":
            sql_text += " and tp.product_sales_count <=" + str(maxSales)
        if shopName is not None and shopName != "":
            sql_text += " and ts.shop_name like '%" + shopName + "%'"
        if shopArea is not None and shopArea != "":
            sql_text += " and ts.shop_area like '%" + shopArea + "%'"
        if shopType is not None and shopType != "":
            sql_text += " and ts.shop_type =" + shopType
        sql_text += " group by tp.product_id order by tp.create_time desc "
        return self.session.execute(sql_text).fetchall()

    ##总的数量
    def get_product_count_and_shop(self, taskId, productName, minPrice, maxPrice,
                                   minComments, maxComments, minSales, maxSales,
                                   shopName, shopArea, shopType):
        sql_text = "select count(*) from t_product as tp left join t_shop as ts on tp.shop_id = ts.shop_id where 1 = 1"
        if taskId is not None and taskId != "":
            sql_text += " and tp.task_id=" + taskId
        if productName is not None and productName != "":
            sql_text += " and tp.product_name like '%" + productName + "%'"
        if minPrice is not None and minPrice != "":
            sql_text += " and tp.current_price >=" + str(minPrice)
        if maxPrice is not None and maxPrice != "":
            sql_text += " and tp.current_price <=" + str(maxPrice)
        if minComments is not None and minComments != "":
            sql_text += " and tp.product_comments >=" + str(minComments)
        if maxComments is not None and maxComments != "":
            sql_text += " and tp.product_comments <=" + str(maxComments)
        if minSales is not None and minSales != "":
            sql_text += " and tp.product_sales_count >=" + str(minSales)
        if maxSales is not None and maxSales != "":
            sql_text += " and tp.product_sales_count <=" + str(maxSales)
        if shopName is not None and shopName != "":
            sql_text += " and ts.shop_name like '%" + shopName + "%'"
        if shopArea is not None and shopArea != "":
            sql_text += " and ts.shop_area like '%" + shopArea + "%'"
        if shopType is not None and shopType != "":
            sql_text += " and ts.shop_type =" + shopType
        sql_text += " order by tp.create_time desc "
        return self.session.execute(sql_text).first()

    ##通过ID获取最新的产品信息
    def get_product_by_id(self, productId):
        sql_text = "select tp.product_id, tp.product_url, tp.product_name, tp.current_price, tp.original_price, tp.product_sales_count, " \
                   "tp.good_comments, tp.mid_comments, tp.bad_comments,tp.product_collections, ts.shop_name,ts.shop_url, ts.shop_boss_tb, " \
                   "ts.shop_area, ts.shop_level, ts.shop_time, ts.shop_desc_count, ts.shop_service_count, " \
                   "ts.shop_logis_count, ts.month_tuikuan_value, ts.month_dispute_value, ts.month_punish_value " \
                   "from t_product as tp left join t_shop as ts on tp.shop_id = ts.shop_id" \
                   " where tp.product_id=:productId and tp.status = 0 group by tp.product_id order by tp.create_time desc"
        args = {"productId": productId}
        return self.session.execute(sql_text, args).first()

    ##价格分析
    def get_price_by_product_id(self, productId):
        sql_text = 'select tp.current_price, tp.original_price, DATE_FORMAT(tp.create_time,"%Y%m%d") ' \
                   'from t_product as tp where tp.product_id = ' + productId + ' and tp.status = 0 group by tp.create_time order by tp.create_time desc'
        return self.session.execute(sql_text).fetchall()

    ##销量变化曲线
    def get_sales_by_product_id(self, productId):
        sql_text = 'select tp.product_sales_count, DATE_FORMAT(tp.create_time,"%Y%m%d") from t_product as tp where ' \
                   'tp.product_id=:productId and tp.status = 0 group by tp.create_time order by tp.create_time desc'
        args = {"productId": productId}
        return self.session.execute(sql_text, args).fetchall()

    ##评论变化
    def get_comments_by_product_id(self, productId):
        sql_text = 'select tp.product_comments, CAST(sum(tp.mid_comments + tp.bad_comments) as SIGNED) as md, ' \
                   'DATE_FORMAT(tp.create_time,"%Y%m%d") from t_product as tp where tp.product_id=:productId and tp.status = 0 ' \
                   'group by tp.create_time order by tp.create_time desc'
        args = {"productId": productId}
        return self.session.execute(sql_text, args).fetchall()

    ##人气指数
    def get_popular_by_product_id(self, productId):
        sql_text = 'select CAST(sum(tp.product_collections + tp.product_fukuan) as SIGNED) as popular, ' \
                   'DATE_FORMAT(tp.create_time,"%Y%m%d") from t_product as tp where ' \
                   'tp.product_id=:productId and tp.status = 0 group by tp.create_time order by tp.create_time desc'
        args = {"productId": productId}
        return self.session.execute(sql_text, args).fetchall()

    def get_data_date_by_task_id(self, taskId):
        sql_text = 'select DATE_FORMAT(create_time, "%Y%m%d") from t_product as tp where tp.task_id = :taskId and tp.status = 0 ' \
                   'group by DATE_FORMAT(create_time, "%Y%m%d")'
        args = {"taskId": taskId}
        return self.session.execute(sql_text, args).fetchall()
    ##根据日期分页显示数据
    def get_data_by_date_with_taskid(self, createDate, taskId, page, pageSize):
        sql_text = text('select tp.product_id, tp.product_url, tp.product_name from t_product as tp where DATE_FORMAT(tp.create_time, "%Y%m%d") =:createDate '
                        'and tp.task_id=:taskId and tp.status = 0 order by tp.create_time limit :start_num, :end_num')
        start_num = (page - 1) * pageSize
        args = {"createDate": createDate, "taskId": taskId, "start_num": start_num, "end_num": pageSize}
        return self.session.execute(sql_text, args).fetchall()
    ##根据日期任务ID显示所有的数据
    def get_all_count_by_date_with_taskid(self, createDate, taskId):
        sql_text = text('select count(*) from t_product as tp where DATE_FORMAT(tp.create_time, "%Y%m%d") =:createDate'
                        ' and tp.task_id=:taskId and tp.status = 0')
        args = {"createDate": createDate, "taskId": taskId}
        return self.session.execute(sql_text, args).first()[0]
    ##根据任务ID和日期显示所有的数据
    def get_all_data_by_date_with_taskid(self, createDate, taskId):
        sql_text = text('select tp.product_id from t_product as tp where DATE_FORMAT(tp.create_time, "%Y%m%d") =:createDate '
                        'and tp.task_id=:taskId and tp.status = 0 order by tp.create_time')
        args = {"createDate": createDate, "taskId": taskId}
        return self.session.execute(sql_text, args).fetchall()

# productDao = ProductDao()
# print productDao.get_data_by_date_with_taskid('20170428', 67, 1, 20)
# print productDao.get_all_count_by_date_with_taskid('20170428', 67)[0]
# print len(productDao.get_data_date_by_task_id(67));
# print productDao.get_price_by_product_id('45353762204')[0][2]
# print productDao.get_sales_count_by_taskid(65)
# print productDao.get_mid_price_by_taskid(65)
# print productDao.get_comments_count_by_shop_id(36284466)
# print productDao.get_product_list_and_shop("", "", "", "", "", "", "", "", "", "", "", 1, 20)
