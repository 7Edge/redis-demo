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
# 首先原生multi/exec和pipeline区别和redis script：
#                                 a) multi是将命令即刻发送给redis server的queued中，每条命令都会有一次RTT，
#                                 执行exec给redis server再一口气执行queued中的指令。但是这时事务的。
#                                 b)而pipeline是再client端本地queued起来，执行时一次性发送给服务端，只有一次通信开销，但是不是事务，
#                                 执行会返回一个列表，代表每个命令的执行状态。
#                                 c) redis script虽然也是事务的，是比较老的支持方式，和现在MULTI/EXEC具有相同效果。
# 非原生python的redis.py将multi/exec和pipeline结合在一起，也就是Pipeline中嵌套MULTI/EXEC执行。看下满源码
"""

    def execute(self, raise_on_error=True):
    "Execute all the commands in the current pipeline"
    stack = self.command_stack
    if not stack:
        return []
    if self.scripts:
        self.load_scripts()
    if self.transaction or self.explicit_transaction:  # 根据是否开启事务在pipeline中执行事务。
        execute = self._execute_transaction
    else:
        execute = self._execute_pipeline
----------------------------代码分割线--------------------------------------
    def _execute_transaction(self, connection, commands, raise_on_error):
        cmds = chain([(('MULTI', ), {})], commands, [(('EXEC', ), {})])  源码这里就说明默认开启的事务执行时添加了MULTI/EXEC的。
"""
# 这里需要说明一下：
#   Pipeline类作用只是缓冲命令，只有执行了pipeline.execute()才会一起作为原子发送到server执行行。
#   如果，pipeline开启了watch，那么pipeline以后执行的命令不会缓冲，而是立即执行，如果要开启缓冲那么要再次执行pipeline.multi()命令。
#   而且使用了watch，pipeline会绑定一个redis的连接，所以必须在watch完后进行pipeline.reset()操作，将连接返回到连接池中。

pipe = conn.pipeline(transaction=True)  # 通过transaction控制是否开启管道事务，最后通过pipe.execute()执行

pipe.set('info1', 'test1')
pipe.hset('info2', 'k1', 10)
pipe.lpush('info3', 300)
pipe.execute()

# pipeline配合watch的diamond
with conn.pipeline(transaction=True) as p2:
    while True:
        try:
            p2.watch('info1')
            current_val = p2.get('info1')  # 此时的info1获取是立即执行的。
            p2.multi()  # 又开启缓冲redis命令。
            p2.set('info5', 10)
            p2.set('info1', current_val)
            p2.execute()  # 如果抛出了WatchError，那么说明watch的可发生了变化，只需要捕获WatchError再执行一次
            break  # 退出循环
        except redis.WatchError:
            continue

# 或者
p3 = conn.pipeline(transaction=True)
while True:
    try:
        p3.watch('info1')
        current_val = p3.get('info1')  # 此时的info1获取是立即执行的。
        p3.multi()  # 又开启缓冲redis命令。
        p3.set('info5', 10)
        p3.set('info1', current_val)
        p3.execute()  # 如果抛出了WatchError，那么说明watch的可发生了变化，只需要捕获WatchError再执行一次。
        break
    except redis.WatchError:
        continue
    finally:
        p3.reset()

if __name__ == '__main__':
    pass
