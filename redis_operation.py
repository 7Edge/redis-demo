#!/usr/bin/env python
# coding=UTF-8
# author: zhangjiaqi <1399622866@qq.com>
# File: user_redis_pool
# Date: 2/14/2019
# redis-py操作
"""
初识redis的操作，给每个key设置后，注意对key的销毁，避免文件重复执行，影响下一次执行。
"""

import redis
from redis_pool import rpool

# 每次操作都建立一次TCP连接并关掉
r = redis.Redis(host='127.0.0.1', port='6379')
r.set('time', '2018-10-10')
r.expire('time', 7200)
print(r.get('time'))

# 使用redis连接池
# redis实例使用连接池
conn = redis.Redis(connection_pool=rpool)

conn.set('foo', 'bar')

ret = conn.get('foo')

print(ret.decode('utf-8'))

conn.hset('persons', 'egon', 18)
conn.hset('persons', 'alex', 81)

ret = conn.hgetall('persons')
print(ret)

# 计数器
conn.hincrby('persons', 'egon', amount=20)  # amount是负数这是计算减
print(conn.hget('persons', 'egon'))

# 多个hash数据设置
conn.hmset('persons', {'egon': 40, 'zjqi': 28})
print(conn.hmget('persons', ['egon', 'zjqi', 'alex', 'test']))  # 'test'没有会得到一个None

# 使用hgetall获取全部hash数据，服务器内存可能无法承受，因为服务端收到这个命令后，回家数据都从redis再放到内存，再通过网络传输给用户。
# 可能造成撑爆内存，所以使用hscan_iter得到一个生成器，迭代从redis server获取，设置count值，每次获取多少条数据。
# 原理利用游标指针cursor的概念，最开始是0，第二次就是count+1，源码中hscan_iter利用的是hscan。
# 注意迭代出来的是一个元组，实际就是类似{'1': 'a','2': 'b'}.items() 的迭代出的。
res_itr = conn.hscan_iter('persons', count=2)
for i in res_itr:
    print(i[0], i[1])

# 千万别hgetall 可能造成故障。通过hscan_iter取

# hash 里面不能key再嵌套列表或者字典，也就是只有第一层value支持列表字典。所以我们要将嵌套字典通过json序列化放入
val = {'a': 1, 'b': 2, 'c': 3}
import json

# conn.hset('k1', 'd1', val) 这样会抛出异常:
# "redis.exceptions.DataError: Invalid input of type: 'dict'. Convert to a byte, string or number first."

json_str = json.dumps(val)
conn.hset('k2', 'd2', json_str)
print(conn.hget('k2', 'd2'))



