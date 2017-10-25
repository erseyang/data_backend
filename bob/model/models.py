# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String, Text, text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class TAreaInfo(Base):
    __tablename__ = 't_area_info'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer)
    name = Column(String(45))
    type = Column(Integer)


class TComment(Base):
    __tablename__ = 't_comments'

    id = Column(Integer, primary_key=True)
    shop_id = Column(String(100))
    product_id = Column(String(100))
    comment = Column(String(2000))
    comment_type = Column(String(45))
    comment_time = Column(DateTime)


class TImage(Base):
    __tablename__ = 't_image'

    id = Column(Integer, primary_key=True)
    image_url = Column(String(200))
    image_url_1 = Column(String(200))
    create_time = Column(DateTime)


class TImageRela(Base):
    __tablename__ = 't_image_rela'

    id = Column(Integer, primary_key=True)
    image_id = Column(Integer)
    rela_id = Column(String(200))
    type = Column(Integer)


class TMarkProduct(Base):
    __tablename__ = 't_mark_product'

    id = Column(Integer, primary_key=True)
    product_id = Column(String(45))
    shop_id = Column(String(45))
    type = Column(Integer)
    product_name = Column(String(200))
    mark_status = Column(Integer, server_default=text("'0'"))
    mark_time = Column(DateTime)


class TMarkShop(Base):
    __tablename__ = 't_mark_shop'

    id = Column(Integer, primary_key=True)
    shop_id = Column(String(100))
    shop_name = Column(String(200))
    mark_time = Column(DateTime)
    status = Column(Integer, server_default=text("'0'"))
    area_id = Column(String(45))
    shop_status = Column(Integer)
    shop_type = Column(Integer)


class TOpraLog(Base):
    __tablename__ = 't_opra_log'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    opra_name = Column(String(45))
    create_time = Column(DateTime)


class TProduct(Base):
    __tablename__ = 't_product'

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer)
    product_id = Column(String(100))
    product_url = Column(String(1000))
    product_name = Column(String(200))
    create_time = Column(DateTime)
    shop_id = Column(String(200))
    current_price = Column(String(100))
    pdocut_details = Column(Text)
    product_desc = Column(String(5000))
    product_sales_count = Column(Integer)
    product_stock = Column(Integer)
    type = Column(Integer)
    product_comments = Column(Integer)
    good_comments = Column(Integer)
    mid_comments = Column(Integer)
    bad_comments = Column(Integer)
    product_collections = Column(Integer)
    product_fukuan = Column(Integer)
    original_price = Column(String(100))
    status = Column(Integer, server_default=text("'0'"))
    tag_comments = Column(String(5000), server_default=text("''"))


class TRole(Base):
    __tablename__ = 't_role'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    code = Column(String(10))
    create_time = Column(DateTime)


class TShop(Base):
    __tablename__ = 't_shop'

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer)
    shop_id = Column(String(100))
    shop_name = Column(String(200))
    shop_url = Column(String(200))
    shop_type = Column(Integer)
    shop_collections = Column(Integer)
    shop_area = Column(String(50))
    shop_boss_tb = Column(String(100))
    shop_level = Column(Integer)
    shop_desc_count = Column(String(10))
    shop_service_count = Column(String(10))
    shop_logis_count = Column(String(10))
    shop_desc_compare = Column(String(45))
    shop_service_compare = Column(String(45))
    shop_logis_compare = Column(String(45))
    shop_time = Column(String(10))
    shop_gszz = Column(Text)
    create_time = Column(DateTime)
    shop_key = Column(String(1000))
    month_tuikuan_value = Column(String(45))
    month_average_value = Column(String(45))
    month_auto_end = Column(String(45))
    month_auto_average_value = Column(String(45))
    month_dispute_value = Column(String(45))
    month_dispute_average_value = Column(String(45))
    month_punish_value = Column(String(45))
    month_punish_average_value = Column(String(45))
    shop_main_business = Column(String(100))
    shop_product_satis_value = Column(String(45))
    product_statis_average_value = Column(String(45))
    product_desc_statis_value = Column(String(45))
    product_desc_average_value = Column(String(45))
    return_value = Column(String(45))
    return_average_value = Column(String(45))
    response_time = Column(String(45), server_default=text("''"))
    response_rate = Column(String(45), server_default=text("''"))


class TTask(Base):
    __tablename__ = 't_task'

    id = Column(Integer, primary_key=True)
    task_name = Column(String(100))
    task_id = Column(String(45))
    task_url = Column(String(200))
    task_key = Column(String(200))
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    task_status = Column(Integer)
    task_type = Column(Integer)
    task_num = Column(Integer)
    start_time = Column(DateTime)
    is_open = Column(Integer)
    created_id = Column(Integer)
    updated_id = Column(Integer)
    parent_id = Column(Integer)
    is_comments = Column(Integer)

class TTaskType(Base):
    __tablename__ = 't_task_type'

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer)
    task_type = Column(Integer)


class TUser(Base):
    __tablename__ = 't_user'

    id = Column(Integer, primary_key=True)
    user_name = Column(String(100))
    mobile = Column(String(45))
    password = Column(String(200))
    real_name = Column(String(45))
    create_time = Column(DateTime)
    role_id = Column(Integer)
