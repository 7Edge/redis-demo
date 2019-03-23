#!/usr/bin/env python
# coding=UTF-8
# author: zhangjiaqi <1399622866@qq.com>
# File: redis_others
# Date: 3/22/2019
"""
redis的其他操作,包括key存在，key有效时长
只有改变了key的值的存储位置的操作才会刷新expiry， 像list，和hash的field操作都不会影响它两key的expire。
"""
import redis
from redis_pool import rpool

conn = redis.Redis(connection_pool=rpool)

# 判定key是否存在，存在返回1， 不存在返回0。
print(conn.exists('k1'))

# 设置key的有效期
conn.set('k120', 20, ex=5)  # ex设置有效时长单位是秒， px设置有效时长，单位是毫秒
print(conn.get('k120'))

if __name__ == '__main__':
    pass
