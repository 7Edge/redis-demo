#!/usr/bin/env python
# coding=UTF-8
# author: zhangjiaqi <1399622866@qq.com>
# File: redispool
# Date: 8/26/2019
"""
用于Flask应用的redis连接池
    - 利用python的redis.py，执行完成后，连接会自动回收
    - 目前只支持单个redis库

Usage:
1. 使用RedisPool类，该类提供API
2. 再flask应用实例化后，进行调用init_pool(app)，初始化连接池。
3. get_value获取key值
4. get_redis_conn 从连接池中获取连接。

Flask APP中添加Redis配置：
REDIS_ADDR  redisserver的ip
REDIS_PORT  redisserver的端口
REDIS_MAX_CONNECTIONS 连接池最大连接数
REDIS_PASS  redisserver如果有密码则配置，如果没密码则不配置。
"""

import redis


class RedisPool(object):
    _global_redis_pool = None

    @staticmethod
    def init_pool(app):
        """
        初始化redis pool
        :return:
        """
        if RedisPool._global_redis_pool is not None:
            return
        redis_config_ext = dict()

        host = app.config.get('REDIS_ADDR', '127.0.0.1')
        port = app.config.get('REDIS_PORT', 6379)
        max_connections = app.config.get('REDIS_MAX_CONNECTIONS', 2)
        password = app.config.get('REDIS_PASS', None)

        if password is not None:  # 有密码配置
            redis_config_ext['password'] = password

        RedisPool._global_redis_pool = redis.ConnectionPool(host=host, port=port, max_connections=max_connections,
                                                            **redis_config_ext)

    @staticmethod
    def get_value(key):
        conn = redis.Redis(connection_pool=RedisPool._global_redis_pool)
        try:
            ret = conn.get(key)

        except Exception as e:
            # logger.error("Unexpected error occur: {}".format(e))
            # logger.error(e, exc_info=True)
            # return None
            raise e
        return ret

    @staticmethod
    def get_redis_conn():
        return redis.Redis(connection_pool=RedisPool._global_redis_pool)
