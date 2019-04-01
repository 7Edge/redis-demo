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

# 判定key是否存在,放回存在的key的个数，如果只是test一个key，那么存在返回1, 不存在返回0；如果多个，这是多个中存在的。
print(conn.exists('k1'))  # 可以检查多个key是否存在，conn.exists('k1', 'k2')
# 判断多个存在可以通过len(keys) == conn.exists(*keys) 判定是否都存在

# 设置key的有效期
conn.set('k120', 20, ex=5)  # ex设置有效时长单位是秒， px设置有效时长，单位是毫秒
print(conn.get('k120'))

# 获取所有key
conn.set('k130', 40)
print(conn.keys())
print(conn.keys(pattern='k*'))

# 模糊匹配key，得到获取key的生成器
for k in conn.scan_iter('k*'):
    print(k)

# 删除一个key
conn.delete('k120')

# 清空所有的key，禁止且慎重使用，做了解
conn.flushall()

if __name__ == '__main__':
    pass
