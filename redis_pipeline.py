#!/usr/bin/env python
# coding=UTF-8
# author: zhangjiaqi <1399622866@qq.com>
# File: redis_pipeline
# Date: 3/14/2019
"""
批量提交操作
支持操作事务
"""
import redis
from redis_pool import rpool

conn = redis.Redis(connection_pool=rpool)

# 取出一个conn来创建一个pipeline 管道
pipe = conn.pipeline(transaction=True)  # 通过transaction控制是否开启管道事务，最后通过pipe.execute()执行

pipe.set('info1', 'test1')
pipe.hset('info2', 'k1', 10)
pipe.lpush('info3', 300)
pipe.execute()

if __name__ == '__main__':
    pass
