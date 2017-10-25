#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: eric.yang
@contact: erseyang@gmail.com
@site: http://www.lizit.net
@software: PyCharm
@desc:任务
@time: 17/3/6 下午4:56
"""
import datetime
from sqlalchemy import text
from bob.core.db import Session
from bob.model.models import TTask, TTaskType
from bob.util.jsonutils import model_object_to_json, type_list_to_json


class TaskDao():
    def __init__(self):
        self.session = Session()

    def add_task(self, name, keyword, type, num, start_time, user_id, url, parentId, is_comment):
        task = TTask()
        task.create_time = datetime.datetime.now()
        task.task_key = keyword
        task.task_num = num
        task.task_status = 0
        task.task_name = name
        task.task_type = type
        task.created_id = user_id
        task.updated_id = user_id
        task.update_time = datetime.datetime.now()
        task.start_time = start_time
        task.task_url = url
        task.is_open = 0
        task.parent_id = parentId
        task.is_comments = is_comment
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task.id
    def get_all_task_count(self):
        return self.session.query(TTask).distinct(TTask.task_id).count()
    ## 更新任务状态
    def update_task_status(self, taskid, status):
        self.session.query(TTask).filter(TTask.task_id == taskid).update({"task_status": status}, synchronize_session=False)
        self.session.commit()
    ##更新任务ID
    def update_task_id(self, id, taskid):
        self.session.query(TTask).filter(TTask.id == id).update({"task_id": taskid}, synchronize_session=False)
        self.session.commit()
    ##关闭或者开启任务
    def close_or_open_task(self, id, open):
        self.session.query(TTask).filter(TTask.id == id).update({"is_open": open}, synchronize_session=False)
        self.session.commit()
    ##任务列表
    def get_task_list(self, keyword, page, page_size, status):
        if status is None or status == '':
            return self.session.query(TTask).order_by(TTask.create_time.desc()).filter(TTask.task_key.like('%{0}%'.format(keyword)))\
                .filter(TTask.parent_id == 0).offset((page - 1) * page_size).limit(page_size).all()
        else:
            return self.session.query(TTask).order_by(TTask.create_time.desc()).filter(TTask.task_status == status).filter(TTask.task_key.like('%{0}%'.format(keyword)))\
                .filter(TTask.parent_id == 0).offset((page - 1) * page_size).limit(page_size).all()
    ##获取子任务
    def get_child_task_list(self, parentId, status):
        return self.session.query(TTask).filter(TTask.parent_id == parentId).all()
    ## 获取任务总的数量
    def get_task_count(self, keyword, status):
        if status is None or status == '':
            return self.session.query(TTask).filter(TTask.task_key.like('%{0}%'.format(keyword))).filter(TTask.parent_id == 0).count()
        else:
            return self.session.query(TTask).filter(TTask.task_status == status).\
                filter(TTask.task_key.like('%{0}%'.format(keyword))).filter(TTask.parent_id == 0).count()
    ##查询任务详情
    def get_task_details(self, taskId):
        return self.session.query(TTask).filter(TTask.task_id == taskId).first()
    ##价格空间分布
    def get_price_range_by_task_id(self, taskId):
        sql_text = text('select tp.current_price as price, tp.product_sales_count from t_product as tp where '
                        'tp.task_id=:taskId and tp.current_price <> "" and tp.shop_id <> ""')
        args = {"taskId": taskId}
        return self.session.execute(sql_text, args).fetchall()

class TaskTypeDao():
    def __init__(self):
        self.session = Session()

    def add_type(self, task_id, typelist):
        for type in typelist:
            taskType = TTaskType()
            taskType.task_id = task_id
            taskType.task_type = type
            self.session.add(taskType)
        self.session.commit()

    def get_task_type(self, task_id):
        return self.session.query(TTaskType).filter(TTaskType.task_id == task_id).all()

# taskDao = TaskDao()
# print taskDao.get_price_range_by_task_id(52)

# taskTypeDao = TaskTypeDao()
# taskType = taskTypeDao.get_task_type(66)
# taskType = type_list_to_json(taskType)
# types = []
# for type in taskType:
#     types.append(type["task_type"])
# print types
