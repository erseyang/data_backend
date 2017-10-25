CREATE TABLE `t_shop` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` int(11) DEFAULT NULL COMMENT '任务ID',
  `shop_id` varchar(100) DEFAULT NULL COMMENT '商铺ID\\n',
  `shop_name` varchar(200) DEFAULT NULL COMMENT '商铺名称\\n',
  `shop_url` varchar(200) DEFAULT NULL COMMENT '商铺主页',
  `shop_type` int(11) DEFAULT NULL COMMENT '商家类别 1淘宝商家 2淘宝自己运营 3京东自营 4京东商家\\n5天猫\\n',
  `shop_collections` int(11) DEFAULT NULL COMMENT '收藏数量',
  `shop_area` varchar(50) DEFAULT NULL COMMENT '地理区域',
  `shop_boss_tb` varchar(100) DEFAULT NULL COMMENT '掌柜昵称\\n',
  `shop_level` int(12) DEFAULT NULL COMMENT '店铺级别\\n',
  `shop_desc_count` varchar(10) DEFAULT NULL COMMENT '描述分数',
  `shop_service_count` varchar(10) DEFAULT NULL COMMENT '服务分数',
  `shop_logis_count` varchar(10) DEFAULT NULL COMMENT '物流评分',
  `shop_desc_compare` varchar(45) DEFAULT NULL COMMENT '描述与同行相比较\\n',
  `shop_service_compare` varchar(45) DEFAULT NULL COMMENT '服务与同行相比',
  `shop_logis_compare` varchar(45) DEFAULT NULL COMMENT '物流与同行相比',
  `shop_time` varchar(10) DEFAULT NULL COMMENT '开店时长',
  `shop_gszz` text COMMENT '工商执照，一般为url地址',
  `create_time` datetime DEFAULT NULL,
  `shop_key` varchar(1000) DEFAULT NULL COMMENT '公司主营描述',
  `month_tuikuan_value` varchar(45) DEFAULT NULL COMMENT '天猫28天退款率,淘宝30天退款率 1688 是90天的数据 jd上也是90天的数据',
  `month_average_value` varchar(45) DEFAULT NULL COMMENT '退款率行业均值',
  `month_auto_end` varchar(45) DEFAULT NULL COMMENT '天猫自主完结率，淘宝的售后率',
  `month_auto_average_value` varchar(45) DEFAULT NULL COMMENT '自主完结率行业均值',
  `month_dispute_value` varchar(45) DEFAULT NULL COMMENT '30天纠纷率',
  `month_dispute_average_value` varchar(45) DEFAULT NULL COMMENT '纠纷退款率行业均值 ',
  `month_punish_value` varchar(45) DEFAULT NULL COMMENT '处罚率，针对淘宝，天猫没有',
  `month_punish_average_value` varchar(45) DEFAULT NULL COMMENT '处罚率行业均值',
  `shop_main_business` varchar(100) DEFAULT NULL COMMENT '主营，主要针对淘宝',
  `shop_product_satis_value` varchar(45) DEFAULT NULL COMMENT '商品满意度 京东',
  `product_statis_average_value` varchar(45) DEFAULT NULL COMMENT '平均值，京东',
  `product_desc_statis_value` varchar(45) DEFAULT NULL COMMENT '商品描述满意度，京东',
  `product_desc_average_value` varchar(45) DEFAULT NULL COMMENT '平均值，针对京东',
  `return_value` varchar(45) DEFAULT NULL COMMENT '退换货反修率 京东 90天的统计数据',
  `return_average_value` varchar(45) DEFAULT NULL COMMENT '行业平均值',
  `response_time` varchar(45) DEFAULT '' COMMENT '响应时间，针对阿里巴巴英文网站',
  `response_rate` varchar(45) DEFAULT '' COMMENT '响应率，针对阿里巴巴英文网站',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5311 DEFAULT CHARSET=utf8;


CREATE TABLE `t_product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` int(11) DEFAULT NULL COMMENT '任务ID',
  `product_id` varchar(100) DEFAULT NULL COMMENT '商品ID\\n',
  `product_url` varchar(1000) DEFAULT NULL COMMENT '商品的URL地址',
  `product_name` varchar(200) DEFAULT NULL COMMENT '商品名称',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `shop_id` varchar(200) DEFAULT NULL COMMENT '店铺ID',
  `current_price` varchar(100) DEFAULT NULL COMMENT '当前价格',
  `pdocut_details` text COMMENT '详情',
  `product_desc` varchar(5000) DEFAULT NULL COMMENT '产品描述',
  `product_sales_count` int(11) DEFAULT NULL COMMENT '交易数量',
  `product_stock` int(11) DEFAULT NULL COMMENT '库存',
  `type` int(11) DEFAULT NULL COMMENT '1.淘宝 2京东 3.1688',
  `product_comments` int(11) DEFAULT NULL COMMENT '评论数量\\n',
  `good_comments` int(11) DEFAULT NULL COMMENT '好评数量',
  `mid_comments` int(11) DEFAULT NULL COMMENT '中评数量',
  `bad_comments` int(11) DEFAULT NULL COMMENT '差评数量',
  `product_collections` int(11) DEFAULT NULL COMMENT '收藏数量',
  `product_fukuan` int(11) DEFAULT NULL COMMENT '付款人数',
  `original_price` varchar(100) DEFAULT NULL COMMENT '原价',
  `status` int(2) DEFAULT '0' COMMENT '商品的状态 0为正常 1为删除 2不明确',
  `tag_comments` varchar(5000) DEFAULT '' COMMENT '评论标签，针对没有具体的评论分数的商城。',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31298 DEFAULT CHARSET=utf8;


CREATE TABLE `t_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_name` varchar(100) DEFAULT NULL COMMENT '任务名称',
  `task_id` varchar(45) DEFAULT NULL COMMENT '任务ID',
  `task_url` varchar(200) DEFAULT NULL COMMENT '任务地址，可以不需要，由爬虫端来配置',
  `task_key` varchar(200) DEFAULT NULL COMMENT '任务关键字，空格分开',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `task_status` int(11) DEFAULT NULL COMMENT '任务状态 1未开始 2 执行中 3 已完成',
  `task_type` int(11) DEFAULT NULL COMMENT '1,每天爬取 2，每周爬取 3每月爬取 4一次性任务',
  `task_num` int(11) DEFAULT NULL COMMENT '需要查询的页面数',
  `start_time` datetime DEFAULT NULL COMMENT '任务开始时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;


CREATE TABLE `t_task_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` int(11) DEFAULT NULL COMMENT '任务ID\\n',
  `task_type` int(11) DEFAULT NULL COMMENT '任务类型(商品搜索：1，淘宝店铺搜索：21，天猫店铺搜索：22，京东搜索 23 阿里巴巴搜索',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;