#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: zxc
@contact: zhangxiongcai337@gmail.com
@site: http://www.lizit.net
@file: api.py
@time: 17/3/1 上午10:52
"""
import hashlib
import json
import logging
import time

import pandas as pd
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from sqlalchemy import *
from tornado.options import define, options

define("port", default=8081, help="run on the given port", type=int)
# 允许发起请求的host列表
HOST_ACCEPT_LIST = ["127.0.0.1:4001"]
# 数据库配置
db_conn = 'mysql://bob:bobspider@114.55.151.132:3306/bob_spider?charset=utf8'


class Application(tornado.web.Application):
    def __init__(self):
        self.db = create_engine(db_conn, convert_unicode=True, encoding='utf-8', echo=True, pool_size=100)
        handlers = [
            (r"/", MainHandler),
            (r"/token-test", TestHandler),
            (r"/shop/month/sales", ShopMonthSalesHandler),  # 月销量接口
            (r"/shop/credit", ShopCreditHandler),  # 信用排名接口
            (r"/product/price", ProductPriceHandler),  # 价格空间分布接口
            (r"/shop/level", ShopLevelHandler),  # 商户等级分布接口
            (r"/shop/service", ShopServiceHandler),  # 服务情况变化接口
            (r"/shop/comment", ShopCommentHandler),  # 动态评分比接口
            (r"/product/comment", ProductCommentHandler),  # 中差评比排名接口
            (r"/shop/sales", ShopSalesHandler),  # 30天销量接口
            (r"/shop/area", ShopAreaHandler),  # 地区分布接口
        ]
        settings = {
            "debug": True,
        }
        tornado.web.Application.__init__(self, handlers, **settings)


# 基础类
class BaseHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def db_find_one(self, coll, param):
        return self.application.db[coll].find_one(param)

    def db_update(self, coll, param, data, upsert=False):
        return self.application.db[coll].update(param, {"$set": data}, upsert)


# RESTful API接口实现类
class ApiHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    # 预处理header，允许跨域
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        # self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')

    def update_access_token(self, access_account, access_type):
        secret_key = "__YOUR_KEY__"
        access_create = int(time.time())

        # 使用下面四个参数生成 new_token
        tmpArr = [secret_key, access_account, access_type, str(access_create)]
        tmpArr.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, tmpArr)
        new_token = sha1.hexdigest()

        # 向客户端返回 new_token
        self.set_header("New-Token", new_token)
        # 将新token更新到数据库
        self.db_update("user", {"account": access_account}, {"access_token": new_token, "access_create": access_create})

    def finish(self, chunk=None, info=""):
        if chunk:
            response = {"meta": {"code": 200, "info": info}, "data": chunk}
        else:
            if info is "":
                response = {"meta": {"code": 404, "info": "not found"}, "data": {}}
            else:
                response = {"meta": {"code": 403, "info": info}, "data": {}}

        callback = tornado.escape.to_basestring(self.get_argument("callback", None))
        # 兼容jsonp请求
        if callback:
            # 直接发送js代码段发起执行
            # self.set_header("Content-Type", "application/x-javascript")
            # 发送数据文本，需要前端再处理
            self.set_header("Content-Type", "text/html")
            response = "%s(%s)" % (callback, tornado.escape.json_encode(response))
        else:
            # 直接发送json
            # self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.set_header("Content-Type", "text/html")
        super(ApiHandler, self).finish(response)


# 请求权限处理类
class AccessHandler(ApiHandler):
    def prepare(self):
        # 获取请求头，并对请求头做做处理
        headers = self.request.headers
        if not self.ckeck_access_token(headers):
            # 不通过则返回禁止信息
            self.finish(chunk=None, info="access forbidden")
        else:
            return

    def ckeck_access_token(self, headers):
        # 判断host是否合法
        if "Host" in headers and headers["Host"] in HOST_ACCEPT_LIST:
            user_host = headers["Host"]
        else:
            # return False
            logging.info('Host:' + headers["Host"])
        # 判断token
        if ("Access-Type" and "Access-Token" and "Access-Account") in headers:
            access_type = headers["Access-Type"]
            access_token = headers["Access-Token"]
            access_account = headers["Access-Account"]

            logging.info(access_token)
            # 自定义字段 access_type
            if access_type == "__YOUR_TYPE__":
                # 查询数据库
                cont = self.db_find_one("user", {"account": access_account})
            else:
                return False

            if cont["access_token"] == access_token:
                # token有效期7200秒
                # 其中，在过期前10分钟有获取新token资格
                # 一旦获得新token，旧token立即废弃
                if int(time.time()) <= int(cont["access_create"]) + 7200:
                    # 如果token合法且即将过期，则更新
                    if int(time.time()) > int(cont["access_create"]) + 6600:
                        # 生成新的token
                        self.update_access_token(access_account, access_type)
                    return True
        # 执行到最后还不返回True就说明token错误
        return False


# 请求处理类
class MainHandler(ApiHandler):
    def post(self):
        res = json.dumps({k: self.get_argument(k) for k in self.request.arguments})
        self.finish(chunk=res, info="post method")


# token-test
class TestHandler(AccessHandler):
    def get(self):
        self.finish(chunk={"msg": "hello world"}, info="your access_token is valid")


# 地区分布接口
class ShopAreaHandler(ApiHandler):
    def post(self):
        task_id = self.get_argument('task_id')
        province_dic = [
            u'河北', u'山西', u'吉林', u'辽宁', u'黑龙江', u'陕西', u'甘肃', u'青海', u'山东', u'福建', u'浙江', u'台湾', u'河南', u'湖北', u'湖南',
            u'江西', u'江苏', u'安徽',
            u'广东', u'海南', u'四川', u'贵州', u'云南', u'北京', u'上海', u'天津', u'重庆', u'内蒙古', u'新疆', u'宁夏', u'广西', u'西藏', u'香港',
            u'澳门'
        ]
        result = {}
        for province in province_dic:
            query = text(
                u"select count(DISTINCT shop_id) from t_shop where task_id = " + task_id + " and  shop_area like '%" + province + u"%';")
            count = self.db.execute(query).scalar()
            result[province] = count
        self.finish(chunk=result, info="ShopAreaHandler")


# 月销量接口
class ShopMonthSalesHandler(ApiHandler):
    def post(self):
        task_id = self.get_argument('task_id')
        self.finish(chunk={}, info="ShopMonthSalesHandler")


# 信用排名接口
class ShopCreditHandler(ApiHandler):
    def post(self):
        task_id = self.get_argument('task_id')
        df = pd.read_sql_query('select * from t_shop where task_id = ' + str(task_id) + ' order by shop_level DESC',
                               self.application.db)
        res = df.to_json()
        self.finish(chunk=res, info="ShopCreditHandler")


# 价格空间分布接口
class ProductPriceHandler(ApiHandler):
    def post(self):
        task_id = self.get_argument('task_id')
        df = pd.read_sql_query(
            'select product_sales_count,cast(SUBSTRING_INDEX(current_price,"￥", -1) AS DECIMAL(10,2)) AS price from t_product  where task_id = ' + str(
                task_id),
            self.application.db)
        df['price'] = pd.cut(df['price'], 6, precision=2)
        # df['Group_sales'] = pd.cut(df['product_sales_count'], 6, precision=2)
        # df_res = df.groupby(['price', 'Group_sales']).sum()
        df_res = df.groupby(['price']).sum()
        res = df_res.head(36).to_json()
        self.finish(chunk=res, info="ProductPriceHandler")


# 商户等级分布接口
class ShopLevelHandler(ApiHandler):
    def post(self):
        task_id = self.get_argument('task_id')
        df = pd.read_sql_query(
            'select (CASE WHEN shop_level>=4 and shop_level<=250 then 1 WHEN shop_level>=251 and shop_level<=10000 then 2 WHEN shop_level>=10001 and shop_level<=500000 then 3 WHEN shop_level>=5000001 and shop_level<=10000000 then 4 WHEN shop_level>=100000001 then 5 ELSE 0 END) as star,count(id) as shop_count from t_shop where task_id =  ' + str(
                task_id) + 'group by star order by star DESC', self.application.db)
        res = df.to_json()
        self.finish(chunk=res, info="ShopLevelHandler")


# 服务情况变化接口
class ShopServiceHandler(ApiHandler):
    def post(self):
        shop_id = self.get_argument('shop_id')
        df = pd.read_sql_query(
            'select DATE_FORMAT(`create_time`, "%%Y%%m") AS date_frame,`month_tuikuan_value`,`month_dispute_value`,`month_punish_value` from t_shop where shop_id = ' + str(
                shop_id), self.application.db)
        df['date_frame'] = pd.cut(df['date_frame'], 6, precision=2)
        df_res = df.groupby(['date_frame']).sum()
        res = df_res.head(36).to_json()
        self.finish(chunk=res, info="ShopServiceHandler")

# 动态评分比接口
class ShopCommentHandler(ApiHandler):
    def post(self):
        shop_id = self.get_argument('shop_id')
        df = pd.read_sql_query(
            'select DATE_FORMAT(create_time, "%%Y%%m") as date_frame,shop_desc_count,shop_service_count,shop_logis_count from t_shop where shop_id = 108796693 ' + str(
                shop_id), self.application.db)
        res = df.to_json()
        self.finish(chunk=res, info="ShopCommentHandler")


# 中差评比排名接口
class ProductCommentHandler(ApiHandler):
    def post(self):
        product_id = self.get_argument('product_id')
        df = pd.read_sql_query(
            'select DATE_FORMAT(create_time, "%%Y%%m%%d") as date_frame,IFNULL((bad_comments+mid_comments)/product_comments,0) as not_good_comments from t_product where product_id = ' + str(
                product_id) + ' group by date_frame order by date_frame',
            self.application.db)
        res = df.to_json()
        self.finish(chunk=res, info="ProductCommentHandler")


# 30天销量接口
class ShopSalesHandler(ApiHandler):
    def post(self):
        shop_id = self.get_argument('shop_id')
        df = pd.read_sql_query(
            'select DATE_FORMAT(create_time, "%%Y%%m%%d") as date_frame,count(product_sales_count) as sales from t_product where shop_id = ' + str(
                shop_id) + ' group by date_frame order by date_frame',
            self.application.db)
        res = df.to_json()
        self.finish(chunk=res, info="ShopSalesHandler")


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
