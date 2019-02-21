#!/usr/bin/env python
# coding=UTF-8
# author: zhangjiaqi <1399622866@qq.com>
# File: user_redis_pool
# Date: 2/14/2019
# redis-py操作

import redis
from redis_pool import rpool
# 每次操作都建立一次TCP连接并关掉

# 使用redis连接池
conn = redis.Redis(connection_pool=rpool)

conn.set('foo', 'bar')

ret = conn.get('foo')

print(ret.decode('utf-8'))

conn.hset('persons', 'egon', 18)
conn.hset('persons', 'alex', 81)

ret = conn.hgetall('persons')
print(ret)

# 计数器
conn.hincrby('persons', 'egon', amount=20)
print(conn.hget('persons', 'egon'))

# 多个hash数据设置
conn.hmset('persons', {'egon': 40, 'zjqi': 28})
print(conn.hmget('persons', ['egon', 'zjqi', 'alex', 'test']))

# 使用hgetall获取全部hash数据，服务器内存可能无法承受，因为服务端收到这个命令后，回家数据都从redis再放到内存，再通过网络传输给用户。
# 可能造成
