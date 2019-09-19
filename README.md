# redis-demo
https://github.com/andymccurdy/redis-py 模块常用操作记录

# 安装
pipenv install -r requirements.txt

# 运行
pipevn run python redis_operation.py
or
pipenv shell
python redis_operation.py

# 删除pipenv创建的虚拟环境
pipenv --rm

# 更新日志
1. Date: 8/26/2019 增加flask应用的redis连接池模块：redispool.py。具体使用查看redispool中说明。
2. Date: 9/19/2019 新增对pipeline中事务结合的源码理解以及watch命令和pipeline结合使用。