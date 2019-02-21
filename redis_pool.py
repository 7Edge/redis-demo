#!/usr/bin/env python
# coding=UTF-8
# author: zhangjiaqi <1399622866@qq.com>
# File: redis_pool
# Date: 2/21/2019

import redis

rpool = redis.ConnectionPool(host='127.0.0.1', port='6379', max_connections=1000)
