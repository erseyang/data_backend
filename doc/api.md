##需求

####4.分析各商家出月销量排名，信用排名。
* 1.月销量：根据任务ID搜索出商家，并根据商家shop_id,来预估商家的商品大概月销量，并进行排名。
* 2.信用排名：根据任务ID搜索出商家，并根据商家的Level数据进行排名。直接用字段shop_level排序就行。

####5.分析价格空间分布，商户等级分布。
* 1.格空间分布：根据某个任务ID,分析出这个任务的所有商品的价格空间分布，其中x轴显示6个梯队的价格，y轴显示6个梯队数量。
* 2.商户等级分布：根据某个任务ID，分析这个任务的所有商家的shop_level并分析出进行统计，比如，绿钻有多少家，占比多少。
* ~~3.商品数量地区分析：根据某个任务ID，分析所有商家的区域，并进行统计。~~

####6.分析商家服务情况变化，动态评分比。
* 1.服务情况变化：商家服务情况变化:根据商家的历史数据，统计商家的退款速度，退款率，纠纷率，处罚数数量。
* 2.动态评分比：根据商家的ID，商家的历史数据，统计商家的动态评分比。

####7.分析商品的动态售价，评论变化（好中差），30天销量，人气变化。
* 1.中差评比排名:根据product_id，搜索出中差评点整个评论的比例，并根据日期进行统计，x轴显示日期，y轴显示中差评比。
* 2.30天销量：根据商家的shop_id，搜索该商家历史数据，统计商家的30天销量变化，x轴显示时间，y轴显示销量。
* ~~3.人气变化：暂时没有数据统计，这个等我和客户沟通了再说。~~


##接口
####月销量接口
```
curl -XPOST 'http://127.0.0.1:8080/shop/month/sales' -d ' 
{
    "task_id": 3
}'
```
```
{
  "status":200,
  "data":{}
}
```

####信用排名接口
```
curl -XPOST 'http://127.0.0.1:8080/shop/credit' -d ' 
{
    "task_id": 3
}'
```
```
{
  "status":200,
  "data":{}
}
```

####价格空间分布接口
```
curl -XPOST 'http://127.0.0.1:8080/product/price' -d ' 
{
    "task_id": 3
}'
```
```
{
  "status":200,
  "data":{}
}
```

####商户等级分布接口
```
curl -XPOST 'http://127.0.0.1:8080/shop/level' -d ' 
{
    "task_id": 3
}'
```
```
{
  "status":200,
  "data":{}
}
```

####服务情况变化接口
```
curl -XPOST 'http://127.0.0.1:8080/shop/service' -d ' 
{
    "shop_id": 3
}'
```
```
{
  "status":200,
  "data":{}
}
```

####动态评分比接口
```
curl -XPOST 'http://127.0.0.1:8080/shop/comment' -d ' 
{
    "shop_id": 3
}'
```
```
{
  "status":200,
  "data":{}
}
```

####中差评比排名接口
```
curl -XPOST 'http://127.0.0.1:8080/product/comment' -d ' 
{
    "product_id": 3
}'
```
```
{
  "status":200,
  "data":{}
}
```

####30天销量接口
```
curl -XPOST 'http://127.0.0.1:8080/shop/sales' -d ' 
{
    "shop_id": 3
}'
```
```
{
  "status":200,
  "data":{}
}
```