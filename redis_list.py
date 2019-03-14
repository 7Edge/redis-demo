#!/usr/bin/env python
# coding=UTF-8
# author: zhangjiaqi <1399622866@qq.com>
# File: redis_list
# Date: 3/14/2019
"""
redis list 操作及自定义生成器取数据
"""
import redis
from redis_pool import rpool

conn = redis.Redis(connection_pool=rpool)

conn.delete('k10')  # 确保不存在实验的key，注意操作都在实验redis中，不要疏忽在生产中运行。
conn.delete('k11')
conn.delete('k12')

# 没有list就创建，在推入元素
conn.lpush('k10', 11)
conn.lpush('k10', 12)
conn.rpush('k11', 10)
print(conn.lrange('k10', 0, 2))

# 从头或者尾取出元素
l1 = conn.rpop('k10')  # 列表没有值后就不存在了，也就是pop取完后就没有了。
# l2 = conn.lpop('k10')
# print(l1, l2)

# 获取list的长度
print(conn.llen('k10'))

# 阻塞获取，没有了则io阻塞，导致线程hung住，但是可以设置线程io阻塞超时时间
l3 = conn.brpop(['k11', 'k10'])  # 注意，这里给了两个list获取，如果第一个阻塞，那么从第二获取。
# 将多个列表排列，按照从左到右去pop对应列表的元素，知道拿到，不然阻塞
print(conn.llen('k10'))
print('--', l3)
l4 = conn.brpop('k10', timeout=5)  # 这里程序会由于io阻塞，而hung住。kill进程即可.
print(l4, type(l4))

# 插入
conn.linsert('k10', 'BEFORE', '12', 10)  # 注意这里where: BEFORE or AFTER ，refvalue必须提供值，最后是插入的值。
print(conn.lrange('k10', 0, 1))

# 列表存在才插入
conn.lpushx('k13', 10)

# 更新指定index的值
conn.lpush('k11', 20)
conn.lset('k11', 0, 30)
print(conn.lrange('k11', 0, 100))

# 删除指定的值
conn.lrem('k11', '20', 0)  # 删除列表中所有等于20的值，第三个参数，指定删除的个数，0表示所有，1表示正向第一个，2正向两个，负数则反向

# 根据所有获取列表的值
print(conn.lindex('k11', 0))

# 从一个list取元素到另一个list
conn.rpoplpush('k11', 'k12')

# 截取，保留某个区间的值
conn.lpush('k12', 100)
conn.lpush('k12', 101)
conn.lpush('k12', 102)

print(conn.lrange('k12', 0, 100))
print(conn.ltrim('k12', 1, 2))
print(conn.lrange('k12', 0, 100))

# 创建生成器，从list中获取数据
conn.lpush('k12', 100)
conn.lpush('k12', 101)
conn.lpush('k12', 102)


def list_iter(connection, name, count=10):
    index = 0
    while True:
        data = connection.lrange(name, index, index + count - 1)
        if not data:
            return
        index += count
        print(index)
        for item in data:
            yield item


k12_iter = list_iter(conn, 'k12', count=2)

for i in k12_iter:
    print(i)


if __name__ == '__main__':
    pass
