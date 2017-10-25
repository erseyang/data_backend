#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: eric.yang
@contact: erseyang@gmail.com
@site: http://www.lizit.net
@desc: 用于对商家的影响
@time: 17/2/16 上午11:11
"""
from sqlalchemy import text
from bob.core.db import Session
from bob.model.models import TShop


"""
商家搜索包括以下内容:
1.商家名关键字
2.商家所在地区
3.店铺类别
4.店铺标注
5.卖家信用区间
6.创店年限
7.退款率区间
8.30天处罚数区间
"""
class ShopDao():
    def __init__(self):
        self.session = Session()

    ##搜索所有的商家
    def select_shop_list(self, page, pageSize, key, area, type, mark, minLevel, maxLevel, taskId):
        sql = "select ts.*, tp.* from t_shop as ts left join (select shop_id, sum(product_sales_count), " \
              "sum(good_comments), sum(mid_comments), sum(bad_comments) from t_product group by product_id order by create_time desc) " \
              "as tp on ts.shop_id = tp.shop_id "
        if mark is not None and mark != '':
            sql +=" left join t_mark_shop as tms on tms.shop_id = ts.shop_id and tms.status=" + mark
        sql += " where 1=1"
        if key is not None and key != '':
            sql += " and ts.shop_name like '%" + key + "%'"
        if area is not None and area != '':
            sql += " and ts.shop_area like '%" + area + "%'"
        if minLevel is not None and minLevel != '':
            sql += " and ts.shop_level >=" + str(minLevel)
        if maxLevel is not None and maxLevel != '':
            sql += " and ts.shop_level <=" + str(maxLevel)
        if type is not None and type != '':
            sql += " and ts.shop_type=" + type
        if taskId is not None and taskId != '':
            sql += " and ts.task_id=" + taskId
        sql += " group by ts.shop_id order by ts.create_time desc "
        sql += " limit " + str((page - 1) * pageSize) + ", " + str(pageSize)
        sql_text=text(sql)
        return self.session.execute(sql_text).fetchall()

    def select_shop_list_all(self, key, area, type, mark, minLevel, maxLevel, taskId):
        sql = "select ts.*, tp.* from t_shop as ts left join (select shop_id, sum(product_sales_count), " \
              "sum(good_comments), sum(mid_comments), sum(bad_comments) from t_product group by product_id order by create_time desc) " \
              "as tp on ts.shop_id = tp.shop_id "
        if mark is not None and mark != '':
            sql +=" left join t_mark_shop as tms on tms.shop_id = ts.shop_id and tms.status=" + mark
        sql += " where 1=1"
        if key is not None and key != '':
            sql += " and ts.shop_name like '%" + key + "%'"
        if area is not None and area != '':
            sql += " and ts.shop_area like '%" + area + "%'"
        if minLevel is not None and minLevel != '':
            sql += " and ts.shop_level >=" + str(minLevel)
        if maxLevel is not None and maxLevel != '':
            sql += " and ts.shop_level <=" + str(maxLevel)
        if type is not None and type != '':
            sql += " and ts.shop_type=" + type
        if taskId is not None and taskId != '':
            sql += " and ts.task_id=" + taskId
        sql += " group by ts.shop_id order by ts.create_time desc "
        sql_text=text(sql)
        return self.session.execute(sql_text).fetchall()

    ##搜索商家的总数
    def select_shop_list_count(self, key, area, type, mark, minLevel, maxLevel, taskId):
        sql = "select count(DISTINCT ts.shop_id) from t_shop as ts where 1=1"
        if key is not None and key != '':
            sql += " and ts.shop_name like '%" + key + "%'"
        if area is not None and area != '':
            sql += " and ts.shop_area like '%" + area + "%'"
        if minLevel is not None and minLevel != '':
            sql += " and ts.shop_level >=" + minLevel
        if maxLevel is not None and maxLevel != '':
            sql += " and ts.shop_level <=" + maxLevel
        if type is not None and type != '':
            sql += " and ts.shop_type=" + type
        if taskId is not None and taskId != '':
            sql += " and ts.task_id=" + taskId
        sql_text=text(sql)
        return self.session.execute(sql_text).fetchall()[0]
    ##搜索商家最后一条信息
    def select_shop_last_data_by_id(self, shopId):
        return self.session.query(TShop).filter(TShop.shop_id == shopId).order_by(TShop.create_time.desc()).first()

    ##平台总共多少商家
    def select_all_shop_count(self):
        return self.session.query(TShop).distinct(TShop.shop_id).count()
    ##根据任务ID查询所有商家
    def select_all_shop_by_task_id(self, taskId):
        return self.session.query(TShop.shop_id).\
            filter(TShop.task_id == taskId).distinct().count()
    ##销售排名
    def get_sales_ranking_by_task_id(self, taskId):
        sql_text = text('select ts.shop_id, ts.shop_name, ts.shop_url, tp.product_sales_count from t_shop as ts left join t_product '
                        'as tp on ts.shop_id = tp.shop_id where ts.task_id = :taskId group by ts.shop_id '
                        'order by tp.product_sales_count desc limit 10')
        args = {"taskId": taskId}
        return self.session.execute(sql_text, args).fetchall()
    ##信用排名
    def get_shop_level_by_task_id(self, taskId):
        sql_text = text('select ts.shop_id, ts.shop_name, ts.shop_url, ts.shop_level from t_shop as ts where ts.task_id = :taskId '
                        'group by ts.shop_id order by ts.shop_level desc limit 10')
        args = {"taskId": taskId}
        return self.session.execute(sql_text, args).fetchall()
    ##中差评排名
    def get_comments_by_task_id(self, taskId):
        sql_text = text('select ts.shop_id, ts.shop_name, ts.shop_url, (tp.mid_comments + tp.bad_comments) as md from t_shop as '
                        'ts left join t_product as tp on tp.shop_id = ts.shop_id where ts.task_id = :taskId '
                        'group by ts.shop_id order by (tp.mid_comments + tp.bad_comments) desc limit 10')
        args = {"taskId": taskId}
        return self.session.execute(sql_text, args).fetchall()
    ##服务情况变化
    def get_service_vary_by_shop_id(self, shopId):
        sql_text = text('select DATE_FORMAT(ts.create_time,"%Y%m%d") as shop_date, ts.month_tuikuan_value, ts.month_auto_end, '
                        'ts.month_dispute_value, ts.month_punish_value'
                        ' from t_shop as ts where ts.shop_id =:shopId group by ts.shop_id order by ts.create_time desc')
        args = {"shopId": shopId}
        return self.session.execute(sql_text, args).fetchall()
    #动态评分
    def get_comments_vary_by_shop_id(self, shopId):
        sql_text = text('select DATE_FORMAT(ts.create_time,"%Y%m%d") as shop_date, ts.shop_desc_count, '
                        'ts.shop_service_count, ts.shop_logis_count from t_shop as ts where ts.shop_id =:shopId '
                        'group by ts.shop_id order by ts.create_time desc')
        args = {"shopId": shopId}
        return self.session.execute(sql_text, args).fetchall()




# shopDao = ShopDao()
# print shopDao.select_shop_list(1, 20, None, None, None, None, None)